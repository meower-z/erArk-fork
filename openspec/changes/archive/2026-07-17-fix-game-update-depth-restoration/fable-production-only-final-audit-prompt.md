/investigate-game-bug
/review-erark-pr-artifacts

请作为全新上下文的 erArk 上游 PR artifact reviewer，严格审计下面的 production-only 候选和 Fable 5 高强度会话修订后的 PR draft。不要编辑文件或改写文案。按 review-erark-pr-artifacts 返回 PASS、REVISE 或 BLOCKED，并分别说明代码/文案是否通过、是否只因真实 Tk 前后证据缺失而阻断上游 PR。

候选身份：

- base: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`
- head: `bc1bfb44ea5f7ae6b12e97788c5e4f063f21aaa8`
- proposed diff 只有 `Script/Design/update.py`，5 insertions / 4 deletions。
- upstream 当前没有 `tests/` 树；用户明确要求不要把自动化测试提交到 upstream。
- 自动化测试只作为本地未跟踪证据保存，绝对不能出现在 PR-facing 文案、diff 或对外证据中。

已经在 base/current source 中直接确认：

- `Script/Design/handle_npc_ai_in_h.py:155` 定义 `recover_from_unconscious_h()`。
- 该函数在 `Script/Design/handle_npc_ai_in_h.py:256` 调用 `update.game_update_flow(5)`。
- `Script/Settle/default.py:7105` 在角色结算路径调用 `recover_from_unconscious_h(character_id)`。

完整 proposed diff：

```diff
diff --git a/Script/Design/update.py b/Script/Design/update.py
index 9caffd5fe..fcd4340d8 100644
--- a/Script/Design/update.py
+++ b/Script/Design/update.py
@@ -13,8 +13,9 @@ def game_update_flow(add_time: int):
     if cache_control.cache.game_update_flow_running >= 2:
         return

-    # 设置游戏更新流程运行标志
-    cache_control.cache.game_update_flow_running += 1
+    # 保存调用者深度，并进入当前更新层级
+    caller_depth = cache_control.cache.game_update_flow_running
+    cache_control.cache.game_update_flow_running = caller_depth + 1

     try:
         # 去掉了第一次结算
@@ -23,5 +24,5 @@ def game_update_flow(add_time: int):
         character_behavior.init_character_behavior()
         py_cmd.focus_cmd()
     finally:
-        # 无论是否发生异常，都要清除运行标志
-        cache_control.cache.game_update_flow_running = 0
+        # 无论是否发生异常，都恢复调用者进入前的深度
+        cache_control.cache.game_update_flow_running = caller_depth
```

完整 PR draft：

```markdown
Title: 修复 game_update_flow 嵌套调用返回后运行深度被误清零的问题

Body:

## 问题

`Script/Design/update.py` 的 `game_update_flow()` 用 `cache.game_update_flow_running` 记录更新流程的运行深度，并在深度达到 2 时拦截更深的嵌套调用。生产代码中存在嵌套路径：角色结算过程中，`recover_from_unconscious_h()` 会再次调用 `game_update_flow(5)`。旧实现在每一层的 `finally` 中都把标志固定清零，于是内层调用返回时，外层流程明明还在运行，深度却已被清成 0。此后该标志不再能正确反映外层仍在运行，后续的防重入判断失去了正确的深度依据。

## 修复

进入 `game_update_flow()` 时先保存调用者的深度 `caller_depth`，再将 `cache.game_update_flow_running` 置为 `caller_depth + 1`；`finally` 中不再固定清零，而是恢复为 `caller_depth`。这样每一层退出时只撤销自己增加的那一层深度，嵌套调用返回后外层深度保持正确。`>= 2` 的守卫阈值不变，时间推进、角色结算与聚焦的执行顺序也不变。
```

PR-facing evidence：无截图、GIF、玩家路线或外部证据。真实 Tk 尽力探索没有进入修改分支，因此不得把调查过程写进 draft，也不得发明 A/B。用户此前允许在难以取得证据时仍把小修提交到 fork side branch 供审核；这不等于创建上游 PR 或豁免项目的视觉证据规则。

重点核对：

1. draft 是否完全没有测试内容。
2. “后续的防重入判断失去了正确的深度依据”是否是由旧代码和已确认嵌套路径直接支持的条件/不变量陈述，而不是声称已观察到第三次进入。
3. production diff 是否仍是最小、语义正确且不改变守卫阈值或 try-body 顺序。
4. 若唯一剩余问题是缺少真实 Tk A/B，请明确写成：代码 PASS、文案 PASS、上游 PR artifact 仅证据 BLOCKED；不要要求再改生产代码或 PR 文案。
