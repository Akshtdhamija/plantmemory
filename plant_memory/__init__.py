"""
PlantMemory — institutional memory for industrial AI troubleshooting.

A knowledge-continuity layer that sits on top of the boiler troubleshooting
agent. Diagnostic conclusions (root causes, corrective actions, evidence) are
stored as canonical, human-readable Markdown, each one *grounded* to specific
plant assets — sensor tags, equipment, and knowledge-graph nodes — and stamped
with a fingerprint of the plant conditions it was derived under.

When the plant changes (a sensor is recalibrated, equipment is upgraded, a
setpoint is retuned, the process distribution drifts), PlantMemory recomputes
those fingerprints and flags exactly which stored knowledge is now stale —
without discarding everything. This is the direct answer to the question
"when a component changes, must the system relearn from scratch?": no, only the
knowledge grounded to what actually changed is flagged for review.

Modules
-------
plant_state : snapshot of the plant's ground-truth configuration + overrides
schema      : data structures for knowledge entries, groundings, drift results
fingerprint : deterministic fingerprints of grounded plant state
store       : canonical Markdown (+YAML frontmatter) persistence
drift       : the drift checker — classify each grounding intact/changed/missing
capture     : turn an agent audit trace into a grounded knowledge entry
inbox       : propose -> review -> approve workflow for knowledge
relay       : shift-handover / onboarding context batons
simulate    : reproducible plant-change scenarios
evaluate    : knowledge-retention / cost-of-change metrics
seed        : seed the store with realistic diagnostic knowledge
cli         : command-line interface
"""

__version__ = "0.1.0"

from .paths import KNOWLEDGE_DIR, INBOX_DIR, RELAY_DIR, PLANTMEM_DIR  # noqa: F401
