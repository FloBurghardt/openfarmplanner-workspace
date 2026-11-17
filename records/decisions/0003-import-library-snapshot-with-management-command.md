---
number: 0003
title: Import library snapshots with a management command in the code repo
status: proposed
date: 2026-11-17
decided:
supersedes:
superseded_by:
source: records/work/records/work/261117_idea_local_openfarmplanner
---

# 0003 — Import library snapshots with a management command in the code repo

## Context
Snapshots from 0002 are API payloads (cm units, family names, hosted species ids). 14 of the 66
species in the first snapshot don't exist in a fresh local taxonomy. Upstream already creates
library rows through the ORM for its demo. Details: [import_design](../work/records/work/261117_idea_local_openfarmplanner/import_design.md).

## Decision
We will write a Django management command, `import_public_library_snapshot`, on a feature
branch of our code repo. It maps species by name (creating missing ones), writes published
library rows idempotently, records source and licence, and has a dry-run mode.

## Alternatives considered
- Script in the workspace that posts entries as project crops through the API: no code change,
  but no local library, no update tracking, and missing species stay missing.

## Consequences
Every instance (Windows, CachyOS, NAS) gets the library by running one command. The command
has to follow upstream's model changes; offering it upstream would move that burden. Revisit
when upstream ships its own export/import.
