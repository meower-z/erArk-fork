# PR Draft

Status: submitted as PR #215 (OPEN, unmerged) — https://github.com/Godofcong-1/erArk/pull/215. The body below is the pre-submission fable-5 draft; in the live PR the two image placeholders were replaced with commit-pinned public URLs.

## Title

修复：NPC 异地发生的多重绝顶被延迟到玩家在场时才显示和结算

## Body

## 问题

实际游玩中，NPC 在玩家不在场时发生的双重至十一重绝顶不会当场结算，而是残留下来，等这名 NPC 之后来到玩家附近并做完当前行为时才突然显示和结算。于是玩家在等待、移动后的结算等本身与绝顶无关的操作之后，会毫无来由地看到一条此前异地发生的多重绝顶提示。原因是 `data/csv/Behavior_Effect.csv` 中 `plural_orgasm_2` 至 `plural_orgasm_11` 十个多重绝顶结算效果缺少 997 标记：玩家不在场时它们不会进入必须结算列表，旧行为一直留在二段行为队列中，直到玩家在场时才被处理。

## 修复

为上述十行各追加 997 标记。在这十个多重绝顶行为现有的远程二段结算路径中，997 使该效果进入必须结算列表而不进入必须显示列表：玩家不在场时数值当场结算完毕、队列即时清除，不向玩家显示异地口上，也不再残留到玩家之后的结算中。NPC 与玩家同处一地时的原有显示逻辑保持不变。

## 验证

以一条代表性路线做修复前后对比：同一存档、同一随机种子、同一玩家操作，在咖啡馆执行等待五分钟。

![修复前](BEFORE_URL)

![修复后](AFTER_URL)

## Image alt/captions

- BEFORE_URL: 修复前：在咖啡馆执行等待五分钟后，结算文本底部出现延迟的黄色“小满双重绝顶”。
- AFTER_URL: 修复后：同一路线的对应时点回到咖啡馆界面，不再出现该延迟的多重绝顶文本。
