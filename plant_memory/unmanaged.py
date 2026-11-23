"""
Closing the MOC loop: unmanaged-change detection and post-change verification.

A change that bypasses MOC is invisible to a paper process. Here the plant's own
data is watched for persistent shifts. Signals are reduced to 5-minute means m_t;
a rolling reference (the previous 6 h, ending 1 h before t) gives mu_ref, sd_ref.

Fingerprint detector (the PlantMemory distribution facet, k-sigma bins)
    flag when round(mean_1h / (k sigma)) != round(mu_ref / (k sigma))
    for P consecutive evaluations; sigma is the tag's operating spread.

CUSUM detector (Page 1954), on z_t = (m_t - mu_ref) / sd_ref
    S+_t = max(0, S+_{t-1} + z_t - kappa),   S-_t = max(0, S-_{t-1} - z_t - kappa)
    alarm when S+ or S- > h, then reset.

Sensitivity study: a step of delta * sigma is injected into the real historian at
a random time; a detector scores a hit if it alarms within H after the step, and
its false alarms per day are counted on the clean signal. Sweeping k (bins) and h
(CUSUM) traces each detector's operating curve.
"""
from __future__ import annotations

import numpy as np

from . import plantdata

WIN = 60                 # 60 x 5 s = 5-minute means
REF, GAP, CUR = 72, 12, 12   # 6 h reference, 1 h gap, 1 h current block (in windows)
H = 48                   # 4 h detection horizon (windows)
PERSIST = 3
KAPPA = 0.5
WIN_PER_DAY = 24 * 60 // 5


