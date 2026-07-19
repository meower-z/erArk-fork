## Context

**状态：暂缓。** 用户于 2026-07-14 判断该大型重构短期收益不足，不投入 Phase 0 或实现。本 design 负责保存已经完成的架构调查和审阅结论；除非用户以后明确恢复，否则不得据此修改生产代码。

口上、地文、一般提示、事件正文和状态变化都是“游戏刚刚发生、需要按顺序告诉玩家的信息”，但当前没有共同 owner：

- `Script/Design/talk.py` 的口上/地文 producer 同时决定内容、Tk rich-text draw 和 Web instruct history、realtime text、main/minor dialog。
- `Script/Design/settle_behavior.py` 的结算路径同时产生 Tk 结算叙述、Web history 和结构化 `web_value_changes`；快捷用药等路径还会在 `Script/Core/web_server.py` 直接写状态浮字。
- 事件正文会在 `draw_event_text_panel.py` 与 `event_option_panel.py` 之间经过 `pending_event_text`、history、realtime text 和 modal。
- Web 还同时存在 `current_draw_elements`、`web_draw_history`、instruct/other buffers、dialog queues、value changes 和多个 Socket-only modal，各自有不同的发送、清空或破坏性读取时机。
- Tk 的 draw 入队与 `askfor_wait` 相邻，但主线程绘制和 flow 线程等待并不是一个串行 payload。

因此同一事实的类别、相对顺序、多个投影和清空所有权散落在 producer、UI flow、Web buffer 与前端。时停还会回拨 `game_time`，它不能作为稳定显示序号；冻结的 Web payload 也无法承载新的跨 Socket 全序保证。

现有文档经过源码抽查、四种 interface 设计比较、fresh-context 审阅和两轮 Fable 5 讨论。Fable 最终 verdict 为 `ACCEPT`，范围仅限架构方向；聚焦追问为 `KEEP`。这不代表源码独立验证、运行时 parity、implementation-ready 或 live-cutover 批准。

## Goals / Non-Goals

**Goals:**

- 为时间序玩家可见信息建立单一语义 seam。
- 让 producer 只说明发生了什么，不再选择 Tk/Web sink。
- 在同一进程内为已接受 fact 分配不会随游戏时间回退的顺序。
- 让 Tk/Web 差异集中在 renderer-specific adapter，并保持现有玩家可见行为。
- 通过 producer-side shadow、逐 `(producer, sink)` owner matrix 和静止点切换，使未来迁移可验证、可回滚。
- 在任何 live cutover 前先建立真实 Tk/Web baseline、完整 producer/sink/clear inventory 和 payload/Socket capture。

**Non-Goals:**

- 不接管面板、布局、地图、按钮、命令绑定、输入或等待协议。
- 不让核心 module 管理 flush、clear、dialog 推进、modal 生命周期或重连。
- 不设计新版 Web payload，不增加 ack、cursor、可靠 replay 或跨进程持久化。
- 不顺便修复状态浮字 2 秒过滤、5 秒清理、切换目标刷新时间戳或浏览器内容去重。
- 不统一 rich-text spans，不替换 Web runtime draw patching。
- 不兼容现有 mod，不提供 shim、旧 patch point、弃用窗口或 extension registry。
- 暂缓期间不开始 Phase 0、OpenSpec apply、代码、测试、PR 或 maintainer 外发。

## Decisions

### 1. 长期 producer interface 只有 `publish(fact)`

说明性 interface：

```python
publish(fact: InformationFact) -> InformationId
```

第一版 fact union 封闭为：

```text
Talk
Narration
Notice
EventText
StatusChange
```

不使用任意 `dict`、通用 event bus、namespaced kind registry、持久 journal、公开 flush/replay 或 renderer escape hatch。相比 caller-first 多方法、cursor journal 和 extensible facet 方案，这个形状最小，并且足以隔离真实的 Tk/Web seam。

`publish()` 在接受前校验输入，在返回前复制可变数据，随后分配单调 sequence。游戏时间只是 fact 属性，不参与排序。空文本、错误类型或未配置 renderer 必须在分配 sequence 前失败。

### 2. 只承诺进程内 single dispatch

当前运行模式只启用 Tk 或 Web adapter；核心同步调用 active renderer adapter 一次。sequence 只约束进程内接受与 adapter 调用顺序，不新增到 Web payload，也不宣称控制多个 Socket/payload sink 的浏览器到达顺序。

