/investigate-game-bug

请以怀疑视角只读审查 T2 `judge-orgasm-edge-once-per-settlement` 的 current-upstream 第一次外层等待生命周期记录，并裁决下一次是否可以进行一次有界的路线续探。不要修改文件，不要写 PR 文案，不要因为代码和旧版证据曾通过而默认当前路线值得继续。

已验证事实：

- current upstream/base 是 `72e28051ebaaabb069d06059b4633fda90b0b621`。独立最终代码候选 commit 是 `4b307f1d75ca8d4eb3ec06b8eb827adfe20506f6`，生产 diff 仅 `Script/Design/second_behavior.py`，按最新版 skill 为 `a=19,b=19,S=11,U=0,penalty=49`；focused 11 passed、py_compile 和 diff-check 通过。本次问题只审证据路线，不重新裁代码。
- Attempt 9 使用未修改 upstream、真实 Tk、pristine save99、seed0、`PYTHONHASHSEED=0`。evidence-only wrapper 在首次游戏 import 前冻结 Python/NumPy RNG，并记录每次 `askfor_wait` 的 production call stack 和第一次 outer wait 的 entry/exit；安装前后 RNG fingerprint 相等。
- visual runner 只提交了一次 `[6001]等待五分钟`。随后逐张检查全分辨率画面，只在确认是普通等待页后发送一次空 Return。
- 完成的九次 wait 顺序为：凯尔希阴道小绝顶；0.2 power；凯尔希心理绝顶；0.5 power；凯尔希心理强绝顶；1.0 power；凯尔希双重绝顶；玩家结算页含5分钟过去；NPC阶段页含清流结算、30分钟过去、杜宾行动、成功寸止和杜宾肛肠绝顶寸止。
- 第九次 Return 后出现正常玩法选择面板：可露希尔发现群交，选择 `[1]支开`、`[4]邀请加入群交`、`[5]结束H`。Attempt 9 合同规定任何选择面板都无效，因此没有输入；有 `outer_wait_entry=1`、无 `outer_wait_exit=1`，未提交第二个6001，也未运行候选。save99 前后 hash 相同。
- 完整、校验过的 archive 是 `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/2026-07-15-orgasm-edge-first-wait-lifecycle-attempt9/`；中央记录是 `current-upstream-wait-lifecycle.md`。Attempt 9 是 INVALID 的路线诊断，不是 bug before evidence。
- 旧版证据的目标是比较同一结算批次的寸止结果是否重复；当前 upstream 上正式 A/B 仍必须在 baseline/candidate 用相同存档、seed、物理输入到达匹配触发。当前候选尚未运行。

待裁决的单一步骤：是否允许下一次路线诊断在完全相同设置下，重放已映射的九个 wait，仅当出现同一名可露希尔、同一三项选择的面板时选择可见的 `[4]邀请加入群交`，然后继续逐页检查，但只映射到第一次 `outer_wait_exit` 并立即停止，严格禁止第二次 `[6001]`。

请判断：

1. `current-upstream-wait-lifecycle.md` 对 Attempt 8 的纠正、Attempt 9 的九页顺序、INVALID 状态和后果是否准确，文档是否 PASS；有事实错误时给最小修正。
2. 上述单次续探是否是合理且有界的下一步，还是应把 current-upstream 路线冻结为 evidence blocker。不要把发现面板本身当 bug 证据。
3. 若允许，明确完整合同：固定输入、预期面板身份/选项、join 成功或失败哪个结果可接受、之后允许出现哪些 wait 或选择、任何意外面板/拒绝/角色差异时如何 INVALID、何时认定第一次 `outer_wait_exit` 完成、如何停止并证明没有第二个6001。
4. 即使路线续探成功，何种事实仍只算 route map，何时才足以启动正式 baseline/candidate A/B；不得用 trace、日志或旧版截图替代 current-upstream 可读 Tk 前后图。
5. 只有确实必须由玩家决定时才写 `PLAYER INPUT REQUIRED`；否则按 stopping rule 给出可执行裁决。

请以 `PASS`、`REVISE` 或 `BLOCKED` 开头，分 `DOCS`、`NEXT STEP`、`BOUND CONTRACT`、`EVIDENCE GATE`。不要修改任何文件。
