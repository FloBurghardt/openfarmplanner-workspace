# Setting up on a new machine

How to get the local OpenFarmPlanner running on another PC (planned: CachyOS) with the same
code, records and farm data. Written 2026-11-17 on Windows; the Linux steps follow the
upstream README and were **tested on CachyOS on 2026-11-17** (see "Differences found on CachyOS").

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

Prerequisites: `git`, `uv`, Node.js 22+ with npm 10+, and an SSH key for GitHub:

- Own key per machine: `ssh-keygen -t ed25519 -C "<machine>-openfarmplanner"`, then add
  `~/.ssh/id_ed25519.pub` on GitHub under Settings → SSH and GPG keys. Same account
  (`FloBurghardt`): `ssh -T git@github.com` answers "Hi FloBurghardt!".
- A different GitHub account: invite it as collaborator in **both** repos (Settings →
  Collaborators), accept the invitation, and add the key to that account instead.
- `git config --global user.name "…"` and `user.email "…"` on the new machine.

Layout (one folder per project, data outside both repos as in decision 0004):

```
~/Projekte/OpenFarmPlanner/
  workspace/        repo openfarmplanner-workspace
    upstream/       repo openfarmplanner, branch local
  data/             db.sqlite3 + media/ (from a backup or the USB stick)
```

```bash
# 1. Workspace and code
mkdir -p ~/Projekte/OpenFarmPlanner && cd ~/Projekte/OpenFarmPlanner
git clone git@github.com:FloBurghardt/openfarmplanner-workspace.git workspace
cd workspace
git clone -b local git@github.com:FloBurghardt/openfarmplanner.git upstream
git -C upstream remote add upstream https://github.com/OpenFarmPlanner/openfarmplanner.git

# 2. Farm data: db.sqlite3 and media/ of a backup folder -> ~/Projekte/OpenFarmPlanner/data/
mkdir -p ../data && cp -r /path/to/backup/{db.sqlite3,media} ../data/

# 3. Backend
uv tool install pdm
cp tools/backend.env.example upstream/backend/.env   # set SQLITE_PATH / MEDIA_ROOT to ../data
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

## Differences found on CachyOS (2026-11-17)

- **SSH agent from KeePassXC:** enable SSH agent integration in KeePassXC, add the key to the
  agent, and make sure `SSH_AUTH_SOCK` is set in the shell (here
  `/run/user/1000/ssh-agent.socket`; it was empty until the shell was restarted). Check with
  `ssh-add -l`.
- **`~/.ssh/config`:** `IdentityFile ~/.ssh/id_ed25519.pub` (public file, with
  `IdentitiesOnly yes`) prints "UNPROTECTED PRIVATE KEY FILE / bad permissions" if the `.pub`
  is 0644. Harmless once the agent serves the key (the warning stays); `chmod 600` silences it.
- **Collaborator account:** `ssh -T git@github.com` answers with the collaborator's own
  username (here `sandragmiaskistl`), not `FloBurghardt`. That is expected.
- **Node:** `sudo pacman -S --needed nodejs npm` gave Node 26.13 / npm 12.2 (newer than the
  required 22 / 10); install, tests and dev server work. An agent cannot run `sudo`; do it
  yourself with `! sudo ...`.
- **pdm:** `uv tool install pdm` puts it in `~/.local/bin`; that must be on `PATH`.
- **Tests need the test group:** `pdm install -dG test`, then
  `pdm run test farm/tests/test_import_public_library_snapshot.py`. Frontend:
  `npx vitest run src/__tests__/taskBoard.test.ts`. Both passed (2 and 3 tests).
- **npm** warns that the `core-js` postinstall script is blocked (`npm install-scripts`);
  the app is not affected.
- **Data:** the USB stick's `data/` was already copied to `~/Projekte/OpenFarmPlanner_transfer/`;
  `cp -r` from there to `data/` worked, `PRAGMA integrity_check` returned `ok`. The database
  holds 318 species (HANDOFF said 316; the difference is probably the demo project).
- `pdm run migrate` found nothing to apply: the backup was already migrated.

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
