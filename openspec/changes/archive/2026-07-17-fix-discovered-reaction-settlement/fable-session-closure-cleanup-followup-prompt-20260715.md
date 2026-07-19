/investigate-game-bug

只读 follow-up，不得修改文件、Git 或 PR。主仓库 `/home/ubuntu/games/erArk`，change 为 `openspec/changes/fix-discovered-reaction-settlement/`。你上一轮 PASS 的唯一 required finding 是两个 PR #218 final-rerun disposable roots 尚未删除。

请只核验：

1. `/tmp/erark-pr218-final-tk-rerun-20260715/` 和 `/tmp/erark-pr-images/discovery-settlement/pr218-final-rerun-20260715/` 已不存在，Git worktree registrations 也不存在；
2. append-only archive 仍存在且 `sha256sum -c CHECKSUMS.sha256` 通过；
3. allocator 不再列出本次 replay owner，且没有触碰无关 owner；
4. 新增 `focused-test-matrix-20260715.md` 的 29-case 计数与最终本地测试合同一致，`session-closure-20260715.md` 没有夸大其已提交进 main history；
5. 三个 discovery worktree 不再有本任务的未跟踪测试目录，干净 PR candidate worktree/branch 未被改动。

输出简洁明确的 `PASS` 或 `FAIL` 和任何必须修正 finding。不要重跑 GUI、测试或完整 PR 审查。
