# Fable publication supervision

## Final code and side-branch confirmation — 2026-07-14

### Exact prompt

`````text
/investigate-game-bug

请作为 erArk bugfix program 的 Fable 决策监督者，对下面这个已经提交到本地 side branch、尚未 push 的候选做最终技术确认。不要编辑文件，不要代替用户授权外部动作。用户已经明确授权：先尽力取证；即使没有可用 Tk A/B，只要 Codex 与 Fable 确认代码，就把候选 push 到 fork repo 的 side branch；不开 PR，由用户先审核。

请把三件事严格分开：
1. 候选代码/测试本身是否正确、最小、适合发布到 fork side branch 供人审核；
2. 缺少真实可见 A/B 是否影响代码正确性，还是只影响 PR artifact readiness；
3. 当前 PR draft 是否仍需修订/证据，不能因为允许 push 就把它误判为已满足上游 PR 门槛。

输出固定结构：
- `CODE: PASS | REVISE | BLOCKED`
- `SIDE-BRANCH REVIEW STATE: ACCEPT | DEFER`（这只是技术判断，不是外部动作授权）
- `PR ARTIFACT STATE: PASS | REVISE | BLOCKED`
- `Reasoning`：逐项解释；若代码需要改，给出精确必要修改；若代码无需改，明确说“无需修改代码”。
- `Next`：说明 push 后用户审核时必须知道的证据限制，以及 PR draft 下一步。

候选身份：
- upstream/master 当前仍为 abebf33b52ebf51424f71365946eb8df1f75a23c。
- local branch: codex/fix-game-update-depth-restoration。
- local commit: 80a711603734eb3913a608bbece79059aae0e08a。
- pr-fork 上同名 branch 当前不存在。
- 候选 worktree tracked status 为空。

自动化证明：
- 候选上 `pytest -q tests/test_game_update_depth_restoration.py` 为 4 passed。
- 同一测试在基线旧实现上 red-capable：顺序嵌套测试得到 `[1,2,0,1,0]` 而期望 `[1,2,1,2,1]`；嵌套异常测试得到 `[1,2,0]` 而期望 `[1,2,1]`；最外层异常恢复 0 与 depth>=2 拒绝路径在基线也通过。
- `py_compile`、`git diff --check` 通过。

上游源码静态核对：
- 运行期只有 `Script/Design/update.py` 写 `game_update_flow_running`；`game_type.py` 初始化为 0，`save_handle.py` 读档时重置为 0。
- 生产代码确有嵌套入口：`realtime_settle.settle_sleep_h -> handle_npc_ai_in_h.judge_weak_up_in_sleep_h -> recover_from_unconscious_h -> update.game_update_flow(5)`；`default.handle_recover_from_unconscious_add_adjust` 也可进入同一恢复函数。

真实 Tk 尽力取证结果（fixed Python/NumPy/PYTHONHASHSEED=20260714，真实 Tk，allocator display :32）：
- 99 号档是用户截图附近的群交场景。一次“等待五分钟”确实显示凯尔希阴道小绝顶，随后显示凯尔希心理绝顶；但观察窗口内 trace 只有外层 `CALL add_time=5 depth_before=0`，档内没有 unconscious_h。它复现线索，但没有进入此次修改分支。
- 97 号档含一个 unconscious_h=3 角色，但普通“等待五分钟”完整返回的 trace 只有 `CALL depth_before=0` -> `RETURN depth_after=0`，中间没有第二次 CALL，也没有恢复提示。
- 因两条候选路线都没进入嵌套分支，没有运行 baseline/98，也没有制作无因果 before/after。要得到真实 A/B，需要另一个天然位于“无意识 H 即将恢复、且外层 update 仍在运行”的保存点。
- 这些诊断截图不作为 PR evidence。

现有 Fable PR artifact reviewer 在取证前给过 BLOCKED：硬 blocker 是没有真实 Tk A/B；另有 draft 措辞问题——“实际失效”缺生产触发证明，以及“旧实现记录到”暗示提交了运行记录。上述静态路径现在只证明生产嵌套入口存在，Tk 探索仍没有证明一个可见 A/B。

完整候选提交：

````text
commit 80a711603734eb3913a608bbece79059aae0e08a
Author:     meower-z <299913659+meower-z@users.noreply.github.com>
AuthorDate: Tue Jul 14 11:26:34 2026 +0000
Commit:     meower-z <299913659+meower-z@users.noreply.github.com>
CommitDate: Tue Jul 14 11:26:34 2026 +0000

    修正游戏更新嵌套深度恢复
---
 Script/Design/update.py                     |   9 +-
 tests/test_game_update_depth_restoration.py | 157 ++++++++++++++++++++++++++++
 2 files changed, 162 insertions(+), 4 deletions(-)

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
diff --git a/tests/test_game_update_depth_restoration.py b/tests/test_game_update_depth_restoration.py
new file mode 100644
index 000000000..f7458e58d
--- /dev/null
+++ b/tests/test_game_update_depth_restoration.py
@@ -0,0 +1,157 @@
+# -*- coding: UTF-8 -*-
+"""游戏更新嵌套深度生命周期回归测试。"""
+
+import importlib.util
+import sys
+from pathlib import Path
+from types import ModuleType, SimpleNamespace
+
+import pytest
+
+
+REPO_ROOT = Path(__file__).resolve().parents[1]
+UPDATE_PATH = REPO_ROOT / "Script" / "Design" / "update.py"
+
+
+def load_update_module():
+    """参数：无；返回：更新模块、缓存、调用记录与恢复函数；用途：通过真实入口隔离验证深度生命周期。"""
+    missing = object()
+    module_names = [
+        "Script",
+        "Script.Design",
+        "Script.Design.character_behavior",
+        "Script.Design.game_time",
+        "Script.Core",
+        "Script.Core.py_cmd",
+        "Script.Core.cache_control",
+        "game_update_depth_under_test",
+    ]
+    old_modules = {name: sys.modules.get(name, missing) for name in module_names}
+
+    script_module = ModuleType("Script")
+    design_module = ModuleType("Script.Design")
+    character_behavior = ModuleType("Script.Design.character_behavior")
+    game_time = ModuleType("Script.Design.game_time")
+    core_module = ModuleType("Script.Core")
+    py_cmd = ModuleType("Script.Core.py_cmd")
+    cache_control = ModuleType("Script.Core.cache_control")
+    cache = SimpleNamespace(game_update_flow_running=0)
+    calls = []
+
+    character_behavior.init_character_behavior = lambda: calls.append("settle")
+    game_time.sub_time_now = lambda minute: calls.append(("time", minute))
+    py_cmd.focus_cmd = lambda: calls.append("focus")
+    cache_control.cache = cache
+    script_module.Design = design_module
+    script_module.Core = core_module
+    design_module.character_behavior = character_behavior
+    design_module.game_time = game_time
+    core_module.py_cmd = py_cmd
+    core_module.cache_control = cache_control
+
+    sys.modules.update(
+        {
+            "Script": script_module,
+            "Script.Design": design_module,
+            "Script.Design.character_behavior": character_behavior,
+            "Script.Design.game_time": game_time,
+            "Script.Core": core_module,
+            "Script.Core.py_cmd": py_cmd,
+            "Script.Core.cache_control": cache_control,
+        }
+    )
+    spec = importlib.util.spec_from_file_location("game_update_depth_under_test", UPDATE_PATH)
+    module = importlib.util.module_from_spec(spec)
+    sys.modules["game_update_depth_under_test"] = module
+    spec.loader.exec_module(module)
+
+    def restore():
+        """参数：无；返回：None；用途：恢复加载测试模块前的模块表。"""
+        for name, old_module in old_modules.items():
+            if old_module is missing:
+                sys.modules.pop(name, None)
+            else:
+                sys.modules[name] = old_module
+
+    return module, cache, calls, character_behavior, restore
+
+
+def test_sequential_nested_updates_restore_outer_depth():
+    """参数：无；返回：None；用途：验证同一外层中的两次嵌套更新之间始终保持外层深度。"""
+    module, cache, _calls, character_behavior, restore = load_update_module()
+    observed_depths = []
+
+    def settle_with_two_nested_updates():
+        """参数：无；返回：None；用途：在真实更新入口内依次发起两次嵌套更新。"""
+        observed_depths.append(cache.game_update_flow_running)
+        if len(observed_depths) == 1:
+            module.game_update_flow(2)
+            observed_depths.append(cache.game_update_flow_running)
+            module.game_update_flow(3)
+            observed_depths.append(cache.game_update_flow_running)
+
+    character_behavior.init_character_behavior = settle_with_two_nested_updates
+    try:
+        module.game_update_flow(1)
+
+        assert observed_depths == [1, 2, 1, 2, 1]
+        assert cache.game_update_flow_running == 0
+    finally:
+        restore()
+
+
+def test_nested_update_exception_restores_outer_depth():
+    """参数：无；返回：None；用途：验证嵌套异常被外层处理后仍恢复外层深度。"""
+    module, cache, _calls, character_behavior, restore = load_update_module()
+    observed_depths = []
+
+    def settle_with_nested_exception():
+        """参数：无；返回：None；用途：令嵌套结算抛错并由外层结算继续处理。"""
+        observed_depths.append(cache.game_update_flow_running)
+        if len(observed_depths) == 1:
+            try:
+                module.game_update_flow(2)
+            except RuntimeError:
+                observed_depths.append(cache.game_update_flow_running)
+        else:
+            raise RuntimeError("nested settlement failed")
+
+    character_behavior.init_character_behavior = settle_with_nested_exception
+    try:
+        module.game_update_flow(1)
+
+        assert observed_depths == [1, 2, 1]
+        assert cache.game_update_flow_running == 0
+    finally:
+        restore()
+
+
+def test_outer_update_exception_restores_zero():
+    """参数：无；返回：None；用途：验证最外层更新异常退出后恢复零深度。"""
+    module, cache, _calls, character_behavior, restore = load_update_module()
+
+    def settle_with_outer_exception():
+        """参数：无；返回：None；用途：令最外层结算抛出测试异常。"""
+        raise RuntimeError("outer settlement failed")
+
+    character_behavior.init_character_behavior = settle_with_outer_exception
+    try:
+        with pytest.raises(RuntimeError, match="outer settlement failed"):
+            module.game_update_flow(1)
+
+        assert cache.game_update_flow_running == 0
+    finally:
+        restore()
+
+
+def test_depth_limit_rejects_deeper_update_without_mutation():
+    """参数：无；返回：None；用途：验证深度达到二时仍拒绝更深更新且不改变当前深度。"""
+    module, cache, calls, _character_behavior, restore = load_update_module()
+    cache.game_update_flow_running = 2
+    try:
+        module.game_update_flow(5)
+
+        assert cache.game_update_flow_running == 2
+        assert calls == []
+    finally:
+        restore()
````

`````

