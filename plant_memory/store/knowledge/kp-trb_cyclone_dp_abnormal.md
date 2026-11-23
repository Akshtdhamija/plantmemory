---
id: kp-trb_cyclone_dp_abnormal
title: Troubleshooting Guide — Cyclone Separator Abnormal Differential Pressure
category: failure_mode
statement: Documented troubleshooting knowledge (trb_cyclone_dp_abnormal, Rev 1.5)
  for cyclone_separator_left, cyclone_separator_right, furnace_lower_hearth; valid
  only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: ZCLCCY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_cyclone_dp_abnormal relies on ZCLCCY normal_range
- kind: tag
  ref: ZCLCCY
  aspect: setpoints
  fingerprint: aed3aac7443890fb
  note: trb_cyclone_dp_abnormal relies on ZCLCCY setpoints
- kind: tag
  ref: YCLCCY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_cyclone_dp_abnormal relies on YCLCCY normal_range
- kind: tag
  ref: YCLCCY
  aspect: setpoints
  fingerprint: aed3aac7443890fb
  note: trb_cyclone_dp_abnormal relies on YCLCCY setpoints
- kind: tag
  ref: SXLTCYZ
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_cyclone_dp_abnormal relies on SXLTCYZ normal_range
- kind: tag
  ref: SXLTCYZ
  aspect: setpoints
  fingerprint: d016197cc51effcd
  note: trb_cyclone_dp_abnormal relies on SXLTCYZ setpoints
- kind: tag
  ref: SXLTCYY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_cyclone_dp_abnormal relies on SXLTCYY normal_range
- kind: tag
  ref: SXLTCYY
  aspect: setpoints
  fingerprint: d016197cc51effcd
  note: trb_cyclone_dp_abnormal relies on SXLTCYY setpoints
- kind: tag
  ref: FT_8306A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_cyclone_dp_abnormal relies on FT_8306A normal_range
- kind: tag
  ref: FT_8306A
  aspect: setpoints
  fingerprint: 437bff2dcda0f187
  note: trb_cyclone_dp_abnormal relies on FT_8306A setpoints
- kind: tag
  ref: FT_8306B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_cyclone_dp_abnormal relies on FT_8306B normal_range
- kind: tag
  ref: FT_8306B
  aspect: setpoints
  fingerprint: 437bff2dcda0f187
  note: trb_cyclone_dp_abnormal relies on FT_8306B setpoints
- kind: kg_node
  ref: cyclone_separator_left
  aspect: presence
  fingerprint: 8791e1b4d1519a86
  note: trb_cyclone_dp_abnormal relies on cyclone_separator_left presence
- kind: kg_node
  ref: cyclone_separator_right
  aspect: presence
  fingerprint: 637b6e03b08bdc20
  note: trb_cyclone_dp_abnormal relies on cyclone_separator_right presence
- kind: kg_node
  ref: furnace_lower_hearth
  aspect: presence
  fingerprint: 4e382c298e836394
  note: trb_cyclone_dp_abnormal relies on furnace_lower_hearth presence
evidence:
- trb_cyclone_dp_abnormal Rev 1.5
confidence: 0.8
status: active
tags_referenced:
- ZCLCCY
- YCLCCY
- SXLTCYZ
- SXLTCYY
- FT_8306A
- FT_8306B
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_cyclone_dp_abnormal
  doc_type: troubleshooting
  revision: '1.5'
---

# Troubleshooting Guide — Cyclone Separator Abnormal Differential Pressure

**Documented troubleshooting knowledge (trb_cyclone_dp_abnormal, Rev 1.5) for cyclone_separator_left, cyclone_separator_right, furnace_lower_hearth; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:ZCLCCY` (normal_range) — trb_cyclone_dp_abnormal relies on ZCLCCY normal_range
- `tag:ZCLCCY` (setpoints) — trb_cyclone_dp_abnormal relies on ZCLCCY setpoints
- `tag:YCLCCY` (normal_range) — trb_cyclone_dp_abnormal relies on YCLCCY normal_range
- `tag:YCLCCY` (setpoints) — trb_cyclone_dp_abnormal relies on YCLCCY setpoints
- `tag:SXLTCYZ` (normal_range) — trb_cyclone_dp_abnormal relies on SXLTCYZ normal_range
- `tag:SXLTCYZ` (setpoints) — trb_cyclone_dp_abnormal relies on SXLTCYZ setpoints
- `tag:SXLTCYY` (normal_range) — trb_cyclone_dp_abnormal relies on SXLTCYY normal_range
- `tag:SXLTCYY` (setpoints) — trb_cyclone_dp_abnormal relies on SXLTCYY setpoints
- `tag:FT_8306A` (normal_range) — trb_cyclone_dp_abnormal relies on FT_8306A normal_range
- `tag:FT_8306A` (setpoints) — trb_cyclone_dp_abnormal relies on FT_8306A setpoints
- `tag:FT_8306B` (normal_range) — trb_cyclone_dp_abnormal relies on FT_8306B normal_range
- `tag:FT_8306B` (setpoints) — trb_cyclone_dp_abnormal relies on FT_8306B setpoints
- `kg_node:cyclone_separator_left` (presence) — trb_cyclone_dp_abnormal relies on cyclone_separator_left presence
- `kg_node:cyclone_separator_right` (presence) — trb_cyclone_dp_abnormal relies on cyclone_separator_right presence
- `kg_node:furnace_lower_hearth` (presence) — trb_cyclone_dp_abnormal relies on furnace_lower_hearth presence
