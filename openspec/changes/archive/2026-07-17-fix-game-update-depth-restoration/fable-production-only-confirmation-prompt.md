/investigate-game-bug

请作为 erArk bugfix program 的 Fable 决策监督者，重新确认下面这个 scope 变更。不要编辑文件，也不要授予外部动作权限。

用户明确要求：不要把自动化测试提交到 upstream，因为上游仓库没有测试。Codex 因此把自动化测试保留为本地未跟踪证据，并把候选分支改写为只含生产代码的单个提交。

当前事实：
- upstream/master 当前为 3a1c9e620（tag 2026.7.14）。
- 本地 side branch HEAD 为 bc1bfb44e，基于该 upstream/master，ahead 1。
- proposed diff 只有 Script/Design/update.py，5 insertions / 4 deletions；没有 tests/、OpenSpec、生成数据或证据文件。
- 原自动化测试逐字保存在 candidate 的 untracked local_tests/ 以及 main 的 .codex-evidence/；二者 SHA256 都是 6a0a156b37a5d386994980941b8418abe16f80ec697ba44d52c8245c018e5bf5。
- 在最终 production-only HEAD 上运行本地测试仍为 4 passed；py_compile 和 diff-check 通过。这些是本地验证，不会随 PR 提交。
- 真实 Tk 取证仍没有进入嵌套分支，因此没有可用 baseline/candidate A/B。
- fork 远端同名 side branch 仍指向旧提交 80a711603，旧提交包含 tests/；尚未更新远端。

请固定输出：
1. `CODE: PASS | REVISE | BLOCKED`：production-only diff 是否仍正确且适合 side-branch review。
2. `UPSTREAM SCOPE: PASS | REVISE | BLOCKED`：不提交 tests/ 是否符合用户要求，是否还需往生产代码加入替代自检（请避免凭空扩 scope）。
3. `PR DRAFT REQUIREMENT`：旧 draft 中“随本 PR 提交了自动化测试”和四条测试断言是否必须全部删除；本地测试能否出现在 PR-facing 文案中。
4. `REMOTE UPDATE`：从技术上，为保证同名 fork branch 的整个候选历史也不包含 tests/，是否应以 `--force-with-lease` 把远端 80a711603 替换为本地 bc1bfb44e；只做技术判断，不视为授权。
5. 必须修改项；若没有，明确“无需修改生产代码”。

完整候选提交：

````text
commit bc1bfb44ea5f7ae6b12e97788c5e4f063f21aaa8
Author:     meower-z <299913659+meower-z@users.noreply.github.com>
AuthorDate: Tue Jul 14 11:26:34 2026 +0000
Commit:     meower-z <299913659+meower-z@users.noreply.github.com>
CommitDate: Tue Jul 14 19:33:32 2026 +0000

    修正游戏更新嵌套深度恢复
---
 Script/Design/update.py | 9 +++++----
 1 file changed, 5 insertions(+), 4 deletions(-)

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
