---
id: kp-mnt_feedwater_pump_check
title: Feedwater System Pre-Startup Check
category: procedure
statement: Documented maintenance knowledge (mnt_feedwater_pump_check, Rev 1.1) for
  economizer, steam_drum; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: PTCA_8322A
  aspect: presence
  fingerprint: 7b3120f3fb8376e9
  note: mnt_feedwater_pump_check relies on PTCA_8322A presence
- kind: kg_node
  ref: economizer
  aspect: presence
  fingerprint: 20bfb78b831c15e4
  note: mnt_feedwater_pump_check relies on economizer presence
- kind: kg_node
  ref: economizer
  aspect: connections
  fingerprint: 6373639913b78ab5
  note: mnt_feedwater_pump_check relies on economizer connections
- kind: kg_node
  ref: steam_drum
  aspect: presence
  fingerprint: 54f5530ea3013878
  note: mnt_feedwater_pump_check relies on steam_drum presence
- kind: kg_node
  ref: steam_drum
  aspect: connections
  fingerprint: 72d5d80cf187e567
  note: mnt_feedwater_pump_check relies on steam_drum connections
evidence:
- mnt_feedwater_pump_check Rev 1.1
confidence: 0.85
status: active
tags_referenced:
- PTCA_8322A
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_feedwater_pump_check
  doc_type: maintenance
  revision: '1.1'
---

# Feedwater System Pre-Startup Check

**Documented maintenance knowledge (mnt_feedwater_pump_check, Rev 1.1) for economizer, steam_drum; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:PTCA_8322A` (presence) — mnt_feedwater_pump_check relies on PTCA_8322A presence
- `kg_node:economizer` (presence) — mnt_feedwater_pump_check relies on economizer presence
- `kg_node:economizer` (connections) — mnt_feedwater_pump_check relies on economizer connections
- `kg_node:steam_drum` (presence) — mnt_feedwater_pump_check relies on steam_drum presence
- `kg_node:steam_drum` (connections) — mnt_feedwater_pump_check relies on steam_drum connections
