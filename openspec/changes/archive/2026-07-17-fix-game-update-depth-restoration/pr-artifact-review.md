# Fable PR artifact audit

## Exact audit prompt

````text
/investigate-game-bug
/review-erark-pr-artifacts

请作为全新上下文的 erArk 上游 PR artifact reviewer，严格审计下面的候选 diff 和 Fable 生成的 PR draft。不要编辑任何文件或改写文案。必须按 review-erark-pr-artifacts 返回 PASS、REVISE 或 BLOCKED，并提供 publication_state、visibility ledger、cumulative prefix audit，以及带 draft 行号的可操作发现。

候选身份：
- base ref: upstream/master at abebf33b52ebf51424f71365946eb8df1f75a23c
- head ref: 80a711603
- proposed diff 只有下面两个文件，无生成数据或其他改动。
- 当前开放上游 PR #212、#213、#215 均没有相同 scope。

PR 文案来源：
- title/body 由新的 Fable 5 会话通过 claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence 生成。
- writer 只获得下面的 proposed diff 语义与 submitted tests，没有获得或引用私有 OpenSpec/agent/worktree 内容。

PR-facing evidence：
- submitted automated tests：包含在 proposed diff 中。
- screenshots/GIF/player route：无。
- pending-publication visual evidence：无。
- external evidence：无。

重要限制：
- 不要用私有调查或 OpenSpec 替 draft 辩护。
- 核对 draft 的每个自动化证明是否由 submitted test 实际断言。
- 核对“既有两层上限实际失效”是否由代码与测试足以支持。
- 项目规则要求每个改变游戏行为的 bug fix 有真实 Tk 前后证据；如果此内部生命周期 diff 没有可诚实展示的代表性 Tk 变化，请按规则返回 BLOCKED，而不是发明非视觉豁免。
- 即使 BLOCKED，也要分别判断 draft 本身是否存在可通过文案修订解决的问题，和哪些问题必须通过改变 PR scope 或增加可发布证据解决。
- 不要建议把重复高潮或时间显示写入本 draft，除非这些变化真实进入 proposed diff。

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

```

Fable 生成的完整 draft：

```markdown
# PR Draft

## Title

修复游戏更新流程嵌套调用时运行深度被内层提前清零的问题

## Body

## 问题

`game_update_flow()` 用 `game_update_flow_running` 记录更新流程当前的运行深度，深度达到 2 时直接返回，以限制嵌套层数。但退出时的 `finally` 无条件把 `game_update_flow_running` 写回 0：当一次更新流程内部又触发一次更新时，内层返回后深度被直接清零，而不是恢复成外层进入时的 1。此时外层仍在运行，深度计数已经失真——外层随后再发起的嵌套更新会被当成全新的最外层调用，既有的两层上限实际失效。

## 修复

进入流程时先保存调用前的深度 `caller_depth = game_update_flow_running`，再写入 `caller_depth + 1`；`finally` 中恢复为 `caller_depth`，而不是固定写 0。深度已达 2 时直接返回的准入规则保持不变，推进游戏时间、执行角色结算、聚焦输入的顺序也完全不变。当前运行时只有 `game_update_flow()` 本身会写这个变量，存档加载仅把这个非持久的运行状态初始化为 0，因此恢复调用前深度不会影响其他代码。

## 验证

随 PR 提交自动化回归测试，断言以下四种情况：

1. 同一外层更新先后发起两个嵌套更新：每个嵌套运行期间深度为 2，两次嵌套之间恢复为 1，外层结束后回到 0。在外层运行、两次嵌套运行及其前后各观察点上，旧实现记录到 `[1, 2, 0, 1, 0]`，修复后为 `[1, 2, 1, 2, 1]`。
2. 嵌套更新抛出异常并被外层捕获：回到外层后深度恢复为 1，外层结束后回到 0。旧实现回到外层时深度已被清成 0。
3. 最外层更新抛出异常：深度最终恢复为 0。
4. 深度已为 2 时再次请求更新：不推进游戏时间、不运行角色结算、不聚焦输入，深度保持 2。

