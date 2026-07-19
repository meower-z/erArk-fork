## 1. Root-Cause Design Gate

- [x] 1.1 Trace every core and active-mod writer, reader, caller, retry, and cleanup owner for `orgasm_edge` and `orgasm_edge_count`
- [x] 1.2 Name the violated rule as batch-level decision interleaved with per-part mutation, and select `orgasm_settle()` as the collect/decide/apply owner
- [x] 1.3 Compare first-part reuse, temporary live-ledger preload, caller-owned judgment, explicit judge snapshot, and larger plan/result designs; select the backward-compatible explicit snapshot because it keeps provisional counts out of committed state
- [x] 1.4 Give the rewritten proposal, design, formal spec, actual call graph, and local replacement seam to a fresh-context critic; resolve root-cause, semantic, compatibility, and minimality findings before production edits

## 2. Failing-First Core Proof

- [x] 2.1 Add focused judge-input tests proving omitted input reads the live held ledger, a supplied mapping is used directly, and an explicitly supplied empty mapping overrides a nonempty live ledger rather than falling back through truthiness
- [x] 2.2 Add a focused core success case proving several current parts cause one judge call, the supplied candidate snapshot contains prior plus all current counts, the live held ledger still contains only prior committed counts at judge entry, and all parts share success
- [x] 2.3 Add one compound shared-failure case covering prior held counts, overlapping current normal input, production-realistic paired normal/extra input, later-part uncounted input, no queued edge behavior, one ordinary processing pass, existing behavior-ID batching, cleared held ledger, and release state; assert exact per-part level deltas so current normal/extra advance once while prior held and current uncounted-only counts advance zero times
- [x] 2.4 Add a runtime integration case that executes real `orgasm_judge()` through a recording wrapper which delegates to real `orgasm_settle()`; prove a drink-trigger uncounted input and paired normal/extra input are produced once and settlement is called once. Static AST or source call counting does not satisfy this task
- [x] 2.5 Add focused inverse cases for one part, no supported work, non-edge settlement, time-stop accumulation, explicit release, judge exception with naturally untouched live ledger, unsupported current keys, and two consecutive independent settlement invocations
- [x] 2.6 Keep submitted coverage in one focused test file with shared setup and table-driven inverse cases where practical, targeting no more than roughly 250–300 lines; then run it against untouched `upstream/master` and record the exact expected red failures before implementation

## 3. Minimal Core Implementation

- [x] 3.1 Extend `judge_orgasm_edge_success()` with a documented optional count snapshot; preserve existing one-argument behavior and use only the supplied mapping when present
- [x] 3.2 In `orgasm_settle()`, collect supported current work and one candidate count snapshot before per-part mutation, capture routing once, and call the judge once with that snapshot
- [x] 3.3 Apply the captured result through the existing loop: commit all current parts on success, or merge only prior supported held counts into copied uncounted release input on failure; remove the state-`3` writer and caller retry
- [x] 3.4 Re-open the production diff and stop for renewed design review if it touches another production file, adds persistent scheduler/window state, moves the ordinary settlement body, breaks existing one-argument judge callers, or substantially exceeds about 55 touched production lines

## 4. Verification And PR Readiness

- [x] 4.1 Run the focused submitted regression, relevant existing core tests, `py_compile`, and `git diff --check`; separately run existing active local orgasm-batch/group-release tests for private confidence and exclude them from submitted tests and PR-facing proof
- [x] 4.2 Re-open the implementation, submitted tests, and complete upstream diff to confirm the live held ledger never contains provisional counts, one invocation has one decision and one application branch, failure cannot trigger caller replay, and unrelated paths remain unchanged
- [x] 4.3 Complete a deterministic normal Tk A/B route with `local_h_orgasm_batch_fix` and dependent `local_group_edge_release_fix` disabled; align exact revisions, mod configuration, save, route, and seed, then inspect the final 2070x1070 images
  - Completed on 2026-07-13 after the earlier blocked route was superseded. Baseline and candidate used save 99, seed `0`, the same six-wait route, and the same Tk geometry. The baseline shows duplicate results for 清流 and 特蕾西娅; the candidate shows one shared result for each. Durable copies and provenance are under `evidence/`.
- [x] 4.4 Use `fable-5` at medium effort for Chinese PR prose, apply the code-quality audit's comment-precision findings, then pass a fresh `review-erark-pr-artifacts` audit using only the exact proposed diff, submitted tests, and inspected PR-facing evidence
  - The fresh artifact audit returned `PASS` with `publication_state: local-review-ready`; the only remaining draft placeholders are the two image URLs, pending an authorized upload.
- [x] 4.5 Present the final local diff, verification, draft, and images to the user; request separate authorization before publishing evidence, pushing, or creating or editing a PR
  - The user reviewed the ready package and chose to test the behavior locally for several days before deciding whether to submit it upstream.

## 5. Player-Test Gate

- [x] 5.1 Disable `local_h_orgasm_batch_fix` and its dependent `local_group_edge_release_fix`, then enable `local_orgasm_settle_edge_fix` on local development `main` so normal play exercises the candidate rule without applying the upstream core diff to `main`
- [x] 5.2 Preserve the candidate branch and local PR package: commit `579b7c47504038b6523decf71a565029ba76860a` on `pr-fork/codex/fix-edge-settlement-shared-decision`, with the exact proposed diff, tests, evidence, audits, and PR text recorded in this change
- [x] 5.3 Let the user play the enabled test mod for several days and record the decision to accept the current behavior or reopen the candidate
  - Resolved 2026-07-17: the user accepted the behavior; upstream PR #221 was published and refined (`9d18e455f` max(1, n/2) power, `78f360cb0` 0.15 base rate) and remains open awaiting maintainer review.
- [x] 5.4 If the user accepts the behavior, obtain separate authorization to publish the two evidence images, replace the draft placeholders, and create or update the upstream PR; otherwise revise the candidate and refresh evidence and PR text before publication
  - Resolved 2026-07-17: PR #221 was created and updated on the fork branch; the user declared on 2026-07-17 that no further wrap-up work is needed on this change — the only outstanding item is upstream's review decision, which requires no local action.
- [x] 5.5 On 2026-07-16 the maintainer reviewed published PR #221 and objected to the shared-decision difficulty; the author pushed a k-th-power multi-part difficulty refinement (`6de9eb562`) onto the PR branch and replied. Full exchange, implementation, and open threads recorded in [review-response-20260716.md](review-response-20260716.md)
