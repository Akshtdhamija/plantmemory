"""
PlantState — a snapshot of the plant's ground-truth configuration.

This is the "world" that knowledge is grounded against. It is assembled from the
boiler agent's own authoritative sources:

  * tag_metadata.py     -> per-tag description, units, sensor type, normal range
  * alarm_metadata.py   -> per-tag alarm/trip setpoints
  * boiler_kg.json      -> equipment/sensor topology (nodes + connections)
  * (optional) historian -> per-tag distribution statistics (mean/std)

A PlantState can carry an *override layer* on top of the base configuration.
Overrides are how we simulate real plant changes (a recalibrated sensor, an
upgraded fan, a retuned setpoint, distribution drift) without mutating the
source files. Drift detection then compares fingerprints of the base state at
capture time against the current (possibly overridden) state.
"""
from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass, field
from typing import Any, Optional

from .paths import BOILER_KG, HISTORIAN_DB, SNAPSHOT_DIR

# Import the boiler agent's authoritative metadata directly.
import sys
_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT not in sys.path:
    sys.path.insert(0, _PROJECT)

from tag_metadata import TAG_METADATA          # noqa: E402
from alarm_metadata import ALARM_SETPOINTS      # noqa: E402


@dataclass
class PlantState:
    """A concrete, comparable snapshot of the plant configuration."""

    tags: dict[str, dict[str, Any]] = field(default_factory=dict)
    setpoints: dict[str, dict[str, float]] = field(default_factory=dict)
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    adjacency: dict[str, list[list[str]]] = field(default_factory=dict)
    data_stats: dict[str, dict[str, float]] = field(default_factory=dict)
    label: str = "base"

    # -- accessors used by the fingerprinter -------------------------------
    def tag_range(self, tag: str) -> Optional[tuple[Optional[float], Optional[float]]]:
        t = self.tags.get(tag)
        if t is None:
            return None
        return (t.get("normal_min"), t.get("normal_max"))

    def tag_setpoints(self, tag: str) -> Optional[dict[str, float]]:
        return self.setpoints.get(tag)

    def tag_exists(self, tag: str) -> bool:
        return tag in self.tags

    def node(self, node_id: str) -> Optional[dict[str, Any]]:
        return self.nodes.get(node_id)

    def node_exists(self, node_id: str) -> bool:
        return node_id in self.nodes

    def node_neighbors(self, node_id: str) -> Optional[list[list[str]]]:
        if node_id not in self.nodes:
            return None
        return self.adjacency.get(node_id, [])

    def tag_stats(self, tag: str) -> Optional[dict[str, float]]:
        return self.data_stats.get(tag)

    def copy(self) -> "PlantState":
        return PlantState(
            tags=copy.deepcopy(self.tags),
            setpoints=copy.deepcopy(self.setpoints),
            nodes=copy.deepcopy(self.nodes),
            adjacency=copy.deepcopy(self.adjacency),
            data_stats=copy.deepcopy(self.data_stats),
            label=self.label,
        )


# ---------------------------------------------------------------------------
# Building the base state
# ---------------------------------------------------------------------------

def _load_kg() -> tuple[dict[str, dict], dict[str, list[list[str]]]]:
    with open(BOILER_KG, encoding="utf-8") as f:
        kg = json.load(f)
    nodes: dict[str, dict] = {}
    for n in kg.get("nodes", []):
        nid = n.get("node_id") or n.get("id")
        if nid:
            nodes[nid] = n
    adjacency: dict[str, set[tuple[str, str]]] = {nid: set() for nid in nodes}
    for e in kg.get("links", kg.get("edges", [])):
        s, t = e.get("source"), e.get("target")
        et = e.get("edge_type", "EDGE")
        if s in adjacency and t in nodes:
            adjacency[s].add((et, t))
        if t in adjacency and s in nodes:
            adjacency[t].add((et, s))  # undirected neighbourhood for structural fp
    adj_sorted = {nid: sorted([list(x) for x in pairs]) for nid, pairs in adjacency.items()}
    return nodes, adj_sorted


def load_base_state(with_data_stats: bool = False) -> PlantState:
    """Assemble the canonical base PlantState from the boiler agent's sources."""
    tags = {tag: dict(meta) for tag, meta in TAG_METADATA.items()}
    setpoints = {tag: dict(sp) for tag, sp in _clean_setpoints(ALARM_SETPOINTS).items()}
    nodes, adjacency = _load_kg()
    state = PlantState(tags=tags, setpoints=setpoints, nodes=nodes, adjacency=adjacency, label="base")
    if with_data_stats:
        state.data_stats = load_or_compute_data_stats()
    return state


def _clean_setpoints(raw: dict[str, dict]) -> dict[str, dict[str, float]]:
    """Strip non-numeric keys (description/units) so only setpoint levels remain."""
    out: dict[str, dict[str, float]] = {}
    for tag, sp in raw.items():
        levels = {k: float(v) for k, v in sp.items() if isinstance(v, (int, float))}
        out[tag] = levels
    return out


# ---------------------------------------------------------------------------
# Optional: historian distribution statistics (for distribution-drift scenarios)
# ---------------------------------------------------------------------------

def load_or_compute_data_stats() -> dict[str, dict[str, float]]:
    """Per-tag mean/std over the full historian window, cached to disk.

    Only needed for distribution-drift scenarios and ML-grounded knowledge.
    """
    cache = os.path.join(SNAPSHOT_DIR, "data_stats.json")
    if os.path.isfile(cache):
        with open(cache, encoding="utf-8") as f:
            return json.load(f)
    stats: dict[str, dict[str, float]] = {}
    try:
        import duckdb  # local import: only needed here
        con = duckdb.connect(HISTORIAN_DB, read_only=True)
        # Historian is wide-format: table historian_data with one column per tag.
        cols = {r[1] for r in con.execute("PRAGMA table_info('historian_data')").fetchall()}
        tags = [t for t in TAG_METADATA if t in cols]
        if tags:
            select = ", ".join(
                f'avg("{t}") AS "{t}__m", stddev_samp("{t}") AS "{t}__s"' for t in tags
            )
            row = con.execute(f"SELECT {select} FROM historian_data").fetchone()
            names = [d[0] for d in con.description]
            vals = dict(zip(names, row))
            for t in tags:
                stats[t] = {
                    "mean": float(vals.get(f"{t}__m") or 0.0),
                    "std": float(vals.get(f"{t}__s") or 0.0),
                }
        con.close()
    except Exception:
        # Historian shape unknown / unavailable -> leave stats empty; scenarios
        # that need them will synthesise instead.
        stats = {}
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    return stats
