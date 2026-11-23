"""
Alarm replay: the measured consequence of a setpoint change.

Before a setpoint change is authorised, re-run the plant's own ISA-18.2 alarm
state machine over the historian with the *proposed* setpoints and compare it
with the current ones. A setpoint MOC then comes with numbers (extra alarms,
alarm-flood intervals, standing-alarm time, margin to the next limit) instead of
an opinion.

State machine (same rules as the testbed's alarm generator): for a high alarm
with setpoint L and deadband d = max(0.01|L|, 0.5)

    activate when x_t > L,      clear when x_t < L - d     (mirror for low alarms)

Trigger and clear are mutually exclusive at any sample, so the latched state is
the forward-filled sign of the last event: e_t = +1 on trigger, -1 on clear,
state_t = last non-zero e up to t. Activations are the 0 -> 1 transitions.
"""
from __future__ import annotations

import numpy as np

from . import plantdata

DEADBAND_PCT, DEADBAND_ABS = 0.01, 0.5
FLOOD_N, FLOOD_WIN_SEC = 10, 600          # ISA-18.2: >10 alarms in 10 minutes


def deadband(sp: float) -> float:
    return max(abs(sp) * DEADBAND_PCT, DEADBAND_ABS)


def _latched(x: np.ndarray, sp: float, direction: str) -> np.ndarray:
    d = deadband(sp)
    if direction == "high":
        trig, clr = x > sp, x < sp - d
    else:
        trig, clr = x < sp, x > sp + d
    ev = np.zeros(len(x), dtype=np.int8)
    ev[trig] = 1
    ev[clr] = -1
    ev[np.isnan(x)] = 0                                 # missing samples hold state
    idx = np.where(ev != 0, np.arange(len(x)), 0)
    np.maximum.accumulate(idx, out=idx)                 # index of last event so far
    state = ev[idx] == 1
    state[(idx == 0) & (ev[0] != 1)] = False
    return state


def replay(setpoints: dict | None = None, tags: list[str] | None = None) -> dict:
    """Replay the alarm system over the historian.

    Returns per-(tag, level) activations and active-time, plus totals and the
    number of 10-minute alarm-flood windows.
    """
    ts, all_tags, X = plantdata.historian()
    sp0, priority, direction = plantdata.setpoints()
    sp = setpoints if setpoints is not None else sp0
    tags = tags or [t for t in sp if t in all_tags]
    per, onsets = {}, []
    for t in tags:
        x = X[:, all_tags.index(t)]
        for level, value in sp.get(t, {}).items():
            st = _latched(x, value, direction[level])
            rise = np.flatnonzero(st[1:] & ~st[:-1]) + 1
            if st[0]:
                rise = np.r_[0, rise]
            per[(t, level)] = {
                "activations": int(len(rise)),
                "active_hours": float(st.sum() * plantdata.SAMPLE_SEC / 3600),
                "priority": priority[level],
                "setpoint": value,
            }
            onsets.append(rise)
    on = np.sort(np.concatenate(onsets)) if onsets else np.array([], dtype=int)
    secs = on * plantdata.SAMPLE_SEC
    flood = 0
    if len(secs):
        j = np.searchsorted(secs, secs + FLOOD_WIN_SEC, side="left")
        flood = int(np.sum((j - np.arange(len(secs))) > FLOOD_N))
    total = sum(v["activations"] for v in per.values())
    return {"per_alarm": per, "total": total, "flood_onsets": flood}


def margin_sigma(tag: str, new_sp: float, level: str) -> float:
    """Distance from the operating 99th percentile to a limit, in units of σ."""
    _, x = plantdata.tag_series(tag)
    x = x[~np.isnan(x)]
    _, _, direction = plantdata.setpoints()
    sigma = float(np.std(x)) or 1e-9
    if direction[level] == "high":
        return float((new_sp - np.percentile(x, 99)) / sigma)
    return float((np.percentile(x, 1) - new_sp) / sigma)


def compare(changes: dict[tuple[str, str], float]) -> dict:
    """Replay current vs proposed setpoints for the affected tags only.

    `changes` maps (tag, level) -> proposed value.
    """
    sp0, _, _ = plantdata.setpoints()
    tags = sorted({t for t, _ in changes})
    proposed = {t: dict(sp0.get(t, {})) for t in tags}
    for (t, lvl), v in changes.items():
        proposed[t][lvl] = v
    before = replay({t: sp0.get(t, {}) for t in tags}, tags)
    after = replay(proposed, tags)
    rows = []
    for (t, lvl), v in changes.items():
        b = before["per_alarm"].get((t, lvl), {"activations": 0, "active_hours": 0.0})
        a = after["per_alarm"][(t, lvl)]
        rows.append({
            "tag": t, "level": lvl, "old": sp0.get(t, {}).get(lvl), "new": v,
            "activations_before": b["activations"], "activations_after": a["activations"],
            "active_h_before": round(b["active_hours"], 2),
            "active_h_after": round(a["active_hours"], 2),
            "margin_sigma_before": round(margin_sigma(t, sp0[t][lvl], lvl), 2)
            if lvl in sp0.get(t, {}) else None,
            "margin_sigma_after": round(margin_sigma(t, v, lvl), 2),
        })
    days = (len(plantdata.historian()[0]) * plantdata.SAMPLE_SEC) / 86400
    return {
        "rows": rows,
        "standing_h_before": round(sum(r["active_h_before"] for r in rows), 2),
        "standing_h_after": round(sum(r["active_h_after"] for r in rows), 2),
        "min_margin_after": min(r["margin_sigma_after"] for r in rows),
        "limit_inside_envelope": [f"{r['tag']}.{r['level']}" for r in rows
                                  if r["margin_sigma_after"] < 0 <= (r["margin_sigma_before"] or 0)],
        "total_before": before["total"], "total_after": after["total"],
        "per_day_before": round(before["total"] / days, 1),
        "per_day_after": round(after["total"] / days, 1),
        "flood_before": before["flood_onsets"], "flood_after": after["flood_onsets"],
    }
