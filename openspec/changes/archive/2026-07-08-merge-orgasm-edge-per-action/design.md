## Context

寸止（orgasm edge）判定链路：`orgasm_settle()` 逐部位检测快感槽跨级，`handle_self_orgasm_edge` 前提成立时对**每个跨级部位**各调用一次 `second_behavior.judge_orgasm_edge_success(character_id)`（`Script/Design/second_behavior.py:574-614`）。该函数每次调用都独立掷骰（玩家能力[30]×3 对比各部位寸止计数平方和）并**直接绘制**成功/接近极限/失败三种提示之一。失败则 `orgasm_edge = 3` 走失败解放路径。

诊断（存档99真实群交局，随机种子固定）证实了两个症状共享同一根因——判定与提示的作用域是“每次结算 × 每个跨级部位”，而玩家感知窗口是“一次点击”：

- 症状1：杜宾(130)在**同一次** `orgasm_settle` 内两个部位各掷一次骰、各出一条提示；
- 症状2：陈(10)在**同一次玩家行动**内跨两次结算掷骰（第6次结算：自慰推高V部位跨级；第16次结算：发呆空闲结算时环境心理快感增长 990→1073 再次跨级，来源 `realtime_settle.py:494-496` 群交环境持续增长）。一次点击实测产生 117 次 `orgasm_settle` 调用，结算间隙快感槽持续上涨，重复不可避免。

原版 `second_behavior.py:434-448` 结构完全相同，因此该 bug 原版同样存在；修复按本仓库惯例落在已接管 `orgasm_settle` 的 `local_h_orgasm_batch_fix` 组件内。

## Goals / Non-Goals

**Goals:**
- 同一玩家行动窗口内，每个角色最多进行**一次**寸止成功/失败掷骰；同窗口后续跨级复用该结果。
- 合并而非跳过：成功时每个跨级部位仍把 `climax_count` 累加进 `orgasm_edge_count[部位]`，待释放总量与现状完全一致；失败时 `orgasm_edge = 3` 失败解放路径原样执行、不被抑制。
- 每角色每窗口最多显示**一条**成功/失败提示；同一结算内多部位合并时提示列出全部部位名。
- 多部位口上重新设计：合并判定的多个部位只播放**一个代表部位**的 `{part}_orgasm_edge` 口上，其余部位并入提示行的部位列表，风格与既有批处理绝顶显示方案（代表部位+分组单行）一致。
- 掷骰公式、时停寸止分支（`unconscious_flag_3`）、寸止释放结算（效果529、群交结束）全部不变。

**Non-Goals:**
- 不修改核心文件 `Script/Design/second_behavior.py`。
- 不改寸止成功率公式或 `orgasm_edge_count` 数据结构。
- 不新增 CSV 行为 ID 或口上数据（复用现有 `{part}_orgasm_edge` 行为与口上）。
- 不处理非群交场景下本就单次的寸止路径的显示样式（其行为自然退化为与现状一致）。

## Decisions

### 1. 窗口标识：`over_behavior_character` 对象更替（沿用意图修复的成熟模式）

`cache.over_behavior_character` 在 `character_behavior.init_character_behavior()` 每次玩家行动开头整体新建一次（`character_behavior.py:50`），其对象身份即“一次玩家行动”的天然标识。`local_group_masturbation_intent_fix._get_group_sex_masturbation_action_key()` 已用该技术稳定运行。

`h_orgasm_batch.py` 内新增模块级窗口缓存：

- `_EDGE_WINDOW_OVER_OBJECT`：上次见到的 `over_behavior_character` 对象引用；
- `_EDGE_WINDOW_RESULTS: dict[int, dict]`：角色ID → `{"success": bool}`（提示是否已显示、合并了哪些部位均可由"是否首个结算"推出，无需单独字段）。

对象更替时清空缓存。不持久化到存档（窗口不跨存档有意义）。

### 2. 掷骰与合并语义

`patched_orgasm_settle` 的寸止分支改为两阶段：

