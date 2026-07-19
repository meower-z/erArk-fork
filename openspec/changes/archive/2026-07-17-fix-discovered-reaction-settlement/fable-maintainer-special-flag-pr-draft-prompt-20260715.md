# Fable 5 PR draft prompt — maintainer `SPECIAL_FLAG` candidate

```text
/investigate-game-bug

只读撰写任务：不得修改文件、Git、GitHub 或 PR。你是 erArk 上游 PR 的中文文案作者。请实际读取：
- 候选 worktree /home/ubuntu/games/erArk-pr-discovery-settlement-special-flag，base upstream/master@58587deac62149d80c82b5a3c98ad29f51cfe2b4，head c75b3b1737f5ab958b520e568d8aead59cd1d413；只提交四个 production 文件，没有测试文件。
- 当前 live PR #218 的标题和 body（可用 gh pr view 218 --repo Godofcong-1/erArk --json title,body,url 读取）。
- 已验证的本次 real-Tk evidence manifest：/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-special-flag-c75b3b173-20260715/MANIFEST.md。
- 写作规则与示例：/home/ubuntu/games/erArk/.codex/skills/investigate-game-bug/SKILL.md 的 Write The Upstream PR Draft 和 references/pr-draft-examples.md。

Maintainer 要求：此 special case 不能借用 constant.handle_state_machine_data 的返回值；修复须使用角色 SPECIAL_FLAG。候选的真实边界是：面板内七个显式发现者反应各立即结算一次；state 40 仅在 draw() 返回后把 panel-local completion 写入 SPECIAL_FLAG；NPC 外层对带标记的 WAIT 跳过一次后继结算、对带标记的 MOVE 仍结算并清除标记；direct hidden-discovery caller 不写标记。不要提任何被拒方案、helper、旧 boolean/return-chain、OpenSpec、本地测试、分支、工作树、模型或内部计数。

可公开复用的两张证据图已经在现有 PR body 中，且本次 special-flag Tk replay 对它们逐像素 AE=0：
- before: https://raw.githubusercontent.com/meower-z/erArk-fork/e692de85089a29ec50e9015c8e2eba09e342cd1e/pr-codex-fix-discovery-settlement-ad-hoc/before.png
- after: https://raw.githubusercontent.com/meower-z/erArk-fork/e692de85089a29ec50e9015c8e2eba09e342cd1e/pr-codex-fix-discovery-settlement-ad-hoc/after.png

请输出一份可直接替换 PR #218 的完整草稿，且只输出以下两段：
TITLE:
<一行中文标题>

BODY:
<中文 Markdown 正文，必须依次说明可见问题、原因、修复、验证；用上述图片作 before/after；不列文件名、不声称未提交的自动化测试。>
```
