# 玩家可见信息重构可行性记录

状态：**已暂缓（2026-07-14）**。架构方向静态可行并获 Fable 5 `ACCEPT`，但用户判断短期收益不足；Phase 0、运行时验证和实现均未开始。

## 判定

- 架构方向：可行。
- `publish(fact)` + active-renderer adapter：可行。
- 逐 `(producer, sink)` migration：可行。
- 当前优先级：暂缓。
- implementation-ready：否。
- live-cutover approval：否。

## 静态可行性依据

1. 口上/地文、事件正文和结算状态都有高价值集中 producer，可以在最终文本与角色/目标语义仍可取得的位置构造 fact。
2. Tk draw/IO 与 Web buffers/Socket 已经是两个真实 renderer implementation，adapter seam 不是为抽象而抽象。
3. 所有核心依赖在同一 Python 进程，不需要数据库、队列、event store、客户端 ack、插件 registry 或新协议。
4. 第一条 live sink 可以选生命周期较清楚的 settlement narration → Web instruct history，而不是先碰墙钟过滤和输入等待。

## Live cutover 前阻断项

### A. 没有可信现状顺序基线

静态调用图不能证明 Tk 实际 dequeue/render 与 Web 多个 Socket/payload 的浏览器到达顺序。Phase 0 必须产出可重复的双端 trace。

### B. Settlement modal 隐式文本来源

现有 settlement description 可能取自 `web_other_texts` 在 update 前保存的最后一段。迁移 other-text 路径前必须建立显式 owner，或证明 compatibility path 精确保持该依赖。

### C. Scope inventory 尚未闭合

必须继续清点 `new_ui_container`、polling fallback、浏览器内容去重、Socket-only modal、快捷用药等状态直写点和 runtime adapter 安装顺序。旧报告中的“静态消费图已闭合”结论已撤回。

## 关键风险控制

- 双写 → 每个 `(producer, sink)` cell 只有一个 writer。
- shadow 偷走消息 → recording 只从 producer 侧观察，不调用破坏性 consumer。
- 时停重排 → sequence 使用进程内单调整数，game time 只作属性。
- 网络保证被夸大 → single dispatch 不等于多 sink 原子或浏览器 exactly-once。
- wait 回归 → wait ownership 排除，只验证邻接顺序。
- 一般提示吞掉整个 UI → 只迁移明确 producer，不全局捕获 draw。
- 状态显示资格漂移 → publish 前固化 subject/target、视角、draw settings 和名称/style。
- 迁移 framework 永久化 → 最终删除 route/shadow。
- mod 需求扩大范围 → clean upstream、mods disabled；不提供兼容合同。

## 证据计划

真实 Tk 至少覆盖口上/地文、结算叙述、rich text、重复文本、normal/line wait、事件和时停邻接路径。真实 Web 至少覆盖 history、main/minor dialog、状态浮字、event/settlement modal、主/子面板 clear、reconnect 和 polling fallback。

自动 trace 必须同时记录 producer fact 数和各 sink/浏览器可见数，以免把当前客户端去重或状态浮字过滤误判成新丢失。所有动态字段都需要书面归一化规则。

## 审阅结论

Fable 5 第一轮为 `REVISE`，要求补清 runtime order、settlement modal dependency、状态浮字有损规则、重连、时停和 mod 决策。用户完成决策并修订后，第二轮对最终 RFC 给出 `ACCEPT`，仅支持方向批准。聚焦追问为 `KEEP`：成本收益事件史应在 maintainer 讨论或 Phase 0 用真实证据补强；术语在方向讨论中定稿，早于 Phase 1。

fresh-context reviewer 也确认 adapter ownership、single-dispatch、route matrix/quiet point、StatusChange visibility snapshot、quick-medicine inventory 和 parent-event delayed consumption 的文档阻断项已经关闭。

## 恢复条件

只有用户重新判断收益值得投入，或频繁出现跨 Tk/Web 难定位的显示/顺序问题时再恢复。恢复后先刷新源码事实与 maintainer 方向，不直接实施；最多先做 Phase 0。Phase 0 不能关闭 A–C 时继续停止。
