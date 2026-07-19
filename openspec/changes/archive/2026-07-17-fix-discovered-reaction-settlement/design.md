## Context

`Sex_Be_Discovered_Panel` is entered from two materially different call sites. The normal NPC state-machine path returns to `character_behavior()`, which performs an outer status settlement; hidden-sex discovery calls the panel directly and has no such outer settlement. The upstream callback also starts a nested player update when converting single H to group mode. That update can reset the discoverer's pending behavior before the outer NPC settlement consumes it.

The rejected earlier local patch guessed which caller owned settlement from `group_sex_mode`. That was not a reliable ownership boundary: active group mode can also be reached by the direct hidden-discovery call, and initial conversion still returns to an outer NPC settlement after its required early settlement. The retained candidate instead lets the panel report whether it already settled an explicit reaction.

## Goals / Non-Goals

**Goals:**

- Give every explicit discoverer reaction exactly one effect settlement independent of its caller.
- Settle initial group conversion before its nested player update can erase the discoverer's behavior.
- Prevent the later outer NPC settlement from replaying an already consumed discovery behavior.
- Keep discovery settlement independent of hidden-session lifetime and later-witness policy.

**Non-Goals:**

- Redesigning the group template or NPC group-sex AI.
- Changing acceptance calculations, fatigue rules, or hidden-sex discovery selection.
- Treating a character as a template member merely because `is_h` is true.
- Changing merged PR #206's same-witness-before-movement rule or preventing a later different eligible witness.

## Decisions

### Settle synchronously in the selected callback

The panel callback that selects an explicit discoverer behavior settles that behavior synchronously, before any nested player follow-up. Each existing response branch keeps its upstream behavior assignment and duration write; only the branches that currently omit `judge_character_status()` receive that call. The panel is the only operation common to both production callers, but the implementation does not consolidate the branch logic into a shared settlement helper.

Settlement keeps the upstream input timing: Tk and Web both execute the selected callback before `askfor_all()` returns, and `cache.now_panel_id` remains at its existing update point after that return. The panel instance saves only a public `skip_outer_settlement` boolean. State-machine 40 reads it after the synchronous `draw()` call returns; `draw()` keeps its upstream `None` contract. Individual callbacks set the field when they have consumed a non-`MOVE` reaction that the NPC outer loop must not replay; state-machine 40 additionally treats a post-reaction `WAIT` fallback as complete.

Alternative: let the NPC loop settle every path. Rejected because the direct hidden-discovery caller has no outer NPC settlement and initial group conversion can overwrite the pending discoverer behavior.

Alternative: use module-global context, suppression sets, or hidden-session teardown. Rejected because those designs broaden operation identity into process or encounter lifetime, create nesting/exception cleanup problems, and can suppress a later different witness.

### Keep the original NPC settlement with a per-case skip result

State-machine 40 reports `True` for the already-settled non-`MOVE` reactions `JOIN_GROUP_SEX`, `DISCOVER_OTHER_SEX_AND_JOIN`, `SEE_H_BUT_IGNORE`, and `SEE_H_AND_INTERRUPT`, or when a leaving reaction has fallen back to `WAIT`. It reads the result from the panel instance after `draw()`, and the target selector propagates that result to `character_behavior()`, whose original outer `judge_character_status()` call runs only when the result is false.

The leaving reactions `REFUSE_JOIN_GROUP_SEX`, `SEE_H_BUT_DECEIVED`, and `SEE_H_AND_LEAVE` keep the panel field false. Their synchronous reaction settlement normally changes the current behavior to `MOVE` through effect 1721, so state-machine 40 returns false and the NPC outer loop settles that successor in the same round. If route finding instead falls back to `WAIT`, state-machine 40 returns true: the discovery response has already supplied the character's visible reaction, and the idle placeholder expires without a second settlement. The direct hidden-discovery caller intentionally ignores the result: the reaction is already committed by its branch, while any successor remains pending for the character's later normal turn because that path does not own a complete NPC round.

### Run player follow-ups after the discoverer reaction

Group conversion and H interruption remain in their existing callbacks, immediately after the synchronous discoverer settlement. This preserves the visible control flow while preventing nested player settlement from erasing the reaction before it is consumed.

## Risks / Trade-offs

- **[Movement fallback]** Effect 1721 can fall back to `WAIT` when no route exists -> state-machine 40 skips that idle successor; only a real `MOVE` receives the normal same-round outer settlement.
- **[Partial exception effects]** Settlement or a player follow-up can raise after some state changed -> let the synchronous callback fail normally; this change does not add retry behavior or promise transactional rollback that the surrounding settlement system does not provide.
- **[Later-witness policy leak]** Encounter-wide state could accidentally suppress a different witness -> keep identity on the panel instance and do not edit hidden-session teardown or witness eligibility.

