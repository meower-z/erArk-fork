---
timestamp: 2026-07-19
---
# H/群交状态机与发现不变量

隐奸/群交玩法的逐条流程见 [`.github/prompts/数据处理工作流/群交系统.md`](../../.github/prompts/数据处理工作流/群交系统.md) 与 [`隐奸系统.md`](../../.github/prompts/数据处理工作流/隐奸系统.md)（术语见 `CONTEXT.md`）。本页只记跨模块的状态不变量、所有权契约与坑。

## is_h / group_sex_mode / 群交模板 三者关系

- **`sp_flag.is_h` 是每角色布尔**（`game_type.py:734`）。进入 H 的 effect 置 `is_h = True`，并**顺带**置 `see_pl_h = True`（`Script/Settle/default.py:5119-5122`）——"进 H 即视为已目击本场 H"，使力竭合法离场清 `is_h` 后回场也不会被当作新旁观者重复弹发现面板。`handle_is_h(0)` 看玩家或其交互对象任一 `is_h`（`handle_premise_other.py:1376-1388`），`handle_self_is_h` 看单角色（`:1407-1417`）。
- **`group_sex_mode` 是全局 cache 标记**（`game_type.py:1808`），不挂在角色上。`handle_group_sex_mode_on(character_id)` 忽略入参、直接返回 `cache.group_sex_mode`（`handle_premise_other.py:1458-1467`）；只在 `Script/Settle/default.py:2974`（开）与 `:2995`（结束）翻转。
- **群交模板挂在玩家 `h_state`**：`group_sex_body_template_dict` 有 A/B 两套，每套 = (部位→`[对象id, 状态id]` 字典, `[[侍奉id...], 状态]`)（`game_type.py:402`）。参与者集合 = 模板成员 ∪ 当前场景 H 角色（CONTEXT.md"群交上下文参与者"）。
- **不变量**：群交开启时 `group_sex_mode` 与参与者的 `is_h` 并存，但二者**独立**——结束群交只清全局标记，各角色 `is_h` 由各自 H 结束 effect 清；不能从一个推断另一个。

## 参与者资格：统一谓词 handle_self_exhausted

上游 PR #225 把"体力不支"收敛为单一谓词 `handle_self_exhausted`：体力 ≤1、带疲劳标记、或困倦等级 ≥2 任一即力竭，是仅看疲劳标记的 `handle_self_tired` 的广义版（`handle_premise_sp_flag.py:46-68`）。所有群交准入路径**共用同一条**，不各自判断：邀请列表跳过力竭者（`group_sex_panel.py:728`）、`invite_npc` 二次拦截（`:818`）、发现面板"邀请加入群交"分支（`sex_be_discovered_panel.py:240`）、前提 `SCENE_ALL_NOT_TIRED`（`handle_premise_place.py:696-719`）。

## 发现流程的一次性标记契约

三个标记各管一层，语义不可混用：

- **`sp_flag.see_pl_h`（目击者已处理，游戏内窗口级）**：表示该角色已对玩家在当前地点的隐奸/群交完成过发现处理。置位于进 H effect（`default.py:5122`）与发现面板绘制时对发现者的 `handle_see_pl_h`（`sex_be_discovered_panel.py:84`）。**玩家移动时窗口内立即把全体 NPC 清零**（`character_behavior.py:137-139`），换地点后恢复发现资格。消费者：前提 `WITNESS_PL_H_WITH_OTHERS`（`handle_premise_sp_flag.py:2608-2618`）；隐奸中断名单过滤掉已目击者（`hidden_sex_panel.py:245`）。
- **`discoverer_reaction_settled`（面板实例属性，init `False`，`sex_be_discovered_panel.py:51`）**：面板内每条选择分支在手动 `judge_character_status(发现者)` 后置 `True`（`:186`/`:215`/`:221`/`:246`/`:252`/`:262`/`:277`），表示"发现者反应已在面板内提前结算"。
- **`sp_flag.see_h_reaction_settled`（`game_type.py:808`）**：状态机把面板结果写回 `= now_panel.discoverer_reaction_settled`（`StateMachine/default.py:1324`）。外层 NPC 空闲结算据此决定是否补结算：`if not see_h_reaction_settled or MOVE: judge_character_status`，随后**无条件复位 `False`**（`character_behavior.py:169-171`）。

**契约：发现者反应恰好结算一次。** 要么面板内提前结算（`True` → 外层跳过），要么面板未结算（`False` → 外层补一次）；两条路径互斥，外层读后立即复位，不跨窗口残留。

## 所有权边界

- **`Sex_Be_Discovered_Panel`**（由状态机 `SEE_H_AND_MOVE_TO_DORMITORY` 触发）拥有：记录发现者名、重置其逆推状态、目标转玩家、置 `see_pl_h`、行为时长保底 1 分（`sex_be_discovered_panel.py:78-86`），以及"支开/转隐奸/转露出/邀请加入/打断"各分支对发现者 `behavior_id` 的赋值与就地 `judge_character_status`。
- **状态机层**只做三件事：关门房间豁免直接 `return`（`StateMachine/default.py:1315-1316`）、绘面板、把 `discoverer_reaction_settled` 回写到 `see_h_reaction_settled`（`:1324`）。
- **`character_behavior` 外层**只负责：MOVE 时重置 `see_pl_h`、依 `see_h_reaction_settled` 决定是否补结算、复位标记；**不**触碰面板内已提交的行为。
- **坑**：面板内凡已就地 `judge_character_status` 的分支都必须置 `discoverer_reaction_settled = True`，否则外层会二次结算 → 发现者反应重复触发（重复弹"H 中被发现"提示、状态错位）。

## handle_scene_all_not_h 的完整遍历语义

`SCENE_ALL_NOT_H`（`handle_premise_place.py:722-745`）取玩家当前场景全角色（含玩家），少于 2 人返 0（要求玩家之外至少 1 人），遍历时跳过玩家（id 0），**任一** `handle_self_is_h` 为真即返 0，全员非 H 才返 1。语义是**完整遍历**而非首个命中短路：所有非玩家角色都必须非 H。消费者为"邀请群交"指令 5055 的前提（`data/csv/InstructConfig.csv:203`）。姊妹谓词 `SCENE_ALL_NOT_TIRED` 结构同构，把 `handle_self_is_h` 换成 `handle_self_exhausted`（`handle_premise_place.py:696-719`）。
