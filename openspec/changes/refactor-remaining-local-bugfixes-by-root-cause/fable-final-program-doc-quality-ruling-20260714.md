# Fable ruling: final program-document quality review

Invocation: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Prompt: [fable-final-program-doc-quality-prompt-20260714.md](fable-final-program-doc-quality-prompt-20260714.md).

Exact response follows.

```text
**裁定：`FINAL DOC PASS WITH PATCH`。** 除 T4 的证据边界外，所有文档与一手事实一致；T4 在三个文件里仍呈现过期的六-NPC/rehearsal 状态，会误导任务选择和完成状态判断。按下列机械 patch 修完即可，无需回来复审。

## 必须修的问题（按严重性）

### 1. HIGH — `program-task-map.md` T4 三处过期（你标记的六-NPC 疑点确认为过期边界）

**Why it is a bug candidate**，现句 "…but the six-NPC scene has not yet been replayed as baseline/candidate runtime evidence." 问题：把六-NPC 场景当作待复现目标，而正式路线早已改为两-NPC 路线。替换为：

> "The values in an earlier player screenshot match the existing formula for six deferred body-part orgasms; that screenshot remains historical corroboration only. The proven normal-UI route is a two-NPC route: Lin (4080) accumulates deferred counts `{0: 1, 21: 2}` and a qualifying 射精位置 through four oral actions, the player switches the current target to Jingzhe (306), then releases time stop. Matched Tk A/B on that route is still pending."

**Current state**，现句 "…an isolated rehearsal is in progress." 问题：漏掉 attempt 4 run 1 结果与最新裁定，且暗示 rehearsal 正在跑。替换为：

> "Attempt 3 is formally invalid because its pre-registered viewport prerequisite was wrong. Attempt 4 run 1 proved the normal-UI target switch and reached sample2, but the `[4115]` button on a scrolled-back output page was visible with a dead callback, so run 1 is route/endpoint evidence only. The latest Fable ruling is ROUTE A PASS with a mandatory fresh disposable run 2 (start through sample2, then click the bottom active `[4115]` directly, with no post-switch readable proof loop). Run 2 has not started; the formal matched A/B is not complete."

**Next work**，现句 "finish that rehearsal, then run the real loader with the batch mod both disabled and enabled, verify actual applied values and caps, and produce…evidence for the six-NPC release." 问题：real-loader 矩阵、mod-on/off smoke、值/cap、Web 收集均已完成（T4 tasks 2.1–2.4 已勾），再列为 next work 会误导任务选择；六-NPC release 不是目标。替换为：

> "Run the fresh disposable run 2 endpoint rehearsal; only after it succeeds, capture the matched pristine-baseline versus candidate Tk A/B on the Lin→Jingzhe two-NPC route. The real-loader identity matrix, batch-mod compatibility smoke, applied-value/cap checks, and Web collection checks are already complete."

**Done when** 一段可保留：它是完成判据清单，不是状态声明。

### 2. HIGH — T4 `implementation-notes.md` 缺 run 1 / ROUTE A / run 2 记录，且冻结重放的端点描述已被超越

"Multi-target route checkpoint" 段全部保留为历史，但其末句 "The formal replay uses the shorter matched viewport sequence approved by Fable…" 描述的端点已过期。在该段之后追加一段（并在末句前加 "(endpoint later superseded below)" 或等效标注）：

> "## Attempt status (2026-07-14)
>
> Attempt 3 is formally invalid: its pre-registered viewport prerequisite was wrong. Attempt 4 run 1 replayed the route through the target switch and sample2, confirming the switch and the post-switch state, but the `[4115]` visible on a revisited earlier output page had an inert callback; run 1 is endpoint-diagnostic evidence, not a baseline result. Fable's latest ruling is ROUTE A PASS with a mandatory fresh disposable run 2: delete the post-switch readable proof loop, and after sample2 click the bottom active `[4115]` directly. Run 2 has not started. The formal matched A/B remains open and must follow Route A."

### 3. MEDIUM — umbrella `tasks.md` 3.1

现句 "…and the isolated rehearsal is still in progress." 替换为：

> "…attempt 3 is formally invalid because its pre-registered viewport prerequisite was wrong; attempt 4 run 1 proved the target switch and sample2 but exposed a dead scrolled-back `[4115]` callback, and the mandatory fresh disposable run 2 endpoint rehearsal is pending under the ROUTE A PASS ruling."

### 4. MEDIUM — T4 `tasks.md` 3.2 的 pre-release 观察要求与 ROUTE A 端点裁定冲突

现句要求 "pre-release observation must show A's deferred counts and qualifying射精位置 still present while B is the current target"。run 1 已证明在旧输出页做可读证明会使 `[4115]` callback 失效，正式重放不得插入该循环。替换 3.2 尾部为：

> "…with the same save, seed, and physical actions, following Route A: reach sample2, then click the bottom active `[4115]` directly with no post-switch readable proof loop. A's trigger-state persistence is established by attempt 4 run 1's post-switch observer evidence, not by an in-run readable loop. Before the formal A/B, the fresh disposable run 2 endpoint rehearsal must succeed."

## 逐项核对（无需改动）

- **#212/#213/#214 四态**：program-task-map、task-migration、pain 全套（proposal/tasks/design/notes/delta spec）一致且正确——#212 OPEN@21261e9，#213 OPEN@e1a9378 且远端两条退出均保留，#214 MERGED@2026-07-14T10:32:51Z 含于 abebf33，movement-talk 只剩本地对账与授权清理。无"本地目标已在 GitHub"的误述。
- **T2 gate**：五处（map、umbrella 2.2、task-migration、T2 design tail、tasks 5.3–5.7、pr-readiness）表述一致：local-review-ready，固定数日门槛 superseded without execution（且明确"not completed"），三项 pre-PR gate 完整。5.3/5.4 保持未勾并标注 superseded 是正确写法。
- **pain owner**：composition change 全部文档均限定为消费 one-line fix、退役 wrapper、验证组合，Non-Goals 明确禁止复制 core edit；delta spec 的 SHALL NOT 条款正确。
- **T4–T7 顺序与 depth restoration 依赖**：四处一致，无冲突。
- **local-complete vs upstream-published**：`80a711603`、`364ac6d9f`、`579b7c475` 均正确标注为本地/fork side branch 而非 upstream PR；"A pushed side branch is not an upstream PR" 措辞保留。
- **历史文字**：pain implementation-notes 的全部 Historical 段、T4 的 route checkpoint 段、T2 的 2026-07-13 决策记录均可原样保留——它们已被明确标注为 checkpoint/历史且有 supersession 指针。pr-readiness 的 "## Submitted Diff" 在你提供的摘录中为空，若原文件确有 diff 内容则不动；若真为空，补一行指向候选 commit 即可，不算语义问题。

## 复审与玩家介入

**4.** 按上列机械 patch + 三项 strict validate + `git diff --check` 即可，不必再问我：所有替换文本已给全，无剩余判断点。唯一例外——若 patch 时发现 T4 文档中还有本摘录未含的六-NPC 或 "rehearsal in progress" 表述，用第 1 条的同一替换意图处理，仍不需复审。

**5.** 不需要玩家现在介入。当前无 player-input stop；T2 与 `settle-remote-plural-orgasm-silently` 的语义确认只在各自 PR 创建前触发。本轮不改生产代码、不外发。
```
