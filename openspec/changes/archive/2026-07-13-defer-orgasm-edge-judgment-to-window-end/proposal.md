# 寸止判定延迟至玩家行动窗口末尾

## Why

已完成的 `merge-orgasm-edge-per-action` 把寸止掷骰合并为每玩家行动窗口一次，但掷骰时机在**首个跨级结算**：成功率不反映本窗口后续累积（等待 1 小时与等待 5 分钟承担同一难度的单次掷骰），且窗口中途的失败文本会被随后的自动追时间结算淹没。设计讨论收敛为"判最后一次而非第一次"：窗口内只累积、完全静默，判定延迟到窗口末尾统一执行——失败天然落在控制权交还玩家的边界上，无需另建 hard stop 机制。

## What Changes

- 玩家行动窗口内，寸止跨级不再掷骰、不再绘制任何提示/口上：每次跨级立即将 `climax_count` 累进 `orgasm_edge_count[部位]`，并在窗口缓存中登记该角色待判事件。
- 窗口末尾（`init_character_behavior` 主循环结束后、成就结算与 web 文本录制关闭之前）对每个仍满足寸止前提的待判角色执行**一次** `judge_orgasm_edge_success` 掷骰：此时平方和已含本窗口全部累积，长窗口的单次判定难度随累积量上升。
- 成功：计数保留（已累进），绘制一条成功提示；将本窗口全部跨级部位以顿号内联进黄色“绝顶寸止”标题，不再绘制独立部位列表行，并入队一个代表部位的 `{part}_orgasm_edge` 口上；代表部位按 `climax_count` 最高、平局随机选出。
- 失败：绘制失败提示后**当场释放**全部积攒（复刻 `second_behavior` 失败解放语义：以 `orgasm_edge_count` 作为 `un_count_orgasm_dict` 再调一次 `orgasm_settle`），随后按 `local_group_edge_release_fix` 的清算契约清空 `orgasm_edge_count` 并重置 `h_state.orgasm_edge`，不留残留状态。
- 窗口中途退出 H 的角色（疲劳退出、HP 归零、被发现打断、无意识恢复、群交缩减等）由既有 `local_group_edge_release_fix` 退出路径清算；窗口末尾以 `handle_self_orgasm_edge` 前提检查识别并静默跳过。
- 时停寸止分支（`unconscious_flag_3`）不进入新逻辑，行为不变。
- 实现方式：`local_h_orgasm_batch_fix` 组件整函数接管 `Script.Design.character_behavior.init_character_behavior`（手法同既有 `orgasm_settle`、`find_character_target` 接管），核心文件不改。
- **语义变更（相对 merge-orgasm-edge-per-action）**：掷骰与提示从"首个跨级结算"移至"窗口末尾"；失败释放量从"仅旧积攒"变为"旧积攒 + 本窗口全部累积"；窗口内不再有任何中途提示（含"接近极限"预警）。
- **窗口末尾派生闭包修复**：窗口末尾失败释放发生在该角色本窗口的常规 `check_second_effect`、`extra_exp_settle` 与 `gain_talent` 之后。组件以本次释放变化对象为边界，窄化补跑刻印检测、本次新生成刻印二段与自动素质检查，使释放新满足的刻印/素质状态和输出在当前响应完成，不遗留到下一行动。
- **主动解放重复判定修复**：隐奸中执行“释放快感”（效果 526）会先在目标的 `target_change` 上完成一次多部位绝顶批处理，随后同一个 `target_change` 又进入目标 `check_second_effect` 并无条件调用 `orgasm_judge`，把释放批次刚产生的高额快感重新识别为 p2 绝顶。组件现在以变化对象为作用域记录“本角色的主动解放批次已完成”，目标闭环一次性消费该标记并跳过紧随其后的重复绝顶判定及其消费通道；下一变化对象仍按普通规则判定。
- **新增显示需求**：窗口末尾寸止成功时，不再先绘制独立的“寸止部位：……”白色行；将本窗口全部寸止部位按现有顺序以顿号连接，直接嵌入下方黄色标题，例如“可露希尔阴蒂、阴道、肛肠绝顶寸止”，随后仍只播放一个代表部位口上。
- **新增结算排序需求**：绝顶或失败释放使 NPC 达到疲劳退出条件时，“太累了/无法继续跟随（或提前离场）”提示必须出现在触发它的完整绝顶批次之后，不能先宣告退出再回头显示该角色的绝顶。
- **失败释放派生标题修复**：插桩确认五重绝顶后的“胸部小绝顶”并非第二次 `orgasm_settle` 或旧队列，而是同一批的 `b_orgasm_to_milk` 派生口上被核心宽泛 `"orgasm"` 分支误渲染为胸部小绝顶标题。组件只对喷乳/排尿派生的错误通用标题做精确抑制，保留真实派生口上与效果；回归同时断言单次调用、变化对象身份、三类字典、edge 状态及所有 owned 队列终态。

