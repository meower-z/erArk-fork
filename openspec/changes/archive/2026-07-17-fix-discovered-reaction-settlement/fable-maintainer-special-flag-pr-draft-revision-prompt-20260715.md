# Fable 5 PR draft revision prompt — maintainer `SPECIAL_FLAG` candidate

Verified invocation:

```text
claude -p --model claude-fable-5 --effort high --no-session-persistence "$PROMPT"
```

Exit status: `0`; elapsed time: `29.1s`.

```text
/investigate-game-bug

只读、外科式 PR 文案修订：不得修改文件、Git、GitHub 或 PR。请实际读取：
- 当前 Fable 草稿 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/fable-maintainer-special-flag-pr-draft-20260715.md
- 候选 diff：/home/ubuntu/games/erArk-pr-discovery-settlement-special-flag，base 58587deac62149d80c82b5a3c98ad29f51cfe2b4，head c75b3b1737f5ab958b520e568d8aead59cd1d413
- fresh artifact-review finding：草稿中“本次修改不改变发现资格判断、话术/露出/H模式/群交的判定逻辑，也不改变同一发现者的再次发现规则和其他状态机分支的行为。”是独立非目标清单，必须删除。

只做这一处删除：保留标题、所有其他段落、七项分支枚举、SPECIAL_FLAG 说明、验证文字和两条图片 URL 的原有措辞与顺序。不要添加替代性非目标句，不要改标题，不要改任何代码术语或图片说明。输出仅：
TITLE:
<标题>

BODY:
<删除该句后的完整中文 Markdown 正文>
```
