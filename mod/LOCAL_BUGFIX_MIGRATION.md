# 本地 Bug 修复拆分迁移表

本表记录本地 `mod/` 组件与上游 PR 的对应关系。最近一次经由 `rebase-fork-to-upstream`
技能重建（2026-07-18 第四次）：代码基线 = `upstream/master`（`645052d24`，含已合并的
221/223/224/225/227/229/230/232）+ 全部 open PR（228、231、233）的 head + 三个本地候选
分支 `fix-tk-click-dispatch`（`45dbb4c6a`，Tk 单击派发修复）、`perf-batch-scroll`
（`5633e18d9`，批末合并滚动性能优化）、`fix-render-window-input`（`06a6ece25`，渲染期
输入门禁＋快速连点红底选区清除）——三者已在 meower-z/erArk-fork 开审查 PR #1/#2/#3，
待用户审查后向上游提交；本地文档、知识库与非 PR 组件全部保留。#226 被上游拒绝，由本地
mod `local_orgasm_chain_gate_fix` 承接（见下）。

`local_bugfix` 已迁移到 `mod/deprecated/local_bugfix/`，默认配置不再启用。请使用下列拆分组件替代。

## 保留但禁用的本地组件

| 修复行为 | 组件 | 状态 |
| --- | --- | --- |
| 群交结束/NPC退出/转H/无意识恢复前释放寸止计数 | `local_group_edge_release_fix` | 保留但**刻意禁用** |
| 催眠模式持久化、单人催眠状态校正、催眠态口上门禁 | `local_hypnosis_state_fix` | 保留但**禁用**（2026-07-18 起） |

`local_group_edge_release_fix` 是较早的批处理实现，与 PR 221 的一次判定方案重叠，维护者
刻意将其禁用（不写入 `enabled_mods`），本次重建保持该决定。

`local_hypnosis_state_fix` 的缺陷 1（切换模式不即时生效）与缺陷 3（催眠口上被通用无意识
门禁吞掉）已分别由 open PR #232、#233 上游化并作为代码合入本树，若继续启用，mod 的旧包装
函数会遮蔽 PR 代码，故禁用。mod 中仍有 PR 未覆盖的部分：缺陷 2 核心（类型"无"时误清既有
催眠状态，用户 2026-07-18 拍板放弃上游化：触发前置过于刻意）、"无"档位逐次手动选择面板、
理智耗尽后的子状态清理。保留目录以备将来取回；注意其包装函数基于 PR 前的函数体，**重新
启用会回退 #232/#233 的修改**。

`local_group_masturbation_intent_fix` 已于 2026-07-18 撤下删除（再审计认定普通玩法不可达，
记录见 git 历史中的 openspec 归档）。

## 已被上游覆盖、组件已删除或禁用

下列 PR 的修复已在 `upstream/master` 中，核心行为由上游代码及回归测试负责。表中"已删除"
的组件里，`local_orgasm_settle_edge_fix`、`local_group_participant_admission_fix`、
`local_pain_as_pleasure_fix`、`local_h_orgasm_batch_fix`、`local_h_movement_interrupt_fix`
实际仍保留在盘上（2026-07-19 恢复本地基础设施时带回），但均未启用——`mod_config.json` 的
当前启用清单才是运行时事实。重新启用任何一个前必须先核对其包装的上游函数是否已变化。

| PR | 状态 | Core 责任 | 本地组件处理 |
| --- | --- | --- | --- |
| 204 | 已合并 | 外勤委托声望显示 | `local_commission_number_display_fix` 已删除 |
| 205 | 已合并 | 四个场景全员前提完整遍历 | 从参与准入组件移除 `place_all_not_h` |
| 206 | 已合并 | 隐奸发现结算跳过已处理发现者 | 从参与准入组件移除全局发现者 helper 包装 |
| 207 | 已合并 | 跨平台存档路径归一化 | `local_cross_platform_save_fix` 已删除 |
| 210 | 已合并 | 群交 AI 临时 target 恢复 | `local_group_target_context_fix` 已删除 |
| 211 | 已合并 | 无意识奸指令的正交前提 | 无独立组件 |
| 213 | 已合并 | 解除催眠时一并解除苦痛快感化 | 由 `local_hypnosis_state_fix` 之外的上游核心负责 |
| 214 | 已合并 | 干员移动地文来源、普通 NPC 模板上下文 | `local_npc_move_talk_context_fix` 已删除 |
| 215 | 已合并 | 异地多重绝顶延迟显示 | 无独立组件 |
| 216 | 已合并 | `game_update_flow` 嵌套返回后运行深度 | 无独立组件 |
| 217 | 已合并 | 自身状态/经验结算数值缩写单位 | 无独立组件 |
| 218 | 已合并 | H中被发现面板反应漏结算/重复结算 | 无独立组件 |
| 221 | 已合并 | 一次高潮结算只作一次共同寸止判定、绝顶等级只推进一次；多部位取幂改为 max(1, n/2)，基础失败率由 0.2 降为 0.15 | `local_orgasm_settle_edge_fix` 已删除（另含 `local_h_orgasm_batch_fix` 的寸止职责） |
| 223 | 已合并 | 通用口上候选列表跨调用累积污染 | 无独立组件 |
| 224 | 已合并 | 通用口上临时交互目标泄漏 | 无独立组件 |
| 225 | 已合并 | `handle_self_exhausted` 前提统一过滤力竭/疲劳干员 | `local_group_participant_admission_fix` 已删除 |
| 227 | 已合并 | 时停解除时干员的绝顶经验不再错误记在博士名下 | 无独立组件 |
| 229 | 已合并 | 群交中体力耗尽干员正确退出、退出结算不再重复触发 | 无独立组件 |
| 230 | 已合并 | 快感栏部位名按绝顶寸止次数着色（灰/亮粉/深粉/红/紫） | 无独立组件 |
| 232 | 已合并 | 切换催眠模式后立即对当前目标套用催眠状态 | `local_hypnosis_state_fix` 缺陷 1 职责由上游承接，mod 保持禁用 |
| 212 | 已关闭（未合并） | 苦痛快感化只转换正向苦痛、直接苦痛二段转换 | 行为已由上游 `common_default.py`（`final_value > 0` 门禁）与二段结算统一改造覆盖；`local_pain_as_pleasure_fix` 已删除 |

