# Umbrella Task Migration

## Purpose

This ledger splits every task in `tasks.md` as needed and assigns each resulting obligation to exactly one durable destination before the oversized umbrella change is rewritten or archived. It changes no game code and does not approve any unresolved gameplay rule.

The five states mean:

- **completed**: keep only as history or an already-established workflow rule;
- **upstream-owned**: the responsibility is tracked by an exact open or merged upstream PR, not this umbrella; an open PR is conditional ownership until merge, and a PR closed unmerged sends its rows to a named `re-file, revise, or withdraw` decision record;
- **current**: move the obligation to the named active owner;
- **deferred**: retain evidence and wait for a named gameplay, platform, or readiness decision;
- **withdrawn**: preserve the diagnosis/candidate as history, but do not continue it unless the user explicitly reopens it.

Migration-only suffixes such as `2.3k.a` split one mixed source task into separately owned obligations. Removing those suffixes still yields the original 160 task IDs exactly. Creating, renaming, splitting, or archiving OpenSpec changes is a later step.

## Current Status Supersessions (2026-07-14)

### PR #214 is merged

PR #214 merged at `2026-07-14T10:32:51Z` and is present in `upstream/master@abebf33`. Every row below that calls #214 open, live, or waiting for merge is preserved as investigation and migration history from its own date; it is not the current status. The current rule is to stop movement-talk implementation and leave only local overlay/mod/worktree reconciliation plus separately authorized cleanup. In the migration table, `upstream-owned` for #214 now means ownership by that exact **merged** PR.

### PR #213 remote state and selected local target differ

PR #213 remains open at `e1a9378`; its remote code preserves `pain_as_pleasure` through sleep and direct hypnosis cancellation. The later, locally selected target is for both paths to clear the flag. The accepted one-line shared-helper correction belongs only to `clear-pain-as-pleasure-on-hypnosis-cancel`; it is locally complete but uncommitted and has not been pushed, used to edit #213, or accompanied by published images. `activate-granted-pain-as-pleasure` owns only local composition and retirement of the same-direction mod wrapper after core integration. Any historical table row that treats remote preservation as the selected local contract, or treats #213 merge alone as sufficient reason to retire that wrapper, is superseded by this paragraph.

### T2 current gate

`judge-orgasm-edge-once-per-settlement@579b7c4` is `local-review-ready`: code, focused and near-real checks, matched Tk A/B, and artifact review pass. The 2026-07-14 Fable document-reconciliation ruling cancels the fixed several-day playtest gate; passive play is optional clue gathering. Before an upstream PR is created, the user must give final semantic confirmation, the candidate must be refreshed and reverified against upstream after #214, and outward authorization must be obtained. The earlier choice to play for a few days remains history rather than the current gate.

### PR #220 rejected — T5 `fix-elapsed-time-line-ownership` withdrawn (2026-07-16)

The upstream maintainer rejected PR #220 (`codex/fix-elapsed-time-line-ownership`, the T5 "one elapsed-time line per player click" fix); it is CLOSED unmerged as of `2026-07-16T03:03:47Z`. The user decided not to pursue this fix. T5 / `fix-elapsed-time-line-ownership` is therefore **withdrawn**: preserve its diagnosis, candidate diff, and local evidence as history, but do not continue, re-file, or re-verify it unless the user explicitly reopens it. Every row or order line below that calls T5 ready, current, or next-in-queue is preserved as history from its own date; it is not the current status. `fix-game-update-depth-restoration` was the shared prerequisite of T5 and T6; with T5 withdrawn, only T6 `add-per-click-orgasm-chain-gate` still consumes it.

