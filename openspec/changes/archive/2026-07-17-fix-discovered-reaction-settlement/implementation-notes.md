## User Acceptance of the Standalone Settlement Evidence (2026-07-14)

After the scope was explicitly separated from merged PR #206, the user accepted the current before-and-after Tk images as valid evidence for the standalone bug “the selected discoverer reaction is omitted.” The user requested removal of the synthetic red/green title bars. The retained publication candidates are now:

- `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/baseline-missing-closure-response-clean.png`
- `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/candidate-closure-response-once-clean.png`

Each image is a deterministic 72-pixel top crop of the previously inspected labeled image. Both are `1200x900`; ImageMagick pixel comparison reports zero changed pixels against their corresponding raw Tk frame. This acceptance supersedes the earlier evidence-blocked verdict for this standalone settlement scope. It does not weaken the separate rule for a PR claiming that the same NPC discovers the player twice: that different bug still requires one static before-fix image showing both discoveries and the same NPC identity.

The candidate may proceed through Fable-high draft generation and a fresh PR-artifact review. It is not publication-ready until that review passes, the approved images receive public URLs, and the user separately authorizes each outward action.

## Repeated-Discovery Evidence Gate (Separate Scope)

For any PR claiming that the same NPC repeatedly triggers `H中被发现`, valid before-fix evidence must be one full-resolution static Tk screenshot containing both consecutive panels and the same NPC identity. The clean settlement A/B above does not prove that different bug and must never be used as its evidence.

## Retained Technical Candidate (2026-07-14)

### Human-review simplification request

After reviewing the pushed diff, the user rejected the custom `DiscoverySettlementResult` protocol as correct but too expensive to verify by eye. The replacement must preserve the original NPC “find behavior, then settle” structure, add only the discovery-specific exception, and target approximately ten net new production lines. The implementation may rely on the verified current behavior table: discovery reactions produce no replacement or produce `MOVE` through effect 1721; it must not pre-build a generic replacement protocol for hypothetical future behavior effects.

The retained candidate is branch `codex/fix-discovery-settlement-ownership-redo`, base `3a1c9e620`, local head `ffd1d1ee8`. Its proposed diff changes exactly four production files with `a=30` non-blank additions, `b=30` non-blank deletions, and penalty `60`, and uses only a panel-owned boolean settlement flag plus the production `MOVE` case; it has no custom result type, global wrapper, hidden-session teardown, witness-suppression state, or `place_all_not_h` premise edit. Its four production files are byte-identical to pushed fork head `884b2fa30`; the two later local commits cancel each other at the tree level and must be cleaned from history rather than pushed as noise.

Twenty-eight focused tests pass, and fresh independent standards, specification, architecture-simplicity, and settlement-ownership reviews pass on the final head. Its clean real-Tk A/B is user-approved for draft discussion, but must be replayed on the final head before publication readiness is claimed. No upstream PR or remote branch already owns this candidate.

Merged PR #206 is adjacent but separate: it prevents the same witness from immediately discovering again before movement. This candidate does not suppress a later different eligible witness.

## Superseded / Rejected History (2026-07-10)

### Worktree Status After The Old Backout

Per the user's decision, the exact-once global monkeypatch experiment was removed from the worktree on 2026-07-10; the mod script and its tests were reverted to HEAD and only the narrow `place_all_not_h` full-scene loop plus registry/alias replacement was re-applied, together with its two component tests. The full component suite (19 tests, including all restored upstream tests) passed after the re-application. This checkpoint is retained only as rejected history; the later four-file panel-owned candidate supersedes its implementation and verification plan. The old code is no longer present (backup at /tmp/erark-backup-2026-07-10/). Cross-change branch, HEAD, and protected-file state are in `../continue-local-bugfix-audit/design.md`.

## Confirmed Call Graph and Root Causes

### NPC state-machine caller

`character_behavior.character_behavior()` calls `handle_npc_ai.find_character_target()`. NPC state 40 opens `Sex_Be_Discovered_Panel`; after the panel returns, `character_behavior.py` later invokes an outer `judge_character_status()`. In the upstream existing-group accept/refuse paths, the panel also manually settles the selected discovery behavior. The same behavior can therefore be consumed once in the panel and again by the outer NPC settlement.

### Direct hidden-discovery caller

`hidden_sex_panel.settle_discovered()` calls `panel.draw()` directly. There is no later NPC outer settlement. This path depends on the panel performing any required settlement itself, so simply deleting all manual settlement would drop effects here.

### Initial conversion ordering

When single-target H is converted to group mode, upstream assigns `DISCOVER_OTHER_SEX_AND_JOIN` to the discoverer and then immediately settles the player's `OTHER_SEX_BE_FOUND_TO_GROUP_SEX`. That nested player update can overwrite or reset the discoverer's pending behavior before the discoverer is settled. The discoverer must be settled before the nested player flow, and any later NPC outer settlement must then skip only that already consumed behavior.

### Contradictory controls

`handle_scene_all_not_h()` returned success from inside its loop after inspecting the first non-player character. Instruction 5055 uses `SCENE_ALL_NOT_H`, while 6008 uses `GROUP_SEX_MODE_ON|IS_H`. If the first NPC is outside H and a later NPC is already in H, both invite-group and end-group can appear. Correcting the full-scene premise removes the contradiction but does not by itself establish the later participant's H state or normal action interface.

## Superseded Global Ownership Experiment

The removed experimental component included:

- `_DISCOVERY_OUTER_SETTLEMENT_CONTEXT`, a per-character depth table.
- `_SUPPRESS_NEXT_DISCOVERY_OUTER_SETTLEMENT`, a global character-ID set.
- Wrappers around every `handle_npc_ai.find_character_target()` call and the global `character_behavior.judge_character_status()` function.
- Rewritten invitation callbacks: an existing-group NPC path is left to a presumed outer owner; a direct caller settles immediately; initial conversion settles the discoverer before the nested player update and adds suppression for the later outer call.
- A wrapper around `_end_current_h()` to suppress a presumed later duplicate.
- Immediate settlement for tired auto-leave on a direct call.
- A corrected full-scene `place_all_not_h`, installed in both the premise registry and defining-module alias.

This code is rejected history, not the retained candidate or accepted ownership model.

## Known Safety Gaps in the Global Ownership Experiment

1. The design requires a token scoped to one dispatch, but the implementation stores only character IDs in a process-global set. There is no dispatch identity.
2. Wrapping `find_character_target()` assumes every call that enters the context will later perform an outer settlement. A direct caller of that function can create suppression without a matching consumer.
3. If early settlement is not followed immediately by the same character's outer `judge_character_status()`, the next unrelated behavior can be skipped.
4. Cleanup is only proved for exceptions propagating out of the wrapped target search. Caught exceptions, early return, re-entry, nested calls, and interruption between early settlement and outer settlement remain unsafe.
5. The global `judge_character_status()` wrapper can consume suppression for calls made by unrelated mods or flows.
6. Hot reload, partial install rollback, repeated load, same-NPC nesting, and interleaved different-NPC dispatches have no proved invariant.
7. `local_group_masturbation_intent_fix` also wraps `find_character_target()` through a different mechanism. Current load order can make admission outermost while `test_bdd_save_group_ai.py:110` expects the masturbation wrapper to be outermost. Checking `__module__` is insufficient; both load orders, repeated loads, and the complete wrapper chain must be behavior-tested.

These gaps are why the global experiment was rejected. The later panel-owned typed-result candidate avoids the global state and wrapper-composition problem.

## Adjacent Discovery Paths Found but Not Yet in Scope

The direct hidden-discovery call has other choices whose behavior is assigned without a proven settlement owner:

- `_let_find_chara_away()` can assign `SEE_H_BUT_DECEIVED`.
- `_continue_exhibitionism_sex()` can assign `SEE_H_BUT_IGNORE` or `SEE_H_AND_LEAVE` in some branches.
- `_switch_to_hidden_sex()` and the exhibitionism transition contain nested player flows that may create the same overwrite risk.

The old experimental patch did not prove these paths safe. The later retained candidate resolved that boundary by routing every explicit discoverer response through the same panel-owned commit while preserving successful no-explicit-response choices as `None`.

## Superseded Written Verification State

The old experimental component tests contained fake-module cases for NPC existing-group admission/refusal, initial conversion, direct hidden-discovery acceptance, end-H suppression, exception cleanup, same-NPC nesting, interaction with the group extension and pain conversion, and the full-scene premise. At that historical checkpoint none had run.

Two critical component tests are defined but omitted from the file's `main()` runner, so the README-style direct Python command would not execute them; pytest discovery would:

- `test_nested_target_search_keeps_outer_discovery_context_until_outer_return`
- `test_target_search_exception_discards_suppression_created_by_failed_dispatch`

There is no near-real NPC state-machine discovery test and no near-real direct hidden-discovery test. Existing `test_bdd_group_admission.py` only checks a fatigue premise. Missing connected evidence includes:

- Switch the player target to the admitted NPC and inspect the real instruction set: normal group actions present, invite absent, end-group retained.
- Direct hidden-discovery initial conversion, refusal, existing-group end, and other panel selections.
- Both wrapper load orders, repeat load, hot reload, same-NPC nesting, different-NPC interleaving, no-outer return, and exception/caught-exception cleanup.

Static simulation and user choice come before running these tests.

## Fable Final Simplification Review Record (2026-07-14)

### Failed invocation prompt

