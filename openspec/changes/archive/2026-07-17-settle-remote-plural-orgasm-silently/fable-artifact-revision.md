# Fable Artifact Revision

The following is the verbatim output from the artifact-revision `claude-fable-5` call whose prompt is preserved in `fable-artifact-revision-prompt.md`.

```text
以下为定稿，可直接替换原 PR 文案。两处 `REVISE` 均已处理：删除了 12:29 / 异地来源 / “实际发生于另一场景”的叙事，删除了凯尔希在场对照的验证声明；结构与图片占位符保持不变。

---

**标题：**

修复：玩家不在场时多重绝顶结算被延迟显示

**正文：**

## 问题

`data/csv/Behavior_Effect.csv` 中 `plural_orgasm_2` 至 `plural_orgasm_11` 十个多重绝顶结算效果缺少 997 标记，玩家不在场时不会被即时结算，而是残留到玩家后续的结算输出中。实际游玩中表现为：玩家在咖啡馆执行等待五分钟后，结算文本底部出现一条延迟的黄色“小满双重绝顶”。

## 修复

为上述十行各追加 997 标记。997 表示该效果在玩家不在场时也必须结算、且不产生显示文本；补上标记后，多重绝顶在发生当刻即被结算完毕，不再残留到玩家之后的结算中。玩家在场时的显示逻辑不在本次修改范围内，保持原样。

## 验证

同一存档、同一随机种子、同一玩家路线的修复前后对比：

![修复前](BEFORE_URL)

![修复后](AFTER_URL)

**BEFORE caption：**

修复前：在咖啡馆执行等待五分钟后，结算文本底部出现延迟的黄色“小满双重绝顶”。

**AFTER caption：**

修复后：同一路线的对应时点回到咖啡馆界面，不再出现该延迟的多重绝顶文本。
```