Maintainer rationale (closing comment on #220): the per-character `X分钟过去了` line is a **deliberate, long-standing feature** — earlier players asked to see each character's per-action duration, so the prompt was intentionally emitted per settlement panel. The maintainer agreed the wording can mislead and will revise only the text description themselves, while keeping the per-character behavior. The T5 premise (collapse to one elapsed-time line per player click) therefore conflicts with maintainer intent and is **not** an accepted bug; do not re-file it as one. Note this also means the multi-character multi-`X分钟过去了` settlement is the intended design, not a defect — the session's in-progress "multiple simultaneous orgasm" before/after evidence effort for this fix is abandoned with the fix and its `/tmp` runtimes discarded.

## Migration Table

| Original task | State | Destination | Migration note |
| --- | --- | --- | --- |
| `0.1` | completed | umbrella archive | Preserve the ownership exclusions as audit history. |
| `0.2` | completed | umbrella archive | Preserve the read-only audit record. |
| `0.3` | completed | `investigate-game-bug` skill | The durable investigation gates live in the project skill. |
| `0.4` | completed | umbrella archive | Preserve the qualified test baseline; it is not a live implementation task. |
| `0A.1` | completed | umbrella archive | Historical branch setup. |
| `0A.2` | completed | umbrella archive | Historical assumed-upstream overlay record. |
| `0A.3` | completed | umbrella archive | Historical duplicate-responsibility cleanup. |
| `0A.4` | completed | umbrella archive | Historical delegation to corrected core behavior. |
| `0A.5` | completed | umbrella archive | Historical overlay verification. |
| `0A.6` | completed | umbrella archive | Historical rollback and worktree boundary. |
| `0B.1` | completed | umbrella archive | Historical single-main conversion. |
| `0B.2` | completed | umbrella archive | Historical clone and evidence-worktree cleanup. |
| `0B.3` | completed | `investigate-game-bug` skill | Fresh linked-worktree policy is already durable there. |
| `0B.4` | completed | candidate/worktree ledger | Preserve branch creation as history; candidate fate is classified below. |
| `0B.5` | completed | candidate/worktree ledger | Preserve branch creation as history; candidate fate is classified below. |
| `0B.6` | completed | candidate/worktree ledger | Preserve branch creation as history; candidate fate is classified below. |
| `0B.7` | completed | candidate/worktree ledger | Preserve branch creation as history; candidate fate is classified below. |
| `0B.8` | completed | candidate/worktree ledger | Preserve branch creation as history; PR #213 owns the accepted slice. |
| `0B.9` | completed | candidate/worktree ledger | Preserve the discovery worktree provenance. |
| `0B.10` | completed | candidate/worktree ledger | Preserve the withdrawn membership worktree provenance. |
| `0B.11` | completed | candidate/worktree ledger | Preserve the withdrawn registration worktree provenance. |
| `1.1` | upstream-owned | PR #214 movement-talk actor context | The red regression belongs with the open PR. |
| `1.2` | deferred | NPC action-window decision record | Gameplay must choose one long action or repeated short actions first. |
| `1.3` | deferred | orgasm transaction decision record | Multiplicity and pending-edge exit rules remain gameplay decisions. |
| `1.4` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | These paired callers define the retained slice of the existing change. |
| `1.5` | deferred | prompt-protocol decision record | Keep the red-test matrix with the blocked protocol design. |
| `1.6a` | completed | private-font investigation record | Preserve the traced construction and lifetime facts. |
| `1.6b` | completed | private-font investigation record | Preserve why Linux evidence could not decide the Windows defect. |
| `1.6c` | deferred | private-font Windows evidence | Clean-Windows development and packaged proof is still required. |
| `2.0a` | upstream-owned | PR #214 movement-talk actor context | The accepted boundary and critique belong with the open PR. |
| `2.0b` | withdrawn | type-1 ordering ledger | Player-facing text contradicts the proposed behavior change. |
| `2.0c` | deferred | Tk queue performance record | The design exists, but player-representative evidence remains deferred. |
| `2.1a` | upstream-owned | PR #214 movement-talk actor context | Reproduction belongs with the open PR. |
| `2.1b` | upstream-owned | PR #214 movement-talk actor context | Formatter-owner fix belongs with the open PR. |
| `2.1c` | upstream-owned | PR #214 movement-talk actor context | PR prose is now owned by the live PR. |
| `2.1d` | upstream-owned | PR #214 movement-talk actor context | Artifact review is now owned by the live PR. |
| `2.2a` | withdrawn | type-1 ordering ledger | Preserve the reproduction for the rejected candidate. |
| `2.2b` | withdrawn | type-1 ordering ledger | Do not implement the contradicted policy. |
| `2.2c` | withdrawn | type-1 ordering ledger | Preserve local evidence and draft only as history. |
| `2.2d` | withdrawn | type-1 ordering ledger | No readiness review is needed for a rejected boundary. |
| `2.2e` | withdrawn | type-1 ordering ledger | This is the decisive rejection record. |
| `2.3a` | withdrawn | invitation-lifecycle ledger | Preserve the separated diagnosis. |
| `2.3f` | withdrawn | invitation-lifecycle ledger | Preserve the rejected designs and WAIT finding. |
| `2.3b` | withdrawn | invitation-lifecycle ledger | The user decided the narrow issue is not worth upstream work. |
| `2.3c` | withdrawn | invitation-lifecycle ledger | Keep evidence and draft local only. |
| `2.3d` | withdrawn | invitation-lifecycle ledger | Keep the review result as history. |
| `2.3e` | deferred | group admission/arrival decision record | Arrival rechecks and rejection cleanup need authoritative semantics. |
| `2.3g` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | The caller ownership finding defines the retained slice. |
| `2.3h` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Keep the typed result and no-retry contract with that owner. |
| `2.3i` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Move implementation, tests, evidence, and draft together. |
| `2.3j` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Move the independent review with the candidate. |
| `2.3k.a` | upstream-owned | merged PR #206 same-witness rule | Preserve only the frozen repeated-Closure evidence with the merged rule. |
| `2.3k.b` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Keep the stale target-hidden-flag and effect-411 trace with the retained candidate. |
| `2.3l` | withdrawn | hidden-session extension ledger | Preserve why the one-file extension was rejected. |
| `2.3m` | withdrawn | hidden-session extension ledger | Keep the stale extension and package as local history only. |
| `2.3n` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | The corrected fixed-seed A/B belongs with the four-file candidate. |
| `2.3o` | upstream-owned | merged PR #206 same-witness rule | Preserve the Closure-versus-Nine distinction with PR #206 history. |
| `2.4a` | deferred | Tk queue performance record | Preserve the benchmark; player-representative evidence is still missing. |
| `2.4b` | deferred | Tk queue performance record | Preserve the local candidate without calling it ready. |
| `2.4c` | deferred | Tk queue performance record | Keep the route, benchmark, and draft blocked together. |
| `2.4d` | deferred | Tk queue performance record | Prior review does not waive the deferred visual evidence. |
| `2.5` | deferred | private-font Windows evidence | Production bootstrap work waits for Windows proof. |
| `3.1a` | upstream-owned | PR #213 hypnosis sleep preservation | The accepted narrow ownership trace belongs with the open PR. |
| `3.1b` | upstream-owned | PR #213 hypnosis sleep preservation | Only the accepted two-caller slice moves to the PR record. |
| `3.1c` | deferred | pain/hypnosis lifecycle decision record | Remaining callers need target, cancel, and provenance decisions. |
| `3.1d` | upstream-owned | PR #213 hypnosis sleep preservation | Red/green evidence and PR draft belong with the open PR. |
| `3.1e` | upstream-owned | PR #213 hypnosis sleep preservation | Review belongs with the open PR. |
| `3.2` | withdrawn | hypnosis talk-gate ledger | No reproduction or common reaction contract supports the broad bypass. |
| `3.3a` | upstream-owned | PR #212 signed-pain routing | Trace and contract belong with the open PR. |
| `3.3b` | upstream-owned | PR #212 signed-pain routing | Design critique belongs with the open PR. |
| `3.3c` | upstream-owned | PR #212 signed-pain routing | The narrow router implementation belongs with the open PR. |
| `3.3d` | upstream-owned | PR #212 signed-pain routing | Evidence and Chinese draft belong with the open PR. |
| `3.3e` | upstream-owned | PR #212 signed-pain routing | Review belongs with the open PR. |
| `3.3f` | upstream-owned | PR #212 signed-pain routing | Publication is complete; future work follows the live PR. |
| `3.4a` | withdrawn | H-entry movement ledger | Preserve the trace that found no normal production route. |
| `3.4b` | withdrawn | H-entry movement ledger | Do not carry forward the synthetic-state implementation. |
| `3.4c` | withdrawn | H-entry movement ledger | Keep evidence and draft as local history only. |
| `3.4d` | withdrawn | H-entry movement ledger | Prior review does not make the unreachable case viable. |
| `3.5.a` | upstream-owned | PR #212 signed-pain routing | Keep real entry, inverse, and independent-mod verification with this settlement owner. |
| `3.5.b` | upstream-owned | PR #213 hypnosis sleep preservation | Keep cleanup, inverse, and non-hypnosis checks with this state owner. |
| `3.5.c` | current | `activate-granted-pain-as-pleasure` | Verify the unresolved lifecycle owner before disabling any remaining mod responsibility. |
| `3.5.d` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Keep caller, exception, and nested-settlement checks with this owner. |
| `3.5.e` | current | `judge-orgasm-edge-once-per-settlement` | Keep release-state and independent-path checks with the protected candidate. |
| `4.1a` | deferred | NPC action-window decision record | Preserve the repeated-consumption reproduction. |
| `4.1b` | deferred | NPC action-window decision record | Gameplay cadence and retry behavior remain undecided. |
| `4.2a` | deferred | group scheduler/exit decision record | Preserve the overwritten-exit reproduction. |
| `4.2e` | withdrawn | tired-group-exit candidate ledger | Preserve why serial commit was rejected. |
| `4.2f` | deferred | group scheduler/exit decision record | Preserve the caller, membership, reduction, and epoch trace. |
| `4.2g` | deferred | group scheduler/exit decision record | Zero-survivor, priority, and timing rules remain undecided. |
| `4.2b` | withdrawn | tired-group-exit candidate ledger | The narrow shape was invalidated; the underlying defect remains deferred in the group scheduler/exit decision record. |
| `4.2c` | withdrawn | tired-group-exit candidate ledger | Do not prepare PR evidence for this shape; replacement work remains deferred under the decision record. |
| `4.2d` | withdrawn | tired-group-exit candidate ledger | Do not review this shape as ready; the unresolved defect is not closed. |
| `4.3` | deferred | NPC action-window decision record | Implementation waits for the cadence contract. |
| `4.4` | deferred | group scheduler/exit decision record | Manual re-settlement cannot be removed before an owner is chosen. |
| `4.5.a` | deferred | NPC action-window decision record | Preserve retry, exception, per-NPC, and 1/5/10/60-minute verification requirements. |
| `4.5.b` | deferred | group scheduler/exit decision record | Preserve group-exit, nested-settlement, exact-effect, and next-window requirements. |
| `4A.1` | withdrawn | current-group-membership ledger | The membership-only boundary could not avoid scheduler semantics. |
| `4A.2` | withdrawn | current-group-membership ledger | Preserve the candidate locally; do not continue it. |
| `4A.3` | withdrawn | current-group-membership ledger | Preserve evidence and draft as history. |
| `4A.4` | withdrawn | current-group-membership ledger | Preserve review as history. |
| `5.1a` | current | `judge-orgasm-edge-once-per-settlement` | Move the ordinary failed-edge trace to the protected candidate. |
| `5.1b` | current | `judge-orgasm-edge-once-per-settlement` | The collect/decide/apply implementation is owned there. |
| `5.1c` | current | `judge-orgasm-edge-once-per-settlement` | Exact-value evidence and local draft move with the candidate. |
| `5.1d` | current | `judge-orgasm-edge-once-per-settlement` | Independent review moves with the candidate. |
| `5.2` | deferred | orgasm transaction decision record | Consumable-delta architecture depends on the unresolved contract. |
| `5.2a` | deferred | orgasm transaction decision record | Release chaining is a gameplay decision. |
| `5.2b` | deferred | orgasm transaction decision record | Preserve the failure-mode evidence for later design. |
| `5.2c` | deferred | orgasm transaction decision record | This is the explicit stop gate. |
| `5.3` | deferred | orgasm transaction decision record | Counted atomic transaction waits for the semantic gate. |
| `5.4` | deferred | orgasm transaction decision record | Exit finalization waits for proven ownership and exit policy. |
| `5.5.a` | current | `fix-compact-value-formatting` | Compact display belongs to the number formatter, not the orgasm transaction. |
| `5.5.b` | deferred | orgasm presentation decision record | Remote visibility needs its own presentation contract. |
| `5.5.c` | deferred | orgasm presentation decision record | Human-power aggregation needs its own presentation contract. |
| `5.5.d` | deferred | orgasm transaction decision record | Window-end pending-edge policy stays with exit finalization semantics. |
| `5.6` | deferred | orgasm transaction owner checklist | Verification waits for a chosen transaction and presentation boundary. |
| `6.0a` | completed | prompt-protocol investigation record | Preserve proof that prompt identity is absent. |
| `6.0b` | deferred | prompt-protocol decision record | Preserve the stop gate and rejected timing/queue substitutes. |
| `6.1` | deferred | prompt-protocol decision record | Core prompt state needs explicit product semantics. |
| `6.2` | deferred | prompt-protocol decision record | Renderer transport changes wait for the core state machine. |
| `6.3` | deferred | prompt-protocol decision record | Authorization and game-thread ownership remain design work. |
| `6.4` | deferred | prompt-protocol decision record | Skip ownership remains unresolved. |
| `6.5` | deferred | prompt-protocol owner checklist | Cross-renderer verification follows an accepted protocol. |
| `6.6` | deferred | prompt-protocol owner checklist | Remove local patches only after accepted equivalence checks. |
| `7.1` | completed | loader investigation record | Preserve the mutation inventory and no-new-wrapper rule. |
| `7.1a` | completed | loader investigation record | Preserve the real-loader failure reproductions. |
| `7.1b` | completed | loader investigation record | Preserve the boundary critique separating two designs. |
| `7.1c` | withdrawn | atomic-new-registration ledger | The reviewed fix is retained locally but not pursued upstream. |
| `7.1d` | withdrawn | atomic-new-registration ledger | Preserve evidence and draft as local reference. |
| `7.1e` | withdrawn | atomic-new-registration ledger | Preserve review as local reference. |
| `7.2` | deferred | conditional loader-transaction proposal | Create only if a retained runtime mod proves this need. |
| `7.3` | deferred | `group_sex_extension` adaptation | Wait for admitted-participant and orgasm-owner interfaces. |
| `7.4.a` | upstream-owned | PR #212 signed-pain routing | Retire only the duplicate signed-pain mod responsibility after merge or an explicit fallback decision. |
| `7.4.b` | upstream-owned | PR #213 hypnosis sleep preservation | Retire only the duplicate sleep-exit responsibility after merge or an explicit fallback decision. |
| `7.4.c` | upstream-owned | PR #214 movement-talk actor context | Retire only the duplicate actor-context responsibility after merge or an explicit fallback decision. |
| `7.4.d` | current | `fix-talk-common-state-leaks` | Keep its manifest/installer cleanup with its two talk-state responsibilities. |
| `7.4.e` | current | `activate-granted-pain-as-pleasure` | Retire lifecycle wrappers only after its contract and equivalence checks agree. |
| `7.4.f` | current | `judge-orgasm-edge-once-per-settlement` | Retire the replaced edge responsibility only after candidate acceptance. |
| `7.4.g` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Retire only the discovery-settlement duplicate after its owner is accepted. |
| `7.4.h` | current | `fix-time-stop-release-attribution` | Keep target-change mod retirement with this root cause. |
| `7.4.i` | current | `fix-compact-value-formatting` | Keep formatter mod retirement with this separate root cause. |
| `7.4.j` | deferred | prompt-protocol decision record | Retire input patches only after an accepted cross-renderer protocol. |
| `7.4.k` | deferred | conditional loader-transaction proposal | Change loader manifests only if the conditional transaction is approved. |
| `7.4.l` | deferred | `group_sex_extension` adaptation | Retire direct mutations only after owner interfaces exist. |
| `7.5` | completed | `investigate-game-bug` skill and project rules | Fresh worktree and outward-authorization gates are already durable. |
| `8.1.a` | upstream-owned | PR #212 signed-pain routing | Track its focused regression and required composition checks with the live PR. |
| `8.1.b` | upstream-owned | PR #213 hypnosis sleep preservation | Track its focused regression and required composition checks with the live PR. |
| `8.1.c` | upstream-owned | PR #214 movement-talk actor context | Track its focused formatter/classifier checks with the live PR. |
| `8.1.d` | current | `fix-talk-common-state-leaks` | Own focused talk-state and real-loader isolation tests here. |
| `8.1.e` | current | `activate-granted-pain-as-pleasure` | Own lifecycle and maintained-mod composition tests here. |
| `8.1.f` | deferred | `curve-derived-psychological-pleasure` | Define focused balance regressions only after its curve is approved. |
| `8.1.g` | current | `judge-orgasm-edge-once-per-settlement` | Own exact-once regression and relevant BDD checks here. |
| `8.1.h` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Own paired-caller and nested-settlement regressions here. |
| `8.1.i` | current | `fix-time-stop-release-attribution` | Own time-stop target-change regressions here. |
| `8.1.j` | current | `fix-compact-value-formatting` | Own compact-value formatter regressions here. |
| `8.2.a` | upstream-owned | PR #212 signed-pain routing | Keep its accepted representative Tk case with the live PR. |
| `8.2.b` | upstream-owned | PR #213 hypnosis sleep preservation | Keep its accepted representative Tk case with the live PR. |
| `8.2.c` | upstream-owned | PR #214 movement-talk actor context | Keep its current commit-pinned Tk A/B with the live PR. |
| `8.2.d` | current | `fix-talk-common-state-leaks` | Own any visible talk-state Tk/Web checks here. |
| `8.2.e` | current | `activate-granted-pain-as-pleasure` | Own visible lifecycle settlement checks here. |
| `8.2.f` | deferred | `curve-derived-psychological-pleasure` | Define visible balance checks only after curve approval. |
| `8.2.g` | current | `judge-orgasm-edge-once-per-settlement` | The replacement route and matched Tk A/B are complete; the fixed playtest gate is superseded by the current T2 gate above. |
| `8.2.h` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Keep the corrected discoverer-reaction A/B here. |
| `8.2.i` | current | `fix-time-stop-release-attribution` | Own affected Tk/Web attribution checks here. |
| `8.2.j` | current | `fix-compact-value-formatting` | Own affected Tk/Web number-display checks here. |
| `8.2.k` | deferred | prompt-protocol decision record | Cross-renderer input checks wait for an accepted protocol. |
| `8.2.l` | deferred | private-font Windows evidence | Windows development and packaged checks remain platform-gated. |
| `8.2.m` | deferred | Tk queue performance record | Representative responsiveness evidence remains explicitly deferred. |
| `8.3.a` | upstream-owned | PR #212 signed-pain routing | Keep source inspection, exact diff, and fresh review with the live PR. |
| `8.3.b` | upstream-owned | PR #213 hypnosis sleep preservation | Keep source inspection, exact diff, and fresh review with the live PR. |
| `8.3.c` | upstream-owned | PR #214 movement-talk actor context | Keep source inspection, exact diff, and fresh review with the live PR. |
| `8.3.d` | current | `fix-talk-common-state-leaks` | Inspect and review only its two owned talk-state changes. |
| `8.3.e` | current | `activate-granted-pain-as-pleasure` | Inspect and review the rewritten lifecycle boundary here. |
| `8.3.f` | deferred | `curve-derived-psychological-pleasure` | Review source only after a curve and implementation are approved. |
| `8.3.g` | current | `judge-orgasm-edge-once-per-settlement` | Keep exact-diff and fresh-review gates with the protected candidate. |
| `8.3.h` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Keep exact-diff and fresh-review gates with the retained slice. |
| `8.3.i` | current | `fix-time-stop-release-attribution` | Inspect this ownership fix independently. |
| `8.3.j` | current | `fix-compact-value-formatting` | Inspect this formatter fix independently. |
| `8.4.a` | upstream-owned | PR #212 signed-pain routing | Track exact live state until merge; if closed unmerged, use the fallback decision. |
| `8.4.b` | upstream-owned | PR #213 hypnosis sleep preservation | Track exact live state until merge; if closed unmerged, use the fallback decision. |
| `8.4.c` | upstream-owned | PR #214 movement-talk actor context | Track exact live state until merge; if closed unmerged, use the fallback decision. |
| `8.4.d` | current | `fix-talk-common-state-leaks` | Record skipped checks and sync specs only after proven implementation. |
| `8.4.e` | current | `activate-granted-pain-as-pleasure` | Record skipped checks and sync specs only after lifecycle proof. |
| `8.4.f` | deferred | `curve-derived-psychological-pleasure` | Do not sync behavior before its balance contract and implementation are approved. |
| `8.4.g` | current | `judge-orgasm-edge-once-per-settlement` | Preserve the unopened branch boundary and sync only after acceptance. |
| `8.4.h` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | Keep unrelated admission/scheduler work outside this owner. |
| `8.4.i` | current | `fix-time-stop-release-attribution` | Keep this root cause separate during verification and spec sync. |
| `8.4.j` | current | `fix-compact-value-formatting` | Keep this root cause separate during verification and spec sync. |
| `8.5` | completed | umbrella archive | Preserve the second root-cause audit as the final umbrella review. |
| `8A.1` | completed | project skills and artifact policy | The durable Fable, reader, and Tk evidence rules already live there. |
| `8A.2` | completed | umbrella archive | Preserve the 12-draft inventory as history. |
| `8A.3a` | upstream-owned | PR #214 movement-talk actor context | The live PR supersedes the old completion workflow. |
| `8A.3b` | withdrawn | type-1 ordering ledger | Preserve the rejection and cadence blocker. |
| `8A.3c` | deferred | Tk queue performance record | User explicitly deferred representative performance capture. |
| `8A.3d` | withdrawn | invitation-lifecycle ledger | User explicitly withdrew upstream preparation. |
| `8A.3e` | current | `judge-orgasm-edge-once-per-settlement` | The valid route, matched visual A/B, tests, and reviews are complete; apply the current T2 semantic, refresh/reverification, and outward gates above. |
| `8A.3f` | withdrawn | H-entry movement ledger | No truthful normal-route case exists. |
| `8A.3g` | upstream-owned | PR #212 signed-pain routing | Evidence publication and PR opening are complete. |
| `8A.3h` | upstream-owned | PR #213 hypnosis sleep preservation | Narrowed evidence, review, and PR opening are complete. |
| `8A.3i` | current | `fix-discovered-reaction-settlement` (narrowed to discovery settlement) | The corrected four-file candidate remains the retained slice of the existing owner. |
| `8A.3j` | deferred | group scheduler/exit decision record | Replacement waits for zero/one-survivor and epoch semantics. |
| `8A.3k` | withdrawn | atomic-new-registration ledger | User explicitly withdrew upstream preparation. |
| `8A.3l` | withdrawn | tired-group-exit candidate ledger | Candidate is rejected, not the defect; replacement work remains deferred under the group scheduler/exit decision record. |
| `8B.1` | upstream-owned | PR #214 movement-talk actor context | Preserve environment and diff provenance with the live PR record. |
| `8B.2` | upstream-owned | PR #214 movement-talk actor context | Preserve invalid-route removal as PR investigation history. |
| `8B.3` | upstream-owned | PR #214 movement-talk actor context | The eventual accepted route supersedes exploration bookkeeping. |
| `8B.4` | upstream-owned | PR #214 movement-talk actor context | Preserve deterministic evidence tooling as local PR evidence history. |
| `8B.5` | upstream-owned | PR #214 movement-talk actor context | Live PR evidence supersedes this unchecked exploration task. |
| `8B.6` | upstream-owned | PR #214 movement-talk actor context | Live PR evidence supersedes this unchecked repeatability task. |
| `8B.7` | upstream-owned | PR #214 movement-talk actor context | Live PR evidence owns the final checkpoint and route record. |
| `8B.8` | upstream-owned | PR #214 movement-talk actor context | Live PR evidence owns the completed visual operation. |
| `8B.9` | upstream-owned | PR #214 movement-talk actor context | Live PR evidence owns the inspected A/B pair. |
| `8B.10` | upstream-owned | PR #214 movement-talk actor context | Track the submitted one-file diff and any PR-visible checks there; do not infer that every old local check passed. |
| `8B.11` | upstream-owned | PR #214 movement-talk actor context | The live title, body, and commit-pinned captions replace the stale draft without proving every old writing step. |
| `8B.12` | upstream-owned | PR #214 movement-talk actor context | Track any completed or still-required artifact review with the live PR rather than marking the old gate passed here. |
| `8B.13` | upstream-owned | PR #214 movement-talk actor context | Publication, push, and PR creation already occurred with authorization. |
| `8C.1` | completed | Tk capture allocator record | The three-slot supervisor exists. |
| `8C.2` | completed | Tk capture allocator record | Legacy-process capacity accounting exists. |
| `8C.3` | completed | project skill and Tk evidence specification | The sequential-pair/concurrent-unrelated rule is durable. |
| `8C.4` | completed | Tk capture allocator record | Current allocator status has zero legacy sessions, so no migration remains. |

## Current Owner and External-State Records Not Represented By A Dedicated Umbrella Task

The migration of all 160 source tasks must not erase owner assignments or external-state records that were already separated from the umbrella:

- `fix-talk-common-state-leaks` remains the current owner of temporary interaction-target leakage and global paper-doll candidate mutation; PR #214 does not own either defect.
- PR #213 remotely preserves `pain_as_pleasure` through sleep and direct cancellation, but the selected local target is now for both paths to clear it. `clear-pain-as-pleasure-on-hypnosis-cancel` exclusively owns that locally complete one-line correction and waits for authorization to revise #213. `activate-granted-pain-as-pleasure` owns only local composition and retirement of the same-direction wrapper after core integration; its BDD expectation is that cancellation clears. PR #212 still owns signed routing and direct positive-pain effects.
- `curve-derived-psychological-pleasure` remains an independent, unapproved balance-design change.
- `judge-orgasm-edge-once-per-settlement` remains the protected narrow batch-decision candidate, distinct from the deferred deeper orgasm transaction. It is `local-review-ready`; before PR creation it needs final user semantic confirmation, post-#214 upstream refresh/reverification, and outward authorization, while passive play is optional clue gathering rather than a gate.
- `fix-discovered-reaction-settlement` is now narrowed in its active documents to the local-review-ready discovery-settlement slice. It has no playtest gate and no upstream PR; evidence publication, push, and PR creation remain separately authorized outward actions.
- The superseded combined time-stop change is archived without spec sync. `fix-compact-value-formatting` now owns global formatter call-site and Tk display verification; `fix-time-stop-release-attribution` owns real-loader identity, actual-delta/cap, Tk attribution, and independent Web collection. Candidate code remains on local `main`, but each new owner must isolate and prove its own upstream diff.
- `fix-game-update-depth-restoration` is 6/6 locally complete at `80a711603` on a fork side branch. It is a dependency/local-maintenance owner, not a standalone PR; T5 and T6 provide its real-consumer validation.
- `fix-elapsed-time-line-ownership` (T5) is **withdrawn**: the upstream maintainer rejected PR #220 (CLOSED unmerged, 2026-07-16) and the user chose not to pursue the fix. Preserve its diagnosis, display-only candidate, and local evidence as history; do not continue unless the user reopens it. (Historically it was the ready T5 owner after T4, the smaller display-only first consumer of depth restoration.)
- `add-per-click-orgasm-chain-gate` is the ready T6 owner after T5. It also consumes depth restoration; the user has already confirmed a per-click, non-physiological gate while passive settlement continues.
- `settle-remote-plural-orgasm-silently` is implementation-complete and submitted as PR #215 (OPEN, unmerged, unreviewed) from `364ac6d9f`. The player confirmed its semantics and retention on 2026-07-14. OPEN is a passive external state, not an umbrella or owning-change task; do not select, poll, reverify, or modify it. On an explicit status request, perform one read-only refresh and stop. A future verified merge may create a separately authorized cleanup task.

## Post-Migration De-duplication Checkpoint (2026-07-14)

- Discovery settlement must not be re-investigated as a fresh task. Use candidate `5d360f71e`, its 35-test run, deterministic Tk A/B, and completed review packet. PR #206 is adjacent same-witness history, not ownership of this candidate.
- Pain-as-pleasure work must distinguish the remote #213 preservation behavior from the selected local clear-on-both-paths target. Keep the one-line core correction in `clear-pain-as-pleasure-on-hypnosis-cancel`; retire the same-direction mod wrapper only as replaced after local core integration, and keep the BDD expectation on clearing.
- Time-stop release work is verification of code already on local `main`, not permission for a second implementation. Rewrite only when a named check fails.
- The current global order is T4 `fix-time-stop-release-attribution` evidence/rehearsal, then T6 `add-per-click-orgasm-chain-gate`, and T7's two talk-state leaks. T5 `fix-elapsed-time-line-ownership` is withdrawn (PR #220 rejected, CLOSED unmerged 2026-07-16) and is no longer in the queue. Default T7 to two small PRs; combine them only if investigation proves one violated rule, one logical owner, and one lifecycle operation. Depth restoration is a dependency rather than a standalone queue item.

## Closure Rule

The umbrella can be rewritten or archived only after every source task has one or more explicit migration obligations and every obligation has one named, checkable destination. Each **current** obligation must appear in exactly one existing OpenSpec owner; each **deferred** obligation must point to one decision or evidence record that states its unblocker; each **upstream-owned** obligation must link to the exact PR and remain tracked until merge, reverting to a named `re-file, revise, or withdraw` decision if the PR closes unmerged. Completed and withdrawn material must remain reachable as history without presenting a rejected candidate, stale draft, or unverified local gate as active or review-ready work.
