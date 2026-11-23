---
id: kp-mnt_air_preheater_cleaning
title: Air Preheater Cleaning Procedure (Primary and Secondary)
category: procedure
statement: Documented maintenance knowledge (mnt_air_preheater_cleaning, Rev 1.5)
  for primary_air_preheater, secondary_air_preheater; valid only while the referenced
  plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8303
  aspect: presence
  fingerprint: 54c79aa759387159
  note: mnt_air_preheater_cleaning relies on TE_8303 presence
- kind: tag
  ref: TE_8304
  aspect: presence
  fingerprint: 2c157d1ea669d3f7
  note: mnt_air_preheater_cleaning relies on TE_8304 presence
- kind: kg_node
  ref: primary_air_preheater
  aspect: presence
  fingerprint: b2aa4e0a0df27171
  note: mnt_air_preheater_cleaning relies on primary_air_preheater presence
- kind: kg_node
  ref: primary_air_preheater
  aspect: connections
  fingerprint: 54f93d3a67adee8a
  note: mnt_air_preheater_cleaning relies on primary_air_preheater connections
- kind: kg_node
  ref: secondary_air_preheater
  aspect: presence
  fingerprint: bcbaf2072e176ce6
  note: mnt_air_preheater_cleaning relies on secondary_air_preheater presence
- kind: kg_node
  ref: secondary_air_preheater
  aspect: connections
  fingerprint: c98541a4b51b6950
  note: mnt_air_preheater_cleaning relies on secondary_air_preheater connections
evidence:
- mnt_air_preheater_cleaning Rev 1.5
confidence: 0.85
status: active
tags_referenced:
- TE_8303
- TE_8304
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_air_preheater_cleaning
  doc_type: maintenance
  revision: '1.5'
---

# Air Preheater Cleaning Procedure (Primary and Secondary)

**Documented maintenance knowledge (mnt_air_preheater_cleaning, Rev 1.5) for primary_air_preheater, secondary_air_preheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8303` (presence) — mnt_air_preheater_cleaning relies on TE_8303 presence
- `tag:TE_8304` (presence) — mnt_air_preheater_cleaning relies on TE_8304 presence
- `kg_node:primary_air_preheater` (presence) — mnt_air_preheater_cleaning relies on primary_air_preheater presence
- `kg_node:primary_air_preheater` (connections) — mnt_air_preheater_cleaning relies on primary_air_preheater connections
- `kg_node:secondary_air_preheater` (presence) — mnt_air_preheater_cleaning relies on secondary_air_preheater presence
- `kg_node:secondary_air_preheater` (connections) — mnt_air_preheater_cleaning relies on secondary_air_preheater connections