### Exact output

`````text
**CODE: PASS**
**SIDE-BRANCH REVIEW STATE: ACCEPT**
**PR ARTIFACT STATE: BLOCKED**

**Reasoning**

1. **代码/测试本身**：无需修改代码。生产 diff 是最小正确形态——保存 `caller_depth` 并在 `finally` 恢复，是嵌套计数器的标准生命周期修法；`>= 2` 上限守卫语义未变（depth-limit 测试证实拒绝时不改深度、不产生副作用）。测试通过真实 `update.py` 入口加载、桩件只替换外部依赖、`sys.modules` 有完整还原，四个用例分别覆盖顺序嵌套、嵌套异常、最外层异常、深度上限，且前两个在基线上已验证 red-capable（`[1,2,0,1,0]` / `[1,2,0]` 正是旧实现"finally 清零而非恢复"的指纹）。旧实现的缺陷不止是深度显示错：嵌套返回后外层深度被清成 0，会让同一外层结算内的第二次嵌套误判为最外层调用，重入守卫失效——这是测试直接断言的不变量。中文注释符合项目规范。适合发布到 fork side branch 供人审核。

2. **缺少 Tk A/B 与代码正确性的关系**：不影响代码正确性判断。该修改的行为契约（"退出时恢复调用者深度"）是纯状态生命周期不变量，单元测试 + 静态核对（唯一写者是 `update.py`，生产存在 `settle_sleep_h → recover_from_unconscious_h → game_update_flow(5)` 嵌套入口）足以确认。Tk A/B 缺失只影响"向上游审阅者证明玩家可见影响"这一 artifact 维度，二者不应互相污染。

3. **PR draft**：维持 BLOCKED，不因允许 push 而升格。三个理由都未解除：(a) 硬 blocker——没有真实 Tk A/B，两条候选路线（99 号、97 号档）均未进入嵌套分支，静态入口存在≠可见后果已演示；(b) "实际失效"措辞仍缺生产触发证明，目前只能诚实地写"生产存在嵌套调用路径，旧实现在该路径上会破坏重入守卫"；(c) "旧实现记录到"暗示提交了运行记录，需改写为测试断言层面的表述。push side branch 是给用户人工审代码用的，不构成 PR 门槛的任何豁免。

**Next**

- push 后用户审核时必须知道的证据限制：正确性证据全部来自单元测试（red-capable 已验证）与静态调用链核对；**没有任何一次真实运行进入过嵌套分支**。99 号档复现了截图附近的绝顶提示但 trace 停在 depth_before=0 外层；97 号档虽有 unconscious_h=3 角色但观察窗口内未触发恢复。诊断截图不是证据。
- PR draft 下一步：寻找天然处于"无意识 H 即将恢复、外层 update 仍在运行"的保存点（或从 97 号档推进游戏内时间构造一个），用同一 seed/overlay 做 baseline vs candidate 的 Tk A/B；同时按 (b)(c) 修订措辞（经 fable-5 writer）。在获得可见 A/B 之前不要开 PR。
- 本裁定仅为技术判断；push 到 fork 的授权由用户已给出的明确许可承载，不由本裁定扩展。
`````