```text
/investigate-game-bug

只读审查，不得修改任何文件。候选工作树是 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，固定点 upstream/master，候选 HEAD 7dbe0e04b。OpenSpec 在 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。请实际阅读 git diff upstream/master...HEAD、两条生产 caller 路径、design/spec/tasks，并判断：1) 这个 panel callback 同步结算 + 单字段 DiscoverySettlementResult + 四层透传，是否已经是根因层面最简单、最易 maintainer 肉眼审查的修法；2) 精确一次、follow-up 顺序、仍 current replacement、direct caller 边界、无 explicit reaction 和 scheduler tail 是否自洽；3) 是否有可删除的抽象或真实 correctness 问题。不得沿用旧候选结论。输出明确 PASS/FAIL、actionable findings（文件和行号）及 residual risk。
```

## Minimum-Penalty Fable Review (2026-07-14)

### First prompt

```text
/investigate-game-bug

只读 fresh design critic，不得修改任何文件。候选工作树为 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，当前候选 HEAD 884b2fa30，基线 upstream/master 3a1c9e620；中央 OpenSpec change 为 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。本地 investigate-game-bug skill 刚更新：在所有逻辑正确且保持必要行为的生产修复中，必须选择最低 penalty `3a - b`，a 为最终 diff 新增行，b 为删除行，不得通过删除必要行为、测试或无关代码刷分。

用户要求依据新规则重新探索更小、逻辑等价、对人类更易审查的修法；若存在则实现。当前生产 diff 为 a=33、b=30、penalty=69，四文件布尔透传：面板 callback 同步结算明确反应并保存 bool，state 40 和 find_character_target 透传，character_behavior 仅在 flag 为假或当前行为为 MOVE 时保留原外层结算。

已核验的不可丢合同：
1. NPC state-machine caller 和 hidden_sex_panel direct caller 上，每个已有明确发现者反应都恰好结算一次。
2. DISCOVER_OTHER_SEX_AND_JOIN 与结束 H 的发现者反应先于 nested player update，避免当前 behavior 被覆盖。
3. 成功转隐奸或转露出没有发现者侧明确反应，NPC caller 仍按上游结算 SHARE_BLANKLY，direct caller 仍没有外层 NPC 结算。
4. effect 1721 产生的 MOVE 在 NPC caller 同轮继续结算，在 direct caller 留待之后正常 NPC 回合。
5. 普通状态机和 scheduler tail 不变；异常不留下跨操作 suppression。

已核验的结构事实：Tk 与 Web 的按钮基础设施都执行 cmd_func 但丢弃其返回值；find_character_target 通过注册状态机间接进入面板；nested player update 可能在面板返回前改写发现者当前 behavior；SHARE_BLANKLY 虽然 effect 是 NOTHING，judge_character_status 仍执行 before/after event 检查，所以不能把它无条件跳过。

中央 design 记录了这些候选：只补截图 case 约 a=1/b=0/3，但不满足两 caller 和 sibling exact-once，故不合格；旧 generic result 候选 a=65/b=29/166，正确但过大；当前 bool a=33/b=30/69；拟议 compact bool 预计 a=28/b=38/46，保持同一四层结构，只去掉 scheduler 中间变量、把 flag 初始化压成一行中文注释、将两个必须更新的多行函数 docstring 压成完整的一行中文输入/返回合同，不扩修旧文档债。

请实际读取更新后的 local skill、当前 diff、原始 upstream casework、两条 caller、UI callback 实现、测试和 OpenSpec design。判断：
- compact bool 是否保持全部逻辑与异常/嵌套边界；
- 是否存在 penalty 更低且仍明确、可维护、符合项目注释规范的正确候选；
- absent-attribute/getattr、行为历史推断、全局 marker、无条件 state-machine sentinel 等是否应因隐藏状态或语义变化排除；
- 当前计划的文档压缩是否是相关合同更新，还是违反“不可删除无关代码刷分”。

输出明确 PASS 或 FAIL；列出可执行的最低-penalty 代码形状、预计或可核验的 a/b/penalty，以及任何必须在编辑生产代码前解决的阻塞项。不要因为当前实现已通过测试就默认保留，也不要只按行数接受不透明技巧。
```

### First invocation result

The exact invocation was:

```text
claude -p --model claude-fable-5 --effort high --no-session-persistence "$PROMPT"
```

It was externally terminated after 296.2 seconds with exit code 143 and produced no verdict. It is retained as a failed review attempt and was not used to authorize the production edit.

### Retry prompt

```text
/investigate-game-bug

只读 fresh critic，不得修改文件。工作树 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，HEAD 884b2fa30，基线 upstream/master 3a1c9e620；OpenSpec 为 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。请读取刚更新的 local investigate-game-bug skill、最终 diff、两条 caller、UI callback、28 项测试及 design 的“2026-07-14 Minimum-Penalty Re-evaluation”。新规则要求在所有逻辑正确的生产修复中最小化 `3a - b`。

必须保持：两 caller 的已有明确发现者反应恰好一次；反应先于 nested player update；成功转隐奸/露出在 NPC caller 仍结算 SHARE_BLANKLY、direct caller 无外层结算；effect 1721 的 MOVE 在 NPC caller 同轮结算、direct caller 留待以后；普通状态机、事件检查、scheduler tail、异常边界不变。Tk/Web 丢弃按钮 callback 返回值；nested update 可覆盖 behavior；SHARE_BLANKLY 的 judge 仍跑事件，不能无条件省略。

当前 bool 方案 a=33,b=30,penalty=69。设计拟将同一四层 bool 结构压为预计 a=28,b=38,penalty=46：scheduler 直接在 if 中调用 find_character_target，flag 初始化与中文说明一行，两个因返回合同必须修改的函数 docstring 各压成完整的一行中文目的/参数类型/返回类型。只补单 case 不满足合同；旧 generic result 为 65/29/166。

请判断该 compact bool 是否等价、文档压缩是否属于相关合同更新；并寻找 penalty 更低但仍显式、可维护、符合注释规范的正确方案。明确排查 absent-attribute/getattr、行为历史、全局 marker、无条件 state-40 sentinel 是否因隐藏状态或行为变化不合格。输出 PASS 或 FAIL、最低可接受代码形状、a/b/penalty；若无法精确计数说明需实现后复核。只回答本设计问题。
```

### Retry verdict

```text
**PASS**(有一处可再省 3 分的修正,见下)。compact bool 与现方案逻辑等价,文档压缩属于合法的合同更新;四类"省行"替代方案均确认不合格。以下为逐项裁定。

## 等价性:compact bool = 现方案

我逐行核对了 884b2fa30 的最终 diff、`character_behavior.py:170-174` 的 scheduler、`handle_npc_ai.py:423` 与 `StateMachine/default.py:1324` 两个透传点、面板全部 7 个结算调用点,并实跑 28 项测试(28 passed)。

1. **scheduler 内联调用**:`if not handle_npc_ai.find_character_target(...) or character_data.behavior.behavior_id == constant.Behavior.MOVE:` 与现有局部变量版严格等价——Python 从左到右求值,find 恰好调用一次且先于 behavior_id 读取;find 返回 falsy 时短路,judge 照跑,与上游"无条件 judge"在所有 None/False 路径上一致。唯一行为差异仍只是"state-40 已结算且非 MOVE 时跳过外层 judge",即本修复本身。行长约 120 字符,Black(200)合规。
2. **flag 初始化压一行**:语义不变。相邻属性用"下一行 docstring"式注释,尾注释是本改动里唯一的风格偏离,但中文、显式,可接受;维护者若要求统一,恢复两行只多 3 分。
3. **回调返回值通道**:实证确认 Tk(`flow_handle.py:234`)与 Web(`flow_handle_web.py:321`)都以 `cmd_func(*args, **kw)` 调用后丢弃返回值,所以实例 flag + `draw()` 返回是必要通道;yrn→是否结算的映射依赖回调内运行时分支(骗过成功/失败、转换成功/失败),不能静态由选项号推出。四个 return hop 均结构必需。

## 文档压缩:合法

两个函数的返回合同确实改变,docstring 必须动;将整个多行 docstring 重写为一行完整中文合同(目的+参数类型+返回类型)满足 CLAUDE.md 的函数注释三要素,不删除任何信息,且一行式在本改动自身代码(helper docstring、测试文件)已是既有风格。判定为相关合同更新,不算刷分删除。`now_time` 一并写入一行合同,零成本,应包含。

## 四类替代方案:全部不合格(已逐一排查)

- **absent-attribute/getattr**:把 flag 从 `__init__` 移出、`draw()` 用 `getattr(self, ..., False)`——最多省 3 分,但属性从类的显式声明中消失,是隐藏状态协议;不满足"显式、可维护"。排除。
- **行为历史推断**:结算后的角色状态与"状态机新赋值待结算"不可区分——每个普通状态机本来就会改 behavior_id 再等外层 judge,且非 MOVE 反应(如 SEE_H_BUT_IGNORE)结算后 behavior 仍停留在该值。逻辑错误。排除。
- **全局 marker**:群交转换的 nested player follow-up 会在 `draw()` 返回前重入 scheduler 处理同一发现者(测试 `_nested_tick` 即刻画此路径),全局位会被嵌套轮误读/误清;direct caller 设了 marker 却没有外层消费者,毒化下一个 NPC 轮。破坏 operation identity。排除。
- **无条件 state-40 sentinel**:成功转隐奸/露出不结算发现者反应,NPC caller 必须照常跑 SHARE_BLANKLY 的 judge(事件检查),无条件 True 会吞掉它——`test_successful_mode_switch` 期望 npc caller 结算 `["share_blankly"]`,该方案直接红。排除。

## 最低可接受形状与计分

Compact candidate 4,**外加一处修正**:删掉现 diff 中 `sex_be_discovered_panel.py` 类定义前新增的那个空行(纯格式化,与修复无关,白付 3 分)。我按最终 diff 逐 hunk 重算:

| 文件 | a | b |
|---|---|---|
| character_behavior.py(内联 if) | 3 | 3 |
| handle_npc_ai.py(一行 docstring + return) | 2 | 6 |
| StateMachine/default.py(同上) | 2 | 6 |
| sex_be_discovered_panel.py(去空行、flag 一行) | 20 | 23 |
| **合计** | **27** | **38** |

**penalty = 81 − 38 = 43**(保留空行则为设计预估的 28/38/46;设计预估的 a=28 与我的 27 之差就是这一空行)。此数为静态重构计数,须按 design 自己的要求在实现后用 `git diff --stat` 复测,并重跑 28 项测试确认全绿。未发现更低且仍显式合规的正确形状:helper 已消重 7 处、MOVE 例外放在 scheduler(其语义所有者)、再压缩只能走上述四条被排除的路。
```

