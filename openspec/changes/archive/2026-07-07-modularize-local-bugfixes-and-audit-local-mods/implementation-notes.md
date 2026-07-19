# Implementation Notes

Date: 2026-07-04

## Ultracode Status

Ultracode was attempted for the initial multi-lane audit. The first run failed with `spawn EPERM`; a retry using the npm Codex wrapper failed with `spawn EINVAL`; a shim retry was rejected by the approval reviewer because worker subprocesses would send repository context to the external Codex service. No Ultracode worker evidence was produced. The repo-local OpenSpec audit below is therefore based on direct source inspection and local test runs.

## Scope Control

Task 1.1 confirms this change excludes the deferred UI panel stability work. The active modularization proposal explicitly excludes title screen, save-list, settings-panel, and disabled-AI-dialogue UI bugs in `proposal.md:34`, while the sibling `fix-playtest-corner-case-regressions` now contains only `ui-panel-stability`.

Task 1.6 trimmed the sibling change:

- Removed `specs/local-bugfixes/spec.md` and `specs/h-orgasm-settlement/spec.md`.
- Removed hypnosis and H orgasm batch tasks from `tasks.md`.
- Removed `local-bugfixes` and `h-orgasm-settlement` modified capabilities from the sibling proposal.
- Revalidated with `openspec validate "fix-playtest-corner-case-regressions" --type change --strict`: pass.
- Verified no absorbed keywords remain in that sibling change with `rg -n "hypnosis|催眠|orgasm|绝顶|local_bugfix|local-bugfix|h-orgasm|error\.log" openspec/changes/fix-playtest-corner-case-regressions`: no matches.

## Baseline Mod Config

Task 1.4 baseline `mod/mod_config.json`:

- `enabled_mods`: `easy_mode`, `local_bugfix`, `group_sex_extension`, `local_fontfix`, `local_performance`.
- `load_order`: `easy_mode`, `local_bugfix`, `group_sex_extension`, `local_fontfix`, `local_performance`.

This matters because `local_bugfix` must later be replaced by split components without changing default local behavior.

## Baseline Tests

Task 1.5 baseline commands and results:

- `python mod/local_bugfix/tests/test_local_bugfix_mod.py`: pass.
- `python mod/local_bugfix/tests/test_group_sex_edge_release_mod.py`: pass.
- `python mod/local_bugfix/tests/test_h_orgasm_batch_mod.py`: pass.
- `python mod/group_sex_extension/tests/test_group_sex_extension_mod.py`: pass.
- `python mod/local_performance/tests/test_local_performance_mod.py`: requires `--mod-root`; raw command fails with argparse `--mod-root` missing.
- `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`: pass.
- `python mod/local_fontfix/tests/test_local_fontfix_mod.py`: requires `--mod-root`; raw command fails with argparse `--mod-root` missing.
- `python mod/local_fontfix/tests/test_local_fontfix_mod.py --mod-root mod/local_fontfix`: pass.

Environment assumption: tests run under the workspace Python 3.12 on Windows from repo root.

## Local Bugfix Inventory

Task 1.2 inventory:

- Manifest `mod/local_bugfix/mod_info.json` declares `dependencies: []`, `incompatible: []`, `load_priority: 10`.
- Manifest replacements in `scripts/local_bugfix.py`: `judge_character_tired_sleep`, `find_character_target`, `own_charcter_move`, `judge_character_h_obscenity_unconscious`, `npc_active_h`, `npc_ai_in_group_sex`, `npc_ai_in_group_sex_type_3`, `recover_from_unconscious_h`.
- Manifest replacements in `scripts/h_orgasm_batch.py`: `check_second_effect`, `orgasm_settle`, `store_power_by_human_power`.
- Manifest new registration: `local_bugfix_is_orgasm_batch_settling` registered to `Script.Design.second_behavior`.
- Hidden import-time registry patches are installed by `_install_registry_patches()` at `mod/local_bugfix/scripts/local_bugfix.py:1358`: base state settlement, hypnosis cancel, group edge release, pain second effects, sex discovered panel draw, hypnosis panel method, hypnosis-one effect, talk premise weighting, state-machine movement handlers.
- Hidden registry targets include `common_default.base_chara_state_common_settle` and imported aliases at `mod/local_bugfix/scripts/local_bugfix.py:1184`, `settle_behavior_effect_data` entries for hypnosis cancel/one and group/end H HP/MP max at `mod/local_bugfix/scripts/local_bugfix.py:1204`, `mod/local_bugfix/scripts/local_bugfix.py:1218`, `mod/local_bugfix/scripts/local_bugfix.py:1246`, second-effect pain handlers at `mod/local_bugfix/scripts/local_bugfix.py:1271`, `Sex_Be_Discovered_Panel.draw` at `mod/local_bugfix/scripts/local_bugfix.py:1290`, `Chose_Hypnosis_Type_Panel.change_hypnosis_type` at `mod/local_bugfix/scripts/local_bugfix.py:1345`, and state-machine movement handlers at `mod/local_bugfix/scripts/local_bugfix.py:1378`.
- README headings are: player target preservation, H-state movement/leave, auto masturbation marker routing, repeated auto masturbation settlement, tired discovery auto-leave, player move interruption, tired/sleep rejudge, NPC active-H move interruption, pain-as-pleasure consistency, and H multi-orgasm batch.
- README omits separate headings for hypnosis mode persistence/talk gate, group edge release, and upstream reimplementation drift, all of which are real code/test surfaces.

