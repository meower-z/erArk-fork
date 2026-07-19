# PR 草稿（中文）

> 已开上游 PR：[Godofcong-1/erArk#226](https://github.com/Godofcong-1/erArk/pull/226)。正文以 PR 为准（含真实 Tk 前后对比截图）；本草稿为过程记录。


分支：`codex/add-per-click-orgasm-chain-gate`（基于 `upstream/master@97c35826e`，单次提交，五文件约 25 行）

---

## 标题

修复：NPC 多重绝顶后在同一次点击内被反复调度、堆叠大量口上

## 正文

### 问题

在一次玩家行动结算中，如果 NPC 进行了高潮释放（尤其是多重高潮），展示大量口上之后，其仍可能在同一次点击内立即被重新调度、生成下一轮主动行为，从而反复主动行动、反复高潮，展示出非常大量口上、影响游戏观感。

### 方案

只针对多重绝顶、且只在本次玩家行动内做一次很轻的主动行为阻断：NPC 在本次行动内发生一次多重绝顶后，本次行动剩余结算中不再生成新的自主行为；下一次玩家行动即自动恢复。不按游戏分钟恢复、不引入眩晕或冷却，单部位高潮完全不受影响。

用一个与 `see_pl_h`、`see_h_reaction_settled` 同类的角色临时结算标记记录该逻辑状态：

- `Script/Core/game_type.py`：`SPECIAL_FLAG` 新增 `multi_orgasm_this_player_action`，语义为“本次玩家行动内已多重绝顶”。
- `Script/Design/update.py`：`game_update_flow()` 在最外层点击开始时重置全体 NPC 的该标记；嵌套更新复用同一标记。
- `Script/Design/second_behavior.py`：`orgasm_settle()` 完整释放事务结束后，**仅当本次为多重绝顶（`part_count >= 2`，即 ≥2 个部位同时高潮）**才置位该 NPC 的标记。单部位高潮、玩家（`character_id` 为 0）、成功寸止与时停蓄积（循环内 `continue`，`part_count` 保持 0）都不会置位。
- `Script/Design/handle_npc_ai.py`、`Script/Design/handle_npc_ai_in_h.py`：普通空闲 AI 入口 `find_character_target()` 与群交 type-1/type-2 入口 `npc_ai_in_group_sex()` 读取该标记。命中时不再创建新目标、自慰意图或模板占位，但保留其群交参与关系，随后仍走 `judge_character_status()` 等被动结算尾部并最终加入 `over_behavior_character`（不改成会跳过结算的 `WAIT`，不挂起调度循环）。

### 影响范围

只影响「同一次玩家行动内、刚发生过多重绝顶的那名 NPC 会不会紧接着又被安排一次主动行为」。单部位高潮、玩家行动、寸止、时停、以及下一次行动都不受影响。被标记的 NPC 仍照常接受刺激、结算被动数值与已发生的绝顶口上，只是不再自己发起下一轮动作。新增的 `sp_flag` 布尔字段会随角色存档，但每次最外层点击开始必重置，不跨点击/跨存档遗留影响；旧存档经既有加载路径（重建 `Character()` 后 `recursive_update` 覆盖）自动补上默认值 False，兼容安全。

### 未改动

高潮阈值/次数/概率、寸止与时停语义、多部位与多重绝顶事务本身、群交模板成员关系、通用 NPC 分钟调度策略均未改变；存档只多一个默认 False 的临时标记字段。前置的更新深度成对恢复由上游 #216 提供，本 PR 只消费稳定的最外层更新身份。

---

## 给审查者的说明（不进 PR 正文）

- 本 PR **不夹带自动化测试**。行为验证以 headless A/B 完成（真实 `save/99` + 真实函数体），证据留在本地 `.codex-evidence/per-click-orgasm-chain-gate/`。
- **真实玩家可见文本 A/B**（`screen_text_baseline.log` / `screen_text_candidate.log`，多重绝顶场景）：捕获游戏真实渲染出口 `era_print`。亚叶发生多重绝顶后，baseline 屏幕出现「亚叶开始自慰了」+ 再次绝顶及自慰增益（`final=masturebate`）；candidate 无此新自慰、只保留已发生绝顶的被动结算（`final=share_blankly`）。
- **边界验证**（`single_part_not_gated.log`）：同为开启 gate，但用单部位高潮时标记不置位、NPC 未被拦截、仍出现「亚叶开始自慰了」——与「只针对多重绝顶」的设计一致。
- 诚实边界：释放被安排在点击早期以忠实复现文档记录的真实触发条件；未取得「未改动自然存档 + 一条自然玩家路线」的 Tk 截图 A/B。未用 trace 或测试冒充玩家证据。
- bug 复现描述来自玩家报告（多名 NPC 多重绝顶后连锁、堆叠大量口上）。
