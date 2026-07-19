/investigate-game-bug

直接基于下列已核验材料作最终裁定并起草最小文档 patch。没有工具可用，不要请求 Bash/读取文件；需要的原文都在这里。上一调用因尝试禁用工具而没有裁定，已记录为无效。请保持怀疑视角：不能由 PR 已存在倒推玩家确认/外发授权已发生，也不能把开放 PR 写成完成。

事实：PR #215 `OPEN`、非 draft、未合并，URL `https://github.com/Godofcong-1/erArk/pull/215`，head `364ac6d9fc7022f9e69e238e8f3e80481ed40ae5`，1 commit/1 file/10 additions/10 deletions；唯一生产 diff 是 `Behavior_Effect.csv` 中 plural_orgasm_2..11 各加 997。PR API base `abebf33b...`，实时 master `3a1c9e620...`。该 CSV 在候选父提交、#214 后 base、当前 master 的 blob 相同；current-master 与 head merge-tree 无冲突。CI 唯一失败步骤是 Create Release，精确错误 `Resource not accessible by integration`；buildconfig、cache、PyInstaller、全部打包、artifact upload 成功。没有 review/comment。PR 正文使用既有 Fable 定稿并已把两张图占位符替换成 commit-pinned public URL。

当前文档须改的原文：

1. `program-task-map.md` upstream boundary 目前止于：“PR #214 is MERGED ... present in upstream/master@abebf33.”；任务行是：“`settle-remote-plural-orgasm-silently` is 14/14 locally complete at candidate `364ac6d9f` on a fork side branch. A pushed side branch is not an upstream PR. Before submission, refresh and reverify against post-#214 upstream, obtain final user semantic confirmation, and obtain outward authorization.”；stop rule 是：“... `settle-remote-plural-orgasm-silently` needs final semantic confirmation before submission ...”
2. umbrella `tasks.md` 2.5 是：“`settle-remote-plural-orgasm-silently` is locally complete at `364ac6d9f` on a fork side branch; before an upstream PR it needs post-#214 refresh/reverification, final user semantic confirmation, and outward authorization”
3. `task-migration.md` 当前行与 2.5 同义，写 fork branch “which is not an upstream PR”。
4. owning `pr-draft.md` 顶部是：“This draft is written by fable-5 and has not been submitted.”，正文图为 `BEFORE_URL`/`AFTER_URL`。为保持草稿历史，可只改顶部状态并链接 #215，不必把草稿正文变成 published snapshot；请最终选择。
5. owning `implementation-notes.md` 第 8 行说 artifact review pending，但后文已记录 PASS；第 78 行说 `unsubmitted PR text`；还没有 #215/head/CI/current-master compatibility 段落。
6. owning `tasks.md` 历史阶段 `Prepare the unsubmitted PR package` 与已完成 4.4 “Stop for user review before uploading images, pushing branch, or creating PR”。没有找到其后玩家最终语义确认和逐项外发授权的耐久记录。不要回改历史 checkbox；请决定是否新增 tracking section。

历史 Fable prompt/verdict、`fable-program-doc-reconciliation-20260714.md`、`fable-final-program-doc-quality-{prompt,ruling}-20260714.md` 必须逐字不动。

请在 1400 字内给：

1. 单一分类（建议候选之一：`open-upstream-tracking`）。
2. 五份当前文档 + owning tasks 的可直接应用替换/新增文字。
3. 是否要求 current-master 本地重验；若要求，给最小检查。
4. CI 是否 blocker 及精确表述。
5. 缺失授权记录是否要求玩家现在介入。当前不会再改/推/评/关 #215；本地其他任务仍可继续。
6. 修改后检查命令。不要修改代码或远端。
