# Handoff — OpenFarmPlanner

Rules and where everything lives: [AGENTS.md](AGENTS.md).
Rewrite this file when the state changes; don't keep a history here, git has it.
Short as possible, precise as needed: link to records instead of restating them.

Last updated: 2026-11-17

## State

Local evaluation instance on this Windows PC from `upstream/` (git-ignored clone of upstream
`87e3f847`): backend `cd upstream/backend && pdm run runserver` (:8000), frontend
`cd upstream/frontend && npm run dev` (:5173), demo login demo@example.com / demo-local-only.
`upstream/` is on branch `feat/library-snapshot-import` (commit `bf2dd523`, the import command)
(pushed to `origin`, i.e. `FloBurghardt/openfarmplanner`, private)
and carries one uncommitted Windows workaround (`frontend/src/pages/Dashboard.tsx:16`, see the
improvement log); stash it before `git pull`.

Workspace repo: `git@github.com:FloBurghardt/openfarmplanner-workspace.git` (private).

Community library: full snapshot (158 crops, 316 species) in
`records/work/261117_idea_local_openfarmplanner/data/`, pulled with `tools/pull_public_library.py`,
imported into the local instance. Results: [test_results.md](records/work/261117_idea_local_openfarmplanner/test_results.md).
Decisions 0001, 0002 accepted; 0003 (import command) and 0004 (repo layout) built/agreed but still `proposed` until the user confirms.

## Next

1. Upstream updates: `git -C upstream fetch upstream`, merge into `main`, push to `origin`; rebase `feat/library-snapshot-import` on it.
2. Configurable SQLite path (`backend/config/settings.py` hardcodes `BASE_DIR / 'db.sqlite3'`; `MEDIA_ROOT` already configurable), so farm data can live outside the code.
3. Start planning real data in German: own project, seasons from 2027, crops from the library.

## Waiting for the user

- Confirm 0003 and 0004.
- Confirm `share` class in PROJECT_CARD.md (set to `internal`).
