# Implementation Notes

## Upstream State Recorded 2026-07-11

- Pull request: `https://github.com/Godofcong-1/erArk/pull/207`
- State at inspection: open and ready for review, base `master`, head `meower-z:codex/fix-cross-platform-save-paths`
- Title: `修复跨系统读档后房间地址不匹配导致的场景角色丢失`
- Commit: `2dd4e9d6bc9f743a830ba8761d3bb1f214d5173d` (`fix: normalize cross-platform save paths`)
- Author and committer identity: `meower-z <299913659+meower-z@users.noreply.github.com>`
- Upstream changed-file boundary: only `Script/Core/save_handle.py`, with 80 additions and two deletions
- Screenshot asset commit: `d038c4622c95ed4ae4a93b26e0176da61f7f8e82` on `meower-z/erArk-fork:assets`

The live PR body and source diff were read back before this record was written. The implementation normalizes the loaded cache immediately after `pickle.load()` returns and before `input_load_save()` performs later update work.

## Accepted Behavioral Scope

The saved room address is a game identifier assembled using the operating system's separator; it is not a filesystem library object. Compatibility therefore belongs at the save deserialization boundary rather than in map lookup or rendering.

The source fix enumerates scene keys and `scene_path`, map keys and `map_path`, character `dormitory` and `pre_dormitory`, `work.dormitory_admin_target_room`, `pl_ability.air_hypnosis_position`, Rhodes Island `facility_damage_data` keys, and `maintenance_place` values. It does not recursively rewrite ordinary strings. Native path-keyed dictionaries remain unchanged when no conversion is required.

The user-facing proof is an ordinary Windows-format save loaded on Linux in Tk mode. Before the fix, the scene loses the player registration and raises `KeyError: 0`; after the fix, the game immediately shows the normal scene with the player and four nearby characters. No special H or group state is part of the current PR contract or evidence.

## Historical Audit Boundary

The archived 2026-07-07 audit remains historical evidence of the original diagnosis and earlier live reproduction. It is not rewritten to match this later PR presentation. This active change supersedes that evidence as the continuation point for upstream adoption and deliberately uses the ordinary-load scenario.

## Transitional Local Ownership

`mod/local_cross_platform_save_fix` remains enabled until an upstream merge is present in the private branch and passes the focused compatibility checks. An open PR is not enough to remove it. Tasks 2.1 through 3.2 are the continuation boundary.

## Evidence

- Before: `https://raw.githubusercontent.com/meower-z/erArk-fork/d038c4622c95ed4ae4a93b26e0176da61f7f8e82/pr-fix-cross-platform-save-paths/before.png`
- After: `https://raw.githubusercontent.com/meower-z/erArk-fork/d038c4622c95ed4ae4a93b26e0176da61f7f8e82/pr-fix-cross-platform-save-paths/after.png`

## Upstream Adoption Recorded 2026-07-13

- PR #207 merged as `16960e1b89e72da0d5a31ef5e716c0368cd0b924` from source commit `2dd4e9d6bc9f743a830ba8761d3bb1f214d5173d`.
- Current `main` and `upstream/master` have no diff in `Script/Core/save_handle.py`.
- `mod/local_cross_platform_save_fix` and its enabled/load-order entries are absent.
- The combined focused verification for save portability, participant admission, and assumed-upstream overlays passed: `43 passed`.
- The full `.venv/bin/pytest mod/tests -q` gate is not green: `test_instruct_settlement_advances_game_time` does not advance Web game time, and `test_hypnosis_cancel_clears_pain_as_pleasure_flag` conflicts with the current pain-as-pleasure lifecycle. Neither failure exercises save portability, but task 2.5 remains open until the configured suite is green.
