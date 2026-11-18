"""
Drift detection — the heart of PlantMemory.

Given the current PlantState, evaluate every stored knowledge entry: for each of
its groundings, recompute the fingerprint and compare it to the one captured
when the knowledge was written. Classify each grounding as intact / changed /
missing, then roll up to an entry-level health verdict.

Crucially this is a *review signal*, not a delete signal. A flagged entry is not
"wrong" — it is "the plant condition it relied on has moved; a human should
re-confirm it." That distinction is what lets a plant keep its accumulated
knowledge across change instead of relearning from scratch.
"""
from __future__ import annotations

from .fingerprint import MISSING, fingerprint
from .plant_state import PlantState
from .schema import (
    DriftStatus,
    EntryDrift,
    EntryHealth,
    Grounding,
    GroundingDrift,
    KnowledgeEntry,
)


def stamp_groundings(state: PlantState, groundings: list[Grounding]) -> list[Grounding]:
    """Fill in each grounding's fingerprint from `state` (used at capture time)."""
    for g in groundings:
        g.fingerprint = fingerprint(state, g.kind, g.ref, g.aspect)
    return groundings


def _describe_change(g: Grounding, state: PlantState, status: str) -> str:
    if status == DriftStatus.MISSING:
        if g.kind == "tag":
            return f"tag {g.ref} no longer present in the plant configuration"
        return f"knowledge-graph node '{g.ref}' has been removed"
    if status == DriftStatus.CHANGED:
        if g.aspect == "normal_range":
            lo, hi = state.tag_range(g.ref)
            return f"normal operating range of {g.ref} is now {lo}–{hi}"
        if g.aspect == "setpoints":
            sp = state.tag_setpoints(g.ref) or {}
            return f"alarm setpoints of {g.ref} retuned to {sp}"
        if g.aspect == "distribution":
            st = state.tag_stats(g.ref) or {}
            return f"operating distribution of {g.ref} shifted (mean≈{st.get('mean')})"
        if g.aspect == "connections":
            return f"process connections of '{g.ref}' changed (equipment reconfigured)"
        if g.aspect == "presence":
            return f"identity/type of {g.ref} changed"
    return ""


def evaluate_entry(entry: KnowledgeEntry, state: PlantState) -> EntryDrift:
    grounding_drifts: list[GroundingDrift] = []
    for g in entry.groundings:
        new_fp = fingerprint(state, g.kind, g.ref, g.aspect)
        if new_fp == MISSING:
            status = DriftStatus.MISSING
        elif new_fp == "unverified" or g.fingerprint == "unverified":
            status = DriftStatus.UNVERIFIED
        elif new_fp == g.fingerprint:
            status = DriftStatus.INTACT
        else:
            status = DriftStatus.CHANGED
        detail = _describe_change(g, state, status) if status in (
            DriftStatus.CHANGED, DriftStatus.MISSING) else ""
        grounding_drifts.append(
            GroundingDrift(
                grounding=g, status=status,
                old_fingerprint=g.fingerprint, new_fingerprint=new_fp, detail=detail,
            )
        )

    # roll-up
    has_missing = any(d.status == DriftStatus.MISSING for d in grounding_drifts)
    has_changed = any(d.status == DriftStatus.CHANGED for d in grounding_drifts)
    if has_missing:
        health = EntryHealth.BROKEN
    elif has_changed:
        health = EntryHealth.REVIEW
    else:
        health = EntryHealth.INTACT

    confidence = _decayed_confidence(entry, grounding_drifts)
    return EntryDrift(
        entry_id=entry.id, title=entry.title, health=health,
        groundings=grounding_drifts, confidence=confidence,
    )


def _decayed_confidence(entry: KnowledgeEntry, drifts: list[GroundingDrift]) -> float:
    """Reduce confidence in proportion to how much of the grounding drifted."""
    if not drifts:
        return entry.confidence
    penalty = 0.0
    for d in drifts:
        if d.status == DriftStatus.MISSING:
            penalty += 0.6
        elif d.status == DriftStatus.CHANGED:
            penalty += 0.35
    frac = penalty / len(drifts)
    return round(max(0.0, entry.confidence * (1.0 - min(frac, 1.0))), 3)


def evaluate_all(entries: list[KnowledgeEntry], state: PlantState) -> list[EntryDrift]:
    return [evaluate_entry(e, state) for e in entries]


def summarize(drifts: list[EntryDrift]) -> dict:
    total = len(drifts)
    intact = sum(1 for d in drifts if d.health == EntryHealth.INTACT)
    review = sum(1 for d in drifts if d.health == EntryHealth.REVIEW)
    broken = sum(1 for d in drifts if d.health == EntryHealth.BROKEN)
    return {
        "total": total,
        "intact": intact,
        "review": review,
        "broken": broken,
        "flagged": review + broken,
        "flagged_fraction": round((review + broken) / total, 3) if total else 0.0,
        "retained_fraction": round(intact / total, 3) if total else 0.0,
    }
