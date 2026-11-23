# PlantMemory, final phase: Computable Management of Change

**Technical plan for approval.** Nothing below is built yet. Once you approve (with
any changes), I build it work package by work package, push each one to GitHub, and
then we write the final BTP report from the results.

---

## 0. Where we stand after mid-sem

**What exists and works**
- Grounding + per-facet fingerprints + drift verdicts + confidence decay.
- 14 knowledge entries, 7 change scenarios, 98-cell grid: zero false positives,
  precision = recall = 1.0, 89.8% re-validation effort saved.
- MOC v0: each change classed material / organisational, knowledge impact shown,
  a raise / approve / reject register.
- Public repo with a one-command launch: github.com/Akshtdhamija/plantmemory.

**What an examiner will push on (and what this phase fixes)**

| Weakness today | Fixed by |
|---|---|
| Corpus is 14 hand-written entries by one author | WP1: corpus built from the plant's 62 documents, many owners |
| MOC only looks at *knowledge*. Real MOC must also cover procedures, alarms, drawings, models, training | WP2, WP3: one dependency graph over all of them |
| Impact is exact but only "who references this asset". No physical propagation (an IDF change also disturbs furnace draft and O2) | WP3, WP4: process propagation, calibrated on historian data |
| No validation on real plant behaviour, only on scenarios we wrote | WP4: validated against 6,005 real alarm events |
| ½σ threshold never tested | WP7: sensitivity study with injected changes, ROC curves |
| MOC is one click. Real MOC has risk ranking, tiers, multiple sign-offs, PSSR, closure | WP5, WP6 |
| Nothing happens after approval, and changes that skip MOC are invisible | WP7: post-change verification + unmanaged-change detection |
| "What does MOC mean for AI?" is answered only in words | WP9: a real process-monitoring model put under MOC |
| Organisational change is only a story | WP8: quantified knowledge-loss risk when people change |

---

## 1. The final thesis

**Working title:** *Computable Management of Change for computational chemical plants*

**Thesis in one paragraph.** Management of Change is conservative today because its
central step, impact assessment, is a manual reasoning task, and that was affordable
when plant changes were rare and physical. In a computational plant, change is
continuous: recalibrations, setpoint retunes, feedstock shifts, model updates, staff
turnover. Each one silently invalidates knowledge, procedures, alarms and models. This
project makes the impact assessment of MOC **computable**. It represents the plant,
its knowledge, procedures, alarms, models and people as one dependency graph calibrated
on plant data. It propagates a proposed change through that graph to get a ranked,
explainable impact set, derives a risk tier and the required approvers, generates the
MOC package, verifies the change after implementation, and detects changes that
bypassed MOC. Authorisation stays with people.

**Research questions**
- **RQ1 (coverage).** Can the full impact of a plant change (knowledge, procedures,
  alarms, models, people) be computed from a dependency graph, exactly and with an
  explanation for each item?
- **RQ2 (physics).** Can physical impact propagation be calibrated from historian data
  and validated against real disturbance propagation in the alarm log?
- **RQ3 (closing the loop).** Can a change that bypassed MOC be detected from operating
  data, how fast, and at what false-alarm cost?
- **RQ4 (AI).** What does MOC mean for the models a computational plant runs on, and
  can model validity be tied to plant change?
- **RQ5 (people).** Can the knowledge-loss risk of an organisational change be
  quantified before the change happens?

**Direct answers to the professor's questions** (these become a section of the report)

| Professor's point | Our answer |
|---|---|
| MOC objects: material and organisational | Both are modelled as first-class change objects with their own impact channels (WP2, WP8) |
| MOC is conservative because change is small and rare | It stays manual because impact assessment is human reasoning. We compute it, so MOC can scale to frequent change |
| What would change mean in AI-enabled processes | Three things: (a) far more changes need MOC (software-paced changes); (b) AI models are themselves assets under MOC (WP9); (c) MOC itself becomes computational in its assessment step |
| MOC does not use AI | Deliberate design choice: the core is deterministic and auditable (graph, rules, statistics). No black box approves anything. Any text drafting is optional, labelled, and off by default. This is what makes it acceptable under process-safety regulation |
| Approval for MOC | Risk-tiered, multi-role sign-off with a tamper-evident audit trail (WP5, WP6) |