## Fable Final Simplification Review Record (continued)

### Failed invocation verdict

```text
FAIL — 无法执行审查：本会话没有可用的文件读取或 shell 工具。

当前环境只暴露了两个与任务无关的 OAuth 认证工具（Adobe、Gmail MCP），`Bash`、`Read`、`Grep` 等全部不可用，我无法：

- 读取 `/home/ubuntu/games/erArk-pr-discovery-settlement-redo` 的 `git diff upstream/master...HEAD`
- 追踪两条生产 caller 路径
- 阅读 `openspec/changes/fix-discovered-reaction-settlement/` 的 design/spec/tasks

按规则我不能在未读源码的情况下给出 PASS/FAIL 或对"panel callback 同步结算 + DiscoverySettlementResult 四层透传"的设计裁决——那只会是编造的结论。

请在启用了文件/shell 工具的会话中重新运行此命令，或调整本会话的权限配置后重试。
```

The failed invocation incorrectly disabled Claude Code's normal tools. It was retried with the exact skill-required command shape and normal tool access.

### Successful invocation prompt

```text
/investigate-game-bug

只读审查，不得修改任何文件。候选工作树是 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，固定点 upstream/master，候选 HEAD 7dbe0e04b。OpenSpec 在 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。已核验事实：相对 upstream/master 的生产 diff 是 4 个文件、+65/-29；本地行为矩阵 28 项通过；两个生产 caller 分别是 NPC 状态机路径和 hidden_sex_panel.settle_discovered 的直接路径。旧的 pending/commit 三字段协议已删除。请实际阅读 git diff upstream/master...HEAD、两条生产 caller 路径、design/spec/tasks，并判断：1) 这个 panel callback 同步结算 + 单字段 DiscoverySettlementResult + 四层透传，是否已经是根因层面最简单、最易 maintainer 肉眼审查的修法；2) 精确一次、follow-up 顺序、仍 current replacement、direct caller 边界、无 explicit reaction 和 scheduler tail 是否自洽；3) 是否有可删除的抽象或真实 correctness 问题。不得沿用旧候选结论。输出明确 PASS/FAIL、actionable findings（文件和行号）及 residual risk。
```

### Successful invocation verdict

```text
## 结论:PASS

我实际读取了 `git diff upstream/master...HEAD`(4 文件,+65/-29,与所述一致)、两条生产 caller、全部回调路径以及 design/spec/tasks。判定如下。

### 1) 修法是否已是根因层面最简 — 是

- 面板是两条生产 caller(`Script/StateMachine/default.py:1324` 状态机路径、`Script/System/Sex_System/hidden_sex_panel.py:253` 直接路径)唯一共用的代码,是精确一次结算的唯一可行 owner。按 caller 猜测所有权(旧方案)和全局 flag/session teardown 均已被正确否决,理由在 design.md:31-33 成立。
- 四层透传是最小管线:`find_character_target` 全库只有一个调用点(`character_behavior.py:171`),状态机是注册表分发,返回值沿现有调用链上传,零新增状态。替代方案(挂在 character_data 上的 flag)是隐藏全局状态,更差。
- `DiscoverySettlementResult` 单字段 frozen dataclass 不可再删:必须区分"无显式反应"(`None`)与"已结算、无替换行为"(`Result(None)`),裸字符串编码不了这两态。行为 id 是字符串(`Behavior.py:334`),`Optional[str]` 注解正确。

### 2) 六项语义自洽性 — 全部核验通过

- **精确一次**:全部 6 个显式反应(DECEIVED/IGNORE/LEAVE/JOIN/REFUSE/INTERRUPT)都走 `_settle_discoverer_reaction`(panel:63-78);外层调度器仅在替换行为仍 current 时补结算一次(`character_behavior.py:181`)。上游的两类故障(状态机路径重复结算 3 条、直接路径漏结算 3 条)均被同一机制修复。
- **follow-up 顺序**:`DISCOVER_OTHER_SEX_AND_JOIN` 先结算(panel:264)再跑玩家群交转换(panel:265);`_end_current_h` 先结算(panel:281)再 `handle_h_end`/`handle_group_sex_end`。嵌套玩家更新无法再擦除未消费的反应。
- **仍 current 替换**:快照在 panel:76-77,校验在 character_behavior.py:181,过期即丢弃,与 design.md:47 声明一致。
- **direct caller 边界**:`settle_discovered` 有意忽略返回值,反应已由面板提交;替换行为留待该角色后续正常回合。与 design.md:39 一致。
- **无显式反应路径**:隐奸/露出转换成功时 `_settlement_result` 保持 `None`,`draw()` 返回 `None`,外层走原有 `judge_character_status`,与上游行为逐位一致。
- **scheduler tail**:跳过分支仅省掉重复的 `judge_character_status`;realtime 结算、持续状态、打断判定、time_over(character_behavior.py:191-198)在所有分支照常执行。`find_character_target` 的早返回(handle_npc_ai.py:427)之后只有注释,未跳过任何逻辑。

### 3) 可删抽象 / 可选改进(非阻塞)

- **`character_behavior.py:172-185`**:三路分支在两个 arm 里重复了 `judge_character_status`。可压成两路:`if isinstance(dispatch_result, DiscoverySettlementResult): …仅结算仍 current 的替换… else: judge_character_status(...)`(`None` 自然落入 else)。省约 6 行,maintainer 肉眼审查更快。当前写法正确,改不改由你。
- 无其他可删抽象;无 pending/recommit/全局 wrapper 残留(已 grep 确认)。

### Residual risk

1. **直接路径的替换行为永不获得效果结算**(NPC 循环只对 SHARE_BLANKLY/MOVE 结算,替换行为只会跑完 duration 后转空闲)。上游基线该路径整个反应都不结算,故严格无回归;已在 design.md:39 记录为边界。
2. **结算文本时序**:状态机路径下结算输出现在出现在面板循环返回之前(回调内),上游是面板关闭后。已被接受的 Tk A/B 证据覆盖此可见差异。
3. **回调内异常**:`behavior_id` 赋值后、结算前抛异常会留下未结算行为——与上游任何结算失败等价,design.md:48 已明确不承诺事务回滚。

以上为静态代码审查结论;28 项行为矩阵通过是你方提供的已核验事实,我确认了测试文件存在(`tests/test_discovery_settlement_ownership.py`,11 个测试函数)但未重跑。tasks.md 2.3(fable 起草 + 独立 artifact review)仍是发布前的未完成门。
```

The final code implements Fable's optional branch simplification. Fresh standards, specification, architecture-simplicity, and settlement-ownership reviewers then passed amended head `52eb801de`.

## Fable Boolean Simplification Review Record (2026-07-14)

### Superseded invocation prompt

The first invocation used unsafe double-quoted shell transport, so its backtick-delimited code fragment produced shell substitution noise. The intended prompt was:

```text
/investigate-game-bug

只读设计审查，不得修改文件。候选工作树 /home/ubuntu/games/erArk-pr-discovery-settlement-redo 当前 HEAD 52eb801de，基线 upstream/master=3a1c9e620；OpenSpec change 在 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/，刚更新为待实现的简化设计。用户指出当前 4 文件 +58/-31（净增27）和自定义 DiscoverySettlementResult 对人类维护者不够友好，并要求保留原有 NPC 'find_character_target 后 judge_character_status' 骨架，只局部修被发现 case，目标约净增10行。已核验生产事实：两个 caller 仍要求 panel callback 同步结算；当前所有明确发现反应中，只有 REFUSE_JOIN_GROUP_SEX、SEE_H_BUT_DECEIVED、SEE_H_AND_LEAVE 通过 Behavior_Effect 1721 把当前行为替换为 MOVE，其余不产生非 MOVE replacement；注册的 state-machine handler 目前没有其他 handler 返回 bool。拟议方案：panel 保存并返回 bool 'explicit reaction already settled'；state 40 和 find_character_target 原样透传；character_behavior 保留原 judge 调用，只加 `if not discovery_reaction_settled or behavior_id == MOVE:`，因此普通路径照旧、已结算反应跳过、MOVE 仍同轮结算、direct caller 忽略 flag。请实际读取 diff、两条 caller、Behavior_Effect 和更新后的 design/spec/tasks，判断这个布尔 + MOVE 局部 case 是否是正确且更适合 maintainer 审查的最小修法，还是有现实生产 case 必须保留 generic replacement result。输出明确 PASS/FAIL、具体反例（若有）、以及最小可接受代码形状。
```

