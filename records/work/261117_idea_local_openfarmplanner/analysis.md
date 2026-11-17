# Analysis — running OpenFarmPlanner locally

State of 2026-11-17. Upstream repo read at commit `87e3f84` (2026-11-17), shallow clone.
**V** = verified (read in source/docs, or ran), **A** = assumption / inferred.

## 1. What the software is

- **V** AGPL-3.0, source at https://github.com/OpenFarmPlanner/openfarmplanner. Exception: the
  logo is © Martin Stipsitz, all rights reserved; a fork must replace it (`TRADEMARKS.md`).
- **V** Stack: Django 5.2 + DRF backend (Python 3.12+, PDM), React 19 + TypeScript + Vite +
  MUI frontend (Node 22+, npm 10+). SQLite by default, PostgreSQL via env. Django Channels +
  daphne for realtime; Redis only needed for multi-process deployments.
- **V** Local dev setup is documented in the README: `pdm install && pdm run migrate && pdm run
  runserver` (`:8000`) plus `npm install && npm run dev` (`:5173`). LAN script for phones.
- **V** No Dockerfile or DevContainer in the repo. Deployment lives in a separate `ops` repo
  that is **not public** (clone returns "not found"). Production runs on Uberspace behind
  Cloudflare (from `.env.example` comments).
- **V** Very active: changelog, CI, security reviews, and the repo is itself developed with
  AI agents (`CLAUDE.md`, `.claude/skills/`, Codex workflows). Contributions via PR welcome;
  larger changes → issue first (`CONTRIBUTING.md`).
- **V** A demo project (30 crops, 65 planting plans) can be seeded locally with
  `seed_demo_project` (`docs/demo-project.md`).

## 2. The community crop library (riskiest assumption)

- **V Legally pullable.** Contributions are licensed **CC BY-SA 4.0**; the docs state the data
  is "intended to be reusable through the app, future public APIs, future downloads/exports,
  and external open-source or commercial projects" (`docs/crop-library-architecture.md`).
  Obligation: keep attribution and share-alike when redistributing.
- **V No bulk export yet.** Downloads/exports are named as *future*.
- **V Technically only with a login.** `GET /api/public-crops/` returns 403 anonymously
  (tested). The viewset requires `IsAuthenticated`; project API tokens may only *update*
  public crops, not list them (`farm/crops/views/public.py`, `api_token_actions =
  {'update','partial_update'}`). So reading the library from a script needs a **browser
  session** (login + CSRF cookie), paginated at 100 per page.
- **V** Inside the hosted app, a project imports library crops and can pull later updates
  (link via `source_public_crop`). A local instance has its **own empty library**; the
  bootstrap file `backend/crops/migrations/data/species_bootstrap_v1.json` holds only the
  species taxonomy (44 KB), not the cultivation data.
- **A** Library size is unknown (needs a login to see). Scraping it with a session is
  allowed by the licence; whether the Terms of Service limit automated session use was **not
  checked** — read `/en/terms` (or ask the maintainer) before scripting it.

## 3. Working with an LLM

- **V** Hosted: a `ProjectApiToken` (`ofp_pat_…`, read/write/delete scopes, one project) is
  meant for agents. Rate limits: 2000 reads/h, 300 writes/h (600/h for a declared agent).
  The API docs are at `/api/docs/`.
- **V Important limit:** with a token, **only crops** can be created/changed. Suppliers,
  locations, fields, beds, **planting plans** and tasks are **read-only** ("Known limitations"
  in `docs/agent-api.md`). An LLM on the hosted site can fill in crop data but **cannot lay
  out the plan** (when/where) — that stays manual in the browser.
- **A** Locally there is no such wall: the LLM can use a Django shell or management commands,
  or the allowlist can be widened (a "deliberate one-line change" per endpoint, as the docs
  say). That is also the natural first upstream contribution.

## 4. Where to run it

- **V** On this PC: Python 3.13, Node 22.18, npm 11.5, uv are installed; **PDM is not**
  (`uv tool install pdm` would do); Docker is not installed. The dev servers are Linux-first
  (`scripts/*.sh`) but plain Django/Vite run on Windows. **A** some shell scripts need Git Bash.
- **A** Synology NAS: needs a container (Container Manager). With no upstream Dockerfile, we
  would write our own (Django + built frontend + SQLite volume). Doable, but only worth it once
  the setup is used every day and from several devices.