def window_means(x: np.ndarray) -> np.ndarray:
    n = (len(x) // WIN) * WIN
    with np.errstate(invalid="ignore"):
        return np.nanmean(x[:n].reshape(-1, WIN), axis=1)


def _rolling_ref(m: np.ndarray):
    n = len(m)
    mu = np.full(n, np.nan)
    sd = np.full(n, np.nan)
    cs = np.concatenate([[0], np.nancumsum(m)])
    cs2 = np.concatenate([[0], np.nancumsum(m ** 2)])
    for t in range(REF + GAP, n):
        a, b = t - GAP - REF, t - GAP
        s, s2 = cs[b] - cs[a], cs2[b] - cs2[a]
        mu[t] = s / REF
        sd[t] = np.sqrt(max(s2 / REF - mu[t] ** 2, 1e-12))
    return mu, sd


def fingerprint_alarms(m: np.ndarray, sigma: float, k: float) -> np.ndarray:
    mu, _ = _rolling_ref(m)
    cur = np.convolve(m, np.ones(CUR) / CUR, mode="full")[: len(m)]
    w = k * sigma
    diff = np.round(cur / w) != np.round(mu / w)
    diff[np.isnan(mu)] = False
    run = np.zeros(len(m), dtype=int)
    for t in range(1, len(m)):
        run[t] = run[t - 1] + 1 if diff[t] else 0
    return run == PERSIST                         # one event when persistence is reached


def cusum_alarms(m: np.ndarray, h: float) -> np.ndarray:
    mu, sd = _rolling_ref(m)
    al = np.zeros(len(m), dtype=bool)
    sp = sn = 0.0
    for t in range(len(m)):
        if np.isnan(mu[t]) or sd[t] <= 0:
            continue
        z = (m[t] - mu[t]) / sd[t]
        sp, sn = max(0.0, sp + z - KAPPA), max(0.0, sn - z - KAPPA)
        if sp > h or sn > h:
            al[t] = True
            sp = sn = 0.0
    return al


def wander_scale(m: np.ndarray, upto: int) -> float:
    """How much the 1-h mean naturally departs from its 6-h reference in normal
    operation (std of cur - mu over the calibration part of the series)."""
    mu, _ = _rolling_ref(m)
    cur = np.convolve(m, np.ones(CUR) / CUR, mode="full")[: len(m)]
    d = (cur - mu)[:upto]
    return float(np.nanstd(d)) or 1.0


def wander_alarms(m: np.ndarray, scale: float, c: float) -> np.ndarray:
    """Wander-normalised detector: |cur - mu_ref| / scale > c for PERSIST windows."""
    mu, _ = _rolling_ref(m)
    cur = np.convolve(m, np.ones(CUR) / CUR, mode="full")[: len(m)]
    z = np.abs(cur - mu) / scale
    over = np.nan_to_num(z) > c
    run = np.zeros(len(m), dtype=int)
    for t in range(1, len(m)):
        run[t] = run[t - 1] + 1 if over[t] else 0
    return run == PERSIST


def study_tags() -> list[str]:
    _, tags, X = plantdata.historian()
    return [t for j, t in enumerate(tags)
            if np.nanstd(X[:, j]) > 0 and np.isnan(X[:, j]).mean() < 0.01]


def _run(kind, m, p, sigma, scale):
    if kind == "fingerprint":
        return fingerprint_alarms(m, sigma, p)
    if kind == "cusum":
        return cusum_alarms(m, p)
    return wander_alarms(m, scale, p)


def sensitivity(deltas=(0.25, 0.5, 1.0, 2.0, 3.0), trials: int = 12,
                ks=(0.25, 0.5, 1.0, 2.0), hs=(4.0, 10.0, 20.0),
                cs=(2.0, 3.0, 4.0, 6.0), seed: int = 7) -> dict:
    """Held-out sensitivity study.

    sigma (fingerprint bins) and the wander scale are estimated on the first half
    of the historian only. False alarms and injected steps are evaluated on the
    second half only. Because a busy detector also "hits" by chance, the chance
    rate (a clean alarm inside a random H-window) is reported and subtracted.
    """
    rng = np.random.default_rng(seed)
    _, tags, X = plantdata.historian()
    tlist = study_tags()
    configs = ([("fingerprint", k) for k in ks] + [("cusum", h) for h in hs]
               + [("wander", c) for c in cs])
    res = {c: {"fp": [], "chance": [], **{d: [] for d in deltas},
               "delay": {d: [] for d in deltas}} for c in configs}
    for t in tlist:
        x = X[:, tags.index(t)]
        m = window_means(x)
        half = len(m) // 2
        sigma = float(np.nanstd(x[: half * WIN])) or 1.0
        scale = wander_scale(m, half)
        test_days = (len(m) - half) / WIN_PER_DAY
        clean = {c: _run(c[0], m, c[1], sigma, scale) for c in configs}
        for c in configs:
            a = clean[c][half:]
            res[c]["fp"].append(a.sum() / test_days)
            win = np.convolve(a.astype(float), np.ones(H), mode="full")[H - 1:H - 1 + len(a)]
            res[c]["chance"].append(float((win > 0)[: len(a) - H].mean()))
        for d in deltas:
            for _ in range(trials):
                t0 = int(rng.integers(half, len(m) - H))
                mm = m.copy()
                mm[t0:] += d * sigma
                for c in configs:
                    a = _run(c[0], mm, c[1], sigma, scale)
                    idx = np.flatnonzero(a[t0:t0 + H])
                    res[c][d].append(1.0 if len(idx) else 0.0)
                    if len(idx):
                        res[c]["delay"][d].append(idx[0] * 5)        # minutes
    out = {}
    for c, r in res.items():
        chance = float(np.mean(r["chance"]))
        out[f"{c[0]}:{c[1]}"] = {
            "detector": c[0], "param": c[1],
            "fp_per_day_per_tag": float(np.mean(r["fp"])),
            "chance": chance,
            "tpr": {d: float(np.mean(r[d])) for d in deltas},
            "excess": {d: float(np.mean(r[d]) - chance) for d in deltas},
            "delay_min": {d: (float(np.median(r["delay"][d])) if r["delay"][d] else None)
                          for d in deltas},
        }
    return {"configs": out, "tags": tlist, "trials": trials, "deltas": list(deltas)}


C_DEFAULT = 3.0           # chosen operating point from the sensitivity study


def scan(c: float = C_DEFAULT, tags: list[str] | None = None,
         covered: dict[str, list] | None = None) -> list[dict]:
    """Run the wander-normalised detector over the historian and report candidate
    changes. If `covered` maps tag -> [(t_start, t_end)] of approved MOCs, a
    detection inside such an interval is 'managed', otherwise 'without MOC'."""
    ts, all_tags, X = plantdata.historian()
    tw = ts[: (len(ts) // WIN) * WIN: WIN]
    out = []
    for t in tags or study_tags():
        m = window_means(X[:, all_tags.index(t)])
        scale = wander_scale(m, len(m) // 2)
        for i in np.flatnonzero(wander_alarms(m, scale, c)):
            when = tw[i]
            managed = any(a <= when <= b for a, b in (covered or {}).get(t, []))
            out.append({"tag": t, "time": str(when), "index": int(i),
                        "status": "managed (approved MOC)" if managed else "change without MOC"})
    return out


def verify(expected_tags: set[str], effects: dict, t0_frac: float = 0.6,
           c: float = C_DEFAULT) -> dict:
    """Post-change verification: realise a change's data effects at t0, detect what
    moved in the next H hours, and split it into expected vs unanticipated."""
    _, tags, X = plantdata.historian()
    t0 = int(len(X) * t0_frac)
    Xc = X.copy()
    for t, (kind, val) in effects.items():
        j = tags.index(t)
        if kind == "scale":
            Xc[t0:, j] *= val
        elif kind == "offset":
            Xc[t0:, j] += val
    w0 = t0 // WIN
    moved = set()
    for t in study_tags():
        j = tags.index(t)
        m0, m1 = window_means(X[:, j]), window_means(Xc[:, j])
        scale = wander_scale(m0, len(m0) // 2)
        clean, chg = wander_alarms(m0, scale, c), wander_alarms(m1, scale, c)
        if np.any((chg & ~clean)[w0:w0 + H]):
            moved.add(t)
    return {"expected_and_seen": sorted(moved & expected_tags),
            "expected_not_seen": sorted(expected_tags - moved),
            "unanticipated": sorted(moved - expected_tags)}