## PR draft evidence-limiting revision — 2026-07-14

### Exact prompt

`````text
/investigate-game-bug

请作为 erArk 上游 PR 文案作者，用中文重写下面这个候选的 PR title 和 body，供用户审核。输出只能包含一行 `Title: ...`，然后 `Body:` 和完整 Markdown 正文；不要输出审计结论、解释、备选版本或发布建议。

正文只用三个章节：`## 问题`、`## 修复`、`## 验证`。

必须遵守：
- 只写提交中真实改变的 `game_update_flow_running` 嵌套深度生命周期。
- 不声称修复了重复高潮、时间显示、玩家截图中的具体输出，或任何已被 Tk A/B 证明的可见问题。
- 不写“既有上限实际失效”。可以准确写：生产代码存在嵌套 `game_update_flow()` 调用路径；旧实现的内层 `finally` 固定清零会破坏外层仍在运行时的深度状态，使后续重入判断使用错误深度。
- 不写“旧实现记录到……”，也不要暗示 PR 附带旧版运行日志。验证只陈述随 PR 提交的自动化测试断言。
- 不写截图/GIF，也不声称有视觉证据。
- 不提本地 branch、commit、fork、worktree、OpenSpec、Fable、agent、私有调查或尚未实现的队列。
- 不写文件清单、非目标清单、rejected design。
- 标题用普通中文准确命名深度被内层提前清零的问题。