### Superseded invocation verdict

```text
**判定:PASS** —— 布尔 flag + 一个局部 MOVE 条件是正确的,且明显比自定义 `DiscoverySettlementResult` 更适合 maintainer 审查。未找到必须保留通用 replacement 协议的生产反例。

## 实际核验的证据

**Behavior_Effect 1721(读取 `data/csv/Behavior_Effect.csv` + `Script/Settle/default.py:2656`):**
- 1721 = `MOVE_TO_OWN_DORMITORY`,实现是调用 `general_movement_module(角色, 宿舍)`,只可能把行为设为 `MOVE`(寻路失败则行为不变,两种方案下都正确跳过 judge)。
- 带 1721 的发现反应仅 `refuse_join_group_sex`、`see_h_but_deceived`、`see_h_and_leave`(CSV 行 172/186/187)。其余反应(`see_h_and_interrupt`、`see_h_but_ignore`、`join_group_sex`、`discover_other_sex_and_join`)的效果全是数值/心情/flag 类(23、24、364、462、602、604、1408、1418、1511、1512、1523、1524、1602、10010),逐一对照 `constant_effect.py` 确认没有任何一个改写 `behavior_id`。CSV 里另一个用 1721 的是 `pee`(行 36),不经过发现面板,无关。
- **结论:替换行为的封闭集 = {MOVE}。**布尔 + `behavior == MOVE` 判断与 `replacement_behavior_id` 协议在全部生产路径上行为等价。

**两条 caller:**
- 状态机 40(`Script/StateMachine/default.py:1307`):同步 draw,返回值可原样透传。
- 直连 caller `hidden_sex_panel.settle_discovered`(`hidden_sex_panel.py:253`):`now_panel.draw()` 本来就丢弃返回值,忽略 flag 无需改动;MOVE 留待该角色下一正常回合的 `elif MOVE` 分支结算,与 design 声明一致。

**透传安全性:**扫描了全部注册 state-machine handler(`Script/StateMachine/default.py` + `Script/System/Dormitory_System/dormitory_manager_system.py`,仅此两处注册),除 state 40 外没有任何 handler 返回非 None(default.py:57/63 的 `return True/False` 属于 helper `general_movement_module`,且没有 handler `return` 它的结果)。透传不会误伤。

**一处布尔方案反而更稳的细节:**当前结果类在 `_settle_discoverer_reaction` 内、嵌套玩家 follow-up(如 `OTHER_SEX_BE_FOUND_TO_GROUP_SEX` 结算)**之前**快照 replacement;布尔方案在 `character_behavior` 里读取的是 follow-up 之后的最终行为。若嵌套结算再次改写发现者行为,布尔判断用的是真实现场状态——语义上更准,不是妥协。

## 最小可接受代码形状(净增 ≈10 行)

```python
# sex_be_discovered_panel.py —— __init__: self._settled = False
def _settle_discoverer_reaction(self, behavior_id: str) -> None:
    from Script.Design import character_behavior
    self.find_chara_data.behavior.behavior_id = behavior_id
    self.find_chara_data.behavior.duration = game_config.config_behavior[behavior_id].duration
    character_behavior.judge_character_status(self.character_id)
    self._settled = True

def draw(self) -> bool:            # 循环出口处
    ...
    return self._settled

# StateMachine/default.py:1325 —— return now_panel.draw()   (维持现状)
# handle_npc_ai.py:427 —— return constant.handle_state_machine_data[...](character_id)   (维持现状)

# character_behavior.py
settled = handle_npc_ai.find_character_target(character_id, now_time)
# 面板已同步结算明确的发现反应;效果1721产生的移动仍需当轮结算
if not settled or character_data.behavior.behavior_id == constant.Behavior.MOVE:
    judge_character_status(character_id)
```

同时删掉的坏味道:`character_behavior.py` 里 Design 层反向 import Sex_System 面板类(现 diff 第 172 行)——这本身就是维护者会拒的依赖倒置,布尔方案顺带消除。

## 两点备案(不阻塞)

1. **共同的既有属性,非本次差异:**两种方案都让 1721 产生的 MOVE 在 `SHARE_BLANKLY` 分支内当轮结算(比 baseline 的下一轮 `elif MOVE` 早一拍)。这是已被 A/B 证据覆盖的既定候选行为,与 bool-vs-result 之争无关。
2. **文档小瑕疵:**`design.md` 第 53 行 "Current Implementation Disposition" 用现在时描述"无自定义结果类",但 HEAD 52eb801de 仍含 `DiscoverySettlementResult`(tasks 1.6 未勾)。实现 1.6 后自然一致;若在实现前送审文档,建议改为目标态措辞。未来若出现非 MOVE 的替换效果,`design.md` 第 47 行的风险条目已正确记录扩展路径,无需现在预建协议。
/bin/bash: command substitution: line 2: syntax error: unexpected end of file
```

Because the shell transport altered this invocation, it was not used as the final acceptance record. The final head was reviewed again with safely quoted input below.
### Final safely quoted Fable review prompt

```text
/investigate-game-bug

只读最终实现审查，不得修改文件。候选工作树 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，最终候选 HEAD 884b2fa30，基线 upstream/master 3a1c9e620。OpenSpec change 位于 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。用户要求保持原有 NPC 寻找行为后结算的结构，仅局部处理被发现 case，并把人类审查成本和净增行数压低。最终生产 diff 是四个文件 +33/-30，净增3行；本地行为矩阵28项通过。实现为：panel callback 同步结算明确反应并保存 bool；state 40 与 find_character_target 透传 bool；character_behavior 保留原 judge_character_status 调用，仅加条件 `if not discoverer_reaction_settled or behavior_id == MOVE`。已静态核验发现反应的生产 replacement 封闭集只有 Behavior_Effect 1721 产生的 MOVE，其他注册 state-machine handler 不返回 bool。请实际读取最终 diff、两条 caller、Behavior_Effect、测试与更新后的 design/spec/tasks，判断最终实现是否正确、是否满足局部修 case 和 maintainer 易审查目标、是否仍有必须修复的生产反例。输出明确 PASS/FAIL、actionable findings 和 residual risk。
```

### Final safely quoted Fable review verdict

```text
## 结论：PASS

我实际读取了最终 diff（`3a1c9e620..884b2fa30`，4 文件 +33/-30）、两条生产 caller、状态机注册全集、Behavior_Effect 数据、28 项测试与更新后的 design/spec/tasks/proposal/implementation-notes，并重跑了测试（28 passed）。实现正确，满足"局部修 case + maintainer 易审查"目标，未发现必须修复的生产反例。

### 核验结果

**1. 精确一次结算 — 逐分支核对通过。** 六个显式反应全部收敛到 `_settle_discoverer_reaction`（sex_be_discovered_panel.py:53）。对照基线：
- `join_group_sex` / `see_h_and_interrupt`：基线内层+外层双结算（重复 bug）→ 现在仅内层，外层被 flag 跳过 ✓
- `discover_other_sex_and_join`：基线先跑玩家群交转换、可能擦除待结算反应（丢失 bug）→ 现在先结算再转换（sex_be_discovered_panel.py 中顺序对调是本修复的核心）✓
- `refuse_join_group_sex`（1721→MOVE）：新旧行为逐位一致（基线内层结算后外层无条件结算 MOVE，等于新代码的 `or MOVE` 分支）✓
- 隐奸/露出转换成功（无显式反应）：flag 保持 False，外层原样结算，与基线一致 ✓

**2. 封闭集声明 — 独立复核成立。** `add_state_machine` 注册只存在于 `Script/StateMachine/default.py` 和 `Script/System/Dormitory_System/dormitory_manager_system.py`。逐一检查：唯一返回值的注册 handler 是 state 40（default.py:1324）；`general_movement_module` 返回 True/False 但没有任何 handler `return` 它的结果；dormitory 文件中带返回值的都是未注册 helper。`find_character_target` 只有一个调用点（character_behavior.py:171）、一个 dispatch return（handle_npc_ai.py:426）。1721 = `MOVE_TO_OWN_DORMITORY`，反应行为中带 1721 的恰为 deceived/leave/refuse 三个 — 与 design 声明一致。

**3. 直接 caller 边界正确。** hidden_sex_panel.py:253 丢弃返回值：反应已由面板提交，1721 产生的 MOVE 留待该 NPC 下一轮 `elif MOVE` 分支结算；基线在该路径上整个反应都不结算，严格无回归。

**4. maintainer 易审查目标达成。** 生产 diff 净增 3 行；两处透传是单行 `return`，调度器改动是一个带中文注释的局部条件；无新类型、无全局状态、无注册表改动。旧 `DiscoverySettlementResult` 协议已在 884b2fa30 彻底移除（grep 确认无残留）。

### Actionable findings（均为文档级，非阻塞实现）

1. **tasks.md 1.6 未勾选但已完成** — 884b2fa30 正是"布尔 flag + 局部 MOVE case"的落地；**2.1 同样**（28 项矩阵存在且通过）。发布评审前应在主仓 main 更新勾选状态。
2. **proposal.md "Current Status" 过期** — 仍写"is being simplified from local head `52eb801de`"；应改为最终 head 884b2fa30 已完成简化。

### Residual risk（低，均已在 design 记录或有测试覆盖）

- **未来非 MOVE 替换效果**：若日后给发现反应新增会替换行为的效果，需同步扩展该局部条件，否则外层结算被静默跳过。design.md:47 已声明此为有意的封闭集权衡。
- **deceive/leave 的 MOVE 提前一轮结算**：相对基线早一个 NPC 循环轮次开始移动（与基线 refuse 路径的既有时序对齐）；`test_npc_refusal_progresses_the_new_move_in_the_same_round` 覆盖，游戏时间上无差异。
- **回调内异常**：behavior 赋值后、结算前抛异常会留下未结算行为 — 与上游任何结算失败等价，design.md:48 已声明不承诺事务回滚。

发布仍以 tasks 2.3（fable 起草 + 独立 artifact review）和第 3 节的逐项用户授权为门槛，本审查不解锁任何 outward 动作。
```

