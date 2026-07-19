/investigate-game-bug

你是 erArk 本地 bugfix program 文档的最终监督者和 patch 作者。请以怀疑视角处理一个外部状态变化：本地文档仍把 `settle-remote-plural-orgasm-silently` 写成“只有 fork side branch、尚无上游 PR”，但 GitHub 现在已有开放 PR #215。只请裁定并起草最小文档修整；不要修改生产代码、测试、PR、GitHub 状态或历史 Fable prompt/verdict。不要因为 PR 已经存在就倒推出玩家确认或外发授权曾发生，也不要因为缺少这段过程记录就否认 GitHub 的当前事实。

## 已由主协调者实时核验的 GitHub 事实

- PR #215：https://github.com/Godofcong-1/erArk/pull/215
- title：`修复：NPC 异地发生的多重绝顶被延迟到玩家在场时才显示和结算`
- `OPEN`，`isDraft=false`，`mergedAt=null`，创建时间 `2026-07-14T11:28:31Z`。
- head：`meower-z/erArk-fork:codex/settle-remote-plural-orgasm-silently`，精确 SHA `364ac6d9fc7022f9e69e238e8f3e80481ed40ae5`；其父提交为 `06fc59c1e71d092224375fc4a096b956aea2ad63`。
- GitHub API 当前 PR base SHA 报告 `abebf33b52ebf51424f71365946eb8df1f75a23c`；实时 `upstream/master` 已是 `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`。
- `MERGEABLE`，merge state `UNSTABLE`；没有 review、comment、review request、label 或 assignee。
- 1 commit、1 file、10 additions/10 deletions。唯一生产差异是 `data/csv/Behavior_Effect.csv` 中 `plural_orgasm_2` 至 `plural_orgasm_11` 十行各追加 `997`。
- `Behavior_Effect.csv` 在 `06fc59c1`、`abebf33b`、当前 `3a1c9e6` 的 blob 都是 `11f971ab6e8fbfec549dd71f7f49e97738267b02`；候选 blob 是 `cfd7accc3a41abd6da353618dbdb3991ee40858a`。`git merge-tree --write-tree 3a1c9e6 364ac6d9f` 成功得到 tree `b8da4daf...`，没有冲突。
- PR 正文与 Fable 定稿内容一致，两个占位图已替换成 commit-pinned public raw URLs。

## CI 精确状态

- `build-windows` 整体为 FAILURE，run `29329019019`，job `87072184906`。
- Checkout、依赖安装、PyInstaller、Build Game Config、Build Game Cache、全部打包、ArkEditor、artifact upload 等步骤均 success。
- 唯一 failure 是 `Create Release`，日志精确错误：`Resource not accessible by integration`；后续四个 release-asset upload 因此 skipped。
- 因此文档可以说“构建/配置/打包与 artifact 上传均成功；Create Release 权限步骤失败”。不能简称“CI 通过”。把它解释成 PR workflow token 权限而非候选代码问题是有支持的推断，不是已证明事实。

## 当前文档中的错误时态

以下五份是当前状态文档，允许机械更新：

1. `program-task-map.md`
   - upstream boundary 只列 #212、#213、#214，且把 master 表述停在 `abebf33`。
   - 第 70 行写候选只在 fork side branch，`A pushed side branch is not an upstream PR`，提交前需 refresh、玩家确认和外发授权。
   - stop rule 第 129 行仍写该任务“before submission”需要最终确认。
2. umbrella `tasks.md` 第 15 行同样写 `before an upstream PR`。
3. `task-migration.md` 第 268 行同样写 fork side branch `which is not an upstream PR`。
4. owning change `pr-draft.md` 第 3 行写 `This draft is written by fable-5 and has not been submitted.`；正文仍保留 `BEFORE_URL`/`AFTER_URL` 占位符，而 GitHub 已使用公开图片链接。
5. owning change `implementation-notes.md`
   - 第 8 行仍写 fresh artifact review pending，但第 86 行已经记录 review PASS。
   - 第 78 行仍称 `unsubmitted PR text`。
   - 没有 PR #215、当前 head、CI 或 current-master compatibility 状态。

owning `tasks.md` 的阶段标题是 `Prepare the unsubmitted PR package`，可保留为历史阶段；但第 4.4 是 `[x] Stop for user review before uploading images, pushing the branch, or creating the PR`。本 change 内没有找到随后“玩家最终语义确认”和“逐项外发授权”如何满足的耐久记录。当前会话也不能从 GitHub 事实倒推它们。请决定是否新增一个未完成 tracking section，而不是回改历史 checkbox。

## 必须保持逐字不动的历史材料

- `fable-program-doc-reconciliation-20260714.md`
- `fable-final-program-doc-quality-prompt-20260714.md`
- `fable-final-program-doc-quality-ruling-20260714.md`
- owning change 中所有既有 `fable-*-prompt.md`、`fable-*.md` verdict/output

这些文件记录的是当时真实状态。只能用本次日期化 prompt/ruling 和当前文档的新段落 supersede，不能重写旧 Fable 原话。

## 需要你作最终决定并起草 patch

1. 给出 #215 的当前分类：`open-upstream-tracking`、`local-complete`、`complete/retirable` 或你认为更准确的单一分类。它尚未合并，不得偷换成完成。
2. 给出上述五份当前文档的最小精确修改。请尽量提供可直接应用的替换段落/新增 checklist，不要只给原则。
3. 旧 head 未 rebase 到 #214/当前 master，但相关 CSV 三个 base 版本完全相同、merge-tree 无冲突。是否仍要求在本地构造 current-master integration 并重跑 focused regression/buildconfig/diff check？若要求，请明确最小命令级检查和它是否阻塞文档校正；若不要求，也要说明为何。
4. CI 在 release 权限步骤失败。它是否是候选 blocker？当前文档应如何准确记载，避免“CI failed = code failed”或“CI passed”两种误述？
5. 对缺失的玩家语义确认/外发授权耐久记录，文档应只写“记录未知”，还是必须现在让玩家补确认？请决定是否形成 `player-input stop`。注意我们当前不会再修改、push、rebase、close、comment 或 otherwise touch #215；用户已明确要求本地工作继续，只有你认为确实需要玩家介入才暂停。
6. 是否应把 local `pr-draft.md` 更新为 published snapshot（嵌入实际 URL），还是保留当时 draft 并只在顶部添加发布状态与 GitHub 正文链接/差异说明？请选择最利于未来审计且不篡改历史的方案。
7. 明确列出哪些历史文件不可改，以及本轮修改后需要跑的 OpenSpec/document checks。
