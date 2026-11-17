# Handoff — OpenFarmPlanner

Rules and where everything lives: [AGENTS.md](AGENTS.md).
Rewrite this file when the state changes; don't keep a history here, git has it.
Short as possible, precise as needed: link to records instead of restating them.

Last updated: 2026-11-17

## State

Local evaluation instance on this Windows PC from `upstream/`, branch `local` (upstream `main`
`57831b28` + our three branches, see [AGENTS.md](AGENTS.md#map)): backend
`cd upstream/backend && pdm run runserver` (:8000), frontend `cd upstream/frontend && npm run dev`
(:5173), demo login demo@example.com / demo-local-only. Farm data (database, media) in
`../OpenFarmPlanner_data/`, set in `upstream/backend/.env`; the old database copy is in
`upstream/backend/old_db_before_move/` (git-ignored, delete once happy).

Our branches on `origin` (`FloBurghardt/openfarmplanner`, private), each an upstream PR candidate:

| Branch | What |
|---|---|
| `feat/library-snapshot-import` | command `import_public_library_snapshot` (0003) |
| `feat/configurable-sqlite-path` | `SQLITE_PATH` env var |
| `fix/case-colliding-file-names` | dashboard crash on Windows/macOS |

Workspace repo: `git@github.com:FloBurghardt/openfarmplanner-workspace.git` (private).
Community library: full snapshot (158 crops, 316 species) in
`records/work/261117_idea_local_openfarmplanner/data/`, pulled with `tools/pull_public_library.py`,
imported locally. Results: [test_results.md](records/work/261117_idea_local_openfarmplanner/test_results.md).
Decisions 0001–0004 accepted.

## Next

1. Start planning in German: own project, seasons from 2027, crops from the library — needs the user's farm (locations, fields, beds) and crop wishes.
2. Back up `OpenFarmPlanner_data/` (target to be chosen by the user).
3. Upstream updates: `git -C upstream fetch upstream`, update `main`, push; merge `main` into `local`.
4. Later: offer the three branches upstream (open an issue first for the import, see its commit note on the species-API rule); move to CachyOS.

## Waiting for the user

- Farm structure and crop plans to start with (Next 1).
- Where to back up `OpenFarmPlanner_data/`.
- Confirm `share` class in PROJECT_CARD.md (set to `internal`).