可公开核对的源码事实：
- `game_update_flow()` 在 `game_update_flow_running >= 2` 时直接返回。
- 旧实现获准进入后 `+= 1`，但每层退出时 `finally` 都固定写 0。
- 生产代码存在从结算进入 `recover_from_unconscious_h()` 再调用 `game_update_flow(5)` 的嵌套路径。
- 运行期只有 `game_update_flow()` 写该变量；初始化和读档把它设为 0。

候选生产改动：
- 通过守卫后保存 `caller_depth = game_update_flow_running`。
- 当前层设置为 `caller_depth + 1`。
- `finally` 恢复 `caller_depth`。
- `>= 2` 守卫，以及推进时间、角色结算、聚焦输入的顺序均不变。

随 PR 提交的自动化测试实际断言：
1. 同一外层先后发起两个嵌套更新，观察深度是 `[1, 2, 1, 2, 1]`，外层最后回到 0。
2. 嵌套更新抛错并被外层捕获，回到外层时深度是 1，外层最后回到 0。
3. 最外层更新抛错，最后回到 0。
4. 已处于深度 2 时再次请求更新，不推进时间、不运行角色结算、不聚焦输入，深度保持 2。

请写成简洁、每一段独立成立、不会超出上述证据的 draft。

`````

### Exact output

`````text
Title: 修复 game_update_flow 嵌套调用时内层退出提前清零运行深度的问题

