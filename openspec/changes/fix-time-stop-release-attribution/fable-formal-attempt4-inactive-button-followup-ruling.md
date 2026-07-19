# Fable ruling: attempt 4 inactive old-button follow-up

Invocation: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Prompt: [fable-formal-attempt4-inactive-button-followup-prompt.md](fable-formal-attempt4-inactive-button-followup-prompt.md).

Exact response follows.

```text
**裁定：`ROUTE A PASS`（附条件：必须完成 run2 端点演练）。**

## 逐项回答

**1. 路线裁定 — ROUTE A PASS。**
run1 的严格执行结果是合格的否证：旧 grid 上的 `[4115]` 文字可见但回调已死，这是运行事实，推翻了我上一轮"证明循环免费在路径上"的前提。在新事实下重新比较：post-switch 可读证明循环的唯一价值是一张人类可读的展示图，它不服务 bug 触发，却要求引入一条完全未验证的 scrollbar down-route（新坐标 anchor + 新探索 + 两侧重放一致性负担）。sample 2 是更强的当前状态正证——它直接测量了 formal 所要断言的东西（target=306、trigger map 仅林 4080、林各项与 sample 1 不变）。选 B 是用一条新的脆弱路线去买一张装饰图，不符合最小、可信、可重复的标准。

**2. 是否需要 run2 — 需要，这是 PASS 的硬条件。**
run1 从未成功触发过任何一次 release：目前整个证据链里"点击活跃 `[4115]` → 进入结算"这个端点从未被演示过，而本轮恰恰证明了关于该端点的假设可以错。formal 不允许是史上第一次尝试 release 点击。因此：关闭 run1；新建 disposable baseline rehearsal run2，从头重放已验证路线（同 seed、同 PYTHONHASHSEED、同 overlay、同物理输入序列），到 post-switch bottom/sample 2 后不上翻，只点一次当前底部活跃 `[4115]`，冻结第一张字节稳定 release anchor。run2 任一既有 anchor 不符即停、不补输入。run2 成功后即可冻结 formal prereg；"点击后 anchor 不符即作废"继续作为 formal 侧的失效条款，但它是保险，不是端点演练的替代。

**3. B 路线探索授权 — 不适用，且明确撤销：** 不授权任何 scrollbar down-route 探索。旧 H grid 失效按钮永久禁用作输入端点。

**4. PR-facing 证据构成 — 不再要求"惊蛰高亮+状态"图。**
以下组合足以让人类审稿者理解 A/B 目标切换：(a) 点击前人类可读的名单帧（含惊蛰条目可辨认），(b) 点击惊蛰的 transport 帧记录，(c) sample 2 对称 observer 输出（作为可审计内部正证归档，不必进 PR 正文），(d) matched baseline/candidate release 结算页——这两张图本身就是 bug 的展示：错误归属 vs 正确归属，是最有说服力的 reviewer-facing 画面。PR 草拟时由 fable-5 写图注，说明"已切换目标至惊蛰后解除时停"这一前置即可。

**5. Observer — 接受，按现 SHA 冻结。**
对称输出 lin_4080/jingzhe_306 的 experience 10/20/78/111/156、counts、shoot position、is_h，保留全体非默认 npc_states、target、player H、time stop、sample index，满足我上一轮要求。独立只读审查 PASS（零 count 过滤、缺经验补 0、原对象不变、排序 JSON 可重复）已覆盖我的验收关注点。`e33cfec8...` 原样用于 run2 与 formal prereg，不得再改动；若必须改动则重新走独立审查。

**6. 玩家介入 — 现在不需要。**
不改玩法语义、不做外发动作，全部在既有授权边界内。玩家介入点仍是既定的两处：上游 PR 提交前的语义最终确认，以及任何 push/publish/PR 外发动作。

**执行摘要：** 关 run1 → 建 run2 全程重放 + 一次活跃 `[4115]` 点击 → anchor 全符则冻结 formal prereg（含 observer `e33cfec8...`）→ 执行 matched A/B formal。run2 再失败一次即回来 `REVISE`，不得自行换路线。

请将本裁定逐字存入该 change 的记录。
```
