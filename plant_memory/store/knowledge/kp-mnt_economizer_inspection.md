---
id: kp-mnt_economizer_inspection
title: Economizer Tube Inspection and Hydrotest
category: procedure
statement: Documented maintenance knowledge (mnt_economizer_inspection, Rev 1.3) for
  economizer; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8319A
  aspect: presence
  fingerprint: 117c0074924b8233
  note: mnt_economizer_inspection relies on TE_8319A presence
- kind: tag
  ref: TE_8319B
  aspect: presence
  fingerprint: fa644d58f3e2a50e
  note: mnt_economizer_inspection relies on TE_8319B presence
- kind: tag
  ref: AIR_8301A
  aspect: presence
  fingerprint: e9968992122b006e
  note: mnt_economizer_inspection relies on AIR_8301A presence
- kind: tag
  ref: AIR_8301B
  aspect: presence
  fingerprint: c5ca3f05ac49acfb
  note: mnt_economizer_inspection relies on AIR_8301B presence
- kind: kg_node
  ref: economizer
  aspect: presence
  fingerprint: 20bfb78b831c15e4
  note: mnt_economizer_inspection relies on economizer presence
- kind: kg_node
  ref: economizer
  aspect: connections
  fingerprint: 6373639913b78ab5
  note: mnt_economizer_inspection relies on economizer connections
evidence:
- mnt_economizer_inspection Rev 1.3
confidence: 0.85
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
  doc_id: mnt_economizer_inspection
  doc_type: maintenance
  revision: '1.3'
---

# Economizer Tube Inspection and Hydrotest

**Documented maintenance knowledge (mnt_economizer_inspection, Rev 1.3) for economizer; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8319A` (presence) — mnt_economizer_inspection relies on TE_8319A presence
- `tag:TE_8319B` (presence) — mnt_economizer_inspection relies on TE_8319B presence
- `tag:AIR_8301A` (presence) — mnt_economizer_inspection relies on AIR_8301A presence
- `tag:AIR_8301B` (presence) — mnt_economizer_inspection relies on AIR_8301B presence
- `kg_node:economizer` (presence) — mnt_economizer_inspection relies on economizer presence
- `kg_node:economizer` (connections) — mnt_economizer_inspection relies on economizer connections