## Current Implementation Disposition

The retained technical boundary is a four-file boolean pass-through without a shared settlement helper. Existing response branches settle locally; four non-`MOVE` branches set one panel-instance result, and state-machine 40 also returns true for a post-reaction `WAIT` fallback. The state-machine and target-selector files pass that result through, while the NPC loop adds one local guard around its existing settlement call. The design contains no custom result type, pending/commit state machine, recommit guard, global wrapper, suppression set, hidden-session cleanup, or premise-registry edit.

The user accepted the clean static Tk A/B as valid evidence for this standalone settlement bug. The baseline visibly omits Closure's selected response; the candidate visibly shows it once before Dobermann's H text continues. The same-NPC repeated-discovery evidence gate belongs to that separate bug and does not govern this approved settlement scope.

The candidate may proceed through draft discussion and fresh artifact review. It remains not publication-ready until that review passes and the user separately authorizes the outward publication steps.

## Open Questions

No gameplay-semantic question remains for the standalone settlement scope. Publication still requires a fresh review of the new clean-image draft and separate user authorization for each outward action.

Resolved after the 2026-07-10 experiment was rejected:

1. The panel, not either caller, owns an explicit discoverer reaction.
2. Every explicit reaction settles synchronously in its existing response branch; there is no unified settlement helper. Successful choices that intentionally produce no explicit discoverer reaction return `False` and preserve ordinary caller behavior.
3. A later different eligible witness remains allowed. Merged PR #206 separately prevents the same witness from immediately rediscovering before movement.
4. The earlier `place_all_not_h` premise experiment is not part of the retained four-file candidate.

## 2026-07-14 Minimum-Penalty Re-evaluation

The updated local investigation rule chooses the lowest penalty `3a - b` among production diffs that preserve the full confirmed contract. Here `a` is added lines and `b` is deleted lines relative to `upstream/master` `3a1c9e620`.

The non-negotiable contract remains: both production callers settle every existing explicit discoverer reaction exactly once; settlement precedes nested player follow-ups; successful hidden/exhibition mode conversion keeps no discoverer-side reaction; an NPC-round `MOVE` follow-up still settles in that round; a no-route `WAIT` fallback does not settle again; the direct caller leaves its successor pending.

Considered boundaries:

1. **Patch only the photographed missing-reaction branch:** approximately `a=1, b=0, penalty=3`. Rejected as ineligible because the shared panel still has the same missing reaction in its other caller and still double-settles callbacks that already call `judge_character_status()`.
2. **Earlier generic result protocol:** the reviewed `7dbe0e04b` candidate was `a=65, b=29, penalty=166`. It is logically capable but pays for a result class and generic replacement protocol that the closed production set does not need.
3. **Current boolean pass-through:** `a=33, b=30, penalty=69`. It is logically correct but carries a removable scheduler local variable and expands pre-existing docstrings while adding the return contract.
4. **Compact boolean pass-through:** measured `a=27, b=38, penalty=43`. It keeps the same operation-local boolean and the same four necessary return hops, calls `find_character_target()` directly in the existing `if`, keeps the flag initialization on one commented line, replaces the two touched multiline docstrings with complete one-line Chinese contracts instead of repairing unrelated documentation debt, and removes one purely added blank line.

The four return hops are structural rather than speculative: Tk and Web both discard button callback return values, nested player updates can overwrite the discoverer's current behavior, and the direct caller has no outer NPC settlement. A process-global marker, absent-attribute trick, behavior-history inference, or unconditional state-machine sentinel would reduce lines only by weakening operation identity or changing ordinary `SHARE_BLANKLY` event settlement, so those are not logically equivalent candidates.

Fresh Fable 5 review chose candidate 4 as the lowest explicit, maintainable, logically equivalent shape. The implemented production diff measures `a=27, b=38, penalty=43`; all 28 focused tests pass, so it replaces candidate 3.

## 2026-07-15 Style-Normalized Recount

The local investigation rule now counts only non-blank added and deleted lines and forbids changing normal code style merely to improve the score. This supersedes the raw-line comparison and disqualifies the compact formatting in `9ec3bcee4` as a scoring optimization: its inlined scheduler expression, compressed docstrings, inline attribute comment, and removed blank line do not represent a smaller behavioral design.

