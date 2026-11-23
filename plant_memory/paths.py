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

# Source data files (from the boiler testbed, read-only for us). The bundled
# copies under data/ are preferred so every experiment reproduces from a clone.
DATA_DIR = os.path.join(PROJECT_DIR, "data")
BOILER_KG = os.path.join(PROJECT_DIR, "boiler_kg.json")


def _prefer_data(name: str) -> str:
    bundled = os.path.join(DATA_DIR, name)
    return bundled if os.path.isfile(bundled) else os.path.join(PROJECT_DIR, name)


HISTORIAN_DB = _prefer_data("boiler_historian.duckdb")
ALARM_DB = _prefer_data("boiler_alarms.duckdb")
DOC_INDEX = os.path.join(DATA_DIR, "doc_index.json")   # document metadata only, no content
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")      # experiment outputs (figures, json)
ROSTER = os.path.join(DATA_DIR, "roster.json")          # people / roles (synthetic, labelled)


def ensure_dirs() -> None:
    for d in (PLANTMEM_DIR, KNOWLEDGE_DIR, INBOX_DIR, RELAY_DIR, EVAL_DIR,
              SNAPSHOT_DIR, MOC_DIR):
        os.makedirs(d, exist_ok=True)