## Feature Mod Inventory

Task 1.3 inventory:

- `group_sex_extension` manifest declares no dependencies and no manifest functions; all registration occurs at import from `_install_patch()` in `mod/group_sex_extension/scripts/group_sex_extension.py:314`.
- `group_sex_extension` registers custom premise `group_sex_extension_complete_hypnosis_ge_2` at `mod/group_sex_extension/scripts/group_sex_extension.py:325`.
- It registers three commands through `_register_instruction()`: `group_sex_extension_edge_all`, `group_sex_extension_equip_toys_all`, and `group_sex_extension_hypnosis_boost_all` at `mod/group_sex_extension/scripts/group_sex_extension.py:326`.
- Current tests cover only hypnosis boost visibility and flag application without state mutation at `mod/group_sex_extension/tests/test_group_sex_extension_mod.py:39` and `mod/group_sex_extension/tests/test_group_sex_extension_mod.py:57`.
- `local_performance` manifest replaces `Script.Core.main_frame.read_queue` and `Script.Core.flow_handle.askfor_wait`, with no dependencies and `load_priority: 20`.
- `local_performance` script drains stale input via `_drain_pending_orders()` at `mod/local_performance/scripts/local_performance.py:11`, coalesces `read_queue` scroll calls at `mod/local_performance/scripts/local_performance.py:36`, delegates web mode at `mod/local_performance/scripts/local_performance.py:83`, skips benchmark wait at `mod/local_performance/scripts/local_performance.py:85`, and drains stale input around Tk waits at `mod/local_performance/scripts/local_performance.py:92`.
- `local_performance` tests cover queue flushing, stale click/button input, residual right-click/mouse state, web delegation, benchmark return, late input cleanup, next-panel safety, and consecutive waits from `mod/local_performance/tests/test_local_performance_mod.py:63` through `mod/local_performance/tests/test_local_performance_mod.py:383`.

## Root-Cause Audit Matrix

Task 2.1 matrix and tasks 2.2-2.12 decisions:

