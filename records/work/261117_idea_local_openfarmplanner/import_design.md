# Design — importing a library snapshot into a local instance

State 2026-11-17, upstream `87e3f847`. **V** = verified, **A** = assumption.

## What we have

- **V** Snapshot (first, crops-only; now `data/public_library_snapshot_2026-11-17.json`): 158 entries in the shape of the
  API payload, not of the model. Differences that need mapping:
  - spacing and depth in cm in the payload (`row_spacing_cm`, `distance_within_row_cm`,
    `sowing_depth_cm`) → `*_m` fields in the model;
  - `crop_family` is a botanical name (92 entries have none: varieties inherit from the species);
  - `crop_species` is an id of the hosted instance → useless locally; the payload also carries
    `crop_species_canonical_name`, `crop_species_translations`, `crop_species_search_names`;
  - seed rates are flattened (`seed_rate_direct_*`, `seed_rate_pre_cultivation_*`) → model
    `seed_rate_by_cultivation`;
  - `translations` (158 non-empty) → `PublicCropTranslation` rows;
  - computed or display-only keys (`display_name`, `imported_crops_count`, …) are dropped.
- **V** Local taxonomy: 188 species from the frozen bootstrap. **14 of the 66 species in the
  snapshot are missing locally** (e.g. Cherry tomato, Ginger, Turmeric, Kopfsalat,
  Schlangengurke): the hosted taxonomy has grown since, and its API is the only place it is
  maintained.
- **V** Upstream already writes library rows directly with the ORM in
  `farm/services/demo_project.py::populate_public_demo_library_from_project` — the same
  approach an import would take.

## Options

### A — Management command in the code repo (recommended)

`python manage.py import_public_library_snapshot <file> [--dry-run]` on a feature branch of
our code repo, using the ORM.

1. Species: match by canonical name, then by translated common name/search names; create the
   missing ones as published `CropSpecies` with their translations.
2. Families: look up by botanical name; none → leave empty (as in the source).
3. Library rows: create or update `PublicCrop` (`status=published`), keyed by
   species + name + variety, so running it again updates instead of duplicating.
4. Attribution: the source URL, the snapshot date and the licence go in a record of the import
   (**A** model field or notes field to be chosen while building; no migration if avoidable).
5. `--dry-run` prints what would be created, updated or skipped, and why.

- + The local library works as on the hosted site: import into any project from the UI, more
  than one project, the app's own update comparison.
- + Same code on Windows, CachyOS and the NAS; pairs with upstream's planned export
  ("downloads/exports" in their docs) → a good upstream PR candidate.
- − Code in the code repo to keep in step with upstream's model (85 fields, still changing).

### B — Script in the workspace, via the local API

A script in this repo posts each entry as a **project crop** (`POST /api/crops/`, allowed for
project tokens) into one chosen project.

- + No change to the code repo at all; uses the validated, supported import path.
- − No local library: crops land in one project, not linked to library entries, so no update
  tracking and no reuse across projects.
- − Missing species stay missing (the token can't create species), so 14 species' crops come in
  without a species link.

## Recommendation and riskiest part

**A.** The riskiest part is species matching, not the row mapping: a wrong match quietly files
a crop under the wrong species. Cheapest test: the dry run on this snapshot must report exactly
14 species to create and 0 ambiguous matches before anything is written.

Next improvement to the pull: also fetch `/api/crop-species/` into the snapshot, so new
species come with their full translations instead of the subset in each entry. **A** that
session reads are allowed there (docs say visibility "same as a session request") — not
tested, needs a login.

## Outcome

Built as option A; results in [test_results.md](test_results.md#full-library-pull-and-import--2026-11-17-pass).