---

## 2. The two MOC objects, modelled fully

**Material (physical / technical) changes**
equipment modification or replacement, instrument recalibration or decommissioning,
setpoint and alarm-limit changes, feedstock / raw-material changes, control-logic
changes, **model changes** (new or retrained process models).

**Organisational changes**
a person or role leaving, shift-structure change, responsibility transfer, procedure
revision.

**MOC types** (following CCPS practice)
- **Permanent**: the normal path.
- **Temporary**: carries an expiry date; the system tracks it and escalates when it
  goes overdue (a classic failure mode is a temporary change quietly becoming
  permanent).
- **Emergency**: implemented first, retrospective review due within a fixed window.
- **Replacement-in-kind (RIK)**: exempt from MOC. New idea: RIK is **computed, not
  judged**. If every facet fingerprint of the new item equals the old one, it is
  provably in-kind; if any facet differs, it is not RIK and must go through MOC.

---

## 3. System architecture (final)

```
DATA
  historian (86,400 rows x 30 tags)   alarm log (6,005 events, ISA-18.2)
  knowledge graph (75 nodes / 154 edges)   62 plant documents (type, revision, tags, equipment)
  knowledge store   people roster   model registry
        |
MOC DEPENDENCY GRAPH  (new: one typed graph over everything above)
        |
ENGINES
  grounding + fingerprints (existing, generalised to every node type)
  impact propagation (new)        data calibration of propagation (new)
  risk + tiering + approver routing (new)
  alarm replay for setpoint changes (new)
  MOC package generator (new)     audit chain (new)
  post-change verification (new)  unmanaged-change detector (new)
  organisational-change engine (new)   model MOC (new)
        |
WORKFLOW  draft -> assessed -> in review -> approved/rejected -> implemented
          -> PSSR -> verified -> closed     (+ temporary expiry, emergency retro-review)
        |
HUB (web UI) + CLI + exportable MOC packages
```

**Node types in the MOC graph**

| Node | Source | Facets fingerprinted |
|---|---|---|
| Equipment | knowledge graph | presence, connections |
| Tag / instrument | tag metadata, historian | presence, range, distribution |
| Alarm / setpoint | alarm setpoint register | limits, priority |
| Procedure section | 62 documents (SOPs, maintenance, safety) | revision, section content |
| Knowledge entry | knowledge store + corpus builder | groundings (as today) |
| Model | model registry | input tags, training-distribution fingerprint, version, limits |
| Person / role | roster | role, active, ownerships, training |

**Edge types**: `measures`, `controls`, `flows_to` (process stream), `references`
(document or knowledge to asset), `grounded_in`, `alarms_on`, `trained_on`,
`owns`, `trained_for`, `mitigates`.

---

## 4. Work packages

### WP1. Data and corpus expansion  *(the "capture" stage from the mid-sem roadmap)*
- Bundle the historian and alarm databases into the repo under `data/` (about 11 MB)
  with a loader, so every experiment is reproducible from a clean clone.
- **Corpus builder**: turn the 13 troubleshooting and 13 maintenance documents into
  grounded knowledge entries automatically, using each document's sensor-tag and
  equipment metadata for grounding and its revision as evidence. Target: 60 to 100
  entries with many authors (document owners), up from 14 by one author.
- **Procedures as nodes**: every SOP / maintenance / safety document becomes a node,
  fingerprinted by revision, so "which procedures must be revised" falls out of the
  same mechanism.
- **People roster**: about 12 realistic roles (four shift engineers, control engineer,
  instrument technician, maintenance planner, process-safety lead, model owner, etc.)
  with ownership and training links. Clearly labelled synthetic.
- *Deliverable:* `python -m plant_memory corpus build`, expanded store, tests.

### WP2. The MOC dependency graph
- Typed node / edge schema (tables above) and a builder that merges every source.
- Generalise fingerprints from tags and graph nodes to all node types (documents by
  revision, models by training-distribution fingerprint, people by role and status).
- *Deliverable:* `mocgraph.py`, graph stats, graph view in the hub.