| Behavior | Patch points | Tests / reproduction evidence | Root cause / invariant | Candidate component |
| --- | --- | --- | --- | --- |
| Group-mode player target preservation | `patched_npc_ai_in_group_sex()` and `patched_npc_ai_in_group_sex_type_3()` at `mod/local_bugfix/scripts/local_bugfix.py:1160`; upstream targets at `Script/Design/handle_npc_ai_in_h.py:556` and `Script/Design/handle_npc_ai_in_h.py:627` | Target restore tests at `mod/local_bugfix/tests/test_local_bugfix_mod.py:93`, `:111`, `:128` | Group AI may temporarily change player target for premise filtering; transient target must not leak after AI calculation. | `local_group_target_context_fix` |
| Player/NPC stale movement interruption | `_stop_player_move_if_interrupted()` at `mod/local_bugfix/scripts/local_bugfix.py:466`, `_stop_player_move_on_h_interrupt()` at `:476`, `_stop_group_sex_h_move()` at `:486`, `patched_own_charcter_move()` at `:1030`, `patched_npc_active_h()` at `:1154`, state-machine movement wrappers at `:1172` and `:1178` | NPC active-H test at `mod/local_bugfix/tests/test_local_bugfix_mod.py:148`; helper coverage at `mod/local_bugfix/tests/test_group_sex_edge_release_mod.py:714` | Movement plans must be cancelled when H/group state becomes the active state. This is a stale movement lifecycle invariant across player movement, NPC active-H, and group H movement. | `local_h_movement_interrupt_fix` |
| Group auto masturbation marker routing and repeated settlement | `patched_find_character_target()` at `mod/local_bugfix/scripts/local_bugfix.py:986`, marker helpers at `:508`, `:529`, `:542`, `:547`; upstream writes `masturebate = 3` at `Script/Design/handle_npc_ai_in_h.py:586`, `:621`, `:707` | Tests at `mod/local_bugfix/tests/test_local_bugfix_mod.py:381`, `:436`, `:506`, `:569` | `masturebate == 3` is an intent marker, not an idempotent behavior marker; it must route to `default91` once per player action and clear stale/regenerated markers. | `local_group_masturbation_intent_fix` |
| Tired group-sex discovery auto-leave | `_should_auto_leave_group_sex_discovery()` at `mod/local_bugfix/scripts/local_bugfix.py:601`, `_auto_leave_group_sex_discovery()` at `:624`, `patched_sex_be_discovered_draw()` at `:1024`; upstream panel class at `Script/System/Sex_System/sex_be_discovered_panel.py:31` | Tests at `mod/local_bugfix/tests/test_local_bugfix_mod.py:613`, `:639`, `:699`, `:755` | Group-sex participant admission must reject exhausted/tired discoverers instead of offering invite/interrupt choices that can re-enter or disrupt the group. | `local_group_participant_admission_fix` |
| Group tired/sleep rejudge | `patched_judge_character_tired_sleep()` at `mod/local_bugfix/scripts/local_bugfix.py:955`; upstream at `Script/Design/handle_npc_ai.py:38` | Existing helper coverage at `mod/local_bugfix/tests/test_group_sex_edge_release_mod.py:714` plus edge-transition tests below | After upstream tired/sleep judgment, group H/follow state may still require status settlement and pending edge release before cleanup. This touches group lifecycle but has edge-release hooks. | Owned by `local_group_edge_release_fix` when pending-edge cleanup is involved; otherwise kept as `local_group_participant_admission_fix` helper coverage. |
| Hypnosis mode persistence and talk gate | `_apply_current_hypnosis_state()` at `mod/local_bugfix/scripts/local_bugfix.py:726`, `patched_handle_hypnosis_one()` at `:833`, `patched_change_hypnosis_type()` at `:1302`, `patched_get_weight_from_premise_dict()` at `:820`; upstream hypnosis panel at `Script/UI/Panel/hypnosis_panel.py:280` and premise weighting at `Script/Design/handle_premise/__init__.py:197` | Tests at `mod/local_bugfix/tests/test_local_bugfix_mod.py:179`, `:203`, `:233`, `:819`, `:890`, `:955`; H orgasm batch second-talk gate tests at `mod/local_bugfix/tests/test_h_orgasm_batch_mod.py:719`, `:735`, `:803` | Chosen high-level hypnosis mode must persist independently of submenu exits, and hypnosis unconscious flags need a scoped talk-gate bypass without affecting ordinary unconscious states. | `local_hypnosis_state_fix` |
| Pain-as-pleasure consistency | `patched_base_chara_state_common_settle()` at `mod/local_bugfix/scripts/local_bugfix.py:667`, `patched_handle_hypnosis_cancel()` at `:697`, direct pain conversion at `:644`, second-effect wrappers at `:883`, `:896`, `:909`, `:920`; upstream at `Script/Settle/common_default.py:154`, `Script/Settle/default.py:1552`, `Script/Settle/Second_effect.py:1225`, `:1817`, `:2605`, `:3168` | Tests at `mod/local_bugfix/tests/test_local_bugfix_mod.py:256`, `:275`, `:310`, `:354` | Pain-as-pleasure must affect positive pain increases only, clear on hypnosis cancel, and also apply to direct second-effect pain paths that bypass common settlement. | `local_pain_as_pleasure_fix` |
| Group pending edge release before H reset | Group participant collection at `mod/local_bugfix/scripts/local_bugfix.py:82`, `:92`, `:119`; release helpers at `:367`, `:395`, `:419`; wrappers at `:853`, `:861`, `:869`, `:955`; upstream recover/end effects at `Script/Design/handle_npc_ai_in_h.py:155`, `Script/Settle/default.py:6726`, `Script/Settle/default.py:6792` | Tests at `mod/local_bugfix/tests/test_group_sex_edge_release_mod.py:297`, `:324`, `:368`, `:396`, `:425`, `:453`, `:476`, `:502`, `:626`, `:653`, `:686` | Pending edge counters and generated second effects must be flushed before group participants are removed, unconscious recovery clears state, or group-to-H transitions reset templates. | `local_group_edge_release_fix`; depends on `local_h_orgasm_batch_fix` for batch-flush coordination. |
| H orgasm batch settlement | `OrgasmBatch` and helpers in `mod/local_bugfix/scripts/h_orgasm_batch.py:156`; exported state hook at `:203`; replacements at `:491`, `:522`, `:650`; upstream targets at `Script/Design/second_behavior.py:46`, `Script/Design/second_behavior.py:371`, `Script/UI/Panel/manage_power_system_panel.py:196` | Tests at `mod/local_bugfix/tests/test_h_orgasm_batch_mod.py:48`, `:62`, `:93`, `:164`, `:239`, `:338`, `:447`, `:544`, `:676`, `:719`, `:735`, `:803`, `:871`; playtest traceback in `error.log:56`/`:58` | Same settlement tick can produce repeated/multi-part orgasm effects; display, queue clearing, remote draw suppression, human-power aggregation, second-talk bypass, tired/sleep deferral, and achievement helper binding must stay coherent for one batch. | `local_h_orgasm_batch_fix` |

## Historical / Unreproduced Symptoms

Task 2.10 record:

- The old README's manual-only symptoms for group H movement, player movement interruption, tired/sleep rejudge, and NPC active-H interruption are not all reproduced through a full game flow in this session.
- Automated baseline tests do exercise parts of those invariants: NPC active-H move clearing at `mod/local_bugfix/tests/test_local_bugfix_mod.py:148`, stale move helper and tired-sleep delegation at `mod/local_bugfix/tests/test_group_sex_edge_release_mod.py:714`, and tired discovery auto-leave at `mod/local_bugfix/tests/test_local_bugfix_mod.py:613`.
- The retained guards remain justified because upstream patch points still lack local cleanup hooks in the inspected functions, and later BDD tasks must decide which flows need manual evidence.

## Reimplementation Drift

Task 2.11 record:

- `patched_judge_character_h_obscenity_unconscious()` at `mod/local_bugfix/scripts/local_bugfix.py:1068` is a broad copy of upstream `judge_character_h_obscenity_unconscious()` at `Script/Design/handle_npc_ai_in_h.py:34`.
- The visible local delta is the group-mode `masturebate == 3` early return around `mod/local_bugfix/scripts/local_bugfix.py:1134`; upstream returns after group AI without that guard around `Script/Design/handle_npc_ai_in_h.py:129`.
- Resync strategy: replace the broad copy with a narrow wrapper or a small extracted helper during component migration, and add a focused test proving group-mode auto masturbation survives the H unconscious gate.
- Other wrappers mostly call originals and patch registries rather than fully reimplementing upstream functions; `patched_own_charcter_move()` is another larger body and should be reviewed when extracting `local_h_movement_interrupt_fix`.

## Final Component Boundaries

Task 2.12 boundary list:

1. `local_group_target_context_fix`: no dependencies; owns player target preservation around group AI.
2. `local_h_movement_interrupt_fix`: no dependencies; owns stale movement cleanup across player move, NPC active-H, and group H movement state machine hooks.
3. `local_group_masturbation_intent_fix`: no dependencies; owns group auto-masturbation marker routing and per-player-action consumption.
4. `local_group_participant_admission_fix`: no dependencies; owns tired/exhausted group-sex discoverer auto-leave and participant admission guard.
5. `local_hypnosis_state_fix`: no dependencies; owns hypnosis mode persistence and hypnosis-state talk-gate bypass.
6. `local_pain_as_pleasure_fix`: no dependencies; owns hypnosis cancel cleanup, positive-only pain conversion, and direct pain second-effect conversion.
7. `local_h_orgasm_batch_fix`: no dependencies; owns H orgasm batch settlement and exposes a documented batch-flush state hook.
8. `local_group_edge_release_fix`: declares dependency on `local_h_orgasm_batch_fix`; owns pending edge release before group/H cleanup and uses the batch hook instead of hidden imports.

`group_sex_extension` and `local_performance` stay unsplit feature mods. `local_fontfix` is baseline-only for this change unless default full-suite verification finds an interaction.

## Dependency and Loader Verification

Tasks 3.1-3.5 results:

- Added a loader smoke/dependency harness at `mod/tests/test_mod_manager_dependencies.py`.
- The harness provides `enable_only_with_dependencies(manager, mod_id)` so a test can enable exactly one target mod plus declared dependencies, excluding unrelated local mods.
- Verified pre-change behavior from `Script/Core/mod_manager.py`: `ModInfo` reads `dependencies`, `incompatible`, and `load_priority`, but the old `get_sorted_enabled_mods()` only used `mod_config.json` `load_order` followed by enabled leftovers. No dependency or incompatible diagnostic existed.
- Implemented narrow dependency diagnostics in `Script/Core/mod_manager.py`: missing or disabled dependencies now produce `缺少依赖mod: ...`, cycle dependencies produce `mod依赖存在循环: ...`, and dependents are skipped when a dependency fails to load with `依赖mod尚未成功加载: ...`.
- Implemented stable dependency-before-dependent ordering. The sorter only adds dependency edges; unrelated mods keep their configured relative order.
- `load_priority` remains metadata only. This preserves existing behavior for mods without declared dependency relationships.
- `incompatible` remains read-only metadata in this narrow section 3 implementation; no current enabled local mod declares incompatibilities, and the OpenSpec dependency requirement is satisfied by dependency diagnostics/order.

Section 3 verification commands:

- `python mod/tests/test_mod_manager_dependencies.py`: pass.
- `python -m py_compile Script/Core/mod_manager.py mod/tests/test_mod_manager_dependencies.py`: pass.
- `python mod/local_bugfix/tests/test_local_bugfix_mod.py`: pass.
- `python mod/local_bugfix/tests/test_group_sex_edge_release_mod.py`: pass.
- `python mod/local_bugfix/tests/test_h_orgasm_batch_mod.py`: pass.
- `python mod/group_sex_extension/tests/test_group_sex_extension_mod.py`: pass.
- `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`: pass.
- `python mod/local_fontfix/tests/test_local_fontfix_mod.py --mod-root mod/local_fontfix`: pass.

## Split Component: local_group_target_context_fix

Tasks 4.1 and 4.2 results:

