/investigate-game-bug

你是 erArk 本地 bugfix 计划的怀疑型文档与任务边界监督者。请根据下面的最新一手事实，裁定并起草最小文档修订。不要为了维护此前总表而忽略后来事实，也不要把“本地技术完成”“可以继续本地工作”“可以提交上游”混成一个状态。此轮只改 OpenSpec/计划文档，不改生产代码、测试、远端 PR 或 GitHub。

用户给你的授权边界是：你可以决定本地做哪些修复、怎样拆成小 PR task、怎样推进；游戏语义相关变更可以先按你判断最合理的方案完成本地实现，但用户会在提交 PR 前最终确认；push、发布证据、创建/修改 PR 等外发动作仍需另行授权。若 Codex 与你意见不一致，由你最终决定。

## 新的一手事实 A：PR 状态

2026-07-14 本轮用 GitHub CLI 直接读取上游：

- PR #212：OPEN，head `21261e9513984a50fa715009655e0731d769fe15`，标题“修复：开启苦痛快感化后，减少苦痛的结算会错误扣减心理快感”。
- PR #213：OPEN，head `e1a9378b140f99cd62f9c678c3a1113981e4e342`，标题“修复：干员熟睡后\"苦痛快感化\"被错误解除”。远端 diff 的 `clear_hypnosis_sub_states()` 仍不清除 `pain_as_pleasure`，所以远端现状仍是睡眠和直接取消都保留。
- PR #214：MERGED，mergedAt `2026-07-14T10:32:51Z`，head `64dcab6c5cf1042ad0eaed32204ac996f56f4b19`。本地 `upstream/master@abebf33b52ebf51424f71365946eb8df1f75a23c` 已包含该合并提交。

但当前 `program-task-map.md` 仍把 #214 写成 open/upstream-owned，`task-migration.md` 多行也仍以 live PR tracking 描述它。任何 movement-talk 实现都必须停止，剩余只可能是本地 overlay/mod/worktree 对账与经授权清理。

## 新的一手事实 B：#213 语义已被用户反转，但尚未外发

后来独立 change `clear-pain-as-pleasure-on-hypnosis-cancel` 已完整记录：

- 用户最终选择：睡眠和直接解除催眠都清除 `pain_as_pleasure`。
- Fable 最终审查接受在共享 `clear_hypnosis_sub_states()` 中增加唯一一行 `pain_as_pleasure = False`；13 个检查、`py_compile`、真实 Tk A/B 和最终证据审查通过。
- 本地 worktree `/home/ubuntu/games/erArk-pr-hypnosis-target-runtime` 正停在远端 PR #213 head `e1a9378b...`，仅有该一行生产修改与未跟踪 focused tests；未 commit、未 push、未改 PR、未发布图片。
- `clear-pain-as-pleasure-on-hypnosis-cancel/final-review.md` 明确写远端 PR head/title/body/images 仍描述已被否决的“保留”语义。

然而当前总表、`activate-granted-pain-as-pleasure` 的 proposal/tasks/spec/design，以及 `task-migration.md` 仍说 #213 的 accepted contract 是“睡眠和直接取消都保留”，并要求删除旧 mod 的 cancel-clear wrapper、把 BDD 改成保留。这会把本地维护方向做反。

请区分：远端 #213 当前事实仍是“保留”；用户/Fable 已选择但尚未外发的目标修订是“两条都清除”。不要把目标修订写成已经在 GitHub 生效。

## 新的一手事实 C：T2 玩家试玩门槛文档冲突

T2 `judge-orgasm-edge-once-per-settlement` 当前技术状态：

- 干净候选 worktree `/home/ubuntu/games/erArk-pr-edge-shared-settlement`，commit `579b7c47504038b6523decf71a565029ba76860a`。
- 11 个 submitted tests 与 11 个 near-real/local checks 本轮重跑通过；严格 OpenSpec 校验通过。
- matched Tk A/B、代码审查、Fable PR 文案、fresh artifact audit 均完成；artifact audit verdict `PASS`, publication state `local-review-ready`。
- 旧 owning docs 明确记录：用户曾选择本地玩几天再决定；tasks 5.3 和 5.4 仍未完成。

后来 umbrella `program-task-map.md:27` 与 umbrella `tasks.md:12` 却声称 2026-07-14 Fable 已取消 T2 的数日试玩门槛。实际 `fable-supervision.md` 的唯一 evidence follow-up 只逐字取消了 T1 discovery 的 playtest gate；它没有逐字对 T2 作同样裁定，较早处反而记录 T2 仍有 live player-test gate。因此 umbrella 当前把未发生的裁定归给了你。