### WP3. Impact propagation engine  *(core contribution, RQ1)*
Two channels, combined into one ranked impact set with an explanation per item:
1. **Dependency channel (exact).** Everything that references a changed facet:
   knowledge, procedure sections, alarms, models, owners. Exact, via fingerprints,
   inherits today's locality guarantee.
2. **Process channel (graded).** A change to an asset disturbs downstream process
   variables along process streams. Score of node v:

   s(v) = max over paths p from the change to v of  ∏ w_e  (e in p)

   computed exactly with Dijkstra on edge costs −log w_e, cut off below a threshold θ.
   Items that depend on a disturbed variable inherit its score.
- Every impacted item carries its path, for example:
  `IDF bearing+VFD -> furnace draft (PT_8313x) -> flue-gas O2 (AIR_8301A) -> entry "low O2 means incomplete combustion"`.
- *Why max-product and not sum or noisy-OR:* stays in [0, 1], never double-counts
  parallel paths, has an exact fast algorithm, and the most-likely path is itself the
  explanation an engineer reads. (Full derivation goes in the handbook v2.)

### WP4. Data calibration of propagation  *(chemical-engineering core, RQ2)*
- Edge weights from the historian using **lagged cross-correlation** between connected
  tags on detrended signals, with lag direction required to agree with the process
  flow direction, and a significance cut |ρ| > z / √N_eff. This follows established
  plant-wide disturbance propagation analysis (Bauer and Thornhill 2008; Yang, Duan,
  Shah and Chen 2014). Transfer entropy as an optional comparison.
- **Validation against reality, the alarm log.** For each alarm on tag u, which other
  tags alarm within a window after it, beyond their base rate (lift). That is an
  empirical propagation ground truth from 6,005 real events.
- Compare three predictors of "what does a disturbance at u reach": (i) same-system
  heuristic, (ii) graph hop distance, (iii) data-calibrated graph. Metrics:
  precision@k, recall@k, NDCG, Spearman rank correlation.

### WP5. Risk assessment, tiering and approver routing
- **Severity S (1 to 5)** from the most critical impacted asset: alarm priority tiers
  already in the setpoint register (Trip / HiHiHi / LoLo = Critical), safety
  interlocks, the KPI tag.
- **Likelihood L (1 to 5)** from change type, historical alarm frequency of the
  impacted tags (alarm log), and change magnitude relative to the operating spread
  (a setpoint moved by z standard deviations).
- **Risk R = S × L** on a 5 × 5 matrix gives the tier: RIK (computed, exempt) / Minor
  (one approver) / Major (multidisciplinary review + PSSR) / Emergency path.
- **Approver routing**: required sign-off roles derived from impacted domains (process,
  instrumentation, operations, safety, maintenance, model owner).
- **Alarm replay for setpoint changes** (strong, quantitative feature): rerun the
  ISA-18.2 alarm state machine the project already has, over the 5-day historian,
  with the *proposed* setpoints. Output: how many extra alarms, how many alarm-flood
  intervals, how much less margin to trip. A setpoint MOC gets a measured consequence,
  not an opinion.
- Every score shows its contributors (no unexplained numbers).

### WP6. MOC workflow, package and audit trail
- State machine: draft -> assessed -> in review (parallel role sign-offs) ->
  approved / rejected -> implemented -> PSSR -> verified -> closed. Temporary changes
  with expiry and overdue escalation; emergency changes with retro-review deadline.
- **MOC package export** (Markdown + PDF): description, technical basis, risk matrix,
  ranked impact set with paths, procedure sections to revise (doc id + revision),
  alarms to re-rationalise, knowledge to re-validate, models to re-validate, people to
  inform or train, a PSSR checklist built from the plant's own pre-startup safety SOP,
  and a sign-off table.
- **Tamper-evident audit chain**: h_i = SHA-256(h_(i−1) ‖ record_i). Any edited
  record breaks the chain and is detected.
- Optional text drafting with a language model: off by default, clearly labelled,
  never part of a decision.

### WP7. Post-change verification and unmanaged-change detection  *(RQ3)*
- **Verification.** After a change is marked implemented at t0, compare predicted
  against observed: did the impacted tags shift as expected; did anything *outside*
  the impact set drift? An unanticipated drift reopens the MOC.
