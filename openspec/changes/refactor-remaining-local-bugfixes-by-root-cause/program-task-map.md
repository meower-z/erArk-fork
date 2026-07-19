# Remaining Local Fix Program

## What this document is

This is the short, current map for the remaining local-fix program. It replaces the old umbrella task list as the place to answer three questions:

1. Which player problem is actually proven?
2. What is the next small reviewable change?
3. Does work need a gameplay choice before an upstream PR?

The detailed investigation history remains in the owning OpenSpec changes. A green mod test or a polished README is not enough to promote a local patch into this queue.

## Current upstream boundary (2026-07-15)

- PR #212 is **OPEN** at head `77eb7616c` and owns signed pain routing and direct positive-pain effects. The final reviewer-response commit removes the duplicated continuous-instruction adjustment and its now-unused parameter without changing the helper or direct-writer behavior. On 2026-07-15 the user marked it **no action for now**: treat OPEN as passive external state and do not poll, revise, push, reply, publish, or clean up unless explicitly requested. The authoritative record is `pr-212-session-closure-20260715.md`.
- PR #213 is **OPEN** at head `e1a9378`. Its remote code does not clear `pain_as_pleasure`, so the current GitHub behavior still preserves the flag through both sleep and direct hypnosis cancellation.
- The locally selected target for #213 is different and has **not** been sent outward: the user chose to clear `pain_as_pleasure` on both paths. `clear-pain-as-pleasure-on-hypnosis-cancel` owns the accepted one-line change in shared `clear_hypnosis_sub_states()`. Thirteen checks, `py_compile`, real Tk A/B, and final evidence review pass, but the worktree change is uncommitted; it has not been pushed, used to edit #213, or accompanied by published images. Revising #213 still needs separate outward authorization.
- PR #214 is **MERGED** as of `2026-07-14T10:32:51Z` and is present in `upstream/master@abebf33`. Stop all movement-talk implementation work. Only local overlay/mod/worktree reconciliation and separately authorized cleanup remain.
- PR #215 is **OPEN** (not draft, unmerged, no reviews/comments): https://github.com/Godofcong-1/erArk/pull/215, head `364ac6d9f`, 1 commit / 1 file (`Behavior_Effect.csv`, `plural_orgasm_2` through `plural_orgasm_11` +997 each). PR API base is `abebf33b`; live master is `3a1c9e620`. The CSV blob is identical across the candidate parent, post-#214 base, and current master, and merge-tree against current master is clean. Its implementation and submission are complete, and the player confirmed its semantics and retention on 2026-07-14. OPEN is a passive external state, not a queue item: do not select, poll, reverify, or modify #215 unless the user explicitly requests a new bounded action.
- PRs #204-207 and #210-211 are merged.
- PR #220 is **CLOSED unmerged** — the upstream maintainer rejected it (closed `2026-07-16T03:03:47Z`): https://github.com/Godofcong-1/erArk/pull/220. It submitted the T5 `fix-elapsed-time-line-ownership` fix (`codex/fix-elapsed-time-line-ownership`, one elapsed-time line per player click). The maintainer's closing comment treats the per-character `X分钟过去了` line as an **intentional, long-standing feature** (players wanted each character's per-action duration) and will only revise its wording, so the one-line-per-click premise is not an accepted bug. The user decided not to pursue this fix, so T5 is **withdrawn**: preserve its diagnosis, display-only candidate, and local evidence as history; do not continue, re-file, or re-verify it unless the user explicitly reopens it.

Do not reimplement or proactively act on #212 or #214 locally. Do not describe the locally selected #213 correction as live on GitHub until it is actually sent outward.

## Ready local candidates

