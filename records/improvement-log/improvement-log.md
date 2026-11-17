# Improvement log — OpenFarmPlanner

Issues, risks, ideas, lessons learned and loose notes, one row each. Nobody is on the hook:
the moment something gets an owner and a target it belongs in the open points list instead.
**A rough entry now beats a perfect entry never** — a date and one sentence is enough.

| Date | Entry | Type | Status | Update |
|------|-------|------|--------|--------|
| 2026-11-17 | Upstream dashboard crashes on Windows ("page could not be restored"): `TaskBoard.tsx` and `taskBoard.ts` differ only in case, so `import ... /TaskBoard` resolves to the `.ts` file on case-insensitive file systems. Works on Linux. | issue | in-progress | 2026-11-17 local workaround in `upstream/`: explicit `.tsx` in `src/pages/Dashboard.tsx:16`. Proper fix (rename `taskBoard.ts`) is a candidate first upstream PR. Also `useAutoSizeSidebarWidth.test.ts`/`.tsx` collide (tests only). |

## Columns

| Column | What goes in it |
|--------|-----------------|
| `Date` | the day the entry was written |
| `Entry` | what happened or what the idea is, in one or two sentences someone else understands |
| `Type` | `issue` (happened), `risk` (could happen), `idea` (improvement or loose thought), `lesson-learned` |
| `Status` | `open`, `in-progress`, `resolved`, `parked`, `discarded` |
| `Update` | dated lines (`YYYY-MM-DD`), newest last: what was done or decided |

- **`parked` is not `discarded`.** A parked row says what would bring it back — "back when a
  third sensor size appears" — written so anyone can tell whether it has happened. Without
  that line it is `discarded`.
- **When work starts on a row**, it gets a working folder in `records/work/` if the project
  uses them; the update names the folder. Parked again → the row goes back to `parked`
  with its "back when", and so does the folder.
- **An entry that outgrows its row** gets its own note in this folder,
  `YYYY-MM-DD_short-slug.md`, free form, no type or status (the row holds those). The row
  stays filled and names the note. Pictures go next to it.
- Review the open and in-progress rows whenever the project reviews its state; a problem
  that repeats is a process problem, not another quick fix.

## Example

Not rows of this list — shown as text so they are never read as data:

```
| Date | Entry | Type | Status | Update |
|------|-------|------|--------|--------|
| 2026-09-15 | Torque spec read two ways by the supplier and by us | issue | resolved | 2026-09-17 requirement reworded, REQ-04 -> REQ-06 |
| 2026-09-18 | One fixture for both sensor sizes would save a setup per build | idea | parked | 2026-09-18 back when a third sensor size appears |
| 2026-09-21 | Bracket printed in PETG instead of PA12, see `2026-09-21_bracket-printed-in-petg.md` | issue | open | 2026-09-21 note opened with photos |
```
