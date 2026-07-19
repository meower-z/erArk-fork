/investigate-game-bug
/review-erark-pr-artifacts

请作为全新上下文的 erArk 上游 PR artifact reviewer，严格审计下面 production-only proposed diff 和 Fable high-effort draft。不要编辑或改写。按 review-erark-pr-artifacts 输出 PASS、REVISE 或 BLOCKED，并提供 publication_state、visibility ledger、cumulative prefix audit 和带 draft 行号的 findings。

候选身份：
- base: upstream/master 3a1c9e620。
- head: bc1bfb44e。
- proposed diff 只有 Script/Design/update.py；没有 tests/、fixture、生成数据或证据文件。

PR-facing evidence：无自动化测试、无截图/GIF、无外部 evidence。自动化测试只存在本地未跟踪目录，必须视为 local-only，不可用来替 draft 辩护。

请特别检查：
- draft 是否已完全删除所有自动化测试、命令、数量与断言结论。
- 所有行为主张是否能由 upstream 源码与 production diff 静态支持；尤其“新的进入会被当作第一层放行，>=2 守卫实际失效”是否超出 proposed diff/静态调用路径所能证明。
- 没有真实 Tk A/B 是否仍是 behavior-changing PR 的 BLOCKED 条件。
- writer 使用命令 `claude -p --model claude-fable-5 --effort high --tools "" --no-session-persistence`，满足 high-effort 要求。

完整 proposed diff：

````diff
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
````

完整 draft（从第 1 行编号）：

````markdown
# PR Draft

## Title

修复 game_update_flow 嵌套调用返回后运行深度被误清零的问题

## Body

## 问题

`Script/Design/update.py` 的 `game_update_flow()` 用 `cache.game_update_flow_running` 记录更新流程的运行深度，并在深度达到 2 时拦截更深的嵌套调用。但生产代码中存在嵌套路径：角色结算过程中经 `recover_from_unconscious_h()` 会再次调用 `game_update_flow(5)`。旧实现在每一层的 `finally` 中都把标志固定清零，于是内层调用返回时，外层流程明明还在运行，深度却已被清成 0。此后在外层剩余的执行期间，新的进入会被当作第一层放行，`>= 2` 的防重入守卫实际失效。

## 修复

进入 `game_update_flow()` 时先保存调用者的深度 `caller_depth`，再将 `cache.game_update_flow_running` 置为 `caller_depth + 1`；`finally` 中不再固定清零，而是恢复为 `caller_depth`。这样每一层退出时只撤销自己增加的那一层深度，嵌套调用返回后外层深度保持正确。`>= 2` 的守卫阈值不变，时间推进、角色结算与聚焦的执行顺序也不变。
````
