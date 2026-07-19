## Why

口上、地文、提示、事件文本和状态变化目前分别选择 Tk/Web 输出路径；Web 内部又有历史、实时消息、对话框、弹窗和状态浮字等多套写入与清空时机，因此同一玩家可见事实的归属和相对顺序缺少单一负责人。现在记录该方向是为了在 session 结束前保留完整设计；用户已判断短期收益不足，本 change **暂缓，不得进入 Phase 0 或实现**。

## What Changes

- 未来建立只负责“按发生顺序交给玩家的信息”的 deep module，生产者统一提交类型化 fact。
- 由 module 固化可变输入并分配进程内单调 sequence；Tk/Web 只启用当前 renderer adapter。
- Tk/Web adapters 继续投影到现有路径，保持当前 Tk 表现、Web payload/Socket/clear、状态浮字过滤、重连和时停行为。
- 面板、布局、按钮、输入、等待、flush 和 clear 继续由现有 UI/flow owner 管理。
- 未来先做只读 Phase 0 证据与 shadow 对比，再按 `(producer, sink)` 逐项切换和回滚。
- **BREAKING**：若未来实施，不保留现有 mod patch points、shim、弃用窗口或扩展 registry；验收以 clean upstream、mods disabled 为准。
- **HOLD**：当前只持久化提案和审阅证据，不授权 OpenSpec apply、生产代码修改、测试、PR 或 maintainer 外发。

## Capabilities

### New Capabilities

- `player-visible-information-flow`: 定义时间序玩家可见事实、进程内顺序、active-renderer 投影边界、当前行为兼容约束及可回滚迁移门。

### Modified Capabilities

无。

## Impact

未来可能影响 `Script/Design/talk.py`、`Script/Design/settle_behavior.py`、事件文本面板、Tk draw/IO 路径，以及 `Script/Core/io_web.py`、`Script/Core/web_server.py` 和 `Script/System/Web_Draw_System/` 下的 Web compatibility 路径。当前 change 不增加依赖、不改变代码或运行行为；详细证据、接口和迁移设计见本 change 的 `design.md` 与附件。
