---
id: kp-ds_cyclone_separator
title: Equipment Datasheet — Cyclone Separators (Left and Right)
category: design_basis
statement: Documented datasheet knowledge (ds_cyclone_separator, Rev 1.3) for cyclone_separator_left,
  cyclone_separator_right; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: ZCLCCY
  aspect: presence
  fingerprint: c4fb5203a4d7e21d
  note: ds_cyclone_separator relies on ZCLCCY presence
- kind: tag
  ref: ZCLCCY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_cyclone_separator relies on ZCLCCY normal_range
- kind: tag
  ref: YCLCCY
  aspect: presence
  fingerprint: bad6a047719f2b26
  note: ds_cyclone_separator relies on YCLCCY presence
- kind: tag
  ref: YCLCCY
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_cyclone_separator relies on YCLCCY normal_range
- kind: kg_node
  ref: cyclone_separator_left
  aspect: presence
  fingerprint: 8791e1b4d1519a86
  note: ds_cyclone_separator relies on cyclone_separator_left presence
- kind: kg_node
  ref: cyclone_separator_left
  aspect: connections
  fingerprint: 216692d645d70dde
  note: ds_cyclone_separator relies on cyclone_separator_left connections
- kind: kg_node
  ref: cyclone_separator_right
  aspect: presence
  fingerprint: 637b6e03b08bdc20
  note: ds_cyclone_separator relies on cyclone_separator_right presence
- kind: kg_node
  ref: cyclone_separator_right
  aspect: connections
  fingerprint: 59bd42f2cb055e11
  note: ds_cyclone_separator relies on cyclone_separator_right connections
evidence:
- ds_cyclone_separator Rev 1.3
confidence: 0.9
status: active
tags_referenced:
- ZCLCCY
- YCLCCY
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_cyclone_separator
  doc_type: datasheet
  revision: '1.3'
---

# Equipment Datasheet — Cyclone Separators (Left and Right)

**Documented datasheet knowledge (ds_cyclone_separator, Rev 1.3) for cyclone_separator_left, cyclone_separator_right; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:ZCLCCY` (presence) — ds_cyclone_separator relies on ZCLCCY presence
- `tag:ZCLCCY` (normal_range) — ds_cyclone_separator relies on ZCLCCY normal_range
- `tag:YCLCCY` (presence) — ds_cyclone_separator relies on YCLCCY presence
- `tag:YCLCCY` (normal_range) — ds_cyclone_separator relies on YCLCCY normal_range
- `kg_node:cyclone_separator_left` (presence) — ds_cyclone_separator relies on cyclone_separator_left presence
- `kg_node:cyclone_separator_left` (connections) — ds_cyclone_separator relies on cyclone_separator_left connections
- `kg_node:cyclone_separator_right` (presence) — ds_cyclone_separator relies on cyclone_separator_right presence
- `kg_node:cyclone_separator_right` (connections) — ds_cyclone_separator relies on cyclone_separator_right connections
