---
number: 0002
title: Pull the community crop library as a local snapshot
status: accepted
date: 2026-11-17
decided: 2026-11-17
supersedes:
superseded_by:
source: records/work/261117_idea_local_openfarmplanner
---

# 0002 — Pull the community crop library as a local snapshot

## Context
A local instance starts with an empty crop library. Verified: library contributions are CC BY-SA
4.0 and are intended to be reusable outside the app; there is no bulk export yet;
`GET /api/public-crops/` needs a logged-in session (403 anonymously; project tokens cannot list
it). Assumed, not checked: the Terms of Service allow a session script to read it.

## Decision
We will fetch the published library with a script using the user's own login session, store the
raw snapshot (JSON) with its date and attribution, and import it as local crops with a script that runs on any instance (Windows now, Linux later).

## Alternatives considered
- Enter crops by hand or from spreadsheets (the app has a spreadsheet import): no dependency on
  the site, but throws away the community's work.
- Wait for the announced export/public API: clean, but no date is known.
- Ask the maintainer for a dump: possible and friendly; can run alongside this decision.

## Consequences
The snapshot ages; refresh means re-running the script. Attribution and share-alike apply if
we ever redistribute the data. Revisit when upstream ships an official export or public API.
- 2026-11-17 — ToS checked (no rule against it, §7 confirms CC BY-SA reuse); first full pull: 158 entries, `records/work/261117_idea_local_openfarmplanner/data/public_crops_snapshot_2026-11-17.json`.
- 2026-11-17 — second pull, full library: 158 crops, 316 species, 16 families, plant-health catalogue empty → `records/work/261117_idea_local_openfarmplanner/data/public_library_snapshot_2026-11-17.json` (replaces the crops-only file above). Script now `tools/pull_public_library.py`.
