## Why

The H-discovery panel is reached from two callers with different outer-settlement behavior. Its response callbacks historically mixed “settle here” and “leave it to the caller,” so an explicit discoverer reaction could be lost or consumed twice. In the reproduced case, Closure accepts being talked away but her acceptance/departure text is entirely missing before Dobermann's H text continues.

## What Changes

- Settle every explicit discoverer reaction exactly once in its existing response branch, regardless of whether the panel was opened from the NPC behavior loop or a direct hidden-discovery call; do not consolidate the cases into a unified settlement helper.
- After the NPC state-machine panel call completes, record whether it already settled the discoverer reaction in a dedicated character `SPECIAL_FLAG`; the NPC scheduler consumes and clears that flag without changing the return value of `constant.handle_state_machine_data`.
- Let the NPC outer loop settle a real `MOVE` successor in the same round, but skip a no-route `WAIT` successor because the discovery response has already supplied the visible reaction; leave any direct-call successor for the later normal NPC turn.
- Preserve the ordering in which the discoverer's reaction settles before any player follow-up converts or ends the current H scene.
- Keep a later different eligible witness allowed. Merged PR #206 owns only exclusion of the same witness before movement.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-bugfixes`: Adds source-independent, exactly-once settlement ownership for explicit discoverer reactions.

## Impact

- Affects the H discovery panel, the narrow NPC state-machine path that records its completion, and the NPC scheduler that consumes the character flag.
- Does not change witness eligibility, group templates, consent rolls, fatigue thresholds, ordinary direct invitation behavior, or the same-witness rule already merged in PR #206.

## Current Status

The shared-helper candidate at tree `884b2fa30` is superseded for implementation-shape reasons. The user retained the full sibling-bug scope but required explicit per-case repair instead of a unified owner function. The accepted local implementation has the projected normal-format production diff exactly: `a=22`, `b=5`, penalty `61`, with 27 changed non-blank lines instead of 60. Twenty-eight focused tests, compileall, diff checks, strict OpenSpec validation, a fresh-context review, and final Fable acceptance all pass.

The user has accepted the clean static Tk before-and-after pair for this standalone settlement bug: the baseline omits Closure's selected reaction, while the candidate shows it once before Dobermann's H text continues. The separate same-NPC repeated-discovery rule remains owned by merged PR #206 and is not the claim of this candidate.

After explicit user authorization, fork review branch `codex/fix-discovery-settlement-ad-hoc` points to `4e226f4f5`. That head is rebased onto current `upstream/master` `94d586840` and includes the user-confirmed boundary: settle a real `MOVE` successor, but skip a no-route `WAIT` successor. The change is one replaced source line, keeps the full production diff at `a=22`, `b=5`, penalty `61`, and passes the 29-case focused matrix, compileall, diff checks, and strict OpenSpec validation. At the user's direction, the PR reuses the already approved clean static A/B instead of replaying Tk again, and the user explicitly waived the fresh artifact-review gate after both Fable review attempts produced no verdict. The approved images are published through the fork's append-only assets branch, and upstream draft PR #218 is open with base `master@94d586840` and head `meower-z:codex/fix-discovery-settlement-ad-hoc@4e226f4f5`.

The later session-closing real-Tk replay used those exact PR base/head revisions and the approved deterministic route. Its new baseline crop is pixel-identical to the PR before image, and its new candidate crop is pixel-identical to the PR after image (`AE=0`, `RMSE=0` for both comparisons). The observed behavior also matches: baseline omits Closure's selected response, while candidate shows the response, stamina `-15`, and the five-minute passage exactly once before Dobermann's H text continues. This was a read-only verification of the already-open PR; the PR was not edited.

## 2026-07-15 Maintainer-requested revision

The maintainer accepted the bug but rejected the return-value protocol through `constant.handle_state_machine_data`. The replacement shall preserve the same player-visible contract while using a dedicated `SPECIAL_FLAG`: the panel keeps only operation-local completion until its nested work is finished, state-machine 40 records that completion on the discoverer after `draw()` returns, and the NPC scheduler consumes then clears it. The direct hidden-discovery caller never writes the character flag.
