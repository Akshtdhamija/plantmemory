# PlantMemory as a Management-of-Change tool for computational plants

*A research framing for the next phase of the project.*

---

## 1. What Management of Change is

In the process industries, **Management of Change (MOC)** is a formal safety
discipline: no change to a process may be made until it has been *described*, its
consequences *assessed*, and the change *authorised* by a competent person. It is a
core element of Process Safety Management (OSHA 29 CFR 1910.119(l)), of API RP 750,
and of the CCPS (Center for Chemical Process Safety) guidelines, and it exists
because most major process incidents trace back not to steady operation but to a
*change* whose consequences were not fully understood.

A workable way to classify what changes is by the **object of change**:

| Object | Examples | Classic MOC question |
|---|---|---|
| **Material** (physical / technical) | a recalibrated sensor, a new or modified piece of equipment, a different feedstock, a decommissioned instrument, a re-plumbed line | *Is the plant still safe and operable after this physical change?* |
| **Organisational** (procedural / people) | a revised operating limit, a new procedure, a changed staffing or shift structure, an operator who leaves | *Do the people and procedures still match how the plant now runs?* |

Only a change that is a **replacement-in-kind** (truly identical) is exempt.
Everything else must pass MOC.

## 2. Why MOC today is deliberately conservative

Conventional MOC is slow, manual, and paper-driven **by design**, and that works
because of an assumption that is now breaking:

> In a traditional plant, change is **rare, small, and physical**. A human reviewer
> can sit down, reason about the one thing that changed, and sign it off.

Because change is infrequent, a conservative gate is affordable: you can afford to
review everything, every time, by hand. The cost of that conservatism is low when
there are only a handful of changes a year.

## 3. What "change" becomes in a computational / AI-enabled plant

Process operation is becoming **computational**: plants increasingly run on
data-driven models, soft sensors, and simulation-run "digital twins". In that
world, the *definition of a change expands dramatically*:

- a sensor is **recalibrated**, shifting the baseline a model was tuned on;
- a control loop is **retuned**, moving a setpoint a diagnostic rule relied on;
- a **new feedstock** shifts the operating distribution a model assumes;
- a tag is **decommissioned** in a DCS migration, removing an input;
- a model is **retrained** or **re-versioned**.

These changes are **frequent, often silent, and software-paced** — not the rare,
visible, physical changes MOC was designed around. Each one can *invalidate encoded
knowledge* (a threshold, a baseline, a learned model, a diagnostic conclusion)
without anyone noticing. Manual, conservative MOC cannot keep up: you cannot
convene a review board every time a model drifts.

**So the open question is: what should MOC mean in a computational plant?** If a
change is now a recalibration or a distribution shift, then MOC's impact assessment
has to run at the speed and scale of software, and it has to answer a new question:
*which encoded knowledge does this change invalidate?*

## 4. PlantMemory's answer: MOC as a continuous, automatically-scoped control

PlantMemory turns the three steps of MOC into a mechanism that runs continuously
and touches only what a change affects.

| MOC step | Conventional (manual) | PlantMemory (automatic, scoped) |
|---|---|---|
| **Describe the change** | a change request form | a classified change object: *material* or *organisational*, with the facets it moves |
| **Assess the impact** | an engineer reasons by hand about consequences | drift detection computes *exactly* which knowledge the change invalidates, and by how much (confidence decay) |
| **Authorise** | a reviewer signs the paperwork | an auditable approval record in the MOC register, scoped to the assessed impact |

The key shift is in the **impact-assessment step**. Conventional MOC is conservative
because a human cannot cheaply trace the full consequence of a change, so it reviews
broadly and slowly. PlantMemory *grounds* each piece of knowledge to the plant
assets it depends on, so the consequence of a change is computed directly: a change
flags the knowledge tied to what it touched, and **provably nothing else** (see the
locality property in the project's formal write-up). Impact assessment stops being a
conservative manual gate and becomes an exact, instant, local computation.

### How the two MOC objects map onto the system

- **Material change** is handled by **drift detection**. A recalibration, upgrade,
  feedstock change, or decommissioning moves plant-state facets; PlantMemory
  fingerprints those facets, so it detects precisely which grounded knowledge is
  now in doubt. This is the Drift Explorer and the automatic impact assessment in
  the **Change (MOC)** view.
- **Organisational change** is handled by **retention and handover**. The classic
  organisational change — an experienced operator leaving with their know-how — is
  exactly the knowledge-loss this project exists to stop: the knowledge is written
  down, grounded, and retained, and the **Relay** (shift handoff) carries the live
  knowledge-health to the next person. MOC for an organisational change becomes
  "hand over the knowledge, intact and current," not "hope it was written down."

### The approval workflow

PlantMemory keeps MOC's human-authority boundary. A change is **raised** (an MOC
record is opened with its automatic impact assessment embedded), and a competent
person **approves or rejects** it. Nothing is auto-applied; the software prepares
the assessment, a human authorises the change. This mirrors MOC's originator →
reviewer → approver chain and leaves an auditable register.

## 5. The contribution, stated plainly

> Conventional Management of Change is conservative because, in a traditional plant,
> change is rare and physical and a human can reason about it by hand. As plants
> become computational, change becomes frequent, software-paced, and knowledge-
> invalidating. PlantMemory re-casts MOC for that world: it classifies the change,
> **automatically assesses which encoded knowledge the change invalidates** (and by
> how much), and records a scoped human authorisation — making MOC continuous and
> local instead of conservative and wholesale.

## 6. Where this sits on the roadmap

This framing is the research thesis for the **next phase** of the project. The
mid-semester work delivered the memory mechanism (grounding + drift) on one unit.
Casting that mechanism as the impact-assessment engine of MOC gives it a recognised
process-safety home and a clear industrial value proposition. The post-midsem
stages — automatic knowledge capture, threshold validation, and cross-unit
connection — are what take MOC-by-PlantMemory from one unit to a plant-wide,
transferable change-control layer.

---

### References

- OSHA, *Process Safety Management of Highly Hazardous Chemicals*, 29 CFR
  1910.119(l) — Management of Change.
- CCPS (Center for Chemical Process Safety), *Guidelines for the Management of
  Change for Process Safety*.
- API Recommended Practice 750, *Management of Process Hazards*.
- Practitioner resources on MOC classification and approval (e.g.
  safetydesigninc.com) informed the material/organisational framing used here.
