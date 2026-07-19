## Why

`group_sex_extension` adds a group-mode "全员寸止" command that can leave NPCs in edge mode when group sex ends. Current group-sex end behavior resets H state without first releasing pending edge counts, so retained edge orgasms are not settled at the correct end-of-group moment and can appear later during sleep settlement.

This should be fixed as a mod-level bugfix because other agents may be changing core code, and the active local setup already uses mods for behavior corrections.

## What Changes

- Add a mod-level group-sex end cleanup that releases every group-context participant still in `h_state.orgasm_edge == 1` before H state reset runs.
- Convert each released participant's `orgasm_edge_count` into normal orgasm settlement immediately at group-sex end, including synchronous execution of the generated second-stage orgasm effects before the original end summary reads `h_state.orgasm_count`.
- Clear released edge counters and transition release state consistently with existing edge release semantics, so no pending or release marker leaks into later sleep settlement.
- Ensure group-sex end summary/max-stat settlement sees the released orgasms before `GROUP_SEX_END_H_ADD_HPMP_MAX` completes or before any H-state reset clears the counts.
- Cover normal group-sex end, player-HP-zero group-sex interruption, and "被发现并打断" paths that route to `GROUP_SEX_END` and therefore the same `529` wrapper.
- Explicitly handle the `group_sex_to_h` transition as a targeted group-context reduction, not as a mode-off effect: it uses a `9999` no-op effect chain and does not pass through `529` or `10011`.
- Treat `group_sex_npc_hp_0_end` as a single-NPC exit, not a full group end: release the exiting NPC's own pending edge counts before its `END_H_ADD_HPMP_MAX` (`528`) and `SELF_H_STATE_RESET` (`403`) path if needed, but never release unrelated participants who remain in group sex.
- Cover unconscious-recovery group-sex shutdown, where `recover_from_unconscious_h()` directly clears group templates and turns group mode off without passing through the full group-end effect chain.
- Keep core game files unchanged; implement through the local mod layer.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `local-bugfixes`: Add a group-sex end bugfix that releases pending edge orgasms before group or scoped participant H state is reset.

## Impact

- Affected mod: `mod/local_bugfix` or an equivalent local bugfix mod hook.
- Affected active feature: `mod/group_sex_extension` "全员寸止" command, because it can create the pending edge state being released.
- Affected core paths by hook/wrapper only: `group_sex_end`, `group_sex_pl_hp_0_end`, discovered-interrupt routing to `GROUP_SEX_END`, `group_sex_npc_hp_0_end`, `group_sex_to_h`, `recover_from_unconscious_h()` group shutdown, group-sex behavior effect ordering, and second-stage orgasm settlement.
- Unaffected global behavior: `DESIRE_POINT_TO_0` (`1503`) remains a shared effect and must not be globally wrapped for this fix.
- Tests should cover pending edge release before group end reset, no-op behavior when no participants are edged, ordering before group end HP/MP max settlement, discovered interrupt, targeted group-context reduction, unconscious-recovery shutdown before template clear/mode off, and no accidental all-participant release on single-NPC exit.