| 222 | 已关闭（未合并） | 异地干员的 H 结算文本泄漏给玩家 | 上游 `97c35826e` 改为异地一律走 must-show/must-settle 通道，泄漏绘制效果 404–408 均非 must-settle，已验证覆盖；`local_h_orgasm_batch_fix` 已删除。详见 git 历史中的 openspec 归档 2026-07-17-remote-display-leaks-closed |

PR 212、222 虽被上游关闭而非合并，但同一行为均已由维护者直接在上游修复，因此其组件无保留必要。

## 已作为代码合入本地、上游仍 open 的 PR

本次重建把下列仍 open 的 PR head 直接合并为代码；这不表示它们已被上游合并。对应的本地
运行时组件因此删除（代码已在树内，无需再叠加 mod）。

| PR | 上游 head | Core 责任 | 删除的组件 |
| --- | --- | --- | --- |
| 228 | `68f594b72` | 在 `handle_h_flag_to_1` 首次进入 H 时集中撤销旧移动计划（玩家与 NPC 均经此 effect 进入 H），`own_charcter_move` 检测计划被撤销后停止寻路 | `local_h_movement_interrupt_fix` 已删除（PR 是同一意图的根因集中修复，取代 mod 的逐入口 monkey-patch） |
| 231 | `060b87352` | 绝顶等二段结算的纸娃娃地文主语不再被错误替换为玩家 | 无独立组件 |
| 233 | `8dbe6cc70` | 催眠类无意识对象绕过通用无意识口上门禁，催眠专属口上可显示 | `local_hypnosis_state_fix` 相应职责（缺陷 3）由 PR 承接，mod 保持禁用 |

另有三个本地候选分支（非上游 PR）同样以代码形式合入：`fix-tk-click-dispatch`（单击指令
按钮误判为空白点击）、`perf-batch-scroll`（一批输出合并为一次滚动）、`fix-render-window-input`
（渲染期/黑屏期点击不再误触发到未显示的新界面＋快速连点不再露出红色选区底）。三者待本地
试玩验证后再开上游 PR。

## 2026-07-18 用户决定移除的个人组件

下列组件本属 KEEP 类个人 mod，但用户在本次重建中明确要求移除（`local_settlement_input_fix`
依赖 `local_performance`，一并移除以保持一致）。已从 `enabled_mods` 与 `load_order` 删除，目录已删除。

| 组件 | 原职责 | 移除依据 |
| --- | --- | --- |
| `local_performance` | Tk `_get_main_frame` 输入隔离（避免普通等待消费旧输入）＋ `askfor_wait` 队列重复滚动合并 | 其点击/输入隔离目的已由本地分支 `fix-tk-click-dispatch` 在核心层（`key_listion_event.py` 等）解决 |
| `local_settlement_input_fix` | Web 显式等待节奏、录制期显式 `wait` 保留、作用域化跳过标记归属 | Web 等待节奏（wait patch）被判不可上游；其 see_end 相关合并留待未来独立上游 PR；依赖的 `local_performance` 已移除 |

## 已被上游拒绝、保留为本地 mod

上游关闭而非合并、但用户选择在本地保留其行为的 PR，改由 KEEP-and-enable 的本地 mod 承接。
这类 PR 的树内内联代码在下次 `rebase-fork-to-upstream` 时不会再被合入（已不在 open PR 列表），
故必须由 mod 在运行时等价重建行为。本次已同步剥离对应内联代码，使 mod 成为该行为的唯一所有者。

| PR | 状态 | Core 责任 | 承接组件 |
| --- | --- | --- | --- |
| 226 | 已关闭（未合并） | NPC 多重绝顶后在同一次玩家点击内不再被反复调度、堆叠大量口上（per-click 链式门禁） | `local_orgasm_chain_gate_fix`（KEEP+启用）。上游维护者计划把"绝顶后影响意识程度"纳入将来的负体力 H / 无意识 H 大系统，与本 PR 冲突而拒绝合并。mod 用 wrapper 等价重建：检测 `plural_orgasm_*` 二段行为置 `sp_flag.multi_orgasm_this_player_action`，两个 AI 生成入口读标记早退，`game_update_flow` 最外层重置。已剥离树内内联代码（`game_type`/`handle_npc_ai`/`handle_npc_ai_in_h`/`second_behavior`/`update`）。 |

## 已被上游拒绝且无组件承接

| PR | 状态 | 说明 |
| --- | --- | --- |
| 220 | 已关闭（未合并） | 「X分钟过去了」逐面板重复输出的统一显示修复被撤回；无对应组件，其代码不再随本地保留 |
