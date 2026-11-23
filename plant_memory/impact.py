"""
Computable MOC impact assessment and risk tiering.

For a proposed change this computes, without any human reasoning step:

  1. the change set Δ(S, S') (and so whether it is a replacement-in-kind);
  2. exact impact (dependency channel): knowledge whose grounding moved, procedure
     documents that reference a changed facet, alarm limits that changed, models
     whose inputs moved;
  3. graded impact (process channel): assets the change disturbs physically, with
     a max-product score and the path that explains it, and the knowledge,
     procedures and alarms that sit on them ("watch" items);
  4. the people who must review or be informed;
  5. for setpoint changes, an alarm replay over the historian;
  6. risk R = S x L on a 5 x 5 matrix, the MOC tier, required approvers and
     whether a pre-startup safety review (PSSR) is required.

Every number carries its contributors, so the tier is explainable.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np

from . import alarm_replay, mocgraph, org, plantdata
from .drift import evaluate_all
from .plant_state import load_base_state
from .simulate import get_scenario
from .store import load_all

WATCH = 0.30          # graded impact worth watching
PRIO = {"Critical": 5, "High": 4, "Medium": 3, "Low": 2}

# Which document types must be revised when a given facet changes.
DOC_RELEVANCE = {
    "setpoints": {"controls", "troubleshooting", "sop", "safety"},
    "normal_range": {"controls", "troubleshooting", "sop", "datasheet"},
    "distribution": {"controls", "troubleshooting"},
    "presence": {"controls", "troubleshooting", "sop", "safety", "maintenance", "datasheet"},
    "connections": {"maintenance", "datasheet", "sop", "safety", "controls"},
}

ROLE = {"process": "P05", "c_and_i": "P07", "maintenance": "P09", "safety": "P10",
        "model": "P11", "operations": "P12"}


@lru_cache(maxsize=1)
def _adjacency():
    from .calibrate import calibrated_tag_weights
    return mocgraph.physical_graph(tag_weights=calibrated_tag_weights())


def _role_name(pid):
    return next((f"{p['id']} {p['role']}" for p in plantdata.roster() if p["id"] == pid), pid)


def _setpoint_changes(base, after) -> dict:
    out = {}
    for t in set(base.setpoints) | set(after.setpoints):
        b, a = base.setpoints.get(t, {}), after.setpoints.get(t, {})
        for lvl in set(b) | set(a):
            if b.get(lvl) != a.get(lvl) and a.get(lvl) is not None and t in after.tags:
                out[(t, lvl)] = a[lvl]
    return out


def assess(scenario_name: str, run_replay: bool = True) -> dict:
    sc = get_scenario(scenario_name)
    base = load_base_state(with_data_stats=True)
    after = sc.apply(base)
    delta = mocgraph.diff_states(base, after)
    changed = {(r, f) for _, r, f in delta}
    changed_assets = {r for _, r, _ in delta}
    entries = load_all()

    # ---- knowledge (exact) ------------------------------------------------
    d0 = {d.entry_id: d for d in evaluate_all(entries, base)}
    knowledge = []
    for d in evaluate_all(entries, after):
        h = getattr(d.health, "value", d.health)
        if h != "intact":
            knowledge.append({"id": d.entry_id, "title": d.title, "health": h,
                              "conf_before": d0[d.entry_id].confidence,
                              "conf_after": d.confidence,
                              "reasons": [g.detail for g in d.groundings if g.detail]})
    flagged_ids = {k["id"] for k in knowledge}

    # ---- physical propagation (graded) -----------------------------------
    src = mocgraph.disturbance_sources(delta)
    reach = mocgraph.propagate(src, _adjacency()) if src else {}
    disturbed = {n: r["score"] for n, r in reach.items() if n not in src}
    physical = sorted(({"asset": n, "score": round(s, 3),
                        "path": mocgraph.explain(n, reach)} for n, s in disturbed.items()
                       if s >= WATCH), key=lambda x: -x["score"])
    watch_k = []
    for e in entries:
        if e.id in flagged_ids:
            continue
        s = max((disturbed.get(g.ref, 0) for g in e.groundings), default=0)
        if s >= WATCH:
            watch_k.append({"id": e.id, "title": e.title, "score": round(s, 3)})
    watch_k.sort(key=lambda x: -x["score"])

    # ---- procedures -------------------------------------------------------
    procedures, watch_p = [], []
    for doc in plantdata.documents():
        refs = set(doc.get("tags", [])) | set(doc.get("equipment", []))
        hit = [f"{a}:{f}" for a, f in changed if a in refs and doc["doc_type"] in DOC_RELEVANCE[f]]
        if hit:
            procedures.append({"doc_id": doc["doc_id"], "title": doc["title"],
                               "type": doc["doc_type"], "revision": doc["revision"],
                               "because": sorted(hit)})
        else:
            s = max((disturbed.get(a, 0) for a in refs), default=0)
            if s >= WATCH:
                watch_p.append({"doc_id": doc["doc_id"], "type": doc["doc_type"], "score": round(s, 3)})

    # ---- alarms -----------------------------------------------------------
    sp0, prio, _ = plantdata.setpoints()
    sp_changes = _setpoint_changes(base, after)
    alarms = [{"alarm": f"{t}.{lvl}", "old": sp0.get(t, {}).get(lvl), "new": v,
               "priority": prio[lvl]} for (t, lvl), v in sp_changes.items()]
    removed = [r for k, r, f in delta if k == "tag" and f == "presence" and r not in after.tags]
    for t in removed:
        alarms += [{"alarm": f"{t}.{lvl}", "old": v, "new": None, "priority": prio[lvl]}
                   for lvl, v in sp0.get(t, {}).items()]
    watch_a = sorted(({"alarm": f"{t}.{lvl}", "priority": prio[lvl], "score": round(disturbed[t], 3)}
                      for t in disturbed if t in sp0 and disturbed[t] >= WATCH
                      for lvl in sp0[t]), key=lambda x: -x["score"])
    replay = alarm_replay.compare(sp_changes) if (run_replay and sp_changes) else None

    # ---- models -----------------------------------------------------------
    models = []
    try:
        from . import model_moc
        mentry = _model_entry()
        v = model_moc.validity(mentry, after)
        if v["verdict"] != "valid":
            models.append({"model": model_moc.MODEL_ID, **v})
    except Exception as exc:                          # model optional (needs scipy)
        models.append({"model": "unavailable", "verdict": str(exc)})

    # ---- people -----------------------------------------------------------
    people = org.plantdata.roster()
    system = org._system_index()
    by_id = {e.id: e for e in entries}
    reviewers = {}
    for k in knowledge:
        q = org.qualified(by_id[k["id"]], people, system)
        reviewers[k["id"]] = sorted(q)

    # ---- risk -------------------------------------------------------------
    risk = _risk(scenario_name, base, after, delta, knowledge, procedures, alarms,
                 sp_changes, removed, disturbed, models, replay)
    approvers = _approvers(risk, delta, procedures, alarms, models)
    return {
        "scenario": scenario_name, "description": sc.description,
        "moc_object": sc.moc_object, "moc_class": sc.moc_class,
        "change_set": [f"{k}:{r}:{f}" for k, r, f in delta],
        "replacement_in_kind": not delta,
        "knowledge": knowledge, "watch_knowledge": watch_k,
        "procedures": procedures, "watch_procedures": watch_p,
        "alarms": alarms, "watch_alarms": watch_a, "alarm_replay": replay,
        "models": models, "reviewers": reviewers,
        "physical": physical[:15], "n_disturbed": len([s for s in disturbed.values() if s >= WATCH]),
        "risk": risk, "approvers": [_role_name(p) for p in approvers],
        "pssr_required": risk["tier"] in ("Major", "Major + HAZOP") or any(
            k == "kg_node" for k, _, _ in delta),
        "corpus_size": len(entries),
    }


@lru_cache(maxsize=1)
def _model_entry():
    from . import model_moc
    m, *_ = model_moc.train()
    return model_moc.model_entry(m)


def _risk(name, base, after, delta, knowledge, procedures, alarms, sp_changes,
          removed, disturbed, models, replay) -> dict:
    if not delta:
        return {"S": 0, "L": 0, "R": 0, "tier": "Replacement in kind (exempt)",
                "severity_from": ["no facet fingerprint moved"], "likelihood_from": []}
    sp0, prio, _ = plantdata.setpoints()
    sev = [(1, "change touches plant configuration")]
    for a in alarms:
        sev.append((PRIO[a["priority"]], f"{a['alarm']} ({a['priority']}) limit changed"))
    if any(k["health"] == "broken" for k in knowledge):
        sev.append((4, "knowledge depends on an asset this change removes"))
    if "TE_8332A" in {r for _, r, _ in delta}:
        sev.append((4, "primary KPI TE_8332A affected"))
    if any(p["type"] == "safety" for p in procedures):
        sev.append((4, "a safety procedure must be revised"))
    for t, s in disturbed.items():
        if t in sp0 and s >= 0.5:
            c = max(PRIO[prio[l]] for l in sp0[t])
            sev.append((min(5, round(c * s)), f"disturbs {t} (score {s:.2f}) with {c}-level alarms"))
    if any(m["verdict"].startswith("broken") for m in models):
        sev.append((4, "monitoring model loses an input"))
    S = max(s for s, _ in sev)

    lik = [(1, "base")]
    z_max = 0.0
    for _, r, f in delta:
        st = base.tag_stats(r) if base.tag_exists(r) else None
        sd = (st or {}).get("std") or 0
        if f == "setpoints" and sd:
            for (t, lvl), v in sp_changes.items():
                if t == r and lvl in sp0.get(t, {}):
                    z_max = max(z_max, abs(v - sp0[t][lvl]) / sd)
        if f == "distribution" and sd:
            sa = after.tag_stats(r) or {}
            z_max = max(z_max, abs(sa.get("mean", 0) - st.get("mean", 0)) / sd)
    bump = int(z_max >= 0.5) + int(z_max >= 1) + int(z_max >= 2)
    if bump:
        lik.append((1 + bump, f"largest move = {z_max:.2f} sigma of operating spread"))
    if any(k == "kg_node" for k, _, _ in delta):
        lik.append((3, "equipment rewired or re-identified"))
    if removed:
        lik.append((3, "instrument removed"))
    if replay:
        if replay["total_before"] and replay["total_after"] > 1.25 * replay["total_before"]:
            lik.append((4, f"replay: activations rise {replay['total_before']} -> {replay['total_after']}"))
        if replay["standing_h_before"] and replay["standing_h_after"] > 1.25 * replay["standing_h_before"]:
            lik.append((4, f"replay: standing-alarm time {replay['standing_h_before']} h -> "
                           f"{replay['standing_h_after']} h"))
        if replay["limit_inside_envelope"]:
            lik.append((5, "new limit lies inside the normal operating envelope: "
                           + ", ".join(replay["limit_inside_envelope"])))
    L = min(5, max(l for l, _ in lik))
    R = S * L
    # Standard four-band 5 x 5 matrix
    tier = ("Minor" if R <= 4 else "Moderate" if R <= 9 else
            "Major" if R <= 16 else "Major + HAZOP")
    return {"S": S, "L": L, "R": R, "tier": tier,
            "severity_from": [t for s, t in sorted(sev, reverse=True) if s == S][:3],
            "likelihood_from": [t for l, t in sorted(lik, reverse=True) if l == L][:3],
            "z_max": round(z_max, 2)}


def _approvers(risk, delta, procedures, alarms, models) -> list[str]:
    if risk["tier"].startswith("Replacement"):
        return []
    a = [ROLE["process"]]
    if alarms:
        a.append(ROLE["c_and_i"])
    if any(k == "kg_node" for k, _, _ in delta) or any(
            f == "presence" for _, _, f in delta):
        a.append(ROLE["maintenance"])
    if procedures:
        a.append(ROLE["operations"])
    if models:
        a.append(ROLE["model"])
    if risk["tier"] != "Minor" or any(x["priority"] == "Critical" for x in alarms) or any(
            p["type"] == "safety" for p in procedures):
        a.append(ROLE["safety"])
    seen = []
    for x in a:
        if x not in seen:
            seen.append(x)
    return seen
