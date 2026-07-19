## Context

This is a retrospective OpenSpec sync for local mods that existed before OpenSpec was initialized. The active local mod load order is:

1. `easy_mode`
2. `local_bugfix`
3. `group_sex_extension`
4. `local_fontfix`
5. `local_performance`

The notes below emphasize when a bug occurred, what was observed, the inferred cause, and how the local mod fixes it. Where automated tests exist, the verification command is listed.

## local_bugfix

### Group-mode auto-fill leaks the player's interaction target

- Bug context: During group-mode AI auto-fill, NPC selection temporarily changes the player's `target_character_id`.
- Observed symptom: The visible interaction target and the settlement target could diverge. One recorded abnormal case applied a large pain/terror/mark result to a character who was not the visible target.
- Cause: `npc_ai_in_group_sex()` and `npc_ai_in_group_sex_type_3()` temporarily assign `cache.character_data[0].target_character_id` while filtering candidate group positions, but upstream code did not restore the previous value.
- Fix: `patched_npc_ai_in_group_sex()` and `patched_npc_ai_in_group_sex_type_3()` wrap the upstream calls with `_call_with_preserved_player_target()`, restoring the old player target in a `finally` block even if the upstream call raises.
- Verification: `python mod/local_bugfix/tests/test_local_bugfix_mod.py` covers both wrappers and the exception path.

### Group-mode H-state NPCs leave the scene or continue ordinary movement

- Bug context: NPCs in group-mode H state could enter ordinary movement flows.
- Observed symptom: Characters participating in the group-mode scene could leave to eat, move, or continue a previous route.
- Cause: The normal movement state machine did not treat group-mode H state as a forced stop condition, and already-moving NPCs could keep their movement targets.
- Fix: `patched_general_movement_module()` and `patched_character_continue_move()` call `_stop_group_sex_h_move()` before upstream movement. The helper clears movement targets, sets the NPC back to `WAIT`, and anchors the target to itself.
- Verification: Manually verified in group-mode scenes; no automated movement fixture exists yet.

### Group-mode masturbation marker is set but not executed

- Bug context: Group-mode AI type "only masturbate" or "fill empty slots, otherwise masturbate" can set `sp_flag.masturebate = 3`.
- Observed symptom: Some NPCs entered the intended marker state but then stood idle instead of executing the action.
- Cause: H-state NPCs do not naturally continue through the normal target-finding path that consumes the marker. Upstream `judge_character_h_obscenity_unconscious()` also returned immediately after group AI, so the marker could remain without reaching the formal target.
- Fix: `patched_judge_character_h_obscenity_unconscious()` only returns immediately after group AI when the marker is present, and `patched_find_character_target()` routes marked group-mode H NPCs directly to `default91` so the formal action can settle and clear the state.
- Verification: Manually verified in group-mode scenes; the marker routing is noted for a future fake-target registry test.

### Player movement survives H/group-mode interruption

- Bug context: The player can be interrupted by H-state or group-mode state while moving.
- Observed symptom: The old destination and movement path could remain after the interruption, causing panel/state mismatch or continued movement toward a stale target.
- Cause: `own_charcter_move()` advanced toward the target scene without a shared interruption check for `move_stop`, `is_h`, or `group_sex_mode`.
- Fix: `patched_own_charcter_move()` calls `_stop_player_move_if_interrupted()` before and after each movement step. The helper clears `move_target` and `move_final_target` and stops the loop.
- Verification: Manually verified by interrupting movement during H/group-mode transitions.

### Tired/sleep status is stale at group-mode boundaries

- Bug context: Group-mode H/follow NPCs can cross tired or sleep thresholds while locked into special states.
- Observed symptom: NPCs near fatigue boundaries could keep stale state and drift back toward ordinary behavior.
- Cause: Upstream tired/sleep judgement can finish without a second status settlement pass for group-mode H/follow edge cases.
- Fix: `patched_judge_character_tired_sleep()` records whether the NPC needs status rejudgement, calls upstream, then invokes `character_behavior.judge_character_status()` when the group-mode fatigue condition is met.
- Verification: Manually verified around fatigue thresholds; an automated fixture is still pending.

### NPC active-H does not cancel the player's current move

- Bug context: An NPC can trigger active-H while the player still has a movement final target.
- Observed symptom: After active-H begins, the player may still carry the old movement destination.
- Cause: `npc_active_h()` assigns a new behavior and advances time without clearing `move_final_target`.
- Fix: `patched_npc_active_h()` calls `_stop_player_move_on_h_interrupt()` after selecting the active-H behavior and before starting the new player behavior.
- Verification: Manually verified by triggering active-H while the player had a pending movement route.

