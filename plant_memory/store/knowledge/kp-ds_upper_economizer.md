---
id: kp-ds_upper_economizer
title: Equipment Datasheet — Upper Economizer
category: design_basis
statement: Documented datasheet knowledge (ds_upper_economizer, Rev 1.2) for economizer;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8319A
  aspect: presence
  fingerprint: 117c0074924b8233
  note: ds_upper_economizer relies on TE_8319A presence
- kind: tag
  ref: TE_8319A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_upper_economizer relies on TE_8319A normal_range
- kind: tag
  ref: TE_8319B
  aspect: presence
  fingerprint: fa644d58f3e2a50e
  note: ds_upper_economizer relies on TE_8319B presence
- kind: tag
  ref: TE_8319B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_upper_economizer relies on TE_8319B normal_range
- kind: tag
  ref: AIR_8301A
  aspect: presence
  fingerprint: e9968992122b006e
  note: ds_upper_economizer relies on AIR_8301A presence
- kind: tag
  ref: AIR_8301A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_upper_economizer relies on AIR_8301A normal_range
- kind: tag
  ref: AIR_8301B
  aspect: presence
  fingerprint: c5ca3f05ac49acfb
  note: ds_upper_economizer relies on AIR_8301B presence
- kind: tag
  ref: AIR_8301B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_upper_economizer relies on AIR_8301B normal_range
- kind: kg_node
  ref: economizer
  aspect: presence
  fingerprint: 20bfb78b831c15e4
  note: ds_upper_economizer relies on economizer presence
- kind: kg_node
  ref: economizer
  aspect: connections
  fingerprint: 6373639913b78ab5
  note: ds_upper_economizer relies on economizer connections
evidence:
- ds_upper_economizer Rev 1.2
confidence: 0.9
status: active
tags_referenced:
- TE_8319A
- TE_8319B
- AIR_8301A
- AIR_8301B
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_upper_economizer
  doc_type: datasheet
  revision: '1.2'
---

# Equipment Datasheet — Upper Economizer

**Documented datasheet knowledge (ds_upper_economizer, Rev 1.2) for economizer; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8319A` (presence) — ds_upper_economizer relies on TE_8319A presence
- `tag:TE_8319A` (normal_range) — ds_upper_economizer relies on TE_8319A normal_range
- `tag:TE_8319B` (presence) — ds_upper_economizer relies on TE_8319B presence
- `tag:TE_8319B` (normal_range) — ds_upper_economizer relies on TE_8319B normal_range
- `tag:AIR_8301A` (presence) — ds_upper_economizer relies on AIR_8301A presence
- `tag:AIR_8301A` (normal_range) — ds_upper_economizer relies on AIR_8301A normal_range
- `tag:AIR_8301B` (presence) — ds_upper_economizer relies on AIR_8301B presence
- `tag:AIR_8301B` (normal_range) — ds_upper_economizer relies on AIR_8301B normal_range
- `kg_node:economizer` (presence) — ds_upper_economizer relies on economizer presence
- `kg_node:economizer` (connections) — ds_upper_economizer relies on economizer connections
