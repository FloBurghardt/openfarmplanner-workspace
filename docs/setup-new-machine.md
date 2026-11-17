# Setting up on a new machine

How to get the local OpenFarmPlanner running on another PC (planned: CachyOS) with the same
code, records and farm data. Written 2026-11-17 on Windows; the Linux steps follow the
upstream README but are **not yet tested** on CachyOS.

## What moves how

| What | How it gets there |
|---|---|
| This workspace (records, tools, library snapshot) | `git clone` from GitHub |
| The code | `git clone` from GitHub into `upstream/` |
| Farm data (database, photos) | restore the newest backup from the SMB share |
| `upstream/backend/.env` | from [tools/backend.env.example](../tools/backend.env.example) (git-ignored, so never in a repo) |
| `.venv`, `node_modules` | rebuilt by `pdm install` / `npm install` (machine- and OS-specific, never copied) |

**Don't work directly on the SMB share.** SQLite's WAL mode (used by upstream) does not work
over network file systems and can corrupt the database; `node_modules` and `.venv` are tens of
thousands of small files (slow over SMB, and OS-specific anyway); upstream uses relative
symlinks (`.agents/skills/`) and executable bits that SMB handles poorly; and two machines on
one working copy fight over git's lock files. The share is for **backups** (see
[tools/backup_data.py](../tools/backup_data.py)); GitHub is how code and records move.

## Steps (Linux)

Prerequisites: `git`, `uv`, Node.js 22+ with npm 10+, and an SSH key for GitHub
(`ssh -T git@github.com` answers "Hi FloBurghardt!").

```bash
# 1. Workspace and code
git clone git@github.com:FloBurghardt/openfarmplanner-workspace.git OpenFarmPlanner
cd OpenFarmPlanner
git clone -b local git@github.com:FloBurghardt/openfarmplanner.git upstream
git -C upstream remote add upstream https://github.com/OpenFarmPlanner/openfarmplanner.git

# 2. Farm data: newest backup folder from the share -> local disk
mkdir -p ~/OpenFarmPlanner_data
cp -r /path/to/share/openfarmplanner/<newest>/{db.sqlite3,media} ~/OpenFarmPlanner_data/

# 3. Backend
uv tool install pdm
cp tools/backend.env.example upstream/backend/.env   # then fix the two paths
cd upstream/backend && pdm install && pdm run migrate && cd ../..

# 4. Frontend
cd upstream/frontend && npm install && cd ../..

# 5. Run (two terminals)
cd upstream/backend && pdm run runserver
cd upstream/frontend && npm run dev        # http://localhost:5173
```

Without a backup (fresh start) skip step 2 and fill the library from the snapshot instead:
`cd upstream/backend && pdm run python manage.py import_public_library_snapshot ../../records/work/261117_idea_local_openfarmplanner/data/public_library_snapshot_2026-11-17.json`,
then create an account with `pdm run createsuperuser`.

## Starting prompt for the agent on the new machine

Paste this into the first session in the cloned workspace folder:

```
This is the OpenFarmPlanner workspace, freshly cloned on a new machine (CachyOS). Read
AGENTS.md and HANDOFF.md first. Then follow docs/setup-new-machine.md step by step:
check the prerequisites, clone the code into upstream/ (branch local), set up the backend
.env from tools/backend.env.example with this machine's data paths, install, migrate and
start both servers. Ask me where the newest backup on the SMB share is before restoring
farm data. Record what differed from the guide (it was written on Windows and is untested
on Linux) in the guide itself and in HANDOFF.md, and run the tests of our branches
(backend/farm/tests/test_import_public_library_snapshot.py). Don't push or change anything
online without asking.
```
