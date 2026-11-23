---
id: kp-trb_high_furnace_pressure
title: Troubleshooting Guide — High Furnace Pressure (Trending Positive)
category: failure_mode
statement: Documented troubleshooting knowledge (trb_high_furnace_pressure, Rev 2.0)
  for furnace_chamber, induced_draft_fan; valid only while the referenced plant facets
  hold.
corrective_actions: []
groundings:
- kind: tag
  ref: PT_8313A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on PT_8313A normal_range
- kind: tag
  ref: PT_8313A
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_high_furnace_pressure relies on PT_8313A setpoints
- kind: tag
  ref: PT_8313B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on PT_8313B normal_range
- kind: tag
  ref: PT_8313B
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_high_furnace_pressure relies on PT_8313B setpoints
- kind: tag
  ref: PT_8313C
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on PT_8313C normal_range
- kind: tag
  ref: PT_8313C
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_high_furnace_pressure relies on PT_8313C setpoints
- kind: tag
  ref: PT_8313D
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on PT_8313D normal_range
- kind: tag
  ref: PT_8313D
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_high_furnace_pressure relies on PT_8313D setpoints
- kind: tag
  ref: PT_8313E
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on PT_8313E normal_range
- kind: tag
  ref: PT_8313E
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_high_furnace_pressure relies on PT_8313E setpoints
- kind: tag
  ref: PT_8313F
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on PT_8313F normal_range
- kind: tag
  ref: PT_8313F
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_high_furnace_pressure relies on PT_8313F setpoints
- kind: tag
  ref: YFJ3_AI
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on YFJ3_AI normal_range
- kind: tag
  ref: YFJ3_AI
  aspect: setpoints
  fingerprint: 7a0b322eae4fb288
  note: trb_high_furnace_pressure relies on YFJ3_AI setpoints
- kind: tag
  ref: YFJ3_ZD1
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on YFJ3_ZD1 normal_range
- kind: tag
  ref: YFJ3_ZD1
  aspect: setpoints
  fingerprint: 4c70db290afc43a5
  note: trb_high_furnace_pressure relies on YFJ3_ZD1 setpoints
- kind: tag
  ref: YFJ3_ZD2
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on YFJ3_ZD2 normal_range
- kind: tag
  ref: YFJ3_ZD2
  aspect: setpoints
  fingerprint: 4c70db290afc43a5
  note: trb_high_furnace_pressure relies on YFJ3_ZD2 setpoints
- kind: tag
  ref: FT_8301
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on FT_8301 normal_range
- kind: tag
  ref: FT_8301
  aspect: setpoints
  fingerprint: 73c1cefabdffe5dc
  note: trb_high_furnace_pressure relies on FT_8301 setpoints
- kind: tag
  ref: FT_8302
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on FT_8302 normal_range
- kind: tag
  ref: FT_8302
  aspect: setpoints
  fingerprint: 019618f4bda8eea0
  note: trb_high_furnace_pressure relies on FT_8302 setpoints
- kind: tag
  ref: AIR_8301A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on AIR_8301A normal_range
- kind: tag
  ref: AIR_8301A
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_high_furnace_pressure relies on AIR_8301A setpoints
- kind: tag
  ref: AIR_8301B
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_high_furnace_pressure relies on AIR_8301B normal_range
- kind: tag
  ref: AIR_8301B
  aspect: setpoints
  fingerprint: b0c0fbbb2e5a78da
  note: trb_high_furnace_pressure relies on AIR_8301B setpoints
- kind: kg_node
  ref: furnace_chamber
  aspect: presence
  fingerprint: 94b36a9c522e2988
  note: trb_high_furnace_pressure relies on furnace_chamber presence
- kind: kg_node
  ref: induced_draft_fan
  aspect: presence
  fingerprint: 762b82e81f982cdd
  note: trb_high_furnace_pressure relies on induced_draft_fan presence
