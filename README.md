# PlantMemory

**A knowledge-continuity and Management-of-Change layer for computational plant operation.**

Process plants run on hard-won operating knowledge — *"if the induced-draft fan
starts vibrating, the bearings are wearing out."* Today that knowledge lives in
people's heads and in brittle models, and it is **silently invalidated every time
the plant changes**: a recalibrated sensor, a new feedstock, an upgraded fan, a
decommissioned tag. The usual fix is to relearn or retrain from scratch, discarding
knowledge the change never touched.

PlantMemory makes that knowledge **survive change**. It *grounds* each piece of
knowledge to the exact plant assets it depends on, then *detects drift* when those
assets change — so a change invalidates **only what it actually touches**, and
everything else is kept. On top of that it provides a **Management of Change (MOC)**
workflow: classify a change, automatically assess which knowledge it invalidates,
and record a scoped human authorisation.

> Built and validated on a real coal-fired circulating-fluidised-bed (CFB) boiler.

---

## Quickstart — one command, live in your browser

PlantMemory's hub is almost pure Python standard library; its only runtime
dependency is PyYAML, and the data it needs is bundled. No database to set up.

```bash
git clone https://github.com/Akshtdhamija/plantmemory.git
cd plantmemory
pip install -r requirements.txt
python -m plant_memory hub
```

That starts the dashboard at **http://127.0.0.1:7700** and opens it in your browser.

### Even simpler

```bash
pip install -e .   # installs the `plantmemory` command
plantmemory        # starts the hub and opens the browser
```

### Zero local setup (Docker)

```bash
docker compose up
```

Then open **http://localhost:7700**. (Inside a container the hub binds `0.0.0.0`;
the port is mapped to your machine.)

---

## What you get

A local, single-page dashboard (nothing leaves `127.0.0.1`) with seven views:

| View | What it does |
|---|---|
| **Overview** | the plant's living memory at a glance; reacts to a simulated change |
| **Drift Explorer** | pick a plant change and watch which knowledge is flagged vs kept |
| **Change (MOC)** | classify a change (material / organisational), auto-assess the knowledge it invalidates, and authorise it with an auditable record |
| **Knowledge** | every diagnostic conclusion, grounded to plant assets, with cited procedures |
| **Plant Graph** | the change traced over the plant topology |
| **Inbox** | propose → review → approve new knowledge (human-authority boundary) |
| **Relays** | shift handoffs that carry the live knowledge-health to the next engineer |
| **Evaluation** | retention and the cost of change, across all scenarios |

## Management of Change

PlantMemory re-casts MOC for computational plants: conventional MOC is conservative
because change used to be rare and physical; as operation becomes computational,
change is frequent and knowledge-invalidating. PlantMemory makes the **impact
assessment automatic and local**, and keeps MOC's human authorisation. See
[docs/MANAGEMENT_OF_CHANGE.md](docs/MANAGEMENT_OF_CHANGE.md) for the full framing.

## How it works (in one paragraph)

Each knowledge entry is grounded to a set of **anchors** `g = (asset, facet)` — e.g.
*(IDF, vibration setpoints)*. Each anchor is reduced to a short, exact **fingerprint**
(a truncated SHA-256 of that facet). When the plant changes, PlantMemory recomputes
every fingerprint: a moved one marks the anchor *changed*, a vanished asset marks it
*missing*, and the entry takes the worst verdict. Because a fingerprint depends only
on its own facet, a change can only flag the knowledge that actually depended on what
moved — which is why, on the evaluation, flagged knowledge equals the truly-affected
knowledge exactly (precision = recall = 1.0) with a zero false-positive rate on an
unchanged plant.

## Architecture

```
plant_memory/
  schema.py         knowledge entry, grounding, drift types
  plant_state.py    the plant "world" (tags, setpoints, graph, distributions)
  fingerprint.py    per-facet fingerprints (the locality mechanism)
  drift.py          drift detection + confidence decay
  simulate.py       reproducible plant-change scenarios (classified for MOC)
  moc.py            Management-of-Change: impact assessment + approval register
  inbox.py          propose → review → approve knowledge
  relay.py          shift handoffs
  evaluate.py       retention + cost-of-change metrics and plots
  store.py          on-disk knowledge store
  hub.py            dependency-free local web hub (stdlib http.server)
  hub_static/       the single-page dashboard
  launch.py         `plantmemory` console entry point
```

Everything PlantMemory owns lives under `plant_memory/store/` as plain files, so the
team's grounded knowledge is easy to version in git.

## The testbed

The process data and structure come from an open-source, instrumented CFB-boiler
system by **Scott Duncan** (*Industrial AI Troubleshooting Assistant*,
github.com/ScottDuncanAI) — a historian, alarm log, process knowledge graph, and
plant documents. PlantMemory is the knowledge-continuity and MOC **layer on top of
it**. The small data files needed to run the hub (`tag_metadata.py`,
`alarm_metadata.py`, `boiler_kg.json`, and a precomputed statistics cache) are
bundled here; the full 5-day historian is not required at runtime.

## Developing / regenerating

The hub runs on `pyyaml` alone. Regenerating the evaluation plots or the statistics
cache needs the optional dev extras:

```bash
pip install -e ".[dev]"   # duckdb, matplotlib, numpy
```

## Roadmap

- **Done (first node):** the grounding + drift memory mechanism, validated on one
  unit, re-cast as the MOC impact-assessment engine.
- **Next:** automatic knowledge *capture* from investigations; *validation* of the
  drift thresholds (sensitivity of the ½σ multiplier); *cross-unit connection* so
  knowledge and change-control transfer between units.

## License

MIT — see [LICENSE](LICENSE).