### Pain-as-pleasure leaks, reverses, or is bypassed

- Bug context: The hypnosis `pain_as_pleasure` flag changes how pain settlement should be interpreted.
- Observed symptoms: The flag could remain after hypnosis cancellation; pain decreases could incorrectly reduce psychological pleasure; direct second effects could still add pain while the flag was active.
- Causes: `handle_hypnosis_cancel()` did not clear `pain_as_pleasure`; common settlement treated pain changes without distinguishing positive from negative final deltas; some second effects wrote directly to `status_data[17]` and bypassed common settlement.
- Fix: `patched_handle_hypnosis_cancel()` clears the target's `pain_as_pleasure`. `patched_base_chara_state_common_settle()` temporarily disables the flag for non-positive pain changes. `patched_handle_add_small_pain()`, `patched_handle_add_middle_pain()`, `patched_handle_add_large_pain()`, and `patched_handle_extra_orgasm()` route direct positive pain through psychological pleasure settlement instead.
- Verification: `python mod/local_bugfix/tests/test_local_bugfix_mod.py` covers cancellation, negative pain settlement, direct conversion, and small-pain second effect conversion.

## group_sex_extension

- Adds three group-mode arts commands: "全员寸止", "全员戴上玩具", and "全员催眠增强".
- "全员寸止" enables edge mode for every NPC discovered in the current group-mode context.
- "全员戴上玩具" ensures body item slots `0`, `1`, `2`, and `3` exist and equips them when missing.
- "全员催眠增强" only appears when at least two group-mode NPCs are completely hypnotized, where complete hypnosis means talent `73` or hypnosis degree `>= 200`.
- The hypnosis boost sets `increase_body_sensitivity` and `pain_as_pleasure` without changing the current hypnosis state or unconscious flag.
- Verification: `python mod/group_sex_extension/tests/test_group_sex_extension_mod.py` covers the visibility condition and non-destructive hypnosis boost.

## easy_mode

- Replaces hypnosis progress calculation so the random multiplier changes from upstream `0.5..1.5` to local `5..10`, while retaining the existing capability ceiling and player/target modifiers.
- Replaces sanity max growth so daily sanity cost grows max sanity by `round(today_cost)` instead of upstream `round(today_cost / 50)`, still capped at `9999`.
- Replaces hotel room booking flow so room prices change from upstream `[2, 10, 100]` to `[1, 2, 3]`, while retaining checkout time and room rewards.
- This is tuning rather than a bug fix; no automated tests were found for `easy_mode`.

## local_fontfix

- Bug context: Desktop Tk mode depends on the bundled Sarasa font, but Windows may not have that font installed globally.
- Observed symptom: The UI can fall back to SimSun or another default font, causing poorer Chinese alignment and rendering.
- Cause: Tk resolves configured font families before bundled files are available to the Windows font table.
- Fix: `local_fontfix` scans `static/fonts` and `fonts` under likely runtime roots, then calls `AddFontResourceExW(..., FR_PRIVATE, 0)` for `.ttf`, `.otf`, and `.ttc` files. Registration is process-private and does not install fonts system-wide.
- Verification: `python mod/local_fontfix/tests/test_local_fontfix_mod.py --mod-root mod/local_fontfix` covers supported file registration and Sarasa availability to Tk on Windows.

## local_performance

### Tk queue rendering repeatedly scrolls to the end

- Bug context: Normal draw mode drains many small draw fragments into Tk.
- Observed symptom: Every operation could feel slow because each fragment and button requested `see(END)`.
- Cause: Upstream rendering forced scroll-to-end repeatedly during a single queue drain.
- Fix: `patched_read_queue()` temporarily defers `main_frame.see_end()` calls, drains the upstream queue renderer, then performs one final scroll and `update_idletasks()`.
- Verification: `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance` checks repeated scroll calls coalesce into one final call.

### WaitDraw consumes stale click/enter input

- Bug context: A command click can still be propagating when the following settlement output reaches its trailing wait.
- Observed symptom: The wait prompt may auto-advance without fresh player input.
- Cause: Queued empty input or a stale mouse-up state remained when `askfor_wait()` was armed.
- Fix: `patched_askfor_wait()` drains pending orders, clears `w_frame_up`, waits briefly before arming the wait, drains again, and then waits for fresh input. It also preserves web mode, benchmark mode, and active right-click skip behavior.
- Verification: `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance` covers stale queue input and right-click skip.
