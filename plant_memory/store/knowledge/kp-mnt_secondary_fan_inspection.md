---
id: kp-mnt_secondary_fan_inspection
title: Secondary Fan Annual Inspection and Flow Calibration
category: procedure
statement: Documented maintenance knowledge (mnt_secondary_fan_inspection, Rev 1.2)
  for secondary_fan; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: FT_8302
  aspect: presence
  fingerprint: 04003aa2b9526cfc
  note: mnt_secondary_fan_inspection relies on FT_8302 presence
- kind: kg_node
  ref: secondary_fan
  aspect: presence
  fingerprint: 562fe19a5d8a7d10
  note: mnt_secondary_fan_inspection relies on secondary_fan presence
- kind: kg_node
  ref: secondary_fan
  aspect: connections
  fingerprint: 2982b832f7011881
  note: mnt_secondary_fan_inspection relies on secondary_fan connections
evidence:
- mnt_secondary_fan_inspection Rev 1.2
confidence: 0.85
status: active
tags_referenced:
- FT_8302
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_secondary_fan_inspection
  doc_type: maintenance
  revision: '1.2'
---

# Secondary Fan Annual Inspection and Flow Calibration

**Documented maintenance knowledge (mnt_secondary_fan_inspection, Rev 1.2) for secondary_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:FT_8302` (presence) — mnt_secondary_fan_inspection relies on FT_8302 presence
- `kg_node:secondary_fan` (presence) — mnt_secondary_fan_inspection relies on secondary_fan presence
- `kg_node:secondary_fan` (connections) — mnt_secondary_fan_inspection relies on secondary_fan connections
