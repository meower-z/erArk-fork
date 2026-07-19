# Fable 5 OpenSpec handoff-audit prompt

```text
/investigate-game-bug

只读 OpenSpec handoff record 接受审查：不得修改文件、Git、GitHub 或 PR。请实际读取：
- OpenSpec change `/home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/` 的 `implementation-notes.md` 末尾 `2026-07-15 PR #218 Local Handoff State` 段；
- candidate commit `c75b3b1737f5ab958b520e568d8aead59cd1d413`、其 parent `58587deac62149d80c82b5a3c98ad29f51cfe2b4`；
- local Tk archive manifest `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-special-flag-c75b3b173-20260715/MANIFEST.md`；
- final Fable PR-draft record and review evidence in this same change；
- current PR #218 state (read-only gh query allowed)。

用户明确要求：PR 不需进一步动作；知识必须进入 local main；仅删除这次的本地 special-flag worktree/branch，保留远程 PR ref 和旧 local ad-hoc checkout。请判断该 handoff section 是否准确、是否保留足够知识而不引入未证实事实。输出仅 PASS 或 FAIL，随后列出必须修复 finding（如有）。
```
