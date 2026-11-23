---
id: kp-mnt_boiler_annual_outage
title: Annual Outage Master Checklist
category: procedure
statement: Documented maintenance knowledge (mnt_boiler_annual_outage, Rev 3.1) for
  induced_draft_fan, primary_fan, secondary_fan, primary_air_preheater; valid only
  while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8332A
  aspect: presence
  fingerprint: 78f1080a5f2eb57d
  note: mnt_boiler_annual_outage relies on TE_8332A presence
- kind: tag
  ref: PTCA_8322A
  aspect: presence
  fingerprint: 7b3120f3fb8376e9
  note: mnt_boiler_annual_outage relies on PTCA_8322A presence
- kind: tag
  ref: YFJ3_ZD1
  aspect: presence
  fingerprint: 6e5139ca3779c193
  note: mnt_boiler_annual_outage relies on YFJ3_ZD1 presence
- kind: tag
  ref: YFJ3_ZD2
  aspect: presence
  fingerprint: 84032c15374c3114
  note: mnt_boiler_annual_outage relies on YFJ3_ZD2 presence
- kind: tag
  ref: AIR_8301A
  aspect: presence
  fingerprint: e9968992122b006e
  note: mnt_boiler_annual_outage relies on AIR_8301A presence
- kind: tag
  ref: AIR_8301B
  aspect: presence
  fingerprint: c5ca3f05ac49acfb
  note: mnt_boiler_annual_outage relies on AIR_8301B presence
- kind: tag
  ref: ZCLCCY
  aspect: presence
  fingerprint: c4fb5203a4d7e21d
  note: mnt_boiler_annual_outage relies on ZCLCCY presence
- kind: tag
  ref: YCLCCY
  aspect: presence
  fingerprint: bad6a047719f2b26
  note: mnt_boiler_annual_outage relies on YCLCCY presence
- kind: kg_node
  ref: induced_draft_fan
  aspect: presence
  fingerprint: 762b82e81f982cdd
  note: mnt_boiler_annual_outage relies on induced_draft_fan presence
- kind: kg_node
  ref: induced_draft_fan
  aspect: connections
  fingerprint: eac398facfdee248
  note: mnt_boiler_annual_outage relies on induced_draft_fan connections
- kind: kg_node
  ref: primary_fan
  aspect: presence
  fingerprint: e990b1d5a8d281d6
  note: mnt_boiler_annual_outage relies on primary_fan presence
- kind: kg_node
  ref: primary_fan
  aspect: connections
  fingerprint: 52498e61aa2e79c2
  note: mnt_boiler_annual_outage relies on primary_fan connections
- kind: kg_node
  ref: secondary_fan
  aspect: presence
  fingerprint: 562fe19a5d8a7d10
  note: mnt_boiler_annual_outage relies on secondary_fan presence
- kind: kg_node
  ref: secondary_fan
  aspect: connections
  fingerprint: 2982b832f7011881
  note: mnt_boiler_annual_outage relies on secondary_fan connections
- kind: kg_node
  ref: primary_air_preheater
  aspect: presence
  fingerprint: b2aa4e0a0df27171
  note: mnt_boiler_annual_outage relies on primary_air_preheater presence
- kind: kg_node
  ref: primary_air_preheater
  aspect: connections
  fingerprint: 54f93d3a67adee8a
  note: mnt_boiler_annual_outage relies on primary_air_preheater connections
- kind: kg_node
  ref: secondary_air_preheater
  aspect: presence
  fingerprint: bcbaf2072e176ce6
  note: mnt_boiler_annual_outage relies on secondary_air_preheater presence
- kind: kg_node
  ref: secondary_air_preheater
  aspect: connections
  fingerprint: c98541a4b51b6950
  note: mnt_boiler_annual_outage relies on secondary_air_preheater connections
- kind: kg_node
  ref: furnace_lower_hearth
  aspect: presence
  fingerprint: 4e382c298e836394
  note: mnt_boiler_annual_outage relies on furnace_lower_hearth presence
- kind: kg_node
  ref: furnace_lower_hearth
  aspect: connections
  fingerprint: 43282b4cf173bb96
  note: mnt_boiler_annual_outage relies on furnace_lower_hearth connections
- kind: kg_node
  ref: furnace_chamber
  aspect: presence
  fingerprint: 94b36a9c522e2988
  note: mnt_boiler_annual_outage relies on furnace_chamber presence
