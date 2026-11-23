---
id: kp-ctrl_furnace_draft_loop
title: Furnace Draft Control Loop — Description and Tuning
category: convention
statement: Documented controls knowledge (ctrl_furnace_draft_loop, Rev 1.8) for induced_draft_fan,
  furnace_chamber; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: PT_8313A
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: ctrl_furnace_draft_loop relies on PT_8313A setpoints
- kind: tag
  ref: PT_8313A
  aspect: distribution
  fingerprint: 329f7e16f59b55a5
  note: ctrl_furnace_draft_loop relies on PT_8313A distribution
- kind: tag
  ref: PT_8313B
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: ctrl_furnace_draft_loop relies on PT_8313B setpoints
- kind: tag
  ref: PT_8313B
  aspect: distribution
  fingerprint: 4b310e1f699e79c0
  note: ctrl_furnace_draft_loop relies on PT_8313B distribution
- kind: tag
  ref: PT_8313C
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: ctrl_furnace_draft_loop relies on PT_8313C setpoints
- kind: tag
  ref: PT_8313C
  aspect: distribution
  fingerprint: 30c37cac9dd6a197
  note: ctrl_furnace_draft_loop relies on PT_8313C distribution
- kind: tag
  ref: PT_8313D
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: ctrl_furnace_draft_loop relies on PT_8313D setpoints
- kind: tag
  ref: PT_8313D
  aspect: distribution
  fingerprint: d9747964979b2e79
  note: ctrl_furnace_draft_loop relies on PT_8313D distribution
- kind: tag
  ref: PT_8313E
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: ctrl_furnace_draft_loop relies on PT_8313E setpoints
- kind: tag
  ref: PT_8313E
  aspect: distribution
  fingerprint: 30c37cac9dd6a197
  note: ctrl_furnace_draft_loop relies on PT_8313E distribution
- kind: tag
  ref: PT_8313F
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: ctrl_furnace_draft_loop relies on PT_8313F setpoints
- kind: tag
  ref: PT_8313F
  aspect: distribution
  fingerprint: bf629d74bb949498
  note: ctrl_furnace_draft_loop relies on PT_8313F distribution
- kind: tag
  ref: YFJ3_AI
  aspect: setpoints
  fingerprint: 7a0b322eae4fb288
  note: ctrl_furnace_draft_loop relies on YFJ3_AI setpoints
- kind: tag
  ref: YFJ3_AI
  aspect: distribution
  fingerprint: dcb6788a8065a256
  note: ctrl_furnace_draft_loop relies on YFJ3_AI distribution
- kind: kg_node
  ref: induced_draft_fan
  aspect: connections
  fingerprint: eac398facfdee248
  note: ctrl_furnace_draft_loop relies on induced_draft_fan connections
- kind: kg_node
  ref: furnace_chamber
  aspect: connections
  fingerprint: 41c13b32f7879b9b
  note: ctrl_furnace_draft_loop relies on furnace_chamber connections
evidence:
- ctrl_furnace_draft_loop Rev 1.8
confidence: 0.85
status: active
tags_referenced:
- PT_8313A
- PT_8313B
- PT_8313C
- PT_8313D
- PT_8313E
- PT_8313F
- YFJ3_AI
source: library
author: P07 Control and Instrumentation Engineer
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ctrl_furnace_draft_loop
  doc_type: controls
  revision: '1.8'
---

# Furnace Draft Control Loop — Description and Tuning

**Documented controls knowledge (ctrl_furnace_draft_loop, Rev 1.8) for induced_draft_fan, furnace_chamber; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:PT_8313A` (setpoints) — ctrl_furnace_draft_loop relies on PT_8313A setpoints
- `tag:PT_8313A` (distribution) — ctrl_furnace_draft_loop relies on PT_8313A distribution
- `tag:PT_8313B` (setpoints) — ctrl_furnace_draft_loop relies on PT_8313B setpoints
- `tag:PT_8313B` (distribution) — ctrl_furnace_draft_loop relies on PT_8313B distribution
- `tag:PT_8313C` (setpoints) — ctrl_furnace_draft_loop relies on PT_8313C setpoints
- `tag:PT_8313C` (distribution) — ctrl_furnace_draft_loop relies on PT_8313C distribution
- `tag:PT_8313D` (setpoints) — ctrl_furnace_draft_loop relies on PT_8313D setpoints
- `tag:PT_8313D` (distribution) — ctrl_furnace_draft_loop relies on PT_8313D distribution
- `tag:PT_8313E` (setpoints) — ctrl_furnace_draft_loop relies on PT_8313E setpoints
- `tag:PT_8313E` (distribution) — ctrl_furnace_draft_loop relies on PT_8313E distribution
- `tag:PT_8313F` (setpoints) — ctrl_furnace_draft_loop relies on PT_8313F setpoints
- `tag:PT_8313F` (distribution) — ctrl_furnace_draft_loop relies on PT_8313F distribution
- `tag:YFJ3_AI` (setpoints) — ctrl_furnace_draft_loop relies on YFJ3_AI setpoints
- `tag:YFJ3_AI` (distribution) — ctrl_furnace_draft_loop relies on YFJ3_AI distribution
- `kg_node:induced_draft_fan` (connections) — ctrl_furnace_draft_loop relies on induced_draft_fan connections
- `kg_node:furnace_chamber` (connections) — ctrl_furnace_draft_loop relies on furnace_chamber connections
