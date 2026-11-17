# Agent instructions — OpenFarmPlanner

Current state, next steps and open questions: [HANDOFF.md](HANDOFF.md). Read it first.

## What this is

[OpenFarmPlanner_CARD.md](OpenFarmPlanner_CARD.md): what it is and what others may reuse. Without a card:
one or two sentences instead. Details for users: [README.md](README.md).

## Map

- [records/decisions/](records/decisions/) — decision records: why things are the way they are. Read before reopening any decision.
- [records/improvement-log/](records/improvement-log/improvement-log.md) — issues, risks, ideas, lessons and loose notes; nobody on the hook.
- [records/open-points/](records/open-points/open-points.md) — what must be settled, each with an owner and a target.
- [records/requirements/](records/requirements/requirements.md) — what the result must do; cited documents in `sources/`.
- [records/work/](records/work/index.md) — one working folder per piece of work; `README.md` in each is its status.
- [tools/](tools/) — scripts that run outside the app, e.g. `pull_public_library.py` (library snapshot from openfarmplanner.org).
- `upstream/` — git-ignored clone of the code repo `git@github.com:FloBurghardt/openfarmplanner.git` (private, 1:1 copy of upstream; own work on branches). Remote `origin` is our copy, `upstream` is https://github.com/OpenFarmPlanner/openfarmplanner. New machine: `git clone git@github.com:FloBurghardt/openfarmplanner.git upstream && git -C upstream remote add upstream https://github.com/OpenFarmPlanner/openfarmplanner.git`. Branches there: `main` = upstream unchanged; one `feat/…`/`fix/…` branch per change, based on `main` so it can go upstream as a PR; `local` = `main` merged with our branches, the one that runs. Farm data lives outside both repos, set in `upstream/backend/.env` via `SQLITE_PATH` and `MEDIA_ROOT` ([0004](records/decisions/0004-separate-code-workspace-and-farm-data.md)); on this PC `../OpenFarmPlanner_data/`.
- [docs/](docs/) — shipped documentation, every file linked from README.

## Rules

- Keep `HANDOFF.md` current at the end of every task and before every commit. Rewrite, don't append.
- When a requirement, open point or decision changes, update its record in the same step.
- When what the project is, what it offers others or what may leave it changes, update `OpenFarmPlanner_CARD.md`.
- A rule lives in one place. Link to it; don't copy it.
- Scripts that maintain records run with `uv run`, e.g. `uv run records/reindex.py`.

## Commits

If the project uses git, work an agent did names it in trailers at the end of the commit
message. Write what you know; write `unknown` for what you cannot see, never a guess. A
harness that adds its own `Co-Authored-By` line covers the first line; add the other three.

```
Co-Authored-By: <model name> <noreply address of the vendor>
AI-Model: <model id>
AI-Effort: <effort setting, or unknown>
AI-Harness: <claude-code | opencode | codex | …, or unknown>
```
