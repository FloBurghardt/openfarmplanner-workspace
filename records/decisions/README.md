# Decision records

Why things are the way they are. One decision per file, `NNNN-short-kebab-title.md`, started
from [0000-template.md](0000-template.md). If `reindex.py` is used, the list is
[index.md](index.md) (generated, never hand-edited); otherwise list each record below.

## When one is required

A decision that:

- is expensive or disruptive to reverse
- defines or changes an interface, data or file format, or layout
- selects a tool, library, method, supplier, material or approach
- trades one quality against another (cost vs. time, simplicity vs. flexibility, …)
- rejects an option that was seriously considered — record it under the winner's alternatives
- would make a later reader ask "why on earth is it like this?"

Not for naming, formatting, or choices with only one real option. Too many records kill the habit.

## Rules

- Numbers count up from `0001`, never reused, renumbered or deleted.
- One decision per record. "And also" in the Decision section means two records.
- `proposed` while being worked out; `accepted` when the user agrees.
- **Every record reaches a terminal status.** Dropped before anyone ruled on it → `rejected`,
  with `decided` filled and a `## Why rejected` section of one or two sentences. Never leave
  one `proposed` after the work that produced it has closed.
- **Once accepted, Context and Decision are frozen.** When reality disagrees, append a dated
  line under Consequences. When the decision itself changes, write a new record that
  `supersedes` it and set the old one to `superseded` with `superseded_by`.
- `source` names the working folder or meeting it came from; that folder's README lists it back.
