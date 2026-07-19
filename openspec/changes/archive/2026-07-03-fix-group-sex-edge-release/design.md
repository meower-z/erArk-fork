## Context

The active mod set includes `group_sex_extension`, which adds a "全员寸止" command by setting each group-context NPC's `h_state.orgasm_edge` to `1` and resetting `orgasm_edge_count`. The base full group-sex end effect chain is `529 - 407 - 636 - 800 - 10011`: it summarizes group-sex orgasms, resets H state for scene characters, restores clothing, resets insert position, and turns group mode off. It does not include effect `526`, the ordinary edge-release effect used by normal H end. Discovered-interrupt handling can also set the player behavior to `GROUP_SEX_END` and call `handle_group_sex_end()`, so it reaches the same full-end effect chain.

Effect `526` is not directly sufficient for group-sex end because it releases only the player's current `target_character_id`. Group-sex end must release every relevant participant that still has pending edge counts before any H-state reset clears those counts.

There is also a `group_sex_to_h` behavior for "群交时NPC数量不足转为单人H". Its effect chain is `9999`, so it will not be covered by a wrapper on `529`; it also does not run `GROUP_SEX_MODE_OFF` (`10011`). Treat it as a targeted group-context reduction rather than a full group-mode shutdown. In contrast, `group_sex_npc_hp_0_end` is a single-NPC exit with its own H-state reset path; it may need a scoped release for the exiting NPC, but it must not trigger a full-group release for participants who continue group sex.

`recover_from_unconscious_h()` has a separate group-sex shutdown path: when unconscious H recovery happens during group sex, it directly calls `handle_clear_group_sex_template()` and `handle_group_sex_mode_off()` before settling other scene participants. This bypasses `529`, `10011`, and `GROUP_SEX_TO_H`, so it needs its own pre-clear release hook.

## Goals / Non-Goals

**Goals:**

- Release all pending group-mode edge orgasms immediately when group sex ends.
- Ensure released orgasms are included in the group-sex end summary and HP/MP max growth settlement.
- Preserve the existing group-sex end effect ordering after the release step.
- Implement as a mod-level hook so core game files and CSV data remain untouched.
- Cover normal group-sex end, discovered-interrupt group-sex end, and player-HP-zero group-sex interruption because they share the same group end reset pattern.
- Cover group-context reductions by releasing pending edge counts only for participants that leave the group context before their own H state is reset.
- Cover unconscious-recovery group-sex shutdown before group templates are cleared and group mode is turned off.
- Prevent single-NPC group-sex exit from releasing unrelated participants who remain in group sex, while still allowing scoped release for the exiting NPC.

**Non-Goals:**

- Do not redesign the edge-mode command or its UI.
- Do not change normal single-target `orgasm_edge_off` behavior.
- Do not change sleep settlement, jewel conversion, or H-state reset semantics outside this bug.
- Do not make direct core-file edits while other agents may be working.
- Do not turn every single-NPC group-sex exit into a full group-end release.

## Decisions

1. Patch the registered behavior effect for `GROUP_SEX_END_H_ADD_HPMP_MAX` (`529`) instead of editing `Behavior_Effect.csv`.

   Rationale: `529` is the first effect in the `group_sex_end` and `group_sex_pl_hp_0_end` chains, so a wrapper can release pending edge counts before the existing summary code reads `h_state.orgasm_count`. This keeps generated data stable and avoids conflicting with other agents' work.

   Alternative considered: add `526` to the CSV effect chain. That would still only release the current player target and would not cover multiple group participants.

2. Release participants by iterating the group-sex context, not by relying on the current player target.

   Rationale: group sex can include multiple NPCs in templates, current scene participants, and NPCs affected by the extension's batch command. The release helper should gather the same practical participant set used by `group_sex_extension._get_group_sex_character_ids()` (group templates plus current-scene H participants), deduplicate IDs, then release only existing NPC/operator characters while group mode is active, and only when they are in H state or are present in the group template/context, have `h_state.orgasm_edge == 1`, and have non-zero `orgasm_edge_count`.

   For the full-end `529` wrapper, released current-scene participants must be visible to the original `529` summary. Template-only or stale off-scene participants may be cleaned to prevent sleep-time leakage, but the plan does not require the original `529` summary to include characters it does not normally inspect.

   Alternative considered: iterate only the current scene. That catches end settlement participants but can miss template participants if scene/template state is temporarily inconsistent.

3. Use the existing second-stage orgasm settlement path, but synchronously finish release settlement before the original end summary.

   Rationale: released edge counts should become ordinary orgasm outcomes, including second behavior effects, talk, achievements, and local `h_orgasm_batch` behavior. The helper should set `orgasm_edge = 2`, settle a snapshot of `orgasm_edge_count`, synchronously flush or execute only the newly generated orgasm second-stage effects, verify `h_state.orgasm_count` has been updated before delegating to the original `529` handler, original `528` handler, or continuing to a scoped H reset, then clear the counters and reset `orgasm_edge` to `0` when no following H-state reset will do it. If the local batch replacement is active, the implementation may use its immediate flush behavior; without that replacement it must not merely enqueue second-stage work for a later behavior tick.

   The fallback must not call a broad `check_second_effect()` pass just to flush release effects, because that can also run unrelated orgasm judge, item, insert, mark, and other queued second effects. It should snapshot queued second behaviors before release, then apply only the new orgasm-related second behaviors produced by that release. If `h_orgasm_batch` already flushed the release-generated effects, the fallback must detect that and avoid double-flushing or reapplying the same second behaviors.

   Alternative considered: manually increment `orgasm_count` without second-stage settlement. That would make the group end summary work but skip normal orgasm side effects.