## Fable Exhibition-Transition Semantics Review (2026-07-14)

### Prompt

```text
/investigate-game-bug

只读游戏语义裁决，不得修改任何文件。候选工作树为 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，候选 HEAD 884b2fa30，基线 upstream/master 3a1c9e620；OpenSpec change 为 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。

需要裁决的问题：玩家在“被发现”面板中从普通 H 成功转为露出时，是否必须再给第三人发现者结算一个明确 NPC 反应，还是允许只记录“已经目击”并结算玩家与当前 H 对象的转露出行为。用户当前判断是“转露出确实可以不用发现者反应，我觉得没问题”，但要求结合游戏其他部分的语义设计由 Fable 决定。

已核验事实：
1. Sex_Be_Discovered_Panel.draw 一打开就为第三人发现者设置 see_pl_h=True、把目标转为玩家，并记录发现者名字；这发生在任何选项之前。see_pl_h 在生产代码中只用于“本次玩家与他人 H 已被该 NPC 目击”的 premise、排除同一行动中的重复隐奸发现者，并在玩家 MOVE 时统一清除。
2. 非露出状态的选项文案是“光明正大地展示，转为露出”。成功后 exhibitionism_sex_panel 结算 OTHER_SEX_BE_FOUND_TO_EXHIBITIONISM_SEX；Behavior_Data 将其 actor 记为 both，Behavior_Effect 只作用于 A1/A2，口上是“{Name}和{TargetName}的H被{HInterruptCharaName}发现了，于是干脆直接公开露出H”，成就 934 是“在H被目击后成功转为露出H模式”。该行为覆盖玩家与当前 H 对象，不给第三人发现者设置 SEE_H_BUT_IGNORE / SEE_H_AND_LEAVE / SEE_H_AND_INTERRUPT。
3. 成功转隐奸同样只结算玩家侧 OTHER_SEX_BE_FOUND_TO_HIDDEN_SEX，没有明确发现者行为。当前本地测试把这两种成功模式转换都定义为“无明确发现者行为”。
4. 如果玩家本来已经处于露出模式，同一个按钮文案改为“无视对方，正常继续”，代码会依据发现者实行值明确结算 SEE_H_BUT_IGNORE、SEE_H_AND_LEAVE 或 SEE_H_AND_INTERRUPT。
5. 上述“新转露出成功时没有第三人反应”的生产行为在 upstream/master 已存在，相关分支主体可追溯到 2025 年；候选没有改变该 case 的运行结果。NPC caller 在结果为 False 时仍按原流程结算发现者当前 SHARE_BLANKLY；hidden_sex_panel 的 direct caller 原本和现在都不做外层 NPC 结算。
6. 当前 PR 的边界是修复已经存在的明确发现者反应在两条 caller 上丢失或重复结算，并保持上游没有明确反应的模式转换语义；不是为所有“已发现”场景新增反应。

请实际读取相关源码、行为 CSV、口上、成就、两条 caller、当前 diff 和测试，结合 erArk 的行为/结算语义裁决：
- 成功“新转露出”只有 see_pl_h 记录和玩家/对象的转露出结算、没有第三人明确反应，是否语义完整且应由本 PR 保持？
- 它与“已经处于露出时必须结算发现者反应”的不对称是否有合理的行动所有权解释，还是构成必须在本 PR 中修复的生产缺口？
- 当前 bool=False 和把隐奸/露出成功模式转换归为“无明确发现者反应”的测试是否正确？

输出明确 KEEP 或 CHANGE；给出游戏全局语义理由、对当前 PR 边界的结论，以及若 CHANGE 时最小必须修改的生产行为。不要仅以“上游原来如此”为理由。
```

### Verdict

```text
**裁决：KEEP。** 成功“新转露出”只结算玩家/对象侧的转露出行为、不给第三人发现者结算明确反应，是语义完整的设计，本 PR 应当保持，而不是必须修复的生产缺口。

## 游戏全局语义理由（基于实际读取的代码与数据）

**1. 面板的结算模型是“每次面板退出恰好结算一个主行为，归属于做出决定性动作的角色”。** 我核对了候选面板的全部五条出口（`sex_be_discovered_panel.py:177-271`）：

| 出口 | 主结算行为 | actor（Behavior_Data.csv） |
|---|---|---|
| 话术支开成功 | `see_h_but_deceived` (392) | npc |
| 已露出时无视/离开/打断 | `see_h_but_ignore`/`see_h_and_leave`/`see_h_and_interrupt` (394/393/391) | npc |
| 邀请加入群交成功/拒绝 | `discover_other_sex_and_join`/`refuse_join_group_sex` | npc |
| 转隐奸/转露出成功 | `other_sex_be_found_to_hidden_sex` (382, actor=pl) / `other_sex_be_found_to_exhibitionism_sex` (388, actor=both) | pl / both |
| 任何失败 | `see_h_and_interrupt` | npc |

没有任何出口是零结算。差别只在**结算的归属者**：当决定性动作是发现者做的（无视、离开、打断、被骗、加入、拒绝），行为记在发现者头上；当决定性动作是玩家做的（把 H 转成公开露出/藏起来），行为记在玩家侧，`Behavior_Effect.csv:182` 的效果只作用 A1/A2，口上通过 `HInterruptCharaName` 把发现者写进玩家侧叙事。成就 934 也以玩家为主语。这是一贯的行动所有权模式，不是遗漏。

**2. 发现者的生命周期由 `see_pl_h` 见证标记闭环，不依赖明确反应行为。** 关键证据是 `data/target/default/target.csv` 的目标 601：状态机 40（触发被发现面板）的前提含 `not_witness_pl_h_with_others`。即游戏对“目击者”的设计契约是：每个 NPC 对本次 H **恰好进入一次面板**，进入即打 `see_pl_h`，之后被 601 排除，回归普通 AI，玩家 MOVE 时统一清除（`character_behavior.py:143`）。转露出后 H 仍是非隐奸 H，**后续新来的 NPC 依然会触发 601 并走“已露出→按实行值结算明确反应”的分支**——所以“已露出时必须结算发现者反应”和“转露出瞬间不结算”并不矛盾：前者是该回合唯一发生的事（玩家“正常继续”，没有新动作可结算，只剩发现者的反应可写）；后者的结算名额被玩家的转变动作占用了，发现者按外层原流程落到 `SHARE_BLANKLY`——叙事上就是愣在原地看着玩家公开化，机制上保持了“每个 NPC 回合结算一次当前行为”的调度不变量。

**3. 若 CHANGE，需要发明新的游戏语义，超出任何已有证据。** 给转露出成功追加发现者反应，必须回答“哪个反应、按谁的实行值判”——转露出成功与否目前判的是 H 对象的露出接受度（`exhibitionism_sex_panel.py:141`），发现者的意愿根本不参与。追加 `see_h_but_ignore` 之类会给发现者叠一份猥亵类行为效果，改变数值结果，且没有上游口上、CSV、成就任何一处支持这个组合。这是设计提案，不是缺陷修复。

## 对 PR 边界的结论

本 PR 的契约是“已存在的明确发现者反应在两条 caller 上恰好结算一次”，候选 diff（面板返回 bool、`find_character_target` 透传、调度器仅在已结算时跳过外层 `judge_character_status`）正确地把转露出/转隐奸成功归为 `False` 路径，让外层按原流程走。保持这个边界。

有一处**记录在案但不在本 PR 修的设计褶皱**：一个本会打断 H 的低接受度发现者，可以被“转露出成功”永久中和（`see_pl_h` 使其无法再触发 601，也没有事后反应判定）。这是上游见证生命周期的既有设计后果，玩家可见影响是偏宽松的收益而非错误结算；如要收紧，应作为独立的游戏体验提案交用户和上游决定。

## 测试正确性

正确。`test_successful_mode_switch_keeps_no_explicit_discoverer_behavior` 断言 npc caller 结算 `["share_blankly"]`、direct caller 结算 `[]`、followup 为对应 `other_sex_be_found_to_*` 加成就——这精确刻画了上述所有权语义；其 docstring“刻画未定义发现者行为而不擅自修复”的定性也对（准确说是“无发现者侧明确反应”，而非“无结算”——玩家侧结算是存在的，测试本身已用 followup 断言覆盖了这一点）。`draw()` 对这两条路径返回 `False` 是对的。
```

## Minimum-Penalty Post-Implementation Fable Review (2026-07-14)

### Prompt

