# Fable 5 final review verdict — maintainer `SPECIAL_FLAG` candidate

```text
PASS.

1) 返回合同保持原状 — 通过。生产 diff 只触及 4 个文件；handle_npc_ai.find_character_target 与状态机 dispatch 均未改动。character_see_h_and_move_to_dormitory 只在 draw() 返回后写入标记，函数仍返回 None。

2) 七个显式反应各结算一次、四个遗漏分支补齐、顺序正确 — 通过。基线已有 JOIN、REFUSE、INTERRUPT 三处结算；候选补充话术支开、露出无视、露出离开、初次转群交四处。每个分支各有一次结算和一次 panel marker，且转群交及结束 H 的结算均发生在嵌套玩家更新前。

3) marker 延迟写入 — 通过。面板内部只写实例字段；sp_flag.see_h_reaction_settled 只由状态机 40 在 draw() 完全返回后写入。嵌套 game_update_flow 期间角色标记仍为 False，不会被提前消费或清除。

4) hidden_sex_panel 直调不写标记 — 通过。settle_discovered 相对基线零改动，不读也不写 SPECIAL_FLAG；该路径的面板分支内结算已经完整。

5) 调度器语义 — 通过。标记为 False 或当前行为为 MOVE 时结算，随后无条件清标记。WAIT 后继被跳过，真实 MOVE 仍同轮推进；成功转隐奸/露出不置标记，因此保留普通 SHARE_BLANKLY 结算。

6) 计分 a=21, b=1, S=7, U=0, penalty=29 — 确认正确。新增 21 行非空、删除 1 行；没有可重复抵扣的删除。

7) 独立复跑验证 — 候选 13 passed；基线 11 failed, 2 passed。四个文件 compileall 通过，git diff --check 干净。

更低方案审查：在“逐 case 显式、必须用 SPECIAL_FLAG、不改状态机返回值”约束下未发现更低的正确方案。将 panel marker 直接写入 sp_flag 会破坏延迟写入的重入安全；为了少一行而移动局部 import 会改变本文件既有循环导入规避风格，不采纳。

Residual risk：嵌套 game_update_flow 的具体行为仍需真实 Tk 重放确认；测试是聚焦协作者替身，未覆盖完整的真实结算副作用链。
```
