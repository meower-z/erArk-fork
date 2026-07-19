/investigate-game-bug

你刚为 erArk PR #212 生成了标题、正文和 review reply。现在对最终 Tk 图片做人工复核后发现一处证据标签需要逐字纠正：Group A candidate 截图里实际显示的是 `心理 +3656`，不是 `心理快感 +3656`。这是 state 23 的游戏内显示名；概念仍是心理快感，但引用截图数值时必须使用屏幕上的精确文字。

请只输出这个单一纠正的裁决，格式严格如下：

VERDICT_BEGIN
PASS_CORRECTION 或 REJECT_CORRECTION
VERDICT_END
REPLACEMENT_BEGIN
应替换进 PR 验证段的完整一句话
REPLACEMENT_END

当前句子：
“修复后，相同操作显示 `心理快感 +3656`、`苦痛 -31028 (lv7→4)`——负向变化留在苦痛，正向部分正常转换：”

除把 code span `心理快感 +3656` 改成截图精确文字 `心理 +3656` 外，不得改动句子其他任何文字，不得改标题、正文其他段落或 review reply。
