---
id: kp-trb_idf_high_current
title: Troubleshooting Guide — IDF Motor High Current
category: failure_mode
statement: Documented troubleshooting knowledge (trb_idf_high_current, Rev 1.3) for
  induced_draft_fan; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: YFJ3_AI
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_idf_high_current relies on YFJ3_AI normal_range
- kind: tag
  ref: YFJ3_AI
  aspect: setpoints
  fingerprint: 7a0b322eae4fb288
  note: trb_idf_high_current relies on YFJ3_AI setpoints
- kind: tag
  ref: YFJ3_ZD1
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_idf_high_current relies on YFJ3_ZD1 normal_range
- kind: tag
  ref: YFJ3_ZD1
  aspect: setpoints
  fingerprint: 4c70db290afc43a5
  note: trb_idf_high_current relies on YFJ3_ZD1 setpoints
- kind: tag
  ref: YFJ3_ZD2
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_idf_high_current relies on YFJ3_ZD2 normal_range
- kind: tag
  ref: YFJ3_ZD2
  aspect: setpoints
  fingerprint: 4c70db290afc43a5
  note: trb_idf_high_current relies on YFJ3_ZD2 setpoints
- kind: tag
  ref: PT_8313A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: trb_idf_high_current relies on PT_8313A normal_range
- kind: tag
  ref: PT_8313A
  aspect: setpoints
  fingerprint: eafa06181230c8b4
  note: trb_idf_high_current relies on PT_8313A setpoints
- kind: kg_node
  ref: induced_draft_fan
  aspect: presence
  fingerprint: 762b82e81f982cdd
  note: trb_idf_high_current relies on induced_draft_fan presence
evidence:
- trb_idf_high_current Rev 1.3
confidence: 0.8
status: active
tags_referenced:
- YFJ3_AI
- YFJ3_ZD1
- YFJ3_ZD2
- PT_8313A
source: library
author: P05 Process Engineer, Combustion and Air
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: trb_idf_high_current
  doc_type: troubleshooting
  revision: '1.3'
---

# Troubleshooting Guide — IDF Motor High Current

**Documented troubleshooting knowledge (trb_idf_high_current, Rev 1.3) for induced_draft_fan; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:YFJ3_AI` (normal_range) — trb_idf_high_current relies on YFJ3_AI normal_range
- `tag:YFJ3_AI` (setpoints) — trb_idf_high_current relies on YFJ3_AI setpoints
- `tag:YFJ3_ZD1` (normal_range) — trb_idf_high_current relies on YFJ3_ZD1 normal_range
- `tag:YFJ3_ZD1` (setpoints) — trb_idf_high_current relies on YFJ3_ZD1 setpoints
- `tag:YFJ3_ZD2` (normal_range) — trb_idf_high_current relies on YFJ3_ZD2 normal_range
- `tag:YFJ3_ZD2` (setpoints) — trb_idf_high_current relies on YFJ3_ZD2 setpoints
- `tag:PT_8313A` (normal_range) — trb_idf_high_current relies on PT_8313A normal_range
- `tag:PT_8313A` (setpoints) — trb_idf_high_current relies on PT_8313A setpoints
- `kg_node:induced_draft_fan` (presence) — trb_idf_high_current relies on induced_draft_fan presence
