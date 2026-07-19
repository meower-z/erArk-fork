# CONTEXT.md — 本地 fork 领域词汇与机制

本仓库是 `erArk/erArk` 的 fork。上游系统文档在 `.github/prompts/数据处理工作流/`;本文件只覆盖**本地 fork 自己的**词汇、机制和现状(含已被上游吸收的本地决策,注明"现由上游提供")。决策记录在 `docs/adr/`;机制快照(跨模块契约、不变量、坑)在项目 wiki,入口 [docs/wiki/INDEX.md](docs/wiki/INDEX.md)——本文件是词汇表(术语定义),wiki 是机制细节,别混。各条目提到的 openspec 规格原文已随 openspec 工作流废弃删除,可在 git 历史的 `openspec/specs/` 下找回。

## 本地开发模式

- **mod 组件化**:所有本地修复/增强以独立 mod 组件交付(`mod/<name>/`),通过 mod loader 的函数替换打补丁,上游 `Script/` 文件保持干净。见 [ADR-0001](docs/adr/0001-local-fixes-as-mod-components.md)。
- **上游优先**:能被上游接受的修复走 upstream PR;被拒或过于个人化的才留作本地 mod。rebase 后被上游吸收的 mod 转为**禁用**留档(见下)。
- 当前启用的 mod(`mod/mod_config.json`):`easy_mode`、`group_sex_extension`、`local_fontfix`、`local_orgasm_chain_gate_fix`。其余 `local_*` 组件在盘上但禁用——其行为已由上游合并的 PR 提供或待重新评估。

## 词汇表

- **玩家动作窗口(player action window)**:一次最外层玩家点击驱动的完整结算周期——玩家行为结算 + 全体 NPC 追赶(catch-up),以 `cache.over_behavior_character` 收齐为界。多个本地机制以它为作用域单位。
- **群交 type-1/type-2**:群交模式下 NPC 自主行为的两个 AI 生成入口——type-1 为"全员/只自慰"策略,type-2 为普通群交主动行为策略。多条规则按这两个入口分别约束。
- **点击级释放门(per-click orgasm chain gate)**:同一玩家动作窗口内,已**实际高潮释放**的 NPC 不再生成新的自主行为(普通空闲 AI 与群交 type-1/type-2 入口都拒绝),但被动结算、二段效果、循环完成不受影响;下一次点击重置。成功寸止、时停蓄积、玩家自身高潮不登记。实现:`mod/local_orgasm_chain_gate_fix`(上游拒收后落地为 mod,见 [ADR-0002](docs/adr/0002-orgasm-chain-gate-as-local-mod.md))。
- **窗口末寸止判定(window-end edge judgment)**:寸止(edge)跨级在窗口内静默累计进 `orgasm_edge_count`,窗口结束时每角色至多掷一次成败;失败则当场把全部累计转普通高潮结算。禁用组件 `local_orgasm_settle_edge_fix` 曾以替换 `init_character_behavior` 实现。
- **高潮批(orgasm batch)**:一次结算里同一角色的全部高潮事件视为一个原子批——**效果全结算、显示只取代表**(每部位只显示最强;代表部位 ≤3,其余按强度分组汇总一行;人力发电——罗德岛动力系统的发电量——提示聚合为一条)。力竭中断必须排在批完成之后。载体组件 `local_h_orgasm_batch_fix` 当前禁用,重新启用前见 [ADR-0003](docs/adr/0003-orgasm-batch-effect-display-separation.md) 的维护注意项。
- **完全催眠(complete hypnosis)**:素质 73 存在或催眠度 ≥200;群交催眠增强的门槛是 ≥2 名完全催眠参与者,**不**额外要求 `unconscious_h` 激活。
- **群交上下文参与者(group context participants)**:群交模板成员 + 当前场景 H 状态角色的统一资格集合;不同准入路径(发起 H / 被邀请加入)按同一条 eligibility 规则计数,不区别对待。
- **目击者已处理标记**:`sp_flag.see_pl_h` 表示该角色已对玩家当前地点的隐奸/群交完成过发现处理;玩家移动前不再重复入选发现者,移动重置后恢复资格。
- **pain_as_pleasure 域**:该 flag 是催眠授予的永久标记,但只在催眠 unconscious 状态(`unconscious_h ∈ {4,5,6,7}`)激活时把正向直接痛苦转为心理快感;域外休眠不清除,仅催眠解除时移除。
- **地文所属角色**:paper-doll 文本(如 `{move}`)必须用被绘制角色本人的 id 和场景上下文格式化;历史 bug 是硬编码 character_id=0 导致 NPC 移动地文冠以玩家主语。
- **结构化房间地址**:存档中形如路径的房间字段(`scene_path`、宿舍、空气催眠位等**枚举**字段)。跨 OS 读档时只对这些字段做分隔符转换,普通文本一律不动。该行为现由上游核心提供(PR #207 已合并),本地不再有对应组件。

## 各启用 mod 一句话契约

- **easy_mode**:催眠随机乘数 5..10;每日理智消耗 ≥50 时 1:1 转理智上限成长(上限 9999);爱情旅馆三档房价 1/2/3 粉票。
- **group_sex_extension**:群交模式三个批量指令——全员寸止、全员戴玩具(身体槽 0-3)、全员催眠增强(对完全催眠者加敏感度+pain_as_pleasure,不改催眠状态本身);单一 mod,不拆分。
- **local_fontfix**:Windows 下用 `AddFontResourceExW`+`FR_PRIVATE` 进程内私有注册 `static/fonts`/`fonts` 下的捆绑字体,免系统安装即可让 Tk 解析更纱黑体。
- **local_orgasm_chain_gate_fix**:见"点击级释放门"。

## Tk 输入与渲染(禁用组件 local_performance 曾覆盖,部分已直接进上游/本地提交)

- **新鲜输入原则**:`askfor_wait()` 布防前后必须排空滞留的点击/回车(order 队列、`w_frame_up`),一次用户输入不能同时推进指令和其后的等待;`w_frame_skip_wait_mouse` 只在显式调用点(如 `LineFeedWaitDraw`)生效,全局 wait 不因它跳过。
- **渲染合并**:队列渲染期间的多次 `see_end()` 合并为排空后一次。
