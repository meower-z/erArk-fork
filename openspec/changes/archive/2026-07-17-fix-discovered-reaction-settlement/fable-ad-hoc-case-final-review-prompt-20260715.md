/investigate-game-bug

只读最终接受审查，不得修改任何文件。候选工作树 `/home/ubuntu/games/erArk-pr-discovery-settlement-redo`，基线 `upstream/master=3a1c9e620`；中央 OpenSpec `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/`。请实际读取工作树相对基线的未提交最终生产 diff、`tests/test_discovery_settlement_ownership.py`、两条生产 caller、状态机 40/96、Behavior_Effect、最新 proposal/design/spec/tasks/implementation-notes，以及本次 prompt/verdict 记录。

用户确认的范围：多个相邻发现者反应 bug 一起修，但禁止统一 owner/helper function；逐个 case 检查哪里漏结算或重复结算，只修坏分支，保持逻辑等价和正常格式。

已核验最终状态：

- 最终生产 diff 仅 4 文件，raw 和非空行均为 `a=22,b=5,penalty=61`，共 27 个变更非空行；无 `_settle_discoverer_reaction`。
- panel 恢复上游 `draw() -> None` 及各分支赋值/duration；只给 DECEIVED、IGNORE、LEAVE、初次 DISCOVER 补 `judge_character_status()`；保留 JOIN、REFUSE、INTERRUPT 原结算。
- panel 实例公开字段 `skip_outer_settlement=False` 只在 JOIN、DISCOVER、IGNORE、INTERRUPT 结算后逐 case 设 True，且 DISCOVER/INTERRUPT 均在 nested follow-up 前设置。
- 状态机 40 在 `draw()` 后读取字段并返回；`find_character_target()` 透传；scheduler 仅在 falsy 时执行原外层 `judge_character_status()`。DECEIVED/LEAVE/REFUSE 因字段保持 False，NPC 同轮处理后继 MOVE/WAIT，direct caller 只提交反应并保留后继。
- 成功转隐奸/露出不设字段；普通状态机 96 返回 None，普通 JOIN 不被跳过。
- `pytest -q tests/test_discovery_settlement_ownership.py` 为 28 passed；四个生产文件 compileall 通过；`git diff --check` 通过；OpenSpec strict validation 通过。
- fresh-context reviewer PASS，无 actionable finding；额外探测 effect 1721 无路径 fallback 为 NPC `[reaction, wait]`、direct 只结算 reaction 并留下 WAIT。
- 本轮没有在最终 dirty tree 重跑真实 Tk；用户已接受的 A/B 来自前一个语义等价 helper 候选，主可见路径的反应文本顺序保持一致。没有 commit、push 或 PR outward action。

请判断：

1. 最终实现是否严格满足逐-case、exactly-once、MOVE/direct边界和嵌套顺序，无隐藏 owner/helper 或 scope creep。
2. `22/5/61` 是否是禁止统一 helper 约束下最低可接受正常格式，代码是否适合 maintainer 肉眼审查。
3. 最新 OpenSpec 是否准确记录最终接口、历史 supersession、WAIT边角与验证状态，可以接受。
4. 是否存在必须在提交前修复的 production correctness、公开游戏语义或文档问题；最终 Tk 未重跑是否阻止本地代码候选完成，还是只阻止 publication-ready 声明。

输出明确 PASS/FAIL、actionable findings、文档接受结论和 residual risk。没有真实 blocker 时不要要求用户输入。
