/investigate-game-bug

请作为 erArk 上游 PR 文案作者，用中文重写下面这个 production-only 候选的 PR title 和 body，供用户审核。输出只能包含一行 `Title: ...`，然后 `Body:` 和完整 Markdown 正文；不要输出审计结论、解释或备选。

硬性边界：
- proposed diff 只有 Script/Design/update.py，不包含 tests/。
- 自动化测试只在本地未跟踪证据中，按项目技能规则不得出现在 PR-facing 文案中。
- 删除旧 draft 的整个“验证”章节及所有“随本 PR 提交自动化测试”、测试序列、测试用例断言、pytest 等内容。
- 没有可用 Tk baseline/candidate A/B；不要写截图、GIF、玩家可见验证或任何虚构证据。
- 不声称修复了重复高潮、时间显示或用户截图里的具体输出。
- 不提 branch、commit、fork、worktree、OpenSpec、Fable、agent、本地测试或私有调查。
- 不写文件清单、non-goal 清单或 rejected design。

正文只保留 `## 问题` 和 `## 修复` 两节。问题说明生产代码存在从角色结算进入 `recover_from_unconscious_h()` 后再次调用 `game_update_flow(5)` 的嵌套路径；旧实现每层 finally 固定清零，使内层返回时外层仍在运行却丢失深度。修复说明保存 `caller_depth`、进入时加一、finally 恢复；>=2 守卫阈值和时间/结算/聚焦顺序不变。

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
