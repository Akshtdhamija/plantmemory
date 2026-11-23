---
id: kp-ds_secondary_air_preheater
title: Equipment Datasheet — Secondary Air Preheater
category: design_basis
statement: Documented datasheet knowledge (ds_secondary_air_preheater, Rev 1.1) for
  secondary_air_preheater; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8304
  aspect: presence
  fingerprint: 2c157d1ea669d3f7
  note: ds_secondary_air_preheater relies on TE_8304 presence
- kind: tag
  ref: TE_8304
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_secondary_air_preheater relies on TE_8304 normal_range
- kind: kg_node
  ref: secondary_air_preheater
  aspect: presence
  fingerprint: bcbaf2072e176ce6
  note: ds_secondary_air_preheater relies on secondary_air_preheater presence
- kind: kg_node
  ref: secondary_air_preheater
  aspect: connections
  fingerprint: c98541a4b51b6950
  note: ds_secondary_air_preheater relies on secondary_air_preheater connections
evidence:
- ds_secondary_air_preheater Rev 1.1
confidence: 0.9
status: active
tags_referenced:
- TE_8304
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_secondary_air_preheater
  doc_type: datasheet
  revision: '1.1'
---

# Equipment Datasheet — Secondary Air Preheater

**Documented datasheet knowledge (ds_secondary_air_preheater, Rev 1.1) for secondary_air_preheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8304` (presence) — ds_secondary_air_preheater relies on TE_8304 presence
- `tag:TE_8304` (normal_range) — ds_secondary_air_preheater relies on TE_8304 normal_range
- `kg_node:secondary_air_preheater` (presence) — ds_secondary_air_preheater relies on secondary_air_preheater presence
- `kg_node:secondary_air_preheater` (connections) — ds_secondary_air_preheater relies on secondary_air_preheater connections