## Capabilities

### New Capabilities

- 无

### Modified Capabilities

- `h-orgasm-settlement`：修改 `merge-orgasm-edge-per-action` 引入的两条 requirement——"Merge orgasm edge judgment per player action window"的掷骰时机从窗口首个跨级结算改为窗口末尾、掷骰难度含本窗口累积、失败解放在窗口末尾当场执行并清空 edge 状态；"Show one edge prompt and one representative edge talk per window"的提示/口上呈现时机同步移至窗口末尾，代表部位从全窗口跨级部位中选取。

## Impact

- **归档顺序依赖**：本变更的 MODIFIED delta 以 `merge-orgasm-edge-per-action` 的两条 requirement 为基准，需先将该变更归档/同步进主 spec（`openspec/specs/h-orgasm-settlement/spec.md`），本变更方可干净归档。
- 受影响 mod：`mod/local_h_orgasm_batch_fix/scripts/h_orgasm_batch.py`（寸止分支改为纯累积；新增窗口末尾判定与失败解放；`_EDGE_WINDOW_RESULTS` 语义从"掷骰结果复用"改为"待判事件累积"）。
- 新增接管面：`Script.Design.character_behavior.init_character_behavior` 整函数副本进入 mod 层，核心函数升级时需人工跟进（本仓库整函数接管 mod 的既有共同成本）。
- 受影响测试：`mod/local_h_orgasm_batch_fix/tests/` 单元测试、`mod/tests/bdd/` 存档 99 近真实回归（掷骰次数 ≤1/角色/窗口、判定发生在窗口末尾、失败释放含本窗口累积并清空状态、中途退出角色被跳过）。
- 新增回归覆盖：窗口末尾失败释放跨过快乐/无觉刻印阈值时，刻印能力、对应二段效果与可见文本必须在同一玩家行动窗口内完成，下一窗口不得消费上一窗口遗留的刻印行为；同时盘点由绝顶经验触发的自动素质检查是否存在同类延迟。
- 新增回归覆盖：效果 526 多部位主动解放只输出一个紧凑批次（最多三个完整代表部位，其余合并摘要），同一 `target_change` 的目标二段闭环不得再次触发 p2；抑制标记不得跨变化对象或跨玩家行动泄漏。
- 新增回归覆盖：多部位寸止成功标题内联全部部位且不再出现独立部位行；疲劳退出提示排在绝顶批次之后；失败释放完成后不得再显示同批的低等级部位绝顶或其派生喷乳/排尿作为第二波。
- 交互组件：`local_group_edge_release_fix`（退出清算契约不变，仅在窗口末尾新增前提检查与其互斥咬合）；`local_group_masturbation_intent_fix`（窗口 token 语义不变，无需改动）。
- 核心 `Script/` 文件与 CSV/JSON 数据保持不变；存档格式不变；关闭组件即回退。
