---
number: 0004
title: Keep code, workspace and farm data separate
status: proposed
date: 2026-11-17
decided:
supersedes:
superseded_by:
source: records/work/records/work/261117_idea_local_openfarmplanner
---

# 0004 — Keep code, workspace and farm data separate

## Context
Upstream keeps code and deployment apart. We need to pull upstream updates and offer features
back, keep our records and library snapshots, and move later to CachyOS, possibly to another
GitHub user. A GitHub fork of a public repo can't be private. SQLite's path is hardcoded inside
the code tree; `MEDIA_ROOT` is configurable.

## Decision
We will keep three things apart: the code in a private repo `openfarmplanner` that stays a
1:1 copy of upstream (remote `upstream`, own work on branches), cloned into the git-ignored
`upstream/` folder of this workspace; this folder as its own private repo
`openfarmplanner-workspace`; and the farm data (database, media) outside both, backed up
separately.

## Alternatives considered
- One repo with our records inside the code tree: simpler at first, but every upstream merge and
  every PR has to work around our files.
- Git submodule for the code: pins commits explicitly, but makes everyday pulls clumsy.

## Consequences
A new machine needs two clones plus the data folder from the backup. The database location has
to become configurable first (or PostgreSQL). Moving to another GitHub user is a repo transfer or
a collaborator invite plus `git remote set-url`.