- Created `mod/local_group_target_context_fix/` as the first no-dependency split bugfix component.
- Component manifest replaces only `Script.Design.handle_npc_ai_in_h.npc_ai_in_group_sex` and `Script.Design.handle_npc_ai_in_h.npc_ai_in_group_sex_type_3`.
- Component script keeps the old local invariant: save player `target_character_id`, run upstream group AI through `call_original`, and restore the saved target in `finally`.
- Component README records symptom, root cause, patch points, dependency-free status, test command, and pending BDD scenario.
- Existing target-preservation coverage was rewritten into isolated component tests that do not import unrelated split components.

Verification commands:

- `python mod/local_group_target_context_fix/tests/test_local_group_target_context_fix_mod.py`: pass.
- `python -m py_compile mod/local_group_target_context_fix/scripts/local_group_target_context_fix.py mod/local_group_target_context_fix/tests/test_local_group_target_context_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_h_movement_interrupt_fix

Task 4.3 results:

- Created `mod/local_h_movement_interrupt_fix/` as a no-dependency split bugfix component.
- Component manifest replaces `Script.Design.character_move.own_charcter_move` and `Script.Design.handle_npc_ai_in_h.npc_active_h`.
- Component script migrates the stale movement lifecycle guards from old `local_bugfix`: player `move_stop`/H/group interruption cleanup, NPC active-H pre-cleanup, and group-H movement cancellation for state-machine movement entry points.
- The hidden runtime registry patch for `Script.StateMachine.default.general_movement_module`, `character_continue_move`, and `constant.handle_state_machine_data[CONTINUE_MOVE]` remains inside the component because those upstream entry points are table-driven rather than manifest replacement targets.
- Component README records symptom, root cause, patch points, dependency-free status, test command, and pending BDD paths.
- Existing stale-movement coverage was rewritten into isolated tests that do not import unrelated split components.

Verification commands:

- `python mod/local_h_movement_interrupt_fix/tests/test_local_h_movement_interrupt_fix_mod.py`: pass.
- `python -m py_compile mod/local_h_movement_interrupt_fix/scripts/local_h_movement_interrupt_fix.py mod/local_h_movement_interrupt_fix/tests/test_local_h_movement_interrupt_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_group_masturbation_intent_fix

Task 4.4 results:

- Created `mod/local_group_masturbation_intent_fix/` as a no-dependency split bugfix component.
- Component manifest replaces only `Script.Design.handle_npc_ai.find_character_target`.
- Component script migrates the group auto-masturbation lifecycle guards from old `local_bugfix`: route `masturebate == 3` in group H mode to `default91`, mark the role consumed for the current player-action slice, clear regenerated/stale markers in the same slice, and end the NPC action when `default91` is unavailable.
- The old broad `judge_character_h_obscenity_unconscious` reimplementation was not migrated. Current upstream `Script/Design/handle_npc_ai_in_h.py` already returns immediately after `npc_ai_in_group_sex(character_id)` in the group-AI branch, so the retained behavioral surface is the intent marker routing in `find_character_target`.
- Component README records symptom, root cause, patch point, no-dependency status, upstream resync decision, test command, and pending BDD path.
- Existing auto-masturbation marker coverage was rewritten into isolated tests that do not import unrelated split components.

Verification commands:

- `python mod/local_group_masturbation_intent_fix/tests/test_local_group_masturbation_intent_fix_mod.py`: pass.
- `python -m py_compile mod/local_group_masturbation_intent_fix/scripts/local_group_masturbation_intent_fix.py mod/local_group_masturbation_intent_fix/tests/test_local_group_masturbation_intent_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_group_participant_admission_fix

Task 4.5 results:

- Created `mod/local_group_participant_admission_fix/` as a no-dependency split bugfix component.
- Component manifest loads a script with no registered replacement functions because the required patch point is the class draw method `Script.System.Sex_System.sex_be_discovered_panel.Sex_Be_Discovered_Panel.draw`.
- Component script migrates the tired/exhausted discoverer admission guard from old `local_bugfix`: detect group mode, reject hit-point depleted, tired-flagged, or tired-level-2 discoverers, reuse the existing discovery status effects, set `SEE_H_AND_LEAVE`, and return to the in-scene panel.
- Component README records symptom, root cause, hidden patch point, no-dependency status, test command, and pending BDD path.
- Existing tired-discoverer and auto-leave coverage was rewritten into isolated tests that do not import unrelated split components.

Verification commands:

- `python mod/local_group_participant_admission_fix/tests/test_local_group_participant_admission_fix_mod.py`: pass.
- `python -m py_compile mod/local_group_participant_admission_fix/scripts/local_group_participant_admission_fix.py mod/local_group_participant_admission_fix/tests/test_local_group_participant_admission_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_hypnosis_state_fix

Task 4.6 results:

