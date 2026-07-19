# Fable ruling: attempt 4 setup-page viewport variance

Invocation: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Prompt: [fable-formal-attempt4-setup-viewport-prompt.md](fable-formal-attempt4-setup-viewport-prompt.md).

Exact response follows.

```text
**裁定:CONTINUE WITHOUT SCROLL。** 这是旧协议把视口像素误当语义,不是内容缺失,也不是输入污染。

十帧 byte-identical、AE0、首帧即完整可读、人物/数值/文本与 run1 一致、无异常菜单——这就是稳定语义页的定义。run1 与 run2 的 SHA 差异完全由文本 widget 自动滚动的停靠位置解释,而滚动停靠位置不是游戏语义,是 Tk 渲染的非确定性表面。用整页 SHA 做门,等于把"下一个标题是否恰好露出在可视区"当成了状态断言,这是错误的门。

逐条答复:

1. **CONTINUE WITHOUT SCROLL,明确禁止为追 run1 SHA 而滚动。** 补滚动本身就是一次未预注册的输入,会真正污染这次 run。从当前 wait 页按一次正常 Return 进入 numeric settlement,之后由 sample1 的硬状态门(Lin counts `{0:1,21:2}`、shoot_position_body `2`、经验、target/H/time-stop、全部 trigger NPC)裁定 setup 是否正确。状态门比"上一屏是否看见下一块标题"直接且严格得多。

2. **不属于。** "必须捕获的承载被测结算文本的 wait 页"指的是 T4 被测契约——切换惊蛰后点 `[4115]` 的解除时停归属输出页。当前页是普通口交的 setup 输出页,只需满足"在预注册语义链上"即可,而它满足。顺带说明:即便按更严的标准,本页也已被从首帧起完整可读地捕获,例外条款无论如何未被触发。

3. **正式 prereg 对 setup 输出页只要求语义锚点:** 人物(林)、动作词(`射出`)、射精位置(口腔)、数值(20ml)、以及"醒来第一发+"标记。计数、shoot_position_body、经验等内部状态留给 sample1 state gate,不要求在像素上可见。**禁止把整页 SHA 或 scroll offset 写成通过条件**;SHA 只允许作为 provenance/去重元数据。同理禁止"必须与另一 run 的帧逐像素一致"。

4. **是,必须。** 解除时停后的归属输出页是本任务的被测契约,契约本身是玩家可见文本的归属与分组。它必须逐页可读捕获,并按 baseline/candidate 的预期文本与分组人工审查;sample3 只能证明内部状态,不能证明输出页把结算归到了正确的人和正确的块。二者都要,缺一即整轮重启——这条例外仅适用于该页。

5. **批准原计划不变:** numeric page → H menu → sample1 → 两次 trough → 点惊蛰 → bottom menu → sample2 → 一次 active `[4115]`;任何硬状态不符立即 STOP 并回报,不得为到达 endpoint 而继续。

6. **不需要玩家介入。** 此裁定不改玩法语义、不外发,且 run2 维持永久 INVALID / DIAGNOSTIC ONLY——其任何产物不得进入 PASS 或 PR 证据。

**给正式 prereg 的修订指令:** 把所有"稳定页一致性"门从整页 SHA 改写为"帧间 byte-identical 达到稳定 + 语义锚点可读"两段式;跨 run 比较只比锚点,不比像素。
```
