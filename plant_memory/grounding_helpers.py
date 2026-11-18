"""
Grounding inference — turn free text (an investigation summary, a decision note)
into concrete plant groundings by recognizing tag names and knowledge-graph nodes.
"""
from __future__ import annotations

import re

from .plant_state import PlantState, load_base_state
from .schema import Grounding

_TAG_RE = re.compile(r"\b([A-Z]{2,6}_?\d{3,4}[A-Z]?|[A-Z]{4,8})\b")


def infer_groundings(text: str, state: PlantState | None = None,
                     extra_tags: list[str] | None = None) -> list[Grounding]:
    state = state or load_base_state(with_data_stats=True)
    found_tags: set[str] = set(extra_tags or [])
    for m in _TAG_RE.finditer(text or ""):
        tok = m.group(1)
        if state.tag_exists(tok):
            found_tags.add(tok)

    groundings: list[Grounding] = []
    for tag in sorted(found_tags):
        # Always ground presence; add richer facets where they carry meaning.
        groundings.append(Grounding("tag", tag, "presence"))
        lo, hi = state.tag_range(tag)
        if lo is not None or hi is not None:
            groundings.append(Grounding("tag", tag, "normal_range"))
        if state.tag_setpoints(tag):
            groundings.append(Grounding("tag", tag, "setpoints"))

    # Match knowledge-graph nodes by name keyword.
    low = (text or "").lower()
    for node_id, node in state.nodes.items():
        name = (node.get("name") or "").lower()
        if node.get("node_type") in ("Equipment", "System", "ControlLoop") and name:
            key = name.split("(")[0].strip()
            if key and len(key) > 4 and key in low:
                groundings.append(Grounding("kg_node", node_id, "presence"))
    return groundings
