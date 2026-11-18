"""
Fingerprinting — the mechanism that makes drift detection localized.

For each Grounding (an asset + a facet of that asset), we compute a short,
deterministic fingerprint from the current PlantState. Two states that agree on
that facet produce the same fingerprint; any change produces a different one.

Because fingerprints are per-facet, a change to (say) the IDF vibration trip
setpoint only alters the fingerprint of groundings anchored to
`tag:YFJ3_ZD1:setpoints` — every other piece of knowledge stays intact. That
locality is the whole point: knowledge is invalidated surgically, not wholesale.
"""
from __future__ import annotations

import hashlib
import json
from typing import Optional

from .plant_state import PlantState
from .schema import AnchorKind

# A "MISSING" sentinel fingerprint distinguishes "asset gone" from "facet changed".
MISSING = "∅"


def _hash(payload) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def fingerprint(state: PlantState, kind: str, ref: str, aspect: str) -> str:
    """Return the fingerprint of one grounding facet under `state`."""
    if kind == AnchorKind.TAG:
        return _tag_fingerprint(state, ref, aspect)
    if kind == AnchorKind.KG_NODE:
        return _node_fingerprint(state, ref, aspect)
    raise ValueError(f"unknown anchor kind: {kind}")


# ---------------------------------------------------------------------------
# Tag facets
# ---------------------------------------------------------------------------

def _tag_fingerprint(state: PlantState, tag: str, aspect: str) -> str:
    if not state.tag_exists(tag):
        return MISSING

    if aspect == "presence":
        t = state.tags[tag]
        return _hash(["tag", tag, t.get("sensor_type"), t.get("units")])

    if aspect == "normal_range":
        lo, hi = state.tag_range(tag)
        return _hash(["range", _round(lo), _round(hi)])

    if aspect == "setpoints":
        sp = state.tag_setpoints(tag) or {}
        return _hash(["setpoints", {k: _round(v) for k, v in sorted(sp.items())}])

    if aspect == "distribution":
        st = state.tag_stats(tag)
        if not st:
            return "unverified"
        # Quantize the mean against the tag's own std (its natural noise scale) so
        # a shift larger than ~half a sigma trips drift, but ordinary run-to-run
        # noise does not. Quantize std against the mean to catch spread changes.
        # Cross-scaling avoids the scale-invariance trap of self-referential steps.
        mean = float(st.get("mean") or 0.0)
        std = float(st.get("std") or 0.0)
        m_scale = max(abs(std) * 0.5, abs(mean) * 1e-3, 1e-9)   # ~0.5 sigma
        s_scale = max(abs(mean) * 0.02, abs(std) * 1e-3, 1e-9)  # ~2% of mean
        return _hash(["dist", round(mean / m_scale), round(std / s_scale)])

    raise ValueError(f"unknown tag aspect: {aspect}")


# ---------------------------------------------------------------------------
# Knowledge-graph node facets
# ---------------------------------------------------------------------------

def _node_fingerprint(state: PlantState, node_id: str, aspect: str) -> str:
    if not state.node_exists(node_id):
        return MISSING

    if aspect == "presence":
        n = state.node(node_id)
        return _hash(["node", node_id, n.get("node_type"), n.get("name")])

    if aspect == "connections":
        neigh = state.node_neighbors(node_id) or []
        return _hash(["conn", node_id, sorted(neigh)])

    raise ValueError(f"unknown node aspect: {aspect}")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _round(v: Optional[float]) -> Optional[float]:
    if v is None:
        return None
    return round(float(v), 4)
