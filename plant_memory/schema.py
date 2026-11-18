"""
Data structures for PlantMemory knowledge and drift.

A KnowledgeEntry is a durable diagnostic conclusion. Each entry is *grounded*
to one or more plant assets via Grounding anchors. Every anchor carries a
fingerprint of the plant state it depended on at capture time; drift detection
recomputes those fingerprints against the current state.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Grounding
# ---------------------------------------------------------------------------

class AnchorKind(str, Enum):
    TAG = "tag"          # a sensor tag (ref = tag name, e.g. "TE_8332A")
    KG_NODE = "kg_node"  # an equipment/system/sensor node (ref = node_id)


# Which facet of the asset the knowledge depends on.
TAG_ASPECTS = ("presence", "normal_range", "setpoints", "distribution")
NODE_ASPECTS = ("presence", "connections")


@dataclass
class Grounding:
    """A single anchor tying a knowledge claim to a facet of a plant asset."""
    kind: str            # AnchorKind value
    ref: str             # tag name or node_id
    aspect: str          # facet of the asset (see *_ASPECTS)
    fingerprint: str = ""       # fingerprint of that facet at capture time
    note: str = ""              # human note: why this grounding matters

    def key(self) -> str:
        return f"{self.kind}:{self.ref}:{self.aspect}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Grounding":
        return cls(
            kind=d["kind"], ref=d["ref"], aspect=d["aspect"],
            fingerprint=d.get("fingerprint", ""), note=d.get("note", ""),
        )


# ---------------------------------------------------------------------------
# Knowledge entry
# ---------------------------------------------------------------------------

CATEGORIES = (
    "failure_mode",       # a known way the plant fails
    "root_cause",         # a diagnosed cause from an investigation
    "corrective_action",  # what to do about a condition
    "convention",         # operating convention / rule of thumb
    "decision",           # a recorded engineering decision
)


@dataclass
class KnowledgeEntry:
    id: str
    title: str
    category: str
    statement: str                                 # one-line plain conclusion
    body: str = ""                                 # full markdown explanation
    corrective_actions: list[str] = field(default_factory=list)
    groundings: list[Grounding] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)   # citations / trace step refs
    confidence: float = 0.8                        # 0..1 at capture time
    status: str = "active"                          # active | archived | superseded
    tags_referenced: list[str] = field(default_factory=list)
    source: str = "manual"                          # audit_trace | manual | inbox | seed
    author: str = "unknown"
    session: str = ""
    created_at: str = ""
    updated_at: str = ""
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["groundings"] = [g.to_dict() for g in self.groundings]
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "KnowledgeEntry":
        d = dict(d)
        d["groundings"] = [Grounding.from_dict(g) for g in d.get("groundings", [])]
        known = cls.__dataclass_fields__.keys()
        return cls(**{k: v for k, v in d.items() if k in known})


# ---------------------------------------------------------------------------
# Drift results
# ---------------------------------------------------------------------------

class DriftStatus(str, Enum):
    INTACT = "intact"     # fingerprint matches current state
    CHANGED = "changed"   # asset still exists but the depended-on facet changed
    MISSING = "missing"   # asset (tag/node) no longer exists
    UNVERIFIED = "unverified"  # could not evaluate (e.g. stats unavailable)


# entry-level roll-up
class EntryHealth(str, Enum):
    INTACT = "intact"     # every grounding intact
    REVIEW = "review"     # >=1 grounding changed (needs human review, not discard)
    BROKEN = "broken"     # >=1 grounding missing (asset gone)


@dataclass
class GroundingDrift:
    grounding: Grounding
    status: str            # DriftStatus value
    old_fingerprint: str
    new_fingerprint: str
    detail: str = ""       # human-readable what-changed

    def to_dict(self) -> dict[str, Any]:
        return {
            "grounding": self.grounding.to_dict(),
            "status": self.status,
            "old_fingerprint": self.old_fingerprint,
            "new_fingerprint": self.new_fingerprint,
            "detail": self.detail,
        }


@dataclass
class EntryDrift:
    entry_id: str
    title: str
    health: str                          # EntryHealth value
    groundings: list[GroundingDrift] = field(default_factory=list)
    confidence: float = 0.0              # decayed confidence after drift

    @property
    def n_changed(self) -> int:
        return sum(1 for g in self.groundings if g.status == DriftStatus.CHANGED)

    @property
    def n_missing(self) -> int:
        return sum(1 for g in self.groundings if g.status == DriftStatus.MISSING)

    @property
    def is_flagged(self) -> bool:
        return self.health != EntryHealth.INTACT

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "title": self.title,
            "health": self.health,
            "confidence": self.confidence,
            "n_changed": self.n_changed,
            "n_missing": self.n_missing,
            "groundings": [g.to_dict() for g in self.groundings],
        }
