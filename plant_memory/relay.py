"""
Relay — the shift-handover / onboarding context baton.

A Relay packages what the next person on shift (or a newly joined engineer) needs
to continue safely: a summary, the knowledge currently flagged for review, a
watch-list of tags, next actions, and the observed plant/repo state. It is a
durable handoff, not a chat message — it travels with the repository via Git.

This is the human side of knowledge continuity: it answers the professor's
"how does a new person get blended in?" — they take the baton and inherit the
accumulated, grounded context instead of starting cold.
"""
from __future__ import annotations

import glob
import json
import os
import subprocess

from .drift import evaluate_all
from .paths import RELAY_DIR, PROJECT_DIR, ensure_dirs
from .plant_state import load_base_state
from .schema import EntryHealth
from .simulate import get_scenario
from .store import load_all, now_iso


def _path(relay_id: str) -> str:
    return os.path.join(RELAY_DIR, f"{relay_id}.json")


def _next_relay_id() -> str:
    ensure_dirs()
    existing = glob.glob(os.path.join(RELAY_DIR, "relay-*.json"))
    nums = [int(os.path.basename(p).split("-")[1].split(".")[0]) for p in existing
            if os.path.basename(p).split("-")[1].split(".")[0].isdigit()]
    return f"relay-{(max(nums) + 1) if nums else 1:04d}"


def _observed_state() -> dict:
    """Best-effort Git snapshot (branch, HEAD, dirty flag)."""
    def _git(*args):
        try:
            return subprocess.run(["git", *args], cwd=PROJECT_DIR,
                                  capture_output=True, text=True, timeout=10).stdout.strip()
        except Exception:
            return ""
    return {
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "head": _git("rev-parse", "--short", "HEAD"),
        "dirty": bool(_git("status", "--porcelain")),
        "timestamp": now_iso(),
    }


def build_handoff_context(scenario: str | None = None) -> dict:
    """Compute the current knowledge health to embed in a relay."""
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    state = get_scenario(scenario).apply(base) if scenario else base
    drifts = evaluate_all(entries, state)
    flagged = [
        {"entry_id": d.entry_id, "title": d.title, "health": d.health,
         "confidence": d.confidence,
         "reasons": [g.detail for g in d.groundings if g.detail]}
        for d in drifts if d.is_flagged
    ]
    watch_tags = sorted({
        g.grounding.ref for d in drifts for g in d.groundings
        if g.status != "intact" and g.grounding.kind == "tag"
    })
    return {"under_change": scenario, "flagged": flagged, "watch_tags": watch_tags,
            "flagged_count": len(flagged), "corpus_size": len(entries)}


def create_relay(*, title: str, summary: str, from_member: str,
                 to: str = "team", next_actions: list[str] | None = None,
                 scenario: str | None = None) -> dict:
    ensure_dirs()
    rid = _next_relay_id()
    record = {
        "relay_id": rid,
        "status": "open",
        "title": title,
        "summary": summary,
        "from_member": from_member,
        "to": to,
        "next_actions": next_actions or [],
        "context": build_handoff_context(scenario),
        "observed_state": _observed_state(),
        "created_at": now_iso(),
        "taken_by": "",
        "taken_at": "",
        "closed_at": "",
        "log": [f"{now_iso()} created by {from_member}"],
    }
    with open(_path(rid), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return record


def list_relays(status: str | None = None) -> list[dict]:
    ensure_dirs()
    out = []
    for p in sorted(glob.glob(os.path.join(RELAY_DIR, "relay-*.json"))):
        with open(p, encoding="utf-8") as f:
            rec = json.load(f)
        if status is None or rec.get("status") == status:
            out.append(rec)
    return out


def get_relay(rid: str) -> dict | None:
    p = _path(rid)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _save(rec: dict) -> None:
    with open(_path(rec["relay_id"]), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)


def take_relay(rid: str, member: str) -> dict:
    rec = get_relay(rid)
    if not rec:
        raise KeyError(rid)
    if rec["status"] != "open":
        raise ValueError(f"relay {rid} is {rec['status']}, cannot take")
    rec.update(status="taken", taken_by=member, taken_at=now_iso())
    rec["log"].append(f"{now_iso()} taken by {member}")
    _save(rec)
    return rec


def close_relay(rid: str, member: str) -> dict:
    rec = get_relay(rid)
    if not rec:
        raise KeyError(rid)
    if rec["status"] not in ("taken", "open"):
        raise ValueError(f"relay {rid} is {rec['status']}, cannot close")
    rec.update(status="closed", closed_at=now_iso())
    rec["log"].append(f"{now_iso()} closed by {member}")
    _save(rec)
    return rec