```text
/investigate-game-bug

只读 post-implementation 审查，不得修改任何文件。工作树 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，当前 HEAD 仍为 884b2fa30，基线 upstream/master 3a1c9e620；需要审查的是当前未提交 production diff。中央 OpenSpec 为 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/，其中已记录最低 penalty 规则和 fresh design critic。

请实际读取更新后的 local investigate-game-bug skill、`git diff upstream/master`、两条 caller、Tk/Web callback、28 项测试及 OpenSpec。已落地的目标形状应为四个生产文件 a=27、b=38、penalty=43：panel callback 通过一个 helper 同步结算明确发现者反应并在实例上保存 bool；draw、state 40、find_character_target 逐层返回；scheduler 内联调用 find，仅当返回 falsy 或结算后行为为 MOVE 时运行原 judge。两个返回合同 docstring 压成完整一行，flag 初始化和中文说明同一行，删除了一个纯新增空行。

必须保持：两 caller 的已有明确反应恰好一次；发现者反应先于 nested player update；成功转隐奸/露出在 NPC caller 仍结算 SHARE_BLANKLY、direct caller 无外层结算；effect 1721 的 MOVE 在 NPC caller 同轮结算、direct caller 留待以后；普通状态机、before/after events、scheduler tail、异常边界不变。不得接受隐藏属性、行为历史猜测、全局 marker 或无条件 state-40 sentinel。

请重算实际 a/b/penalty，重跑 28 项聚焦测试，检查 `git diff --check`，并判断实际落地是否与批准的 compact bool 方案逻辑等价、是否仍有更小而显式可维护的正确方案、是否存在必须修复的 production finding。输出明确 PASS 或 FAIL；列出计数、测试结果、actionable findings 和 residual risk。不要审查 PR 文案或执行 outward action。
```

### Failed invocation

The prompt was first invoked from the candidate worktree with the required command:

```text
claude -p --model claude-fable-5 --effort high --no-session-persistence "$PROMPT"
```

The candidate worktree did not contain the main repository's Claude skill link. The invocation exited in 1.2 seconds with code 0 and this exact output:

```text
Unknown command: /investigate-game-bug
```

It produced no review verdict and was not treated as acceptance. The identical prompt and command were then run from the main repository, whose Claude skill link points to the updated local skill.

### Verdict

```text
## 结论:PASS

实际落地与批准的 compact bool 方案(design.md 候选 4)逻辑等价,计数吻合,28 项测试全过,无必须修复的 production finding。

### 计数(实测,vs upstream/master 3a1c9e620,HEAD 884b2fa30)

| 文件 | a | b |
|---|---|---|
| character_behavior.py | 3 | 3 |
| handle_npc_ai.py | 2 | 6 |
| StateMachine/default.py | 2 | 6 |
| sex_be_discovered_panel.py | 20 | 23 |
| **合计** | **27** | **38** |

Penalty = 3×27−38 = **43**,与 OpenSpec 记录一致。`git diff --check` 干净(exit 0,无输出)。

### 测试:28/28 通过(6.66s)

测试名与合同逐条对应:三类群交反应 + 三类非群交反应 × 两 caller 恰好一次;NPC caller 的 MOVE 同轮推进 / direct caller 无外层回合;`see_h_and_interrupt` 在 player follow-up(单 H / 群交结束)之前结算;成功转隐奸/露出不留明确发现者行为(NPC 侧外层 SHARE_BLANKLY 结算保留);callback 返回值被丢弃时 draw 返回实例 flag;state 40 与 find 逐层透传;scheduler 只跳过外层 `judge_character_status` 且 tail 不变;普通状态机(None/False)保留外层结算;已消费的替换不被重放。

### 逻辑等价性核验(实读代码)

- **flag 载体必要性成立**:Tk(`flow_handle.py:349` `cmd_map[order]()`)与 Web(`flow_handle_web.py:321`)都在 `askfor_all` 返回前执行 callback 且丢弃返回值,实例 bool 是唯一显式通道。
- **无 truthy 泄漏**:全 default.py 只有 state 40 一个注册状态机返回值;`general_movement_module` 的 `return True/False` 无任何 `return general_movement_module(...)` 调用点,不会误触 scheduler 的跳过分支。即使未来出现,成功路径 behavior 已是 MOVE,会被 `or MOVE` 子句兜住。
- **effect 1721 确认**:`MOVE_TO_OWN_DORMITORY`,恰好挂在 `refuse_join_group_sex`、`see_h_but_deceived`、`see_h_and_leave` 三个离开反应上,与 scheduler 条件的封闭集一致。
- **direct caller**(hidden_sex_panel.py:249)按设计忽略返回值:反应已由面板结算,MOVE 留待正常回合。
- **禁止形状**:diff 中无隐藏属性、无行为历史推断、无全局 marker、无无条件 state-40 sentinel——只有实例 bool、显式 return 链、一个局部条件。
- **更小方案**:未发现。单分支补丁(penalty 3)不合格(漏 sibling caller 且双重结算);去掉 `or MOVE` 需面板替 direct caller 提前结算 MOVE,改语义;全局 flag 属禁止形状。四跳是两个 UI 丢弃 callback 返回值下的结构最小值。

### Findings(均非阻塞)

1. **文档小疵**:`find_character_target` 的单行 docstring 说"返回 bool 表示已结算,否则返回 None",但面板路径也可返回 `False`(bool)。实际合同是"truthy=已结算"。措辞略欠精确,不影响任何调用方。
2. penalty 优化确实通过压缩两个被触及函数的 docstring 换取 b——两处合同本就必须改写,且单行版保留了参数与返回说明,属已被 fresh critic 接受的范围,我判定不构成"删除换分"。

### Residual risk(与 OpenSpec 记录一致)

- 未来若有发现效果把反应替换成非 MOVE 的新行为,需扩展 scheduler 局部条件(设计已记录,不预建协议)。
- callback 中途异常的部分状态语义与 upstream 相同,本 diff 未增减事务性承诺。
- `tests/` 为 worktree 内未跟踪本地证据,不在生产 diff 中,符合边界。
```

The non-blocking docstring finding was corrected immediately afterward without changing line counts or runtime logic: the contract now states that the function returns `True (bool)` when the discoverer reaction was settled and otherwise returns `False (bool)` or `None`. The four production files were recompiled, all 28 focused tests passed again, `git diff --check` remained clean, and the production diff remained `a=27, b=38, penalty=43`.

## Style-Normalized Non-Blank Recount (2026-07-15)

The user changed the scoring rule so `a` and `b` count only non-blank lines and formatting must not be changed merely to improve the score. The candidate therefore restores the readable, project-normal source from `884b2fa30` without changing the four-file boolean settlement boundary.

### First Fable prompt

```text
/investigate-game-bug

只读 style-normalization 审查，不得修改文件。主仓为 /home/ubuntu/games/erArk；候选工作树为 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，当前 HEAD 9ec3bcee4，需审查当前未提交的四个 production 文件改动。基线 upstream/master 为 3a1c9e620，中央 OpenSpec change 为 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。

用户已更新本地规则：`a` 和 `b` 只统计非空行；不得为了改善数字改变代码风格。Codex 因此撤销 9ec3bcee4 中仅为计分做的压缩，恢复项目正常格式：scheduler 恢复具名局部变量，两个函数恢复项目常用的多行输入/返回 docstring，实例 flag 恢复相邻字符串说明，并恢复类定义前空行。四层 bool 通道、helper、所有分支顺序和运行逻辑不变；当前四文件内容应与 884b2fa30 逐字一致。

请实际读取更新后的 local skill、当前工作树 diff、884b2fa30、9ec3bcee4、两条 caller 和 28 项测试。按“只计非空增删行”的规则独立重算当前候选、7dbe0e04b、52eb801de、884b2fa30 和 9ec3bcee4；确认当前风格恢复是否逻辑等价、是否符合项目既有格式、是否仍残留仅为分数压缩的写法。重跑聚焦测试并检查 diff。输出明确 PASS 或 FAIL、各版本 a/b/penalty、任何必须修复的 finding。用户的计数和风格规则是既定约束，不要重新裁决它。
```

The exact required invocation ran for 360.1 seconds and timed out with exit code 124 without producing output. It yielded no verdict and was not treated as acceptance.

### Retry Fable prompt

```text
/investigate-game-bug

只读最终核验，不得修改文件。主仓 /home/ubuntu/games/erArk；候选 /home/ubuntu/games/erArk-pr-discovery-settlement-redo，HEAD 9ec3bcee4，审查当前未提交四文件 diff；基线 upstream/master 3a1c9e620。用户规则已写入 local skill：a/b 只计非空增删行，禁止为分数改变代码风格。

Codex 已把 9ec3bcee4 的计分型压缩恢复为项目正常格式；当前四个生产文件应与 884b2fa30 逐字一致，逻辑仍是 panel-owned bool 四层透传和 scheduler 局部 MOVE 例外。本地按非空行实测 a=30、b=30、penalty=60，28 项测试通过，diff check 干净。

请实际读取更新 skill、当前四文件 diff、884b2fa30 和聚焦测试，只核验：当前内容是否与 884b2fa30 一致；30/30/60 是否正确；风格恢复是否逻辑等价且符合项目惯例；测试是否通过；有无必须修复 finding。输出 PASS 或 FAIL。不要重算其他历史候选，不要讨论 PR 文案或证据。
```

### Retry Fable verdict

