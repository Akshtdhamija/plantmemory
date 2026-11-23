"""
Data calibration and validation of impact propagation (plant-wide disturbance
propagation analysis on the boiler historian).

Calibration (first half of the historian)
-----------------------------------------
Signals are reduced to 1-minute means and first-differenced, so that common slow
trends (load) do not masquerade as coupling. For an ordered tag pair (u, v) the
lagged cross-correlation

    rho_uv(tau) = corr( du_t , dv_{t+tau} ),   tau = 0 .. TAU_MAX minutes

is computed, and the data score is the strongest *forward* coupling

    s_D(u -> v) = max_{0 <= tau <= TAU_MAX} |rho_uv(tau)|,   kept only if > z / sqrt(N)

(Bauer & Thornhill 2008; Yang et al. 2014). Forward lags only: v must respond
after u, which is what a propagating disturbance does.

Validation (second, held-out half)
----------------------------------
Ground truth is taken from what the plant actually did: a *disturbance onset* on
tag u is a 1-minute change larger than K_EVT robust standard deviations. Tag v is
said to follow u when v also has an onset within DELTA minutes afterwards, more
often than chance:

    lift(u -> v) = P(v onset in (t, t+DELTA] | u onset at t) / P(v onset in a random DELTA window)

Pairs with lift >= LIFT_MIN and at least MIN_CO co-occurrences are the relevant set.
Four predictors are ranked against it: same-system heuristic, graph prior,
data-calibrated, and the physics-gated hybrid s_C = sqrt(s_G * s_D).
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np

from . import mocgraph, plantdata

MIN_PER_BIN = 12          # 12 x 5 s = 1 minute
TAU_MAX = 15              # minutes
Z_SIG = 3.0               # significance multiplier on 1/sqrt(N)
K_EVT = 4.0               # disturbance onset threshold (robust sigmas)
DELTA = 15                # minutes a response may lag its cause
LIFT_MIN, MIN_CO, MIN_SRC_EVENTS = 2.0, 3, 5


def minute_means(X: np.ndarray) -> np.ndarray:
    n = (len(X) // MIN_PER_BIN) * MIN_PER_BIN
    M = X[:n].reshape(-1, MIN_PER_BIN, X.shape[1])
    with np.errstate(invalid="ignore"):
        return np.nanmean(M, axis=1)


def _halves():
    _, tags, X = plantdata.historian()
    M = minute_means(X)
    h = len(M) // 2
    return tags, M[:h], M[h:]


def _standardise_diff(M: np.ndarray) -> np.ndarray:
    D = np.diff(M, axis=0)
    D = np.where(np.isnan(D), 0.0, D)
    sd = D.std(axis=0)
    sd[sd == 0] = 1.0
    return (D - D.mean(axis=0)) / sd


def data_scores(M: np.ndarray, tags: list[str]) -> dict[tuple[str, str], float]:
    """s_D(u -> v) from lagged cross-correlation of differenced minute means."""
    Z = _standardise_diff(M)
    n = len(Z)
    thr = Z_SIG / np.sqrt(n)
    best = np.zeros((len(tags), len(tags)))
    for tau in range(0, TAU_MAX + 1):
        A, B = Z[: n - tau], Z[tau:]
        C = np.abs(A.T @ B) / len(A)             # |corr(u_t, v_{t+tau})| for all pairs
        best = np.maximum(best, C)
    best[best < thr] = 0.0
    np.fill_diagonal(best, 0.0)
    return {(tags[i], tags[j]): float(best[i, j])
            for i in range(len(tags)) for j in range(len(tags)) if i != j}


def onsets(M: np.ndarray) -> list[np.ndarray]:
    """Disturbance onsets per tag: minute changes above K_EVT robust sigmas."""
    D = np.diff(M, axis=0)
    out = []
    for j in range(D.shape[1]):
        d = D[:, j]
        d = d[~np.isnan(d)] if np.isnan(d).any() else d
        med = np.nanmedian(D[:, j])
        mad = np.nanmedian(np.abs(D[:, j] - med)) * 1.4826 or np.nanstd(D[:, j]) or 1.0
        big = np.abs(D[:, j] - med) > K_EVT * mad
        idx = np.flatnonzero(big)
        if len(idx):                                   # keep first sample of each burst
            idx = idx[np.r_[True, np.diff(idx) > 1]]
        out.append(idx)
    return out


def ground_truth(M: np.ndarray, tags: list[str]) -> dict:
    ev = onsets(M)
    T = len(M) - 1
    lift, co = {}, {}
    for i, u in enumerate(tags):
        if len(ev[i]) < MIN_SRC_EVENTS:
            continue
        for j, v in enumerate(tags):
            if i == j or len(ev[j]) == 0:
                continue
            ej = ev[j]
            hits = 0
            for t in ev[i]:
                k = np.searchsorted(ej, t + 1)
                if k < len(ej) and ej[k] <= t + DELTA:
                    hits += 1
            # chance that a random window of DELTA minutes contains an onset of v
            cover = np.zeros(T + DELTA + 1, dtype=bool)
            for t in ej:
                cover[max(0, t - DELTA):t] = True
            p0 = cover[:T].mean() or 1e-9
            p1 = hits / len(ev[i])
            lift[(u, v)] = p1 / p0
            co[(u, v)] = hits
    relevant = defaultdict(set)
    for (u, v), L in lift.items():
        if L >= LIFT_MIN and co[(u, v)] >= MIN_CO:
            relevant[u].add(v)
    sources = sorted(u for u in relevant if relevant[u])
    return {"lift": lift, "co": co, "relevant": relevant, "sources": sources,
            "n_events": {t: int(len(e)) for t, e in zip(tags, ev)}}


def system_of() -> dict[str, str]:
    k = plantdata.kg()
    part = {l["source"]: l["target"] for l in k["links"] if l["edge_type"] == "PART_OF"}
    out = {}
    for n in k["nodes"]:
        if n["node_type"] == "Sensor":
            eq = part.get(n["node_id"])
            out[n["node_id"]] = part.get(eq, eq)
    return out


def _ap(ranked: list[str], rel: set[str]) -> float:
    hits, s = 0, 0.0
    for i, v in enumerate(ranked, 1):
        if v in rel:
            hits += 1
            s += hits / i
    return s / len(rel) if rel else 0.0


def _ndcg(ranked: list[str], rel: set[str], k: int = 5) -> float:
    dcg = sum(1 / np.log2(i + 1) for i, v in enumerate(ranked[:k], 1) if v in rel)
    idcg = sum(1 / np.log2(i + 1) for i in range(1, min(k, len(rel)) + 1))
    return dcg / idcg if idcg else 0.0


def _blend(sG: dict, sD: dict, alpha: float) -> dict:
    """Physics-gated hybrid s_C = s_D^alpha * s_G^(1-alpha) (zero without a path)."""
    out = {}
    for p, d in sD.items():
        g = sG.get(p, 0.0)
        out[p] = float((d ** alpha) * (g ** (1 - alpha))) if g > 0 else 0.0
    return out


def _score(s: dict, gt: dict, tags: list[str], sG: dict) -> dict:
    aps, nd, p3, expl = [], [], [], []
    for u in gt["sources"]:
        cand = [v for v in tags if v != u]
        ranked = sorted(cand, key=lambda v: (-s.get((u, v), 0.0), v))
        rel = gt["relevant"][u]
        aps.append(_ap(ranked, rel))
        nd.append(_ndcg(ranked, rel, 5))
        p3.append(len(set(ranked[:3]) & rel) / 3)
        expl.append(np.mean([sG.get((u, v), 0) > mocgraph.THETA for v in ranked[:5]]))
    return {"MAP": float(np.mean(aps)), "NDCG@5": float(np.mean(nd)),
            "P@3": float(np.mean(p3)), "explained_top5": float(np.mean(expl))}


def evaluate() -> dict:
    """Rank propagation predictors against held-out disturbance propagation.

    The hybrid's blend exponent alpha is chosen on the calibration half only
    (its own ground truth), then frozen and scored on the test half.
    """
    tags, M_cal, M_test = _halves()
    sD = data_scores(M_cal, tags)
    sG = mocgraph.tag_to_tag_scores()
    sysm = system_of()
    sH = {(u, v): (1.0 if sysm.get(u) == sysm.get(v) else 0.0) for (u, v) in sD}
    gt_cal = ground_truth(M_cal, tags)
    alphas = [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]
    sweep = {a: _score(_blend(sG, sD, a), gt_cal, tags, sG)["MAP"] for a in alphas}
    a_best = max(sweep, key=sweep.get)
    sC = _blend(sG, sD, a_best)
    gt = ground_truth(M_test, tags)
    preds = {"Same-system heuristic": sH, "Graph prior (max-product)": sG,
             "Data-calibrated (lagged x-corr)": sD,
             f"Physics-gated hybrid (alpha={a_best})": sC}
    res = {name: _score(s, gt, tags, sG) for name, s in preds.items()}
    # random baseline (expected AP of a random ranking = prevalence)
    prev = np.mean([len(gt["relevant"][u]) / (len(tags) - 1) for u in gt["sources"]])
    return {"predictors": res, "random_MAP": float(prev), "alpha": a_best,
            "alpha_sweep_cal": sweep,
            "n_sources": len(gt["sources"]),
            "n_relevant_pairs": int(sum(len(gt["relevant"][u]) for u in gt["sources"])),
            "sources": gt["sources"], "data_scores": sD, "graph_scores": sG,
            "events_test": gt["n_events"]}


def calibrated_tag_weights(min_w: float = 0.15) -> dict[tuple[str, str], float]:
    """Data-calibrated sensor couplings to add to the propagation graph,
    restricted to pairs that also have a physical path (physics-gated)."""
    tags, M_cal, _ = _halves()
    sD = data_scores(M_cal, tags)
    sG = mocgraph.tag_to_tag_scores()
    return {p: round(float(np.sqrt(sD[p] * sG.get(p, 0))), 3) for p in sD
            if sD[p] >= min_w and sG.get(p, 0) > mocgraph.THETA}
