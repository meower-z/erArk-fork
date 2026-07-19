# 项目 Wiki 索引

机制快照:描述 HEAD 现状的跨模块契约、不变量与坑。改动落地后按 `/project-wiki` 的 fold 纪律重写受影响页面。词汇定义在 [CONTEXT.md](../../CONTEXT.md),决策理由在 [docs/adr/](../adr/),上游系统流程在 `.github/prompts/数据处理工作流/`。

- [玩家动作窗口与 NPC 调度](player-action-window.md) — 窗口边界=最外层 `game_update_flow`;NPC 追赶;时停回滚;调度器独占提交;漏加 `over_behavior_character` 会挂起主循环
- [结算管线与变更累积](settlement-pipeline.md) — change_data/TargetChange 归属不变量;exchange_flag 中途把 character_id 改写为 0;异地抑制的 must-show/must-settle 两条通道
- [H/群交状态机与发现不变量](h-group-state.md) — is_h/群交全局标记/模板三者独立;see_pl_h 等三个标记的"发现者反应恰好结算一次"契约
- [高潮与寸止结算](orgasm-edge-settlement.md) — 一次调用=一个原子批;寸止一次共同判定;时停/寸止硬互斥;效果 526/527 分工;多重绝顶唯一产出点
- [Tk/Web 输入与等待契约](tk-web-io-contract.md) — 三个输入标志的唯一所有者;渲染期门禁的 after_idle 时序;Web 输入全局变量缺口
- [mod 组件系统与本地组件现状](mod-system.md) — mod_config.json 是运行时唯一事实;replace 型 mod 再启用会回退上游改动;deprecated 不被扫描
- [数据构建链与验收](data-build-chain.md) — 增量构建何时不够;PO 保护与字节对比法;buildata.py 不在构建链上
- [存档兼容契约](save-compat.md) — 重建+覆盖式迁移;删字段留幽灵属性;序列化但必须边界重置的自愈式标记
