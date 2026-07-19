# Design: 寸止判定延迟至玩家行动窗口末尾

## Context

### 引擎既定事实（设计讨论中逐一核实）

1. **窗口是原子推进**：`update.game_update_flow(add_time)` 先把 `cache.game_time` 一次性推进到目标时间（`Script/Design/update.py:22`），再进 `character_behavior.init_character_behavior()`。玩家的行为在任何 NPC 动之前按完整 duration 结算完毕（`character_behavior.py:54-57`）。
2. **NPC 行为效果在选择时满额入账**：NPC 空闲时 `find_character_target` 选中新行为后立即 `judge_character_status` → `handle_settle_behavior(character_id, end_time, ...)`，`end_time = start + duration`（`character_behavior.py:206/232`）。"做到一半"的动作没有可撤销的部分效果，时间流逝期间只有 realtime/二段效果累积。
3. **NPC 追时间是 round-robin、各自本地时钟**：窗口进行中任意时刻，各 NPC 本地时间不一致；"把所有角色回滚/统一结算到窗口中间任意时刻 T"在现架构下无干净做法。因此窗口中途打断（hard stop）方案被否决。
4. **`over_behavior_character` 每窗口新建**（`character_behavior.py:50`），其对象身份即"一次玩家行动窗口"的天然 token，`_get_edge_window_results()` 已在用。
5. **掷骰公式**：`over_count = 玩家能力[30]×3 − Σ(orgasm_edge_count[部位]²)`，超限后每超一点 20% 失败率（`second_behavior.py:585-609`）。难度由累积计数的平方和决定——判定时机越晚、累积越多、越难守住。
6. **失败解放的原版机制**：结算链中 `orgasm_edge == 3` → 置 2 → 以 `orgasm_edge_count` 作为 `un_count_orgasm_dict` 再调一次 `orgasm_settle`（`second_behavior.py:366-368`）。这是普通函数调用，可在任意时点复刻。
7. **退出清算体系已完备**：`local_group_edge_release_fix` 覆盖疲劳退出、玩家 HP 归零、被发现打断、群交缩减单人、单 NPC 退出、无意识恢复等全部退出路径，契约为"释放待释放计数 → 清空 `orgasm_edge_count` → 重置 `h_state.orgasm_edge`"（`openspec/specs/local-bugfixes/spec.md:130-178`）。

### 现状（merge-orgasm-edge-per-action 已落地）

`h_orgasm_batch.py:676-701`：窗口内首个跨级结算时掷骰并绘制，结果存 `_EDGE_WINDOW_RESULTS[character_id]`，同窗口后续跨级静默复用。问题：掷骰发生在累积之前（长窗口与短窗口难度相同）；失败若发生在窗口中途，失败文本被后续追时间结算淹没；成功后整个窗口免疫。

### 手动验证新发现：窗口末尾失败释放缺少派生结算闭包（2026-07-10）

存档 99 手动验证中观察到：一次多重绝顶已经在窗口末尾释放并显示，但由该批绝顶新满足的快乐刻印、无觉刻印等获取文本没有紧随本批输出，而是在玩家执行下一条指令后才出现。截图中的刻印叙事属于上一窗口的释放结果，却混入下一窗口的常规结算输出。

已建立一个不落盘的最小复现，直接驱动 `settle_pending_edge_judgments_at_window_end()` 的失败分支：

- 窗口末尾释放使绝顶派生效果计数达到 4；
- 窗口末尾刻印输出为 `[]`；
- 紧接着调用下一次 `patched_check_second_effect()` 后，输出变为 `['happy_mark_1']`；
- 同一套桩仅走普通 `patched_check_second_effect()` 时，`happy_mark_1` 会在本次结算内输出，说明回归边界位于新增的窗口末尾路径，而不是所有多重绝顶路径。

确认的调用顺序如下：

