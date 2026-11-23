---
id: kp-ctrl_combustion_air_o2_trim
title: Combustion Air / O2 Trim Control Loop — Description and Tuning
category: convention
statement: Documented controls knowledge (ctrl_combustion_air_o2_trim, Rev 1.6) for
  primary_fan, secondary_fan, furnace_chamber, economizer; valid only while the referenced
  plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: AIR_8301A
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: ctrl_combustion_air_o2_trim relies on AIR_8301A setpoints
- kind: tag
  ref: AIR_8301A
  aspect: distribution
  fingerprint: ee085b305c8ce4d2
  note: ctrl_combustion_air_o2_trim relies on AIR_8301A distribution
- kind: tag
  ref: AIR_8301B
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: ctrl_combustion_air_o2_trim relies on AIR_8301B setpoints
- kind: tag
  ref: AIR_8301B
  aspect: distribution
  fingerprint: 65ea2930589e81f5
  note: ctrl_combustion_air_o2_trim relies on AIR_8301B distribution
- kind: tag
  ref: FT_8301
  aspect: setpoints
  fingerprint: 73c1cefabdffe5dc
  note: ctrl_combustion_air_o2_trim relies on FT_8301 setpoints
- kind: tag
  ref: FT_8301
  aspect: distribution
  fingerprint: 2f2ee614bca54921
  note: ctrl_combustion_air_o2_trim relies on FT_8301 distribution
- kind: tag
  ref: FT_8302
  aspect: setpoints
  fingerprint: 019618f4bda8eea0
  note: ctrl_combustion_air_o2_trim relies on FT_8302 setpoints
- kind: tag
  ref: FT_8302
  aspect: distribution
  fingerprint: 1ab1d0457f744435
  note: ctrl_combustion_air_o2_trim relies on FT_8302 distribution
- kind: kg_node
  ref: primary_fan
  aspect: connections
  fingerprint: 52498e61aa2e79c2
  note: ctrl_combustion_air_o2_trim relies on primary_fan connections
- kind: kg_node
  ref: secondary_fan
  aspect: connections
  fingerprint: 2982b832f7011881
  note: ctrl_combustion_air_o2_trim relies on secondary_fan connections
- kind: kg_node
  ref: furnace_chamber
  aspect: connections
  fingerprint: 41c13b32f7879b9b
  note: ctrl_combustion_air_o2_trim relies on furnace_chamber connections
- kind: kg_node
  ref: economizer
  aspect: connections
  fingerprint: 6373639913b78ab5
  note: ctrl_combustion_air_o2_trim relies on economizer connections
evidence:
- ctrl_combustion_air_o2_trim Rev 1.6
confidence: 0.85
status: active
tags_referenced:
- AIR_8301A
- AIR_8301B
- FT_8301
- FT_8302
source: library
author: P07 Control and Instrumentation Engineer
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ctrl_combustion_air_o2_trim
  doc_type: controls
  revision: '1.6'
---

# Combustion Air / O2 Trim Control Loop — Description and Tuning

**Documented controls knowledge (ctrl_combustion_air_o2_trim, Rev 1.6) for primary_fan, secondary_fan, furnace_chamber, economizer; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:AIR_8301A` (setpoints) — ctrl_combustion_air_o2_trim relies on AIR_8301A setpoints
- `tag:AIR_8301A` (distribution) — ctrl_combustion_air_o2_trim relies on AIR_8301A distribution
- `tag:AIR_8301B` (setpoints) — ctrl_combustion_air_o2_trim relies on AIR_8301B setpoints
- `tag:AIR_8301B` (distribution) — ctrl_combustion_air_o2_trim relies on AIR_8301B distribution
- `tag:FT_8301` (setpoints) — ctrl_combustion_air_o2_trim relies on FT_8301 setpoints
- `tag:FT_8301` (distribution) — ctrl_combustion_air_o2_trim relies on FT_8301 distribution
- `tag:FT_8302` (setpoints) — ctrl_combustion_air_o2_trim relies on FT_8302 setpoints
- `tag:FT_8302` (distribution) — ctrl_combustion_air_o2_trim relies on FT_8302 distribution
- `kg_node:primary_fan` (connections) — ctrl_combustion_air_o2_trim relies on primary_fan connections
- `kg_node:secondary_fan` (connections) — ctrl_combustion_air_o2_trim relies on secondary_fan connections
- `kg_node:furnace_chamber` (connections) — ctrl_combustion_air_o2_trim relies on furnace_chamber connections
- `kg_node:economizer` (connections) — ctrl_combustion_air_o2_trim relies on economizer connections