adapter 可能在写入一个 legacy sink 后、写入另一个 sink 前失败，因此本设计不承诺多 sink 原子性、浏览器 exactly-once、安全重试、断线补发或进程恢复。异常只有在实际从 adapter 冒出时才能 fail-fast；若现有 Web helper 会记录并吞掉 Socket 异常，本次保持该错误语义。

### 3. StatusChange 在 publish 前固化视角与可见性

StatusChange 不能只保存一个仍会被修改的 `CharacterStatusChange` 引用。module-owned factory 必须显式接收 settlement context，并固化：

- subject 与相关 target id；
- 当时使用的名称和 style token；
- 不可变 change snapshot；
- elapsed minutes、source behavior 和 game time；
- 玩家/NPC 互换、`PC_information_flag` 结果及本次 draw-setting 可见性判定。

adapter 不得在稍后投影时重新读取可变角色目标或 draw settings 来重新解释同一事实。

### 4. 核心 fact 不认识 renderer vocabulary

核心 fact 禁止包含：

- `text_content`、`instruct_texts`、`other_texts`、`value_changes` 等 Web 字段；
- Socket 事件名、HTML/CSS、`await_input` 或 wait id；
- Tk JSON、draw class、button/panel id；
- clear/history/reconnect 策略；
- mod metadata。

Tk adapter 只负责现有 engine text/style 到 rich-text、draw objects 和 Tk JSON 的映射。Web compatibility adapter 只负责“已迁移 fact 如何写入被 route 指定的 legacy sink”。它不接管整个 `current_draw_elements`、共享 buffer、按钮、wait、图片、panel、flush 或 clear。

### 5. 旧 UI/flow 继续拥有等待和生命周期

以下 owner 不变：

- `WaitDraw` / `LineFeedWaitDraw` 是否等待；
- `askfor_all` / `askfor_wait`；
- event/settlement modal 的选项、按钮和响应；
- panel/layout/input snapshot；
- `web_server` 对 `game_state_update` 的 copy/emit/clear；
- dialog queue 推进、sub-panel clear 和重连处理。

迁移 gate 只验证“内容投影先发生、随后进入同一个等待”的邻接次序，不让新 module 调用 wait。

### 6. 冻结当前 Tk/Web 行为

未来迁移期间必须保持：

- Tk 文本、style、换行、分页、draw 入队顺序和等待邻接次数；
- Web payload 字段、数组顺序、Socket 事件、发送/clear 时机和当前可见结果；
- 状态浮字按角色读取、2 秒筛选、5 秒清理和切换目标刷新 timestamp；
- 当前 best-effort reconnect，不新增 ack/cursor/replay；
- 时停消息显示一次，`game_time` 回拨不撤回消息；
- 浏览器当前按内容去重造成的重复文本抑制。

这些都是 compatibility adapter 和验收 trace 的约束，不反向进入核心 fact。

Web payload freeze 与 Tk behavior freeze 是两份并列的 adapter contract。冻结 Web payload 不会给 Tk 增加 Web 字段、Socket、flush/clear 或其他额外约束；Tk 侧只需保持自己的既有文本、样式、入队和等待邻接行为。

### 7. 迁移期使用可删除的逐 sink route matrix

临时 matrix 以 `(producer, legacy sink)` 为单元，每格只能是：

- `LEGACY`：旧路径是唯一 writer，新 module 最多记录 fact；
- `SHADOW`：旧路径仍是唯一 writer，候选 projection 只能写 recording trace；
- `CUTOVER`：新 adapter 是该 sink 的唯一 writer，旧路径只抑制这一格。

切换只能发生在该 sink 的静止点：上一批 buffer 已按现状 flush/clear，没有正在执行的 producer/adapter 调用，下一条 fact 尚未开始。切换和 rollback 只影响未来 fact，不 replay、不补发、不自动 fallback。

route matrix、recording adapter 和开关都是迁移壳，最终必须删除；长期 public interface 仍只有 `publish(fact)`。

### 8. 第一条 live projection 选择 Web settlement history

在 Phase 0 和 shadow 通过后，首个候选只切换 `settle_behavior` 结算叙述到 `web_instruct_texts` 的 append。`realtime_text`、Tk settlement narrative 和 `web_value_changes` 仍由 legacy writer 负责。

选择它是因为 append/copy/clear 生命周期清楚，不涉及 value-change 墙钟过滤、目标切换或等待。切换点是一轮既有 `game_state_update` 已清空 instruct buffer 之后、下一次 settlement producer 开始之前。

### 9. 父事件保持现有延迟消费