```text
普通角色结算
  handle_settle_behavior
    -> check_second_effect
       -> orgasm_judge / orgasm batch effects
       -> mark_effect
       -> mark second behaviors
    -> extra_exp_settle
  -> gain_talent

窗口末尾失败释放（新增路径）
  patched_orgasm_settle
    -> orgasm batch effects
  -> clear edge state
  -> collect/draw value changes
  -> achievement flow / return control
  X  no post-orgasm mark settlement
  X  no post-release automatic talent eligibility check
```

因此当前问题不是单纯的绘制顺序错误，也不应归因于普通路径预建 `mark_list` 的既有风险；直接原因是窗口末尾新增了一个能产生绝顶计数、经验与二段效果的结算入口，却只移植了“绝顶 batch + 数值绘制”，没有移植常规行为结算在其后的派生检查。

目前按可信度排序的判断：

1. **已确认：窗口末尾失败释放没有执行 post-orgasm 刻印检测与刻印二段消费。** 最小复现精确呈现“本窗口无输出、下一常规结算出现”。
2. **源码确认、尚待场景复现：自动素质获得也可能延后一窗口。** `character_behavior()` 中 `gain_talent(now_gain_type=0)` 已在窗口末尾 hook 之前执行；而失败释放可增加绝顶相关经验，例如经验 111 跨过 50 时满足“饮精绝顶”素质条件。
3. **对照排除为本截图主因：普通多重绝顶路径自身统一延迟。** 普通路径在 `orgasm_judge` 后仍会执行 `mark_effect` 与刻印二段结算，对照复现同回合完成。
4. **次要既有风险：预建 `mark_list` 过滤列表滞后。** 该风险仍值得单独审计，但角色初始化会预置二段行为键，且它不能解释本次窗口末尾路径完全没有调用 `mark_effect` 的事实。

### 手动验证新发现：效果 526 主动解放后同一变化对象被再次绝顶判定（2026-07-10）

隐奸中主动选择“释放快感”后，截图显示第一段多部位绝顶结算完成，随后又出现“八重绝顶”及尿道绝顶等 p2 后续波次。代码追踪确认这是两条相邻但职责重叠的调用链：

```text
效果 526 handle_orgasm_edge_release
  -> orgasm_edge = 2
  -> patched_orgasm_settle(target_id, target_change, un_count_orgasm_dict=edge_count)
     -> 已完成多部位批处理、效果应用与队列清理
  -> 清空 edge_count

同一行为的目标二段闭环
  -> patched_check_second_effect(target_id, 同一个 target_change)
     -> first broad second_behavior_effect
     -> orgasm_judge(target_id, target_change)  # 再次读取释放刚产生的高额变化
     -> second broad second_behavior_effect      # 消费新生成的 p2 队列
```

定向测试进一步把两个现象拆开：直接调用主动解放批处理时，8 个部位已经遵守“复数绝顶 + 3 个完整代表部位 + 5 个部位合并摘要”的既有显示契约；红点精确落在随后同一 `target_change` 的 `orgasm_judge` 被调用一次。因此截图中“所有部位完整显示”不能归因于 `_flush_orgasm_batch` 的代表部位上限本身，可靠修复目标是阻止同一变化对象生成第二批；若重启加载新代码后首批仍全量展开，应作为独立的运行时加载/队列来源继续取证，而不能靠扩大本修复的抑制范围猜测处理。

### 手动验证新发现：失败释放后又出现低等级部位绝顶（2026-07-10）

群交场景中为两名参与者装备玩具并连续等待后，寸止失败输出出现以下顺序：

```text
五重绝顶
  胸部强绝顶
  阴道强绝顶
  肛肠强绝顶
  阴蒂、心理 小绝顶（合并摘要）
胸部小绝顶
喷乳
```

首段恰好符合批处理器的显示上限：三个完整代表部位 + 其余部位摘要。之后的“胸部小绝顶”不能是同一批的合法部位代表，因为 `OrgasmBatch.part_display_behavior` 对同一部位只保留最高强度，胸部强绝顶已经占据该部位代表。

存档 99 确定性插桩给出最终诊断：

