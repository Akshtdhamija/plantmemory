---
id: kp-ds_stack_chimney
title: Equipment Datasheet — Stack / Chimney
category: design_basis
statement: Documented datasheet knowledge (ds_stack_chimney, Rev 1.0) for chimney;
  valid only while the referenced plant facets hold.
corrective_actions: []
groundings:
- kind: kg_node
  ref: chimney
  aspect: presence
  fingerprint: 53c39231a3b2a531
  note: ds_stack_chimney relies on chimney presence
- kind: kg_node
  ref: chimney
  aspect: connections
  fingerprint: 28f161baf207227d
  note: ds_stack_chimney relies on chimney connections
evidence:
- ds_stack_chimney Rev 1.0
confidence: 0.9
status: active
tags_referenced: []
source: library
author: P09 Maintenance Planner, Rotating Equipment
session: ''
created_at: '2026-11-23T07:51:32+00:00'
updated_at: '2026-11-23T07:51:32+00:00'
provenance:
  doc_id: ds_stack_chimney
  doc_type: datasheet
  revision: '1.0'
---

# Equipment Datasheet — Stack / Chimney

**Documented datasheet knowledge (ds_stack_chimney, Rev 1.0) for chimney; valid only while the referenced plant facets hold.**

## Grounded to

- `kg_node:chimney` (presence) — ds_stack_chimney relies on chimney presence
- `kg_node:chimney` (connections) — ds_stack_chimney relies on chimney connections
