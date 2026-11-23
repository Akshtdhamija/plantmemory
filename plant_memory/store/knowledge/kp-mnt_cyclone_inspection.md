---
id: kp-mnt_cyclone_inspection
title: Cyclone Separator Internal Inspection
category: procedure
statement: Documented maintenance knowledge (mnt_cyclone_inspection, Rev 1.6) for
  cyclone_separator_left, cyclone_separator_right; valid only while the referenced
  plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: ZCLCCY
  aspect: presence
  fingerprint: c4fb5203a4d7e21d
  note: mnt_cyclone_inspection relies on ZCLCCY presence
- kind: tag
  ref: YCLCCY
  aspect: presence
  fingerprint: bad6a047719f2b26
  note: mnt_cyclone_inspection relies on YCLCCY presence
- kind: kg_node
  ref: cyclone_separator_left
  aspect: presence
  fingerprint: 8791e1b4d1519a86
  note: mnt_cyclone_inspection relies on cyclone_separator_left presence
- kind: kg_node
  ref: cyclone_separator_left
  aspect: connections
  fingerprint: 216692d645d70dde
  note: mnt_cyclone_inspection relies on cyclone_separator_left connections
- kind: kg_node
  ref: cyclone_separator_right
  aspect: presence
  fingerprint: 637b6e03b08bdc20
  note: mnt_cyclone_inspection relies on cyclone_separator_right presence
- kind: kg_node
  ref: cyclone_separator_right
  aspect: connections
  fingerprint: 59bd42f2cb055e11
  note: mnt_cyclone_inspection relies on cyclone_separator_right connections
evidence:
- mnt_cyclone_inspection Rev 1.6
confidence: 0.85
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
  doc_id: mnt_cyclone_inspection
  doc_type: maintenance
  revision: '1.6'
---

# Cyclone Separator Internal Inspection

**Documented maintenance knowledge (mnt_cyclone_inspection, Rev 1.6) for cyclone_separator_left, cyclone_separator_right; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:ZCLCCY` (presence) — mnt_cyclone_inspection relies on ZCLCCY presence
- `tag:YCLCCY` (presence) — mnt_cyclone_inspection relies on YCLCCY presence
- `kg_node:cyclone_separator_left` (presence) — mnt_cyclone_inspection relies on cyclone_separator_left presence
- `kg_node:cyclone_separator_left` (connections) — mnt_cyclone_inspection relies on cyclone_separator_left connections
- `kg_node:cyclone_separator_right` (presence) — mnt_cyclone_inspection relies on cyclone_separator_right presence
- `kg_node:cyclone_separator_right` (connections) — mnt_cyclone_inspection relies on cyclone_separator_right connections