Body:

## 问题

`game_update_flow()` 用 `game_update_flow_running` 记录更新流程的嵌套深度：当该值 `>= 2` 时直接返回，不再执行更深一层的更新。运行期间只有 `game_update_flow()` 本身写这个变量，初始化和读档会把它设为 0。

生产代码中存在嵌套调用路径：角色结算过程中会进入 `recover_from_unconscious_h()`，其中再次调用 `game_update_flow(5)`。旧实现在通过守卫后对深度 `+= 1`，但每一层退出时的 `finally` 都固定把它写成 0。于是内层更新一结束，深度就被清零，而此时外层更新仍在运行——外层后续再触发的重入判断读到的是错误的深度，`finally` 也无法把状态恢复到进入前的值。

## 修复

把 `finally` 从“固定清零”改为“恢复调用前的深度”：

- 通过 `>= 2` 守卫后，先保存 `caller_depth = game_update_flow_running`；
- 当前层将深度设为 `caller_depth + 1`；
- `finally` 中恢复为 `caller_depth`。

这样每一层退出时深度都精确回到它进入前的值，最外层退出后回到 0。`>= 2` 的守卫阈值，以及推进时间、角色结算、聚焦输入的执行顺序均保持不变。

## 验证

随本 PR 提交了自动化测试，断言以下行为：

1. 同一外层更新中先后发起两次嵌套更新，观察到的深度序列为 `[1, 2, 1, 2, 1]`，外层结束后回到 0。
2. 嵌套更新抛出异常并被外层捕获后，回到外层时深度为 1，外层结束后回到 0。
3. 最外层更新抛出异常时，深度最终回到 0。
4. 已处于深度 2 时再次请求更新：不推进时间、不运行角色结算、不聚焦输入，深度保持 2。
`````

## Revised PR artifact audit — 2026-07-14

### Exact prompt

`````text
/investigate-game-bug
/review-erark-pr-artifacts

请作为新的、无前文上下文的 erArk 上游 PR artifact reviewer，审计下面的完整 proposed diff 与 Fable 重写后的完整 PR draft。不要编辑或改写。按 review-erark-pr-artifacts 返回 PASS、REVISE 或 BLOCKED，并提供 publication_state、visibility ledger、cumulative prefix audit 和带 draft 行号的 findings。

边界：用户已授权把代码推到 fork side branch 供审核，但没有授权创建 PR；这项 side-branch push 不是视觉证据豁免，也不能提升 PR readiness。

PR-facing evidence：
- submitted automated tests：就在 proposed diff 中。
- screenshots/GIF：无。真实 Tk 探索得到的图片是失败路线诊断材料，不用于 PR。
- external evidence：无。

真实 Tk 探索结论仅供判断证据缺口，不可用于替 draft 辩护：
- 99 号档复现等待后连续高潮文本，但 trace 只有外层 depth_before=0，没有进入嵌套分支。
- 97 号档普通等待完整返回，trace 为外层 0 -> 0，中间无第二个 CALL。
- 因候选路线都未进入修改分支，没有 baseline A/B。

