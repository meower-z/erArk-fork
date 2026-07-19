/investigate-game-bug

这是对 `fable-ad-hoc-case-design-verdict-20260715.md` 的唯一一次事实性澄清，只读，不得修改文件。请读取原 prompt、原 verdict、候选 diff 和 OpenSpec。

原 verdict 同时给出两组互相不兼容的结论：

1. 最低形状是预计 `a=22,b=5,penalty=61`；这对应原 prompt 明确描述的接口：panel 保留公开字段 `skip_outer_settlement`，`draw()` 保持上游 `None` 合同，状态机 40 执行 `now_panel.draw()` 后 `return now_panel.skip_outer_settlement`。按文件预算：panel `12/0`、state 40 `3/1`、find `4/2`、scheduler `3/2`，合计 `22/5`。
2. verdict 又写“四跳返回链(面板字段→draw 返回→状态机 40→find→scheduler)”和“经返回值读一次”。若 `draw()` 改为返回 bool，则还必须修改 `draw` 签名/docstring/循环出口，并让 state 40 `return now_panel.draw()`；按正常格式预算变为 panel `15/3`、state 40 `3/2`、find `4/2`、scheduler `3/2`，合计约 `25/9,penalty=66`。

原 prompt 的拟议严格等价方案采用第 1 种：状态机 40 在 `draw()` 返回后读取 panel 的公开字段。这个字段不是私有属性，也不是跨操作全局状态；它是单次面板对象公开给唯一 NPC 状态机 caller 的结果。直接 caller 只调用 `draw()` 并忽略该字段。

请裁定唯一最终接口：

- 若第 1 种正确，请明确确认状态机 40 读取 `now_panel.skip_outer_settlement` 是可接受的最小公开结果协议，`draw()` 保持 `None`，并确认 `22/5/61`。
- 若必须由 `draw()` 返回 bool，请明确否决第 1 种并把最低预算修正为约 `25/9/66`，说明为何公开 panel 字段不能由创建该 panel 的状态机读取。

只回答该矛盾；给出 PASS/FAIL、最终代码形状和修正后的 a/b/penalty。若没有新的游戏语义选择，不要求用户输入。
