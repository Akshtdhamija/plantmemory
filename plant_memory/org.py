"""
Organisational Management of Change: knowledge-loss risk from people changes.

Grounded knowledge stays in the store when a person leaves, but it is only *useful*
while someone competent can re-validate it when the plant changes. So the
organisational quantity that matters is review capacity.

  qualified(e) = {author of e} U { p : systems(p) ∩ systems(e) ≠ ∅  and  years(p) >= s_min(e) }

with s_min = 8 years for diagnostic knowledge (root causes, failure modes) and 2 years
for documented procedures and conventions.

  coverage(a | Active) = sum_{e grounded to a} c_e * 1[ qualified(e) ∩ Active ≠ ∅ ] / sum_e c_e
  bus factor(a)        = smallest |L| such that coverage(a | People \\ L) < TAU
  KRI(a)               = criticality(a) * (1 - coverage after the change)

An organisational change (a departure, a role move) is assessed by recomputing
coverage with that person removed.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from . import plantdata
from .store import load_all

TAU = 0.5
S_MIN = {"root_cause": 8, "failure_mode": 8, "corrective_action": 5,
         "decision": 5, "convention": 2, "procedure": 2, "design_basis": 2}
PRIORITY_SCORE = {"Critical": 5, "High": 4, "Medium": 3, "Low": 2}


def _system_index():
    k = plantdata.kg()
    part = {l["source"]: l["target"] for l in k["links"] if l["edge_type"] == "PART_OF"}
    ntype = {n["node_id"]: n["node_type"] for n in k["nodes"]}

    def system(a):
        seen = 0
        while a in part and ntype.get(a) != "System" and seen < 5:
            a, seen = part[a], seen + 1
        return a if ntype.get(a) == "System" else None
    return system


def entry_assets(e) -> set[str]:
    return {g.ref for g in e.groundings}


def entry_systems(e, system=None) -> set[str]:
    system = system or _system_index()
    return {s for s in (system(a) for a in entry_assets(e)) if s}


def qualified(e, people, system=None) -> set[str]:
    sys_e = entry_systems(e, system)
    q = {p["id"] for p in people
         if set(p["systems"]) & sys_e and p["years"] >= S_MIN.get(e.category, 5)}
    author = (e.author or "").split(" ")[0]
    if author in {p["id"] for p in people}:
        q.add(author)
    elif e.source == "seed":
        q.add("P01")              # seeded tacit know-how was written by the senior engineer
    return q


def criticality() -> dict[str, int]:
    sp, prio, _ = plantdata.setpoints()
    return {t: max(PRIORITY_SCORE[prio[l]] for l in levels) for t, levels in sp.items() if levels}


def coverage(active: set[str], entries=None, people=None) -> dict[str, float]:
    entries = entries if entries is not None else load_all()
    people = people or plantdata.roster()
    system = _system_index()
    num, den = defaultdict(float), defaultdict(float)
    for e in entries:
        held = bool(qualified(e, people, system) & active)
        for a in entry_assets(e):
            den[a] += e.confidence
            num[a] += e.confidence * held
    return {a: num[a] / den[a] for a in den if den[a] > 0}


def bus_factor(max_k: int = 3) -> dict[str, int]:
    people = plantdata.roster()
    ids = {p["id"] for p in people}
    entries = load_all()
    base = coverage(ids, entries, people)
    bf = {a: max_k + 1 for a in base}
    for k in range(1, max_k + 1):
        for leave in combinations(sorted(ids), k):
            cov = coverage(ids - set(leave), entries, people)
            for a, c in cov.items():
                if c < TAU and bf[a] > k:
                    bf[a] = k
    return bf


def assess_departure(person_id: str) -> dict:
    """Organisational MOC impact of one person leaving."""
    people = plantdata.roster()
    ids = {p["id"] for p in people}
    entries = load_all()
    system = _system_index()
    before = coverage(ids, entries, people)
    after = coverage(ids - {person_id}, entries, people)
    crit = criticality()
    orphaned = [e for e in entries
                if qualified(e, people, system) and not (qualified(e, people, system) - {person_id})]
    exposed = sorted(((a, before[a], after.get(a, 0.0)) for a in before
                      if after.get(a, 0.0) < before[a] - 1e-9),
                     key=lambda x: -(crit.get(x[0], 1) * (1 - x[2])))
    successors = defaultdict(set)
    for e in orphaned:
        for p in people:
            if p["id"] != person_id and set(p["systems"]) & entry_systems(e, system):
                successors[e.id].add(p["id"])
    person = next((p for p in people if p["id"] == person_id), {})
    return {
        "person": person,
        "orphaned_entries": [{"id": e.id, "title": e.title, "category": e.category,
                              "train": sorted(successors[e.id])} for e in orphaned],
        "assets_exposed": [{"asset": a, "coverage_before": round(b, 2),
                            "coverage_after": round(c, 2),
                            "KRI": round(crit.get(a, 1) * (1 - c), 2)} for a, b, c in exposed],
        "below_tau": sum(1 for a, _, c in exposed if c < TAU),
    }