1. **部位循环内只收集**：跨级且寸止前提成立的部位不再逐个调用 `judge_orgasm_edge_success`，改为记入本次结算的 `edge_crossed_parts`（连同各自 `climax_count`），部位循环继续（不 return）。
2. **循环后统一判定**：若 `edge_crossed_parts` 非空——
   - 窗口缓存无该角色记录 → 调用一次 `judge_orgasm_edge_success`（掷骰+绘制其自带提示，绘制受既有 `_suppress_draw_when_needed` 控制），结果写入窗口缓存；
   - 已有记录 → 直接复用 `success` 值，**不掷骰、不出提示**（静默合并）。
   - 成功：每个跨级部位 `orgasm_edge_count[部位] += climax_count`；
   - 失败：`orgasm_edge = 3`，flush 批次后 return（与现行为一致，失败解放不受窗口缓存影响——此后 `handle_self_orgasm_edge` 前提为假，后续结算自然走解放路径）。

掷骰时机在“该窗口首个跨级结算”，此时 `orgasm_edge_count` 尚未加上本窗口新增计数——与现状首部位掷骰的成功率一致；下一次玩家行动重新掷骰时自然使用累加后的更高计数（成功率递降语义保留）。

### 3. 多部位提示与口上显示方案

- **提示行**：`judge_orgasm_edge_success` 的原提示文本不含部位名（“成功寸止了陈的绝顶”）。同一结算内多部位合并时，在该提示后追加同风格部位列表行：`寸止部位：阴道、心理`（部位名用既有 `ORGASM_PART_NAME_BY_PREFIX` 映射）；单部位时不追加，显示与现状完全一致。同窗口**后续结算**的静默合并不补显示（提示已随首次掷骰绘制，不可回溯改写；待释放量在寸止释放结算时按合并后总量如实体现）。
- **口上**：合并的多个部位只入队**一个**代表部位的 `{part}_orgasm_edge` 二段行为（经既有 `_queue_second_behavior` 批处理通道，`count` 取该部位合并 `climax_count`）。代表部位选择规则与批处理绝顶方案一致：`climax_count` 最高者优先，平局随机。其余部位不再产生 `{part}_orgasm_edge` 口上（其存在感由提示行部位列表承担）。
- 同窗口后续结算的静默合并部位同样不产生口上。

### 4. 回归测试：把诊断回路转为 BDD 测试

在 `mod/tests/bdd/` 新增近真实层测试（模式同 `test_bdd_save_group_ai.py`）：`boot_game_once` + 桩 `get_wait_response` + 读档99 + `random.seed` 固定；把陈(10)的 `status_data[23]=990 / orgasm_level[23]=2`、`status_data[4]=990 / orgasm_level[4]=2` 放到跨级门槛下（复刻诊断脚本布置）；插桩 `second_behavior.judge_orgasm_edge_success` 计数；驱动一次 `handle_wait_1_hour()`。断言：

- 每角色掷骰次数 ≤ 1（修复前红：杜宾同结算2次、陈跨结算2次）；
- 陈的 `orgasm_edge_count` 增量等于所有跨级部位 `climax_count` 之和（合并而非跳过）；
- 失败路径场景（掷骰打桩为失败）：`orgasm_edge == 3` 且解放路径不被抑制。

## Risks / Trade-offs

- **窗口内成功后“无限免费寸止”**：同窗口后续跨级不再掷骰，理论上一次长行动内可积累多次计数而只承担一次失败风险。接受：这正是用户要求的语义（一次点击最多一次结算）；下一次行动掷骰时计数平方和已变大，风险后置而非消失。
- **静默合并部位玩家不可见**：同窗口后续结算新增的寸止计数没有即时提示。接受：消除刷屏是本修复的目的；总量在释放时如实结算。若实测体验不佳，可后续在窗口末尾（玩家下次行动前）补一条汇总，属显示增强，不影响本设计的结算正确性。
- **模块级状态与读档**：窗口缓存以对象身份为键，读档后 `over_behavior_character` 对象必然更替，缓存自动失效，无跨存档泄漏。
- **时停路径**：`unconscious_flag_3` 分支在寸止分支之前 `continue`，不进入新逻辑，行为不变。

## Migration Plan

1. 修改 `mod/local_h_orgasm_batch_fix/scripts/h_orgasm_batch.py` 寸止分支（现第579-590行）为两阶段窗口合并逻辑；无 manifest 变更（`orgasm_settle` 已被该组件替换）。
2. 新增 BDD 回归测试文件；先在修复前跑红（复用诊断布置），再实现后跑绿。
3. 全量跑 `mod/tests/`（含存档99全流程 E2E），确认寸止释放、效果529、群交结束链路无回归。
4. 删除临时诊断脚本 `debug_edge_loop.py`，grep 清理 `[DEBUG-edg1]`。

无数据迁移；存档格式不变；关闭该 mod 组件即回退到原版行为。
