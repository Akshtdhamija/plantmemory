---
id: kp-ds_desuperheater
title: Equipment Datasheet — Primary Desuperheater
category: design_basis
statement: Documented datasheet knowledge (ds_desuperheater, Rev 1.3) for primary_desuperheater;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TV_8329ZC
  aspect: presence
  fingerprint: 7c1cd016342aab1e
  note: ds_desuperheater relies on TV_8329ZC presence
- kind: tag
  ref: TV_8329ZC
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_desuperheater relies on TV_8329ZC normal_range
- kind: tag
  ref: YJJWSLL
  aspect: presence
  fingerprint: 8c7a3e77912dcd94
  note: ds_desuperheater relies on YJJWSLL presence
- kind: tag
  ref: YJJWSLL
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_desuperheater relies on YJJWSLL normal_range
- kind: kg_node
  ref: primary_desuperheater
  aspect: presence
  fingerprint: 86ec87aa23525fd3
  note: ds_desuperheater relies on primary_desuperheater presence
- kind: kg_node
  ref: primary_desuperheater
  aspect: connections
  fingerprint: 7fb6dfa8af8a0f3a
  note: ds_desuperheater relies on primary_desuperheater connections
evidence:
- ds_desuperheater Rev 1.3
confidence: 0.9
status: active
tags_referenced:
- TV_8329ZC
- YJJWSLL
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_desuperheater
  doc_type: datasheet
  revision: '1.3'
---

# Equipment Datasheet — Primary Desuperheater

**Documented datasheet knowledge (ds_desuperheater, Rev 1.3) for primary_desuperheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TV_8329ZC` (presence) — ds_desuperheater relies on TV_8329ZC presence
- `tag:TV_8329ZC` (normal_range) — ds_desuperheater relies on TV_8329ZC normal_range
- `tag:YJJWSLL` (presence) — ds_desuperheater relies on YJJWSLL presence
- `tag:YJJWSLL` (normal_range) — ds_desuperheater relies on YJJWSLL normal_range
- `kg_node:primary_desuperheater` (presence) — ds_desuperheater relies on primary_desuperheater presence
- `kg_node:primary_desuperheater` (connections) — ds_desuperheater relies on primary_desuperheater connections