1. **只有一次释放调用。** `patched_orgasm_settle` 由窗口末尾失败释放调用一次；`change_data` 身份保持不变，normal/extra 字典为空，`un_count` 为完整释放计数，调用时 edge 为 2。
2. **所有 owned 队列在该调用后均为空。** `second_behavior`、must-show 与 must-settle 没有遗留 `b_orgasm_small`，因此不是第二次结算或陈旧队列。
3. **真实所有者是 `b_orgasm_to_milk` 的标题渲染。** 批处理器把它正确识别为非部位派生并进入派生口上；核心 `talk.second_behavior_info_text` 却先命中宽泛的 `"orgasm"` 分支，再到不了后面的喷乳专用分支，于是错误补出“胸部小绝顶”标题。
4. **最窄修复位于组件派生口上边界。** 仅在当前角色、当前 `b_orgasm_to_milk`/`u_orgasm_to_pee` 调用期间压制错误的通用标题，再以 `finally` 恢复原函数；真实喷乳/排尿口上和效果仍各结算一次，其他绝顶标题不受影响。

### 新显示要求：寸止部位内联到黄色标题

当前成功路径先由 `_draw_edge_merged_part_line()` 输出白色“寸止部位：阴蒂、阴道、肛肠”，再让代表部位 `{part}_orgasm_edge` 生成黄色“角色名 + 代表部位 + 绝顶寸止”。新要求把两个信息源合成一个标题：黄色标题使用全窗口 `edge_crossed_parts` 的全部部位，以顿号连接，格式为“{角色名}{部位1}、{部位2}、{部位3}绝顶寸止”；删除独立白色部位行。口上选择仍可使用原有代表部位，不要求新增多部位口上数据。

### 新排序要求：疲劳退出在绝顶批次之后

当前 `character_behavior()` 在 NPC 入口先调用 `handle_npc_ai.judge_character_tired_sleep()`，随后才进入 H 状态处理与 `judge_character_status()`；因此疲劳提示可能先于同一行为已经产生、但尚未显示的绝顶二段输出。目标顺序是因果顺序而非简单延迟所有疲劳检查：

```text
行为与玩具数值结算
  -> 绝顶检测、批次口上、派生效果
  -> 数值面板/批次收尾
  -> 若本批导致疲劳退出，显示“太累了”并执行退出清算
```

实现前必须区分“行为开始前已经疲劳”与“本行为结算后才疲劳”两种情况；前者仍可在入口阻止新行为，后者的可见提示与退出副作用应在当前原子批次完成后发生。

### 被否决的替代方案

- **切片化长等待 + 失败 hard stop**：把 1 小时等待拆为多个 `game_update_flow(5)`，失败后不再发片。可行但改动面大（等待指令族、事件密度、意图修复窗口 token 全部受扰动），且"每切片一次掷骰"提示仍可能刷屏。
- **窗口中途 hard stop + 时间回退**：时停模式的回退（`character_behavior.py:59-62`）之所以成立是因为该分支 NPC 根本不动；追时间中途回退面对"玩家已满额结算 + 部分 NPC 已越过 T 且效果前置入账"的不可逆状态，不可行（事实 2、3）。

窗口末尾延迟判定以最小改动同时满足：难度随累积上升（事实 5）、失败必然落在控制权交还边界（hard stop 目的被构造性满足）、一角色一窗口一提示。

## Goals / Non-Goals

**Goals:**

- 窗口内寸止跨级零掷骰、零提示、零口上：只把 `climax_count` 累进 `orgasm_edge_count` 并登记待判事件。
- 窗口末尾对每个仍满足寸止前提的待判角色恰好掷骰一次，难度含本窗口全部累积。
- 成功：一条成功提示 + 内联全部部位的黄色“绝顶寸止”标题 + 一个代表部位寸止口上，不绘制独立部位列表行（代表部位取自全窗口跨级部位）。
- 失败：一条失败提示 + 当场释放全部积攒 + 按退出清算契约清空 edge 状态。
- 中途退出 H 的角色由 `local_group_edge_release_fix` 清算，窗口末尾静默跳过。
- 效果 526 主动解放在同一变化对象中只形成一个紧凑绝顶批次，不被紧随其后的目标闭环重新判定为 p2。
- 底层量表积累（快感、玩具、环境增长）与原版完全一致，不因提示合并而削弱。

