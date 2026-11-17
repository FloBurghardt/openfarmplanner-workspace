# Requirements — OpenFarmPlanner

What the result must do, one row each. Nothing is left out: a requirement nobody has decided
yet gets a row with status `open`.

| ID | Requirement | Source | Status | Verified by | Comment |
|----|-------------|--------|--------|-------------|---------|
| REQ-01 | | | open | | |

## Columns

| Column | What goes in it |
|--------|-----------------|
| `ID` | `REQ-01`, counted up, never reused |
| `Requirement` | what is binding **for us**, written so it can be tested |
| `Source` | where it comes from: specification, standard, the mail or note that records an agreement. Agreed in person or in chat: the initials of whoever stated it and the date, `JS 2026-10-02`; initials unknown → ask, never copy another row's |
| `Status` | one of the five below, nothing else |
| `Verified by` | the record that shows it is met — test record, test name, review note — and its section. Empty until verified; a failed test does not verify |
| `Comment` | what the others don't carry: a deviation, a successor, a reason, what is missing |

| Status | Meaning |
|--------|---------|
| `open` | not agreed yet: our assumption, a text not yet accepted, a value nobody knows; the comment says what is missing |
| `agreed` | confirmed by whoever decides (customer, management, the user); binding, pass or fail |
| `target` | agreed to be measured and reported, but not binding; never blocks |
| `changed` | superseded; the comment begins with the successor, `-> REQ-06` |
| `dropped` | no longer applies; the comment says why |

- `open` rows may be rewritten freely. On an `agreed` or `target` row the Requirement and
  Source never change and the row is never deleted; it ends as `changed` or `dropped`. The
  successor row's Source names what caused the change: the decision record, the mail.
- A specification may be cited as one row instead of being copied; the row names its
  revision and date, and names any rows that deviate from it.
- Every document a Source cites lives in `sources/`, named so the row finds it:
  `CD-44_rev3_2026-08-20.pdf`. **`sources/` is append-only**: a new revision is a new file,
  nothing is overwritten, renamed or deleted.

## Example

Not rows of this list — shown as text so they are never read as data:

```
| ID | Requirement | Source | Status | Verified by | Comment |
|----|-------------|--------|--------|-------------|---------|
| REQ-03 | Connector withstands 60 N pull-out | CD-44 rev3 2026-08-20 | agreed | 2026-09-10_bench-test, pull-out | |
| REQ-04 | Connector withstands 40 N pull-out | CD-44 rev2 2026-06-11 | changed | | `-> REQ-06`. Raised to 60 N with the larger harness |
| REQ-07 | CLI returns exit code 2 on invalid input | FB 2026-10-02 | agreed | `tests/test_cli.py::test_bad_input` | |
```
