# Fable 5 架构方向审阅记录

状态：该重构已暂缓。本记录只支持架构方向，不代表源码验证、运行时 parity、implementation-ready 或 live-cutover approval。

## 调用

```text
claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence
```

输入为最终 RFC 与可行性说明全文；工具与会话持久化均禁用。要求 Fable 只判断 maintainer 是否应给予方向批准，不得把尚未执行的 Phase 0 当成方向拒绝理由。

## 最终 verdict

`ACCEPT`

Fable 的总评：

> The documents now make a technically sound, maintainer-persuasive case for direction approval. Internal consistency is good; I found no contradiction that makes the direction unsafe.

它明确认可：

- 时间序玩家可见 fact 与 snapshot UI/输入/等待的职责边界；
- 封闭 fact union 和 `publish(fact)` 最小 interface；
- sequence 只约束进程内接受/adapter 调用，single dispatch 不冒充网络 exactly-once；
- StatusChange 在 publish 前固化视角、目标、draw settings 与名称/style；
- `(producer, sink)` 的 LEGACY/SHADOW/CUTOVER matrix、单 writer 和静止点切换；
- 首刀选择 settlement narration → `web_instruct_texts`，同时保持 `realtime_text` 等其他 sink 为 legacy；
- current-behavior freeze，包括 2 秒/5 秒状态浮字、target-switch timestamp、reconnect、time-stop 和浏览器去重；
- Phase 0 blocker 与方向批准分离。

Fable 保留的 Phase 0 条件：

1. 可重复的 Tk enqueue/dequeue/wait 与 Web append/buffer/emit/browser trace。
2. 闭合的 producer/sink/clear/Socket inventory。
3. settlement-modal description 的显式来源或精确 compatibility 证明。
4. payload 字段/事件 capture 和动态字段归一化规则。
5. Phase 0 关闭 blocker 后另行申请 live-cutover approval。

## 聚焦追问

第一次追问在工具禁用时只产生 Bash 检查意图，没有 verdict，因此作废。使用相同模型参数并明确 text-only 后，有效 verdict 为 `KEEP`。

Fable 认为：

- 不应为了送审而臆造 bug 事件史；成本收益可在 maintainer 讨论或 Phase 0 用真实清单补强。
- 术语已安排在方向讨论中定稿，早于 Phase 1，无需额外改正文。
- 审阅记录已明确排除源码验证、运行时 parity、实现批准和 live-cutover 批准，没有夸大 `ACCEPT`。
