# PlantMemory

**Computable Management of Change for computational chemical plants.**

Every change to a process plant must pass **Management of Change (MOC)**: describe the
change, assess its impact, authorise it (OSHA 29 CFR 1910.119(l), CCPS, API RP 750).
MOC today is conservative and manual because its central step, impact assessment, is
human reasoning, which was affordable when changes were rare and physical. In a plant
that runs on models, change is continuous: recalibrations, setpoint retunes, new
feedstock, model updates, staff turnover. Each silently invalidates knowledge,
procedures, alarms and models.

PlantMemory makes the impact assessment of MOC **computable** and keeps the
authorisation **human**. It grounds the plant's knowledge to the exact assets and
facets it depends on, computes the change itself, propagates it through a
data-calibrated process graph, and tells you exactly what must be re-confirmed: which
knowledge, which procedures, which alarm limits (with an alarm replay over real plant
data), which models, and which people. It then tiers the risk, routes sign-offs,
generates the MOC package, verifies the change afterwards and detects changes that
skipped MOC. Every decision is deterministic and auditable; nothing opaque approves
anything.

> Built and validated on a real coal-fired circulating-fluidised-bed (CFB) boiler:
> 5 days x 30 tags of historian data, 6,005 ISA-18.2 alarms, a 75-node process graph and
> 62 plant documents.

---

## Quickstart (one command, live in your browser)

```bash
git clone https://github.com/Akshtdhamija/plantmemory.git
cd plantmemory
pip install -r requirements.txt
python -m plant_memory hub
```

The dashboard opens at **http://127.0.0.1:7700**. Open **Change (MOC)** and pick a change.
Deep links work too, for example `http://127.0.0.1:7700/?view=moc&scenario=kpi_rerate`.

Other ways to run it: `pip install -e . && plantmemory`, or `docker compose up`
(then open http://localhost:7700).

## What one MOC assessment computes

| Step | How |
|---|---|
| **The change itself** | Δ(S, S') = every (asset, facet) whose fingerprint moved. Empty Δ ⟹ provably a *replacement in kind* (exempt) |
| **Knowledge to re-validate** | entries grounded to a moved facet, with confidence decay. Exact: precision = recall = 1 |
| **Procedures to revise** | documents that reference a moved facet, by document type |
| **Alarm limits** | changed limits plus an **alarm replay** of the ISA-18.2 state machine over the historian with the proposed limits (activations, standing time, margin in σ) |
| **Physical propagation** | max-product paths through the process graph, strengths calibrated on historian data, each item with its explaining path |
| **Models** | a PCA / T² / SPE monitoring model grounded to its inputs: valid, revalidate, or broken |
| **People** | qualified reviewers; for organisational change, who is left able to re-validate what |
| **Risk and approvals** | R = S × L on a 5 × 5 matrix → Minor / Moderate / Major / Major + HAZOP, required sign-off roles, PSSR |

Then the workflow: in review → approved → implemented → PSSR → verified against plant data
→ closed, with temporary/emergency changes, an exportable MOC package, and a
hash-chained audit log that detects tampering.

## Results (all reproducible: `python -m plant_memory.experiments`)

| | Result |
|---|---|
| Localisation (59 entries × 9 changes) | 0 false positives on the unchanged plant; precision = recall = 1.00; 87 % of knowledge kept; 87 % re-validation effort saved |
| MOC coverage | a full assessment surfaces 309 review items vs 69 for knowledge alone (procedures, alarms, models, disturbed assets) |
| Propagation, held-out days | data-calibrated MAP 0.352 vs graph prior 0.202 vs random 0.153 |
| Alarm replay | reproduces all 6,005 logged alarms exactly; shows the KPI re-rate would place the Hi limit inside normal operation (activations 5 → 55, standing time 0.8 h → 30 h) |
| Changes without MOC | wander-normalised detector: 0.6 false alarms/tag/day, detects 3σ shifts +79 pp above chance within ~45 min |
| MOC for AI models | PlantMemory's verdict matches the model's real behaviour, incl. an 18.6× false-alarm inflation flagged in advance |
| Organisational change | tacit knowledge alone leaves 6 flue-gas assets with a bus factor of 1; with the grounded corpus the minimum is 3 |
| Scaling | effort saved grows from 85 % to 99.5 % as the plant grows from 1 to 32 units |

## Architecture

```
plant_memory/
  plantdata.py      historian, alarm log, graph, setpoints, document index, roster
  fingerprint.py    per-facet fingerprints (the locality mechanism)
  drift.py          drift verdicts and confidence decay
  mocgraph.py       computed change set, physical graph, max-product propagation
  calibrate.py      lagged cross-correlation calibration + held-out validation
  alarm_replay.py   vectorised ISA-18.2 replay with proposed limits
  impact.py         full MOC impact assessment, risk tiering, approver routing
  moc.py            workflow, sign-offs, PSSR, verification, package, audit chain
  unmanaged.py      change detection without MOC and post-change verification
  model_moc.py      PCA / T² / SPE monitoring model under change control
  org.py            organisational MOC: review capacity, bus factor, KRI
  corpus.py         grounded knowledge from the plant document index
  experiments.py    E1 to E8, writes results/ and results/figures/
  hub.py, hub_static/   the local web hub
```

## Data and credit

The process data and structure come from an open-source instrumented CFB-boiler
testbed by **Scott Duncan** (github.com/ScottDuncanAI). They are bundled under `data/`
(historian, alarm log, document *index* only) so every result reproduces from a clean
clone. The people roster in `data/roster.json` is **synthetic** and labelled as such.
PlantMemory is the layer on top. See [docs/MANAGEMENT_OF_CHANGE.md](docs/MANAGEMENT_OF_CHANGE.md).

## License

MIT, see [LICENSE](LICENSE).
