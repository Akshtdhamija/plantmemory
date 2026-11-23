---
id: kp-ds_steam_drum
title: Equipment Datasheet — Steam Drum
category: design_basis
statement: Documented datasheet knowledge (ds_steam_drum, Rev 1.4) for steam_drum;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: PTCA_8322A
  aspect: presence
  fingerprint: 7b3120f3fb8376e9
  note: ds_steam_drum relies on PTCA_8322A presence
- kind: tag
  ref: PTCA_8322A
  aspect: normal_range
  fingerprint: 8cd0951ac9bdf94f
  note: ds_steam_drum relies on PTCA_8322A normal_range
- kind: kg_node
  ref: steam_drum
  aspect: presence
  fingerprint: 54f5530ea3013878
  note: ds_steam_drum relies on steam_drum presence
- kind: kg_node
  ref: steam_drum
  aspect: connections
  fingerprint: 72d5d80cf187e567
  note: ds_steam_drum relies on steam_drum connections
evidence:
- ds_steam_drum Rev 1.4
confidence: 0.9
status: active
tags_referenced:
- PTCA_8322A
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_steam_drum
  doc_type: datasheet
  revision: '1.4'
---

# Equipment Datasheet — Steam Drum

**Documented datasheet knowledge (ds_steam_drum, Rev 1.4) for steam_drum; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:PTCA_8322A` (presence) — ds_steam_drum relies on PTCA_8322A presence
- `tag:PTCA_8322A` (normal_range) — ds_steam_drum relies on PTCA_8322A normal_range
- `kg_node:steam_drum` (presence) — ds_steam_drum relies on steam_drum presence
- `kg_node:steam_drum` (connections) — ds_steam_drum relies on steam_drum connections
