"""
Management of Change (MOC) — PlantMemory as a change-control tool.

In a chemical plant, any change to the process must pass through Management of
Change: the change is described, its impact is assessed, and it is formally
approved before it takes effect (OSHA PSM 1910.119(l); API RP 750). The object
of change is usually classed as **material** (a physical / technical change —
equipment, instrument, feedstock) or **organisational** (a procedural, operating-
spec, or people change).

Conventional MOC is deliberately conservative and manual, because in a
traditional plant change is rare and small, and a human can reason about its
consequences. But when operation runs on computational models, "change" also
means a recalibration, a retune, a new feedstock distribution, a decommissioned
tag — changes that are frequent and that silently invalidate encoded knowledge.
Reviewing each one by hand does not scale.

This module turns PlantMemory's drift detection into the **impact-assessment**
step of MOC, and its human approval into the **authorisation** step:

  1. classify the change (material / organisational);
  2. automatically assess which knowledge the change invalidates, and how badly
     (confidence decay), using the same grounding + drift engine;
  3. record an auditable MOC entry with a disposition (approved / rejected).

So MOC stops being a conservative manual gate and becomes a continuous,
automatically-scoped control that touches only the knowledge a change affects.
"""
from __future__ import annotations

import glob
import json
import os

from .drift import evaluate_all
from .paths import MOC_DIR, ensure_dirs
from .plant_state import load_base_state
from .simulate import SCENARIOS, get_scenario
from .store import load_all, now_iso

# MOC object vocabulary -----------------------------------------------------
MATERIAL = "material"
ORGANISATIONAL = "organisational"


def _next_moc_id() -> str:
    ensure_dirs()
    existing = glob.glob(os.path.join(MOC_DIR, "moc-*.json"))
    nums = [int(os.path.basename(p).split("-")[1].split(".")[0]) for p in existing
            if os.path.basename(p).split("-")[1].split(".")[0].isdigit()]
    return f"moc-{(max(nums) + 1) if nums else 1:04d}"


def _path(moc_id: str) -> str:
    return os.path.join(MOC_DIR, f"{moc_id}.json")


# ---------------------------------------------------------------------------
# Impact assessment (the automated MOC review step)
# ---------------------------------------------------------------------------

def assess(scenario_name: str) -> dict:
    """Assess the knowledge impact of a proposed change (an MOC review).

    Returns the change classification plus the list of knowledge entries the
    change would invalidate, with their new health and confidence. This is the
    impact-assessment a reviewer would otherwise do by hand.
    """
    sc = get_scenario(scenario_name)
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    after = sc.apply(base)

    before = {d.entry_id: d for d in evaluate_all(entries, base)}
    drifts = evaluate_all(entries, after)

    impacted = []
    for d in drifts:
        health = getattr(d.health, "value", d.health)
        if health == "intact":
            continue
        c0 = before[d.entry_id].confidence if d.entry_id in before else None
        impacted.append({
            "entry_id": d.entry_id,
            "title": d.title,
            "health": health,                         # review | broken
            "confidence_before": c0,
            "confidence_after": d.confidence,
            "reasons": [g.detail for g in d.groundings if g.detail],
        })
    # worst first: broken before review, then larger confidence drop
    impacted.sort(key=lambda x: (x["health"] != "broken",
                                 (x["confidence_before"] or 0) - (x["confidence_after"] or 0)),
                  reverse=False)

    n_broken = sum(1 for x in impacted if x["health"] == "broken")
    n_review = sum(1 for x in impacted if x["health"] == "review")
    corpus = len(entries)
    disposition = _recommend(n_broken, n_review, corpus)

    return {
        "scenario": scenario_name,
        "moc_object": getattr(sc, "moc_object", "material"),
        "moc_class": getattr(sc, "moc_class", "Technical change"),
        "kind": sc.kind,
        "description": sc.description,
        "corpus_size": corpus,
        "impacted_count": len(impacted),
        "n_broken": n_broken,
        "n_review": n_review,
        "unaffected": corpus - len(impacted),
        "impacted": impacted,
        "recommendation": disposition,
    }


def _recommend(n_broken: int, n_review: int, corpus: int) -> dict:
    """A simple, explainable disposition recommendation for the reviewer."""
    if n_broken:
        level = "action-required"
        text = (f"{n_broken} knowledge item(s) depend on an asset this change "
                f"removes. Re-author or retire them before the change is authorised.")
    elif n_review:
        level = "review"
        text = (f"{n_review} knowledge item(s) must be re-confirmed against the new "
                f"plant state. The rest of the corpus is unaffected and carries over.")
    else:
        level = "clear"
        text = "No encoded knowledge depends on what this change touches. Clear to proceed."
    return {"level": level, "text": text}


# ---------------------------------------------------------------------------
# MOC register (the authorisation + audit record)
# ---------------------------------------------------------------------------

def raise_moc(scenario_name: str, *, originator: str = "engineer",
              title: str = "", reason: str = "") -> dict:
    """Open an MOC record for a change, embedding its impact assessment."""
    ensure_dirs()
    a = assess(scenario_name)
    mid = _next_moc_id()
    sc = SCENARIOS.get(scenario_name)
    record = {
        "moc_id": mid,
        "status": "open",                 # open | approved | rejected
        "title": title or (sc.description if sc else scenario_name),
        "scenario": scenario_name,
        "moc_object": a["moc_object"],
        "moc_class": a["moc_class"],
        "originator": originator,
        "reason": reason,
        "assessment": a,
        "decided_by": "",
        "decision_note": "",
        "created_at": now_iso(),
        "decided_at": "",
    }
    with open(_path(mid), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return record


def decide_moc(moc_id: str, *, decision: str, approver: str = "approver",
               note: str = "") -> dict:
    """Authorise (approve) or reject an open MOC record."""
    rec = get_moc(moc_id)
    if rec is None:
        raise KeyError(f"unknown MOC record '{moc_id}'")
    if decision not in ("approved", "rejected"):
        raise ValueError("decision must be 'approved' or 'rejected'")
    rec["status"] = decision
    rec["decided_by"] = approver
    rec["decision_note"] = note
    rec["decided_at"] = now_iso()
    with open(_path(moc_id), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)
    return rec


def get_moc(moc_id: str) -> dict | None:
    p = _path(moc_id)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def list_moc(status: str | None = None) -> list[dict]:
    ensure_dirs()
    out = []
    for p in sorted(glob.glob(os.path.join(MOC_DIR, "moc-*.json"))):
        with open(p, encoding="utf-8") as f:
            rec = json.load(f)
        if status and rec.get("status") != status:
            continue
        out.append(rec)
    out.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return out
