---
id: kp-trb_low_steam_temperature
title: Troubleshooting Guide — Low Steam Temperature (TE_8332A < 530°C)
category: failure_mode
statement: Documented troubleshooting knowledge (trb_low_steam_temperature, Rev 2.1)
  for steam_outlet, high_temp_superheater, primary_desuperheater, low_temp_superheater;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8332A
  aspect: normal_range
  fingerprint: 35700a8893a58270
  note: trb_low_steam_temperature relies on TE_8332A normal_range
- kind: tag
  ref: TE_8332A
  aspect: setpoints
  fingerprint: 4112efe131c0fc1f
  note: trb_low_steam_temperature relies on TE_8332A setpoints
- kind: tag
  ref: TV_8329ZC
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on TV_8329ZC normal_range
- kind: tag
  ref: TV_8329ZC
  aspect: setpoints
  fingerprint: de8480d4a6e7c62c
  note: trb_low_steam_temperature relies on TV_8329ZC setpoints
- kind: tag
  ref: YJJWSLL
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on YJJWSLL normal_range
- kind: tag
  ref: YJJWSLL
  aspect: setpoints
  fingerprint: 0104e33760b03d96
  note: trb_low_steam_temperature relies on YJJWSLL setpoints
- kind: tag
  ref: ZZQBCHLL
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on ZZQBCHLL normal_range
- kind: tag
  ref: ZZQBCHLL
  aspect: setpoints
  fingerprint: a7f21a6b333e22f9
  note: trb_low_steam_temperature relies on ZZQBCHLL setpoints
- kind: tag
  ref: AIR_8301A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on AIR_8301A normal_range
- kind: tag
  ref: AIR_8301A
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_low_steam_temperature relies on AIR_8301A setpoints
- kind: tag
  ref: AIR_8301B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on AIR_8301B normal_range
- kind: tag
  ref: AIR_8301B
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_low_steam_temperature relies on AIR_8301B setpoints
- kind: tag
  ref: TE_8313B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on TE_8313B normal_range
- kind: tag
  ref: TE_8313B
  aspect: setpoints
  fingerprint: f6978d61088b4c8f
  note: trb_low_steam_temperature relies on TE_8313B setpoints
- kind: tag
  ref: FT_8301
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on FT_8301 normal_range
- kind: tag
  ref: FT_8301
  aspect: setpoints
  fingerprint: 73c1cefabdffe5dc
  note: trb_low_steam_temperature relies on FT_8301 setpoints
- kind: tag
  ref: FT_8302
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on FT_8302 normal_range
- kind: tag
  ref: FT_8302
  aspect: setpoints
  fingerprint: 019618f4bda8eea0
  note: trb_low_steam_temperature relies on FT_8302 setpoints
- kind: tag
  ref: SXLTCYZ
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on SXLTCYZ normal_range
- kind: tag
  ref: SXLTCYZ
  aspect: setpoints
  fingerprint: d016197cc51effcd
  note: trb_low_steam_temperature relies on SXLTCYZ setpoints
- kind: tag
  ref: SXLTCYY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_temperature relies on SXLTCYY normal_range
- kind: tag
  ref: SXLTCYY
  aspect: setpoints
  fingerprint: d016197cc51effcd
  note: trb_low_steam_temperature relies on SXLTCYY setpoints
- kind: kg_node
  ref: steam_outlet
  aspect: presence
  fingerprint: cc797c63c73e81f3
  note: trb_low_steam_temperature relies on steam_outlet presence
- kind: kg_node
  ref: high_temp_superheater
  aspect: presence
  fingerprint: 45079fb9eb8efd8c
  note: trb_low_steam_temperature relies on high_temp_superheater presence
- kind: kg_node
  ref: primary_desuperheater
  aspect: presence
  fingerprint: 86ec87aa23525fd3
  note: trb_low_steam_temperature relies on primary_desuperheater presence
- kind: kg_node
  ref: low_temp_superheater
  aspect: presence
  fingerprint: db008506ee6ef24f
  note: trb_low_steam_temperature relies on low_temp_superheater presence
- kind: kg_node
  ref: furnace_lower_hearth
  aspect: presence
  fingerprint: 4e382c298e836394
  note: trb_low_steam_temperature relies on furnace_lower_hearth presence
