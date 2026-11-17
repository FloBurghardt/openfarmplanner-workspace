---
number: 0001
title: Run OpenFarmPlanner locally on the PC, NAS later
status: accepted
date: 2026-11-17
decided: 2026-11-17
supersedes:
superseded_by:
source: records/work/261117_idea_local_openfarmplanner
---

# 0001 — Run OpenFarmPlanner locally on the PC, NAS later

## Context
The goal is to plan crops (what, when, where, cultivation) together with an LLM and to add
missing features. Verified in upstream `87e3f84`: the hosted project API token can write crops
only; beds, planting plans and tasks are read-only for tokens. The app is AGPL-3.0, Django +
React, with a documented local dev setup; there is no upstream Dockerfile and the ops repo is
private. The Windows PC is for evaluation only; the long-term machine is Linux (CachyOS), which is upstream's native platform. Details: [analysis](../work/261117_idea_local_openfarmplanner/analysis.md), [options](../work/261117_idea_local_openfarmplanner/options.md).

## Decision
We will run upstream OpenFarmPlanner from our own repository on a PC with the documented dev setup
(SQLite), let the LLM work against that local instance, and treat a Synology NAS container as
a later deployment step.

## Alternatives considered
- Hosted only with an API token: no install, live library; loses because the LLM cannot write
  planting plans and own features wait for upstream.
- NAS container right away: always on, LAN access; loses for now because we would write and
  maintain the image before knowing the setup is used.

## Consequences
We own backups and upgrades (git pull + migrate). The community library has to be pulled in
separately (see 0002). Revisit if upstream opens planting-plan writes to tokens, or once the
local setup is used daily from more than one device (→ NAS).
