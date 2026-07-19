/investigate-game-bug
/review-erark-pr-artifacts

请对你刚才为 PR #212 写的正文做一次最小、定点修订，并重新输出完整 TITLE/BODY markers。

唯一必须修正的问题在验证段最后一句：你写了 `心理 +168` 与 `心理经验 +3` “是修复前后都存在的正常副作用”。这会被理解为 buggy baseline 也实际执行或显示了这个副作用，但 baseline 因为负苦痛被提前改道到 state 23 并 return，实际没有进入 state 17 的 `extra_feel_settle`。准确含义是：这套副作用机制原本就属于普通 state 17 路径；修复后负变化重新落回该路径，所以候选画面显示了它。这证明原有普通结算被保留，而不是转换错误残留。

请只改正这处因果表述，保留其余标题、结构、数据、图片 placeholders 和文字不变。不得自行新增测试、入口或范围。只输出：

```text
TITLE_BEGIN
<title>
TITLE_END
BODY_BEGIN
<body markdown>
BODY_END
```
