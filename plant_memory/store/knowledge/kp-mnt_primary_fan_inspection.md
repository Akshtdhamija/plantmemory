---
id: kp-mnt_primary_fan_inspection
title: Primary Fan Annual Inspection and Flow Calibration
category: procedure
statement: Documented maintenance knowledge (mnt_primary_fan_inspection, Rev 1.3)
  for primary_fan; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: FT_8301
  aspect: presence
  fingerprint: ff99b5724f33b718
  note: mnt_primary_fan_inspection relies on FT_8301 presence
- kind: kg_node
  ref: primary_fan
  aspect: presence
  fingerprint: e990b1d5a8d281d6
  note: mnt_primary_fan_inspection relies on primary_fan presence
- kind: kg_node
  ref: primary_fan
  aspect: connections
  fingerprint: 52498e61aa2e79c2
  note: mnt_primary_fan_inspection relies on primary_fan connections
evidence:
- mnt_primary_fan_inspection Rev 1.3
confidence: 0.85
status: active
tags_referenced:
- FT_8301
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_primary_fan_inspection
  doc_type: maintenance
  revision: '1.3'
---

# Primary Fan Annual Inspection and Flow Calibration

**Documented maintenance knowledge (mnt_primary_fan_inspection, Rev 1.3) for primary_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:FT_8301` (presence) — mnt_primary_fan_inspection relies on FT_8301 presence
- `kg_node:primary_fan` (presence) — mnt_primary_fan_inspection relies on primary_fan presence
- `kg_node:primary_fan` (connections) — mnt_primary_fan_inspection relies on primary_fan connections