请特别判断：
- 重写后的 draft 是否已经删除此前不受支持的“既有上限实际失效”和“旧实现记录到”暗示。
- 每个验证项是否由 submitted tests 实际断言。
- 生产嵌套入口的表述是否准确地停留在静态源码事实，没有暗示可见后果已演示。
- 即使文案已无其他问题，项目对 behavior-changing fix 的真实 Tk A/B 要求是否仍使 PR artifact BLOCKED。不得发明非视觉豁免。

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
diff --git a/tests/test_game_update_depth_restoration.py b/tests/test_game_update_depth_restoration.py
new file mode 100644
index 000000000..f7458e58d
--- /dev/null
+++ b/tests/test_game_update_depth_restoration.py
@@ -0,0 +1,157 @@
+# -*- coding: UTF-8 -*-
+"""游戏更新嵌套深度生命周期回归测试。"""
+
+import importlib.util
+import sys
+from pathlib import Path
+from types import ModuleType, SimpleNamespace
+
+import pytest
+
+
+REPO_ROOT = Path(__file__).resolve().parents[1]
+UPDATE_PATH = REPO_ROOT / "Script" / "Design" / "update.py"
+
+
+def load_update_module():
+    """参数：无；返回：更新模块、缓存、调用记录与恢复函数；用途：通过真实入口隔离验证深度生命周期。"""
+    missing = object()
+    module_names = [
+        "Script",
+        "Script.Design",
+        "Script.Design.character_behavior",
+        "Script.Design.game_time",
+        "Script.Core",
+        "Script.Core.py_cmd",
+        "Script.Core.cache_control",
+        "game_update_depth_under_test",
+    ]
+    old_modules = {name: sys.modules.get(name, missing) for name in module_names}
+
+    script_module = ModuleType("Script")
+    design_module = ModuleType("Script.Design")
+    character_behavior = ModuleType("Script.Design.character_behavior")
+    game_time = ModuleType("Script.Design.game_time")
+    core_module = ModuleType("Script.Core")
+    py_cmd = ModuleType("Script.Core.py_cmd")
+    cache_control = ModuleType("Script.Core.cache_control")
+    cache = SimpleNamespace(game_update_flow_running=0)
+    calls = []
+
+    character_behavior.init_character_behavior = lambda: calls.append("settle")
+    game_time.sub_time_now = lambda minute: calls.append(("time", minute))
+    py_cmd.focus_cmd = lambda: calls.append("focus")
+    cache_control.cache = cache
+    script_module.Design = design_module
+    script_module.Core = core_module
+    design_module.character_behavior = character_behavior
+    design_module.game_time = game_time
+    core_module.py_cmd = py_cmd
+    core_module.cache_control = cache_control
+
+    sys.modules.update(
+        {
+            "Script": script_module,
+            "Script.Design": design_module,
+            "Script.Design.character_behavior": character_behavior,
+            "Script.Design.game_time": game_time,
+            "Script.Core": core_module,
+            "Script.Core.py_cmd": py_cmd,
+            "Script.Core.cache_control": cache_control,
+        }
+    )
+    spec = importlib.util.spec_from_file_location("game_update_depth_under_test", UPDATE_PATH)
+    module = importlib.util.module_from_spec(spec)
+    sys.modules["game_update_depth_under_test"] = module
+    spec.loader.exec_module(module)
+
+    def restore():
+        """参数：无；返回：None；用途：恢复加载测试模块前的模块表。"""
+        for name, old_module in old_modules.items():
+            if old_module is missing:
+                sys.modules.pop(name, None)
+            else:
+                sys.modules[name] = old_module
+
+    return module, cache, calls, character_behavior, restore
+
+
+def test_sequential_nested_updates_restore_outer_depth():
+    """参数：无；返回：None；用途：验证同一外层中的两次嵌套更新之间始终保持外层深度。"""
+    module, cache, _calls, character_behavior, restore = load_update_module()
+    observed_depths = []
+
+    def settle_with_two_nested_updates():
+        """参数：无；返回：None；用途：在真实更新入口内依次发起两次嵌套更新。"""
+        observed_depths.append(cache.game_update_flow_running)
+        if len(observed_depths) == 1:
+            module.game_update_flow(2)
+            observed_depths.append(cache.game_update_flow_running)
+            module.game_update_flow(3)
+            observed_depths.append(cache.game_update_flow_running)
+
+    character_behavior.init_character_behavior = settle_with_two_nested_updates
+    try:
+        module.game_update_flow(1)
+
+        assert observed_depths == [1, 2, 1, 2, 1]
+        assert cache.game_update_flow_running == 0
+    finally:
+        restore()
+
+
+def test_nested_update_exception_restores_outer_depth():
+    """参数：无；返回：None；用途：验证嵌套异常被外层处理后仍恢复外层深度。"""
+    module, cache, _calls, character_behavior, restore = load_update_module()
+    observed_depths = []
+
+    def settle_with_nested_exception():
+        """参数：无；返回：None；用途：令嵌套结算抛错并由外层结算继续处理。"""
+        observed_depths.append(cache.game_update_flow_running)
+        if len(observed_depths) == 1:
+            try:
+                module.game_update_flow(2)
+            except RuntimeError:
+                observed_depths.append(cache.game_update_flow_running)
+        else:
+            raise RuntimeError("nested settlement failed")
+
+    character_behavior.init_character_behavior = settle_with_nested_exception
+    try:
+        module.game_update_flow(1)
+
+        assert observed_depths == [1, 2, 1]
+        assert cache.game_update_flow_running == 0
+    finally:
+        restore()
+
+
+def test_outer_update_exception_restores_zero():
+    """参数：无；返回：None；用途：验证最外层更新异常退出后恢复零深度。"""
+    module, cache, _calls, character_behavior, restore = load_update_module()
+
+    def settle_with_outer_exception():
+        """参数：无；返回：None；用途：令最外层结算抛出测试异常。"""
+        raise RuntimeError("outer settlement failed")
+
+    character_behavior.init_character_behavior = settle_with_outer_exception
+    try:
+        with pytest.raises(RuntimeError, match="outer settlement failed"):
+            module.game_update_flow(1)
+
+        assert cache.game_update_flow_running == 0
+    finally:
+        restore()
+
+
+def test_depth_limit_rejects_deeper_update_without_mutation():
+    """参数：无；返回：None；用途：验证深度达到二时仍拒绝更深更新且不改变当前深度。"""
+    module, cache, calls, _character_behavior, restore = load_update_module()
+    cache.game_update_flow_running = 2
+    try:
+        module.game_update_flow(5)
+
+        assert cache.game_update_flow_running == 2
+        assert calls == []
+    finally:
+        restore()
````

