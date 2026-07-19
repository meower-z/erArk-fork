/investigate-game-bug

请只对 `/home/ubuntu/games/erArk/openspec/changes/fix-time-stop-release-attribution/pr-draft.md` 做一次最小 PR 文案修订。不要改其他句子，不要修改文件，只输出修订后的完整 TITLE 与 BODY。

Fresh-context artifact reviewer 的唯一 finding 是：验证段第一段第二句“修复前后直到结果页为止的所有画面完全一致，只有结果页不同。”依赖不会公开的本地逐帧清单；PR 公开材料只有两张最终结果图，因此这句话在 PR 内不可自证。

要求：删除且仅删除这一个完整句子。保留前一句“在普通 Tk 模式中走同一条玩家路线：时停中对林进行 H，随后解除时停。”，保留其余标题、问题、修复、两张图说明和字面 URL 占位符不变。不要补写替代说法。

输出格式必须只有：

```text
TITLE:
<一行标题>

BODY:
<完整 Markdown 正文>
```
