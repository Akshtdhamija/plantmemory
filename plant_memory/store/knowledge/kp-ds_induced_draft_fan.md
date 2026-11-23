---
id: kp-ds_induced_draft_fan
title: Equipment Datasheet — Induced Draft Fan
category: design_basis
statement: Documented datasheet knowledge (ds_induced_draft_fan, Rev 1.5) for induced_draft_fan;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: YFJ3_AI
  aspect: presence
  fingerprint: 4dc65c48c9f9d08f
  note: ds_induced_draft_fan relies on YFJ3_AI presence
- kind: tag
  ref: YFJ3_AI
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_induced_draft_fan relies on YFJ3_AI normal_range
- kind: tag
  ref: YFJ3_ZD1
  aspect: presence
  fingerprint: 6e5139ca3779c193
  note: ds_induced_draft_fan relies on YFJ3_ZD1 presence
- kind: tag
  ref: YFJ3_ZD1
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_induced_draft_fan relies on YFJ3_ZD1 normal_range
- kind: tag
  ref: YFJ3_ZD2
  aspect: presence
  fingerprint: 84032c15374c3114
  note: ds_induced_draft_fan relies on YFJ3_ZD2 presence
- kind: tag
  ref: YFJ3_ZD2
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_induced_draft_fan relies on YFJ3_ZD2 normal_range
- kind: kg_node
  ref: induced_draft_fan
  aspect: presence
  fingerprint: 762b82e81f982cdd
  note: ds_induced_draft_fan relies on induced_draft_fan presence
- kind: kg_node
  ref: induced_draft_fan
  aspect: connections
  fingerprint: eac398facfdee248
  note: ds_induced_draft_fan relies on induced_draft_fan connections
evidence:
- ds_induced_draft_fan Rev 1.5
confidence: 0.9
status: active
tags_referenced:
- YFJ3_AI
- YFJ3_ZD1
- YFJ3_ZD2
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_induced_draft_fan
  doc_type: datasheet
  revision: '1.5'
---

# Equipment Datasheet — Induced Draft Fan

**Documented datasheet knowledge (ds_induced_draft_fan, Rev 1.5) for induced_draft_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:YFJ3_AI` (presence) — ds_induced_draft_fan relies on YFJ3_AI presence
- `tag:YFJ3_AI` (normal_range) — ds_induced_draft_fan relies on YFJ3_AI normal_range
- `tag:YFJ3_ZD1` (presence) — ds_induced_draft_fan relies on YFJ3_ZD1 presence
- `tag:YFJ3_ZD1` (normal_range) — ds_induced_draft_fan relies on YFJ3_ZD1 normal_range
- `tag:YFJ3_ZD2` (presence) — ds_induced_draft_fan relies on YFJ3_ZD2 presence
- `tag:YFJ3_ZD2` (normal_range) — ds_induced_draft_fan relies on YFJ3_ZD2 normal_range
- `kg_node:induced_draft_fan` (presence) — ds_induced_draft_fan relies on induced_draft_fan presence
- `kg_node:induced_draft_fan` (connections) — ds_induced_draft_fan relies on induced_draft_fan connections