**Non-Goals:**

- 不修改核心 `Script/` 文件（接管副本除外，核心文件本身不动）。
- 不改掷骰公式、`orgasm_edge_count` 数据结构、寸止释放效果（529）、群交结束链路。
- 不引入等待切片化或任何 hard stop 机制。
- 不处理时停寸止分支（`unconscious_flag_3`，原样 continue）。
- 不新增 CSV 行为 ID 或口上数据。

## Decisions

### 1. 判定时机：窗口末尾 hook 而非"识别最后一次跨级"

"判最后一次"不需要 lookahead：把判定推迟到**不可能再有下一次跨级**的时刻即可，即 `init_character_behavior()` 主循环 break 之后。此时所有角色已追齐 `cache.game_time`，本窗口不会再有任何结算。

替代方案（在每次跨级时预测是否为最后一次）需要模拟前瞻，被否决。

### 2. Hook 实现：整函数接管 `init_character_behavior`

`local_h_orgasm_batch_fix` 以整函数副本接管 `Script.Design.character_behavior.init_character_behavior`（注册表 patch，手法同 `orgasm_settle`、`find_character_target` 接管）。窗口末尾判定插入点：主循环 break 之后、成就结算（`achievement_flow`）与 web 文本录制标志关闭（`cache.web_text_recording_flag = False`）**之前**——保证 web 模式的文本回溯能录到判定输出。

替代方案（外层 wrapper，先调原函数再补判定）无法控制插入点在录制关闭之前，web 模式丢文本，被否决。整函数接管的维护成本（核心升级需人工跟进副本）是本仓库既有接管 mod 已接受的共同成本。

### 3. 窗口内累积语义：立即入账 + 待判登记

`patched_orgasm_settle` 寸止分支（现 `h_orgasm_batch.py:676-701`）改为：

- 每次跨级立即 `orgasm_edge_count[部位] += climax_count`（不再区分成功/失败入账时机）；
- `_EDGE_WINDOW_RESULTS[character_id]` 语义从 `{"success": bool}`（掷骰结果复用）改为待判事件记录：`{"parts": {部位: 累计climax_count}}`，跨结算合并同部位；
- 不掷骰、不绘制、不入队口上，部位循环继续。

窗口缓存仍以 `over_behavior_character` 对象身份换代清空（`_get_edge_window_results()` 机制不变），不持久化到存档；读档后对象必然更替，缓存自动失效。

### 4. 窗口末尾判定流程

对 `_EDGE_WINDOW_RESULTS` 中每个待判角色（按角色 ID 升序，保证输出确定性）：

1. **前提守卫**：`handle_premise.handle_self_orgasm_edge(character_id)` 为假（中途退出 H 已被 release fix 清算、或死亡等）→ 静默跳过，删除待判记录。
2. **掷骰**：调用 `second_behavior.judge_orgasm_edge_success(character_id)` 一次（自带提示绘制）；此时计数已含本窗口累积，即"判最后一次"的难度。
3. **成功**：把待判记录中的全部部位写入 `OrgasmBatch.edge_title_parts`，由黄色“绝顶寸止”标题按顿号内联绘制且不输出独立部位行；按 `climax_count` 最高、平局随机选代表部位，入队一个 `{part}_orgasm_edge` 二段口上并 flush（复用 `_queue_second_behavior`/`_flush_orgasm_batch` 通道，需新建局部 `CharacterStatusChange`）。
4. **失败**：复刻原版解放语义——置 `h_state.orgasm_edge = 2`，以 `orgasm_edge_count` 全量作为 `un_count_orgasm_dict` 调用（已接管的）`orgasm_settle`，随后**清空 `orgasm_edge_count`、重置 `h_state.orgasm_edge`**（遵循 release fix 的清算契约，防止残留状态在睡眠结算二次触发）。解放产生的二段效果同步 flush，数值变化经局部 `CharacterStatusChange` 绘制。

