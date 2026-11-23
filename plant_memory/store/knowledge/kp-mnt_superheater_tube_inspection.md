---
id: kp-mnt_superheater_tube_inspection
title: Superheater Tube Inspection — Low Temp and High Temp
category: procedure
statement: Documented maintenance knowledge (mnt_superheater_tube_inspection, Rev
  1.4) for low_temp_superheater, high_temp_superheater; valid only while the referenced
  plant facets hold.
corrective_actions: []
groundings:
- kind: tag
  ref: TE_8332A
  aspect: presence
  fingerprint: 78f1080a5f2eb57d
  note: mnt_superheater_tube_inspection relies on TE_8332A presence
- kind: kg_node
  ref: low_temp_superheater
  aspect: presence
  fingerprint: db008506ee6ef24f
  note: mnt_superheater_tube_inspection relies on low_temp_superheater presence
- kind: kg_node
  ref: low_temp_superheater
  aspect: connections
  fingerprint: e3b700afc5d9b890
  note: mnt_superheater_tube_inspection relies on low_temp_superheater connections
- kind: kg_node
  ref: high_temp_superheater
  aspect: presence
  fingerprint: 45079fb9eb8efd8c
  note: mnt_superheater_tube_inspection relies on high_temp_superheater presence
- kind: kg_node
  ref: high_temp_superheater
  aspect: connections
  fingerprint: 49b9a1468e7cc8af
  note: mnt_superheater_tube_inspection relies on high_temp_superheater connections
evidence:
- mnt_superheater_tube_inspection Rev 1.4
confidence: 0.85
status: active
tags_referenced:
- TE_8332A
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: mnt_superheater_tube_inspection
  doc_type: maintenance
  revision: '1.4'
---

# Superheater Tube Inspection — Low Temp and High Temp

**Documented maintenance knowledge (mnt_superheater_tube_inspection, Rev 1.4) for low_temp_superheater, high_temp_superheater; valid only while the referenced plant facets hold.**

## Grounded to

- `tag:TE_8332A` (presence) — mnt_superheater_tube_inspection relies on TE_8332A presence
- `kg_node:low_temp_superheater` (presence) — mnt_superheater_tube_inspection relies on low_temp_superheater presence
- `kg_node:low_temp_superheater` (connections) — mnt_superheater_tube_inspection relies on low_temp_superheater connections
- `kg_node:high_temp_superheater` (presence) — mnt_superheater_tube_inspection relies on high_temp_superheater presence
- `kg_node:high_temp_superheater` (connections) — mnt_superheater_tube_inspection relies on high_temp_superheater connections
