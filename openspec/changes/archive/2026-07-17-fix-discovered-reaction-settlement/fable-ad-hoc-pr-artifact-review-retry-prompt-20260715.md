/review-erark-pr-artifacts
/investigate-game-bug

Fresh-context、只读、简洁审查，不修改文件。输出必须以 `PASS`、`REVISE` 或 `BLOCKED` 开头，并包含精简 visibility ledger 与 cumulative prefix ledger；不要写长篇背景复述。

审查包：

- worktree `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc`
- exact base `94d586840484adf21fcf746dba0444551dd6a5a1`
- exact head `4e226f4f587b82a87368a3d7976650593323a7b4`
- copyable PR draft `/tmp/erark-discovery-settlement-ad-hoc-pr-draft-20260715.md`
- intended pending-publication before `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/baseline-missing-closure-response-clean.png`
- intended pending-publication after `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/candidate-closure-response-once-clean.png`
- provenance `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/MANIFEST.md`
- physical route `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/action-log.tsv`

请实际读取完整 base...head diff、draft、manifest、action log，并打开两张 PNG。提交边界只有四个 production 文件，无 tests/evidence/generated data。PR draft 由 `claude-fable-5` effort high 原创并经同模型 high 修订，provenance 记录位于 `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/fable-ad-hoc-pr-draft-*-20260715.md`。

核验：

1. 文案顺序是玩家可见问题 → 原因 → 当前修复 → 两图验证；没有旧方案、内部历史、本地测试或路径。
2. 缺结算四分支准确为 DECEIVED、IGNORE、LEAVE、DISCOVER；JOIN 原本已结算。完成标记对应 JOIN、DISCOVER、IGNORE、INTERRUPT。REFUSE/DECEIVED/LEAVE 的真实 MOVE 本轮继续结算，无路 WAIT 跳过；direct caller 不虚构 NPC round。
3. 图中是与杜宾 H、被可露希尔发现；before 无可露希尔反应，after 恰好一次后杜宾文本继续。图注只声称该漏反应案例，不声称图证明 WAIT 或所有分支。
4. 两张图来自真实 Tk、同 save/route/seed、逐帧 xdotool 操作且已由用户批准，但 manifest 的 refs 是较早的 `06fc59c1e7...5d360f71ec`，不是当前 base/head。当前 diff 仍修复同一可见漏反应；后来缩小实现并增加的唯一新语义是无路 WAIT 跳过，主证据路线不走 WAIT。用户明确要求这次不要重跑 Tk。必须诚实判断旧图能否作为当前 diff 的 representative pending-publication evidence；不能假装是 final-head 图，也不得要求或启动新 Tk。
5. URL 尚为占位符，所以即使 PASS 也只能 `publication_state: local-review-ready`。

若 `REVISE`，只列必须改的 draft 行号与最小修改；若 `BLOCKED`，只列缺失的 PR-visible proof。Visibility ledger 至少分类 implementation diff、submitted tests、two PNGs、manifest/route、public URL；prefix ledger 可按标题/问题/原因/修复1/修复2/修复3/边界句/验证分组，每项一行。