- Created `mod/local_hypnosis_state_fix/` as a no-dependency split bugfix component.
- Component manifest loads a script with no registered replacement functions because all three patch points are runtime hooks: `Chose_Hypnosis_Type_Panel.change_hypnosis_type`, behavior effect `1211` / `handle_hypnosis_one`, and `handle_premise.get_weight_from_premise_dict`.
- Component script migrates hypnosis mode persistence from old `local_bugfix`: instruction-mode hypnosis type changes immediately apply the current target, single-target hypnosis settlement re-applies the chosen hypnosis unconscious flag after upstream settlement, and the manual type selector can apply a one-off type while preserving the default "none" type.
- Component script migrates the hypnosis talk-gate bypass: targets with hypnosis unconscious flags `4/5/6/7` pass through the generic unconscious talk premise gate, while ordinary sleep/unconscious flags keep the original gate.
- Component README records symptom, root cause, hidden patch points, no-dependency status, test command, and pending BDD paths.
- Existing hypnosis mode and talk-gate coverage was rewritten into isolated tests that do not import unrelated split components.

Verification commands:

- `python mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`: pass.
- `python -m py_compile mod/local_hypnosis_state_fix/scripts/local_hypnosis_state_fix.py mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_pain_as_pleasure_fix

Task 4.7 results:

- Created `mod/local_pain_as_pleasure_fix/` as a no-dependency split bugfix component.
- Component manifest loads a script with no registered replacement functions because the patch points are runtime registry hooks: `base_chara_state_common_settle` aliases, behavior effect `1213` / `handle_hypnosis_cancel`, and direct pain second-effect handlers.
- Component script migrates the old `local_bugfix` pain-as-pleasure invariants: pain decreases temporarily disable the conversion flag and use upstream pain settlement, hypnosis cancel clears the target's `pain_as_pleasure` flag, and small/middle/large pain plus extra-orgasm direct pain paths convert positive pain into psychological pleasure.
- Component README records symptom, root cause, hidden patch points, no-dependency status, test command, and pending BDD path.
- Existing pain-as-pleasure coverage was rewritten into isolated tests that do not import unrelated split components.

Verification commands:

- `python mod/local_pain_as_pleasure_fix/tests/test_local_pain_as_pleasure_fix_mod.py`: pass.
- `python -m py_compile mod/local_pain_as_pleasure_fix/scripts/local_pain_as_pleasure_fix.py mod/local_pain_as_pleasure_fix/tests/test_local_pain_as_pleasure_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_h_orgasm_batch_fix

Task 4.9 results:

- Created `mod/local_h_orgasm_batch_fix/` as a no-dependency split bugfix component.
- Component manifest replaces `Script.Design.second_behavior.check_second_effect`, `Script.Design.second_behavior.orgasm_settle`, and `Script.UI.Panel.manage_power_system_panel.store_power_by_human_power`.
- Component manifest registers `local_h_orgasm_batch_fix_is_settling` as the documented batch-state hook for dependent components.
- Component also registers legacy `local_bugfix_is_orgasm_batch_settling` for migration compatibility while old tests and any still-unsplit local logic are being retired.
- The component script is the existing self-contained H orgasm batch implementation, with only the new hook alias added.
- Existing H orgasm batch coverage was copied into the split component suite and the one old `local_bugfix.py` coupling test was replaced with direct hook coverage.

Verification commands:

