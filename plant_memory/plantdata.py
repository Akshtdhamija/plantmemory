"""
Plant data access for the Management-of-Change engines.

Loads the five-day historian, the ISA-18.2 alarm log, the process knowledge
graph, the alarm setpoint register and the document index once per process and
hands them out as plain numpy / python structures. Everything here is read-only.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

import numpy as np

from .paths import ALARM_DB, BOILER_KG, DOC_INDEX, HISTORIAN_DB, ROSTER

SAMPLE_SEC = 5  # historian resolution


@lru_cache(maxsize=1)
def historian():
    """Return (timestamps[datetime64], tags[list], X[n_samples, n_tags])."""
    import duckdb
    con = duckdb.connect(HISTORIAN_DB, read_only=True)
    cols = [r[0] for r in con.execute("describe historian_data").fetchall()]
    tags = [c for c in cols if c != "timestamp"]
    arr = con.execute("select * from historian_data order by timestamp").fetchnumpy()
    con.close()
    ts = np.asarray(arr["timestamp"]).astype("datetime64[s]")
    X = np.column_stack([np.asarray(arr[t], dtype=float) for t in tags])
    return ts, tags, X


@lru_cache(maxsize=1)
def alarms():
    """Alarm events as a list of dicts (activation-ordered)."""
    import duckdb
    con = duckdb.connect(ALARM_DB, read_only=True)
    rows = con.execute(
        "select tag_name, alarm_level, priority, setpoint, activated_at, cleared_at, "
        "duration_sec from alarm_events order by activated_at").fetchall()
    con.close()
    return [dict(tag=r[0], level=r[1], priority=r[2], setpoint=r[3],
                 t_on=np.datetime64(r[4], "s"),
                 t_off=np.datetime64(r[5], "s") if r[5] is not None else None,
                 duration=r[6]) for r in rows]


@lru_cache(maxsize=1)
def kg():
    with open(BOILER_KG, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def setpoints():
    """{tag: {level: value}} plus priority / direction maps from the register."""
    import sys
    from .paths import PROJECT_DIR
    if PROJECT_DIR not in sys.path:
        sys.path.insert(0, PROJECT_DIR)
    from alarm_metadata import ALARM_DIRECTION, ALARM_SETPOINTS, PRIORITY_MAP
    sp = {t: {k: v for k, v in d.items() if k in ALARM_DIRECTION}
          for t, d in ALARM_SETPOINTS.items()}
    return sp, dict(PRIORITY_MAP), dict(ALARM_DIRECTION)


@lru_cache(maxsize=1)
def documents():
    if not os.path.isfile(DOC_INDEX):
        return []
    with open(DOC_INDEX, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def roster():
    if not os.path.isfile(ROSTER):
        return []
    with open(ROSTER, encoding="utf-8") as f:
        return json.load(f)["people"]


def tag_series(tag: str):
    ts, tags, X = historian()
    return ts, X[:, tags.index(tag)]


def split_index(frac: float = 0.5) -> int:
    """Index splitting the historian into a calibration half and a test half."""
    ts, _, _ = historian()
    return int(len(ts) * frac)