- **Unmanaged-change detector.** Rolling windows over the historian; per-tag
  distribution fingerprints (the ½σ bins) plus a CUSUM test on the mean (Page 1954).
  A detected change on an asset with no open or approved MOC raises
  *"change detected without MOC"*, a leading cause of process incidents.
- **Sensitivity study (promised at mid-sem).** Inject synthetic step, ramp and
  sensor-bias changes of 0.25σ to 3σ at random times into copies of the historian.
  Measure detection rate, false alarms per day on clean data, and detection delay, for
  k = 0.25, 0.5, 1, 2. ROC curves either justify ½σ or tell us the better value.

### WP8. Organisational MOC  *(RQ5)*
- Coverage of an asset = sum of confidence of its knowledge held by *active* owners.
- **Bus factor** of an asset = smallest number of people whose departure drops its
  coverage below a threshold. A **Knowledge Risk Index** per asset.
- Simulate a senior shift engineer leaving: which assets lose coverage, which entries
  become orphaned, which procedures lose their owner, and an automatically generated
  handover (Relay) and training plan. Framed on CCPS guidance for organisational
  change.

### WP9. MOC for AI models  *(RQ4, the clearest answer to "MOC in the AI world")*
- Train a real process-monitoring model on normal historian data: PCA with
  Hotelling T² and SPE control limits, the standard multivariate SPC model in process
  engineering. Register it as an asset with facets (input tags, training-distribution
  fingerprint, version, limits).
- A plant change that moves its inputs makes it invalid: PlantMemory flags "model
  revalidation required" inside the MOC, **before** it misbehaves.
- Experiment: apply the feedstock change and measure how the model's false-alarm rate
  inflates. Show PlantMemory flagged it in advance.
- Updating the model is itself a change that goes through MOC (impact: the alarms and
  decisions it drives).

### WP10. Cross-unit transfer  *(stretch; the third mid-sem roadmap stage)*
- A second boiler configuration (different equipment and setpoints). Compare
  fingerprints across units to show which knowledge transfers intact and which needs
  review before it is reused.

### WP11. Product: the hub, rebuilt around MOC
- **MOC dashboard** (home): open changes by state, overdue temporary changes, pending
  sign-offs, unmanaged-change alerts.
- **New change request** form (object, type, assets, temporary/permanent, description).
- **Impact view**: propagation graph with highlighted paths, ranked lists by category
  (knowledge, procedures, alarms, models, people).
- **Risk view**: 5 × 5 matrix with contributors; alarm replay results.
- **Sign-off panel**, **package export**, **verification view**, **organisational
  change view**, **model registry**. Existing views stay.
- Stretch: public live demo (Docker image on a free host) so examiners can open a link.

### WP12. Engineering and GitHub
- The standalone repo becomes the single source of truth.
- One branch and pull request per work package, merged into `main`.
- GitHub Actions CI: tests, lint, and a smoke test that the hub starts.
- Tests for every engine.
- `python -m plant_memory eval --all` regenerates every figure and table in the report
  from a clean clone.
- Releases: v0.3 (graph + propagation), v0.4 (risk + workflow), v0.5 (verification +
  unmanaged change), v1.0 (final).

---

## 5. Evaluation plan (what the report will show)

| # | Experiment | Data | Metrics |
|---|---|---|---|
| E1 | Knowledge localisation at scale | expanded corpus, all scenarios | precision, recall, null false-positive rate |
| E2 | Impact coverage of an MOC | all scenarios | items found per category (knowledge, procedures, alarms, models, people), v0 vs full graph |
| E3 | Propagation vs real disturbances | alarm log + historian | precision@k, recall@k, NDCG, Spearman for 3 predictors |
| E4 | Alarm replay of setpoint changes | historian + ISA-18.2 machine | change in alarm count, flood intervals, margin to trip |
| E5 | Unmanaged-change detection | historian with injected changes | detection rate, false alarms/day, delay, ROC per k |
| E6 | Model MOC | PCA / T² / SPE model | false-alarm inflation after change, flagged in advance (yes/no) |
| E7 | Organisational change | roster + corpus | coverage lost, bus factor distribution, orphaned items |
| E8 | Effort and scaling | synthetic plants up to ~1,000 entries | review items targeted vs blanket, saving curve |

