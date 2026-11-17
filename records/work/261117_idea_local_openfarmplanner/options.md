# Options

Based on [analysis.md](analysis.md). Goal: plan crops (what, when, where, cultivation) together
with an LLM, and be able to add missing features.

## A — Hosted only, LLM through the API token

Use openfarmplanner.org, create a project token, let the LLM read everything and write crops.

- + Nothing to install or run; community library and updates built in; backups not our job.
- + Data you publish flows back to the community directly.
- − Token cannot write beds, planting plans or tasks → the LLM can't do the planning half.
- − Own features only arrive once upstream merges and deploys them.
- − Rate limits (300 writes/h) are fine for planning, not a real obstacle.

## B — Local instance on the PC (dev setup), library pulled in (recommended)

Clone upstream, run backend + frontend locally (SQLite), keep our changes on a fork branch.
Fetch the community library once via a logged-in session script and import it as local crops
(CC BY-SA: keep attribution).

- + The LLM has full access (Django shell / extended token allowlist), so it can also plan.
- + Features can be built and tested right away and offered upstream as PRs (AGPL).
- − Library is a snapshot; refresh means re-running the pull. No live "pull updates".
- − We own backups and upgrades (git pull + migrate).

## C — Local instance on the Synology NAS (container)

Like B, but deployed as a container on the NAS, reachable from phone/tablet in the LAN.

- + Always on, usable in the field, one data set for all devices.
- − No upstream Dockerfile and the ops repo is private → we write and maintain the image.
- − Development still happens on the PC; NAS is a deployment target, not a dev environment.

## Hybrid worth noting

B for development and the LLM-driven planning, plus a hosted account to read (and contribute
to) the library. C becomes a later step once B is used regularly — the same code, packaged.

## Recommendation

**B now, C later, contribute upstream where it makes sense.** The deciding fact is that the
hosted API can't write planting plans, so A fails the core goal. The riskiest remaining
assumptions, with their cheapest tests:

1. *The app runs on Windows with the documented setup* → install PDM, run backend + frontend,
   seed the demo project (≈ 30 min).
2. *The library can be fetched with a session and imported locally* → read the Terms of
   Service, then fetch one page of `/api/public-crops/` with your login and map it onto the
   local crop model (≈ 1 h). Needs your account on openfarmplanner.org.
3. *An LLM can write planting plans locally* → create one bed + one planting plan via the
   Django shell or the API in the local instance.