结合用户现在授予你的本地推进权与“所有游戏语义在提交 PR 前由用户最终确认”边界，请你现在明确裁定 T2：

- 保留“必须实际玩数日后才能算本地任务完成”的旧门槛；或
- 取消固定数日门槛，把候选保持 `local-review-ready`，由用户在任何上游 PR 创建前做最终语义确认；被动游玩只作可选新线索；或
- 你认为证据支持的另一条精确边界。

不要因为用户旧时说过“玩几天”就自动保留，也不要因为总表已经写“取消”就自动追认；请独立判断证据是否足够。

## 新的一手事实 D：总表漏掉后来成立的 owners

`openspec list --json` 当前还包含但总表未完整纳入：

- `fix-game-update-depth-restoration`：6/6 complete，commit `80a711603` 已在 fork side branch；它是基础修复，但 Fable 曾认为缺单独玩家可见 PR 证据，应随真实 consumer 验证。
- `fix-elapsed-time-line-ownership`：0/12；目标是一次玩家点击只显示一次“分钟过去了”，文档与语义已过 Fable，无玩家选择。
- `add-per-click-orgasm-chain-gate`：0/17；用户已确认“按点击、非生理冷却”，允许被动刺激/高潮/结算继续；文档与语义已过 Fable。
- `clear-pain-as-pleasure-on-hypnosis-cancel`：10/10 local complete，但尚未外发修正 #213。
- `settle-remote-plural-orgasm-silently`：14/14 complete，候选 `364ac6d9f` 已通过 Fable/artifact review 并在 fork side branch；尚未创建 upstream PR，提交前需刷新到 #214 后的 upstream。

当前 T4 `fix-time-stop-release-attribution` 仍在证据阶段；attempt3 因预注册视口前置条件错误被你判 formal invalid，现正做隔离 rehearsal，不能写成已完成。旧总队列写 T4 后是 T5 两个 talk-state leak；elapsed-time 与 per-click chain 相互都依赖 depth restoration，但与 talk leaks 的最新全局顺序尚未由你裁定。

## 请裁定并起草

1. 给 `DOC RECONCILIATION PASS WITH PATCH`、`REVISE` 或 `BLOCK`。是否需要玩家现在介入？
2. 为 `program-task-map.md` 起草最小但自洽的替换文本，至少覆盖：
   - #212/#213/#214 当前真实状态；
   - #213 远端现状与本地已选目标修订的区别；
   - T2 的最终本地/语义/外发门槛；
   - pain local-maintenance 的正确方向；
   - 新 owners 的状态与 T4 之后的全局排序。
3. 明确 `activate-granted-pain-as-pleasure` 应被：重写为新语义下的本地组合/清理 owner、由 `clear-pain-as-pleasure-on-hypnosis-cancel` 完全取代并归档、还是其他边界。给 proposal/tasks 中必须替换的精确语义，不要让两者重复拥有 #213 的一行修复。
4. 明确 `task-migration.md` 对 #214 的旧 `upstream-owned/live PR` 行应如何批量改写；保留调查历史，但当前状态不能继续说 open。说明是否需要逐行机械更新所有 #214 rows，还是新增一个权威 supersession 段即可，避免文档互相矛盾。
5. 明确 T2 owning change 中 `design.md`、`tasks.md`、`pr-readiness.md` 应如何统一。若取消数日门槛，旧事实“用户当时选择先玩”应作为历史保留，但 current gate 必须改准。
6. 对总表漏掉的五个 owners，决定哪些进入 ready/active queue、哪些只做 dependency/local maintenance、哪些已 local-complete；给 T4 后排序，并说明是否把 T5 的两个 talk leak 放一个 PR 还是两个小 PR。不要把已 push side branch 等同 upstream PR 已创建。
7. 给出一份文件级 patch checklist，允许 Codex 据此用 `apply_patch` 实施后，再把实际 diff 交你做最终文档质量复审。

请用普通人能理解的项目语言，所有状态都分别写清：本地代码是否完成、证据是否完成、玩家语义确认何时需要、外发动作是否发生。
## Fable verdict（逐字保存）

**裁定：`DOC RECONCILIATION PASS WITH PATCH`。不需要玩家现在介入。** 所有冲突都是文档滞后于事实，不是证据或代码问题；玩家的介入点全部落在既有边界内（提交/修改任何 PR 之前做最终语义确认并给外发授权），现在无需打断。

