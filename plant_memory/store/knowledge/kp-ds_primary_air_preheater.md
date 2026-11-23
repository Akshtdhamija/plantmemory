---
id: kp-ds_primary_air_preheater
title: Equipment Datasheet — Primary Air Preheater
category: design_basis
statement: Documented datasheet knowledge (ds_primary_air_preheater, Rev 1.1) for
  primary_air_preheater; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8303
  aspect: presence
  fingerprint: 54c79aa759387159
  note: ds_primary_air_preheater relies on TE_8303 presence
- kind: tag
  ref: TE_8303
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_primary_air_preheater relies on TE_8303 normal_range
- kind: kg_node
  ref: primary_air_preheater
  aspect: presence
  fingerprint: b2aa4e0a0df27171
  note: ds_primary_air_preheater relies on primary_air_preheater presence
- kind: kg_node
  ref: primary_air_preheater
  aspect: connections
  fingerprint: 54f93d3a67adee8a
  note: ds_primary_air_preheater relies on primary_air_preheater connections
evidence:
- ds_primary_air_preheater Rev 1.1
confidence: 0.9
status: active
tags_referenced:
- TE_8303
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_primary_air_preheater
  doc_type: datasheet
  revision: '1.1'
---

# Equipment Datasheet — Primary Air Preheater

**Documented datasheet knowledge (ds_primary_air_preheater, Rev 1.1) for primary_air_preheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8303` (presence) — ds_primary_air_preheater relies on TE_8303 presence
- `tag:TE_8303` (normal_range) — ds_primary_air_preheater relies on TE_8303 normal_range
- `kg_node:primary_air_preheater` (presence) — ds_primary_air_preheater relies on primary_air_preheater presence
- `kg_node:primary_air_preheater` (connections) — ds_primary_air_preheater relies on primary_air_preheater connections