| Task | Player-visible proof | Local state | Remaining gate |
| --- | --- | --- | --- |
| T1 Discovery reaction settlement | Matched Tk A/B: a successful dismissal skips Closure's existing departure, `气力 -15`, and five-minute settlement on baseline; the candidate shows them once before the interrupted H action resumes. | Four-file candidate `5d360f71e`, focused tests, code/evidence review, Fable evidence review, and Fable PR-text review all pass. | Technical work is complete. Evidence publication, push, and PR creation each remain separately authorized outward actions. No gameplay choice is needed. |
| T2 One edge decision per ordinary settlement | Reviewed real Tk A/B and focused candidate prove one multi-part settlement is collected, judged once, and applied once. | One-file candidate `579b7c475`; 11 submitted tests and 11 near-real/local checks pass, the artifact audit is `PASS`, and publication state is `local-review-ready`. The test mod remains enabled for passive local coverage. | The 2026-07-14 Fable document-reconciliation ruling cancels the fixed several-day playtest gate. Passive play is optional clue gathering and reopens the task only if it finds a new problem. Before PR creation, the user gives final semantic confirmation, the candidate is refreshed and reverified against upstream after #214, and outward authorization is obtained. No outward action has occurred. The earlier choice to play for a few days remains historical context, not the current gate. |
| T3 Compact settlement values | Matched ordinary Tk `看电影` A/B: the same player learn settlement is shown as the impossible `+3M` on baseline and the corrected `+3K` on the candidate; every target exact field and all other text remain identical. | Two-file candidate `cd28b2b21`; 15 focused tests, strict OpenSpec validation, Fable evidence/document/code/PR-text review, and fresh PR-artifact review pass. | Technical work is complete and `local-review-ready`. Evidence publication, push, and PR creation each remain separately authorized outward actions. No gameplay choice is needed. |

These outward gates do not stop local work on later tasks.

## Ordered small-PR queue

### T4 Attribute time-stop release changes to each NPC

- **Why it is a bug candidate:** the existing release loop records NPC release values on the player's root change object instead of that NPC's `TargetChange`. The values in an earlier player screenshot match the existing formula for six deferred body-part orgasms; that screenshot remains historical corroboration only. The proven normal-UI route is a two-NPC route: Lin (4080) accumulates deferred counts `{0: 1, 21: 2}` and a qualifying 射精位置 through four oral actions, the player switches the current target to Jingzhe (306), then releases time stop. Matched Tk A/B on that route is still pending.
- **Current state:** still in evidence work, not complete. Attempt 3 is formally invalid because its pre-registered viewport prerequisite was wrong. Attempt 4 run 1 proved the normal-UI target switch and reached sample2, but the `[4115]` button on a scrolled-back output page was visible with a dead callback, so run 1 is route/endpoint evidence only. The latest Fable ruling is ROUTE A PASS with a mandatory fresh disposable run 2 (start through sample2, then click the bottom active `[4115]` directly, with no post-switch readable proof loop). Run 2 has not started; the formal matched A/B is not complete.
- **Next work:** run the fresh disposable run 2 endpoint rehearsal; only after it succeeds, capture the matched pristine-baseline versus candidate Tk A/B on the Lin→Jingzhe two-NPC route. The real-loader identity matrix, batch-mod compatibility smoke, applied-value/cap checks, and Web collection checks are already complete.
- **Done when:** root/target ownership, zero/one/multiple/remote NPC cases, actual applied values, Tk output, independent Web collection, and review all pass. The shared settlement-output path feeds both renderer adapters, so the Web check is an inverse collection check rather than separate PR-facing visual evidence.
- **Player decision:** none; ownership follows the character whose values changed.

### T5 Show one elapsed-time line per player click

- **Owner and state:** `fix-elapsed-time-line-ownership`, **withdrawn** — the upstream maintainer rejected PR #220 (CLOSED unmerged, 2026-07-16) and the user chose not to pursue the fix. Preserve as history; do not continue unless the user explicitly reopens it. The lines below record its historical rule and dependency only.
- **Rule:** one player click displays one “minutes passed” line. This is display ownership, not a gameplay-balance choice.
- **Dependency:** it consumes `fix-game-update-depth-restoration`; this first real consumer also supplies that dependency's missing player-visible validation.
- **Player decision:** none.

### T6 Gate orgasm chaining once per player click

