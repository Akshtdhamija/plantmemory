---
id: kp-ds_primary_fan
title: Equipment Datasheet — Primary Fan
category: design_basis
statement: Documented datasheet knowledge (ds_primary_fan, Rev 1.2) for primary_fan;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: FT_8301
  aspect: presence
  fingerprint: ff99b5724f33b718
  note: ds_primary_fan relies on FT_8301 presence
- kind: tag
  ref: FT_8301
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_primary_fan relies on FT_8301 normal_range
- kind: kg_node
  ref: primary_fan
  aspect: presence
  fingerprint: e990b1d5a8d281d6
  note: ds_primary_fan relies on primary_fan presence
- kind: kg_node
  ref: primary_fan
  aspect: connections
  fingerprint: 52498e61aa2e79c2
  note: ds_primary_fan relies on primary_fan connections
evidence:
- ds_primary_fan Rev 1.2
confidence: 0.9
status: active
tags_referenced:
- FT_8301
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_primary_fan
  doc_type: datasheet
  revision: '1.2'
---

# Equipment Datasheet — Primary Fan

**Documented datasheet knowledge (ds_primary_fan, Rev 1.2) for primary_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:FT_8301` (presence) — ds_primary_fan relies on FT_8301 presence
- `tag:FT_8301` (normal_range) — ds_primary_fan relies on FT_8301 normal_range
- `kg_node:primary_fan` (presence) — ds_primary_fan relies on primary_fan presence
- `kg_node:primary_fan` (connections) — ds_primary_fan relies on primary_fan connections
