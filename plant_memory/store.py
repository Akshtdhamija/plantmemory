"""
Canonical persistence — knowledge lives as human-readable Markdown with a YAML
frontmatter header (the same "canonical Markdown, rebuildable indexes" idea MEX
uses). A person can open, read, and review any entry in a text editor; Git is
the sharing layer.
"""
from __future__ import annotations

import glob
import os
import re
from datetime import datetime, timezone
from typing import Optional

import yaml

from .paths import KNOWLEDGE_DIR, ensure_dirs
from .schema import Grounding, KnowledgeEntry

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def entry_to_markdown(e: KnowledgeEntry) -> str:
    meta = e.to_dict()
    body = meta.pop("body", "") or ""
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).rstrip()
    md = [f"---\n{front}\n---\n", f"# {e.title}\n", f"**{e.statement}**\n"]
    if body.strip():
        md.append(body.strip() + "\n")
    if e.corrective_actions:
        md.append("## Recommended corrective actions\n")
        md.extend(f"{i}. {a}" for i, a in enumerate(e.corrective_actions, 1))
        md.append("")
    if e.groundings:
        md.append("## Grounded to\n")
        for g in e.groundings:
            note = f" — {g.note}" if g.note else ""
            md.append(f"- `{g.kind}:{g.ref}` ({g.aspect}){note}")
        md.append("")
    return "\n".join(md).rstrip() + "\n"


def markdown_to_entry(text: str) -> KnowledgeEntry:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("file has no YAML frontmatter")
    meta = yaml.safe_load(m.group(1)) or {}
    # The narrative body below the frontmatter is regenerated from fields, so we
    # keep the authoritative 'body' field from frontmatter if present.
    return KnowledgeEntry.from_dict(meta)


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def _path_for(entry_id: str) -> str:
    return os.path.join(KNOWLEDGE_DIR, f"{entry_id}.md")


def save_entry(e: KnowledgeEntry) -> str:
    ensure_dirs()
    if not e.created_at:
        e.created_at = now_iso()
    e.updated_at = now_iso()
    path = _path_for(e.id)
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry_to_markdown(e))
    return path


def load_entry(entry_id: str) -> Optional[KnowledgeEntry]:
    path = _path_for(entry_id)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return markdown_to_entry(f.read())


def load_all() -> list[KnowledgeEntry]:
    ensure_dirs()
    entries = []
    for path in sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            try:
                entries.append(markdown_to_entry(f.read()))
            except Exception as exc:  # skip malformed, keep going
                print(f"[plant_memory] skipping {os.path.basename(path)}: {exc}")
    return entries


def next_id(prefix: str = "km") -> str:
    ensure_dirs()
    existing = glob.glob(os.path.join(KNOWLEDGE_DIR, f"{prefix}-*.md"))
    nums = []
    for p in existing:
        m = re.search(rf"{prefix}-(\d+)", os.path.basename(p))
        if m:
            nums.append(int(m.group(1)))
    return f"{prefix}-{(max(nums) + 1) if nums else 1:04d}"


def delete_entry(entry_id: str) -> bool:
    path = _path_for(entry_id)
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False