- **Owner and state:** `add-per-click-orgasm-chain-gate`, 0/17, ready after T5.
- **Confirmed rule:** the gate is per click, not a physiological cooldown. Passive stimulation, orgasm, and settlement continue normally.
- **Dependency:** it also consumes `fix-game-update-depth-restoration`, but its change surface is larger than T5's.
- **Player decision:** already made for local implementation; any outward action still needs separate authorization.

### T7 Restore temporary talk state after use

- **Why it is a bug candidate:** common-talk rendering temporarily overwrites the player's interaction target without a `finally` restoration; a second path expands a global paper-doll candidate list in place, so repeated rendering changes future selection weights.
- **Next work:** build red tests for normal, exception, and consecutive-NPC calls; restore the target in a scoped `finally`; copy candidate lists before combining them; capture representative Tk evidence.
- **PR boundary:** default to two small PRs. Merge them only if investigation proves both defects violate the same rule and belong to the same lifecycle operation in the same logical owner.
- **Player decision:** none; both changes restore state isolation rather than choose new game behavior.

T5 precedes T6 because it is smaller, affects only display, needs no player choice, and is the fastest real consumer proof for depth restoration. T7 is independent of that dependency and follows them.

## Local-complete or dependency work outside the ordered PR queue

- `fix-game-update-depth-restoration` is 6/6 locally complete at commit `80a711603` on a fork side branch. It is dependency/local maintenance, not a standalone PR; validate it through T5 and T6.
- `clear-pain-as-pleasure-on-hypnosis-cancel` is 10/10 locally complete. It waits for authorization to revise #213; its selected local target is not yet the remote PR behavior.
- `settle-remote-plural-orgasm-silently` is implementation-complete and submitted as upstream PR #215 (OPEN, unreviewed) from candidate `364ac6d9f`. The player confirmed its semantics and retention on 2026-07-14. It is outside the ordered and local-work queues, with no actionable task: do not monitor, rerun evidence, or modify it. On an explicit status request, perform one read-only refresh and stop; every outward action still needs fresh authorization.

## Later evidence-led records, not part of the current T4-T7 order

### Group-sex admission eligibility

- **Why it is a bug candidate:** real-loader BDD shows exhausted or seriously fatigued characters can still be offered or admitted through normal discovery/invitation entry points. Player-visible Tk A/B is still required.
- **Next work:** capture an exhausted-character baseline through a real discovery or invitation route, then put the shared eligibility check at the premise owner instead of copying UI callers.
- **Provisional rule:** exhausted or seriously fatigued characters cannot receive a new invitation or be confirmed as new participants. A character who became fatigued after being invited remains visible only so the player can cancel that invitation; the character cannot be confirmed into the activity.
- **Done when:** Tk A/B, one shared predicate, inverse cases, and review pass.
- **Player decision:** confirm the provisional rule before an upstream PR, not before local evidence and implementation.

### Split hypnosis state-loss problems by mechanism

- **Why it may be a bug:** a default type or exact sanity exhaustion may erase an existing hypnosis unconscious state, and the common talk gate may treat hypnosis unconsciousness as ordinary sleep and suppress its dialogue.
- **Next work:** first make faithful red tests and one Tk route for each mechanism. Do not implement the mode-switch-immediacy claim until its own normal route fails.
- **PR boundary:** state erasure and talk-gate selection are separate changes. Implement only a mechanism whose red evidence succeeds.
- **Done when:** a normal route proves the loss, the narrow owner-level fix passes inverse cases, Tk evidence and review pass.
- **Player decision:** none for preventing state erasure; confirm any change to dialogue-selection policy before that PR.

### Isolate Tk skip leakage into the next wait

- **Why it may be a bug:** mod-on Tk evidence shows a chat wait after cross-area movement stays put for eight seconds and advances only on a fresh click, but no matched mod-off baseline proves the upstream failure yet.
- **Next work:** capture the missing mod-off A/B. If the old skip really advances the later wait, extract only that ownership fix from `local_settlement_input_fix` and remove its dependency on the 30 ms input-age patch.
- **Done when:** mod-off failure is reproduced, a narrow fix passes, and matched Tk evidence plus review pass. If the baseline does not fail, freeze the task.
- **Player decision:** none for one prompt consuming only its own input.

