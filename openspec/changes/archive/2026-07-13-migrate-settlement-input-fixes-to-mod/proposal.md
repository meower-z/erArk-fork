## Why

The current settlement wait and skip fixes were prototyped as direct edits to upstream game files, which violates this workspace's maintained-local-fix boundary and makes upgrades difficult. Preserve the prototype on a temporary branch, then re-express every viable fix as an independently testable local mod while leaving upstream source clean.

## What Changes

- Add a maintained `local_settlement_input_fix` mod that installs narrow wrappers for Web waits, event/talk pacing, and skip-flag ownership without copying whole upstream functions where a wrapper is sufficient.
- Add a separate `local_npc_move_talk_context_fix` mod for the independently rooted bug where NPC paper-doll movement text is formatted with the player's identity and scene.
- Keep upstream `Script/`, `static/`, and shared test-driver files unchanged on the working branch.
- Classify each prototype edit as migrated, unnecessary, or not representable by the current mod loader; do not silently retain unportable core edits.
- Add focused component tests plus direct Tk GUI verification performed by an interactive agent rather than a scripted BDD driver.
- Record patch points, load-order assumptions, behavioral evidence, residual risks, and future upstream-migration guidance.

## Capabilities

### New Capabilities
- `settlement-input-fix-mod`: Defines the maintained local mod behavior for settlement waits, per-event pacing, and scoped skip ownership.
- `npc-move-talk-context-fix`: Defines NPC movement paper-doll text ownership without changing other paper-doll behavior.

### Modified Capabilities
- `local-mod-componentization`: Requires maintained local fixes to leave upstream game files clean and document any behavior that cannot be represented by the mod loader.

## Impact

- Adds `mod/local_settlement_input_fix/` and enables it in `mod/mod_config.json`.
- Adds component-level regression tests and OpenSpec maintenance documentation.
- Interacts with `local_performance`, Web draw adapters, dialog handling, map/navigation movement, and timed waits.
- Does not include the protected localization files or the unrelated project skill.
