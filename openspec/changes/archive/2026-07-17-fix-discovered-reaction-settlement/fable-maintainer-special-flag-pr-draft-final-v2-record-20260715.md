# Fable 5 final PR draft v2 record — maintainer `SPECIAL_FLAG` candidate

Verified invocation:

```text
claude -p --model claude-fable-5 --effort high --no-session-persistence "$PROMPT"
```

Exit status: `0`; elapsed time: `79.9s`.

## Prompt

```text
/investigate-game-bug

只读、外科式最终 PR 文案修订：不得修改文件、Git、GitHub 或 PR。请实际读取：
- 当前最终草稿 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/fable-maintainer-special-flag-pr-draft-final-20260715.md
- 候选 diff /home/ubuntu/games/erArk-pr-discovery-settlement-special-flag（base 58587deac62149d80c82b5a3c98ad29f51cfe2b4，head c75b3b1737f5ab958b520e568d8aead59cd1d413）。

fresh artifact reviewer 的两个 P1 finding：当前草稿把“所有选择/面板各选项分支”误写为都有发现者反应，但转隐奸、初次转露出等成功模式转换故意不产生发现者反应。只修改下列两处，让它们准确限定为“会设置发现者反应行为的选择分支”：
1. 问题第一段中“玩家做出选择后，发现者本应恰好表现一次对应的反应”这一断言；
2. 原因第一句中“面板各选项分支各自设置发现者的反应行为”。

只做这两处范围限定；保持标题、所有其他文字、四点修复、七项枚举、图片 caption 和 URL 的原有措辞与顺序。不要添加非目标句、说明或文件修改。输出仅：
TITLE:
<标题>

BODY:
<完整 Markdown 正文>
```

## Exact stdout

```text
diff 已核对：面板中「转隐奸」「初次转露出」等成功分支确实不设置发现者反应行为，两处断言需按 finding 限定范围。以下为仅含两处外科修订的最终文案，未做任何文件修改。

TITLE:
修复「H中被发现」面板中发现者反应漏结算与重复结算的问题

BODY:
## 问题

玩家 H 中被其他角色发现时会弹出「H中被发现」选择面板。面板有两个入口：NPC 在自己的回合目击玩家 H，以及隐奸流程的发现结算。玩家做出选择后，在会给发现者设置反应行为的选择分支里，发现者本应恰好表现一次对应的反应（反应文本与数值效果），但两个入口下都不能保证：

- 部分选项分支只给发现者设置了反应行为，从未结算它。例如从隐奸入口进入面板，选择「用花言巧语支开对方」且判定通过后，发现者的被支开反应完全不出现，画面直接回到 H 文本。
- 另一部分分支在面板内已经结算过反应，但从 NPC 回合入口进入时，外层循环在面板关闭后还会无条件再结算一次，同一反应可能重复结算。

## 原因

面板中会给发现者设置反应行为的选项分支各自设置该行为，但是否随即结算并不一致：「结束H」「加入群交」「拒绝加入」等分支会就地结算，「支开成功」「露出时无视」「露出时接受并离开」「初次发现转群交」则不会。同时，NPC 回合的外层循环在目击处理返回后总是再补一次结算，面板没有渠道告知外层「这次反应已经结算过」。两种不一致在两个入口上分别叠加，就产生了漏结算和重复结算。

## 修复

1. 统一面板内的结算时机：每个明确给出发现者反应的选项分支——支开成功（`SEE_H_BUT_DECEIVED`）、露出时对方无视（`SEE_H_BUT_IGNORE`）、露出时对方接受并离开（`SEE_H_AND_LEAVE`）、直接加入群交（`JOIN_GROUP_SEX`）、初次发现转为群交（`DISCOVER_OTHER_SEX_AND_JOIN`）、拒绝加入群交（`REFUSE_JOIN_GROUP_SEX`）、打断当前H（`SEE_H_AND_INTERRUPT`）——都在面板内立即结算一次该反应，并在面板上记录「发现者反应已结算」。
2. NPC 回合入口的目击H状态机在面板绘制返回后，把这一完成情况写入发现者角色的 `SPECIAL_FLAG`（新增字段 `see_h_reaction_settled`）。
3. NPC 回合外层随后按发现者反应后的实际行为收尾：带该标记且停在原地等待（`WAIT`）时，跳过外层这一次补结算——反应的全部可见表现已在面板内给出，再补一轮只会重复；反应使其真正进入移动（`MOVE`）时，外层照常结算这次移动。无论哪种情况，外层处理后随即清除该标记，不影响此后回合的正常结算。
4. 隐奸流程直接调用面板的入口不写该标记：该入口没有外层补结算，反应在面板内结算一次即已完整。

## 验证

与杜宾 H 中被可露希尔发现，选择「用花言巧语支开对方」且判定通过：

| 修复前 | 修复后 |
| --- | --- |
| [![修复前：判定通过后可露希尔没有任何反应文本，杜宾的H文本直接继续](https://raw.githubusercontent.com/meower-z/erArk-fork/e692de85089a29ec50e9015c8e2eba09e342cd1e/pr-codex-fix-discovery-settlement-ad-hoc/before.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/e692de85089a29ec50e9015c8e2eba09e342cd1e/pr-codex-fix-discovery-settlement-ad-hoc/before.png) | [![修复后：可露希尔的被支开反应恰好出现一次，随后杜宾的H文本正常继续](https://raw.githubusercontent.com/meower-z/erArk-fork/e692de85089a29ec50e9015c8e2eba09e342cd1e/pr-codex-fix-discovery-settlement-ad-hoc/after.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/e692de85089a29ec50e9015c8e2eba09e342cd1e/pr-codex-fix-discovery-settlement-ad-hoc/after.png) |

两张截图对比的是这一条漏反应案例；其余分支的就地结算与跳过重复结算属于同一处理路径上的对应修正。
```