- kind: kg_node
  ref: furnace_chamber
  aspect: presence
  fingerprint: 94b36a9c522e2988
  note: trb_low_steam_temperature relies on furnace_chamber presence
evidence:
- trb_low_steam_temperature Rev 2.1
confidence: 0.8
status: active
tags_referenced:
- TE_8332A
- TV_8329ZC
- YJJWSLL
- ZZQBCHLL
- AIR_8301A
- AIR_8301B
- TE_8313B
- FT_8301
- FT_8302
- SXLTCYZ
- SXLTCYY
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_low_steam_temperature
  doc_type: troubleshooting
  revision: '2.1'
---

# Troubleshooting Guide — Low Steam Temperature (TE_8332A < 530°C)

**Documented troubleshooting knowledge (trb_low_steam_temperature, Rev 2.1) for steam_outlet, high_temp_superheater, primary_desuperheater, low_temp_superheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8332A` (normal_range) — trb_low_steam_temperature relies on TE_8332A normal_range
- `tag:TE_8332A` (setpoints) — trb_low_steam_temperature relies on TE_8332A setpoints
- `tag:TV_8329ZC` (normal_range) — trb_low_steam_temperature relies on TV_8329ZC normal_range
- `tag:TV_8329ZC` (setpoints) — trb_low_steam_temperature relies on TV_8329ZC setpoints
- `tag:YJJWSLL` (normal_range) — trb_low_steam_temperature relies on YJJWSLL normal_range
- `tag:YJJWSLL` (setpoints) — trb_low_steam_temperature relies on YJJWSLL setpoints
- `tag:ZZQBCHLL` (normal_range) — trb_low_steam_temperature relies on ZZQBCHLL normal_range
- `tag:ZZQBCHLL` (setpoints) — trb_low_steam_temperature relies on ZZQBCHLL setpoints
- `tag:AIR_8301A` (normal_range) — trb_low_steam_temperature relies on AIR_8301A normal_range
- `tag:AIR_8301A` (setpoints) — trb_low_steam_temperature relies on AIR_8301A setpoints
- `tag:AIR_8301B` (normal_range) — trb_low_steam_temperature relies on AIR_8301B normal_range
- `tag:AIR_8301B` (setpoints) — trb_low_steam_temperature relies on AIR_8301B setpoints
- `tag:TE_8313B` (normal_range) — trb_low_steam_temperature relies on TE_8313B normal_range
- `tag:TE_8313B` (setpoints) — trb_low_steam_temperature relies on TE_8313B setpoints
- `tag:FT_8301` (normal_range) — trb_low_steam_temperature relies on FT_8301 normal_range
- `tag:FT_8301` (setpoints) — trb_low_steam_temperature relies on FT_8301 setpoints
- `tag:FT_8302` (normal_range) — trb_low_steam_temperature relies on FT_8302 normal_range
- `tag:FT_8302` (setpoints) — trb_low_steam_temperature relies on FT_8302 setpoints
- `tag:SXLTCYZ` (normal_range) — trb_low_steam_temperature relies on SXLTCYZ normal_range
- `tag:SXLTCYZ` (setpoints) — trb_low_steam_temperature relies on SXLTCYZ setpoints
- `tag:SXLTCYY` (normal_range) — trb_low_steam_temperature relies on SXLTCYY normal_range
- `tag:SXLTCYY` (setpoints) — trb_low_steam_temperature relies on SXLTCYY setpoints
- `kg_node:steam_outlet` (presence) — trb_low_steam_temperature relies on steam_outlet presence
- `kg_node:high_temp_superheater` (presence) — trb_low_steam_temperature relies on high_temp_superheater presence
- `kg_node:primary_desuperheater` (presence) — trb_low_steam_temperature relies on primary_desuperheater presence
- `kg_node:low_temp_superheater` (presence) — trb_low_steam_temperature relies on low_temp_superheater presence
- `kg_node:furnace_lower_hearth` (presence) — trb_low_steam_temperature relies on furnace_lower_hearth presence
- `kg_node:furnace_chamber` (presence) — trb_low_steam_temperature relies on furnace_chamber presence
