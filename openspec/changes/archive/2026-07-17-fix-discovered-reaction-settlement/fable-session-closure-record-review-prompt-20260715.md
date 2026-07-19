/investigate-game-bug

只读核验，不得修改任何文件、Git 分支或 GitHub PR。主仓库为 `/home/ubuntu/games/erArk`，OpenSpec change 为 `openspec/changes/fix-discovered-reaction-settlement/`，最终 Tk 证据归档为 `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/`。

请实际读取该 change 的 `proposal.md`、`design.md`、`tasks.md`、`implementation-notes.md`、`tk-final-pr218-rerun-contract-20260715.md`、`session-closure-20260715.md`，并读取归档中的 manifest、comparison metrics、save hashes、action log、checksums 和两张 final PNG。只核验以下事项：

1. 最终记录是否忠实描述 PR #218 exact base `94d586840484adf21fcf746dba0444551dd6a5a1`、head `4e226f4f587b82a87368a3d7976650593323a7b4` 的真实 Tk 重跑；
2. 新 baseline/candidate 是否分别与 PR before/after 像素一致，且游戏可见语义描述准确；
3. 是否如实记录 partial redraw、存档不变、WAIT 未覆盖、PR 未修改和归档校验；
4. `session-closure-20260715.md` 是否完整汇总本 session 的持久知识，同时诚实区分“位于 main worktree”与“已提交进 main history”；
5. 有无必须修正的遗漏、矛盾或无证据断言。

输出简洁明确的 `PASS` 或 `FAIL`，并列出任何必须修正的 finding。不要重新设计修复，不要建议修改 PR，不要执行测试或 GUI 重跑。