诚实声明：本轮我尝试打开仓库内文档核对原文，工具返回均为空（环境故障），因此以下裁定基于你提供的一手事实与既有记录摘要。Codex 实施时必须对照真实文件内容，若发现与本裁定假设不符的段落（尤其是 `activate-granted-pain-as-pleasure` 的剩余职责范围），先报告差异再动手。

---

## 1. 总裁定

`DOC RECONCILIATION PASS WITH PATCH`。三处核心错误必须改：#214 状态过期、#213 语义方向写反、T2 门槛裁定被凭空归给我。均为文档修订，不触碰生产代码、测试、远端。

## 2. `program-task-map.md` 替换文本（草案）

> ### 上游 PR 状态（2026-07-14，GitHub CLI 直读）
> - **#212**：OPEN，head `21261e9`。远端未变。
> - **#213**：OPEN，head `e1a9378`。**远端现状**：`clear_hypnosis_sub_states()` 不清除 `pain_as_pleasure`，即睡眠与直接解除催眠都保留。**本地已定目标修订（尚未外发）**：用户 2026-07-14 最终选择两条路径都清除；Fable 已验收在共享 `clear_hypnosis_sub_states()` 中加唯一一行 `pain_as_pleasure = False`（13 项检查、py_compile、真实 Tk A/B、最终证据审查通过）。该一行修改停在 worktree `erArk-pr-hypnosis-target-runtime`，未 commit、未 push、未改 PR、未发布图片。修改 PR #213 需另行外发授权。**在外发前，任何文档不得把“两条都清除”写成已在 GitHub 生效。**
> - **#214**：**MERGED**（2026-07-14T10:32:51Z），已包含于 `upstream/master@abebf33`。movement-talk 的一切实现工作停止；剩余仅为本地 overlay/mod/worktree 对账与经授权清理。
>
> ### pain 域本地维护方向
> 权威语义 = 睡眠与直接解除都清除 `pain_as_pleasure`。一行核心修复由 `clear-pain-as-pleasure-on-hypnosis-cancel` 独占。旧 mod 的 cancel-clear wrapper 与新语义同向，**不按“语义错误”删除**，仅在核心一行修复完成本地集成后按“被核心修复取代”退役。BDD 以“解除即清除”为准。
>
> ### T2 `judge-orgasm-edge-once-per-settlement` 门槛（2026-07-14 监督者裁定，本轮作出）
> 本地代码：完成（`erArk-pr-edge-shared-settlement@579b7c4`）。证据：完成（11 提交测试 + 11 近真实检查本轮重跑通过、matched Tk A/B、artifact audit PASS，`local-review-ready`）。固定“玩数日”门槛**取消**，理由：22 项检查加匹配 Tk A/B 已覆盖该结算边界缺陷的可证伪面，被动游玩对此缺陷信号极低，且用户已把最终语义确认移到 PR 创建前。被动游玩降级为可选新线索来源，出现新线索即重开。玩家语义确认：在创建上游 PR 前进行。外发：未发生，需另行授权，且提交前须对照 #214 合并后的 upstream 重验 rebase。历史事实“用户当时选择先玩几天”保留为历史记录。此前总表把该裁定归于早先 Fable follow-up 属误记；以本条为准。
>
> ### T4 之后全局队列
> - **T4** `fix-time-stop-release-attribution`：证据阶段。attempt3 因预注册视口前置条件错误判 formal invalid，隔离 rehearsal 进行中。不得写成完成。
> - **T5** `fix-elapsed-time-line-ownership`（0/12）：ready。依赖 depth restoration；作为其第一个真实 consumer，一并提供玩家可见验证。无需玩家语义选择。
> - **T6** `add-per-click-orgasm-chain-gate`（0/17）：ready。依赖 depth restoration。用户已确认“按点击、非生理冷却”语义。
> - **T7** 两个 talk-state leak：默认两个小 PR；仅当调查证明二者违反同一条规则、修复落在同一逻辑 owner 的同一生命周期操作上时才合并为一个 PR。
> - **依赖项** `fix-game-update-depth-restoration`：6/6 本地完成，commit `80a711603` 在 fork side branch。不单独发 PR；随 T5/T6 首个真实 consumer 一起获得玩家可见证据。
> - **local-complete、等待外发授权**：`clear-pain-as-pleasure-on-hypnosis-cancel`（10/10，待修订 #213）；`settle-remote-plural-orgasm-silently`（14/14，候选 `364ac6d9f` 在 fork side branch——**side branch 已 push ≠ upstream PR 已创建**；提交前刷新到 #214 后 upstream 并做用户语义确认）。

