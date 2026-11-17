# Open points — OpenFarmPlanner

What has to be settled before the project can go on, one row each, every row with an owner
and a target. Something worth doing differently with nobody on the hook goes in the
improvement log instead.

| ID | Point | Owner | Target | Status | Update |
|----|-------|-------|--------|--------|--------|
| OP-01 | Where the instance runs for good: local PC only, all-inkl webspace or Synology NAS (old DSM; SSH there is admin-only) | FB | once it runs on the new PC as wanted | open | 2026-11-17 raised; hosted use needs a real deployment (HTTPS, no DEBUG), not the dev setup |
| OP-02 | Regular backups of the farm data folder to the SMB share (`tools/backup_data.py`), automated on the new PC | FB | before the first real farm data is entered | open | 2026-11-17 raised; script exists and was tested against a local folder |

## Columns

| Column | What goes in it |
|--------|-----------------|
| `ID` | `OP-01`, counted up, never reused |
| `Point` | what has to be settled, in one sentence someone else understands |
| `Owner` | initials of the person who answers for it; never a role or a department |
| `Target` | a date, **or** the event that makes it due |
| `Status` | `open` or `done` |
| `Update` | dated lines, newest last. The first is the day it was raised; every moved target or owner says why |

- **Target is never empty.** "before the first customer sample ships" is a target; "when we
  get to it" is not.
- Walk the whole list at every review, not only today's rows — an event target only works if
  someone checks whether the event happened.
- A point that outgrows its row gets a note in this folder named after it,
  `OP-03-connector-pull-out.md`; the row stays filled and names it.

## Example

Not rows of this list — shown as text so they are never read as data:

```
| ID | Point | Owner | Target | Status | Update |
|----|-------|-------|--------|--------|--------|
| OP-01 | Thread pulls out of the printed bracket at 4 Nm | MJ | 2026-09-30 | open | 2026-09-18 raised; trying a heat-set insert |
| OP-02 | Firmware reports the wrong part number | JS | before the next build | done | 2026-09-18 raised. 2026-09-25 fixed in firmware 1.3 |
```