- `python mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py`: pass.
- `python -m py_compile mod/local_h_orgasm_batch_fix/scripts/h_orgasm_batch.py mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Split Component: local_group_edge_release_fix

Task 4.8 results:

- Created `mod/local_group_edge_release_fix/` as a dependent split bugfix component.
- Component manifest declares dependency on `local_h_orgasm_batch_fix`.
- Component manifest replaces `Script.Design.handle_npc_ai.judge_character_tired_sleep` and `Script.Design.handle_npc_ai_in_h.recover_from_unconscious_h`.
- Component script runtime-patches behavior effects `528` and `529` for single NPC H exit and group H exit settlement.
- Component script migrates pending edge release before group cleanup: group end, single NPC exit, group-to-H transition, unconscious recovery, stale template participants, multi-count release waves, release-generated second behavior flushing, and batch-guarded tired/sleep checks.
- The batch guard now prefers `second_behavior.local_h_orgasm_batch_fix_is_settling`, with legacy fallback to `local_bugfix_is_orgasm_batch_settling` during migration.
- Existing group edge release coverage was copied into the split component suite and adapted to load `local_group_edge_release_fix` plus `local_h_orgasm_batch_fix` instead of the monolithic `local_bugfix`.

Verification commands:

- `python mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py`: pass.
- `python -m py_compile mod/local_group_edge_release_fix/scripts/local_group_edge_release_fix.py mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py`: pass.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.

## Component TDD Coverage

Tasks 5.1-5.7 results:

- Rewrote old `test_local_bugfix_mod.py` coverage into the relevant split suites:
  - Target preservation: `mod/local_group_target_context_fix/tests/test_local_group_target_context_fix_mod.py`.
  - Stale movement interruption: `mod/local_h_movement_interrupt_fix/tests/test_local_h_movement_interrupt_fix_mod.py`.
  - Group masturbation intent lifecycle: `mod/local_group_masturbation_intent_fix/tests/test_local_group_masturbation_intent_fix_mod.py`.
  - Tired group discoverer admission: `mod/local_group_participant_admission_fix/tests/test_local_group_participant_admission_fix_mod.py`.
  - Hypnosis persistence and talk gate: `mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`.
  - Pain-as-pleasure consistency: `mod/local_pain_as_pleasure_fix/tests/test_local_pain_as_pleasure_fix_mod.py`.
- Copied and adapted old `test_group_sex_edge_release_mod.py` into `mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py`.
- Copied and adapted old `test_h_orgasm_batch_mod.py` into `mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py`.
- Added missing focused coverage discovered during audit: component manifest checks, hidden registry patch checks, dependency-order loader tests, batch-state hook coverage, and the current-upstream resync decision for group auto-masturbation's old broad `judge_character_h_obscenity_unconscious` copy.
- Each split component suite runs independently of unrelated split components. `local_group_edge_release_fix` loads `local_h_orgasm_batch_fix` only as its declared dependency.
- Every component README records its independent test command.
- H orgasm batch coverage includes `test_orgasm_settle_keeps_translation_function_available_for_achievements`, which drives repeated/multi-part orgasm settlement through the translated achievement call, and `test_remote_plural_orgasm_achievement_notice_is_suppressed`, which covers the remote-draw suppression variant of that achievement path.

Section 5 verification commands:

- `python mod/local_group_target_context_fix/tests/test_local_group_target_context_fix_mod.py`: pass.
- `python mod/local_h_movement_interrupt_fix/tests/test_local_h_movement_interrupt_fix_mod.py`: pass.
- `python mod/local_group_masturbation_intent_fix/tests/test_local_group_masturbation_intent_fix_mod.py`: pass.
- `python mod/local_group_participant_admission_fix/tests/test_local_group_participant_admission_fix_mod.py`: pass.
- `python mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`: pass.
- `python mod/local_pain_as_pleasure_fix/tests/test_local_pain_as_pleasure_fix_mod.py`: pass.
- `python mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py`: pass.
- `python mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py`: pass.

## BDD Verification Scenarios

Tasks 6.1-6.6 results:

- Added `bdd-scenarios.md` with the local-mod BDD template: setup, enabled mods, action, expected state or visible result, automation status, and evidence.
- Added scenarios for all eight split bugfix components.
- Added explicit normal-scene and H-mode hypnosis mind-control persistence scenarios.
- Added the H orgasm batch translated-achievement runtime-safety scenario.
- Added the dependency failure/order scenario for the mod loader.

## Maintained Feature Mod Audit

Tasks 7.1-7.7 results:

- Expanded `mod/group_sex_extension/tests/test_group_sex_extension_mod.py` with command registration coverage for all three commands and the custom complete-hypnosis premise.
- Expanded `group_sex_extension` coverage for participant collection from both `group_sex_panel.count_group_sex_character_list()` and current-scene H-state characters.
- Confirmed `group_sex_extension` remains independent from the split local bugfix components; its manifest still declares no dependencies and the tests install only the module stubs they need.
- Expanded `mod/local_performance/tests/test_local_performance_mod.py` with a manifest smoke check for exactly the two replacement targets `Script.Core.main_frame.read_queue` and `Script.Core.flow_handle.askfor_wait`, with no split-bugfix dependency.
- Recorded `LB-BDD-011` for the local performance wait-flow scenario.
- Re-ran existing `local_performance` web-mode, benchmark-mode, stale-input drain, and next-panel fresh-input safety coverage.
- Existing expanded `全员催眠增强` test verifies complete-hypnosis characters receive sensitivity and pain-as-pleasure boosts while their hypnosis unconscious state is unchanged, and incomplete-hypnosis characters are not modified.

Section 7 verification commands:

- `python mod/group_sex_extension/tests/test_group_sex_extension_mod.py`: pass.
- `python -m py_compile mod/group_sex_extension/tests/test_group_sex_extension_mod.py`: pass.
- `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`: pass.
- `python -m py_compile mod/local_performance/tests/test_local_performance_mod.py`: pass.

## Migration and Deprecated Backup

Tasks 8.1-8.5 results:

- Moved active `mod/local_bugfix/` to `mod/deprecated/local_bugfix/`.
- Removed `local_bugfix` from default `mod/mod_config.json` `enabled_mods` and `load_order`.
- Added replacement split component ids to default `enabled_mods` and `load_order`:
  `local_group_target_context_fix`, `local_h_movement_interrupt_fix`, `local_group_masturbation_intent_fix`, `local_group_participant_admission_fix`, `local_hypnosis_state_fix`, `local_pain_as_pleasure_fix`, `local_h_orgasm_batch_fix`, and `local_group_edge_release_fix`.
- Preserved dependency order by placing `local_h_orgasm_batch_fix` before `local_group_edge_release_fix`.
- Added `mod/LOCAL_BUGFIX_MIGRATION.md` mapping old monolithic behavior to split component ids.
- Added a deprecation note to `mod/deprecated/local_bugfix/README.md`.
- Confirmed `Script/Core/mod_manager.py` scans only immediate children of `mod/` for `mod_info.json`, so `mod/deprecated/local_bugfix/` is not scanned as an active mod by default.

## Follow-up Audit Status: 2026-07-05

The earlier notes below are historical evidence from the first migration pass. A follow-up audit found that several items were overstated as "final" when they were actually unit/script coverage, manifest sorting smoke, or documented BDD scenarios.

Follow-up fixes now implemented in this branch:

- `Script/Core/mod_manager.py` now reports enabled-but-missing configured mods, reports duplicate `mod_id` scans deterministically while keeping the first scanned folder, and rolls back declared function/asset mutations when a mod fails during load. The rollback is intentionally narrow: it restores `_original_functions`, `_mod_functions`, `_mod_assets`, and module attributes declared in the mod manifest; arbitrary side effects inside mod script bodies are not globally reversible.
- `mod/tests/test_split_local_bugfix_manifests.py` now loads each split component through `ModManager.load_all_enabled_mods()` with only declared dependencies enabled, instead of only checking dependency sorting.
- `local_h_movement_interrupt_fix` now clears `move_src`, `move_target`, and `move_final_target` consistently across player interruption, NPC active-H interruption, and group-H movement cancellation.
- `local_hypnosis_state_fix` now uses the current `handle_t_unconscious_hypnosis_flag` premise predicate for the talk gate, with the raw hypnosis flag set retained only as compatibility fallback.
- `local_group_edge_release_fix` treats stale template-only non-H participants as cleanup-only, so stale/out-of-reset entries do not receive live orgasm settlement.
- `group_sex_extension` filters template participants to nonzero, existing, currently H-active characters before later hypnosis/command processing.
- `local_performance` now reads the current cache dynamically, defers web-mode detection to the core predicate when available, and fails closed when required replacement callables are missing. A generation-token queue invariant was not added because the current queue carries bare command strings and a token protocol would be broader than this follow-up.
- Fake module leakage was addressed in `local_group_target_context_fix` and `local_performance` tests by adding restore/teardown paths.

Follow-up verification run in this environment:

- `python -m pytest mod/tests/test_mod_manager_dependencies.py -q`: unavailable, `No module named pytest`.
- `python mod/tests/test_mod_manager_dependencies.py`: pass.
- `python mod/tests/test_split_local_bugfix_manifests.py`: pass.
- `python mod/local_h_movement_interrupt_fix/tests/test_local_h_movement_interrupt_fix_mod.py`: pass.
- `python mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py`: pass.
- `python mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py`: pass.
- `python mod/local_group_target_context_fix/tests/test_local_group_target_context_fix_mod.py`: pass.
- `python mod/local_group_masturbation_intent_fix/tests/test_local_group_masturbation_intent_fix_mod.py`: pass.
- `python mod/local_group_participant_admission_fix/tests/test_local_group_participant_admission_fix_mod.py`: pass.
- `python mod/local_pain_as_pleasure_fix/tests/test_local_pain_as_pleasure_fix_mod.py`: pass.
- `python mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py`: pass.
- `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`: pass.
- `python mod/group_sex_extension/tests/test_group_sex_extension_mod.py`: pass.
- `python -m py_compile ...` for the touched scripts/tests and `Script/Core/mod_manager.py`: pass.
- `openspec validate modularize-local-bugfixes-and-audit-local-mods --strict`: pass in the parent verification environment on 2026-07-05.

Updated verification should supersede the historical final-verification claims below. Full manual BDD/game-flow execution remains pending unless a later dated run records it.

## Historical Final Verification

Tasks 9.1-9.6 results:

- Isolated split component tests all passed:
  `local_group_target_context_fix`, `local_h_movement_interrupt_fix`, `local_group_masturbation_intent_fix`, `local_group_participant_admission_fix`, `local_hypnosis_state_fix`, `local_pain_as_pleasure_fix`, `local_h_orgasm_batch_fix`, and `local_group_edge_release_fix`.
- Initial loader/config smoke tests passed:
  `python mod/tests/test_mod_manager_dependencies.py` and `python mod/tests/test_split_local_bugfix_manifests.py`.
- Maintained local mod tests passed:
  `python mod/group_sex_extension/tests/test_group_sex_extension_mod.py`,
  `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`,
  and `python mod/local_fontfix/tests/test_local_fontfix_mod.py --mod-root mod/local_fontfix`.
- Syntax validation passed for `Script/Core/mod_manager.py`, all new split component scripts/tests, loader smoke tests, and changed maintained-mod tests via `python -m py_compile`.
- BDD scenarios are documented in `bdd-scenarios.md`; full UI/game-flow scenarios are recorded there as manual or near-real harness pending where appropriate. This is scenario documentation plus focused automation, not full manual BDD execution.
- Historical strict validation was recorded here as passing; the 2026-07-05 follow-up rerun also passed in the parent verification environment. Full manual BDD/game-flow execution remains pending.
