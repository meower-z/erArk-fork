`BLOCKED` — final-commit Tk before/after evidence is missing, so this package is not local-review-ready. It is acceptable specifically for creating a Draft PR that remains “not ready for review.”

`publication_state: blocked-before-local-review-ready`

Fable provenance:

- The prompt starts with `/investigate-game-bug` and `/review-erark-pr-artifacts`, names the exact base/head, and limits public evidence correctly.
- The proposed title and body match the preserved Fable output byte-for-byte.
- The files do not themselves record CLI flags; the `claude-fable-5`/high attribution therefore relies on the supplied invocation attestation.

Actionable blocker:

- `pr-body-proposed.md:21` correctly says the latest-code Tk comparison is pending. No comparable, inspected base/head images exist in the review package, and none are intended for this PR-creation step. This is allowed for a Draft PR, but the PR must not be marked ready until final-commit evidence is produced and published with separate authorization.

No draft-text revision is required merely to create the Draft.

## Cumulative-prefix ledger

| Boundary | New concept | Prior context sufficient? | Later rescue needed? | Result |
|---|---|---:|---:|---|
| Title:1 | Multi-character settlement repeats the elapsed-time line per panel | Self-contained player-visible problem | No | Pass |
| Body:1 | Problem section | Yes | No | Pass |
| Body:3 | Exact multi-character scene, both displayed messages, group-sex example, and duration mismatch | Title establishes repetition; paragraph defines its visible shape before explaining mismatch | No | Pass |
| Body:5 | Cause section | Yes | No | Pass |
| Body:7 | Per-character ownership in `handle_settle_behavior`, local `add_time`, and relation to the game clock | Problem already establishes the wrong behavior | No | Pass |
| Body:9 | Fix section | Yes | No | Pass |
| Body:11 | Move the announcement to the outer update flow | Cause establishes why ownership must move | No | Pass |
| Body:13 | Remove both per-panel duration messages | Previous prefix identifies the ownership move | No | Pass |
| Body:14 | Outermost depth, entry/exit clock delta, post-settlement timing, and zero/negative/nested behavior | Previous prefix establishes the new owner | No | Pass |
| Body:15 | Tk and Web delivery behavior | Fix scope is already established; identifiers are literal project terms | No | Pass |
| Body:17 | Verification section | Yes | No | Pass |
| Body:19 | Syntax compilation check | Introduces no behavioral scope | No | Pass |
| Body:20 | Diff whitespace check | Introduces no behavioral scope | No | Pass |
| Body:21 | Final-code Tk evidence remains pending | This is an honest limitation, not a rescue for an earlier claim | No | Pass, but evidence gate blocked |

## Visibility ledger

| Item or claim | Classification | Support/result |
|---|---|---|
| Repeated per-panel elapsed-time messages and NPC alternative wording | PR-visible implementation context | Base code computes per-character `add_time` and appends one of the two messages whenever a settlement panel has content |
| Removal of per-character duration announcements | PR-visible implementation context | Exact diff deletes the nine-line append block |
| One outermost positive net-clock announcement after settlement | PR-visible implementation context | Exact diff records entry time, checks `caller_depth == 0`, computes the clock delta after `init_character_behavior()`, and suppresses non-positive deltas |
| Tk output behavior | PR-visible implementation context | Diff emits through `io_init.era_print`; existing panel drawing ultimately uses the same output layer |
| Web history and real-time `instruct` delivery | PR-visible implementation context | Diff appends the single elapsed text to `web_instruct_texts` and calls `emit_realtime_text(..., "instruct")` |
| `python -m py_compile ...` | Reviewer-rerunnable static check using only submitted files | Re-run successfully; not behavioral proof |
| `git diff --check` | Reviewer-rerunnable patch check | Re-run successfully; not behavioral proof |
| Automated tests or benchmarks | None submitted | `local_tests/` is untracked/local-only and is correctly absent from the draft |
| Tk screenshots | Missing required evidence | No final-commit pair supplied or intended for publication now |
| Fable prompt/output | Local-only provenance record | Exact proposed title/body match confirmed; not PR evidence |

Draft-PR verdict: yes, create only as Draft and leave it not ready for review. The skill remains `BLOCKED` until the final base/head Tk comparison is inspected and approved for publication.
