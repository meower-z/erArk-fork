---
timestamp: 2026-07-19
---
# 玩家动作窗口与 NPC 调度

一次最外层玩家点击驱动的完整结算周期，是本仓库多条本地机制的作用域单位（术语见 `CONTEXT.md`）。行为树逐行流程见 [`.github/prompts/数据处理工作流/角色行为系统.md`](../../.github/prompts/数据处理工作流/角色行为系统.md)，本页只记跨模块契约与坑。

## 窗口边界

- 每个玩家指令经 `update.game_update_flow(duration)` 进入：先 `game_time.sub_time_now(add_time)` 步进时间，再 `character_behavior.init_character_behavior()` 结算（`Script/Design/update.py:23-24`）。窗口的收敛判据是 `cache.over_behavior_character` 集合收齐（`character_behavior.py:50` 每次进入清空）。
- **窗口 ≠ 一次 `game_update_flow` 调用**。结算过程会再触发嵌套 `game_update_flow`（如指令内 `handle_instruct.py` 的多处 `game_update_flow(5)`、`character_move.py:63` 的移动）。真正的"最外层点击"由 `cache.game_update_flow_running` 深度计数区分：进入前为 0 才是外层（`update.py:13-18`，默认值 `game_type.py:1788`，读档重置 `save_handle.py:289`）。深度 ≥2 直接 `return`，防止递归死循环（`update.py:13`）——所以窗口最多嵌套两层。

## 结算顺序与 NPC 追赶（catch-up）

- 玩家先结算到 `0 in over_behavior_character` 为止（`character_behavior.py:54-57`），期间 `pl_start_time` / `pl_duration` 锁定为玩家本次行为的起点与时长。
- 随后 NPC 全体以 `pl_start_time` 为共同基准做**追赶**：`while len(over_behavior_character) <= len(id_list)` 反复轮询未收齐的 NPC（`character_behavior.py:69-74`）。单个 NPC 一次行为不足以填满玩家窗口时会被反复重入、连续消费多个自主行为，直到 `judge_character_status_time_over` 判定其终点追上 `now_time`。这是 NPC 在长点击里连做数事的机制来源。
- 收齐条件：`len(over_behavior_character) >= len(id_list) + 1`（玩家 + 全 NPC，`character_behavior.py:86`）才 break。**任何路径若忘记把角色加入该集合，主循环会挂起空转**——这是新增行为分支最常见的坑。
- 跨天结算与睡觉存档由 `new_day_flag` / `pl_sleep_save_flag` 各自守卫，一个窗口内至多触发一次（`character_behavior.py:78-84`）。

## 时停模式的回滚

时停下玩家结算完即 `break`：先把 `pl_duration` 计入成就，再 `game_time.sub_time_now(minute = pl_duration * -1)` 把时间倒回，NPC 追赶段整段跳过（`character_behavior.py:59-62`）。所以时停窗口只推进玩家、不推进游戏钟、NPC 不被调度——任何"每窗口一次"的 NPC 侧机制在此都不会触发。

## 调度器独占提交（不变量）

窗口内的状态结算会被**重入**，因此"改变角色去向"的转换只能由调度器提交，检查函数只返回窄决定、不得就地结算。群交力竭退出是范例：`judge_character_tired_sleep` 只 `return GROUP_SEX_NPC_HP_0_END`（`handle_npc_ai.py:69-72`），由 `run_npc_pre_behavior_checks` 收到后调用 `commit_group_sex_tired_exit` 提交并**跳过其余前置检查**，否则随后的 H 状态检查会把退出行为覆盖为原地等待（`handle_npc_ai.py:115-133`）。退出效果链在 `commit` 内恰好结算一次（`handle_npc_ai.py:150-152`）。若在检查点就地结算，会造成嵌套周期与重复结算。

## 以窗口为作用域的一次性标记

- **玩家移动重置**：玩家行为为 `MOVE` 时，窗口内立即把全体 NPC 的 `sp_flag.see_pl_h` 清零（`character_behavior.py:137-139`），使目击者在玩家换地点后恢复发现资格（见 `CONTEXT.md`"目击者已处理标记"）。
- **点击级释放门**（契约消费者示例）：mod `mod/local_orgasm_chain_gate_fix` 以本窗口为界。它 wrap `game_update_flow`，仅在 `game_update_flow_running == 0`（最外层点击）时把全体 NPC 的 `multi_orgasm_this_player_action` 标记清零，嵌套更新复用同一标记不重置（`scripts/local_orgasm_chain_gate_fix.py:68-77`）。这印证了"窗口边界 = 外层 `game_update_flow` 进入点、而非每次嵌套调用"这一契约（决策见 [ADR-0002](../adr/0002-orgasm-chain-gate-as-local-mod.md)）。任何"每点击一次"的标记都应挂在这个深度为 0 的进入点上重置，并在读档反序列化后视为未置位。
