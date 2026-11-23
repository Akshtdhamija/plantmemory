---
id: kp-ds_low_temp_superheater
title: Equipment Datasheet — Low Temperature Superheater
category: design_basis
statement: Documented datasheet knowledge (ds_low_temp_superheater, Rev 1.1) for low_temp_superheater;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: kg_node
  ref: low_temp_superheater
  aspect: presence
  fingerprint: db008506ee6ef24f
  note: ds_low_temp_superheater relies on low_temp_superheater presence
- kind: kg_node
  ref: low_temp_superheater
  aspect: connections
  fingerprint: e3b700afc5d9b890
  note: ds_low_temp_superheater relies on low_temp_superheater connections
evidence:
- ds_low_temp_superheater Rev 1.1
confidence: 0.9
status: active
tags_referenced: []
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_low_temp_superheater
  doc_type: datasheet
  revision: '1.1'
---

# Equipment Datasheet — Low Temperature Superheater

**Documented datasheet knowledge (ds_low_temp_superheater, Rev 1.1) for low_temp_superheater; valid only while the referenced plant facets hold.**

## Grounded to

- `kg_node:low_temp_superheater` (presence) — ds_low_temp_superheater relies on low_temp_superheater presence
- `kg_node:low_temp_superheater` (connections) — ds_low_temp_superheater relies on low_temp_superheater connections
