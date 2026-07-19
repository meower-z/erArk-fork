## Why

When an NPC discovers an active H scene and accepts an invitation into group sex, the discovery panel can leave that NPC outside the settled H state. The target then lacks normal group actions while both "invite group sex" and "end group sex" can appear, revealing inconsistent participant state and scene-level premises.

## What Changes

- Make discovery-panel admission settle the discoverer's JOIN/DISCOVER behavior exactly once regardless of whether the panel was opened from the NPC behavior loop or a direct hidden-discovery call.
- Preserve the intended ordering for initial conversion into group mode so nested player settlement cannot erase the discoverer's pending admission.
- Make the scene-wide "all characters are not in H" premise inspect every eligible NPC instead of returning after the first character.
- Keep acceptance, refusal, tired auto-leave, hidden discovery, and later outer NPC settlement from replaying or dropping behavior effects.
- Verify that switching the player target to the admitted NPC exposes the normal group-action interface and removes the contradictory invite control.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-bugfixes`: Adds source-independent, exactly-once admission and complete scene-H premise requirements for discovered group participants.

## Impact

- Affects the local group participant admission component, the H discovery panel integration, premise registration, and near-real group discovery tests.
- Does not change group templates, consent rolls, fatigue thresholds, or ordinary direct invitation behavior.

## Current Status

The full-scene premise correction is a narrow written candidate. On 2026-07-10 the user decided to postpone the exact-once settlement work: the global context/suppression experiment is removed from the worktree, and only the `place_all_not_h` premise fix proceeds to verification. The exact-once defect and its audit remain recorded in `implementation-notes.md` for a future dispatch-scoped ownership design.
