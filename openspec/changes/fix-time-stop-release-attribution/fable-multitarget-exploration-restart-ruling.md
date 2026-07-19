/investigate-game-bug

你是 erArk “时停解除结算归属”任务的证据监督者。此前你裁定原一 NPC Tk 路线无条件失效，并规定：如果正常多目标路线能在把当前对象切到 B 后保留 NPC A 的正 deferred counts 与 `shoot_position_body`，则改用该路线；如果不能，继续穷尽生产路径，不得拿合成状态冒充正常游戏 bug。

现已取得静态与一次未完成 Tk 探索事实。请从怀疑视角裁定这次基础设施中断能否从原始存档重启探索、下一次怎样保持证据诚实。不要把“路线在代码上可达”自动当成玩家证据已完成。

## 已确认的静态生产路径

- H 主场景仍绘制同场全部 NPC。点 NPC 名字或头像的正常 UI 回调只把 `player.target_character_id` 改为该 NPC 并清输入绑定；它不是游戏行为，不调用 `judge_before_pl_behavior()`，不推进时间。
- 下一条真实行为开始时，`judge_before_pl_behavior()` 只清**当前对象 B**的射精位置，从不清旧对象 A，也不清任何 `time_stop_orgasm_count`。
- `[4115]` 的 `IS_H` 在玩家自身仍处于 H 时成立，当前对象 B 不必处于 H。
- 只读真实 premise 探针把 A 设为 `counts={0:2,21:3}, shoot=2` 后，通过同一正常目标回调切到 B；A 两字段原样保留，`[4115]` 所有前提为真。按真实前置清理语句投影，只有 B 的射精位置被清。
- 正常来源存档 `save/8` 在哥伦比亚咖啡馆同场已有博士、可露希尔 A、凯尔希、惊蛰 B、林；玩家射精槽为 0，具有时停能力，时停初始关闭。存档未手改。

## 未完成探索的精确事实

- Baseline ref 为 `06fc59c1e71d092224375fc4a096b956aea2ad63`，`default.py` hash 为 `ecdec42...`。固定 seed `5270714`、`PYTHONHASHSEED=0`，只读多目标 observer 两侧拟保持字节一致。
- 来源 `save/8` 被机械复制到 baseline runtime 的空槽 5；来源与副本 head/data hash 在运行前后均为 `a91afea...` / `45e77cfe...`。
- 逐帧物理输入仅到：读槽 5 → `[4113]` 开时停 → `[5052]` 无意识奸 → Return → 第一次 `[6602]` 口交。
- 最后全分辨率帧只显示第一次口交已被接受、正在输出前提/数值。尚未滚动、Return、看到射精判断、切换惊蛰、点击 `[4115]` 或取得 oral 后 observer 状态。
- 在 session 运行 491 秒时，X display 被外部 SIGTERM 消失，supervised cell exit 143。tee 日志只有一次预期 `zoomed` fallback 与正常初始化；没有 traceback、Exception、TclError、observer 行或游戏侧错误。
- 执行者遵守“异常即停”，没有重启。没有保存游戏，来源与所有副本字节未变；没有看到任何成功/失败触发结果可供挑选。

## 拟议的防重复中断方法

不是由视觉 agent 自己持有长阻塞 shell，而是主协调者用 allocator 启动一个最长 1800 秒、可 yield/resume 的 supervised cell；视觉 agent 只做逐帧查看和单步输入。若一个视觉 agent turn 到时，游戏与 allocator 仍由主 cell 持有，再以新 turn 从当前已截图页面继续。仍禁止盲点、批量坐标或跨帧假设。

重启仍从字节相同的原始 `save/8`、相同 seed/ref/launcher 开始；本次不把第一次中断前的游戏进度接入新运行。新探索只回答 A→B 路线能否真实产生并保留判别状态；它仍不是正式 baseline/candidate A/B。只有路线与 observer 成功后，才另行预注册正式 A/B。

## 请裁定

1. `RESTART EXPLORATION PASS` 或 `STOP/REVISE`。这次是否属于结果出现前的外部基础设施中断，因而从原始存档重启不会构成挑轮？
2. 主协调者持有长生命周期 allocator、视觉 agent 分段逐帧操作是否合格？还必须加入什么停止条件？
3. 若重启探索成功，什么最小事实足以把新路线交给你做正式 A/B 路线审核：是否至少需要切换前后两次 observer、可见 B 成为当前对象、`[4115]` 仍可见、以及 baseline 结算页？
4. 当前是否需要玩家介入？这里没有拟议玩法改动，只是在证明现有 UI 路径。

## Fable verdict（逐字保存）

## 裁定

### 1. RESTART EXPLORATION PASS

这次中断符合"结果出现前的外部基础设施中断"的全部要件：外部 SIGTERM、exit 143、无游戏侧异常、无任何成功/失败触发结果被观察到、来源与副本字节未变、执行者未重启未保存。挑轮的定义是"看到不利结果后丢弃该轮"——这里没有可供丢弃的结果，因此从字节相同的 `save/8` 重启不构成挑轮。

条件：把本次中断作为 attempt #1 写入 runtime manifest（时刻、SIGTERM 来源不明、最后已归档帧的 hash）。从下一轮起，**任何显示出判别性结果（无论方向）的轮次必须报告并计入**，不得再以任何理由丢弃已出结果的轮。

### 2. 拟议方法合格，需补四条停止条件

主协调者持有 allocator supervised cell、视觉 agent 分段逐帧操作，符合技能中"一个 supervised command 持有 slot 全生命周期"的模型，且消除了视觉 agent turn 超时导致的进程连带死亡。合格。必须补充：

1. **续接一致性检查**：每个新视觉 agent turn 的第一个动作必须是重新截图并与上一 turn 最后归档帧比对；不一致则停止并重新评估，禁止基于假设状态输入。
2. **中断即整轮作废**：若 display/游戏进程再次死亡，该轮作废，从原始存档重开新轮；禁止在同一 cell 内原地重启游戏续跑。
3. **基础设施升级阈值**：在重启前先做一次快速排查（session 超时、OOM、tmux/allocator 清理）定位 491 秒 SIGTERM 的来源；若不明原因中断累计达 2 次，停止消耗轮次，转为基础设施调查，不得靠反复重试碰运气。
4. **1800 秒预算内的中途保存点禁止**：探索轮内不得使用游戏内保存来"续进度"——每轮从 `save/8` 完整重走。

### 3. 路线交付正式 A/B 审核的最小事实

必需（缺一不收）：

- **切换前 observer 快照**：oral 射精结算后、切换前，A 的 `time_stop_orgasm_count` 为正且 `shoot_position_body` 已置位，带帧证据与 observer 输出对应；
- **切换后 observer 快照**：同一轮内切到惊蛰后，A 两字段原样保留、仅 B 的射精位置按预测被清；
- **可见 B 成为当前对象的帧**（正常 UI 回调路径，非任何注入）；
- **该状态下 `[4115]` 仍可见/可点的帧**。

**baseline 结算页不是探索交付的必需项**。探索轮只回答"路线能否真实产生并保留判别状态"；结算页归属正式预注册 A/B 的 baseline 侧。若探索中自然走到结算页，归档为诊断材料，不得作为 baseline 证据引用——否则探索轮就变成了未注册的 baseline 运行。

另需随附：完整逐帧动作日志、seed/`PYTHONHASHSEED`/ref/overlay hash、来源与副本存档 hash 前后一致的记录。

### 4. 不需要玩家介入

无玩法语义改动，只是证明现有 UI 路径的可达性与状态保留。按停止规则，继续执行下一轮探索。
