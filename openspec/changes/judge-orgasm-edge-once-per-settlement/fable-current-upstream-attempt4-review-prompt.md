/investigate-game-bug

请以怀疑视角审查 erArk OpenSpec `judge-orgasm-edge-once-per-settlement` 在当前上游重放失败后的状态修正，并决定唯一一个最有信息量的有限下一步。不要假设旧证据仍有效，也不要因为代码测试通过而降低玩家可见证据门槛。

请用工具读取：

- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt4-invalid.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/pr-readiness.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/design.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/tasks.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/formal-current-20260715-attempt4/action-log.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/formal-current-20260715-attempt4/INVALID.md`
- 当前候选 worktree `/home/ubuntu/games/erArk-pr-edge-shared-settlement-current` 的生产 diff 与测试（只读）

已验证事实：

1. 当前上游基线 `72e28051ebaaabb069d06059b4633fda90b0b621`；当前候选生产 diff 的规则仍是一次 `orgasm_settle()` 收集完整批次、只判断一次、共享一个结果，聚焦测试 11 passed，生产评分 `a=19,b=19,S=11,U=0,penalty=49`。
2. 旧 2026-07-13 包在更早基线上有一组真实 Tk 图片和旧 artifact PASS；当前文档已将其降为历史材料，不再声称能证明当前包。
3. 2026-07-15 attempt4 baseline 使用 save99、`random/numpy seed=0`、`PYTHONHASHSEED=0`、真实 Tk，同一物理输入合同；恰好六次 `[6001]`。
4. 没有任何发现面板，因此没有输入 `[4]`，也没有猜第七次；candidate 未启动。
5. 六次结果与一张静置帧字节相同，只显示 `凯尔希阴道小绝顶`，未显示清流/特蕾西娅结果簇；日志无异常，存档哈希未变，allocator 已清空。
6. 因为目标结果路径没有可见触发，本轮不能区分发现前提失败与后续寸止结算，也不能作为 A/B 证据。
7. 文档当前把 publication state 降为 `evidence-blocked`，任务 5.6 保持未完成。

请裁决：

- 上述三个状态文档是否准确、对新人清楚、没有残留的当前 readiness 夸大；
- 是否应保留旧图片/PR 文案作为明确标记的历史材料；
- 下一步应优先做哪一个有限诊断：A) 在只读/诊断运行中逐次观测相关角色高潮计数和发现前提，解释为什么六次只出现凯尔希；B) 放弃旧角色簇，静态/运行搜索一个当前 save99 上能稳定产生多部位同批绝顶的正常路线；C) 其他更窄且更有区分力的一步。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头的裁决。若文档需改，给出精确句子/事实；无论结论如何，只选择一个下一步，并说明它成功/失败各会证明什么。不要写 PR 文案，不要建议扩大为开放式试玩。