```text
**PASS**

核验结果（候选 worktree `/home/ubuntu/games/erArk-pr-discovery-settlement-redo`，HEAD 9ec3bcee4，基线 3a1c9e620）：

1. **与 884b2fa30 一致** ✓ — `git diff 884b2fa30 -- <四文件>` 输出为空，四个生产文件逐字一致。
2. **a=30 / b=30 / penalty=60** ✓ — 对基线 3a1c9e620 按非空行独立复算：增 30、删 30、3a−b=60，与声称完全一致（diff 中另有若干纯空行增删，按规则不计）。
3. **风格恢复逻辑等价且符合惯例** ✓ — 9ec3bcee4→当前的差异逐段核对，全部为风格还原、无逻辑变化：
   - `character_behavior.py`：内联条件拆回「赋值 + 注释 + if」，条件与短路顺序完全相同；
   - `handle_npc_ai.py` / `StateMachine/default.py`：单行 docstring 还原为项目标准的 `Keyword arguments:` 多行格式；
   - `sex_be_discovered_panel.py`：class 前补空行（Black 格式）、行内注释还原为该文件惯用的 `""" … """` 属性说明。新增私有方法用单行 docstring，与本文件既有私有方法（如 `_let_find_chara_away`）局部风格一致，非计分压缩。
   - 逻辑仍为 panel-owned bool 四层透传（panel.draw → 状态机 → find_character_target → scheduler）+ scheduler 局部 MOVE 例外，与 884b2fa30 设计相同。
4. **测试通过** ✓ — `pytest tests/` 实际运行：28 passed（11 个测试函数含参数化，覆盖 panel、隐奸路径、状态机、scheduler 来源）。
5. **必须修复的 finding** — 无。`hidden_sex_panel.py:249` 直接构造面板并忽略返回值，该路径不经 find_character_target，无重复结算风险，属既定设计范围。
```
## 2026-07-15 Ad-hoc Case Design Gate

The user retained the sibling-case scope but prohibited a unified settlement owner/helper. The accepted replacement restores the upstream response branches, adds `judge_character_status()` only to the four branches that currently omit it, and sets one panel-instance `skip_outer_settlement` result only for JOIN, DISCOVER, IGNORE, and INTERRUPT. MOVE-producing reactions keep the result false so the NPC outer loop processes the successor.

The design prompt is preserved verbatim in `fable-ad-hoc-case-design-prompt-20260715.md`. The first invocation timed out locally after 180 seconds with no verdict. The identical retry completed after 391 seconds; its PASS verdict is preserved verbatim in `fable-ad-hoc-case-design-verdict-20260715.md`. Fable rejected post-panel behavior-id inference because nested player updates can erase operation identity, and accepted the explicit per-case result as the lowest-penalty correct shape under the user's no-helper constraint. A single follow-up resolved ambiguous wording in that verdict: state-machine 40 reads the panel's public field after `draw()` returns, while `draw()` keeps its upstream `None` contract. The follow-up prompt and PASS verdict are preserved verbatim in `fable-ad-hoc-case-design-followup-prompt-20260715.md` and `fable-ad-hoc-case-design-followup-verdict-20260715.md`.

## 2026-07-15 Final Ad-hoc Implementation Verification

The final production diff against `upstream/master` `3a1c9e620` changes four files with exactly 22 added and 5 deleted non-blank lines, penalty `61`, and 27 changed non-blank lines total. It contains no unified settlement helper: four previously missing branches call `judge_character_status()` locally, and JOIN, DISCOVER, IGNORE, and INTERRUPT set the panel's public `skip_outer_settlement` result before any nested follow-up. MOVE-producing reactions leave the result false.

`pytest -q tests/test_discovery_settlement_ownership.py` passed all 28 pre-decision cases after the local test seam was updated to execute effect 1721 for DECEIVED and LEAVE as well as REFUSE and to read the public panel field after `draw()`. The four production files passed `compileall` and `git diff --check`; the OpenSpec change passed strict validation. A fresh-context reviewer returned PASS with no actionable finding and additionally probed the then-current no-route 1721 fallback: the NPC path settled `[reaction, wait]`, while the direct path settled the reaction and left `WAIT` pending. The later user-confirmed boundary below supersedes that NPC-path fallback result.

The final Fable prompt and PASS verdict are preserved verbatim in `fable-ad-hoc-case-final-review-prompt-20260715.md` and `fable-ad-hoc-case-final-review-verdict-20260715.md`. Fable accepted the local code candidate and the updated design/spec. Publication readiness remains blocked until task 2.3 replays the Tk route on the final ad-hoc tree and regenerates the after evidence; the accepted earlier A/B remains explanatory evidence but must not be presented as final-tree output.

## 2026-07-15 Fork Review Branch

After explicit user authorization, the final four-file candidate was rebuilt as a clean linked worktree from fetched `upstream/master` `3a1c9e620`, committed once as `356c1e86c` (`修正被发现反应的逐分支结算`), and pushed to `meower-z/erArk-fork` branch `codex/fix-discovery-settlement-ad-hoc`. The commit parent is exactly `3a1c9e620`; the remote branch SHA was read back and matches the local commit. The branch contains only the four production files and the `22/5/61` diff. Local focused tests were copied into the clean worktree for verification, passed 28/28, and were removed before commit. No PR or evidence publication occurred.

## 2026-07-15 User-confirmed WAIT Successor Boundary

After reviewing the difference between the ad-hoc candidate and the earlier behavior audit, the user confirmed the intended gameplay boundary: the outer successor settlement exists to make the discoverer move. If effect 1721 produces a real `MOVE`, the NPC outer loop must still settle that movement in the same round. If route finding instead falls back to `WAIT`, the outer loop must skip it because the discovery response has already given the character sufficient visible presence and there is no follow-up work to perform.

This is implemented narrowly in discovery state-machine 40 as `panel.skip_outer_settlement OR current behavior is WAIT`. The panel flag remains the operation-identity authority for JOIN, DISCOVER, IGNORE, and INTERRUPT, so nested player updates cannot re-enable an outer settlement. The behavior check applies only to the false-field leaving cases and does not alter ordinary state machines or the direct hidden-discovery caller. The PR draft must explain the public design as “settle a real movement successor, skip an idle no-route successor” and must not mention superseded implementation candidates.

The local review branch was first rebased onto fetched `upstream/master` `94d586840`, producing `aa2e8eca2`, and the one-line `WAIT` boundary was then committed as `4e226f4f5` (`发现后无移动时跳过等待结算`). The focused test seam was pointed at that exact worktree and extended with a no-route assertion: the NPC settlements are now `[refuse_join_group_sex]`, the successor remains `WAIT` with duration 1, and route finding still occurs once; the existing route-success assertion remains `[refuse_join_group_sex, move]`. All 29 focused cases pass. Compileall, `git diff --check`, and strict OpenSpec validation pass. The four-file non-blank diff remains `a=22`, `b=5`, penalty `61` because the source change replaces one non-blank line with one non-blank line. The fork branch has not been rewritten or pushed in this step.

The user then explicitly directed that Tk not be replayed again for this draft. The already approved clean static pair from `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/` remains the intended PR evidence. A visual agent had only prepared detached baseline/candidate worktrees when the direction arrived; it was interrupted before allocator acquisition or game launch. Allocator status showed all three slots free and no legacy game, and the task-owned disposable worktrees and parent directory were removed. No new Tk frame was captured.

While the fresh PR-artifact review was still running, the user separately authorized pushing the current code to the fork review branch. The remote ref was first read as `356c1e86c`; `git push --force-with-lease=refs/heads/codex/fix-discovery-settlement-ad-hoc:356c1e86c` then updated it to `4e226f4f5`. A second `ls-remote` read matched the exact local head. The worktree had been left detached by the interrupted visual preparation, so it was reattached to `codex/fix-discovery-settlement-ad-hoc`; local HEAD, the branch, and the fork tracking ref now all equal `4e226f4f5`, and the worktree is clean. No evidence was published and no PR was created or edited.

The first fresh PR-artifact review prompt is preserved in `fable-ad-hoc-pr-artifact-review-prompt-20260715.md`. Its exact Fable 5 high invocation ran for 600.1 seconds and exited 124 with no output. It produced neither a verdict nor findings and is not treated as acceptance. A narrower fresh-context retry keeps the same exact diff, draft, intended images, provenance caveat, and required ledgers while requesting a concise report.

The narrower retry prompt is preserved in `fable-ad-hoc-pr-artifact-review-retry-prompt-20260715.md`. It was still running without output when the user explicitly directed Codex to skip the review and open the PR. The process was terminated and produced no verdict. The review gate is recorded as user-waived, not passed.

The exact approved PNGs were published to the public fork's append-only `assets` branch in commit `e692de85089a29ec50e9015c8e2eba09e342cd1e`, under `pr-codex-fix-discovery-settlement-ad-hoc/before.png` and `after.png`. Their dimensions are both 1200x900 and their SHA-256 hashes remain `584baebf25b79af9ee7769fe4a0d7152a1875d321c5dd8c69d423655aa121bd5` and `1ea9a3603978b393fe976e8a4b3fce31c846fe1a6b24c8a9d507078dd469299e`. Both commit-pinned raw URLs return HTTP 200 with `Content-Type: image/png` and no attachment disposition. GitHub's Markdown renderer produced matching `src` and `href` URLs for each image.

