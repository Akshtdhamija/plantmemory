"""
Corpus builder: grounded knowledge from the plant's own document library.

The mid-semester corpus was fourteen entries written by one author. Here every
troubleshooting guide, maintenance procedure, equipment datasheet and control-
loop description in the plant library becomes a grounded knowledge entry, owned
by the role that owns that document type. Only the document *index* is used
(document id, type, title, revision, equipment and sensor tags); no document text
is read or reproduced.

Which facets a document depends on follows from what kind of document it is:

  troubleshooting : tag normal ranges + alarm setpoints, equipment presence
  controls        : tag setpoints + operating distributions, equipment wiring
  maintenance     : tag presence, equipment presence + wiring
  datasheet       : tag presence + design ranges, equipment presence + wiring
"""
from __future__ import annotations

from . import plantdata
from .drift import stamp_groundings
from .plant_state import load_base_state
from .schema import Grounding, KnowledgeEntry
from .store import load_all, save_entry

FACETS = {
    "troubleshooting": (("normal_range", "setpoints"), ("presence",)),
    "controls": (("setpoints", "distribution"), ("connections",)),
    "maintenance": (("presence",), ("presence", "connections")),
    "datasheet": (("presence", "normal_range"), ("presence", "connections")),
}
CATEGORY = {"troubleshooting": "failure_mode", "controls": "convention",
            "maintenance": "procedure", "datasheet": "design_basis"}
CONFIDENCE = {"troubleshooting": 0.8, "controls": 0.85, "maintenance": 0.85,
              "datasheet": 0.9}


def owner_of(doc_type: str) -> str:
    for p in plantdata.roster():
        if doc_type in p.get("owns_doc_types", []):
            return f"{p['id']} {p['role']}"
    return "plant library"


def build(write: bool = True) -> list[KnowledgeEntry]:
    base = load_base_state(with_data_stats=True)
    existing = {e.id for e in load_all()}
    out = []
    for d in plantdata.documents():
        dt = d["doc_type"]
        if dt not in FACETS:
            continue                       # SOPs and safety docs are procedure nodes
        tag_f, eq_f = FACETS[dt]
        g = []
        for t in d.get("tags", []):
            if base.tag_exists(t):
                g += [Grounding(kind="tag", ref=t, aspect=f,
                                note=f"{d['doc_id']} relies on {t} {f}") for f in tag_f]
        for n in d.get("equipment", []):
            if base.node_exists(n):
                g += [Grounding(kind="kg_node", ref=n, aspect=f,
                                note=f"{d['doc_id']} relies on {n} {f}") for f in eq_f]
        if not g:
            continue
        eid = f"kp-{d['doc_id']}"
        eq = ", ".join(d.get("equipment", [])[:4]) or "the unit"
        e = KnowledgeEntry(
            id=eid, title=d["title"], category=CATEGORY[dt],
            statement=(f"Documented {dt} knowledge ({d['doc_id']}, Rev {d['revision']}) "
                       f"for {eq}; valid only while the referenced plant facets hold."),
            groundings=g, evidence=[f"{d['doc_id']} Rev {d['revision']}"],
            confidence=CONFIDENCE[dt], tags_referenced=list(d.get("tags", [])),
            source="library", author=owner_of(dt),
            provenance={"doc_id": d["doc_id"], "doc_type": dt, "revision": d["revision"]},
        )
        stamp_groundings(base, e.groundings)
        if write and eid not in existing:
            save_entry(e)
        out.append(e)
    return out
