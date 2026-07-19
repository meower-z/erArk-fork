/review-erark-pr-artifacts
/investigate-game-bug

作为 fresh-context upstream reviewer，只读审查，不修改任何文件。必须按 `review-erark-pr-artifacts` 完整执行 visibility ledger、cumulative prefix audit、draft/evidence audit，并以 `PASS`、`REVISE` 或 `BLOCKED` 开头。

审查包四项如下：

1. 候选工作树与精确 refs
   - worktree: `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc`
   - base: `upstream/master` `94d586840484adf21fcf746dba0444551dd6a5a1`
   - head: `4e226f4f587b82a87368a3d7976650593323a7b4`
   - 请实际运行 `git diff --name-status 94d586840...4e226f4f5` 和完整 diff。提交只包含四个 production 文件，没有提交 tests、generated data 或 evidence 文件。

2. 完整 proposed diff
   - 以以上 exact base/head 的 `git diff` 为唯一提交边界，不使用 OpenSpec 或本地测试替 PR 声称兜底。

3. Fable 5 high authored PR draft
   - copyable draft: `/tmp/erark-discovery-settlement-ad-hoc-pr-draft-20260715.md`
   - 初稿与每次 Fable 修订的 prompt/output 原文在 `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/` 下这些文件：
     - `fable-ad-hoc-pr-draft-wait-boundary-prompt-20260715.md`
     - `fable-ad-hoc-pr-draft-wait-boundary-output-20260715.md`
     - `fable-ad-hoc-pr-draft-wait-boundary-revision-prompt-20260715.md`
     - `fable-ad-hoc-pr-draft-wait-boundary-revision-output-20260715.md`
     - `fable-ad-hoc-pr-draft-evidence-name-correction-prompt-20260715.md`
     - `fable-ad-hoc-pr-draft-evidence-name-correction-output-20260715.md`
   - 所有成功 writer/revision 调用均为 `claude-fable-5`、effort high、`--no-session-persistence`；draft 只提当前问题与当前修复，不应包含旧实现或内部历史。

4. 这次 intended PR evidence（pending publication；正文 URL 仍是占位符）
   - before PNG: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/baseline-missing-closure-response-clean.png`
   - after PNG: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/candidate-closure-response-once-clean.png`
   - provenance manifest: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/MANIFEST.md`
   - written physical-input route: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/action-log.tsv`
   - checksums: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/CHECKSUMS.sha256`
   - 请实际以原分辨率打开两张 PNG，并读 manifest/action log。它们来自真实 Tk、同一 save/route/seed、由本地视觉 agent 逐帧 xdotool 操作，clean crop 与对应 raw frame 的像素区域一致；用户已批准这两张 clean static PNG。它们只证明“与杜宾 H、可露希尔发现、选 1 判定成功”这条漏反应案例：before 无可露希尔反应，after 可露希尔反应恰好一次后杜宾 H 文本继续。

重要当前事实：图片最初是对较早的、同样修复该可见漏反应的候选 refs `06fc59c1e7...5d360f71ec` 采集，不是当前 base/head 的重跑。当前最终 diff 保持相同四 production 文件、相同面板局部补结算行为，但实现形状后来缩小，并新增一行仅影响“发现反应之后寻路失败回退 WAIT”的边界。主证据路线寻路成功并继续 H，不走这个 WAIT 边界。用户在本轮明确指示“这次就不要重新跑 Tk 了”，因此必须评估已批准图片是否足以作为当前 draft 的 pending-publication representative evidence；不得要求或启动新的 Tk 运行。若这一 provenance 差异按规则只能构成 blocker，请明确说出，不得假装是 final-head 截图。

重点核验：

- 标题和每个 cumulative prefix 是否先讲玩家可见问题、再讲原因和修复，不依赖后文救场。
- 四个“局部补结算”分支是否准确：`SEE_H_BUT_DECEIVED`、`SEE_H_BUT_IGNORE`、`SEE_H_AND_LEAVE`、`DISCOVER_OTHER_SEX_AND_JOIN`；`JOIN_GROUP_SEX` 原本已经结算，draft 不得把它说成缺失。
- 完成标记对应 JOIN、DISCOVER、IGNORE、INTERRUPT，外层不重放；REFUSE、DECEIVED、LEAVE 在真实 `MOVE` 时外层继续结算移动、无路 `WAIT` 时跳过；direct hidden caller 不虚构 NPC round。
- 图片角色名必须是杜宾与可露希尔，不是多萝西或闭锁；图注不得扩大到所有分支、重复发现或 WAIT 边界。
- draft 不得出现旧方案、内部探索、OpenSpec/worktree、本地测试、计数、agent 名称、本地路径等 PR 不可见内容。
- 没有 public URLs，因此即使 PASS 也只能是 `publication_state: local-review-ready`。

如果是 `REVISE`，给出精确 draft 行号和必须修改的最小文字，不给 optional style preference。如果是 `BLOCKED`，说明具体缺失的 PR-visible proof。无论 verdict，都输出完整 visibility ledger 和 cumulative prefix ledger。