The retained implementation restores the project-normal formatting from `884b2fa30` while keeping the same four-file boolean boundary. Against `upstream/master` `3a1c9e620`, it has `a=30` non-blank additions, `b=30` non-blank deletions, and penalty `60`. The earlier raw `+33/-30` report produced penalty `69`; the nine-point difference comes only from excluding three added blank lines. Under the new rule, the readable `884b2fa30` source already scores `60`, so this normalization claims no semantic or structural reduction over that version.

For comparison under the same non-blank-line rule, the generic-result candidates score `145` (`7dbe0e04b`: `a=58`, `b=29`) and `122` (`52eb801de`: `a=51`, `b=31`). The style-normalized boolean boundary therefore improves the penalty by `85` and `62` respectively without relying on formatting compression.

## 2026-07-15 Ad-hoc Case Boundary

The user retained the full sibling-bug scope but rejected the unified settlement helper as reviewer-hostile. The accepted replacement restores the upstream branch bodies and changes only the broken cases: add missing synchronous settlement to deception success, exhibition ignore, exhibition leave, and initial group conversion; preserve the existing JOIN, REFUSE, and INTERRUPT settlement calls.

Operation identity remains necessary because nested player updates can clear or replace the discoverer's behavior before the panel returns. A panel-instance `skip_outer_settlement` result is therefore set explicitly in only four already-settled non-`MOVE` cases: JOIN, DISCOVER, IGNORE, and INTERRUPT. Leaving reactions keep that field false; state-machine 40 then distinguishes their actual successor, returning false for `MOVE` so the NPC outer loop handles it and true for a no-route `WAIT` so no idle settlement is added. Successful hidden/exhibition conversion also keeps the field false so ordinary outer settlement remains unchanged. Ordinary state-machine 96 returns `None`, so its unrelated JOIN behavior is not suppressed.

The pre-`WAIT` normal-format implementation budget was `a=22`, `b=5`, penalty `61`, with 27 changed non-blank lines versus 60 in the shared-helper candidate. The approved `WAIT` boundary is one local replacement in state-machine 40 and does not infer ownership from behavior alone: the panel flag is still checked first, so nested DISCOVER or INTERRUPT updates remain suppressed even if they clear the behavior. A generic scheduler behavior-id check remains invalid because ordinary state-machine 96 assigns `JOIN_GROUP_SEX` without settling it locally.

Fable 5 passed the original ad-hoc boundary in `fable-ad-hoc-case-design-verdict-20260715.md` and resolved the interface wording in `fable-ad-hoc-case-design-followup-verdict-20260715.md`: state-machine 40 reads the public field after `draw()`, avoiding an unnecessary `draw()` return contract. Its later reassessment in `fable-discovery-wait-nonsettlement-reassessment-verdict-20260715.md` identified the `WAIT` fallback as a gameplay-semantic choice requiring maintainer confirmation. The user has now made that choice: only `MOVE` justifies the successor settlement; a no-route `WAIT` is skipped because the discovery response already gave the character sufficient visible presence.

## 2026-07-15 Maintainer-required `SPECIAL_FLAG` boundary

This section supersedes the boolean return pass-through above for the next PR revision. The maintainer confirmed the bug but rejected changing the return contract of `constant.handle_state_machine_data` for this special case.

The panel keeps an instance-local `discoverer_reaction_settled` boolean. Each existing explicit reaction branch sets it only after its local synchronous `judge_character_status()` call; the four previously missing reaction branches first receive that same call. The branch logic remains explicit and is not consolidated into a helper.

State-machine 40 leaves its return value unchanged. Only after `panel.draw()` completely returns does it copy the panel-local result to `character_data.sp_flag.see_h_reaction_settled`. This delay is required: H ending and initial group conversion run nested `game_update_flow()` calls while the panel callback is still active. A flag written inside the callback could be consumed or cleared by that nested NPC loop before the outer scheduler returns. The hidden-sex direct caller never receives this state-machine write, so it cannot leave a stale marker for a later NPC turn.

The NPC scheduler consumes the flag immediately after `find_character_target()`: it calls its original status settlement when the flag is false or the current behavior is `MOVE`, then clears the flag unconditionally. Thus an explicit reaction is not replayed, a real movement successor still progresses in the same NPC round, a no-route `WAIT` receives no extra idle settlement, and successful hidden/exhibition conversions retain the ordinary `SHARE_BLANKLY` settlement because their panel-local result remains false.

The active penalty rule is `(a + b) + S - 2U`, counting only non-blank production lines. The replaced return candidate is `a=22`, `b=5`, `S=4`, `U=0`, penalty `31`. The selected explicit-branch `SPECIAL_FLAG` shape is expected to be `a=21`, `b=1`, `S=7`, `U=0`, penalty `29`; recount the final diff rather than treating this estimate as proof.
