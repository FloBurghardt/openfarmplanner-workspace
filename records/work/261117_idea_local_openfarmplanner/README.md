---
type: idea
status: active
weight: standard
started: 2026-11-17
closed:
branch:
base_commit: none
merged_commit:
superseded_by:
decisions: [0001, 0002, 0003, 0004]
---

# Run OpenFarmPlanner locally

Find out what it takes to run OpenFarmPlanner (https://openfarmplanner.org/en) locally, on a PC for development or on a Synology NAS. The goal is a planner the user and an LLM fill with data together (crops, where and when, cultivation), extended with missing features since it is open source. Key question: can the community crop data be pulled for local use, or is the hosted version with its API limits the better route?

## History
- 2026-11-17 — started; riskiest assumption is that community crop data may leave the hosted site, checked first.
- 2026-11-17 — analysis and options written; decisions 0001 and 0002 proposed; waiting for the user's go-ahead on the three spike tests in options.md.
- 2026-11-17 — user approved; 0001 accepted. Spikes 1 and 3 pass, spike 2 passes against the local instance and the ToS allow it; hosted run waits for the user's account. Results: test_results.md.
- 2026-11-17 — spike 2 done against the hosted site: 158 entries in data/; 0002 accepted.
- 2026-11-17 — repo layout settled with the user (code / workspace / farm data separate); import designed, 0003 proposed.
- 2026-11-17 — full library pulled (316 species) and imported locally with the new command; pull script moved to tools/.
- 2026-11-17 — SQLite path configurable, Windows bug fixed properly, branch `local` runs; farm data moved to ../OpenFarmPlanner_data/.
