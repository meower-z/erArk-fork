/investigate-game-bug

请为一个尚未创建、尚未推送的 erArk 上游 PR 起草中文标题和 Markdown 正文。只负责 PR-facing prose；不要修改文件、发布图片、推送分支或创建 PR。请先亲自打开精确生产 diff 和两张完整分辨率证据图，并用 `gh pr view` 阅读项目已接受的 #210、#211、#206 当前标题与正文，只模仿它们的高度和简洁程度，不复用措辞。

候选工作树：`/home/ubuntu/games/erArk-pr-time-stop-release-attribution-current`
基线：`upstream/master` 的 `72e28051ebaaabb069d06059b4633fda90b0b621`
唯一生产 diff：该工作树的 `Script/Settle/default.py`

PR-facing 玩家证据只使用以下两张图：

- 修复前：`/home/ubuntu/games/archive/erArk-upstream-pr-evidence/2026-07-15-time-stop-release-attribution-attempt11/baseline/frames/b31-final.png`
- 修复后：`/home/ubuntu/games/archive/erArk-upstream-pr-evidence/2026-07-15-time-stop-release-attribution-attempt11/candidate/frames/c31-final.png`

人类可见事实：同一正常 Tk 玩家路线中，结果前 31 对画面完全相同。修复前结果页把 `无意识绝顶经验+1` 和 `饮精绝顶经验+1` 记在 Doctor 名下，林只有 `无意识绝顶经验+2`；修复后 Doctor 结算块消失，林得到 `无意识绝顶经验+3` 和 `饮精绝顶经验+1`，其他可见数值不变，总量无丢失或重复。

确认原因与修复边界：时间停止解除时，effect 527 正在释放某名 NPC 的延后高潮。旧代码修改该 NPC 的实际状态，却把同步结算记录传入玩家的根结算对象，所以显示归属变成 Doctor。候选只在存在非零延后计数时，为当前被释放 NPC 创建或复用 `TargetChange` 并把它传给原有 `orgasm_settle`；零计数的 no-op 调用、解除标记、计数清理、高潮公式、次数和后续通用二阶段流程均未改变。这是归属 bug 修复，不是玩法语义选择。

写作约束：

- 假设评审玩过 erArk，但没见过这个 bug；直接点明具体功能和可见错误。
- 按“问题、修复、验证”的顺序，使用游戏已有术语；不要介绍整个系统。
- 只写理解所提交生产 diff 所必需的原因与边界。
- 不得提候选评分、文件名、函数调查过程、无效 attempt、种子、存档、未发布 mod、本地测试路径或 OpenSpec。
- 不得声称改动了通用二阶段结算。
- 验证区放一组修复前/修复后图片，URL 分别写成字面占位符 `{{BEFORE_IMAGE_URL}}` 与 `{{AFTER_IMAGE_URL}}`；请写清楚、不过度解释的中文 alt/caption。
- 不要虚构尚未执行的公开动作、CI 或上游审核。

输出格式必须只有：

```text
TITLE:
<一行标题>

BODY:
<完整 Markdown 正文>
```
