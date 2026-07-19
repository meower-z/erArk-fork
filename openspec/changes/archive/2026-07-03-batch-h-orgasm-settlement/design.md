## Context

当前绝顶链路由 `Script/Design/second_behavior.py` 负责检测：`orgasm_judge()` 计算各快感槽跨越的等级，`orgasm_settle()` 按部位和次数调用 `character_get_second_behavior()`，再由 `second_behavior_effect()` 逐个二段行为调用 `talk.handle_second_talk()` 和对应效果。由于 `Character.second_behavior` 是按行为 ID 存储的开关式字典，原版语义是“同一个二段行为 ID 在同一轮队列中只结算一次”。

这个链路带来四个问题：同一部位可能依次显示小绝顶、普绝顶、强绝顶等重复口上；多部位多重绝顶会把每个部位都铺开显示；NPC 分支可能用进入高潮结算前的旧 `orgasm_list` 过滤新生成的绝顶二段行为，导致多重绝顶后残留单独部位提示；人力发电室会逐个显示部位发电量，最后再显示多重绝顶发电量。绝顶效果还可能降低体力，而 H 中断逻辑在后续疲劳判定中可能基于尚未归并完成的二段状态结束 H，导致本该属于 H 内的成长或统计漏算。

用户要求这些修复以 mod 形式实现，因此实现边界改为扩展已启用的 `mod/local_bugfix`，不直接修改 `Script/Design/*.py` 等游戏核心文件。

## Goals / Non-Goals

**Goals:**
- 通过 `local_bugfix` mod 替换必要函数，不直接修改核心游戏文件。
- 同一次绝顶检测周期内，按批次收集所有 NPC 绝顶事件。
- 同一部位只选择最高强度行为用于口上展示；不同强度行为的效果仍按原版二段行为开关语义结算。
- 多重绝顶先展示原版 `plural_orgasm_N` 信息和口上，然后只遍历一次绝顶部位：最重要的 3 个部位播放原格式的部位强度提示与口上，其余部位只显示短强度文本。
- 人力发电室中保持原发电结算调用和数值不变，但把同批次的多条发电提示合并为一条；显示文本沿用原版多重绝顶发电文本，只替换电量数字为合计值。
- 所有批次效果在 H 状态仍有效时完成，之后再允许体力耗尽触发 H 结束。
- 保持现有 CSV 行为 ID、口上文件、二段效果配置可复用。

**Non-Goals:**
- 不重新设计 H 行为、快感槽、刻印或人力发电公式。
- 不把同一个二段行为 ID 从原版 0/1 开关改成发生次数计数器。
- 不新增玩家射精 UI 或射精面板逻辑。
- 不新增新的绝顶 CSV 行为 ID 或口上数据。

## Decisions

### 1. 作为 `local_bugfix` 的新增脚本实现

新增 `mod/local_bugfix/scripts/h_orgasm_batch.py`，通过 `mod_info.json` 替换：
- `Script.Design.second_behavior.check_second_effect`
- `Script.Design.second_behavior.orgasm_settle`
- `Script.UI.Panel.manage_power_system_panel.store_power_by_human_power`

同时注册 `Script.Design.second_behavior.local_bugfix_is_orgasm_batch_settling`，供现有 `local_bugfix.py` 中已替换的 `judge_character_tired_sleep()` 查询批处理状态。这样可以复用现有本地修复 mod，避免创建另一个 mod 再次替换 `judge_character_tired_sleep()` 时覆盖或绕过已有修复。

### 2. 批次对象保留原版二段行为开关语义

批次对象记录：
- `effect_behavior_ids: list[str]` 和 `effect_behavior_set: set[str]`：本批次需要结算的不同二段行为 ID。
- `part_display_behavior: dict[int, str]`：每个部位最终展示的最高强度行为。
- `part_display_rank: dict[int, int]`：每个部位展示行为的强度排序。
- `plural_behavior_id: str` 和 `plural_orgasm_set: set[int]`：多重绝顶汇总行为和部位集合。
- `human_power_climax_degree` / `human_power_draw_flag`：多重绝顶人力发电汇总显示所需信息。

同一个行为 ID 在同一批里仍只结算一次，符合 `Character.second_behavior` 原版开关式设计；不同强度 ID 例如 `b_orgasm_small` 和 `b_orgasm_strong` 都会结算，但同一部位只显示最高强度。

### 3. 拆分“显示代表行为”和“效果行为”