完整 revised draft（请从第 1 行开始编号）：

````markdown
# PR Draft

## Title

修复 game_update_flow 嵌套调用时内层退出提前清零运行深度的问题

## Body

## 问题

`game_update_flow()` 用 `game_update_flow_running` 记录更新流程的嵌套深度：当该值 `>= 2` 时直接返回，不再执行更深一层的更新。运行期间只有 `game_update_flow()` 本身写这个变量，初始化和读档会把它设为 0。

生产代码中存在嵌套调用路径：角色结算过程中会进入 `recover_from_unconscious_h()`，其中再次调用 `game_update_flow(5)`。旧实现在通过守卫后对深度 `+= 1`，但每一层退出时的 `finally` 都固定把它写成 0。于是内层更新一结束，深度就被清零，而此时外层更新仍在运行——外层后续再触发的重入判断读到的是错误的深度，`finally` 也无法把状态恢复到进入前的值。

## 修复

把 `finally` 从“固定清零”改为“恢复调用前的深度”：

- 通过 `>= 2` 守卫后，先保存 `caller_depth = game_update_flow_running`；
- 当前层将深度设为 `caller_depth + 1`；
- `finally` 中恢复为 `caller_depth`。

这样每一层退出时深度都精确回到它进入前的值，最外层退出后回到 0。`>= 2` 的守卫阈值，以及推进时间、角色结算、聚焦输入的执行顺序均保持不变。

## 验证

随本 PR 提交了自动化测试，断言以下行为：

1. 同一外层更新中先后发起两次嵌套更新，观察到的深度序列为 `[1, 2, 1, 2, 1]`，外层结束后回到 0。
2. 嵌套更新抛出异常并被外层捕获后，回到外层时深度为 1，外层结束后回到 0。
3. 最外层更新抛出异常时，深度最终回到 0。
4. 已处于深度 2 时再次请求更新：不推进时间、不运行角色结算、不聚焦输入，深度保持 2。
````

`````

### Exact output

`````text
**Verdict: BLOCKED**

唯一阻断项是证据缺口，不是文案:行为变更类修复缺少项目强制要求的真实 Tk baseline/candidate 前后对比图像。文案本身已达标(无需再改写)。

## publication_state

