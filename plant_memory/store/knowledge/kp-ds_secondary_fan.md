---
id: kp-ds_secondary_fan
title: Equipment Datasheet — Secondary Fan
category: design_basis
statement: Documented datasheet knowledge (ds_secondary_fan, Rev 1.2) for secondary_fan;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: FT_8302
  aspect: presence
  fingerprint: 04003aa2b9526cfc
  note: ds_secondary_fan relies on FT_8302 presence
- kind: tag
  ref: FT_8302
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_secondary_fan relies on FT_8302 normal_range
- kind: kg_node
  ref: secondary_fan
  aspect: presence
  fingerprint: 562fe19a5d8a7d10
  note: ds_secondary_fan relies on secondary_fan presence
- kind: kg_node
  ref: secondary_fan
  aspect: connections
  fingerprint: 2982b832f7011881
  note: ds_secondary_fan relies on secondary_fan connections
evidence:
- ds_secondary_fan Rev 1.2
confidence: 0.9
status: active
tags_referenced:
- FT_8302
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_secondary_fan
  doc_type: datasheet
  revision: '1.2'
---

# Equipment Datasheet — Secondary Fan

**Documented datasheet knowledge (ds_secondary_fan, Rev 1.2) for secondary_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:FT_8302` (presence) — ds_secondary_fan relies on FT_8302 presence
- `tag:FT_8302` (normal_range) — ds_secondary_fan relies on FT_8302 normal_range
- `kg_node:secondary_fan` (presence) — ds_secondary_fan relies on secondary_fan presence
- `kg_node:secondary_fan` (connections) — ds_secondary_fan relies on secondary_fan connections