失败释放量 = 旧积攒 + 本窗口累积（原版流内失败会丢弃触发跨级的那笔计数，本设计更自洽："憋了一窗口的全部出来"）。此为有意的语义变更，已在 proposal 声明。

### 5. 判定输出的绘制通道

窗口末尾已脱离行为结算面板，判定输出（提示行、内联部位标题、口上、解放数值变化）由组件自行绘制：提示文本走 `draw.NormalDraw`（`judge_orgasm_edge_success` 自带），内联部位标题、口上与二段效果走既有批处理 flush 通道，数值变化新建 `CharacterStatusChange` 后复用既有变化绘制辅助。绘制抑制条件（`_can_show_second_behavior` / `_suppress_draw_when_needed`）沿用：窗口末尾判定时角色若处于不应显示二段文本的状态，提示照常绘制但口上按既有抑制规则处理。

### 6. 窗口末尾派生结算闭包

失败释放 batch 完成后执行窄化 post-orgasm closure：先快照角色的二段行为队列，再只运行刻印检测、消费本批新生成的刻印行为，并运行自动素质检查。它不复用完整 `patched_check_second_effect`，因此不会重放初见、插入、道具、普通二段或 `orgasm_judge`。

闭包以生成前后差集限定所有权；即使刻印效果或素质检查抛出异常，也会在 `finally` 中清理本闭包拥有的新增队列后再向上传播。这样由窗口末尾失败释放产生的刻印与素质资格属于当前响应，下一条玩家指令不会消费上一窗口遗留的本批行为。普通结算路径原有的刻印过滤时序不在本次窄闭包范围内。

### 7. 主动解放使用变化对象级一次性闭环标记

效果 526 的 `patched_orgasm_settle` 仅在以下条件同时成立时，把角色 ID 写入当前 `change_data` 的私有集合属性：

- `un_count_orgasm_dict` 非空；
- 当前满足 `handle_self_orgasm_edge_relase_or_time_stop_orgasm_relase(character_id)`；
- 批次实际生成并完成了绝顶效果行为。

目标的 `patched_check_second_effect` 仍先执行原有初见、位置、道具和第一遍普通二段消费；随后检查并一次性消费该角色在当前变化对象上的标记。命中时只跳过 `orgasm_judge` 以及专用于消费该判定新队列的第二遍宽泛 `second_behavior_effect`，刻印检测和刻印过滤消费继续执行。标记集合清空后删除属性，不使用模块级“下次跳过”令牌，因此新的 `CharacterStatusChange` / `TargetChange` 不受影响。

不采用“同步提高 `h_state.orgasm_level` 来阻止再判”的方案：`un_count_orgasm_dict` 表示先前已跨级但被寸止扣留的次数，其 level 在扣留时已经累进，再次修改会破坏计数语义。也不采用角色级全局布尔值，因为异常分支或没有进入目标闭环时会把抑制泄漏到下一条真实结算。

### 8. 与相邻组件的咬合

- **`local_group_edge_release_fix`**：互斥消费。中途退出 → 退出路径释放并清空 → 窗口末尾前提守卫发现空账，跳过。窗口末尾失败释放遵循同一清算契约，两条路径对 `orgasm_edge_count`/`orgasm_edge` 的终态语义一致。
- **`local_group_masturbation_intent_fix`**：其 action key 同样基于 over 对象身份，窗口定义未变，无需改动。
- **时停**：`unconscious_flag_3` 分支在寸止分支之前 continue，不产生待判记录，窗口末尾无事发生。

## Risks / Trade-offs