Plus four end-to-end **case studies**, each run through the full workflow and exported
as an MOC package: IDF bearing + VFD upgrade (material), new coal blend (material /
feedstock), steam-drum HiHi setpoint retune with alarm replay (material / limits),
senior shift engineer leaving (organisational), and the monitoring-model retrain (AI).

---

## 6. New mathematics (goes into the report and a handbook v2)

1. Max-product impact propagation and its shortest-path form (−log weights).
2. Lagged cross-correlation calibration, direction constraint, significance threshold.
3. Lift-based empirical propagation ground truth from the alarm log.
4. Risk score R = S × L with explicit severity and likelihood definitions.
5. Setpoint-change margin in standard deviations; alarm replay counts.
6. CUSUM detector, average run length, and its relation to the ½σ bins.
7. Coverage, bus factor and Knowledge Risk Index.
8. Hotelling T², SPE limits, and the model-validity condition.
9. Hash-chained audit log and why tampering is detectable.
10. Computed replacement-in-kind: RIK ⟺ all facet fingerprints equal.

---

## 7. Priorities and schedule

**Tier A (the thesis; must ship):** WP1, WP2, WP3, WP4, WP5 (with alarm replay),
WP6, WP7, core of WP11, WP12. Experiments E1 to E5.
**Tier B (strong additions):** WP8, WP9. Experiments E6, E7, E8.
**Tier C (stretch):** WP10, live public demo, optional text drafting.

Proposed order, to be compressed or stretched to your deadline:

| Block | Work |
|---|---|
| 1 | WP1 data + corpus, WP2 graph, WP3 propagation. Release v0.3 |
| 2 | WP4 calibration + E3 validation, WP5 risk + alarm replay + E4. Release v0.4 |
| 3 | WP6 workflow + package + audit, WP11 UI, WP7 verification + detector + E5. Release v0.5 |
| 4 | WP8, WP9, E6 to E8, case studies, polish. Release v1.0 |
| 5 | Final BTP report + presentation + defense handbook v2 |

---

## 8. Final BTP report outline (after the build)

1. Introduction: computational operation, and why its knowledge decays
2. Management of Change: practice, standards, and why it is conservative
3. Related work: fault diagnosis, plant-wide disturbance propagation, concept drift,
   knowledge management, MOC systems
4. PlantMemory: grounding, fingerprints, drift (mid-sem work, consolidated)
5. Computable MOC: the dependency graph and impact propagation
6. Data calibration and validation on the boiler
7. Risk, tiering, alarm replay and the MOC workflow
8. Closing the loop: verification and unmanaged-change detection
9. Organisational change and MOC for AI models
10. Results, case studies and discussion
11. Limitations and future work
12. Conclusion

---

## 9. Risks and honest limitations

- **One plant, five days of data.** Validation is real but narrow; we say so.
- **Synthetic parts:** the people roster and injected changes are synthetic and
  labelled as such. Real-data validation comes from the alarm log and historian.
- **Correlation is not causation.** Mitigated by forcing lag direction to agree with
  the process flow graph; stated as a limitation.
- **Decision support, not certified software.** People authorise; the tool assesses.
- **Professor's reference site** (safetydesigninc.com) currently redirects to an
  unrelated domain, so its content could not be checked. The work is positioned
  against OSHA 29 CFR 1910.119(l), CCPS MOC guidelines and API RP 750 instead.

---

## 10. Decisions needed from you

1. **Deadline** for the final report and presentation (this sets how much of Tier B
   and C we do).
2. **Scope**: approve Tier A / B / C as written, or move items.
3. **Synthetic people roster** for organisational MOC: acceptable?
4. **Language-model drafting**: keep the system fully deterministic (recommended,
   strongest answer to "MOC doesn't use AI"), or include optional drafting?
5. **Public live demo** link for examiners: want it?
6. **Commit the historian and alarm data** (~11 MB) to the repo for reproducibility:
   recommended yes.
