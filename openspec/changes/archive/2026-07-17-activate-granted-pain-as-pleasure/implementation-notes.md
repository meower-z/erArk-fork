## Upstream Core Split (2026-07-13)

Upstream PR [#212](https://github.com/Godofcong-1/erArk/pull/212) replaces only the signed-delta routing and direct positive-pain portion of the experimental implementation described below. Its pure router returns the destination state and adjusted value without taking over storage, caps, or change-record ownership. Positive pain that reaches the router converts under the raw flag; zero and negative pain remain state 17. Direct effects 270, 283, 296, and 408 use the same rule.

The final two-file proposed diff is commit `21261e951`, based on upstream commit `06fc59c1e`. It passed 27 focused local tests. The accepted real Tk A/B evidence and fresh artifact review cover the same byte-identical proposed production diff captured before the final parent-only rebase; they are not evidence of the broader group-admission, sleep/unconscious, cancellation/reset, or maintained-mod load-order contract.

The remaining sections preserve the 2026-07-10 investigation history. Their custom local-mod implementation and unresolved connected-path work are not made current or accepted by PR #212.

## Historical Worktree Status (2026-07-10)

The reported root is local and confirmed, but the current conversion implementation is not accepted because it duplicates upstream state-23 settlement with unresolved guard and accounting differences. No component, BDD, loader-order, or gameplay test has run after the edits. Cross-change branch and protected-file state are in `../continue-local-bugfix-audit/design.md`.

## Confirmed Root and Contract History

`group_sex_extension._set_hypnosis_boost()` sets `hypnosis.pain_as_pleasure = True` without changing `sp_flag.unconscious_h`. UI and premise checks read that persistent flag directly. The previous local pain component then imposed its own extra gate, requiring `unconscious_h in {4,5,6,7}` and temporarily hiding the raw flag outside those states. A conscious participant who joined later could therefore display "pain to pleasure" as enabled while settlement still added ordinary pain.

This proposed interpretation conflicts with an existing main specification. `openspec/specs/local-bugfixes/spec.md` currently says that the flag is persistent but dormant outside active hypnosis states. The still-open `fix-group-sex-invite-controls-and-idle-ai` change, however, grants the enhancement to complete-hypnosis participants without changing their current unconscious state. The latest bug report requests that a conscious later joiner actually receive the displayed effect, so this change proposes superseding the old dormant-state rule. Do not sync the main spec or declare the contract settled until the remaining state-23 choice below is discussed with the user.

## Enumerated Runtime Paths

### Activation and clearing

- The ordinary 1230 toggle and group hypnosis boost can set the persistent flag.
- Effect 1213 cancellation, effect 489 full-hypnosis cleanup, `local_hypnosis_state_fix` full reset, and ordinary toggle/off paths clear it.
- The group boost intentionally does not mutate `unconscious_h`.

### Common positive pain

The shared `base_chara_state_common_settle()` alias is used from `Script.Settle.default`, `Script.Settle.Second_effect`, `Script.Settle.realtime_settle`, and `Script.Settle.item_effect`. Upstream already has a raw-premise pain-to-pleasure recursion at state 17. The old local state gate was what made the raw flag dormant.

### Direct positive pain

Second effects 270, 283, 296, and 408 write positive pain without using the common handler and need explicit conversion if the new flag-driven contract is accepted. The direct `originium_arts.py` write found by the audit assigns zero and is a reset, not a positive settlement path.

### Non-positive pain and guards

Negative or zero pain continues through upstream pain settlement with temporary recursion suppression and `finally` restoration. Existing death behavior differs by entry: common settlement and effect 408 have guards; 270/283/296 do not all share that same upstream guard. Requirements must preserve each entry's existing guard rather than inventing one universal rule.

## Experimental Implementation Present but Unaccepted

The current semantic diff removes the `unconscious_h` gate and makes `_has_pain_as_pleasure()` read only the raw flag. It retains the existing custom common conversion, negative delegation, cancellation cleanup, and wrappers for 270/283/296/408. Component and BDD tests were expanded, but none have run.

The common implementation currently calculates positive pain itself, then calls `_settle_direct_psychological_pleasure()` to write state 23 directly. A safer candidate for common positive pain may be to delegate to the upstream state-17 function with the raw flag visible, because upstream already performs the state-17-to-state-23 recursion. That would preserve upstream math and guards. Direct effects would still need explicit handling. This is an analysis option only, not an authorized implementation change.

## State-23 Semantics (resolved 2026-07-10)

Upstream `base_chara_state_common_settle()` refuses psychological pleasure while the target is unconscious or asleep. The user chose contract 2: pain-as-pleasure is an intentional exception. Psychological pleasure is recorded even while unconscious/asleep, and the delta spec explicitly overrides the upstream rule for this conversion path only. The manual state-23 writer's guard bypass is therefore the intended behavior, but it must become formula-equivalent to upstream in every other respect (see gap 1 below).

## Formula and Accounting Gaps

1. Resolved 2026-07-10: `_settle_direct_psychological_pleasure` now takes `apply_repeat_adjust`, and the common path passes it so the consecutive-instruction reduction is applied a second time exactly as upstream's state-17-to-state-23 recursion does. The shared reduction formula lives in `_get_consecutive_instruct_adjust`. Regression: `test_repeated_instruction_applies_second_reduction_like_upstream` (0.55 × 0.55 double reduction verified). Direct effects intentionally do not apply the reduction — upstream never routes them through the recursion.
2. Accepted as the intended contract 2026-07-10 (requested-value recording): at 99998 with request +100, stored state rises by 1 while both record owners keep +100, matching upstream. Regression: `test_cap_keeps_requested_value_in_change_records`.
3. Resolved 2026-07-10: change records report the upstream-compatible requested value at the cap, not the actual clamped delta. The spec says so explicitly; the remaining work is verifying both record owners follow it consistently.
4. Passing both `change_data` and `change_data_to_target_change` can create two records unless the ownership contract is explicit.
5. Alias installation catches import exceptions and continues. A module or later mod can retain an earlier function object; identity checks must run after the complete maintained-mod load order.

## Written but Unexecuted Verification

- Component coverage was expanded for inactive flag, cancellation, negative pain, common aliases, direct effects, and some death behavior.
- `mod/tests/bdd/test_bdd_pain_as_pleasure.py` adds a conscious late-participant case, but it manually sets `pain_as_pleasure=True` and `is_h=True`; it does not drive discovery admission, participant resolution, or the group boost.
- The group admission component has a fake connected case, not a near-real ModManager/NPC-state-machine flow.
- The discovered-admission connection is blocked by the unresolved group settlement-ownership change. A stable direct-invitation route could independently verify resolver to boost to pain settlement first.
- The component file's direct `main()` runner omits `test_dead_character_positive_pain_delegates_to_original`; pytest would discover it, the README-style Python command would not.

Still missing: sleeping/unconscious state-23 behavior, cap with actual delta 0/1, both recording objects, repeated-instruction formula equivalence, each direct effect's own death semantics, toggle/full-reset restoration, alias/load-order behavior, and a real admission-to-boost-to-settlement trace. Audit and user decisions precede tests.
