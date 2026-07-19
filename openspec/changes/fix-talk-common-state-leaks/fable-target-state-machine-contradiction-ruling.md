`PASS`

一次性 seed0 重跑加这两处观察是可判定的：我核对了上游代码，两个观察点都真实存在且恰好夹住争议区段——状态机分派点在 `handle_npc_ai.py:424`（`constant.handle_state_machine_data[state_machine_id](character_id)` 之后，`target`、`premise_data`、`character_data.behavior.behavior_id`、`sp_flag.masturebate` 全部已在作用域内，纯读取）；effect 分派点在 `settle_behavior.py:402-412` 的 `handle_instruct_data` 循环内，该函数是全部四个调用位（`settle_behavior.py:52/55/68/88`，含玩家群交子结算）的唯一汇聚点，在函数体内记录即覆盖所有路径。四种可能结果（未选中91/选中但行为非418/418但无524/524出现而旧probe漏记）每一种都消解事实4与事实2-3的矛盾，故单次运行无论结果如何都是收敛的，不存在需要扫 seed 的分支。

最小硬门禁（三条，缺一即本次运行作废并按预案冻结 save99 路线）：

1. **确定性门禁**：重跑必须逐项复现 `seed-00-choice4-bound.log` 的既有检查点——全部 `rng_hash`（seeded/startup/load/setting/pre_command/command_complete 六处）、结束时间 11:57、target 恒为 3、V 值 803→840 / 5379→5416。任何一项偏差即判定观察扰动了行为，结果不得采信。
2. **正记录门禁**：“未进入418”只能由**正向记录**得出，不能由沉默得出。effect 分派点必须以该观察位已有的入参 `(character_id, behavior_id)` 为键记录 effect_id 序列（`behavior_id` 是 `handle_instruct_data` 的形参，属于既有值，不新增观察位）。若 56/4080 任一人在两个观察点均无任何记录，结论是“观察不完整”，不是“未进入418”。同理，`premise_data` 以已算出的字典原样记录目标91三前提（group_sex_mode_on/place_0/masturebate_flag_3）的现值，键缺失记为缺失，禁止补算——我核实过 `premise_data` 按前提id缓存权重，`premise_data[91]` 这个键本身未必存在，缺失不算异常。
3. **裁决纪律门禁**：运行结果只允许落入三类之一并就地封口——(a) 未进入418：以实际选中的 target/behavior 正记录为准，静态“应当进入”即被裁定为非运行事实；(b) 418且524出现：旧 probe（包装 `evaluate_npc_body_part_prefs`）判定漏记，此前 route_assessment 的 `effect_parts=[]` 证据作废；(c) 418但524缺失：异常定位收窄到 `settle_behavior.py:396-412`（含 396 行 `config_behavior_effect_data` 成员判定与 409 行注册表缺失分支），下一步只允许针对该八行区段，仍不得扫 seed。