- kind: kg_node
  ref: furnace_chamber
  aspect: connections
  fingerprint: 41c13b32f7879b9b
  note: mnt_boiler_annual_outage relies on furnace_chamber connections
- kind: kg_node
  ref: cyclone_separator_left
  aspect: presence
  fingerprint: 8791e1b4d1519a86
  note: mnt_boiler_annual_outage relies on cyclone_separator_left presence
- kind: kg_node
  ref: cyclone_separator_left
  aspect: connections
  fingerprint: 216692d645d70dde
  note: mnt_boiler_annual_outage relies on cyclone_separator_left connections
- kind: kg_node
  ref: cyclone_separator_right
  aspect: presence
  fingerprint: 637b6e03b08bdc20
  note: mnt_boiler_annual_outage relies on cyclone_separator_right presence
- kind: kg_node
  ref: cyclone_separator_right
  aspect: connections
  fingerprint: 59bd42f2cb055e11
  note: mnt_boiler_annual_outage relies on cyclone_separator_right connections
- kind: kg_node
  ref: economizer
  aspect: presence
  fingerprint: 20bfb78b831c15e4
  note: mnt_boiler_annual_outage relies on economizer presence
- kind: kg_node
  ref: economizer
  aspect: connections
  fingerprint: 6373639913b78ab5
  note: mnt_boiler_annual_outage relies on economizer connections
- kind: kg_node
  ref: steam_drum
  aspect: presence
  fingerprint: 54f5530ea3013878
  note: mnt_boiler_annual_outage relies on steam_drum presence
- kind: kg_node
  ref: steam_drum
  aspect: connections
  fingerprint: 72d5d80cf187e567
  note: mnt_boiler_annual_outage relies on steam_drum connections
- kind: kg_node
  ref: low_temp_superheater
  aspect: presence
  fingerprint: db008506ee6ef24f
  note: mnt_boiler_annual_outage relies on low_temp_superheater presence
- kind: kg_node
  ref: low_temp_superheater
  aspect: connections
  fingerprint: e3b700afc5d9b890
  note: mnt_boiler_annual_outage relies on low_temp_superheater connections
- kind: kg_node
  ref: primary_desuperheater
  aspect: presence
  fingerprint: 86ec87aa23525fd3
  note: mnt_boiler_annual_outage relies on primary_desuperheater presence
- kind: kg_node
  ref: primary_desuperheater
  aspect: connections
  fingerprint: 7fb6dfa8af8a0f3a
  note: mnt_boiler_annual_outage relies on primary_desuperheater connections
- kind: kg_node
  ref: high_temp_superheater
  aspect: presence
  fingerprint: 45079fb9eb8efd8c
  note: mnt_boiler_annual_outage relies on high_temp_superheater presence
- kind: kg_node
  ref: high_temp_superheater
  aspect: connections
  fingerprint: 49b9a1468e7cc8af
  note: mnt_boiler_annual_outage relies on high_temp_superheater connections
- kind: kg_node
  ref: steam_outlet
  aspect: presence
  fingerprint: cc797c63c73e81f3
  note: mnt_boiler_annual_outage relies on steam_outlet presence
- kind: kg_node
  ref: steam_outlet
  aspect: connections
  fingerprint: b21894b95d290ebc
  note: mnt_boiler_annual_outage relies on steam_outlet connections
- kind: kg_node
  ref: chimney
  aspect: presence
  fingerprint: 53c39231a3b2a531
  note: mnt_boiler_annual_outage relies on chimney presence
- kind: kg_node
  ref: chimney
  aspect: connections
  fingerprint: 28f161baf207227d
  note: mnt_boiler_annual_outage relies on chimney connections
evidence:
- mnt_boiler_annual_outage Rev 3.1
confidence: 0.85
status: active
tags_referenced:
- TE_8332A
- PTCA_8322A
- YFJ3_ZD1
- YFJ3_ZD2
- AIR_8301A
- AIR_8301B
- ZCLCCY
- YCLCCY
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_boiler_annual_outage
  doc_type: maintenance
  revision: '3.1'
---

# Annual Outage Master Checklist

