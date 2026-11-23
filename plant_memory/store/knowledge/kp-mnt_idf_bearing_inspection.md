---
id: kp-mnt_idf_bearing_inspection
title: IDF Bearing Shell Inspection and Vibration Check
category: procedure
statement: Documented maintenance knowledge (mnt_idf_bearing_inspection, Rev 2.1)
  for induced_draft_fan; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: YFJ3_ZD1
  aspect: presence
  fingerprint: 6e5139ca3779c193
  note: mnt_idf_bearing_inspection relies on YFJ3_ZD1 presence
- kind: tag
  ref: YFJ3_ZD2
  aspect: presence
  fingerprint: 84032c15374c3114
  note: mnt_idf_bearing_inspection relies on YFJ3_ZD2 presence
- kind: tag
  ref: YFJ3_AI
  aspect: presence
  fingerprint: 4dc65c48c9f9d08f
  note: mnt_idf_bearing_inspection relies on YFJ3_AI presence
- kind: kg_node
  ref: induced_draft_fan
  aspect: presence
  fingerprint: 762b82e81f982cdd
  note: mnt_idf_bearing_inspection relies on induced_draft_fan presence
- kind: kg_node
  ref: induced_draft_fan
  aspect: connections
  fingerprint: eac398facfdee248
  note: mnt_idf_bearing_inspection relies on induced_draft_fan connections
evidence:
- mnt_idf_bearing_inspection Rev 2.1
confidence: 0.85
status: active
tags_referenced:
- YFJ3_ZD1
- YFJ3_ZD2
- YFJ3_AI
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_idf_bearing_inspection
  doc_type: maintenance
  revision: '2.1'
---

# IDF Bearing Shell Inspection and Vibration Check

**Documented maintenance knowledge (mnt_idf_bearing_inspection, Rev 2.1) for induced_draft_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:YFJ3_ZD1` (presence) — mnt_idf_bearing_inspection relies on YFJ3_ZD1 presence
- `tag:YFJ3_ZD2` (presence) — mnt_idf_bearing_inspection relies on YFJ3_ZD2 presence
- `tag:YFJ3_AI` (presence) — mnt_idf_bearing_inspection relies on YFJ3_AI presence
- `kg_node:induced_draft_fan` (presence) — mnt_idf_bearing_inspection relies on induced_draft_fan presence
- `kg_node:induced_draft_fan` (connections) — mnt_idf_bearing_inspection relies on induced_draft_fan connections
