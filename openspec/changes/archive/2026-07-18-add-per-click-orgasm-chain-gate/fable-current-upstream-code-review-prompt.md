/investigate-game-bug

请作为怀疑性的最终代码裁决者，审查 erArk 候选 `add-per-click-orgasm-chain-gate`。不要把先前设计文档或本提示里的实现描述当作正确结论；请亲自读取当前 skill、OpenSpec、生产 diff 和测试，寻找逻辑漏洞、范围遗漏、过拟合测试以及更低罚分但同样正确的边界。你可以给 PASS、REVISE 或 BLOCKED。

权威位置：
- 主工作树文档：`/home/ubuntu/games/erArk/openspec/changes/add-per-click-orgasm-chain-gate/`
- 候选工作树：`/home/ubuntu/games/erArk-pr-per-click-orgasm-chain-gate`
- 基线与候选提交基点：`upstream/master@72e28051ebaaabb069d06059b4633fda90b0b621`（包含已合并 PR #216）
- 生产 diff：候选工作树中 `git diff HEAD -- Script/Design/update.py Script/Design/second_behavior.py Script/Design/handle_npc_ai.py Script/Design/handle_npc_ai_in_h.py`
- 聚焦测试：候选工作树 `tests/test_per_click_orgasm_chain_gate.py`
- 生产 diff SHA-256：`e67adab58c6c4bda770420e1014fe16326e7fba551fbb0e8c6065a1843d897b0`

玩家已经确认的玩法规则：同一次最外层玩家点击中，NPC 第一次实际高潮释放事务完整结束后，不再生成新的自主行为；仍接受刺激、被动高潮和全部结算；下一次点击立即恢复。不是冷却、眩晕或存档状态。玩家、成功寸止、时停只蓄积均不登记。

当前候选实际做法：
- `update.py` 用模块私有 set 保存本次点击已实际释放的 NPC；最外层入口与 finally 清空，nested 更新复用。
- 两个窄函数负责登记和查询。登记函数只在 `character_id != 0` 且 `game_update_flow_running > 0` 时写入，查询只做集合成员判断。
- `second_behavior.orgasm_settle()` 在函数最末尾、全部多部位/复数/派生/发电结算之后，`part_count >= 1` 且 NPC 时登记。
- `handle_npc_ai.find_character_target()` 在第一次目标搜索前拒绝已登记 NPC，加入 `over_behavior_character` 后返回；现有 caller 随后仍执行 `judge_character_status` 和 realtime/persistent/interrupt/time-over/talent 尾部。
- `handle_npc_ai_in_h.npc_ai_in_group_sex()` 的玩家早退扩为“玩家或已登记 NPC”，发生在 type-1 自慰写入和 type-2 模板写入之前。当前无生产调用者的 type-3 函数未改。

自动化实跑：
- 当前候选：`15 passed`。
- 全新 detached 当前上游基线、同一测试和源码选择：`9 failed, 6 passed`。
- 红灯覆盖：完整多部位释放未登记；后续被动高潮仍需完整执行；寸止失败与时停蓄积必须到实际解放后才登记；nested 复用、outer 正常/异常清理、下一点击清空；普通 AI 搜索前拒绝；群交 type-1/type-2 写入前拒绝。
- 反向保护覆盖：玩家、成功寸止、时停蓄积不登记；只登记 active click 内 NPC；两名 NPC 隔离且重复登记幂等；未登记普通/群交 NPC 仍走原入口；被拒绝的 SHARE_BLANKLY NPC 仍执行 `judge_character_status` 并完成。
- `py_compile` 与 `git diff --check` 通过。
- 尚未完成真实 Tk A/B；这不是本轮 PASS 可以替代的证据。
- 直接从一个未初始化的短 Python 命令导入完整生产模块会卡在项目既有的配置/导入副作用；测试因此 AST 提取真实函数体。请判断这是否留下必须先补的真实加载测试，而不是默认接受。

按刚更新的评分 skill，生产 diff 丢弃空白行后精确计数为：`a=33, b=2, S=25, U=0, penalty=60`。八个 change group 的 `(a,b,S)` 是 `(1,0,0) (3,0,2) (1,1,0) (1,1,0) (2,0,1) (21,0,20) (2,0,1) (2,0,1)`。高附加主要来自 `update.py` 的模块状态、两个符合项目中文函数说明要求的窄接口，以及两处生命周期清理。

请特别质疑：
1. 模块私有 set 是否真由最外层 update 正确拥有，热重载、换 Cache、异常、深度上限 return 是否可能泄漏；
2. 注册点是否足够晚，寸止失败 replay 与时停解放是否实际可达并只在 release 后登记；
3. 普通、群交 type-1/type-2 是否覆盖所有生产可达的“新自主行为”入口；type-3 无调用是否足以排除；
4. `over_behavior_character` 早退是否在真实循环中仍保留被动二段结算并避免挂起；
5. 未来 T2 对 `orgasm_settle` 的改动是否形成需要现在处理的边界冲突；
6. 是否存在 penalty 明显低于 60、同时保持模块私有状态、active-click-only 登记、集中生命周期、跨模块只读契约和项目正常风格的正确候选。不要建议为了分数压缩/删除必要 docstring，或把生命周期知识散到多个调用者；但如果这些约束本身并非硬门槛，请明确指出并给出可落地的较低分方案。

输出要求：先给 `PASS` / `REVISE` / `BLOCKED`。如果不是 PASS，列出每个必须修改项和能让它转为 PASS 的最小证据；如果 PASS，明确说明自动化代码边界是否通过、真实 Tk 和 PR 文案/审计仍然待做。给出你复算的 `a,b,S,U,penalty`，并判断当前设计记录是否可把自动化相关任务标为完成。
