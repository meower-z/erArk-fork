## 1. Root Cause Confirmation

- [x] 1.1 Trace group-mode `masturebate == 3` through `handle_npc_ai_in_h`, `character_behavior`, and `handle_npc_ai.find_character_target`.
- [x] 1.2 Confirm `default91` consumes the marker but group AI can regenerate it inside the same player action catch-up.
- [x] 1.3 Trace fatigued group-sex exit through `judge_character_tired_sleep`, H-state reset, and `Sex_Be_Discovered_Panel.draw`.
- [x] 1.4 Confirm group-sex invitation judgement does not reject exhausted characters before the invite option is shown.

## 2. Mod Implementation

- [x] 2.1 Add a helper that derives a current player-action token from the active `over_behavior_character` set and resets consumption state when that set changes.
- [x] 2.2 Add per-character consumption tracking for group-mode automatic masturbation routing.
- [x] 2.3 Update `patched_find_character_target()` so the first `masturebate == 3` routing in one player action can execute `default91`, while later routings in the same action mark the NPC complete.
- [x] 2.4 Clear only duplicate or unavailable masturbation markers suppressed by the local wrapper, so stale markers do not leak into later player actions.
- [x] 2.5 Add helpers to detect group-sex discoverers who are exhausted by hit points, tired flag, or tired level.
- [x] 2.6 Patch `Sex_Be_Discovered_Panel.draw` through the local registry patch path.
- [x] 2.7 Implement the tired-discoverer auto-leave path using existing discovery setup side effects and `SEE_H_AND_LEAVE`.

## 3. Documentation

- [x] 3.1 Update `mod/local_bugfix/README.md` with the repeated group-sex masturbation root cause and fix.
- [x] 3.2 Update `mod/local_bugfix/README.md` with the tired group-sex discovery root cause and fix.
- [x] 3.3 Add this OpenSpec change describing both bugfixes and their mod-level constraints.

## 4. Verification

- [x] 4.1 Add a regression test proving one NPC executes `default91` once per player action and can execute again in a later action.
- [x] 4.2 Add a regression test that simulates formal masturbation settlement clearing `masturebate`, group AI regenerating `masturebate = 3` in the same action, and the second routing being blocked.
- [x] 4.3 Add a regression test proving a suppressed duplicate marker is cleared and does not force `default91` in the next action unless group AI sets a new marker.
- [x] 4.4 Add a regression test proving an unavailable `default91` target clears the marker and marks the NPC complete.
- [x] 4.5 Add a regression test for tired group-sex discoverer detection.
- [x] 4.6 Add a regression test proving tired discoverers are assigned `SEE_H_AND_LEAVE`, preserve discovery setup side effects, and restore the in-scene panel state.
- [x] 4.7 Add a regression test proving the auto-leave behavior can be consumed by later status settlement to move the discoverer out of the H scene.
- [x] 4.8 Add a regression test proving the patched draw method skips the original panel only for tired group-sex discoverers.
- [x] 4.9 Run `.\.venv\Scripts\python.exe mod\local_bugfix\tests\test_local_bugfix_mod.py`.
- [x] 4.10 Run `.\.venv\Scripts\python.exe mod\local_bugfix\tests\test_h_orgasm_batch_mod.py`.
- [x] 4.11 Run `.\.venv\Scripts\python.exe -m py_compile mod\local_bugfix\scripts\local_bugfix.py mod\local_bugfix\tests\test_local_bugfix_mod.py`.
- [x] 4.12 Request an independent subagent review of the weak-agent bugfix and incorporate accepted feedback.
