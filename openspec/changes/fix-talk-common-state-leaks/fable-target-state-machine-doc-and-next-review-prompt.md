/investigate-game-bug

请以怀疑视角审查 T7 最新状态机诊断文档，并决定唯一一个后续任务。不要把“存在条件路径”夸大成“已有玩家路线”，也不要因路线随机就建议开放式试玩。

请读取：

- `openspec/changes/fix-talk-common-state-leaks/target-scope-save99-v-reachability.md`
- `openspec/changes/fix-talk-common-state-leaks/target-scope-save99-state-machine-diagnostic.md`
- `openspec/changes/fix-talk-common-state-leaks/target-scope-implementation-notes.md`
- `openspec/changes/fix-talk-common-state-leaks/tasks.md`
- `openspec/changes/fix-talk-common-state-leaks/fable-target-state-machine-contradiction-ruling.md`
- `/tmp/erark-t7-seed-search-20260715/seed-00-state-machine-diagnostic.log`
- 需要时读取 target86/91、SM91/92、flag writers、Behavior_Effect 418 配置。

已验证事实：

1. 单次 seed0 诊断完全复现旧六个rng hash、11:52→11:57、target恒3、V 803→840/5379→5416、存档哈希。
2. 正记录显示 Theresa56/Lin4080 实际选 `default9`、state machine2、behavior wait、mast flag3；effect dispatcher实际序列[9999]，未进418/524。target91三前提缓存只有group/place，mast_flag3项MISSING，因为type12未搜索。
3. 原因：group type1写flag3，但 normal-1 的自慰异常只接受flag1/2或 `npc_masturebate_for_player`，不接受flag3本身；因此target91不在搜索组。
4. 没有behavior418的type0事件；418一旦正常settle，effects456/458/524必经。
5. 后续潜在入口：target86前提满足后，SM91按fall随机可设 `npc_masturebate_for_player=True` 而保留flag3；下一NPC pass type1不清reverse flag，normal-1异常进入type12，87-90因flag1/2失败，91命中并SM92→418。reverse flag的生产清理在同一group/type1/place0路线前不发生；所有mast flag写者和effect412双注册表碰撞已排除。
6. 这只证明条件路径；具体等待次数N取决于save当前desire/fall、正常欲望变化和SM91随机。未继续seed/Tk。任务3.2保持TK EVIDENCE BLOCKER。

请裁决：

- 文档是否把已证运行事实、已撤回模型、静态条件路径和未知N分开，是否有不准确/过度声明；
- 只选一个下一步：A) 只读计算九名B的当前desire/fall、每次正常6001的确定欲望变化与target86首次可满足时点，产出有限N候选后才设计一次受控seed路线；B) 路线随机/多面板成本已不值得继续，把target-scope候选冻结为代码级bug，Tk/PR blocked；C) 比A更窄的一个可判定步骤。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头。若文档需改给精确表述；无论结论只选择一个下一步，说明成功/失败分别证明什么。不要写PR文案、不要提出范围seed扫描或开放式试玩。
