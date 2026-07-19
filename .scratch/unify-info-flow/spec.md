# 统一玩家可见信息流(unify-info-flow)

迁移自 openspec change `unify-player-visible-information-flow`(原文见 git 历史;删除时 1/37,仅有设计与暂缓记录,**零实现**)。属于大型架构提案,处于暂缓状态。

## 设计要点(已定,未动工)

- 把口上、地文、提示、事件文本、状态变化统一为按发生顺序发布的类型化"玩家可见事实":`publish(fact: InformationFact) -> InformationId`;fact 校验冻结后分配进程内单调序号,游戏时间回拨不改变顺序。
- 迁移期按 producer/sink 三态路由:`LEGACY` → `SHADOW`(双写对账)→ `CUTOVER`;不接管等待、清屏、重连生命周期。
- 现状:`Script/Design/talk.py:340-348` 口上直接写 Web 文本,`Script/Design/settle_behavior.py:368-375` 结算信息直接推送——两类生产者各自为政,是本提案要收敛的对象。

## 状态

暂缓中。恢复前需要用户批准(工程量大、跨 Tk/Web 两端)。恢复时建议用 `/wayfinder` 把 37 项拆成 investigation/task 子 ticket。
