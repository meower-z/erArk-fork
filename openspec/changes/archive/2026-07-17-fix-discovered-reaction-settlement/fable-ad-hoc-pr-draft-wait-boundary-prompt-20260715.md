/investigate-game-bug

你是 erArk upstream PR 文案作者。只读，不修改任何文件。请用中文输出一份完整、可直接复制的 PR draft：先给一行标题，再给 Markdown 正文。候选工作树是 `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc`，精确 base 是 `upstream/master` `94d586840484adf21fcf746dba0444551dd6a5a1`，精确 head 是 `4e226f4f587b82a87368a3d7976650593323a7b4`。请实际读取这两个提交之间的四文件 production diff、相关 caller 和面板分支，再写文案。

面向 maintainer 的事实范围：

1. 问题是 H 被发现面板的明确发现者反应在两个 caller 下没有统一的恰好一次保证：某些分支的反应文本和效果会完全漏掉，某些原本已结算的分支又可能被 NPC 外层重复结算。已接受的静态 A/B 只证明玩家最直接可见的问题：baseline 中闭锁选择“劝说离开”后，她的接受/离开反应完全缺失，多萝西的 H 文本直接继续；修复后闭锁的反应恰好出现一次，然后 H 文本继续。
2. 修复保持每个既有 response branch 的写法，只在缺失的分支局部补发现者结算，并把“本次发现处理是否已经完成”沿 NPC 状态机返回给外层。
3. 必须清楚说明这个很小的后继设计：如果发现反应使 NPC 真正进入 `MOVE`，本轮继续结算移动；如果寻路失败而回退为 `WAIT`，不再额外结算这次等待，因为刚才的发现反应已经给了 NPC 足够的可见表现，而等待没有后继工作。直接从隐蔽 H 流程打开面板的 caller 仍不虚构一个完整 NPC 回合。
4. 反应必须先于任何结束 H 或转群交的后续处理，避免 pending reaction 被覆盖。
5. 不改变发现资格、说服判定、群交模板、同一发现者再次发现规则或其他普通 NPC 状态机。

证据正文必须使用两张静态 PNG 的占位 URL，不得使用 GIF：

- before: `{{DISCOVERY_SETTLEMENT_BEFORE_PNG_URL}}`
- after: `{{DISCOVERY_SETTLEMENT_AFTER_PNG_URL}}`

请用简洁的 upstream 风格组织为“问题 / 原因 / 修复 / 验证”或等价的短小结构。验证处用 before/after 表或相邻图片，并给出准确、克制的图注。图片上半部的 candidate 红绿标签已经从最终 clean PNG 中裁掉，所以不要提标签。

严格禁止在标题、正文、图注中出现或暗示以下内容：任何旧实现、统一函数、内部探索历史、被放弃的方案、私有分支比较、OpenSpec、worktree、本地测试、line count、penalty、Fable、Codex、尚未发布的本地路径。也不要说“相比某个旧版本”。Upstream 只需要理解当前 bug、当前 diff 和当前设计。

不要把“有路时继续 MOVE、无路 WAIT 时跳过”写成性能优化；这是避免在已显示发现反应之后再人为增加一次无事可做的结算，同时保留真实移动的游戏行为。不要扩大证据声称：两图只证明这条漏反应案例的 before/after，不证明所有分支，也不证明重复发现规则。

只输出 PR 标题和正文，不要输出分析、审查备注或待办清单。