After the user's explicit instruction to open the PR, upstream draft PR #218 was created at `https://github.com/Godofcong-1/erArk/pull/218`. Live API verification confirms draft state, base `master@94d586840484adf21fcf746dba0444551dd6a5a1`, head `meower-z:codex/fix-discovery-settlement-ad-hoc@4e226f4f587b82a87368a3d7976650593323a7b4`, and exactly four changed production files. The live title and body match the Fable-authored final draft with only the approved URL placeholders replaced by commit-pinned asset URLs. The rendered PR body contains both linked images and no local path, placeholder, private investigation term, or stale character name.

## 2026-07-15 Final PR #218 Real-Tk Replay

The session-closing replay ran the approved route against the exact live PR revisions: baseline `94d586840484adf21fcf746dba0444551dd6a5a1` and candidate `4e226f4f587b82a87368a3d7976650593323a7b4`. Both sides used real Tk (`web_draw = 0`), the same prepared save, evidence-only overlays, Python and NumPy seed `20260712`, `PYTHONHASHSEED=0`, one allocator-owned controller/display, and the same 38 physical inputs. The save and overlay hashes are fixed in `tk-final-pr218-rerun-contract-20260715.md`.

Both sides reached player H with Dobermann, discovered by Closure, selected option 1, and produced the same successful judgment (`1440 >= 200`). The new baseline omitted Closure's selected reaction and continued directly with Dobermann's H text. The new candidate showed Closure's explanation and departure once, stamina `-15` once, `5分钟过去了` once, and then continued with Dobermann's H text.

The new baseline crop and the PR before image compare at `AE=0`, `RMSE=0`; the new candidate crop and the PR after image also compare at `AE=0`, `RMSE=0`. Both new frames are therefore pixel-identical to the corresponding PR images. Their PNG byte hashes differ because of encoding or metadata, not pixels. The new rerun crop hashes are `4351804e971099d34f45a998cbf0378432954e443f4f70893b18057e314c45cb` for baseline and `a9f93a803a77d14673d7cfb380f78127437cae639b5f2babd6c8a2d48f0fc451` for candidate. The existing PR image hashes remain `584baebf25b79af9ee7769fe4a0d7152a1875d321c5dd8c69d423655aa121bd5` and `1ea9a3603978b393fe976e8a4b3fce31c846fe1a6b24c8a9d507078dd469299e`.

Four transient partial redraws occurred: baseline checkpoints 35b and 36b, and candidate checkpoints 20b and 23b. No input followed a partial frame; the controller first captured a settled no-input frame. Both saves retained their exact pre-run hashes after execution, no route-affecting traceback occurred, the task allocator owner was released, and all task PID/PGIDs exited. This route covers the main missing-reaction case shown in the PR; it does not exercise the no-route `WAIT` branch.

The verified append-only archive is `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/`. Its `CHECKSUMS.sha256` validates every retained file and has SHA-256 `db107e95e2b5a9fb28420134cfce090ab03fb091d027145280b43a4a5a31aef7`. Both archived final images were reopened after archival. This replay did not change, comment on, close, or otherwise mutate PR #218.

Fable 5 independently returned PASS on the final OpenSpec and archived evidence record; its exact prompt and verdict are preserved in `fable-session-closure-record-review-prompt-20260715.md` and `fable-session-closure-record-review-verdict-20260715.md`. Its only required finding was to complete the already-contracted disposable-root cleanup. Both `/tmp/erark-pr218-final-tk-rerun-20260715/` and `/tmp/erark-pr-images/discovery-settlement/pr218-final-rerun-20260715/` were then removed, their Git worktree registrations were pruned, the archive checksum was revalidated, and allocator status confirmed that the task owner was absent. The unrelated busy owner `root:t4-current-formal-pair-attempt7` was not touched.

A narrow Fable follow-up then returned PASS with no required finding. It independently confirmed both disposable roots and registrations are absent, the archive still validates, the 29-case matrix is internally and historically consistent, all three discovery worktrees are clean, the PR candidate remains at `4e226f4f5`, and the main-worktree versus main-history limitation is stated accurately. The exact follow-up prompt and verdict are preserved in `fable-session-closure-cleanup-followup-prompt-20260715.md` and `fable-session-closure-cleanup-followup-verdict-20260715.md`.

## 2026-07-15 Maintainer-required `SPECIAL_FLAG` Candidate

Maintainer feedback on PR #218 requires a new field in `SPECIAL_FLAG`, rather than using a return value from `constant.handle_state_machine_data` for this special case. The isolated candidate `codex/fix-discovery-settlement-special-flag` starts from current `upstream/master` `58587deac62149d80c82b5a3c98ad29f51cfe2b4`.

The candidate keeps the upstream `None` return contract. Seven explicit discoverer-response branches synchronously call `judge_character_status()` and set a panel-local `discoverer_reaction_settled` flag. State machine 40 copies that value to `sp_flag.see_h_reaction_settled` only after `draw()` returns, so a nested player update cannot consume it early. The NPC idle path skips one flagged non-movement successor, still settles a flagged `MOVE`, and always clears the flag. The direct hidden-discovery caller does not write the flag.

The local red-capable source-loading matrix reports baseline `11 failed, 2 passed` and candidate `13 passed`. The four production files pass `compileall` and `git diff --check`. Non-blank production diff count is `a=21`, `b=1`, seven change groups, no repeated deletion credit, for penalty `29`. Fable 5 independently returned PASS with no required production finding; the retained prompt and verdict are `fable-maintainer-special-flag-final-review-prompt-20260715.md` and `fable-maintainer-special-flag-final-review-verdict-20260715.md`.

## 2026-07-15 `SPECIAL_FLAG` Real-Tk Before/After Evidence

The fresh evidence contract is `tk-special-flag-before-after-contract-20260715.md`. A dedicated visual runner replayed baseline `58587deac62149d80c82b5a3c98ad29f51cfe2b4` and candidate `c75b3b1737f5ab958b520e568d8aead59cd1d413` sequentially on the same allocator-owned Tk display (`:45`, slot 1, `2100x1100x24` Xvfb, 1200x900 game window). Both used the same two unchanged prepared save files, `PYTHONHASHSEED=0`, and Python/NumPy seed `20260712`; each replayed the same 38 physical inputs.

At the selected Closure response, the baseline visibly omitted Closure's reaction and continued Dobermann's H text. The candidate visibly showed Closure accepting the explanation and leaving, exactly one `气力 -15`, exactly one `5分钟过去了`, then Dobermann's H text. Candidate had no partial redraw; baseline had one step-20 transient redraw, followed by an inspected no-input stable frame that was byte-identical to the preceding raw frame.

The append-only archive is `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-special-flag-c75b3b173-20260715/`. Its `CHECKSUMS.sha256` validates from the archive root and itself hashes to `ccbc1e1d449e8ed03e209341a0e81866046ee997cd8edfa239ede4b71077f28d`. Final baseline/candidate frames are both 1200x900; their expected visible difference is `AE=184656`, while checkpoints 34–37 are `AE=0`. The new baseline and candidate final images each compare pixel-identically (`AE=0`) to their respective existing PR #218 screenshot. The visual runner reopened archived final images before cleanup; the two task-owned `/tmp` roots were removed and allocator status records all slots free. This evidence run did not mutate production source, Git refs, OpenSpec, GitHub, or PR #218.

## 2026-07-15 PR #218 Local Handoff State

At the user's instruction, stop all further PR activity. PR #218 remains open and ready for review; its fork head `meower-z:codex/fix-discovery-settlement-ad-hoc` is `c75b3b1737f5ab958b520e568d8aead59cd1d413`, based on `upstream/master` `58587deac62149d80c82b5a3c98ad29f51cfe2b4`.

The outward-state timeline is recorded rather than inferred. The user explicitly instructed `这次就跳过审查直接开 PR 吧`; GitHub's timeline records `ready_for_review` at `2026-07-15T03:20:19Z`. The user later explicitly instructed `把代码提交到 fork repo 的对应分支，供我审查。同时展示出 PR draft。`; the remote PR branch was then updated with lease from `4e226f4f587b82a87368a3d7976650593323a7b4` to `c75b3b1737f5ab958b520e568d8aead59cd1d413`. GitHub also shows a public reply by `meower-z` at `2026-07-15T13:27:27Z` saying the maintainer-requested special flag implementation is ready for review. This handoff records that reply as an observed external fact; it does not attribute it to a local tool action or invent a separate user authorization absent from this record.

The online title equals the v2 draft title. The online body does **not** equal the v2 draft: it remains the superseded ad-hoc prose and therefore does not describe `SPECIAL_FLAG` or the seven explicit response branches. The v2 draft is local-only because the user instructed that the PR needs no further action; do not publish or edit it unless the user explicitly reauthorizes a PR body change.

The approved local PR draft is the Fable 5 high-effort output and complete invocation/stdout record in `fable-maintainer-special-flag-pr-draft-final-v2-record-20260715.md`. The retained fresh-context artifact review is `pr-artifact-special-flag-v2-final-review-20260715.md`; it returned `PASS` / `publication-ready`: the public before/after PNGs are both 1200x900 and pixel-identical to this candidate's archived Tk final frames, while the draft does not expose local tests, logs, worktrees, or private investigation material.

The candidate's committed production code is retained by the remote PR ref. The local `codex/fix-discovery-settlement-special-flag` worktree and branch are now disposable duplicate transport state and may be removed only after this OpenSpec record is committed to local `main`. The existing local `codex/fix-discovery-settlement-ad-hoc` worktree remains untouched because it is the local checkout of the still-open PR branch.
