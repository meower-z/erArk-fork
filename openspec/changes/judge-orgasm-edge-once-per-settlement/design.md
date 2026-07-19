## Context

`orgasm_judge()` produces per-part normal, extra, and uncounted inputs, then calls `orgasm_settle()`. Core `orgasm_settle()` currently updates one part, rolls edge success, and commits that part before moving to the next. A later failure writes internal state `3`; the caller changes it to release state `2` and calls settlement again with inputs that were already partly consumed.

The violated game rule is: one eligible ordinary orgasm-detection checkpoint for one character is one edge-decision batch, so all eligible parts detected at that checkpoint must share one decision made before any part is committed. In core, that checkpoint maps to one synchronous `orgasm_judge()` → `orgasm_settle()` call, not to one player click, one H instruction, or an entire group-sex round.

The logical owner is `orgasm_settle()`. It alone sees the complete invocation input and owns both held and ordinary application. `orgasm_judge()` owns input production, while `judge_orgasm_edge_success()` owns probability and its player-visible message.

## Goals / Non-Goals

**Goals:**

- Enforce a collect → decide once → apply once flow within one core settlement invocation.
- Base the decision on the complete prior held ledger plus every supported current `normal + un_count` contribution.
- Keep live `orgasm_edge_count` limited to committed successful holds.
- Remove partial commit followed by caller replay.
- Preserve existing level rules, ordinary effects, behavior-ID batching, time-stop, non-edge, and explicit-release paths.
- Keep the production diff in one file and small enough to review directly.

**Non-Goals:**

- Combining separate settlement invocations into one player-action or group-sex window.
- Upstreaming display batching, scheduler hooks, fatigue deferral, representative talk, or other `local_h_orgasm_batch_fix` responsibilities.
- Making all downstream effect application transactional under arbitrary exceptions.
- Repairing synthetic or corrupted input keys that the existing supported-part loop does not process.
- Publishing evidence, pushing a branch, or creating or editing a PR.

## Decisions

### 1. Collect the batch before applying any part

Before the existing application loop, iterate the same supported `part_dict` domain and part-`3` skip used by ordinary settlement. Build a local candidate count snapshot from a copy of the committed `orgasm_edge_count`, adding each current supported part's existing `normal + un_count` count. `extra` remains metadata because production mirrors its count through `normal`.

Capture the character-wide time-stop and active-edge route once for a work-bearing invocation. No part level, held count, or behavior is changed during collection.

### 2. Give the judge an explicit read-only decision input

Extend `judge_orgasm_edge_success()` with one optional count-mapping parameter. Only `None` means “read live `orgasm_edge_count` as today”; an explicitly supplied empty mapping is a valid decision input and must not fall back to live state. When a mapping is supplied by core settlement, the judge calculates the same square-sum probability from that mapping and draws the same result message.

This keeps the judge responsible for probability while making its input explicit. The local candidate snapshot is never installed into character state, so judgment or draw exceptions naturally leave the committed ledger untouched and require no restoration protocol.

All in-repository production callers were traced. Core settlement is the only caller that needs the new argument. The local batch mod that was enabled during design, and the deprecated replacement, call the judge with one argument and therefore retain their existing live-ledger behavior. No in-repository mod replaces the judge itself. A third-party replacement with a strict one-argument signature while retaining new core settlement would need adaptation; no such production example is evidenced here.

### 3. Apply exactly one captured branch

On shared success, use the existing per-part loop to update each current level once, add that part's `normal + un_count` count to the committed ledger, and queue its existing `{part}_orgasm_edge` behavior. No ordinary release behavior is queued.

On shared failure, copy the current uncounted input, merge supported prior held counts into that copy, clear the committed ledger, and set the existing release state `2` before entering the ordinary application path. Current normal/extra inputs stay in their original channels, so current levels advance once while prior held counts do not advance levels again. The failing invocation queues no part-specific edge behavior.

