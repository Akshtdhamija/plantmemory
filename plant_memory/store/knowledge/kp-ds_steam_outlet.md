---
id: kp-ds_steam_outlet
title: Equipment Datasheet — Steam Outlet Header
category: design_basis
statement: Documented datasheet knowledge (ds_steam_outlet, Rev 1.1) for steam_outlet;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8332A
  aspect: presence
  fingerprint: 78f1080a5f2eb57d
  note: ds_steam_outlet relies on TE_8332A presence
- kind: tag
  ref: TE_8332A
  aspect: normal_range
  fingerprint: 35700a8893a58270
  note: ds_steam_outlet relies on TE_8332A normal_range
- kind: tag
  ref: PTCA_8324
  aspect: presence
  fingerprint: 6db4204bdc3dd69e
  note: ds_steam_outlet relies on PTCA_8324 presence
- kind: tag
  ref: PTCA_8324
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_steam_outlet relies on PTCA_8324 normal_range
- kind: tag
  ref: ZZQBCHLL
  aspect: presence
  fingerprint: a6497395b4832b77
  note: ds_steam_outlet relies on ZZQBCHLL presence
- kind: tag
  ref: ZZQBCHLL
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_steam_outlet relies on ZZQBCHLL normal_range
- kind: kg_node
  ref: steam_outlet
  aspect: presence
  fingerprint: cc797c63c73e81f3
  note: ds_steam_outlet relies on steam_outlet presence
- kind: kg_node
  ref: steam_outlet
  aspect: connections
  fingerprint: b21894b95d290ebc
  note: ds_steam_outlet relies on steam_outlet connections
evidence:
- ds_steam_outlet Rev 1.1
confidence: 0.9
status: active
tags_referenced:
- TE_8332A
- PTCA_8324
- ZZQBCHLL
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_steam_outlet
  doc_type: datasheet
  revision: '1.1'
---

# Equipment Datasheet — Steam Outlet Header

**Documented datasheet knowledge (ds_steam_outlet, Rev 1.1) for steam_outlet; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8332A` (presence) — ds_steam_outlet relies on TE_8332A presence
- `tag:TE_8332A` (normal_range) — ds_steam_outlet relies on TE_8332A normal_range
- `tag:PTCA_8324` (presence) — ds_steam_outlet relies on PTCA_8324 presence
- `tag:PTCA_8324` (normal_range) — ds_steam_outlet relies on PTCA_8324 normal_range
- `tag:ZZQBCHLL` (presence) — ds_steam_outlet relies on ZZQBCHLL presence
- `tag:ZZQBCHLL` (normal_range) — ds_steam_outlet relies on ZZQBCHLL normal_range
- `kg_node:steam_outlet` (presence) — ds_steam_outlet relies on steam_outlet presence
- `kg_node:steam_outlet` (connections) — ds_steam_outlet relies on steam_outlet connections
