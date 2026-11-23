"""
Reproducible experiments E1 to E8 for the final report.

    python -m plant_memory.experiments          # all experiments
    python -m plant_memory.experiments E3 E4    # a subset

Writes results/<name>.json and results/figures/<name>.png.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

from .paths import RESULTS_DIR

FIG = os.path.join(RESULTS_DIR, "figures")
SCEN_ORDER = ["kpi_rerate", "idf_bearing_upgrade", "o2_recal", "new_feedstock",
              "economizer_replacement", "drum_setpoint_retune", "sensor_decommission",
              "o2_analyzer_bias", "idf_bearing_rik"]
GREEN, AMBER, RED, BLUE, GREY, NAVY = "#15803d", "#f59e0b", "#dc2626", "#2563eb", "#9ca3af", "#16233f"


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13,
                         "legend.fontsize": 11.5, "xtick.labelsize": 11.5,
                         "ytick.labelsize": 11.5, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 170})
    return plt


def _save(name, obj):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


def _fig(plt, fig, name):
    os.makedirs(FIG, exist_ok=True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, f"{name}.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _short(s):
    return s.replace("_", " ").replace("idf ", "IDF ").replace("kpi", "KPI").replace("o2", "O2")


# ---------------------------------------------------------------------------
def e1_localisation():
    """Knowledge localisation at scale: 59 entries x 9 changes."""
    from .drift import evaluate_all
    from .mocgraph import diff_states
    from .plant_state import load_base_state
    from .simulate import SCENARIOS
    from .store import load_all
    plt = _plt()
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    null = [getattr(d.health, "value", d.health) for d in evaluate_all(entries, base)]
    grid, rows = {}, []
    tp = fp = fn = 0
    for s in SCEN_ORDER:
        after = SCENARIOS[s].apply(base)
        delta = {(r, f) for _, r, f in diff_states(base, after)}
        h = {d.entry_id: getattr(d.health, "value", d.health) for d in evaluate_all(entries, after)}
        truth = {e.id for e in entries if any((g.ref, g.aspect) in delta for g in e.groundings)}
        flagged = {k for k, v in h.items() if v != "intact"}
        tp += len(flagged & truth); fp += len(flagged - truth); fn += len(truth - flagged)
        grid[s] = h
        rows.append({"scenario": s, "flagged": len(flagged), "review": sum(v == "review" for v in h.values()),
                     "broken": sum(v == "broken" for v in h.values()),
                     "retained": 1 - len(flagged) / len(entries), "truth": len(truth)})
    N, S = len(entries), len(SCEN_ORDER)
    flagged_total = sum(r["flagged"] for r in rows)
    real = [r for r in rows if r["scenario"] != "idf_bearing_rik"]
    res = {"N": N, "scenarios": S, "null_false_positives": sum(x != "intact" for x in null),
           "precision": tp / (tp + fp) if tp + fp else 1.0, "recall": tp / (tp + fn) if tp + fn else 1.0,
           "rows": rows, "mean_retained": float(np.mean([r["retained"] for r in rows])),
           "mean_retained_real_changes": float(np.mean([r["retained"] for r in real])),
           "relearn_cost": N * S, "targeted_cost": flagged_total,
           "saving": 1 - flagged_total / (N * S)}
    _save("E1_localisation", res)
    # figure: drift matrix
    ids = [e.id for e in entries]
    code = {"intact": 0, "review": 1, "broken": 2}
    Mx = np.array([[code[grid[s][i]] for s in SCEN_ORDER] for i in ids])
    from matplotlib.colors import ListedColormap
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(Mx, aspect="auto", cmap=ListedColormap([GREEN, AMBER, RED]), vmin=0, vmax=2)
    ax.set_xticks(range(S)); ax.set_xticklabels([_short(s) for s in SCEN_ORDER], rotation=40, ha="right")
    ax.set_yticks(range(N)); ax.set_yticklabels(ids, fontsize=7.5)
    ax.set_title(f"Knowledge (rows, N = {N}) under each change: green intact, amber review, red broken")
    _fig(plt, fig, "E1_drift_matrix")
    fig, ax = plt.subplots(figsize=(10, 4.8))
    x = np.arange(S)
    kept = [r["retained"] * 100 for r in rows]
    rev = [r["review"] / N * 100 for r in rows]
    brk = [r["broken"] / N * 100 for r in rows]
    ax.bar(x, kept, color=GREEN, label="kept intact")
    ax.bar(x, rev, bottom=kept, color=AMBER, label="flagged: review")
    ax.bar(x, brk, bottom=np.add(kept, rev), color=RED, label="flagged: broken")
    ax.set_xticks(x); ax.set_xticklabels([_short(s) for s in SCEN_ORDER], rotation=35, ha="right")
    ax.set_ylabel("% of knowledge"); ax.set_ylim(0, 108)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.13), frameon=False)
    _fig(plt, fig, "E1_retention")
    return res


# ---------------------------------------------------------------------------
def e2_coverage():
    """What an MOC review must cover: knowledge-only (mid-sem) vs full graph."""
    from .impact import assess
    plt = _plt()
    rows = []
    for s in SCEN_ORDER:
        a = assess(s)
        rows.append({"scenario": s, "tier": a["risk"]["tier"], "S": a["risk"]["S"],
                     "L": a["risk"]["L"], "R": a["risk"]["R"],
                     "knowledge": len(a["knowledge"]), "procedures": len(a["procedures"]),
                     "alarms": len(a["alarms"]), "models": len(a["models"]),
                     "physical": a["n_disturbed"], "watch_knowledge": len(a["watch_knowledge"]),
                     "approvers": len(a["approvers"]), "pssr": a["pssr_required"],
                     "change_set": len(a["change_set"])})
    tot = {k: sum(r[k] for r in rows) for k in ("knowledge", "procedures", "alarms", "models", "physical")}
    res = {"rows": rows, "totals": tot,
           "items_full": sum(tot.values()), "items_knowledge_only": tot["knowledge"]}
    _save("E2_coverage", res)
    fig, ax = plt.subplots(figsize=(10.5, 5))
    x = np.arange(len(rows)); bottom = np.zeros(len(rows))
    for key, col, lab in [("knowledge", GREEN, "knowledge entries"), ("procedures", BLUE, "procedure documents"),
                          ("alarms", RED, "alarm limits"), ("models", NAVY, "models"),
                          ("physical", AMBER, "physically disturbed assets")]:
        v = np.array([r[key] for r in rows]); ax.bar(x, v, bottom=bottom, color=col, label=lab); bottom += v
    ax.set_xticks(x); ax.set_xticklabels([_short(r["scenario"]) for r in rows], rotation=35, ha="right")
    ax.set_ylabel("items the MOC review must cover")
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18), frameon=False)
    _fig(plt, fig, "E2_coverage")
    return res


# ---------------------------------------------------------------------------
def e3_propagation():
    from . import calibrate
    plt = _plt()
    r = calibrate.evaluate()
    res = {k: r[k] for k in ("predictors", "random_MAP", "alpha", "alpha_sweep_cal",
                             "n_sources", "n_relevant_pairs")}
    _save("E3_propagation", res)
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    names = list(r["predictors"])
    short = ["Same system", "Graph prior", "Data-calibrated", "Hybrid (tuned)"]
    vals = [r["predictors"][n]["MAP"] for n in names]
    axs[0].bar(short, vals, color=[GREY, BLUE, GREEN, NAVY])
    axs[0].axhline(r["random_MAP"], ls="--", color=RED, label=f"random ({r['random_MAP']:.2f})")
    for i, v in enumerate(vals):
        axs[0].text(i, v + 0.006, f"{v:.3f}", ha="center")
    axs[0].set_ylabel("MAP on held-out days"); axs[0].legend(frameon=False)
    axs[0].set_title("Where does a disturbance go?")
    plt.setp(axs[0].get_xticklabels(), rotation=15)
    a = sorted(r["alpha_sweep_cal"])
    axs[1].plot(a, [r["alpha_sweep_cal"][x] for x in a], "o-", color=NAVY)
    axs[1].set_xlabel(r"blend exponent $\alpha$  (0 = physics prior, 1 = data)")
    axs[1].set_ylabel("MAP on calibration half"); axs[1].set_title(r"Choosing $\alpha$ (calibration only)")
    _fig(plt, fig, "E3_propagation")
    return res


# ---------------------------------------------------------------------------
def e4_replay():
    from . import alarm_replay, plantdata
    plt = _plt()
    base = alarm_replay.replay()
    logged = len(plantdata.alarms())
    cases = {"kpi_rerate": {("TE_8332A", "Hi"): 543.0},
             "idf_bearing_upgrade": {("YFJ3_ZD1", "Alarm"): 3.8, ("YFJ3_ZD2", "Alarm"): 3.8},
             "o2_recal": {("AIR_8301A", "Lo"): 2.5, ("AIR_8301B", "Lo"): 2.5},
             "drum_setpoint_retune": {("PTCA_8322A", "HiHi"): 10.6}}
    out = {"replay_total": base["total"], "logged_total": logged,
           "per_alarm_mismatches": 0, "cases": {}}
    from collections import Counter
    log = Counter((a["tag"], a["level"]) for a in plantdata.alarms())
    out["per_alarm_mismatches"] = sum(1 for k, v in base["per_alarm"].items() if log[k] != v["activations"])
    for s, ch in cases.items():
        out["cases"][s] = alarm_replay.compare(ch)
    _save("E4_alarm_replay", out)
    ts, x = plantdata.tag_series("TE_8332A")
    sp, _, _ = plantdata.setpoints()
    fig, ax = plt.subplots(figsize=(11.5, 4.4))
    hrs = (ts - ts[0]).astype("timedelta64[s]").astype(float) / 3600
    ax.plot(hrs[::12], x[::12], lw=0.6, color=GREY, label="TE_8332A (5 days)")
    ax.axhline(sp["TE_8332A"]["Hi"], color=GREEN, lw=2, label=f"current Hi = {sp['TE_8332A']['Hi']} °C")
    ax.axhline(543, color=RED, lw=2, ls="--", label="proposed Hi = 543 °C")
    ax.axhspan(530, 545, color=GREEN, alpha=0.06)
    c = out["cases"]["kpi_rerate"]["rows"][0]
    ax.set_title(f"Alarm replay of the KPI re-rate: activations {c['activations_before']} -> "
                 f"{c['activations_after']}, standing time {c['active_h_before']} h -> {c['active_h_after']} h")
    ax.set_xlabel("hours"); ax.set_ylabel("°C"); ax.set_ylim(500, 560)
    ax.legend(loc="lower right", ncol=3, frameon=False)
    _fig(plt, fig, "E4_alarm_replay")
    return out


# ---------------------------------------------------------------------------
def e5_unmanaged(trials: int = 12):
    from . import unmanaged
    plt = _plt()
    r = unmanaged.sensitivity(trials=trials)
    _save("E5_unmanaged", r)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.8))
    d = r["deltas"]
    pick = [("fingerprint:0.5", BLUE, r"$\frac{1}{2}\sigma$ fingerprint bins"),
            ("cusum:20.0", AMBER, "CUSUM (h = 20)"),
            ("wander:3.0", GREEN, "wander-normalised (c = 3)"),
            ("wander:4.0", NAVY, "wander-normalised (c = 4)")]
    for k, col, lab in pick:
        c = r["configs"][k]
        axs[0].plot(d, [c["excess"][x] * 100 for x in d], "o-", color=col,
                    label=f"{lab}: {c['fp_per_day_per_tag']:.2f} false/tag/day")
    axs[0].axhline(0, color="k", lw=0.8)
    axs[0].set_xlabel(r"injected step size ($\sigma$)"); axs[0].set_ylabel("detection above chance (pp)")
    axs[0].set_title("Detecting a change that skipped MOC"); axs[0].legend(frameon=False, fontsize=9.5)
    for det, col in (("fingerprint", BLUE), ("cusum", AMBER), ("wander", GREEN)):
        cs = [c for c in r["configs"].values() if c["detector"] == det]
        axs[1].plot([c["fp_per_day_per_tag"] for c in cs], [c["excess"][2.0] * 100 for c in cs],
                    "o-", color=col, label=det)
    axs[1].set_xscale("log"); axs[1].set_xlabel("false alarms per tag per day (log)")
    axs[1].set_ylabel(r"detection above chance at 2$\sigma$ (pp)")
    axs[1].set_title("Operating curves (held-out half)"); axs[1].legend(frameon=False)
    _fig(plt, fig, "E5_unmanaged")
    return r


# ---------------------------------------------------------------------------
def e6_model():
    from . import model_moc
    from .plant_state import load_base_state
    from .simulate import SCENARIOS
    plt = _plt()
    m, Mtr, Mte, tags = model_moc.train()
    e = model_moc.model_entry(m)
    base_n = model_moc._normal_rows(Mte, tags)
    far0 = m.score(base_n)["false_alarm_rate"]
    B = load_base_state(with_data_stats=True)
    rows = []
    for s in SCEN_ORDER:
        v = model_moc.validity(e, SCENARIOS[s].apply(B))
        Mx = model_moc.apply_effects(base_n, tags, model_moc.DATA_EFFECTS.get(s, {}))
        if not model_moc.operable(Mx, tags, m):
            far, obs = None, "inoperable"
        else:
            far = m.score(Mx)["false_alarm_rate"]
            obs = "degraded" if far > 2 * far0 else "unaffected"
        rows.append({"scenario": s, "plantmemory": v["verdict"], "moved_inputs": v["moved_inputs"],
                     "far": far, "inflation": (far / far0) if far is not None else None,
                     "observed": obs})
    res = {"components": m.A, "inputs": len(tags), "t2_limit": m.t2_lim, "spe_limit": m.spe_lim,
           "far_train_normal": m.score(model_moc._normal_rows(Mtr, tags))["false_alarm_rate"],
           "far_heldout_normal": far0, "rows": rows}
    _save("E6_model_moc", res)
    Mx = model_moc.apply_effects(base_n, tags, model_moc.DATA_EFFECTS["new_feedstock"])
    s0, s1 = m.score(base_n), m.score(Mx)
    fig, ax = plt.subplots(figsize=(11.5, 4.2))
    n = min(1000, len(s0["t2"]))
    ax.semilogy(s0["t2"][:n], color=GREEN, lw=0.8, label=f"before change (FAR {s0['false_alarm_rate']*100:.1f} %)")
    ax.semilogy(s1["t2"][:n], color=RED, lw=0.8, label=f"after new coal blend (FAR {s1['false_alarm_rate']*100:.0f} %)")
    ax.axhline(m.t2_lim, color="k", ls="--", label=f"99 % T² limit = {m.t2_lim:.1f}")
    ax.set_xlabel("held-out minutes"); ax.set_ylabel("Hotelling T² (log)")
    ax.set_title("A plant change silently breaks the monitoring model; PlantMemory flags it in advance")
    ax.legend(frameon=False, loc="upper right")
    _fig(plt, fig, "E6_model_moc")
    return res


# ---------------------------------------------------------------------------
def e7_org():
    from . import org, plantdata
    from .store import load_all
    plt = _plt()
    rows = []
    for p in plantdata.roster():
        r = org.assess_departure(p["id"])
        rows.append({"id": p["id"], "role": p["role"], "years": p["years"],
                     "orphaned": len(r["orphaned_entries"]), "exposed": len(r["assets_exposed"]),
                     "max_KRI": max([a["KRI"] for a in r["assets_exposed"]], default=0)})
    full_bf = org.bus_factor()
    seed_only = [e for e in load_all() if e.source == "seed"]
    import plant_memory.org as O
    _orig = O.load_all
    O.load_all = lambda: seed_only
    try:
        seed_bf = org.bus_factor()
    finally:
        O.load_all = _orig
    p01 = org.assess_departure("P01")
    from collections import Counter
    res = {"departures": rows, "senior_departure": p01,
           "bus_factor_full": dict(Counter(full_bf.values())),
           "bus_factor_tacit_only": dict(Counter(seed_bf.values())),
           "bf1_tacit_only": sorted(a for a, v in seed_bf.items() if v == 1)}
    _save("E7_org", res)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.6))
    ex = p01["assets_exposed"][:10]
    axs[0].barh([a["asset"] for a in ex][::-1], [a["KRI"] for a in ex][::-1], color=RED)
    axs[0].set_xlabel("knowledge risk index"); axs[0].set_title("Senior shift engineer leaves: exposed assets")
    ks = sorted(set(res["bus_factor_full"]) | set(res["bus_factor_tacit_only"]))
    w = 0.38
    axs[1].bar(np.array(ks) - w / 2, [res["bus_factor_tacit_only"].get(k, 0) for k in ks], w,
               color=AMBER, label="tacit (seed) knowledge only")
    axs[1].bar(np.array(ks) + w / 2, [res["bus_factor_full"].get(k, 0) for k in ks], w,
               color=GREEN, label="with grounded documented corpus")
    axs[1].set_xticks(ks); axs[1].set_xticklabels([str(k) if k < 4 else "4+" for k in ks])
    axs[1].set_xlabel("bus factor (people)"); axs[1].set_ylabel("assets")
    axs[1].set_title("Review capacity across the unit"); axs[1].legend(frameon=False)
    _fig(plt, fig, "E7_org")
    return res


# ---------------------------------------------------------------------------
def e8_scaling():
    """Re-validation effort as the plant grows (u identical units, local changes)."""
    from .mocgraph import diff_states
    from .plant_state import load_base_state
    from .simulate import SCENARIOS
    from .store import load_all
    plt = _plt()
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    deltas = [{(r, f) for _, r, f in diff_states(base, SCENARIOS[s].apply(base))}
              for s in SCEN_ORDER if s != "idf_bearing_rik"]
    per_unit = [sum(1 for e in entries if any((g.ref, g.aspect) in d for g in e.groundings))
                for d in deltas]
    rows = []
    for u in (1, 2, 4, 8, 16, 32):
        N = len(entries) * u
        naive = len(deltas) * N
        targeted = sum(per_unit)                  # each change touches one unit only
        rows.append({"units": u, "N": N, "naive": naive, "targeted": targeted,
                     "saving": 1 - targeted / naive})
    _save("E8_scaling", {"rows": rows, "flagged_per_change": per_unit})
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.plot([r["N"] for r in rows], [r["saving"] * 100 for r in rows], "o-", color=GREEN)
    for r in rows:
        ax.annotate(f"{r['saving']*100:.1f}%", (r["N"], r["saving"] * 100),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10)
    ax.set_xscale("log"); ax.set_xlabel("knowledge entries (units x 59)")
    ax.set_ylabel("re-validation effort saved (%)"); ax.set_ylim(60, 102)
    ax.set_title("Saving grows with the knowledge base when changes stay local")
    _fig(plt, fig, "E8_scaling")
    return {"rows": rows}


ALL = {"E1": e1_localisation, "E2": e2_coverage, "E3": e3_propagation, "E4": e4_replay,
       "E5": e5_unmanaged, "E6": e6_model, "E7": e7_org, "E8": e8_scaling}


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    which = (argv or sys.argv[1:]) or list(ALL)
    for k in which:
        t = time.time()
        ALL[k]()
        print(f"{k} done in {time.time() - t:.1f}s")


if __name__ == "__main__":
    main()
