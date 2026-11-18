# PlantMemory

**Institutional memory for industrial AI.** A knowledge-continuity layer that
sits on top of the boiler troubleshooting agent. Every diagnostic conclusion is
stored as durable, human-readable Markdown and *grounded* to the specific plant
assets it relied on — sensor tags, alarm setpoints, equipment, and
knowledge-graph nodes. When the plant changes, PlantMemory recomputes those
groundings and flags **only** the knowledge tied to what changed — so a plant
keeps its accumulated expertise across recalibrations, upgrades, retunes, and
process drift instead of relearning from scratch.

> Research question (from the project brief): *when an AI component or the
> process it serves changes, must the system relearn everything from scratch?*
> PlantMemory's answer, made measurable: **no — knowledge is invalidated
> surgically, not wholesale.**

## Why it matters

| Distributed-AI lifecycle question | PlantMemory mechanism |
| --- | --- |
| Does a change force relearning everything? | Grounding + drift → localized invalidation |
| How does a new engineer get "blended in"? | Relay handoffs + explorable grounded Wiki |
| Which knowledge is now stale after a change? | Per-asset drift status (intact/review/broken) |
| What is the cost of absorbing change? | Evaluation harness: targeted vs relearn-from-scratch |

## Concepts

- **Knowledge entry** — a durable diagnostic conclusion (root cause, failure
  mode, corrective action, decision), stored as Markdown + YAML frontmatter.
- **Grounding** — an anchor tying a claim to a facet of a plant asset:
  a tag's `normal_range` / `setpoints` / `distribution` / `presence`, or a
  KG node's `presence` / `connections`.
- **Fingerprint** — a deterministic hash of a grounded facet under the current
  plant state. Drift = the fingerprint moved.
- **Drift** — per-grounding `intact | changed | missing`, rolled up to an entry
  verdict `intact | review | broken`. A review flag is a *signal to re-confirm*,
  not a delete.
- **Inbox** — propose → human review → approve into canonical memory.
- **Relay** — a shift-handover / onboarding "context baton" carrying the
  currently flagged knowledge and a tag watch-list.

## Quick start

Uses only dependencies already in the project venv (pyyaml, duckdb, numpy,
matplotlib). From the project root:

```bash
# seed a realistic grounded knowledge corpus
.venv/Scripts/python -m plant_memory seed

# see drift when the steam-temperature KPI is re-rated
.venv/Scripts/python -m plant_memory drift --scenario kpi_rerate

# run the full evaluation (cost model + figures)
.venv/Scripts/python -m plant_memory evaluate

# launch the web dashboard
.venv/Scripts/python -m plant_memory hub
```

On macOS/Linux use `.venv/bin/python` instead of `.venv/Scripts/python`.

## The Hub (web UI)

`python -m plant_memory hub` opens a local dashboard (127.0.0.1 only):

- **Overview** — corpus health and the available change scenarios.
- **Drift Explorer** — pick a plant change; watch the retention gauge and see
  each flagged entry with the exact reason it drifted.
- **Knowledge** — search/filter the grounded corpus; open any entry to inspect
  its groundings and drift.
- **Plant Graph** — the plant topology with grounded assets highlighted; a
  change lights up the assets it disturbs.
- **Inbox** — review and approve/reject proposed knowledge.
- **Relays** — create, take, and close shift handoffs.
- **Evaluation** — cost-of-change figures and the knowledge×change drift matrix.

## Change scenarios

Reproducible plant changes used as experimental treatments (see
`plant_memory/simulate.py`): `kpi_rerate`, `idf_bearing_upgrade`, `o2_recal`,
`new_feedstock`, `economizer_replacement`, `drum_setpoint_retune`,
`sensor_decommission`.

## Layout

```
plant_memory/
  plant_state.py     assemble the plant's ground-truth config (+ overrides)
  schema.py          knowledge / grounding / drift data structures
  fingerprint.py     deterministic per-facet fingerprints
  drift.py           the drift checker
  store.py           canonical Markdown persistence
  seed.py            realistic seed knowledge
  capture.py         audit-trace -> grounded knowledge
  inbox.py           propose/review/approve
  relay.py           shift handoffs
  simulate.py        plant-change scenarios
  evaluate.py        retention / cost metrics + figures
  hub.py             local web dashboard (stdlib server)
  hub_static/        dashboard front-end
  cli.py             command-line interface
  store/             canonical knowledge, inbox, relays, evaluation output
```

All canonical files under `store/` are plain text and meant to be committed to
Git — that is the sharing layer, the same way a plant team would share memory.
