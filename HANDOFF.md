# Handoff — OpenFarmPlanner

Rules and where everything lives: [AGENTS.md](AGENTS.md).
Rewrite this file when the state changes; don't keep a history here, git has it.
Short as possible, precise as needed: link to records instead of restating them.

Last updated: 2026-11-17 (moved to CachyOS)

## State

Local evaluation instance, now on the CachyOS PC (`~/Projekte/OpenFarmPlanner/`, data in `../data/`; was Windows), from `upstream/`, branch `local` (upstream `main`
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

1. Done 2026-11-17: moved to CachyOS, both servers run, demo login works, tests of our branches pass. Differences from the guide: [docs/setup-new-machine.md](docs/setup-new-machine.md#differences-found-on-cachyos-2026-11-17). Commands here: `export PATH=$HOME/.local/bin:$PATH`, backend `pdm run runserver`, frontend `npm run dev`. `../OpenFarmPlanner_transfer/` can be deleted once the data is confirmed. This PC uses the second GitHub account (collaborator), SSH key from KeePassXC.
2. Then start planning in German there: own project, seasons from 2027, crops from the library — needs the user's farm (locations, fields, beds) and crop wishes.
3. Open points [OP-01](records/open-points/open-points.md) (where it runs for good) and OP-02 (backups to SMB).
4. Upstream updates: `git -C upstream fetch upstream`, update `main`, push; merge `main` into `local`.
5. Later: offer the three branches upstream (open an issue first for the import, see its commit note on the species-API rule).

## Waiting for the user

- Push the workspace (`git push` here; the agent's push was blocked and the SSH agent had no keys).
- Before leaving this PC: run a backup of `../OpenFarmPlanner_data/` to the SMB share — only if the demo data is worth keeping; otherwise start fresh with the snapshot import.
