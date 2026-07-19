## Worktree Status (2026-07-10, post-backout)

Per the user's decision, the exact-once global monkeypatch experiment was removed from the worktree on 2026-07-10; the mod script and its tests were reverted to HEAD and only the narrow `place_all_not_h` full-scene loop plus registry/alias replacement was re-applied, together with its two component tests. The full component suite (19 tests, including all restored upstream tests) passed after the re-application. The sections below describing the experiment are retained as the starting point for a future dispatch-scoped ownership design; that code is no longer present (backup at /tmp/erark-backup-2026-07-10/). Manual target-switch verification remains pending. Cross-change branch, HEAD, and protected-file state are in `../continue-local-bugfix-audit/design.md`.

## Confirmed Call Graph and Root Causes

### NPC state-machine caller

`character_behavior.character_behavior()` calls `handle_npc_ai.find_character_target()`. NPC state 40 opens `Sex_Be_Discovered_Panel`; after the panel returns, `character_behavior.py` later invokes an outer `judge_character_status()`. In the upstream existing-group accept/refuse paths, the panel also manually settles the selected discovery behavior. The same behavior can therefore be consumed once in the panel and again by the outer NPC settlement.

### Direct hidden-discovery caller

`hidden_sex_panel.settle_discovered()` calls `panel.draw()` directly. There is no later NPC outer settlement. This path depends on the panel performing any required settlement itself, so simply deleting all manual settlement would drop effects here.

### Initial conversion ordering

When single-target H is converted to group mode, upstream assigns `DISCOVER_OTHER_SEX_AND_JOIN` to the discoverer and then immediately settles the player's `OTHER_SEX_BE_FOUND_TO_GROUP_SEX`. That nested player update can overwrite or reset the discoverer's pending behavior before the discoverer is settled. The discoverer must be settled before the nested player flow, and any later NPC outer settlement must then skip only that already consumed behavior.

### Contradictory controls

`handle_scene_all_not_h()` returned success from inside its loop after inspecting the first non-player character. Instruction 5055 uses `SCENE_ALL_NOT_H`, while 6008 uses `GROUP_SEX_MODE_ON|IS_H`. If the first NPC is outside H and a later NPC is already in H, both invite-group and end-group can appear. Correcting the full-scene premise removes the contradiction but does not by itself establish the later participant's H state or normal action interface.

## Experimental Implementation Present but Unaccepted

The current local component includes:

- `_DISCOVERY_OUTER_SETTLEMENT_CONTEXT`, a per-character depth table.
- `_SUPPRESS_NEXT_DISCOVERY_OUTER_SETTLEMENT`, a global character-ID set.
- Wrappers around every `handle_npc_ai.find_character_target()` call and the global `character_behavior.judge_character_status()` function.
- Rewritten invitation callbacks: an existing-group NPC path is left to a presumed outer owner; a direct caller settles immediately; initial conversion settles the discoverer before the nested player update and adds suppression for the later outer call.
- A wrapper around `_end_current_h()` to suppress a presumed later duplicate.
- Immediate settlement for tired auto-leave on a direct call.
- A corrected full-scene `place_all_not_h`, installed in both the premise registry and defining-module alias.

This code is a candidate, not an accepted ownership model.

## Known Safety Gaps in the Global Ownership Experiment

1. The design requires a token scoped to one dispatch, but the implementation stores only character IDs in a process-global set. There is no dispatch identity.
2. Wrapping `find_character_target()` assumes every call that enters the context will later perform an outer settlement. A direct caller of that function can create suppression without a matching consumer.
3. If early settlement is not followed immediately by the same character's outer `judge_character_status()`, the next unrelated behavior can be skipped.
4. Cleanup is only proved for exceptions propagating out of the wrapped target search. Caught exceptions, early return, re-entry, nested calls, and interruption between early settlement and outer settlement remain unsafe.
5. The global `judge_character_status()` wrapper can consume suppression for calls made by unrelated mods or flows.
6. Hot reload, partial install rollback, repeated load, same-NPC nesting, and interleaved different-NPC dispatches have no proved invariant.
7. `local_group_masturbation_intent_fix` also wraps `find_character_target()` through a different mechanism. Current load order can make admission outermost while `test_bdd_save_group_ai.py:110` expects the masturbation wrapper to be outermost. Checking `__module__` is insufficient; both load orders, repeated loads, and the complete wrapper chain must be behavior-tested.

These gaps are why the exact-once implementation must not continue until the user chooses between this global approach, a core explicit settlement-owner interface, or postponement.

## Adjacent Discovery Paths Found but Not Yet in Scope

The direct hidden-discovery call has other choices whose behavior is assigned without a proven settlement owner:

- `_let_find_chara_away()` can assign `SEE_H_BUT_DECEIVED`.
- `_continue_exhibitionism_sex()` can assign `SEE_H_BUT_IGNORE` or `SEE_H_AND_LEAVE` in some branches.
- `_switch_to_hidden_sex()` and the exhibitionism transition contain nested player flows that may create the same overwrite risk.

The current experimental patch does not prove these paths safe. They were not part of the reported late-participant admission bug and must not be silently folded into implementation. The user must decide whether a future ownership redesign covers the whole discovery panel or only group admission.

## Written but Unexecuted Verification

The component tests now contain fake-module cases for NPC existing-group admission/refusal, initial conversion, direct hidden-discovery acceptance, end-H suppression, exception cleanup, same-NPC nesting, interaction with the group extension and pain conversion, and the full-scene premise. None have run.

Two critical component tests are defined but omitted from the file's `main()` runner, so the README-style direct Python command would not execute them; pytest discovery would:

- `test_nested_target_search_keeps_outer_discovery_context_until_outer_return`
- `test_target_search_exception_discards_suppression_created_by_failed_dispatch`

There is no near-real NPC state-machine discovery test and no near-real direct hidden-discovery test. Existing `test_bdd_group_admission.py` only checks a fatigue premise. Missing connected evidence includes:

- Switch the player target to the admitted NPC and inspect the real instruction set: normal group actions present, invite absent, end-group retained.
- Direct hidden-discovery initial conversion, refusal, existing-group end, and other panel selections.
- Both wrapper load orders, repeat load, hot reload, same-NPC nesting, different-NPC interleaving, no-outer return, and exception/caught-exception cleanup.

Static simulation and user choice come before running these tests.
