---
timestamp: 2026-07-19
---
# 结算管线与变更累积

系统级流程与通用结算函数在 [`结算系统`](../../.github/prompts/数据处理工作流/结算系统.md)、[`通用结算函数函数`](../../.github/prompts/数据处理工作流/通用结算函数函数.md) 里已有;本页只记跨模块契约、归属不变量和几个不读代码看不出的坑。

## 触发与分段

行为结束由主循环两处调用 `settle_behavior.handle_settle_behavior(character_id, end_time, event_flag)`(`Script/Design/character_behavior.py:230`、`:247`)。`event_flag`:`0` 只结算事件、`1` 只结算指令、`2` 两者都结算(`settle_behavior.py:26`)。指令段进 `handle_instruct_data`(`settle_behavior.py:380`):先跑口上 `talk.handle_talk`,再按 `config_behavior_effect_data[behavior_id]` 逐个触发 effect 函数(`:404`),`"CVE"` 前缀字符串走综合数值结算(`:407`),随后二段结算 `second_behavior.check_second_effect`(`:426`)与额外经验(`:428`)。

## 归属不变量:变更记在谁头上

一次结算只有一个"自己" `change_data: CharacterStatusChange`,交互对象的变更挂在 `change_data.target_change[target_id]: TargetChange`(结构体见 `Script/Core/game_type.py:1833`/`:1861`;`TargetChange` 无 language/knowledge,是 `CharacterStatusChange` 的子集)。综合数值结算 `handle_comprehensive_value_effect` 用主体前缀选落点:`A1` 自己→`change_data`,`A2` 交互对象→`change_data.target_change[target_id]`,`A3|adv` 指定角色(`settle_behavior.py:723-735`)。**不变量:结算对象与被结算角色一致**——写谁的属性,就把增量记进谁对应的那个结构体,否则玩家信息区与对象信息区会串栏。

**归属反转坑(exchange_flag)**:NPC 主动对玩家(`character_id != 0 且 target == 0`)时,`settle_behavior.py:122-132` 把 NPC 的 `change_data` 塞进 `target_change[0].target_change[character_id]`,再对调 `change_data`↔`target_change`、`now_character_data`↔`target_data`,并把 `character_id` 强制为 `0`。之后的显示段一律以"玩家为主视角"渲染,`exchange_flag` 为真时跳过自身状态输出(`:184`)、只走对象分支。改这段显示逻辑时,`character_id` 在中途被改写为 0 是必须记住的前提。

## 异地/远端角色的输出抑制

两道独立的在场判定,别混为一谈:

1. **显示段早退**(`settle_behavior.py:119-120`):`character_id != 0 且 NPC 位置 != 玩家位置` 时 `return`。注意此时 `handle_instruct_data` 已跑完——**数值已落库,只是整段文本/面板不输出**。异地 NPC 的属性照常变化,玩家看不到而已。
2. **二段效果在场门**(`second_behavior.second_behavior_effect`,`Script/Design/second_behavior.py:128-134`):`NPC 位置 != 玩家位置 且 behavior.move_src != 玩家位置` 时,不做常规二段显示结算,改走 `talk.must_show_talk_check` + `must_settle_check` 两条抑制通道后 `return`。`move_src` 让"本回合刚从玩家场景离开"的角色仍算在场,避免离场瞬间丢结算。

### must-show / must-settle 两条通道

二段行为的 effect 表里含 `997` → 该行为登记为"必须结算",含 `998` → "必须显示"(列表在 `Script/Config/game_config.py:857`/`:860` 构建为 `config_behavior_must_settle_cid_list`/`config_behavior_must_show_cid_list`)。角色获得二段行为时 `character_get_second_behavior`(`second_behavior.py:16`)据此把行为 id 追加进角色的 `must_settle_second_behavior_id_list` / `must_show_second_behavior_id_list`(定义 `game_type.py:1536`/`:1538`,读档迁移 `old_chara_to_new.py:724`),`reset=True` 时反向移除。消费点:
- `must_show_talk_check`(`Script/Design/talk.py:393`):异地也**必须画出口上文本**,但 effect 用一次性丢弃的局部 `change_data` 触发——**数值静默结算、不进玩家可见的增量栏**,处理完清空列表。
- `must_settle_check`(`second_behavior.py:167`):**完全静默**,只触发 effect(局部 `change_data` 丢弃),不出任何文本,处理完清空列表。

即"必须让玩家知道发生了"(如妊娠/初见类)的走 must-show 保文本;"数值必须推进但玩家不必看"的走 must-settle 纯静默。异地不同地图的角色靠这两条通道保证状态机不因玩家不在场而漏结算(修复 `97c35826e`:此前分组遍历带 `second_behavior_list` 时不进该门,导致异地的高潮/刻印分批结算被整体跳过)。

## 二段结算的排队与消费

`character_get_second_behavior` 只把 `second_behavior[id]` 置 1 入队,不当场执行;真正消费在 `second_behavior_effect`(`second_behavior.py:141-165`)遍历、触发口上与 effect 后逐个归零。高潮(`orgasm_*`)、刻印(`mark_*`)在 `check_second_effect` 里用 `second_behavior_list` 子集**分组单独遍历**(`second_behavior.py:99-106`),因为它们由 `orgasm_judge`/`mark_effect` 在同一函数内动态入队,须在入队后立刻各自 flush。玩家对 NPC 的行为额外对交互对象补一轮二段结算并挂进对方 `TargetChange`(`settle_behavior.py:431-442`)。高潮批"效果全结算、显示只取代表"的原子性契约见 [ADR-0003](../adr/0003-orgasm-batch-effect-display-separation.md),不在此展开。