批次 flush 的顺序为：
1. 如果是多重绝顶，先设置 `h_state.plural_orgasm_set` 并调用 `talk.handle_second_talk(character_id, plural_orgasm_N)`，直接复用原版多重绝顶信息和口上。
2. 将本批次全部绝顶部位按强度降序排序；同强度平局时随机。
3. 前 3 个代表部位调用 `talk.handle_second_talk()`，保留原格式“部位强度提示 + 口上”；其余部位调用 `talk.second_behavior_info_text()`，只显示强度提示。
   - 代表部位的黄色强度提示通过临时替换 `talk.second_behavior_info_text()` 控制为仅附带一个换行，使提示与后续口上之间只保留一个空行。
   - 非代表部位不再逐行输出，而是按强度降序分组为一行，例如 `{角色名} A、B 强绝顶，C 绝顶，D、E 小绝顶`。
4. 如果本批次在人力发电室触发多重绝顶，开启发电提示合并上下文，先执行原版多重绝顶发电结算，再执行部位绝顶效果中的发电结算。
5. 对本批次不同二段行为 ID 静默执行原配置效果，不再重复播放口上。
6. 清空本批次接管的二段行为标记，并从 must-show/must-settle 列表中移除，避免后续更新再次显示。

### 4. 人力发电只合并显示，不改结算

替换后的 `store_power_by_human_power()` 在普通路径下直接调用原函数。只有处于多重绝顶批次的人力发电合并上下文时，才把原函数的 `draw_flag` 临时改为 `False`，记录每次原函数返回的发电量，最后输出一次原版多重绝顶发电文本：

`在{角色名}{几重}重绝顶的同时，性爱发电装置产生了 {合计电量} 单位电量`

这条文本不新造叙述，只沿用原版多重绝顶发电文本，把电量数字替换为本批次合计值。

### 5. 修复旧二段队列残留导致的后续单部位提示

NPC 分支不再用进入 `orgasm_judge()` 之前构造的旧 `orgasm_list` 过滤高潮结算之后新生成的绝顶行为，而是在 `orgasm_judge()` 后执行一次未过滤的 `second_behavior_effect()`。由于批次 flush 已经接管并清理同批次绝顶行为，这个未过滤调用只会处理真正剩余的二段行为，不会把新绝顶留到后续更新。

### 6. H 结束判定在批次完成后运行

批次 flush 期间把角色 ID 加入 `_ORGASM_BATCH_SETTLING_CHARACTER_IDS`，并用 `try/finally` 确保退出时清除。`local_bugfix.py` 中现有的 `patched_judge_character_tired_sleep()` 在调用原疲劳判定前检查该标记；命中时直接返回，让体力耗尽或疲劳造成的 H 结束延后到批次完成之后。

### 7. 避免实现变量遮蔽翻译函数

批处理脚本中需要保留 `get_text._` 作为翻译函数，用于后续成就流和本地输出。循环计数变量不使用 `_`，避免 Python 局部变量遮蔽导致 `_("绝顶")` 在运行时变成调用整数。

Rationale: 该问题曾在多重绝顶修复后触发 `TypeError: 'int' object is not callable`，错误位置在成就结算调用翻译函数时。修复属于实现安全约束，但直接影响多重绝顶批处理能否继续运行。

## Risks / Trade-offs

- [Risk] 替换 `check_second_effect()` 和 `orgasm_settle()` 需要复制部分原版控制流，后续 upstream 改动可能产生漂移 → Mitigation: 变更集中在 `local_bugfix`，README 记录差异；测试覆盖旧过滤列表残留、多部位显示、人力发电合并和疲劳延后。
- [Risk] 静默执行效果可能改变现有口上与数值变化的交错顺序 → Mitigation: 仅对绝顶批次使用静默效果，普通二段行为仍走原路径；多重绝顶总口上和代表部位口上仍按原口上入口播放。
- [Risk] 人力发电合并显示可能与原始逐条显示的四舍五入观感不同 → Mitigation: 使用原函数返回值累加，并用原版 `{0:.1f}` 格式输出。
- [Risk] H 结束保护标记忘记清除会阻止后续 H 中断 → Mitigation: 使用 `try/finally` 包裹批次 flush，并用测试覆盖保护分支。
- [Risk] 用 `_` 作为无用循环变量会遮蔽翻译函数并导致运行时报错 → Mitigation: 循环变量使用具名变量，并用成就流回归测试覆盖翻译函数仍可调用。

## Migration Plan

1. 在 `mod/local_bugfix/scripts/h_orgasm_batch.py` 中实现批次对象、显示选择、静默效果、人力发电合并和替换函数。
2. 更新 `mod/local_bugfix/mod_info.json` 注册新增脚本和替换函数。
3. 在 `mod/local_bugfix/scripts/local_bugfix.py` 的疲劳判定 wrapper 前置批处理保护。
4. 更新最终显示格式，使代表提示到口上之间只保留一个空行，非代表部位使用一行分组汇总。
5. 修复本地实现中的翻译函数遮蔽风险。
6. 更新 `mod/local_bugfix/README.md` 和测试。
7. 运行 mod 测试、语法编译和 JSON 校验；完整 mod 初始化需当前 Python 安装 `requirements.txt` 中依赖后验证。
