/investigate-game-bug

Review the final PR #212 implementation after it was freshly ported onto current upstream/master 3a1c9e620. Return exactly PASS or REVISE first, followed by concise reasons. Do not propose broader cleanup.

Bug contract:
1. With pain-as-pleasure active, only a positive, already source-adjusted pain delta is converted to psychological pleasure.
2. Zero/negative pain must remain on state 17 so pain can fall normally.
3. Direct positive pain writers (small/middle/large pain and extra orgasm) must not bypass conversion.
4. Psychological ability scaling must be applied exactly once by canonical state-23 settlement, not in the helper.
5. Existing common-path continuous-repeat tuning is intentionally unchanged. A direct writer enters state 23 once, so it receives only state-23 tuning.
6. If canonical state 23 declines settlement because the target sleeps or is unconscious, the helper still reports handled; callers must not fall back to state 17.
7. Extra orgasm always settles terror, clears the counter, and chooses text matching whether pain was converted.

Implementation on latest upstream:
- common_default.py adds try_settle_pain_as_pleasure(character_id, pain_value, change_data=None, change_data_to_target_change=None) -> bool.
- It returns False when pain_value <= 0 or hypnosis is inactive. Otherwise it calls base_chara_state_common_settle exactly once with state_id=23, base_value=0, ability_level=character_data.ability[36], tenths_add=False, forwards both change records, then returns True.
- base_chara_state_common_settle replaces its unconditional state-17 recursion with: if state_id == 17 and try_settle_pain_as_pleasure(character_id, final_value, change_data, change_data_to_target_change): return.
- Second_effect.py imports the helper. handle_add_small_pain, handle_add_middle_pain, and handle_add_large_pain call it after their existing source-specific mark/current-pain formula; True returns before direct state-17 writes.
- handle_extra_orgasm calls the helper for extra_pain; False keeps the old state-17 write. Terror settlement and counter reset are unconditional. Text says psychological pleasure and terror on True, pain and terror on False.

Verification against this exact latest-upstream worktree:
- 28 focused production-function tests passed. They cover signed common deltas, active/inactive flags, both change-record forms, small/middle/large writers, extra-orgasm terror/text/reset, canonical state-23 call count, and sleep/unconscious handled-without-fallback behavior.
- Both production files compile; git diff --check passes.
- Static helper calls are only the active-premise check and canonical base_chara_state_common_settle; it does not call chara_feel_state_adjust itself.
- Mutation search found no other direct positive state-17 production writer; originium_arts only resets state 17.

Assess correctness, ownership, accidental double calculation, missing bypasses, and whether fresh Tk A/B evidence should contain two groups: (A) negative common pain reduction with conversion active, and (B) a direct positive pain source with conversion active, baseline adds state 17 while candidate adds state 23.