Every supported count enters the existing ordinary `climax_count`/degree-selection flow once without caller replay. Existing behavior IDs remain binary flags, so repeated selections of one ID retain existing batching rather than promising repeated downstream effects.

Remove both ends of the obsolete state-`3` handshake: new settlement never writes it, and `orgasm_judge()` no longer retries the call.

### 4. Keep the boundary and inverse paths unchanged

No pending decision survives the function call. Two settlement invocations for the same character decide independently. Non-edge settlement does not call the edge judge. Time-stop accumulation wins over active edging as before. Explicit release in state `2` continues supplying the live held ledger as uncounted input, and its caller retains cleanup ownership.

The operation identity is the dynamic synchronous settlement call. The candidate snapshot and result remain local and are not serialized because the traced judge/draw path only emits output and cannot synchronously re-enter settlement. Same-character overlapping command execution is not an evidenced core path; if it becomes reachable through concurrent Web dispatch, serialization belongs at that command/settlement owner rather than in a local edge flag or lock.

At design time, the enabled local batch mod replaced core `orgasm_settle()` and owned its broader window-end decision. As of 2026-07-13, local development `main` disables that mod and its dependent group-release mod, and enables `local_orgasm_settle_edge_fix` to mirror this candidate's settlement-scoped behavior for player testing. That test mod is local validation infrastructure, not an upstream capability or PR claim.

### 5. Be honest about exceptions

The decision phase does not mutate live settlement state. If the judge or its draw raises, the exception propagates and the held ledger remains untouched.

Application is not a transaction. On successful hold, an exception may leave already visited parts committed while later parts remain unapplied. On failed release, invalidate the held ledger before ordinary effects so the same release is not automatically replayed; already completed effects may remain and later effects may be lost. A recoverable transaction would require a much broader redesign of caller-owned input tokens and downstream effects.

## Alternatives Rejected

- **Roll on the first crossing and reuse it:** small, but later parts do not contribute to difficulty.
- **Temporarily preload the live ledger and restore it in `finally`:** functionally possible, but it makes provisional counts observable as committed state and creates avoidable alias, identity, and rollback obligations.
- **Move the decision into `orgasm_judge()`:** wrong owner and would run before the enabled mod's replacement settlement policy.
- **Pass only a precomputed scalar difficulty:** duplicates part-merge/probability knowledge outside the judge and hides the effective count distribution.
- **Introduce plan/result objects or a general transaction:** clearer in isolation but disproportionate to this one-file rule and still cannot roll back downstream effects.
- **Keep the existing candidate's work-dictionary state machine:** expressive but much larger than the required collect/decide/apply change.

## Review Budget And Risks

The expected production diff is one file and roughly 45–55 touched lines, including the backward-compatible judge parameter and removal of the retry. Stop for renewed design review if implementation needs another production file, persistent cache/window state, a scheduler hook, movement of the ordinary settlement body, or substantially more than about 55 touched production lines.

Submitted regression coverage should stay in one focused file with shared setup and table-driven inverse cases where practical. The expected test diff is at most roughly 250–300 lines. If proving the invariant needs several bespoke files or substantially more test code, stop and simplify the harness or revisit the boundary rather than encoding each reviewer clue as a separate fixture.

Key implementation risks are double-counting paired normal/extra input, merging provisional current counts into the failure release a second time, accidentally including unsupported keys, re-evaluating routing per part, or letting local replacement mods mask core verification. Focused tests and final diff review must target those risks without promoting them into new player-facing rules.

## Current PR Readiness

The candidate code, submitted tests, deterministic Tk evidence, Fable-written Chinese PR text, code-quality audit, and fresh artifact audit are complete. The durable record is [pr-readiness.md](pr-readiness.md), with the inspected evidence copied under [evidence/](evidence/).

The candidate is deliberately not being submitted upstream yet. Local development `main` runs the same player-visible rule through `local_orgasm_settle_edge_fix`, while the user plays it for several days. Publication remains gated on the user's later decision; image upload and PR creation or update still require separate authorization.