- **[窗口内零预警]** "差不多到极限"类中途预警文本消失，玩家在长等待中对累积风险不可见 → 接受：这是"模拟/渲染分离 + 判最后一次"语义的直接推论（用户确认）；窗口末尾提示会如实反映最终结果；如实测体验不佳，可后续加窗口末尾的累积量摘要行，属显示增强。
- **[失败释放更猛]** 释放量含本窗口累积，比原版流内失败（丢弃触发笔）更大 → 接受：语义上更自洽，且原版"丢弃触发笔"本身更像实现巧合而非设计意图；proposal 已声明。
- **[整函数接管新增维护面]** `init_character_behavior` 是主循环核心，上游改动频率可能高于 `orgasm_settle` → 缓解：接管副本内以清晰注释标记插入块边界，确定性组件回归分别覆盖普通玩家/NPC窗口、新一天、睡眠存档与时停回退，生产修复后的远程全量 BDD 40 项通过；核心升级时仍需人工 diff 副本。
- **[窗口末尾角色状态漂移]** 判定时角色位置/状态可能与跨级发生时不同（如 NPC 已移动） → 缓解：前提守卫过滤已退出 H 的角色；仍在 H 中的角色其 edge 状态与计数由本组件与 release fix 独占管理，不受位置影响；口上播放条件按判定时刻状态评估（与原版"下一结算才播口上"的既有漂移程度相当）。
- **[多角色判定顺序]** 同窗口多角色待判时输出顺序影响观感 → 按角色 ID 升序固定，测试可断言。
- **[读档/异常中断]** 窗口缓存为模块级内存态，异常或读档后残留 → 既有机制：over 对象换代即清空；不持久化。
- **[派生结算重入]** 直接复用完整 `check_second_effect` 会重复处理道具、插入、既存二段行为或再次进入绝顶判定 → 已采用生成前后差集限定的窄化闭包，只处理本批刻印行为与自动素质检查，并以异常清理回归锁定队列终态。
- **[自动素质边界]** 窗口末尾释放发生在主循环常规 `gain_talent` 之后 → 窄化闭包在同一窗口补跑自动素质检查，使绝顶经验跨阈值后的资格不额外延迟；原版素质二段行为的既有显示时序不作扩大修改。
- **[主动解放抑制过宽]** 若用角色级状态跳过下一次 `orgasm_judge`，中断或分支变化会吞掉下一条真实绝顶 → 以 `change_data` 对象身份和角色 ID 双重限定，并在目标闭环中一次性消费；回归测试使用新的变化对象确认普通判定恢复。
- **[疲劳检查副作用]** 直接整体后移 `judge_character_tired_sleep` 可能允许本应在行动前退出的角色多执行一次行为 → 设计需保留入口门禁，把“本批新触发的退出提示/清算”延迟到批次之后，而不是删除前置检查。
- **[派生标题抑制过宽]** 直接隐藏所有低级绝顶文本会掩盖真实第二批 → 修复只绑定当前角色与喷乳/排尿派生 ID；回归同时断言一次释放调用、变化对象身份、三类字典、edge 状态、低级效果静默结算、派生效果次数与全部 owned 队列终态。

## Migration Plan

1. 修改 `mod/local_h_orgasm_batch_fix/scripts/h_orgasm_batch.py`：寸止分支改纯累积（Decision 3），新增窗口末尾判定函数（Decision 4/5）。
2. 新增 `init_character_behavior` 接管副本与注册（Decision 2），manifest 更新接管声明。
3. 测试先红后绿：存档 99 BDD 回归改写断言（判定次数、时机、失败释放量、清算终态、跳过路径）；单元测试覆盖窗口缓存语义变更。
4. 全量 `mod/tests/`（含 E2E），确认寸止释放效果 529、群交结束、退出清算链路无回归。
5. 归档顺序：先归档/同步 `merge-orgasm-edge-per-action`，再归档本变更（MODIFIED delta 基于其 requirement 标题）。

回退策略：关闭 `local_h_orgasm_batch_fix` 组件即回退到原版行为；存档格式不变，无数据迁移。

## Open Questions

- 无（设计讨论已收敛，四个语义点均经用户确认或为其直接推论）。