父事件的 Web adapter 只把 EventText fact 映射为现有 `pending_event_text`。`event_option_panel` 继续作为唯一 consumer，把正文和选项标签写 history/`realtime_text` 并发送 modal；不得抑制这些下游写入。

子事件、DIY 事件和无选项事件才由 adapter 直接映射到 dialog/history sink。选项标签属于输入 snapshot，不属于 EventText fact。

### 10. 不建立 mod 兼容合同

未来若实施，验收使用 clean upstream、mods disabled。旧 monkey patch 位置可以作为当前耦合证据，但不约束新 interface，不需要 mod smoke、shim 或迁移窗口。

## Risks / Trade-offs

- **[没有可信 runtime order baseline]** → Phase 0 必须记录 Tk enqueue/dequeue/wait 与 Web producer/buffer/emit/browser render；未解释差异阻塞 live cutover。
- **[settlement modal 隐式依赖 `web_other_texts` tail]** → other-text 相关迁移前必须改成显式 description source，或证明 compatibility projection 精确复现现状。
- **[scope inventory 未闭合]** → Phase 0 必须覆盖快捷用药、`new_ui_container`、polling fallback、内容去重、Socket-only modal 和 runtime adapter 安装顺序。
- **[producer 与 adapter 双写]** → shadow 只记录；每个 matrix cell 永远只有一个 writer。
- **[shadow 偷走破坏性 buffer]** → recording 从 producer 侧旁观，不调用 `_get_value_changes()`、dialog pop 或 history clear。
- **[sequence 被误解为网络全序]** → contract 明确限定为进程内接受与 adapter 调用。
- **[wait 被新 module 接管]** → interface 和架构测试禁止 core import flow/wait；真实 Tk/Web 验证邻接顺序。
- **[一般提示 scope 膨胀]** → 只迁移明确 producer，禁止全局捕获 `NormalDraw`/`WaitDraw` 猜语义。
- **[迁移框架永久留下]** → 最终 phase 必须删除 route/shadow；删除门未满足不得称完成。
- **[no-mod-compat 被误解为可改变 core 行为]** → 仍冻结 clean-upstream 的 runtime adapter 安装顺序和玩家可见基线。
- **[短期成本大于收益]** → 当前保持暂缓；只有用户重新确认价值或频繁跨端缺陷提供足够收益证据时才恢复。

## Migration Plan

### Hold gate

当前停止。恢复前必须有用户明确授权，并重新检查代码与本文之间的漂移。不得从本 change 直接运行 apply。

### Phase 0：方向批准后的证据包

不切生产路径。建立完整 producer/sink/clear/Socket inventory、Tk/Web 双端 trace、payload/Socket capture、动态字段归一化规则，以及 settlement modal description 依赖清单。覆盖口上、地文、重复文本、玩家/NPC 状态、target switch、wait/line wait、事件/结算 modal、主/子面板 clear、reconnect、polling fallback 和时停回拨。

### Phase 1：module skeleton 与 shadow

加入 fact、sequence、recording adapter 和全 LEGACY route matrix。状态结算先做 producer-side tracer；启用/禁用 shadow 时玩家输出必须完全相同。

### Phase 2：首个 Web history sink

只切 settlement narration → `web_instruct_texts`。验证 payload、clear、`realtime_text` 不变和静止点 rollback。

### Phase 3：全部状态 producer

依次切 Tk settlement narrative、结算 Web `value_changes`，再逐项处理快捷用药等 Phase 0 发现的直写 producer。每项必须迁移或由 maintainer 明确判定为范围外。

### Phase 4–6：talk/narration、event text、明确 notices

等待仍由旧 flow 所有。父事件沿用 `pending_event_text` 延迟消费。一般提示只能按明确 producer 清单迁移。

### Phase 7：收口

删除 producer 中已迁移的 Tk/Web 分支、重复 sink 写入、route/shadow 临时设施；每种破坏性读取只留一个 owner。runtime draw patching 是否替换另立 change。

### Rollback

每个 matrix cell 只能在静止点回滚到 LEGACY，且只影响未来 fact；不重放或补发已经发生的输出。

## Open Questions

- module 与领域词汇最终中文/英文命名是什么？方向恢复时由 maintainer 决定，必须早于 Phase 1。
- Phase 0 能否证明多个 sink 的现状顺序和 clear 行为可重复？
- settlement modal description 应改成哪个显式 owner？
- 完整 producer inventory 中还有哪些非结算状态直写点或 Socket-only 路径？
- 实际缺陷频率是否足以支持该大型迁移的成本？当前答案是否定的，因此 change 暂缓。
