/investigate-game-bug

你是这个 erArk 997-only 候选 PR 的最终文案把关者。不要修改代码，不要做复现。你已接受生产 diff、根因、CSV-only 提交边界和 A/B 因果；现在只处理 fresh-context PR artifact audit 的两处精确 `REVISE`，并返回可直接替换的最终中文 PR 标题、正文与两张主图 caption。

固定提交和公开主证据：

- 提交仅为 `data/csv/Behavior_Effect.csv` 中 `plural_orgasm_2` 至 `plural_orgasm_11` 十行各追加 `997`；没有 Python、测试、trace 或图片进入 commit。
- `before.png`（2100x1079）公开可见：咖啡馆的等待五分钟结算底部出现黄色“小满双重绝顶”。
- `after.png`（2100x1079）公开可见：同一存档、seed、玩家路线和对应时点回到咖啡馆角色/行动面板，没有该延迟多重绝顶文本。
- 本地 trace 证明小满 12:29 在玩家位于另一场景时 admission；附近 control 两边均显示凯尔希阴道小绝顶。但这两项保持 local-only，不嵌入 PR 主图，也不能作为公开文案中的验证细节。

fresh-context artifact audit 的两处修改要求：

1. 原 PR 验证段和 BEFORE caption 写了“小满 12:29 在哥伦比亚咖啡馆、玩家在动力内走廊发生该绝顶”。这把 local-only admission trace 和独立的 12:57 可见帧拼成公开连续叙事。请删除 12:29、具体异地来源和“实际发生于另一场景”等只有本地 trace 支撑的措辞。公开文案只可说：同一路线修复前在咖啡馆等待结算后出现延迟的“小满双重绝顶”，修复后对应时点不再出现。
2. 原验证段及 AFTER caption 声称两边 11:57 的“凯尔希阴道小绝顶”证明在场显示不受影响，但 `after.png` 本身不含该内容，附近 control 图不公开。请从正文和两张主图 caption 删除这项验证，不新增第三/第四张图。

约束：

- 保留“问题、修复、验证”三段简洁结构。
- 可以说明 997 是远程必须结算、不必显示，并说明玩家在场显示逻辑不被生产 diff 修改；但不要把 local-only 附近控制写成公开验证结果。
- 不写本地调查、trace、存档内部时间、测试、路径、non-goals 或未提交 artifacts。
- 图片链接保留 `BEFORE_URL` / `AFTER_URL` 占位。
- 输出唯一一版完整定稿；不要建议上传、push 或创建 PR。

