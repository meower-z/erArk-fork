/investigate-game-bug

请以怀疑视角审查 T7 目标泄漏证据路线的新反证、已撤回的静态可达性结论，以及是否还存在一个具体有限的下一步。不要替静态模型辩护，也不要因为候选代码测试通过而降低真实 Tk 门槛。

请读取：

- `openspec/changes/fix-talk-common-state-leaks/target-scope-save99-v-reachability.md`
- `openspec/changes/fix-talk-common-state-leaks/target-scope-implementation-notes.md`
- `openspec/changes/fix-talk-common-state-leaks/tasks.md`
- `/tmp/erark-t7-seed-search-20260715/seed-00-choice4-bound.log`
- 需要时读取当前上游 `handle_npc_ai_in_h`、`character_behavior`、自慰 state machine、effect 524、`orgasm_judge` 与发现面板代码。

已验证事实：

1. save99 当前目标 A 是凯尔希；场景十一人，其中十名 NPC，故不同 B 候选九名。
2. 静态模型曾认为一次 `[6001]` 会让旧 `masturebate` 行为结算两次，因此特蕾西娅或林若两次都随机选 V 就会跨阈值。文档现已明确将它标为被反证的假设，不再声称路线可达。
3. 完整 seed0 诊断保留正常 startup/load，CID213 通过七次真实设置 callback 从30%调到100%且 RNG hash 不变；执行一次真实 `[6001]`。
4. 期间出现可露希尔和陈两个发现面板，均真实选择 `[4]邀请加入群交`。两人的口上是普通 `join_group_sex`，`common_behavior_id=None`，前后 target 都是3；因此没有更早 target 泄漏。
5. 命令在11:57正常完成。特蕾西娅 V 803→840，林 5379→5416；两人 effect_parts 为空，没有 `handle_masturebate_add_adjust`/effect524、没有跨阈值、没有二段绝顶、没有 Talk_Common。存档哈希未变。
6. 这直接推翻“首个等待必然调用两次 effect524”。随机 seed 不能选择一个未发生调用的部位，因此 0..63 扫描已暂停。
7. 当前文档把任务3.2恢复为 `TK EVIDENCE BLOCKER`，不声称 PR-ready。

请裁决：

- 文档是否准确撤回错误结论、保留有用算式而不会误导新人；
- 这个反证是否足以停止 seed 扫描；
- 只选一个下一步：A) 沿真实 seed0 trace 静态追踪为什么 save 中旧 masturebate 没有进入 effect524，并判断一个明确的正常状态/等待时点是否会调用；B) 当前 save99 路线证据已不值得继续，冻结目标泄漏候选为代码级 bug、但保持 Tk/PR blocked；C) 一个比 A 更窄且能直接区分状态生命周期的步骤。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头。若文档需改，指出精确表述；无论结论如何，只选择一个下一步，说明成功/失败分别证明什么。不要写 PR 文案，不要建议开放式试玩或继续盲扫 seed。