```

````

## Exact Fable verdict

````markdown
**Verdict: BLOCKED** — 这是一个改变游戏行为的 bug fix(draft 自己主张"既有的两层上限实际失效",即真实游玩会受影响),但 PR-facing evidence 中没有任何真实 Tk 前后证据。按项目规则,行为变更类修复必须附带一条有代表性的真实 Tk 前后图像对;本候选提交为"无",且我不接受发明非视觉豁免。BLOCKED 的解除路径见末尾。

## publication_state

- 未创建/未编辑任何上游 PR;无已发布截图、GIF、外链或待发布视觉证据。
- 全部候选材料(diff、测试、draft)均为本地。当前无泄露风险。
- 开放 PR #212/#213/#215 与本 scope 不重叠(按提交方声明记录,未独立核实)。

## Visibility ledger

| Draft 中的主张 | 由提交材料支撑? | 备注 |
|---|---|---|
| `finally` 无条件写回 0、内层返回后深度清零(L11) | ✅ | 由 diff 中旧代码直接可见 |
| "既有的两层上限**实际**失效"(L11) | ⚠️ 部分 | 机制由代码逻辑成立;但没有任何提交材料证明生产路径中真的存在嵌套 `game_update_flow` 调用。测试的嵌套是通过 stub 的 `init_character_behavior` 注入的,不是生产触发路径 |
| 修复方案描述(L15 前半) | ✅ | 与 diff 一致 |
| "当前运行时只有 `game_update_flow()` 本身会写这个变量,存档加载仅把这个非持久运行状态初始化为 0"(L15) | ⚠️ | 这是对上游代码库的调查性断言,不在 diff 或测试中。上游代码对 reviewer 可见故可自行核实,但 writer 声明只拿到 diff 语义与测试——这句话的事实来源超出了 writer 的声明输入,提交方需确认其来源合规并自行核实真伪 |
| 验证项 1 修复后序列 `[1,2,1,2,1]`、结束回 0(L21) | ✅ | `test_sequential_nested_updates_restore_outer_depth` 逐字断言 |
| 验证项 1 "旧实现**记录到** `[1,2,0,1,0]`"(L21) | ⚠️ | 我按旧代码手工推演该序列正确,且提交的测试在 base ref 上运行会产出此失败,red-capable 成立;但"记录到"暗示提交了一次旧实现运行记录,实际未提交。属措辞问题 |
| 验证项 2(L22) | ✅ | `test_nested_update_exception_restores_outer_depth` 断言 `[1,2,1]` 与最终 0;"旧实现清成 0"同上为可推演的旧行为 |
| 验证项 3(L23) | ✅ | `test_outer_update_exception_restores_zero` 断言 |
| 验证项 4 "不推进游戏时间、不运行角色结算、不聚焦输入,深度保持 2"(L24) | ✅ | `calls == []` 覆盖全部三个 stub(time/settle/focus),`assert cache.game_update_flow_running == 2` 覆盖深度不变 |
| Tk/玩家可见证据 | ❌ | 无,行为变更修复的硬性要求缺失 |

## Cumulative prefix audit

- L5(标题):自成立,准确描述 diff。✅
- 问题段(L11)截止到"恢复成外层进入时的 1":每个前缀都无需后文救援。✅
- L11 结尾"既有的两层上限实际失效":作为前缀读到此处,读者会认为已证实生产中上限被真实突破;后文没有提供该证明。前缀承诺超出证据。⚠️
- 修复段(L15):不依赖后文;但存档加载那句引入未提交来源的事实(见 ledger)。⚠️
- 验证段(L19–L24):顺序清晰,无前缀依赖后文救援。唯一问题是 L21 的"记录到"措辞。⚠️

## Findings

**必须通过 scope/证据解决(BLOCKED 根因),不可用文案修掉:**

- **B1(L11、整体)**:无 Tk 前后证据。两条出路,二选一:
  (a) 找到一条真实生产嵌套路由(某个在 `init_character_behavior` 结算内再触发 `game_update_flow` 的流程),用规定的 Tk 视觉流程做同种子 A/B 前后图像,发布代表性一例;
  (b) 若排查后确认当前上游没有任何生产路径会嵌套调用——那么"实际失效"不成立,这个 diff 就是防御性/内部一致性修复而非可展示的 bug fix,PR 的定位与理由必须重写,这超出本 draft 文案修订范围,需要用户输入决定是否仍值得上游提交。
- **B2(L11)**:"既有的两层上限实际失效"目前无生产触发证据支撑。B1(a) 成立则保留并配证据;否则必须改写。

**可通过文案修订解决(REVISE 级,BLOCKED 解除后处理):**

- **R1(L21)**:"旧实现记录到 `[1, 2, 0, 1, 0]`"改为可核查表述,如"在修复前的实现上运行同一测试,这些观察点得到 `[1, 2, 0, 1, 0]`",明示 reviewer 可自行在 base ref 上复现,而非暗示附带了一份未提交的运行记录。L22 的"旧实现回到外层时深度已被清成 0"同理。
- **R2(L15)**:存档加载/唯一写入者断言需提交方在最终上游代码上重新核实(`cache_control`、存档恢复路径),并确认该事实来源不是私有调查文档的转述。断言本身若属实可保留——上游代码对 reviewer 可见。

**diff 本身(供记录,非 draft 问题):** 修复逻辑正确;四个测试均由真实 `update.py` 入口加载、red-capable(在 base ref 上测试 1、2 会失败),模块表恢复干净;准入规则 `>= 2` 未动。无生成数据混入。

**结论:BLOCKED。** 解除条件:完成 B1 的 (a) 或 (b)。若走 (a),补 Tk 证据后按 R1/R2 修订文案再送审;若走 (b),需重新界定 PR 定位并获得用户对是否提交的决定。
````

## Post-audit source verification

审计后在当前 `upstream/master` 上重新核对了审计指出的两项事实：

- `game_update_flow_running` 只在 `Script/Design/update.py` 的更新入口运行期间改变；`Script/Core/game_type.py` 初始化为 0，`Script/Core/save_handle.py` 在读档时重置为 0。
- 生产代码存在真实嵌套路由：`Script/Settle/realtime_settle.py` 调用 `handle_npc_ai_in_h.judge_weak_up_in_sleep_h()`，后者进入 `recover_from_unconscious_h()` 并调用 `update.game_update_flow(5)`；`Script/Settle/default.py` 也可进入同一恢复函数。
- 这项静态核对排除了“生产代码完全没有嵌套入口”的分支，但尚未提供一条可复现、可发布的真实 Tk 前后证据。因此 Fable 的 `BLOCKED` 发布结论仍然有效。

PR draft 只保留为本地审阅材料；在补齐 Tk 证据并按 R1/R2 修订、复审前，不应发布。

## 取证后状态与 side branch 边界

真实 Tk 尽力取证使用固定种子 `20260714`：99 号档复现了一次等待后连续出现阴道小绝顶与心理绝顶，但 trace 只有一次最外层 `CALL depth_before=0`；97 号档普通等待完整返回的 trace 为 `CALL depth_before=0` 后 `RETURN depth_after=0`，中间没有第二次调用。两条路线都没有进入本候选修改的嵌套分支，因此没有运行 baseline，也没有把诊断截图作为 PR evidence。完整本地记录位于 `.codex-evidence/game-update-depth-restoration/`。

用户随后明确授权：即使无法取得可用 Tk A/B，只要 Codex 与 Fable 确认代码，也要把候选推到 fork side branch 供用户审核，但不开 PR。Fable 最终分离裁定为 `CODE: PASS`、`SIDE-BRANCH REVIEW STATE: ACCEPT`、`PR ARTIFACT STATE: BLOCKED`，并明确“无需修改代码”。

候选已按该授权推送到 `pr-fork/codex/fix-game-update-depth-restoration`，远端指针核对为 `80a711603734eb3913a608bbece79059aae0e08a`。这项 push 只发布待审核代码，不表示 PR artifact 已满足上游门槛。Fable 已按审计意见重写本地 `pr-draft.md`，删除“实际失效”和“旧实现记录到”等超出证据的措辞；缺少真实 Tk A/B 的 blocker 仍保留。

新的 fresh-context artifact audit 对重写文案仍返回 `BLOCKED`，但明确“唯一阻断项是证据缺口，不是文案；文案本身已达标（无需再改写）”。四项验证声明均与 submitted tests 一致，生产嵌套入口也只作为静态源码事实表述。完整 prompt 与逐字 verdict 记录在 `fable-publication-supervision.md`。
