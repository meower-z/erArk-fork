## 2026-07-14 本地实现验证

- 候选 worktree：`/home/ubuntu/games/erArk-pr-game-update-depth`
- 候选分支：`codex/fix-game-update-depth-restoration`
- 基线：`upstream/master` 的 `abebf33b52ebf51424f71365946eb8df1f75a23c`
- 源级核对确认 `update.game_update_flow()` 是当前 `game_update_flow_running` 的唯一运行时写入者；存档加载只把该非持久运行状态初始化为零。这个所有权结论来自源搜索，不是测试结论。

红阶段通过真实 `game_update_flow()` 入口运行四个隔离回归：同一外层的两次先后嵌套实际观察为 `[1, 2, 0, 1, 0]`，嵌套异常返回实际观察为 `[1, 2, 0]`，两者按规格失败；最外层异常恢复零以及 depth≥2 拒绝且无副作用按既有规则通过。

候选只保存调用者进入前深度、进入时写入加一值，并在 `finally` 恢复调用者深度。green 验证结果：

```text
python -m pytest -q tests/test_game_update_depth_restoration.py
....                                                                     [100%]
4 passed in 0.02s

python -m py_compile Script/Design/update.py tests/test_game_update_depth_restoration.py
通过

git diff --check
通过

openspec validate fix-game-update-depth-restoration --strict
Change 'fix-game-update-depth-restoration' is valid
```

Fable 最终审计返回 PASS，确认候选精确满足深度恢复 contract、四个测试覆盖顺序嵌套/正常与异常退出/depth 上限，且 design 中的非嵌套队列 follow-up 没有进入当前实现。发布限制仍按 `tasks.md` 的显式 blocker 保留：此前置修复不能单独声称上游发布就绪。

## 2026-07-14 Tk 尽力取证与 fork side branch

- 真实 Tk、固定 Python/NumPy/PYTHONHASHSEED `20260714` 的 99 号档路线复现了等待后连续高潮文本，但 trace 只有最外层调用；97 号档普通等待完整返回也只有单层 `0 -> 0`。两条路线均未进入本候选的嵌套分支，因此没有制作无因果 A/B。完整记录在 `.codex-evidence/game-update-depth-restoration/runtime-manifest.md` 与 `action-log.md`。
- 用户明确授权在证据不足时仍可发布 fork side branch 供审核。Fable 最终裁定 `CODE: PASS`、`SIDE-BRANCH REVIEW STATE: ACCEPT`、`PR ARTIFACT STATE: BLOCKED`，且无需修改代码。
- 已推送 `80a711603734eb3913a608bbece79059aae0e08a` 到 `pr-fork/codex/fix-game-update-depth-restoration`；没有创建 PR。side branch publication 与上游 PR readiness 明确分离。