排序理由（供文档引用）：T5 放 T6 前是因为它更小、纯显示语义、无未决玩家选择，能最快让 depth restoration 获得真实 consumer 验证；T6 语义已确认但改动面更大；talk leaks 与 depth restoration 无依赖，殿后。

## 3. `activate-granted-pain-as-pleasure` 的边界

**改写为“pain 域本地组合与 mod 退役 owner”，不归档、不重复持有一行修复。** 精确替换：

- proposal 中 “#213 accepted contract = 睡眠和直接取消都保留” → 替换为上面第 2 节 #213 段的双状态表述（远端现状 vs 本地已定目标修订）。
- tasks 中 “删除旧 mod 的 cancel-clear wrapper（因语义错误）” → “在核心一行修复本地集成后，按被取代退役该 wrapper；退役前用 A/B 确认无双重清除或行为差异”。
- spec/design 中要求 “取消催眠保留 pain_as_pleasure” 的 BDD → 反转为 “睡眠与直接解除均清除”，并注明生产一行修复的 owner 是 `clear-pain-as-pleasure-on-hypnosis-cancel`，本 change 的验收只覆盖组合/退役，不覆盖也不复述那一行 diff。
- 新增非目标：不修改 `clear_hypnosis_sub_states()`。

**兜底规则**：Codex 打开文件后如发现该 change 除 cancel 一行相关内容外已无实质剩余职责（无独立的组合/退役工作），停下报告，届时改为“由 `clear-pain-as-pleasure-on-hypnosis-cancel` 取代并归档”。

## 4. `task-migration.md` 的 #214 行

**新增一个权威 supersession 段，不逐行机械改写历史行。** 段落置于 #214 相关内容之首，内容：MERGED 时间戳、已在 `upstream/master@abebf33`、“以下所有把 #214 描述为 open/live tracking 的行是各自日期时的调查历史，当前状态以本段为准；movement-talk 实现停止，剩余为本地对账与经授权清理”。**例外**：若文档存在意在反映“当前状态”的汇总表/状态列，那些活单元格必须逐个改为 MERGED——历史叙述保留，活状态字段不许说谎。

## 5. T2 owning change 三个文件的统一

- `design.md`：追加 2026-07-14 裁定段（同第 2 节 T2 文本），保留“用户当时选择先玩”原文为历史。
- `tasks.md`：5.3、5.4 标注 “superseded by 2026-07-14 supervisor ruling（未执行，非完成）”，不打勾。
- `pr-readiness.md`：状态保持 `local-review-ready`；剩余门槛明确列三项：① 用户最终语义确认（PR 创建前）；② 外发授权；③ 对 #214 后 upstream 的 rebase 重验。

## 6. 五个漏记 owner 的归类

| owner | 归类 |
|---|---|
| `fix-game-update-depth-restoration` | dependency/local maintenance，随 T5/T6 consumer 验证，不单独排队 |
| `fix-elapsed-time-line-ownership` | ready queue，T5 |
| `add-per-click-orgasm-chain-gate` | ready queue，T6 |
| `clear-pain-as-pleasure-on-hypnosis-cancel` | local-complete，等待外发授权（修订 #213） |
| `settle-remote-plural-orgasm-silently` | local-complete，等待用户语义确认 + 外发授权 + post-#214 rebase 重验 |

Talk leaks：默认两个小 PR，合并条件见第 2 节 T7。

## 7. 文件级 patch checklist（供 Codex apply_patch）

1. `program-task-map.md`：用第 2 节草案替换 PR 状态、pain 方向、T2 门槛、队列各段；删除 “Fable 已于此前取消 T2 试玩门槛” 的误记（第 27 行附近）。
2. umbrella `tasks.md:12` 附近：同样把 T2 门槛来源改为 “2026-07-14 监督者裁定”，不再引用不存在的早先 Fable follow-up。
3. `task-migration.md`：按第 4 节加 supersession 段；核查是否存在活状态汇总字段需逐格改 MERGED。
4. `activate-granted-pain-as-pleasure/{proposal,tasks,design,specs/local-bugfixes/spec}.md`：按第 3 节替换；遇兜底条件先报告。
5. T2 owning change `{design,tasks,pr-readiness}.md`：按第 5 节。
6. 各文件中凡把 “side branch 已 push” 写作 “PR 已创建” 或把本地目标修订写作 “已在 GitHub 生效” 的措辞，一律改为分列四态：本地代码 / 证据 / 玩家语义确认时点 / 外发是否发生。

实施后把实际 diff 交回我做最终文档质量复审；复审时我会同时补上本轮未能完成的原文核对。

