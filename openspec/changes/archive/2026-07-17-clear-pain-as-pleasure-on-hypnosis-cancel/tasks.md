## 1. Confirm The Reversed Boundary

- [x] 1.1 Preserve the successful fable-5 prompt and verdict in this change and record the selected five-field helper boundary
- [x] 1.2 Validate the updated `investigate-game-bug` archive-before-cleanup workflow

## 2. Correct The Candidate

- [x] 2.1 Add `pain_as_pleasure = False` to the existing shared helper without moving caller-specific logic
- [x] 2.2 Update focused local checks for direct cancellation, unchanged sleep cleanup, and untouched neighboring state

## 3. Verify The Production Diff

- [x] 3.1 Run the focused checks, inspect the changed source, and confirm the proposed production diff contains only the selected semantic correction

## 4. Re-record And Preserve Tk Evidence

- [x] 4.1 Prepare exact baseline and corrected-candidate runtimes from the archived reproduction save
- [x] 4.2 Capture a comparable direct-cancellation A/B through the supervised frame-by-frame Tk workflow
- [x] 4.3 Re-open the final media, verify the expected status difference, and archive the media and replay package under `~/games/archive`
- [x] 4.4 Remove task-owned `/tmp` runtimes and disposable capture directories only after archive verification, then confirm they are gone

## 5. Review The Local Result

- [x] 5.1 Re-read the change artifacts and final diff, record remaining local integration impact, and stop before push, asset publication, or PR edits

## 6. Publish And Wait

- [x] 6.1 Rebase the candidate onto current upstream `master`, amend the one-line semantic correction, and update the existing PR branch with an exact force-with-lease
- [x] 6.2 Publish the approved replacement evidence at commit-pinned URLs and update PR #213's title and body
- [x] 6.3 Verify the live two-file diff, rendered evidence, review threads, and final publication-ready artifact review
- [ ] 6.4 Maintainer merges PR #213 — external wait state; no further action is required from this session while the PR remains open

Current handoff state (2026-07-14): PR #213 is open, non-draft, and waiting for merge at head `fe57f98a08368bb2247605d6362cbdc2475edc1d`. Preserve the worktree and archived evidence. Do not push, edit, comment, rebase, recapture evidence, or clean up PR-owned local state unless the user gives new instructions. After a confirmed merge, cleanup still requires separate authorization.

## 归档收尾（2026-07-17）

本 change 已完结并归档：对应上游 PR #213「修复：解除催眠后"苦痛快感化"未被一并解除」已合并（上游提交 b87732664）。tasks.md 中唯一未勾的 6.4 项为「等待维护者合并 PR #213」的外部等待状态，现已满足。实现（解除催眠时清除 pain_as_pleasure 子状态）已交付上游，目录仅作历史记录保留。
