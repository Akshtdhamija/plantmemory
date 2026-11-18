"""Canonical filesystem layout for PlantMemory."""
from __future__ import annotations

import os

# Project root = parent of this package
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Everything PlantMemory owns lives under plant_memory/store so it is easy to
# commit as canonical team memory (mirroring how MEX keeps memory in-repo).
PLANTMEM_DIR = os.path.join(PROJECT_DIR, "plant_memory", "store")

KNOWLEDGE_DIR = os.path.join(PLANTMEM_DIR, "knowledge")   # canonical grounded knowledge
INBOX_DIR = os.path.join(PLANTMEM_DIR, "inbox")           # proposed additions/corrections
RELAY_DIR = os.path.join(PLANTMEM_DIR, "relays")          # shift handoffs
EVAL_DIR = os.path.join(PLANTMEM_DIR, "evaluation")       # metrics + plots
SNAPSHOT_DIR = os.path.join(PLANTMEM_DIR, "snapshots")    # captured plant-state snapshots
MOC_DIR = os.path.join(PLANTMEM_DIR, "moc")               # management-of-change records

# Source data files (owned by the boiler agent, read-only for us)
BOILER_KG = os.path.join(PROJECT_DIR, "boiler_kg.json")
HISTORIAN_DB = os.path.join(PROJECT_DIR, "boiler_historian.duckdb")


def ensure_dirs() -> None:
    for d in (PLANTMEM_DIR, KNOWLEDGE_DIR, INBOX_DIR, RELAY_DIR, EVAL_DIR,
              SNAPSHOT_DIR, MOC_DIR):
        os.makedirs(d, exist_ok=True)
