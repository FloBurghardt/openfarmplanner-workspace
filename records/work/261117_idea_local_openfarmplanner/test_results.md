# Spike results — 2026-11-17

Upstream `87e3f847` cloned to `upstream/` (git-ignored). Windows 11, Python 3.13.2, Node 22.18,
PDM 2.29.7 (installed with `uv tool install pdm`). All results **V** (ran) unless marked **A**.

## Spike 1 — runs on Windows: pass

- `backend/.env` written for local dev (DEBUG, no SSL/HSTS, no notification mail; not the
  production-like `.env.example`). `pdm install` (64 packages), `pdm run migrate`: clean.
- `seed_demo_project --language de --username demo --user-email demo@example.com --password demo-local-only`
  → project "Solawi Sonnenacker": 6 fields, 20 beds, 30 crops, 65 planting plans, 4 seasons,
  30 public library entries.
- `npm install`, `npm run dev`: frontend on http://localhost:5173, backend on :8000, Vite proxy
  works. Login in the browser: demo@example.com / demo-local-only.
- Logs: `throwaway_backend.log`, `throwaway_frontend.log`.
- **Windows bug found by the user:** after login the dashboard crashed ("The page could not be
  restored automatically"). Cause: `TaskBoard.tsx` vs `taskBoard.ts` differ only in case; on a
  case-insensitive file system the default import resolves to the `.ts` file. Local workaround:
  explicit `.tsx` in `frontend/src/pages/Dashboard.tsx:16` (uncommitted change in `upstream/`).
  Not an issue on Linux/CachyOS. See the improvement log.

## Spike 3 — an LLM can plan locally: pass

Through the same session API the browser uses (curl with cookie + CSRF):
- `POST /api/beds/` → bed 21 "Spike-Beet" (10 × 1.2 m) on field "Kohlquartier".
- `POST /api/planting-plans/` with crop Broccoli, bed 21, season 4, planting 2026-08-01, 12 m²
  → plan 66; the app computed harvest 2026-10-10 … 10-24, 60 plants, rotation `ok`.
- Gotcha: a plan needs a season covering its date ("An active season is required…"); the
  demo has 2023–2026 only, so planning 2027 needs a season created first.
- So locally there is no token wall: anything the UI can do, a script/LLM can do. Both test
  rows are still in the local demo project.

## Spike 2 — library pull: pass

- **Terms of Service** (https://openfarmplanner.org/en/terms, read 2026-11-17): no rule against
  scripts or scraping; §8 forbids only automated misuse such as mass registrations or spam.
  §7: published crop data is CC BY-SA 4.0, may be reproduced, distributed, edited and combined
  with attribution, licence notice and share-alike; §14: public APIs/exports are planned.
- Script [tools/pull_public_library.py](../../../tools/pull_public_library.py) (stdlib only): logs in
  with email/password or a copied `sessionid` cookie, pages through `/api/public-crops/`
  (100/page, 1 s pause), writes a JSON snapshot with source, date, licence and attribution.
- Against the local instance: 30/30 entries, 85 fields each → `throwaway/local_test_snapshot.json`.
- Against openfarmplanner.org with a temporary account of the user: **158 entries**, 2 pages,
  all `published` → `data/public_crops_snapshot_2026-11-17.json` (since replaced by the full snapshot below)
  (1.9 MB, UTF-8). 66 species, 14 families, 92 entries with a variety.
  Field fill: growth and harvest duration 158/158, spacing 157, expected yield 141, description
  158, propagation duration 102, nutrient demand 68, seed rate 57; germination data and
  pests/diseases 0 — so planning timings and spacing are well covered, seed and germination
  data thin.
- **Open, not tested:** importing a snapshot into another instance's library. Entries refer to
  `crop_species` by id, which differs per instance → map by botanical/canonical name. The
  import has to write `PublicCrop` rows (Django shell/management command), because the API
  only creates public crops by publishing a project crop.

## Full library pull and import — 2026-11-17: pass

- Second pull, new temporary password, all global library endpoints:
  [data/public_library_snapshot_2026-11-17.json](data/public_library_snapshot_2026-11-17.json) —
  158 library crops, **316 species** (local bootstrap: 188), 16 plant families, plant-health
  entries and hosts 0 (empty on the hosted site too).
- Command `import_public_library_snapshot` on branch `feat/library-snapshot-import` of
  `upstream/`, commit `bf2dd523` (local only, not pushed). Test
  `backend/farm/tests/test_import_public_library_snapshot.py`: 2 passed; ruff clean.
- Dry run: species matched 186, created 130, 0 ambiguous, 0 without a German name; crops created
  158, 0 skipped, 0 unknown families. Real run: same numbers; second run: 158 updated, 0 new.
- Local API afterwards: 318 species, 188 library entries (158 imported + 30 demo rows; the
  demo rows belong to the demo project and are left alone, so some crops show twice).
- Upstream's `CLAUDE.md` says species names are maintained only through the crop-species API;
  the command writes them through the ORM. Fine for our instance; has to be raised if offered
  upstream.
