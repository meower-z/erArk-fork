`PASS`

## 文档裁决

四类陈述分离干净，无过度声明。我逐项核对了主张与一手证据：

**运行事实（正记录）**：日志 `seed-00-state-machine-diagnostic.log`（SHA-256 与文档一致，e4587c…）确实以正向记录给出 `state_machine_dispatch_trace`（56/4080 均 `default9`/状态机2/`wait`/flag3，target91 三前提中 `masturebate_flag_3` 记为 `"MISSING"` 而非补算）和 `effect_dispatch_trace`（56/4080 均 `[9999]`，无 418/524）；六个 rng_hash 检查点、11:52→11:57、target 恒 3、V 803→840/5379→5416 全部在日志中。符合先前 Fable 门禁 2（不得由沉默推断）。

**已撤回模型**：v-reachability 文档开头即声明算术模型已被运行反证、"Do not use"，保留的两次结算计算明确标注为条件假设。分离正确。

**静态条件路径**（逐条对码核实）：
- normal-1 门只认 flag1/2 或逆推 flag，不认 flag3 —— `handle_premise/__init__.py:927` → `handle_premise_sp_flag.py:1444`，与 type-12 搜索入口 `handle_npc_ai.py:269` 一致；
- 群交 type-1 写 flag3、改 `SHARE_BLANKLY`、不清逆推 flag —— `handle_npc_ai_in_h.py:580-586`；
- target86 前提 `normal_1267|desire_point_ge_100|sexual_ignorance_0|not_ask_not_masturbation`、SM91；target87-90 要 flag1/2；target91 要 `group_sex_mode_on|place_0|masturebate_flag_3`、SM92 —— `data/target/default/target.csv` 逐字一致；
- SM91 按 fall 等级随机（fall≥4:50%、3:20%、2:5%、≤1:0%）设 `npc_masturebate_for_player=True` 且该分支不改写 flag3 —— `Script/StateMachine/default.py:1994-2007`；
- SM92 → behavior 418 —— `default.py:2015-2026`；418 效果表含 456/458/524 —— `Behavior_Effect.csv:207`；
- 三个逆推 flag 清零点确如文档归类：H 状态整体重置（离开路线）、独立结算效果、移动等待超时（同场景路线不触发）—— `Settle/default.py:4177/5766`、`character_move.py:164`。

诊断文档结尾"falsifiable entry condition, not a concrete player route"与任务 3.2 的 blocker 措辞把静态路径和未知 N 分离到位。无需修改。

## 唯一下一步：C（比 A 更窄）

**只读取存档 99 中九名 B 候选的路线门控属性，不建任何欲望增长模型**：每人的 fall 等级（换算 SM91 的 activate_rate）、性无知天赋、`ask_not_masturbation` 与 `ask_not_active_h_for_player` 禁止项、当前 `desire_point` 现值。一个离线读存档脚本即可，不进游戏循环、不跑 seed、不算调度。

选 C 而非 A 的理由：A 的后半段（"每次 6001 的确定欲望变化"与"首次可满足时点"）又是一个静态调度算术模型——上一个这种模型刚被 seed-0 运行推翻。在为它付成本之前，先用一次无模型的纯读取判定路线是否在源头就死了。

**成败分别证明什么**：
- **失败侧（决定性冻结）**：若九名 B 无人同时满足 fall≥2、非性无知、两项禁止均未设——则 activate_rate 对所有人恒为 0，SM91 永远走 else 分支，逆推 flag 在存档 99 上不可能被设，target91→418→524 入口静态不可达。target-scope 候选就地冻结为代码级 bug，任务 3.2 的 Tk blocker 转为永久性证据结论（即选项 B），不再做任何路线工作。
- **成功侧（路线存活但仍非玩家路线）**：若至少一名 B 通过全部门控，则路线存活，且把 A 的欲望算术收窄到仅这几名合格者；届时 A 的成功标准是产出有界的最早等待数 N_min 加每次 pass 的已知分支概率，之后才允许设计一次受控 seed 路线。成功侧不解除 3.2 blocker，也不授权 seed 扫描。
