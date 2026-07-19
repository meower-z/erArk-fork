---
timestamp: 2026-07-19
---
# 高潮与寸止结算

`orgasm_settle()`(`Script/Design/second_behavior.py:371`)是本页所有契约的唯一入口:第二结算阶段把某角色本次积累的三类高潮字典(普通 `normal_orgasm_dict`、额外 `extra_orgasm_dict`、不计数 `un_count_orgasm_dict`)一次性收敛为部位二段行为与状态计数。理解它的关键不在逐部位算法,而在**一次调用 = 一个原子批**这个作用域,以及三条互斥的分流。

## 部位集合与互斥分流

- **射精槽(part 3 / "p")永远不参与高潮/寸止结算**。`supported_orgasm_list` 显式排除 3(`second_behavior.py:397`),主循环也对 `orgasm == 3` 直接 `continue`(`:433`)。任何"高潮部位数""寸止计数"都不含射精。
- 本次调用先算一个总开关 `orgasm_work_flag`(有任一支持部位越过阈值),再据角色状态选一条分流(`second_behavior.py:404-405`):
  - `time_stop_flag`(时停,`handle_unconscious_flag_3`)——**优先级最高**;
  - `orgasm_edge_flag`(寸止,`handle_self_orgasm_edge`)——**仅在非时停时**成立;`orgasm_edge_flag = ... and not time_stop_flag` 是硬互斥,时停期间不做寸止判定;
  - 两者都不成立——普通高潮结算。

## 寸止:一次共同判定(上游 PR #221)

同一次 `orgasm_settle` 内多个部位同时越过阈值时,**只掷一次**寸止成败,不是每部位各掷一次(`second_behavior.py:407-417`,核验区间 368-427)。语义:

1. 先对当前 `orgasm_edge_count` 拷一份**候选快照** `candidate_orgasm_edge_count`,把本次每个越阈部位的 `normal + un_count` 计入候选,并数出 `crossed_part_count`(同时越阈的部位数)。
2. `judge_orgasm_edge_success(character_id, candidate, crossed_part_count)` 只调用一次(`:417`,函数体 `:600-648`)。基础成功阈值 = 玩家寸止技巧(`ability[30]`)×3 减去各部位计数的平方和;多部位同时寸止更难——单部位成功率按 `p ** max(1, crossed_part_count/2)` 取幂换算总失败率(`:635`)。
3. **成功**:每个越阈部位的 climax 计入**持久** `orgasm_edge_count`(`:470-471`),赋予 `{部位}_orgasm_edge` 二段行为并 `continue`,**跳过普通高潮结算**——寸止成功不产生绝顶地文,只累积。
4. **失败**:把已累积的整份 `orgasm_edge_count` 并入本次 `un_count_orgasm_dict` 一起释放,随即 `clear()` 清空计数并置 `orgasm_edge = 2`(解放态),让合并后的计数走下面的普通结算(`:419-427`)。失败=当场原子释放全部累计,不遗留到下一次调用。

`orgasm_edge_count` 只在两处清空:失败合并(上面第 4 点)与显式解放效果 526(下)。

## 计数累积与释放路径

- **寸止计数** `orgasm_edge_count`:成功累积(`:470`),失败合并释放(`:425`),或由**效果 526 `ORGASM_EDGE_RELEASE`**(`constant_effect.py:471`)显式解放——`handle_orgasm_edge_release`(`Script/Settle/default.py:6655-6690`)把交互对象置 `orgasm_edge = 2`,以 `un_count_orgasm_dict = 对象的 orgasm_edge_count` 重入 `orgasm_settle`,再逐 state 清零。
- **时停计数** `time_stop_orgasm_count`:时停分流下,climax 只累进此计数并 `continue`,**不出绝顶**(`:462-466`);解除时停时由**效果 527 `TIME_STOP_ORGASM_RELEASE`**(`constant_effect.py:473`)统一释放——`handle_time_stop_orgasm_release`(`Script/Settle/default.py:6693-6725`)对每个 NPC 置 `time_stop_release`、以 `un_count` 重入结算后清零。

526 与 527 的分工:526 是玩家**显式**解除单个对象寸止;527 是**时停解除**时对全体 NPC 批量释放。527 的结算写入按 NPC 归属——仅当该 NPC 有非零时停计数时才用 `change_data.target_change[chara_id]`(`Script/Settle/default.py:6718-6719`,上游 PR #227 的归属修复),让延迟高潮显示挂到对应 NPC 而非玩家名下。

重入 526/527 时角色已处解放态(`orgasm_edge==2` 或 `time_stop_release==True`),故 `time_stop_flag`/`orgasm_edge_flag` 均为假,累计计数按普通 `un_count` climax 落地;此时若单部位 climax ≥ 3 会触发超强绝顶(`:516-527`)。

## 多重绝顶与点击级释放门

同一次结算中越阈部位数 `part_count ≥ 2` 时赋予 `plural_orgasm_{part_count}` 二段行为并记 `plural_orgasm_set`(`second_behavior.py:547-550`)——这是"多重绝顶"的**唯一**产出点。

`sp_flag.multi_orgasm_this_player_action` 是**点击级释放门**的触发信号,但**树内不预声明该字段、也不读写它**。生产者与消费者都在 `mod/local_orgasm_chain_gate_fix`(当前启用):其 `character_get_second_behavior` wrapper 检测到 `plural_orgasm_*` 释放即用 `setattr` 置标记(`scripts/local_orgasm_chain_gate_fix.py:23`、55 起),两个 AI 生成入口读标记后早退,让已多重绝顶的 NPC 在本次玩家点击剩余结算中不再自主行动。详见 [ADR-0002](../adr/0002-orgasm-chain-gate-as-local-mod.md)。

## 批结算 mod(当前禁用,一句提及)

`local_h_orgasm_batch_fix` / `local_orgasm_settle_edge_fix` 改动的是**显示聚合**与**窗口末寸止判定时机**,当前均禁用;本页描述的是未加这两个 mod 的现行行为。其设计见 [ADR-0003](../adr/0003-orgasm-batch-effect-display-separation.md)。

## 已知未决

时停释放的生命周期语义(零计数仍置 `time_stop_release`、遍历 `cache.npc_id_got` 无快照)见 [.scratch/time-stop-release-lifecycle/spec.md](../../.scratch/time-stop-release-lifecycle/spec.md),此处不展开。
