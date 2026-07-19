# Implementation Notes

## Upstream State Recorded 2026-07-11

- Pull request: `https://github.com/Godofcong-1/erArk/pull/206`
- State at inspection: open and ready for review, base `master`, head `meower-z:codex/fix-hidden-sex-witness-dedup`
- Title: `修复玩家未移动时同一角色重复发现 H 行为`
- Commit: `5928fbf81ceaa33cc1807686c95a5f0f7edec022` (`fix: skip handled hidden-sex witnesses`)
- Author and committer identity: `meower-z <299913659+meower-z@users.noreply.github.com>`
- Upstream changed-file boundary: only `Script/System/Sex_System/hidden_sex_panel.py`, with two added lines
- Screenshot asset commit: `5ba724a6be4b4062e9516bcf90da815a29f7334f` on `meower-z/erArk-fork:assets`

The live PR body was read back before this record was written. It states the accepted contract in reader order: the discovery panel is introduced before its repeated appearance, multiple triggers are examples rather than scope, and movement is the reset boundary.

## Accepted Behavioral Scope

The defect is repeated selection of an already handled hidden-sex discoverer. Talk-away followed by return and a single action causing several discovery evaluations are reproductions of the same issue. While the player remains at the same location, each character can open the H discovery panel at most once; movement resets the existing marker and permits later discovery. Other not-yet-handled characters remain eligible in the existing order.

Ordinary H discovery and exposure discovery are not part of this source change: those paths already consult their witnessed-player premise. The shared nearby-character helper also remains unchanged; filtering occurs only at final hidden-sex discoverer selection.

## Transitional Local Ownership

The overlapping local behavior currently lives in `mod/local_group_participant_admission_fix`, whose other tired-character and participant-admission responsibilities remain independent. Upstream merge must therefore lead to surgical removal of the hidden-sex filter and its dedicated coverage, not deletion of the component.

No local cleanup is authorized by an open PR alone. Tasks 2.1 through 3.2 remain the continuation boundary.

## Evidence

- Before: `https://raw.githubusercontent.com/meower-z/erArk-fork/5ba724a6be4b4062e9516bcf90da815a29f7334f/pr-206/before.png`
- After: `https://raw.githubusercontent.com/meower-z/erArk-fork/5ba724a6be4b4062e9516bcf90da815a29f7334f/pr-206/after.png`

The screenshots use the same natural scene before and after the source fix so the repeated panel and its suppression are visible without treating multi-orgasm behavior as the requirement.

## Upstream Adoption Recorded 2026-07-13

- PR #206 merged as `e8a865c4a11d496bc11d29f8af2c9a1a617af9ad` from source commit `5928fbf81ceaa33cc1807686c95a5f0f7edec022`.
- Current `main` and `upstream/master` have no diff in `Script/System/Sex_System/hidden_sex_panel.py`.
- The retained `local_group_participant_admission_fix` no longer filters hidden-sex candidates or replaces the core all-not-H premise; its README assigns both rules to upstream PRs #205/#206.
- The combined focused verification for the retained component, its BDD path, save portability, and assumed-upstream overlays passed: `43 passed`.
- The full `.venv/bin/pytest mod/tests -q` gate is not green: `test_instruct_settlement_advances_game_time` does not advance Web game time, and `test_hypnosis_cancel_clears_pain_as_pleasure_flag` conflicts with the current pain-as-pleasure lifecycle. Neither failure exercises hidden-sex witness selection or participant admission, but task 2.4 remains open until the configured suite is green.
