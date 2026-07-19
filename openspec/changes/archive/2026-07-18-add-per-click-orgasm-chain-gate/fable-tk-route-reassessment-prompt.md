/investigate-game-bug

请以怀疑视角为 erArk 的“同一次玩家点击内，刚完成实际高潮释放的 NPC 不应再次进入普通或群交 AI”候选裁定下一条真实 Tk 证据路线。不要假设当前候选一定值得上游 PR，也不要把出现“绝顶”文字等同于命中门禁。请用工具读取当前代码、测试、OpenSpec 和必要的生产存档/配置；事实以实际调用参数与正常游戏状态为准。

基线：`upstream/master@72e28051ebaaabb069d06059b4633fda90b0b621`
候选工作树：`/home/ubuntu/games/erArk-pr-per-click-orgasm-chain-gate`
当前记录：

- `/home/ubuntu/games/erArk/openspec/changes/add-per-click-orgasm-chain-gate/design.md`
- `/home/ubuntu/games/erArk/openspec/changes/add-per-click-orgasm-chain-gate/tasks.md`
- `/home/ubuntu/games/erArk/openspec/changes/add-per-click-orgasm-chain-gate/current-upstream-implementation-notes.md`
- 本地测试：候选工作树的 `tests/test_per_click_orgasm_chain_gate.py`

已验证代码事实：候选只在一次外层 `game_update_flow` 生命周期中记录实际完成至少一次非玩家高潮释放的 NPC；普通 AI 和群交 AI type 1/2 在后续调度前跳过该 NPC，其他 NPC 与下一次点击不受影响。真实 owner、嵌套 update、普通 AI、群交 AI、时间停止、玩家、零释放和第二 NPC 的聚焦矩阵为候选 `16 passed`；干净 current-upstream 同矩阵为 `11 failed, 5 passed`。新规则评分 `a=36,b=3,S=27,U=0,penalty=66`；新鲜代码 reviewer 已 PASS。两次 Fable 代码/设计调用此前都在 300 秒内无输出超时，不是 verdict。

真实 Tk 探索已使用 production-equivalent copied launcher，只在所有最终模块导入后安装只读 wrapper，baseline/candidate 将使用相同 overlay/hash。无 GUI smoke 证明 wrapper 与 `second_behavior.orgasm_settle`、普通 `handle_npc_ai.find_character_target`、群交 `handle_npc_ai_in_h.npc_ai_in_group_sex` 的真实消费方模块对象完全相同，并记录到真实 group AI call/return。

已否决路线：自然存档中的 11:52 群交现场，玩家点击 `[6001]等待五分钟`。结果队列先显示凯尔希已排队的“阴道小绝顶”二段文本；到“5分钟过去了”数值页才命中新的 `orgasm_settle`，但真实参数是 `normal_orgasm_dict` 中 v=-1、h=-9 的负回调，不是本次点击实际完成高潮释放。没有满足 `part_count >= 1` 的登记，也没有“实际释放后再次进入 AI”的因果链。因此这条路线不能作为 baseline 红灯或 PR evidence，继续走后续 NPC 页面也不会修复该缺陷。

证据要求：必须是正常 Tk 玩家流程。基线和候选使用同一存档、seed、`PYTHONHASHSEED`、窗口、物理输入与只读 observer。trace 必须先显示某非玩家 NPC 在本次外层 update 中以正计数完成真实 `orgasm_settle`，随后 baseline 同一 NPC 又进入普通或群交 AI；候选必须在相同前置画面/状态下缺少这次重入，同时其他 NPC 或下一次点击仍正常。PR-facing 还需要一组人类能理解的完整分辨率可见结果，trace 仅作本地因果证明。

请裁定：

1. 上述 attempt6 否决是否正确；若不正确，请指出被遗漏的真实正释放或调度事实。
2. 读取生产路径和可用存档后，给出最可能成功的下一条正常玩家路线：起始存档/状态、具体玩家操作、应命中的正释放来源、随后可能重入的 ordinary/group AI 入口，以及预期可见差异。优先已有自然存档；若必须先通过正常游戏制作专用 reproduction save，请给最短制作步骤。
3. 是否存在一条更简单的 sibling route（普通场景而非群交、时间停止解除、玩具/持续快感、等待更长时间等），能稳定产生同点击正释放并随后再调度；请说明为什么生产时序允许它。
4. 哪些 evidence-only overlay 可以接受为观察/固定随机性，哪些状态注入会把证据降级为 synthetic、不能支持上游 bug 说服力。
5. 如果正常玩家流程无法在可见结果中区分 baseline/candidate，明确给出最小下一证据或停止该上游 PR 的条件；不要用测试或 trace 替代 skill 要求的真实 Tk 可见 A/B。

输出明确的 `ROUTE PASS`（给一条冻结路线）、`EXPLORE`（给一个有限探索问题）或 `STOP UPSTREAM EVIDENCE`。不要修改文件、不要启动 GUI、不要起草 PR 文案。
