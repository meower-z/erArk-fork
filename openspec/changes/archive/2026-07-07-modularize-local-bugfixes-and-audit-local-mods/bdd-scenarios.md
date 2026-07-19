# BDD Verification Scenarios

Date: 2026-07-04

Follow-up audit note (2026-07-05): this file defines BDD scenarios. Unless evidence explicitly names a `ModManager.load_all_enabled_mods()` run or a dated manual game-flow run, "Automated unit coverage" means focused unit/script coverage, not full BDD execution.

Executable harness note (2026-07-06): `mod/tests/bdd/` now provides two executable BDD tiers, both run with `.venv/bin/pytest mod/tests/bdd/ -v` from the repo root on the Linux VPS:

1. **Web-mode end-to-end** (`web_game_driver.py` + `test_bdd_boot_and_flow.py`): boots a real `game.py` process (web_draw=1), drives title -> new game -> main scene -> a real instruct settlement over the HTTP+SocketIO API, and asserts all 13 enabled mods load with dependency order and `error.log` stays clean.
2. **Near-real in-process** (`near_real_boot.py`): mirrors game.py init through the real `Script/Core/mod_manager.py` against unmocked `Script` modules and real config data, then drives the actually-installed patched functions with real characters (design.md's near-real-game harness definition).

Evidence entries below dated 2026-07-06 refer to these suites (all passing on that date, VPS, branch codex/local-bugfix-audit-fixes).

## Template

- Scenario ID:
- Component:
- Setup:
- Enabled mods:
- Action:
- Expected state or visible result:
- Automation status:
- Evidence:

## LB-BDD-001: Group Target Context

- Scenario ID: LB-BDD-001
- Component: `local_group_target_context_fix`
- Setup: Enable only `local_group_target_context_fix`; put the player in group-sex mode with target `A`; run group AI for participant `B`.
- Enabled mods: `local_group_target_context_fix`
- Action: Execute normal group AI and type-3 group AI.
- Expected state or visible result: Player `target_character_id` is restored to `A` after each AI call, including when the upstream call mutates the target.
- Automation status: Automated unit coverage with restored fake modules; near-real live-save BDD + web full-flow smoke (2026-07-06).
- Evidence: `python mod/local_group_target_context_fix/tests/test_local_group_target_context_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_save_group_ai.py::test_group_ai_preserves_player_target` (real slot-99 group session, player target preserved through real npc_ai_in_group_sex); 2026-07-06 web `mod/tests/bdd/test_bdd_save_full_flow.py::test_group_ai_slice_settles_clean` (all 10 participants' group AI slice in a real process, clean error.log)

## LB-BDD-002: H Movement Interrupt

- Scenario ID: LB-BDD-002
- Component: `local_h_movement_interrupt_fix`
- Setup: Enable only `local_h_movement_interrupt_fix`; player is moving to another room, then H/group state becomes active during the movement tick.
- Enabled mods: `local_h_movement_interrupt_fix`
- Action: Run player movement, NPC active-H interruption, and group-H state-machine movement entry.
- Expected state or visible result: Stale move source, intermediate target, and final target are cleared; NPC active-H delegates upstream after setting move stop; group-H NPC movement is converted to wait.
- Automation status: Automated unit coverage; group-H state-machine movement entry near-real live-save BDD + web full-flow smoke (2026-07-06); player-move/npc-active-H routes remain unit-covered.
- Evidence: `python mod/local_h_movement_interrupt_fix/tests/test_local_h_movement_interrupt_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_save_group_ai.py::test_group_move_entry_converted_to_wait` (real slot-99 participant: move entry returns False, WAIT assigned, move plan cleared, over-marked)

## LB-BDD-003: Group Masturbation Intent

- Scenario ID: LB-BDD-003
- Component: `local_group_masturbation_intent_fix`
- Setup: Enable only `local_group_masturbation_intent_fix`; group-H participant has `masturebate == 3`.
- Enabled mods: `local_group_masturbation_intent_fix`
- Action: Run NPC target selection twice in the same player-action slice, then again after `over_behavior_character` changes.
- Expected state or visible result: `default91` runs once per player action; regenerated stale marker is cleared and the NPC is marked over for the current slice.
- Automation status: Automated unit coverage; near-real live-save BDD + web full-flow smoke (2026-07-06).
- Evidence: `python mod/local_group_masturbation_intent_fix/tests/test_local_group_masturbation_intent_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_save_group_ai.py::test_masturbation_intent_consumed_once_per_action_slice` (real slot-99 participant with masturebate==3: default91 routes into masturbation, second same-slice call clears intent and over-marks)

## LB-BDD-004: Group Participant Admission

- Scenario ID: LB-BDD-004
- Component: `local_group_participant_admission_fix`
- Setup: Enable only `local_group_participant_admission_fix`; exhausted or tired NPC discovers an ongoing group-sex scene.
- Enabled mods: `local_group_participant_admission_fix`
- Action: Open the sex-be-discovered panel draw path.
- Expected state or visible result: No invite/interrupt choice is shown; the discoverer receives `SEE_H_AND_LEAVE`, existing discovery effects run, and the panel returns to scene.
- Automation status: Automated unit coverage; near-real BDD for the group-start premise (2026-07-06); full UI draw remains manual BDD.
- Evidence: `python mod/local_group_participant_admission_fix/tests/test_local_group_participant_admission_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_group_admission.py` (real premise registry + real scene data, includes in-place demonstration of the upstream first-NPC-only defect)

## LB-BDD-005: Hypnosis Normal Flow

- Scenario ID: LB-BDD-005
- Component: `local_hypnosis_state_fix`
- Setup: Enable only `local_hypnosis_state_fix`; in normal scene flow, target has enough hypnosis degree and player default hypnosis type is none.
- Enabled mods: `local_hypnosis_state_fix`
- Action: Complete single-target hypnosis and choose mind-control from the manual type selector.
- Expected state or visible result: Target receives the corresponding hypnosis unconscious flag; player default hypnosis type remains none after the one-off manual selection.
- Automation status: Automated unit coverage; near-real BDD for state preservation through the real evaluate_hypnosis_completion (2026-07-06); manual full-flow BDD pending.
- Evidence: `python mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_hypnosis_state.py`

## LB-BDD-006: Hypnosis H-Mode Flow

- Scenario ID: LB-BDD-006
- Component: `local_hypnosis_state_fix`
- Setup: Enable only `local_hypnosis_state_fix`; in an H/instruction context, current target has enough hypnosis degree.
- Enabled mods: `local_hypnosis_state_fix`
- Action: Switch hypnosis type to mind control through `Chose_Hypnosis_Type_Panel.change_hypnosis_type`.
- Expected state or visible result: The current target immediately receives hypnosis unconscious flag `7`; mind-control option path executes; hypnosis-state talk bypasses the generic unconscious gate through the current hypnosis-state premise predicate.
- Automation status: Automated unit coverage plus manual H-flow BDD pending.
- Evidence: `python mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`

## LB-BDD-007: Pain As Pleasure

- Scenario ID: LB-BDD-007
- Component: `local_pain_as_pleasure_fix`
- Setup: Enable only `local_pain_as_pleasure_fix`; target has `pain_as_pleasure` enabled.
- Enabled mods: `local_pain_as_pleasure_fix`
- Action: Apply pain decrease, direct pain second effect, and hypnosis cancel.
- Expected state or visible result: Pain decrease remains pain; positive direct pain converts to psychological pleasure; hypnosis cancel clears the target flag.
- Automation status: Automated unit coverage; near-real BDD executed (2026-07-06).
- Evidence: `python mod/local_pain_as_pleasure_fix/tests/test_local_pain_as_pleasure_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_pain_as_pleasure.py` (real Script.Settle functions, real config data: positive-pain conversion, decrease-stays-pain, non-hypnosis gate, direct second-effect conversion, dead-character guard, hypnosis-cancel clear)

## LB-BDD-008: H Orgasm Batch Achievement Path

- Scenario ID: LB-BDD-008
- Component: `local_h_orgasm_batch_fix`
- Setup: Enable only `local_h_orgasm_batch_fix`; create repeated or multi-part orgasm settlement that reaches achievement id `1221`.
- Enabled mods: `local_h_orgasm_batch_fix`
- Action: Run `orgasm_settle` through the batch wrapper for repeated/multi-part orgasm effects.
- Expected state or visible result: Batch settlement flushes second behaviors once, translation helper remains available, and achievement flow receives `("绝顶", 1221)` without runtime error.
- Automation status: Automated unit coverage for the playtest traceback path; web full-flow on the real crash-report save (2026-07-06).
- Evidence: `python mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py`; 2026-07-06 web `mod/tests/bdd/test_bdd_save_full_flow.py::test_group_sex_end_full_settlement` — the original playtest crash state (slot 99: ~160-entry player must_settle backlog, 凯尔希 orgasm_edge=2 with 5 pending part-23 counts, live mid-settlement second behaviors) settles through the real batch path with clean error.log

## LB-BDD-009: Group Edge Release

- Scenario ID: LB-BDD-009
- Component: `local_group_edge_release_fix`
- Setup: Enable `local_h_orgasm_batch_fix` and `local_group_edge_release_fix`; participants have pending edge counts before group cleanup.
- Enabled mods: `local_h_orgasm_batch_fix`, `local_group_edge_release_fix`
- Action: Run group end, single NPC exit, group-to-H transition, and unconscious recovery paths.
- Expected state or visible result: Pending edge counts release before participant/template cleanup; generated second effects flush; stale template-only non-H participants are cleanup-only and not included in summaries or live orgasm settlement; batch settlement is not interrupted.
- Automation status: Automated unit coverage; near-real live-save effect-529 release semantics + web full-flow group end (2026-07-06).
- Evidence: `python mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py`; 2026-07-06 near-real `mod/tests/bdd/test_bdd_save_group_edge_release.py` (real slot-99 state: releases exactly the five edge==1 participants with pending counts, per-count settlement plus >=3-count bonus orgasm, edge==2/no-count participants untouched); 2026-07-06 web `mod/tests/bdd/test_bdd_save_full_flow.py::test_group_sex_end_full_settlement`

## LB-BDD-010: Dependency Failure And Ordering

- Scenario ID: LB-BDD-010
- Component: Mod loader
- Setup: Enable a dependent mod without its dependency, then enable both with the dependent before the dependency in `load_order`; also exercise enabled-missing, duplicate `mod_id`, and failed-load rollback cases.
- Enabled mods: Synthetic dependency harness mods.
- Action: Load all enabled mods through `ModManager`.
- Expected state or visible result: Missing dependency produces `缺少依赖mod`; enabled-missing and duplicate IDs produce collected diagnostics; failed mods roll back declared global mutations; enabled dependency loads before dependent; unrelated mods preserve configured relative order.
- Automation status: Automated loader harness; real-game boot BDD executed (2026-07-06).
- Evidence: `python mod/tests/test_mod_manager_dependencies.py`; 2026-07-06 web-mode `mod/tests/bdd/test_bdd_boot_and_flow.py::test_all_enabled_mods_load_in_real_game` (real game.py process: all 12 enabled mods report 成功加载, dependency loads before dependent, no 加载失败) plus `test_new_game_reaches_main_scene` / `test_instruct_settlement_advances_game_time` (real settlement loop, clean error.log)

## LB-BDD-011: Local Performance Wait Flow

- Scenario ID: LB-BDD-011
- Component: `local_performance`
- Setup: Enable only `local_performance`; populate stale queued input and residual mouse flags before a normal Tk wait.
- Enabled mods: `local_performance`
- Action: Run `patched_askfor_wait`, then simulate the next panel reading its command queue.
- Expected state or visible result: Stale input is drained before the wait; fresh next-panel input remains available and is not swallowed; dynamic web mode delegates upstream; benchmark mode returns immediately.
- Automation status: Automated unit coverage for current queue behavior; generation-token input invariant remains out of scope unless the queue protocol is broadened.
- Evidence: `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`

## LB-BDD-012: Cross-Platform Save Loading

- Scenario ID: LB-BDD-012
- Component: `local_cross_platform_save_fix`
- Setup: A save created on a platform with a different `os.sep` (e.g. the user's Windows playthrough saves) is loaded on this platform; live cache is a fresh boot.
- Enabled mods: `local_cross_platform_save_fix` (discovered live: without it, `update_map` deletes all foreign-separator scene keys and substitutes fresh empty scenes, wiping every character's scene registration; `group_sex_end` then crashes with `list.remove(x): x not in list`).
- Action: Load the save through real `input_load_save` (near-real tier) and through the full title-screen UI in a real game process (web tier), then run instructs.
- Expected state or visible result: Scene/map keys and `scene_path`/`map_path`, dormitory fields, `dormitory_admin_target_room`, `air_hypnosis_position`, facility damage keys and maintenance places are normalized to the current platform separator; scene `character_list` registrations survive; native saves load byte-identical (no dict rebuild); `error.log` stays clean.
- Automation status: Automated near-real BDD (synthetic foreign-separator save + real Windows slot-99 crash-report save, the latter skipped when `save/` absent); isolated unit tests; web full-flow reproduction and post-fix verification executed 2026-07-06.
- Evidence: `python3 -B mod/local_cross_platform_save_fix/tests/test_local_cross_platform_save_fix_mod.py`; 2026-07-06 `mod/tests/bdd/test_bdd_save_cross_platform.py` (6 tests, failing-first before the mod); 2026-07-06 web-driver session on slot 99: pre-fix `group_sex_end` failed with `list.remove(x): x not in list`, post-fix load -> wait -> group_sex_end -> rest all settle with clean error.log.

## Save fixture map (transferred playthrough, inventoried 2026-07-06)

All slots are one 博士 playthrough (354 characters, 27 recruited). Only slot 99 holds a live H/group state.

| Slot | In-game time | State highlights | Scenario use |
| --- | --- | --- | --- |
| 99 | 2019-12-29 11:52, ver 2026.6.30-4 | group_sex_mode on; player + 10 NPC in 动力/人力发电室, all is_h + masturebate(418); template empty, lock on, npc_ai_type=1; 凯尔希 orgasm_edge=2 + counts {23:5}, 陈 {4:1,23:3}, 特蕾西娅 {23:3}, 可露希尔/食铁兽/清流 {23:1}, 杜宾/诗怀雅/林/小满 edge=1 no counts; player must_settle backlog ~160 orgasm entries; 9/10 pain_as_pleasure via 全员催眠增强 | LB-BDD-008/009 primary; LB-BDD-001/002/003 live group AI; cross-version + cross-platform load (LB-BDD-012) |
| 6 | 2020-03-03 13:50 | player + 6 NPC in 贸易/七城风情餐厅; unconscious_h=7 on 可露希尔/华法琳/司霆惊蛰/林/小满; 阿米娅 pain_as_pleasure outside H | LB-BDD-005/006 full flow; R2 evidence |
| 7 | 2020-03-03 17:32 | player alone; 阿米娅 pain_as_pleasure in 关押/休息室 exercise; 5 NPC keep unconscious_h=7 | R2 cross-mod evidence |
| 8 | 2020-03-05 07:15 | followers 可露希尔+九 with player in 中枢/休息室 | group-sex START (F4 full-UI); fresh group builder |
| 9 | 2020-03-05 20:49 | follower 惊蛰 (wait) with player | single-target H start, LB-BDD-002 |
| 0/5/1/2/3/4/auto | 2020-03-03 → 03-09 | quiet states with one companion each | spares / latest chain |
