---
id: kp-trb_low_steam_flow
title: Troubleshooting Guide — Low Steam Flow (ZZQBCHLL Below Expected)
category: failure_mode
statement: Documented troubleshooting knowledge (trb_low_steam_flow, Rev 1.4) for
  steam_outlet, steam_drum, low_temp_superheater, high_temp_superheater; valid only
  while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: ZZQBCHLL
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_flow relies on ZZQBCHLL normal_range
- kind: tag
  ref: ZZQBCHLL
  aspect: setpoints
  fingerprint: a7f21a6b333e22f9
  note: trb_low_steam_flow relies on ZZQBCHLL setpoints
- kind: tag
  ref: PTCA_8322A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_flow relies on PTCA_8322A normal_range
- kind: tag
  ref: PTCA_8322A
  aspect: setpoints
  fingerprint: 038211a98afe3da6
  note: trb_low_steam_flow relies on PTCA_8322A setpoints
- kind: tag
  ref: PTCA_8324
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_low_steam_flow relies on PTCA_8324 normal_range
- kind: tag
  ref: PTCA_8324
  aspect: setpoints
  fingerprint: 9c793e10c139c2a6
  note: trb_low_steam_flow relies on PTCA_8324 setpoints
- kind: tag
  ref: TE_8332A
  aspect: normal_range
  fingerprint: 35700a8893a58270
  note: trb_low_steam_flow relies on TE_8332A normal_range
- kind: tag
  ref: TE_8332A
  aspect: setpoints
  fingerprint: 4112efe131c0fc1f
  note: trb_low_steam_flow relies on TE_8332A setpoints
- kind: kg_node
  ref: steam_outlet
  aspect: presence
  fingerprint: cc797c63c73e81f3
  note: trb_low_steam_flow relies on steam_outlet presence
- kind: kg_node
  ref: steam_drum
  aspect: presence
  fingerprint: 54f5530ea3013878
  note: trb_low_steam_flow relies on steam_drum presence
- kind: kg_node
  ref: low_temp_superheater
  aspect: presence
  fingerprint: db008506ee6ef24f
  note: trb_low_steam_flow relies on low_temp_superheater presence
- kind: kg_node
  ref: high_temp_superheater
  aspect: presence
  fingerprint: 45079fb9eb8efd8c
  note: trb_low_steam_flow relies on high_temp_superheater presence
evidence:
- trb_low_steam_flow Rev 1.4
confidence: 0.8
status: active
tags_referenced:
- ZZQBCHLL
- PTCA_8322A
- PTCA_8324
- TE_8332A
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_low_steam_flow
  doc_type: troubleshooting
  revision: '1.4'
---

# Troubleshooting Guide — Low Steam Flow (ZZQBCHLL Below Expected)

**Documented troubleshooting knowledge (trb_low_steam_flow, Rev 1.4) for steam_outlet, steam_drum, low_temp_superheater, high_temp_superheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:ZZQBCHLL` (normal_range) — trb_low_steam_flow relies on ZZQBCHLL normal_range
- `tag:ZZQBCHLL` (setpoints) — trb_low_steam_flow relies on ZZQBCHLL setpoints
- `tag:PTCA_8322A` (normal_range) — trb_low_steam_flow relies on PTCA_8322A normal_range
- `tag:PTCA_8322A` (setpoints) — trb_low_steam_flow relies on PTCA_8322A setpoints
- `tag:PTCA_8324` (normal_range) — trb_low_steam_flow relies on PTCA_8324 normal_range
- `tag:PTCA_8324` (setpoints) — trb_low_steam_flow relies on PTCA_8324 setpoints
- `tag:TE_8332A` (normal_range) — trb_low_steam_flow relies on TE_8332A normal_range
- `tag:TE_8332A` (setpoints) — trb_low_steam_flow relies on TE_8332A setpoints
- `kg_node:steam_outlet` (presence) — trb_low_steam_flow relies on steam_outlet presence
- `kg_node:steam_drum` (presence) — trb_low_steam_flow relies on steam_drum presence
- `kg_node:low_temp_superheater` (presence) — trb_low_steam_flow relies on low_temp_superheater presence
- `kg_node:high_temp_superheater` (presence) — trb_low_steam_flow relies on high_temp_superheater presence
