/investigate-game-bug

请作为怀疑性的最终设计裁决者，审查 erArk OpenSpec `add-per-click-orgasm-chain-gate` 在当前 upstream/master 72e28051e（已包含 #216 深度恢复）上的实施边界。不要因为旧 Fable medium 文档已经 PASS 就默认接受；必须重新读当前源码、OpenSpec、红灯测试和新版评分 skill。可以否决或要求改 scope。

权威文件：
- /home/ubuntu/games/erArk/openspec/changes/add-per-click-orgasm-chain-gate/{proposal.md,design.md,tasks.md,specs/per-click-orgasm-chain-gate/spec.md,fable-supervision.md}
- 当前干净候选工作树（尚无生产改动）：/home/ubuntu/games/erArk-pr-per-click-orgasm-chain-gate
- 红灯测试：该工作树 tests/test_per_click_orgasm_chain_gate.py
- 当前生产源码：Script/Design/update.py、second_behavior.py、handle_npc_ai.py、handle_npc_ai_in_h.py、character_behavior.py

玩家已确认玩法：一次最外层玩家点击内，NPC 第一次实际高潮释放事务完整结束后，不再生成新的自主行为；仍接受刺激、被动高潮和全部结算；下一点击立即恢复。不是冷却/眩晕。玩家、成功寸止、时停只蓄积不登记。

当前红灯实跑：5 failed, 4 passed。失败分别证明：
1. 真实 orgasm_settle 多部位+plural 完整形成后没有登记；
2. 两个连续 nested game_update_flow 共享观察虽可模拟，但最外层正常返回不清集合；
3. nested 异常被外层捕获时登记应保留，但 outer 异常后不清集合；
4. 已登记 NPC 的真实 find_character_target 仍进入第一次 search_target；
5. 已登记群交 NPC 的真实 npc_ai_in_group_sex 仍把 masturebate 从0写成3。
已通过的反向保护：玩家实际高潮、时停蓄积、成功寸止不登记；空闲拒绝后 SHARE_BLANKLY caller 仍会调用 judge_character_status 并进入完成集合。

拟议最小边界 A：
- update.py 模块私有 `_npc_orgasm_release_set`，不进入 Cache/存档；两个有中文契约的窄操作 `register_npc_orgasm_release(character_id)` 与 `is_npc_orgasm_release_registered(character_id)`。
- game_update_flow 已有 caller_depth。caller_depth==0 时入口清空，finally 恢复深度后再次清空；nested 不清。
- second_behavior.orgasm_settle 现有函数最末尾，在 plural/派生/发电等全部路径完成后，若 part_count>=1 且 character_id!=0，调用登记。时停和成功寸止 continue，使 part_count保持0；寸止失败/时停解放进入普通释放后登记。
- handle_npc_ai.find_character_target 最开头查询；命中则加入 over_behavior_character 并 return。character_behavior 现有 caller 随后仍执行 judge_character_status、realtime、persistent、interrupt、time-over、talent tail。
- handle_npc_ai_in_h.npc_ai_in_group_sex 把现有 `if character_id == 0` 扩为玩家或已登记即 return；该函数是 type-1/type-2 共用入口，阻止 masturbation/template 写入。之后 character_behavior 到 find gate，保持 SHARE_BLANKLY 被动结算。
- 不改 dead-code type-3 抢占函数（全仓无调用）；不新建 PlayerActionWindow；不加 Cache 字段。

必须中立比较：
B. 把集合放 Cache 并在 save/load 显式排除/重置；接口仍在 update。文件/序列化半径更大，但依赖更显式。
C. 各模块直接读写一个 Cache 集合，少两个函数 docstring，可能 penalty 更低，但生命周期/语义散落。
D. 新建专用 player_action_window 模块/context manager，接口更深但规模更大。
E. 你发现的其他更正确或更低 penalty 边界。

请检查：逻辑 owner；循环完成是否真的安全；登记是否足够晚；failed-edge replay/time-stop release；普通和群交所有生产可达生成入口；type-3 是否真可不管；nested depth和异常；多 cache/test instance；module global 是否会被读档/热重载污染；测试是否过拟合 AST 或还缺关键真实函数/反向场景；T2 候选未来合并的冲突；与 T5/elapsed 完全独立。

新版评分必须按当前 SKILL.md：penalty=(a+b)+S-2U，S 按连续 change group 净新增超过1计算，U 只认严格共享去重。请先判硬门槛，不要为了分数牺牲契约。给出 PASS/REVISE/BLOCKED 和最终选项；若 A 可实施，列出生产前必须补入设计的精确事实、最低充分测试；给可实际落地的降分建议但不写代码/PR文案。若你与旧监督不同，以本轮为最终裁决。
