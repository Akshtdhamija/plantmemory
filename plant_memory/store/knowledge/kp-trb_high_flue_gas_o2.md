---
id: kp-trb_high_flue_gas_o2
title: Troubleshooting Guide — High Flue Gas O2 (Over-Aeration)
category: failure_mode
statement: Documented troubleshooting knowledge (trb_high_flue_gas_o2, Rev 1.3) for
  furnace_chamber, furnace_lower_hearth, economizer, primary_fan; valid only while
  the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: AIR_8301A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_flue_gas_o2 relies on AIR_8301A normal_range
- kind: tag
  ref: AIR_8301A
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_high_flue_gas_o2 relies on AIR_8301A setpoints
- kind: tag
  ref: AIR_8301B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_flue_gas_o2 relies on AIR_8301B normal_range
- kind: tag
  ref: AIR_8301B
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_high_flue_gas_o2 relies on AIR_8301B setpoints
- kind: tag
  ref: FT_8301
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_flue_gas_o2 relies on FT_8301 normal_range
- kind: tag
  ref: FT_8301
  aspect: setpoints
  fingerprint: 73c1cefabdffe5dc
  note: trb_high_flue_gas_o2 relies on FT_8301 setpoints
- kind: tag
  ref: FT_8302
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_flue_gas_o2 relies on FT_8302 normal_range
- kind: tag
  ref: FT_8302
  aspect: setpoints
  fingerprint: 019618f4bda8eea0
  note: trb_high_flue_gas_o2 relies on FT_8302 setpoints
- kind: tag
  ref: TE_8313B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_flue_gas_o2 relies on TE_8313B normal_range
- kind: tag
  ref: TE_8313B
  aspect: setpoints
  fingerprint: f6978d61088b4c8f
  note: trb_high_flue_gas_o2 relies on TE_8313B setpoints
- kind: tag
  ref: TE_8332A
  aspect: normal_range
  fingerprint: 35700a8893a58270
  note: trb_high_flue_gas_o2 relies on TE_8332A normal_range
- kind: tag
  ref: TE_8332A
  aspect: setpoints
  fingerprint: 4112efe131c0fc1f
  note: trb_high_flue_gas_o2 relies on TE_8332A setpoints
- kind: tag
  ref: ZZQBCHLL
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_flue_gas_o2 relies on ZZQBCHLL normal_range
- kind: tag
  ref: ZZQBCHLL
  aspect: setpoints
  fingerprint: a7f21a6b333e22f9
  note: trb_high_flue_gas_o2 relies on ZZQBCHLL setpoints
- kind: kg_node
  ref: furnace_chamber
  aspect: presence
  fingerprint: 94b36a9c522e2988
  note: trb_high_flue_gas_o2 relies on furnace_chamber presence
- kind: kg_node
  ref: furnace_lower_hearth
  aspect: presence
  fingerprint: 4e382c298e836394
  note: trb_high_flue_gas_o2 relies on furnace_lower_hearth presence
- kind: kg_node
  ref: economizer
  aspect: presence
  fingerprint: 20bfb78b831c15e4
  note: trb_high_flue_gas_o2 relies on economizer presence
- kind: kg_node
  ref: primary_fan
  aspect: presence
  fingerprint: e990b1d5a8d281d6
  note: trb_high_flue_gas_o2 relies on primary_fan presence
- kind: kg_node
  ref: secondary_fan
  aspect: presence
  fingerprint: 562fe19a5d8a7d10
  note: trb_high_flue_gas_o2 relies on secondary_fan presence
evidence:
- trb_high_flue_gas_o2 Rev 1.3
confidence: 0.8
status: active
tags_referenced:
- AIR_8301A
- AIR_8301B
- FT_8301
- FT_8302
- TE_8313B
- TE_8332A
- ZZQBCHLL
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_high_flue_gas_o2
  doc_type: troubleshooting
  revision: '1.3'
---

# Troubleshooting Guide — High Flue Gas O2 (Over-Aeration)

**Documented troubleshooting knowledge (trb_high_flue_gas_o2, Rev 1.3) for furnace_chamber, furnace_lower_hearth, economizer, primary_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:AIR_8301A` (normal_range) — trb_high_flue_gas_o2 relies on AIR_8301A normal_range
- `tag:AIR_8301A` (setpoints) — trb_high_flue_gas_o2 relies on AIR_8301A setpoints
- `tag:AIR_8301B` (normal_range) — trb_high_flue_gas_o2 relies on AIR_8301B normal_range
- `tag:AIR_8301B` (setpoints) — trb_high_flue_gas_o2 relies on AIR_8301B setpoints
- `tag:FT_8301` (normal_range) — trb_high_flue_gas_o2 relies on FT_8301 normal_range
- `tag:FT_8301` (setpoints) — trb_high_flue_gas_o2 relies on FT_8301 setpoints
- `tag:FT_8302` (normal_range) — trb_high_flue_gas_o2 relies on FT_8302 normal_range
- `tag:FT_8302` (setpoints) — trb_high_flue_gas_o2 relies on FT_8302 setpoints
- `tag:TE_8313B` (normal_range) — trb_high_flue_gas_o2 relies on TE_8313B normal_range
- `tag:TE_8313B` (setpoints) — trb_high_flue_gas_o2 relies on TE_8313B setpoints
- `tag:TE_8332A` (normal_range) — trb_high_flue_gas_o2 relies on TE_8332A normal_range
- `tag:TE_8332A` (setpoints) — trb_high_flue_gas_o2 relies on TE_8332A setpoints
- `tag:ZZQBCHLL` (normal_range) — trb_high_flue_gas_o2 relies on ZZQBCHLL normal_range
- `tag:ZZQBCHLL` (setpoints) — trb_high_flue_gas_o2 relies on ZZQBCHLL setpoints
- `kg_node:furnace_chamber` (presence) — trb_high_flue_gas_o2 relies on furnace_chamber presence
- `kg_node:furnace_lower_hearth` (presence) — trb_high_flue_gas_o2 relies on furnace_lower_hearth presence
- `kg_node:economizer` (presence) — trb_high_flue_gas_o2 relies on economizer presence
- `kg_node:primary_fan` (presence) — trb_high_flue_gas_o2 relies on primary_fan presence
- `kg_node:secondary_fan` (presence) — trb_high_flue_gas_o2 relies on secondary_fan presence