## Local maintenance, not new PR work

- Treat sleep and direct hypnosis cancellation clearing `pain_as_pleasure` as the selected local target. The one-line core fix belongs only to `clear-pain-as-pleasure-on-hypnosis-cancel`.
- The disabled pain mod's cancel-clear wrapper points in the same semantic direction. Do not delete it as wrong; after the core fix is locally integrated, retire it as replaced and verify that composition does not double-clear or otherwise change behavior. The BDD expectation is “cancellation clears”.
- Keep `activate-granted-pain-as-pleasure` limited to local composition and mod-retirement checks. It does not own the one-line core fix. PR #212 still owns signed routing and direct positive-pain effects.
- Keep the T2 test mod enabled until its candidate is upstreamed or rejected; passive play may provide new clues but is not a gate.

## Frozen or retained work

| Area | Disposition | Reopen condition |
| --- | --- | --- |
| Group masturbation intent | Freeze. The current global active set and action-window identity are not an upstream boundary. | A deterministic normal trace shows the same intent consumed twice or leaking into the next player action, followed by an explicit duration/retry rule. |
| Group edge release and the rest of the large orgasm batch | Freeze and do not upstream the package. | Re-derive owners after T2 lands; reproduce one exit dropping a nonzero pending edge before choosing exit visibility or discard semantics. |
| Tk queue scrolling | Retain only as an experience/performance candidate. Freeze the 30 ms input-age guess and whole-queue drains. | Player-representative evidence for the batch-scroll change, kept separate from input correctness. |
| H movement interruption | Withdraw to investigation history. | A normal production route demonstrates stale movement continuing after H/group entry. |
| Private font registration | Freeze. | Clean Windows development and packaged-build evidence proves fallback and verifies the actual registered family. |
| Psychological-pleasure curve | Keep as balance-feature backlog. | Measure the current range and obtain a separately reviewed curve contract. |
| `group_sex_extension` | Keep as an independent feature. | Adapt only after shared participant and orgasm owners exist; do not merge its commands into bugfix PRs. |
| `easy_mode` / `semen_boost` | Keep feature / disabled example; no bugfix task. | Explicit feature work. |

## Documentation migration

1. The discovery owner is now `fix-discovered-reaction-settlement`; every existing supervision prompt and verdict stays verbatim, and the broader experiments remain clearly rejected history.
2. `fix-group-sex-admission-eligibility` remains a later evidence-led owner rather than putting admission semantics back into the discovery change.
3. `fix-compact-value-formatting` and `fix-time-stop-release-attribution` now separate the former mixed time-stop change into T3 and T4.
4. Keep the #213 one-line correction in `clear-pain-as-pleasure-on-hypnosis-cancel`; narrow `activate-granted-pain-as-pleasure` to local composition and replaced-mod retirement, then archive it when those checks finish.
5. Keep `fix-game-update-depth-restoration` as a T5/T6 dependency rather than a standalone PR.
6. `add-per-click-orgasm-chain-gate` owns T6; `fix-elapsed-time-line-ownership` (T5) is withdrawn after the upstream maintainer rejected PR #220 (CLOSED unmerged, 2026-07-16). `fix-talk-common-state-leaks` is T7's investigation owner and must split its two defects into separate PR owners unless the merge condition above is proven.
7. The umbrella `tasks.md` is now an index of these owners and frozen records; its original checklist remains in `legacy-tasks.md`. Detailed implementation tasks belong only in each small change.

## Stop rule

There is no player-input stop for the local queue. T2 needs final semantic confirmation before its upstream PR. `settle-remote-plural-orgasm-silently` is not part of that queue: its implementation and submission as PR #215 are complete, its earlier confirmation gap is resolved, and OPEN is only a passive external state. Do not select or monitor #215 when advancing this map. If the user explicitly requests its current status, perform one read-only refresh, report it, and stop. Later admission or dialogue-policy work keeps its own named confirmation gate. T6's per-click rule is already confirmed. Missing outward authorization pauses only that outward action, not local evidence or reversible implementation elsewhere in the queue.