**Documented maintenance knowledge (mnt_boiler_annual_outage, Rev 3.1) for induced_draft_fan, primary_fan, secondary_fan, primary_air_preheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8332A` (presence) — mnt_boiler_annual_outage relies on TE_8332A presence
- `tag:PTCA_8322A` (presence) — mnt_boiler_annual_outage relies on PTCA_8322A presence
- `tag:YFJ3_ZD1` (presence) — mnt_boiler_annual_outage relies on YFJ3_ZD1 presence
- `tag:YFJ3_ZD2` (presence) — mnt_boiler_annual_outage relies on YFJ3_ZD2 presence
- `tag:AIR_8301A` (presence) — mnt_boiler_annual_outage relies on AIR_8301A presence
- `tag:AIR_8301B` (presence) — mnt_boiler_annual_outage relies on AIR_8301B presence
- `tag:ZCLCCY` (presence) — mnt_boiler_annual_outage relies on ZCLCCY presence
- `tag:YCLCCY` (presence) — mnt_boiler_annual_outage relies on YCLCCY presence
- `kg_node:induced_draft_fan` (presence) — mnt_boiler_annual_outage relies on induced_draft_fan presence
- `kg_node:induced_draft_fan` (connections) — mnt_boiler_annual_outage relies on induced_draft_fan connections
- `kg_node:primary_fan` (presence) — mnt_boiler_annual_outage relies on primary_fan presence
- `kg_node:primary_fan` (connections) — mnt_boiler_annual_outage relies on primary_fan connections
- `kg_node:secondary_fan` (presence) — mnt_boiler_annual_outage relies on secondary_fan presence
- `kg_node:secondary_fan` (connections) — mnt_boiler_annual_outage relies on secondary_fan connections
- `kg_node:primary_air_preheater` (presence) — mnt_boiler_annual_outage relies on primary_air_preheater presence
- `kg_node:primary_air_preheater` (connections) — mnt_boiler_annual_outage relies on primary_air_preheater connections
- `kg_node:secondary_air_preheater` (presence) — mnt_boiler_annual_outage relies on secondary_air_preheater presence
- `kg_node:secondary_air_preheater` (connections) — mnt_boiler_annual_outage relies on secondary_air_preheater connections
- `kg_node:furnace_lower_hearth` (presence) — mnt_boiler_annual_outage relies on furnace_lower_hearth presence
- `kg_node:furnace_lower_hearth` (connections) — mnt_boiler_annual_outage relies on furnace_lower_hearth connections
- `kg_node:furnace_chamber` (presence) — mnt_boiler_annual_outage relies on furnace_chamber presence
- `kg_node:furnace_chamber` (connections) — mnt_boiler_annual_outage relies on furnace_chamber connections
- `kg_node:cyclone_separator_left` (presence) — mnt_boiler_annual_outage relies on cyclone_separator_left presence
- `kg_node:cyclone_separator_left` (connections) — mnt_boiler_annual_outage relies on cyclone_separator_left connections
- `kg_node:cyclone_separator_right` (presence) — mnt_boiler_annual_outage relies on cyclone_separator_right presence
- `kg_node:cyclone_separator_right` (connections) — mnt_boiler_annual_outage relies on cyclone_separator_right connections
- `kg_node:economizer` (presence) — mnt_boiler_annual_outage relies on economizer presence
- `kg_node:economizer` (connections) — mnt_boiler_annual_outage relies on economizer connections
- `kg_node:steam_drum` (presence) — mnt_boiler_annual_outage relies on steam_drum presence
- `kg_node:steam_drum` (connections) — mnt_boiler_annual_outage relies on steam_drum connections
- `kg_node:low_temp_superheater` (presence) — mnt_boiler_annual_outage relies on low_temp_superheater presence
- `kg_node:low_temp_superheater` (connections) — mnt_boiler_annual_outage relies on low_temp_superheater connections
- `kg_node:primary_desuperheater` (presence) — mnt_boiler_annual_outage relies on primary_desuperheater presence
- `kg_node:primary_desuperheater` (connections) — mnt_boiler_annual_outage relies on primary_desuperheater connections
- `kg_node:high_temp_superheater` (presence) — mnt_boiler_annual_outage relies on high_temp_superheater presence
- `kg_node:high_temp_superheater` (connections) — mnt_boiler_annual_outage relies on high_temp_superheater connections
- `kg_node:steam_outlet` (presence) — mnt_boiler_annual_outage relies on steam_outlet presence
- `kg_node:steam_outlet` (connections) — mnt_boiler_annual_outage relies on steam_outlet connections
- `kg_node:chimney` (presence) — mnt_boiler_annual_outage relies on chimney presence
- `kg_node:chimney` (connections) — mnt_boiler_annual_outage relies on chimney connections