evidence:
- trb_high_furnace_pressure Rev 2.0
confidence: 0.8
status: active
tags_referenced:
- PT_8313A
- PT_8313B
- PT_8313C
- PT_8313D
- PT_8313E
- PT_8313F
- YFJ3_AI
- YFJ3_ZD1
- YFJ3_ZD2
- FT_8301
- FT_8302
- AIR_8301A
- AIR_8301B
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_high_furnace_pressure
  doc_type: troubleshooting
  revision: '2.0'
---

# Troubleshooting Guide — High Furnace Pressure (Trending Positive)

**Documented troubleshooting knowledge (trb_high_furnace_pressure, Rev 2.0) for furnace_chamber, induced_draft_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:PT_8313A` (normal_range) — trb_high_furnace_pressure relies on PT_8313A normal_range
- `tag:PT_8313A` (setpoints) — trb_high_furnace_pressure relies on PT_8313A setpoints
- `tag:PT_8313B` (normal_range) — trb_high_furnace_pressure relies on PT_8313B normal_range
- `tag:PT_8313B` (setpoints) — trb_high_furnace_pressure relies on PT_8313B setpoints
- `tag:PT_8313C` (normal_range) — trb_high_furnace_pressure relies on PT_8313C normal_range
- `tag:PT_8313C` (setpoints) — trb_high_furnace_pressure relies on PT_8313C setpoints
- `tag:PT_8313D` (normal_range) — trb_high_furnace_pressure relies on PT_8313D normal_range
- `tag:PT_8313D` (setpoints) — trb_high_furnace_pressure relies on PT_8313D setpoints
- `tag:PT_8313E` (normal_range) — trb_high_furnace_pressure relies on PT_8313E normal_range
- `tag:PT_8313E` (setpoints) — trb_high_furnace_pressure relies on PT_8313E setpoints
- `tag:PT_8313F` (normal_range) — trb_high_furnace_pressure relies on PT_8313F normal_range
- `tag:PT_8313F` (setpoints) — trb_high_furnace_pressure relies on PT_8313F setpoints
- `tag:YFJ3_AI` (normal_range) — trb_high_furnace_pressure relies on YFJ3_AI normal_range
- `tag:YFJ3_AI` (setpoints) — trb_high_furnace_pressure relies on YFJ3_AI setpoints
- `tag:YFJ3_ZD1` (normal_range) — trb_high_furnace_pressure relies on YFJ3_ZD1 normal_range
- `tag:YFJ3_ZD1` (setpoints) — trb_high_furnace_pressure relies on YFJ3_ZD1 setpoints
- `tag:YFJ3_ZD2` (normal_range) — trb_high_furnace_pressure relies on YFJ3_ZD2 normal_range
- `tag:YFJ3_ZD2` (setpoints) — trb_high_furnace_pressure relies on YFJ3_ZD2 setpoints
- `tag:FT_8301` (normal_range) — trb_high_furnace_pressure relies on FT_8301 normal_range
- `tag:FT_8301` (setpoints) — trb_high_furnace_pressure relies on FT_8301 setpoints
- `tag:FT_8302` (normal_range) — trb_high_furnace_pressure relies on FT_8302 normal_range
- `tag:FT_8302` (setpoints) — trb_high_furnace_pressure relies on FT_8302 setpoints
- `tag:AIR_8301A` (normal_range) — trb_high_furnace_pressure relies on AIR_8301A normal_range
- `tag:AIR_8301A` (setpoints) — trb_high_furnace_pressure relies on AIR_8301A setpoints
- `tag:AIR_8301B` (normal_range) — trb_high_furnace_pressure relies on AIR_8301B normal_range
- `tag:AIR_8301B` (setpoints) — trb_high_furnace_pressure relies on AIR_8301B setpoints
- `kg_node:furnace_chamber` (presence) — trb_high_furnace_pressure relies on furnace_chamber presence
- `kg_node:induced_draft_fan` (presence) — trb_high_furnace_pressure relies on induced_draft_fan presence
