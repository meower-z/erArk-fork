/investigate-game-bug

你刚为 erArk 候选 `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc` 的 base `94d586840484adf21fcf746dba0444551dd6a5a1`、head `4e226f4f587b82a87368a3d7976650593323a7b4` 写了 PR draft，原稿逐字保存在 `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/fable-ad-hoc-pr-draft-wait-boundary-output-20260715.md`。请重新读取精确 diff 和原稿，只修订 PR 标题与正文，不修改文件。

必须修正一个事实错误：`JOIN_GROUP_SEX` 原本已经在分支内结算，不能列为“缺少结算的分支”。这次局部补结算的四个分支准确是：`SEE_H_BUT_DECEIVED`、`SEE_H_BUT_IGNORE`、`SEE_H_AND_LEAVE`、初次转群交的 `DISCOVER_OTHER_SEX_AND_JOIN`。面板已完成标记覆盖的是另一组语义：JOIN、DISCOVER、IGNORE、INTERRUPT 已在面板内完成，因此 NPC 外层不应重放。REFUSE、DECEIVED、LEAVE 则根据反应后的实际状态处理：真正 `MOVE` 时本轮继续结算移动，无路回退为 `WAIT` 时跳过等待。

同时把正文压短一些，面向读代码的 maintainer 但不要堆调用链和标识符。保留“问题 / 原因 / 修复 / 验证”结构、两张静态 PNG 占位符和准确图注。MOVE/WAIT 的小设计必须用一句或两句清楚说明。不要删除两个 caller 的根因，也不要删除反应先于结束 H/转群交的顺序保证。

继续严格禁止出现或暗示：任何旧实现、统一函数、内部探索历史、被放弃的方案、私有分支比较、OpenSpec、worktree、本地测试、line count、penalty、Fable、Codex、本地路径。不要扩大两张图的证据范围。

只输出修订后的 PR 标题和正文，不要解释修改过程。