- 代码:已授权推送 fork side branch 供审核;该授权明确不是视觉证据豁免,不提升 readiness。
- PR:未授权创建,且即使授权,artifact 也未就绪。
- 阻断条件:Tk 探索(99/97 号档)均未进入嵌套分支(trace 仅外层 depth 0→0,无第二个 CALL),因此无 baseline A/B、无可用截图/GIF。项目规则要求每个 behavior-changing candidate 提供一组经检视的真实 Tk 前后对比图像;不存在非视觉豁免路径。修复本身改变生产运行时语义(深度恢复),属于 behavior-changing,不因"可见后果未演示"而降级为非行为变更。

## Visibility ledger(draft 对外暴露的内容)

| 暴露项 | 判定 |
|---|---|
| `game_update_flow` / `game_update_flow_running` / `caller_depth` / `recover_from_unconscious_h` | 均为上游源码中的真实标识符,允许 |
| 提交的自动化测试及其断言行为 | 与 proposed diff 一致,允许 |
| 本地存档 97/99、Tk trace、失败路线截图 | **未泄露** ✓ |
| mod / OpenSpec / 内部调查、被否路线、文件清单、non-goal 清单 | **未泄露** ✓ |
| 自造术语 | 无;"守卫""嵌套深度"均可由代码直接支撑 ✓ |

## Cumulative prefix audit

- 行 5(标题)单独成立:命名了函数与缺陷("内层退出提前清零运行深度"),无需后文。✓
- 行 1–13(问题):先给状态变量的静态语义,再给嵌套入口与错误机制,读到此处已知问题是什么、为何发生,无待后文救援的悬空断言。✓
- 行 1–23(+修复):修复描述与 diff 逐条对应(守卫后保存/加一/finally 恢复),行 23 明确不变量(阈值、执行顺序不变)。✓
- 行 1–32(+验证):"随本 PR 提交了自动化测试"属实(测试在 diff 内)。✓ 但整体读完,行为修复的 PR 无任何玩家可见验证——这是 B1 阻断,不是前缀连贯性问题。

## Findings

- **B1(阻断)· 行 25–32**:验证节仅含自动化测试。behavior-changing fix 必须附一组真实 Tk 前后对比图像/GIF;当前探索未进入修改分支,无 A/B。在取得进入嵌套分支的可复现玩家路线并完成 baseline/candidate 对比之前,artifact 保持 BLOCKED。side-branch push 授权不构成豁免。
- **F2(通过确认)· 行 13**:此前不受支持的"既有上限实际失效""旧实现记录到"暗示已删除。现文"外层后续再触发的重入判断读到的是错误的深度"是守卫读取被清零变量的直接静态推论,条件式表述,未暗示已演示可见后果。可保留。
- **F3(通过确认)· 行 27–32**:四条验证项均被提交测试逐一断言——序列 `[1,2,1,2,1]` 与归零(test_sequential…)、异常后回到 1 再归零(test_nested…exception)、外层异常归零(test_outer…)、深度 2 拒绝且 `calls == []` 恰好覆盖"不推进时间/不结算/不聚焦"三个桩(test_depth_limit…)。无超出测试断言的验证声明。✓
- **F4(发布前核对)· 行 11、13**:"运行期间只有 `game_update_flow()` 本身写该变量""`recover_from_unconscious_h()` 再次调用 `game_update_flow(5)`"以静态源码事实呈现,表述层级正确;但本次审计无法独立复核源码,发布前须对照当时的 upstream HEAD 逐条确认仍然成立。
- **F5(琐碎,可不改)· 行 7–9**:`## Body` 与其下的 `## 问题` 同级标题;贴入 GitHub PR body 时 `# PR Draft`/`## Title`/`## Body` 脚手架应剥离,仅正文入 body。

## 下一步(非文案)

解除 B1 的唯一路径:找到能真实进入嵌套分支(`recover_from_unconscious_h` → `game_update_flow(5)`)的可复现玩家路线,在同种子、同存档下完成 pristine baseline 与 candidate 的 Tk 对比截图并经 `view_image` 检视。若该路线经充分探索仍不可达,则应把"无法在真实游玩中触达嵌套分支"作为证据结论上报用户决策,而非发布无视觉证据的 PR。
`````
