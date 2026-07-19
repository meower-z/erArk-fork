/investigate-game-bug

只修订 erArk PR 文案，不修改文件。原稿逐字位于 `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/fable-ad-hoc-pr-draft-wait-boundary-revision-output-20260715.md`。精确 diff 仍是 `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc` 的 base `94d586840484adf21fcf746dba0444551dd6a5a1`、head `4e226f4f587b82a87368a3d7976650593323a7b4`。

直接查看并以这两张 clean PNG 为准：

- `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/baseline-missing-closure-response-clean.png`
- `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/candidate-closure-response-once-clean.png`

原稿的验证句和 before 图注误写为“多萝西”。图中实际是玩家与杜宾 H，被可露希尔发现；baseline 的可见结果是可露希尔没有反应，杜宾的 H 文本直接继续；after 是可露希尔的被支开反应恰好出现一次，随后杜宾的 H 文本继续。请只做这项事实修正，并保留两个 URL 占位符。不要改动其他已经核对的标题、问题、原因、修复范围和 MOVE/WAIT 设计说明。

继续禁止提及任何旧实现、内部历史、OpenSpec、worktree、本地测试或本地路径。只输出完整的修订后 PR 标题和正文，不要解释修改过程。
