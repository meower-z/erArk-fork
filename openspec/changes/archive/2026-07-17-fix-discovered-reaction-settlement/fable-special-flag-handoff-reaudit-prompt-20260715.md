# Fable 5 OpenSpec handoff re-audit prompt

```text
/investigate-game-bug

只读交接记录复核：不得修改文件、Git、GitHub 或 PR。上一次 handoff audit 的完整 FAIL 记录在 `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/fable-special-flag-handoff-audit-verdict-20260715.md`。请实际阅读更新后的同一 OpenSpec change 中：
- `implementation-notes.md` 的 `2026-07-15 PR #218 Local Handoff State`；
- `pr-artifact-special-flag-v2-final-review-20260715.md`；
- v2 Fable draft record；
- current PR #218 的只读 GitHub state、评论和 timeline；
- candidate `c75b3b173`、upstream parent `58587de` 与 Tk archive manifest。

核验上轮三个 finding 是否如实解决：线上 body 与本地 v2 未发布草稿的差异、已发生 outward state 的时间/授权或可确认不确定性、artifact-review PASS 留存。用户仍明确要求 PR 不需进一步动作；所有知识进 local main；仅删除 local special-flag worktree/branch，保留 remote ref 和 old ad-hoc checkout。输出仅 PASS 或 FAIL，随后列必须修复 finding（如有）。
```
