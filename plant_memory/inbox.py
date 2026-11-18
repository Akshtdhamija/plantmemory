"""
Inbox — the propose -> review -> approve path for knowledge.

An agent (or engineer) drafts a knowledge addition or correction. It stays a
local proposal until a human explicitly approves it; approval promotes it into
the canonical knowledge store with fingerprints stamped against the current
plant state. This mirrors MEX's human-approval boundary: an agent can prepare,
but a person controls what becomes shared truth.
"""
from __future__ import annotations

import glob
import json
import os

from .drift import stamp_groundings
from .paths import INBOX_DIR, ensure_dirs
from .plant_state import load_base_state
from .schema import KnowledgeEntry
from .store import next_id, now_iso, save_entry


def _path(proposal_id: str) -> str:
    return os.path.join(INBOX_DIR, f"{proposal_id}.json")


def _next_proposal_id() -> str:
    ensure_dirs()
    existing = glob.glob(os.path.join(INBOX_DIR, "prop-*.json"))
    nums = [int(os.path.basename(p).split("-")[1].split(".")[0]) for p in existing
            if os.path.basename(p).split("-")[1].split(".")[0].isdigit()]
    return f"prop-{(max(nums) + 1) if nums else 1:04d}"


def draft_proposal(entry: KnowledgeEntry, *, proposer: str = "agent",
                   kind: str = "addition", target_entry_id: str = "",
                   rationale: str = "") -> dict:
    """Create a pending proposal. `kind` is 'addition' or 'correction'."""
    ensure_dirs()
    pid = _next_proposal_id()
    record = {
        "proposal_id": pid,
        "status": "pending",
        "kind": kind,
        "target_entry_id": target_entry_id,
        "proposer": proposer,
        "rationale": rationale,
        "created_at": now_iso(),
        "decided_at": "",
        "decided_by": "",
        "entry": entry.to_dict(),
    }
    with open(_path(pid), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return record


def list_proposals(status: str | None = None) -> list[dict]:
    ensure_dirs()
    out = []
    for p in sorted(glob.glob(os.path.join(INBOX_DIR, "prop-*.json"))):
        with open(p, encoding="utf-8") as f:
            rec = json.load(f)
        if status is None or rec.get("status") == status:
            out.append(rec)
    return out


def get_proposal(pid: str) -> dict | None:
    p = _path(pid)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def approve_proposal(pid: str, *, approver: str = "reviewer") -> KnowledgeEntry:
    rec = get_proposal(pid)
    if not rec:
        raise KeyError(pid)
    if rec["status"] != "pending":
        raise ValueError(f"proposal {pid} is {rec['status']}, not pending")
    entry = KnowledgeEntry.from_dict(rec["entry"])
    # (Re)stamp groundings against the CURRENT plant state at approval time.
    base = load_base_state(with_data_stats=True)
    stamp_groundings(base, entry.groundings)
    if rec["kind"] == "correction" and rec.get("target_entry_id"):
        entry.id = rec["target_entry_id"]          # overwrite the corrected entry
    elif not entry.id or entry.id.startswith("prop"):
        entry.id = next_id()
    entry.source = "inbox"
    save_entry(entry)
    rec.update(status="approved", decided_at=now_iso(), decided_by=approver,
               approved_entry_id=entry.id)
    with open(_path(pid), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)
    return entry


def reject_proposal(pid: str, *, reviewer: str = "reviewer", reason: str = "") -> dict:
    rec = get_proposal(pid)
    if not rec:
        raise KeyError(pid)
    rec.update(status="rejected", decided_at=now_iso(), decided_by=reviewer,
               reject_reason=reason)
    with open(_path(pid), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)
    return rec
