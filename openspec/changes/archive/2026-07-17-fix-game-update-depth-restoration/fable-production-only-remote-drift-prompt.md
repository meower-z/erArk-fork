/investigate-game-bug
/review-erark-pr-artifacts

请作为 erArk bugfix program 的 Fable 发布监督者，判断一次意外远端漂移后的最小安全处理。不要编辑文件，不要授予 push 权限。

用户要求：不要把自动化测试提交到 upstream；上游仓库没有测试。用户此前授权把修复提交到 fork repo 的 side branch 供审核，但本轮 Codex 不会把该旧授权解释为新的强制改写授权。

已核实的当前状态：

- 当前 `upstream/master`：`3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`。
- 本地 production-only side branch：`bc1bfb44ea5f7ae6b12e97788c5e4f063f21aaa8`，直接基于上述 upstream，单提交只修改 `Script/Design/update.py`（5+/4-），提交树中没有 `tests/`。
- 本地自动化回归只保存在未跟踪 `local_tests/` 与 `.codex-evidence/`，不会进入远端候选。
- 远端 `pr-fork/codex/fix-game-update-depth-restoration` 在 Codex 未操作的情况下，从旧候选 `80a711603` 变成了 `23188ce1afba4cd670542a7428d18d778d546968`。
- `23188ce1a` 是 GitHub 在 2026-07-14 19:30 UTC 创建的 merge commit，父提交为旧候选 `80a711603` 和当前 upstream `3a1c9e620`。
- 因为旧候选是父提交，远端相对 upstream 的拟提交 diff 仍包含 `Script/Design/update.py` 和 `tests/test_game_update_depth_restoration.py`；不能把远端称为 production-only。
- 没有创建 PR。

请明确回答：

1. 是否仍应保持本地 production-only 代码不变。
2. 若用户单独授权远端改写，是否应使用精确 lease：
   `git push --force-with-lease=refs/heads/codex/fix-game-update-depth-restoration:23188ce1afba4cd670542a7428d18d778d546968 pr-fork bc1bfb44ea5f7ae6b12e97788c5e4f063f21aaa8:refs/heads/codex/fix-game-update-depth-restoration`
3. 普通 merge/rebase/push 为什么不能满足“候选完整历史不含测试”的要求。
4. 在获得新授权前是否必须停止，不得 push。
5. 这次远端漂移是否改变此前结论：代码 PASS、文案 PASS、上游 PR artifact 仅因缺少真实 Tk A/B 而 BLOCKED。

输出简洁判定，不要生成 PR 文案。
