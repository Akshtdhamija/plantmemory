---
id: kp-trb_bed_inventory_loss
title: Troubleshooting Guide — Bed Inventory Loss
category: failure_mode
statement: Documented troubleshooting knowledge (trb_bed_inventory_loss, Rev 1.8)
  for furnace_lower_hearth, cyclone_separator_left, cyclone_separator_right; valid
  only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: SXLTCYZ
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on SXLTCYZ normal_range
- kind: tag
  ref: SXLTCYZ
  aspect: setpoints
  fingerprint: d016197cc51effcd
  note: trb_bed_inventory_loss relies on SXLTCYZ setpoints
- kind: tag
  ref: SXLTCYY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on SXLTCYY normal_range
- kind: tag
  ref: SXLTCYY
  aspect: setpoints
  fingerprint: d016197cc51effcd
  note: trb_bed_inventory_loss relies on SXLTCYY setpoints
- kind: tag
  ref: ZCLCCY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on ZCLCCY normal_range
- kind: tag
  ref: ZCLCCY
  aspect: setpoints
  fingerprint: aed3aac7443890fb
  note: trb_bed_inventory_loss relies on ZCLCCY setpoints
- kind: tag
  ref: YCLCCY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on YCLCCY normal_range
- kind: tag
  ref: YCLCCY
  aspect: setpoints
  fingerprint: aed3aac7443890fb
  note: trb_bed_inventory_loss relies on YCLCCY setpoints
- kind: tag
  ref: FT_8306A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on FT_8306A normal_range
- kind: tag
  ref: FT_8306A
  aspect: setpoints
  fingerprint: 437bff2dcda0f187
  note: trb_bed_inventory_loss relies on FT_8306A setpoints
- kind: tag
  ref: FT_8306B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on FT_8306B normal_range
- kind: tag
  ref: FT_8306B
  aspect: setpoints
  fingerprint: 437bff2dcda0f187
  note: trb_bed_inventory_loss relies on FT_8306B setpoints
- kind: tag
  ref: TE_8313B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on TE_8313B normal_range
- kind: tag
  ref: TE_8313B
  aspect: setpoints
  fingerprint: f6978d61088b4c8f
  note: trb_bed_inventory_loss relies on TE_8313B setpoints
- kind: tag
  ref: AIR_8301A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on AIR_8301A normal_range
- kind: tag
  ref: AIR_8301A
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_bed_inventory_loss relies on AIR_8301A setpoints
- kind: tag
  ref: AIR_8301B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_bed_inventory_loss relies on AIR_8301B normal_range
- kind: tag
  ref: AIR_8301B
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_bed_inventory_loss relies on AIR_8301B setpoints
- kind: kg_node
  ref: furnace_lower_hearth
  aspect: presence
  fingerprint: 4e382c298e836394
  note: trb_bed_inventory_loss relies on furnace_lower_hearth presence
- kind: kg_node
  ref: cyclone_separator_left
  aspect: presence
  fingerprint: 8791e1b4d1519a86
  note: trb_bed_inventory_loss relies on cyclone_separator_left presence
- kind: kg_node
  ref: cyclone_separator_right
  aspect: presence
  fingerprint: 637b6e03b08bdc20
  note: trb_bed_inventory_loss relies on cyclone_separator_right presence
evidence:
- trb_bed_inventory_loss Rev 1.8
confidence: 0.8
status: active
tags_referenced:
- SXLTCYZ
- SXLTCYY
- ZCLCCY
- YCLCCY
- FT_8306A
- FT_8306B
- TE_8313B
- AIR_8301A
- AIR_8301B
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_bed_inventory_loss
  doc_type: troubleshooting
  revision: '1.8'
---

# Troubleshooting Guide — Bed Inventory Loss

**Documented troubleshooting knowledge (trb_bed_inventory_loss, Rev 1.8) for furnace_lower_hearth, cyclone_separator_left, cyclone_separator_right; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:SXLTCYZ` (normal_range) — trb_bed_inventory_loss relies on SXLTCYZ normal_range
- `tag:SXLTCYZ` (setpoints) — trb_bed_inventory_loss relies on SXLTCYZ setpoints
- `tag:SXLTCYY` (normal_range) — trb_bed_inventory_loss relies on SXLTCYY normal_range
- `tag:SXLTCYY` (setpoints) — trb_bed_inventory_loss relies on SXLTCYY setpoints
- `tag:ZCLCCY` (normal_range) — trb_bed_inventory_loss relies on ZCLCCY normal_range
- `tag:ZCLCCY` (setpoints) — trb_bed_inventory_loss relies on ZCLCCY setpoints
- `tag:YCLCCY` (normal_range) — trb_bed_inventory_loss relies on YCLCCY normal_range
- `tag:YCLCCY` (setpoints) — trb_bed_inventory_loss relies on YCLCCY setpoints
- `tag:FT_8306A` (normal_range) — trb_bed_inventory_loss relies on FT_8306A normal_range
- `tag:FT_8306A` (setpoints) — trb_bed_inventory_loss relies on FT_8306A setpoints
- `tag:FT_8306B` (normal_range) — trb_bed_inventory_loss relies on FT_8306B normal_range
- `tag:FT_8306B` (setpoints) — trb_bed_inventory_loss relies on FT_8306B setpoints
- `tag:TE_8313B` (normal_range) — trb_bed_inventory_loss relies on TE_8313B normal_range
- `tag:TE_8313B` (setpoints) — trb_bed_inventory_loss relies on TE_8313B setpoints
- `tag:AIR_8301A` (normal_range) — trb_bed_inventory_loss relies on AIR_8301A normal_range
- `tag:AIR_8301A` (setpoints) — trb_bed_inventory_loss relies on AIR_8301A setpoints
- `tag:AIR_8301B` (normal_range) — trb_bed_inventory_loss relies on AIR_8301B normal_range
- `tag:AIR_8301B` (setpoints) — trb_bed_inventory_loss relies on AIR_8301B setpoints
- `kg_node:furnace_lower_hearth` (presence) — trb_bed_inventory_loss relies on furnace_lower_hearth presence
- `kg_node:cyclone_separator_left` (presence) — trb_bed_inventory_loss relies on cyclone_separator_left presence
- `kg_node:cyclone_separator_right` (presence) — trb_bed_inventory_loss relies on cyclone_separator_right presence
