/investigate-game-bug

只读设计审查，不得修改任何文件。候选工作树是 `/home/ubuntu/games/erArk-pr-discovery-settlement-redo`，基线 `upstream/master=3a1c9e620`，当前候选 HEAD `ffd1d1ee8` 的树与已审候选 `884b2fa30` 相同。中央 OpenSpec 位于 `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/`。

用户已经明确修复范围仍包括相邻的发现者反应 bug，但要求不要通过统一的 owner/helper function 合并这些 case；应逐个检查现有分支在哪里漏结算或重复结算，只修坏的分支，并保持逻辑等价、项目正常格式和人类可审查性。

已核验生产事实：

1. 两个生产 caller 是 NPC 状态机 40 -> `find_character_target()` -> `character_behavior()` 的外层结算，以及 `hidden_sex_panel.settle_discovered()` 的直接调用；直接调用没有该 NPC 外层结算。
2. 上游逐 case 状态：
   - `SEE_H_BUT_DECEIVED`、`SEE_H_BUT_IGNORE`、`SEE_H_AND_LEAVE` 与初次转群交的 `DISCOVER_OTHER_SEX_AND_JOIN` 没有面板内结算，因此 direct caller 会丢反应；初次转群交还可能被嵌套玩家更新清掉。
   - 已在群交中接受的 `JOIN_GROUP_SEX`、拒绝的 `REFUSE_JOIN_GROUP_SEX`、中断的 `SEE_H_AND_INTERRUPT` 已在面板内结算；NPC caller 可能再次外层结算。其中 `REFUSE_JOIN_GROUP_SEX` 结算后转为 `MOVE`，外层实际应继续结算这个后继移动。
   - 成功转隐奸或露出故意没有明确发现者反应，NPC caller 应保持普通外层空闲结算。
3. 生产效果表中只有 `REFUSE_JOIN_GROUP_SEX`、`SEE_H_BUT_DECEIVED`、`SEE_H_AND_LEAVE` 经效果 1721 把当前行为变为 `MOVE`；`JOIN_GROUP_SEX`、`DISCOVER_OTHER_SEX_AND_JOIN`、`SEE_H_BUT_IGNORE`、`SEE_H_AND_INTERRUPT` 不会转为 `MOVE`。
4. 普通状态机 96 也会设置 `JOIN_GROUP_SEX`，但没有面板内结算，因此不能在通用 scheduler 里只按 behavior id 跳过。
5. 当前统一 helper 候选相对基线有 4 个生产文件、非空行 `a=30,b=30,3a-b=60`，总计 60 个变更非空行；28 个聚焦测试通过。

拟议的严格等价逐-case方案：

- 删除 `_settle_discoverer_reaction()`，恢复各回调原有的行为赋值和 duration 写法。
- 只在四个原来缺少结算的分支加入 `judge_character_status()`：支开成功、露出模式中的忽略、露出模式中的离开、初次转群交加入；保留原来已经存在的 JOIN/REFUSE/INTERRUPT 结算。
- 面板实例只保留一个公开结果字段 `skip_outer_settlement=False`，不封装统一结算函数。仅在面板已结算而当前 NPC 外层不应再处理的四类非 MOVE 反应中逐 case 设为 True：JOIN、DISCOVER、IGNORE、INTERRUPT。三个会产生 MOVE 的反应保持 False，让外层处理后继 MOVE。
- 状态机 40 在 `draw()` 返回后返回该字段；`find_character_target()` 原样透传；scheduler 改为仅在结果为 falsy 时执行原 `judge_character_status()`。直接 caller 忽略结果，但每个明确反应已经在自己的分支同步结算。
- 成功转隐奸/露出不设字段，NPC caller 仍普通结算；普通状态机 96 返回 None，JOIN 仍由正常外层结算。
- 这个字段在 DISCOVER/INTERRUPT 的嵌套玩家更新之前设为 True，所以即使嵌套更新把行为清成 `SHARE_BLANKLY`，外层仍跳过，和当前已审候选保持一致。
- 按项目正常多行格式的静态预算是 `a=22,b=5,3a-b=61`，总计 27 个变更非空行。计分只比当前 helper 候选差 1，但肉眼审查面从 60 行降到 27 行。

另一个更少一行的方案不保存字段，而由状态机 40 在面板返回后检查当前 behavior 是否属于 JOIN/DISCOVER/IGNORE/INTERRUPT；静态预算约 `a=21,b=5,3a-b=58`、26 个变更非空行。但 DISCOVER/INTERRUPT 的嵌套更新若已清成 `SHARE_BLANKLY`，它会重新执行一次普通空闲结算，和当前候选的外层跳过语义不同。通用 scheduler 直接按 behavior id 判断则会误伤普通状态机 96 的 JOIN，已排除。

请实际读取当前 diff、上游逐 case 代码、两条 caller、状态机 96、效果表、测试和 OpenSpec。判断：

1. 严格等价逐-case方案是否正确、范围是否符合用户要求；公开结果字段是否是最小必要的 operation-local 信息，还是仍属于不合适的隐藏协议。
2. 无字段的 post-panel behavior 推断能否算满足已确认合同；若不能，请指出具体语义差异。
3. 在禁止统一 helper、禁止格式刷分、必须覆盖相邻 case 的约束下，是否存在更低 `3a-b` 且更易审的正确方案。
4. 该方案是否改变任何尚未确认的公开游戏语义。

输出明确 PASS 或 FAIL、最低可接受代码形状、预计 a/b/penalty、actionable findings 与 residual risk。只有确实需要用户决定新的游戏语义时才声明需要用户输入。