4. Store and call the original `529` handler from the mod wrapper.

   Rationale: the wrapper should only add the missing pre-release behavior, then delegate to the original max-stat summary. The mod should patch both `constant.settle_behavior_effect_data[529]` and `Script.Settle.default.handle_group_sex_end_h_add_hpmp_max` to match existing local bugfix registry patch style.

5. Add targeted hooks for single-participant exit and group-context reduction.

   Rationale: `group_sex_npc_hp_0_end` is a single NPC leaving group sex; the hook should release only that NPC's pending edge counts before its original chain reaches `END_H_ADD_HPMP_MAX` (`528`) and `SELF_H_STATE_RESET` (`403`), and must not release unrelated participants. The implementation must not globally patch effect `DESIRE_POINT_TO_0` (`1503`), because that effect is shared by non-group-sex behaviors. It should instead use behavior/caller context guards, a guarded `528` wrapper, or the existing tired-exit branch to scope release to `GROUP_SEX_NPC_HP_0_END`.

   `group_sex_to_h` has a `9999` no-op effect chain and is assigned directly when group sex drops to one remaining NPC, so the `529` wrapper will not run and patching global `9999` would be unsafe. The transition hook should be attached to the concrete `GROUP_SEX_TO_H` assignment/settlement path, such as the `handle_npc_ai.judge_character_tired_sleep` branch or an equivalent pre/post snapshot wrapper. It must capture the pre-transition group participant set, remove the continuing target, and release only that leaver set. A generic wrapper that merely observes `behavior_id == GROUP_SEX_TO_H` without knowing the pre-transition participant set is insufficient. The continuing target remains untouched by this cleanup and follows existing game behavior.

   Alternative considered: leave `group_sex_to_h` and `group_sex_npc_hp_0_end` outside this change. That would keep scoped group-exit paths where pending edge counts can survive until a later unrelated settlement.

6. Add a targeted hook for unconscious-recovery group-sex shutdown.

   Rationale: `recover_from_unconscious_h()` directly clears the player's group-sex template and turns group mode off when the target recovers from unconscious H during group sex. Because template data and `cache.group_sex_mode` are lost immediately afterward, the hook must capture the pre-recovery group participant set and release pending edge counts before `handle_clear_group_sex_template()` and `handle_group_sex_mode_off()` run. It should then preserve the existing recovery flow, including later handling of other scene participants and the possible continuing interaction with the recovered target.

   Alternative considered: rely on the `GROUP_SEX_MODE_OFF` effect hook. This path calls the handler directly and already has the group participant data about to be cleared, so a local wrapper around `recover_from_unconscious_h()` or its explicit group branch is the narrower and more reliable hook.

## Risks / Trade-offs

- [Risk] Calling orgasm settlement during group end may interact with the existing local H orgasm batch mod. -> Mitigation: tests must load the local bugfix orgasm batch replacement and assert that release effects settle before the original `529` handler and before `407` resets H state.
- [Risk] `h_orgasm_batch` is loaded after `local_bugfix.py`, so static module-import assumptions can miss the batch helper. -> Mitigation: release code must detect batch availability at release time after mod replacements are installed.
- [Risk] Participant discovery may include characters not actually in H state. -> Mitigation: base discovery on `group_sex_extension._get_group_sex_character_ids()` semantics, release only existing NPC/operator characters while group mode is active, and only when they are in H state or present in group context with `orgasm_edge == 1` and non-zero pending counts.
- [Risk] Release state `orgasm_edge == 2` could persist past group end. -> Mitigation: clear or reset it after release settlement, and tests must assert both `orgasm_edge_count` and `orgasm_edge` cannot leak into sleep settlement.
- [Risk] `group_sex_to_h` or `group_sex_npc_hp_0_end` release may accidentally include participants who remain in group sex. -> Mitigation: tests must pin the expected scoped behavior: the exiting NPC can be released before its own reset, while unrelated remaining participants and the continuing target are untouched.
- [Risk] `recover_from_unconscious_h()` cleanup may lose participant context after template clear/mode off. -> Mitigation: capture the group participant set before calling the original clear/off logic and test ordering against both `handle_clear_group_sex_template()` and `handle_group_sex_mode_off()`.
- [Risk] A fallback flush may run unrelated second effects. -> Mitigation: tests must assert the fallback applies only second behaviors created by the edge release, not a full `check_second_effect()` pass.
- [Risk] New hooks may replace functions that `mod/local_bugfix` already replaces. -> Mitigation: compose with the existing local bugfix wrappers and preserve their original behaviors, rather than registering independent replacements that overwrite them.
- [Risk] A future core change may add `526` or an equivalent group release. -> Mitigation: wrapper should be idempotent and skip when there are no pending edge counts.
