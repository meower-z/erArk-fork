## 1. Test Coverage

- [x] 1.1 Add a focused test for normal group-sex end with one edged participant, asserting pending edge counts convert before H-state reset and counters clear.
- [x] 1.2 Add a multi-participant test for batch edge release, including stable dedupe between current scene participants and group-sex template participants.
- [x] 1.3 Add a no-op test proving group-sex end behavior is unchanged when no participant has pending edge counts.
- [x] 1.4 Add a player-HP-zero group-sex interruption test proving it uses the same pre-reset release path.
- [x] 1.5 Add an ordering assertion that released counts and second-stage orgasm effects are visible to the original `GROUP_SEX_END_H_ADD_HPMP_MAX` summary before `SCENE_ALL_CHARACTERS_H_STATE_RESET`.
- [x] 1.6 Add a discovered-interrupt test proving the `GROUP_SEX_END` route through `handle_group_sex_end()` uses the same `529` wrapper.
- [x] 1.7 Add a `group_sex_to_h` transition test proving cleanup is attached to the concrete `GROUP_SEX_TO_H` path, not the global `9999` no-op effect, and uses the pre-transition participant set minus the continuing target.
- [x] 1.8 Add a `group_sex_npc_hp_0_end` scoped test proving the exiting NPC can release its own pending edge counts before original `END_H_ADD_HPMP_MAX` (`528`) and that `528` reads the released `orgasm_count`.
- [x] 1.9 Add a `group_sex_npc_hp_0_end` negative test proving a single NPC exit does not release unrelated participants who remain in group sex.
- [x] 1.10 Add cleanup assertions for both `orgasm_edge_count` and `h_state.orgasm_edge`, so released edge state cannot be settled later during sleep.
- [x] 1.11 Add a fallback-flush test proving only release-generated orgasm second effects are applied when `h_orgasm_batch` immediate flush is unavailable.
- [x] 1.12 Add a no-double-flush test proving release-generated second effects are not reapplied when `h_orgasm_batch` already flushed them immediately.
- [x] 1.13 Add a stale template/off-scene participant test pinning whether cleanup prevents later leakage without requiring inclusion in the original `529` summary.
- [x] 1.14 Add a `recover_from_unconscious_h()` group-sex shutdown test proving pending edge release runs before `handle_clear_group_sex_template()` and `handle_group_sex_mode_off()`.
- [x] 1.15 Add a `recover_from_unconscious_h()` scoped negative test proving the recovery flow does not double-release the recovered target or unrelated continuing interaction state.
- [x] 1.16 Add a non-group-sex behavior test for another `DESIRE_POINT_TO_0` (`1503`) user, proving shared effect `1503` does not trigger group-edge release.
- [x] 1.17 Add regression tests proving existing `local_bugfix.py` replacements for tired sleep, group masturbation, movement/H interruption, and unconscious checks still run after the new hooks are installed.

## 2. Mod Implementation

- [x] 2.1 Implement a helper in `mod/local_bugfix` to collect group-sex participants using the same semantics as `group_sex_extension._get_group_sex_character_ids()` with stable dedupe.
- [x] 2.2 Filter the collected participants to existing NPC/operator characters that are in H state or present in group context, have `h_state.orgasm_edge == 1`, and have non-zero `orgasm_edge_count`.
- [x] 2.3 Implement a helper to release one character's `orgasm_edge_count` via the existing second-stage orgasm settlement, synchronously execute or flush only the generated second-stage orgasm effects, clear counters, and reset release state consistently.
- [x] 2.4 Prove the helper does not merely enqueue second-stage work when `h_orgasm_batch` is absent or changed; it must update `h_state.orgasm_count` before the caller continues, must not call a broad `check_second_effect()` pass, and must not double-apply effects already flushed by `h_orgasm_batch`.
- [x] 2.5 Wrap registered behavior effect `529` so group-edge release runs before the original `handle_group_sex_end_h_add_hpmp_max`.
- [x] 2.6 Patch both `constant.settle_behavior_effect_data[529]` and `Script.Settle.default.handle_group_sex_end_h_add_hpmp_max` using the existing local registry patch style.
- [x] 2.7 Add a separate mod hook for the concrete `GROUP_SEX_TO_H` assignment/settlement path, because that transition uses effect `9999` and the global no-op effect must not be patched.
- [x] 2.8 In the `GROUP_SEX_TO_H` hook, capture the pre-transition group participant set and release only the leaver set after excluding the continuing target.
- [x] 2.9 Add scoped handling for `group_sex_npc_hp_0_end` so the exiting NPC releases its own pending edge counts before the original `528` / `403` path when needed.
- [x] 2.10 Ensure `group_sex_npc_hp_0_end` does not trigger all-participant release; unrelated participants and the continuing target must be left untouched.
- [x] 2.11 Confirm the scoped NPC-exit implementation does not patch shared effect `1503`; guard by behavior ID, caller context, or a guarded `528` wrapper.
- [x] 2.12 Add a targeted mod hook for `handle_npc_ai_in_h.recover_from_unconscious_h()` or its explicit group-mode branch, capturing the pre-recovery group participant set before template clear/mode off.
- [x] 2.13 In the unconscious-recovery hook, release pending edge counts for participants leaving group context before calling the original clear-template and mode-off handlers, while preserving the original recovery flow.
- [x] 2.14 Detect `h_orgasm_batch` immediate-flush capability at release time after mod replacements are installed, not once at module import.
- [x] 2.15 Compose new hooks with existing `mod/local_bugfix/scripts/local_bugfix.py` replacement functions instead of registering independent replacements that overwrite current local fixes.
- [x] 2.16 Make the wrappers idempotent so they no-op after a future upstream release or when there are no pending edge counts.

## 3. Verification

- [x] 3.1 Run the new local bugfix tests.
- [x] 3.2 Run existing `mod/local_bugfix` and `mod/group_sex_extension` tests to catch regressions.
- [x] 3.3 Run `openspec validate fix-group-sex-edge-release --strict`.
- [x] 3.4 Manually inspect that the active CSV/compiled group-sex end effect chains remain unchanged and that the mod hooks provide the added runtime behavior for `group_sex_end`, `group_sex_pl_hp_0_end`, discovered `GROUP_SEX_END`, `group_sex_npc_hp_0_end`, the concrete `GROUP_SEX_TO_H` path, and `recover_from_unconscious_h()` group shutdown.
