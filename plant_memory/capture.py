"""
Capture — turn an agent investigation into grounded, durable knowledge.

The boiler agent already writes an audited root-cause report (summary.md /
report.md) at the end of an investigation. Capture reads that output, extracts
the root-cause conclusion and corrective actions, infers the plant groundings,
stamps fingerprints against the current plant state, and produces a
KnowledgeEntry ready for review. This is how one-off investigations become
institutional memory.
"""
from __future__ import annotations

import os
import re

from .drift import stamp_groundings
from .grounding_helpers import infer_groundings
from .plant_state import load_base_state
from .schema import KnowledgeEntry
from .store import next_id, now_iso, save_entry


def capture_manual(title: str, statement: str, *, category: str = "root_cause",
                   body: str = "", corrective_actions: list[str] | None = None,
                   confidence: float = 0.8, author: str = "agent",
                   session: str = "", evidence: list[str] | None = None,
                   extra_tags: list[str] | None = None,
                   save: bool = True) -> KnowledgeEntry:
    base = load_base_state(with_data_stats=True)
    text = " ".join([title, statement, body] + (corrective_actions or []))
    groundings = infer_groundings(text, base, extra_tags=extra_tags)
    stamp_groundings(base, groundings)
    entry = KnowledgeEntry(
        id=next_id(), title=title, category=category, statement=statement,
        body=body, corrective_actions=corrective_actions or [], groundings=groundings,
        evidence=evidence or [], confidence=confidence,
        tags_referenced=sorted({g.ref for g in groundings if g.kind == "tag"}),
        source="agent", author=author, session=session, created_at=now_iso(),
    )
    if save:
        save_entry(entry)
    return entry


# ---------------------------------------------------------------------------
# Parse an audit summary.md written by the boiler agent
# ---------------------------------------------------------------------------

def capture_from_summary(summary_path: str, *, author: str = "agent",
                         session: str = "", save: bool = True) -> KnowledgeEntry:
    with open(summary_path, encoding="utf-8") as f:
        text = f.read()

    title = _first_heading(text) or "Captured investigation"
    root_cause = _extract_after(text, r"root cause", default="")
    actions = _extract_bullets_after(text, r"corrective action")
    statement = root_cause or title
    return capture_manual(
        title=title, statement=statement, category="root_cause",
        body=text.strip()[:4000], corrective_actions=actions,
        author=author, session=session,
        evidence=[os.path.basename(summary_path)], save=save,
    )


def _first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _extract_after(text: str, label_re: str, default: str = "") -> str:
    m = re.search(rf"{label_re}[:\s]*\**\s*(.+)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip().rstrip("*").strip()
    return default


def _extract_bullets_after(text: str, label_re: str) -> list[str]:
    m = re.search(rf"{label_re}", text, re.IGNORECASE)
    if not m:
        return []
    tail = text[m.end():]
    bullets = re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", tail, re.MULTILINE)
    return [b.strip() for b in bullets[:8]]
