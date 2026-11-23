---
id: kp-ds_high_temp_superheater
title: Equipment Datasheet — High Temperature Superheater
category: design_basis
statement: Documented datasheet knowledge (ds_high_temp_superheater, Rev 1.2) for
  high_temp_superheater; valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8332A
  aspect: presence
  fingerprint: 78f1080a5f2eb57d
  note: ds_high_temp_superheater relies on TE_8332A presence
- kind: tag
  ref: TE_8332A
  aspect: normal_range
  fingerprint: 35700a8893a58270
  note: ds_high_temp_superheater relies on TE_8332A normal_range
- kind: kg_node
  ref: high_temp_superheater
  aspect: presence
  fingerprint: 45079fb9eb8efd8c
  note: ds_high_temp_superheater relies on high_temp_superheater presence
- kind: kg_node
  ref: high_temp_superheater
  aspect: connections
  fingerprint: 49b9a1468e7cc8af
  note: ds_high_temp_superheater relies on high_temp_superheater connections
evidence:
- ds_high_temp_superheater Rev 1.2
confidence: 0.9
status: active
tags_referenced:
- TE_8332A
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_high_temp_superheater
  doc_type: datasheet
  revision: '1.2'
---

# Equipment Datasheet — High Temperature Superheater

**Documented datasheet knowledge (ds_high_temp_superheater, Rev 1.2) for high_temp_superheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8332A` (presence) — ds_high_temp_superheater relies on TE_8332A presence
- `tag:TE_8332A` (normal_range) — ds_high_temp_superheater relies on TE_8332A normal_range
- `kg_node:high_temp_superheater` (presence) — ds_high_temp_superheater relies on high_temp_superheater presence
- `kg_node:high_temp_superheater` (connections) — ds_high_temp_superheater relies on high_temp_superheater connections
