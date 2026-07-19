# Fable ruling: PR #215 document reconciliation

Invocation: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Prompt: [fable-pr215-document-reconciliation-retry-prompt-20260714.md](fable-pr215-document-reconciliation-retry-prompt-20260714.md).

The first invocation is separately retained as an incomplete, non-ruling
attempt. Exact final response follows.

```text
**1. 分类:** `open-upstream-tracking` — #215 已 OPEN 但未审、未合并、授权记录缺失;只跟踪,不外发。

**2. 替换/新增文字**

`program-task-map.md` upstream boundary 追加:
> PR #215 is OPEN (not draft, unmerged, no reviews/comments): https://github.com/Godofcong-1/erArk/pull/215, head `364ac6d9f`, 1 commit / 1 file (`Behavior_Effect.csv`, plural_orgasm_2..11 +997 each). PR API base `abebf33b`, live master `3a1c9e620`; the CSV blob is identical across candidate parent, post-#214 base, and current master, and merge-tree against current master is clean. OPEN is not MERGED — do not treat #215 as landed.

任务行替换为:
> `settle-remote-plural-orgasm-silently` is submitted as upstream PR #215 (OPEN, unreviewed) from candidate `364ac6d9f`. Tracking only: no edits, pushes, comments, or closure on #215 without fresh outward authorization. No durable record of post-4.4 final user semantic confirmation or per-item outward authorization was found; this gap must be raised with the player before any further outward action on #215.

stop rule 替换为:
> ... `settle-remote-plural-orgasm-silently` is in open-upstream-tracking (#215); stop before any further outward action on it until the missing confirmation/authorization record is resolved with the player.

umbrella `tasks.md` 2.5 替换为:
> `settle-remote-plural-orgasm-silently` is submitted as PR #215 (OPEN, unmerged, unreviewed); tracking only. No durable record of final semantic confirmation or outward authorization after 4.4 was found — raise with the player before any further outward action. Do not mark complete until #215 is MERGED.

`task-migration.md` 当前行改为与 2.5 同义(submitted as PR #215, OPEN, tracking only, authorization-record gap noted)。

`pr-draft.md` **只改顶部,正文原样保留**(草稿历史价值 > 快照同步;live body 以 GitHub 为准):
> Status: submitted as PR #215 (OPEN, unmerged) — https://github.com/Godofcong-1/erArk/pull/215. Body below is the pre-submission fable-5 draft; in the live PR the two image placeholders were replaced with commit-pinned public URLs.

`implementation-notes.md`:第 8 行改为 "artifact review: PASS (recorded below)";第 78 行 `unsubmitted PR text` → `PR text as submitted in #215`;新增段落:
> ## PR #215 submission record (2026-07-14)
> OPEN, non-draft, unmerged, no reviews/comments. URL https://github.com/Godofcong-1/erArk/pull/215; head `364ac6d9f`; sole production diff: `Behavior_Effect.csv` plural_orgasm_2..11 +997 each (10+/10-). PR base `abebf33b`, live master `3a1c9e620`; CSV blob identical on both and on candidate parent; merge-tree vs current master clean. CI: buildconfig/cache/PyInstaller/packaging/artifact-upload all pass; only Create Release fails with `Resource not accessible by integration` — fork-PR token lacks release permission; environmental, unrelated to the diff. Gap: no durable post-4.4 record of player semantic confirmation or per-item outward authorization exists.

owning `tasks.md`:不动历史 checkbox,新增 tracking section:
> ## 5. Upstream tracking (PR #215) — no outward actions
> - [ ] 5.1 Surface to the player: no durable record of final semantic confirmation / outward authorization after 4.4 was found, yet #215 was created; obtain retroactive confirmation or instruction.
> - [ ] 5.2 Monitor #215 state; take no edit/push/comment/close without fresh authorization.
> - [ ] 5.3 If upstream master advances before merge, re-run merge-tree vs new master and re-compare the `Behavior_Effect.csv` blob.
> - [ ] 5.4 Mark the change complete only when #215 is MERGED (then run authorized retirement).

**3. current-master 重验:** 现在不需要。blob 三方一致 + merge-tree 无冲突已覆盖。最小条件性检查(仅当 master 前进,见 5.3):`git fetch upstream && git merge-tree $(git merge-base upstream/master 364ac6d9f) upstream/master 364ac6d9f` 且比对该 CSV blob SHA。

**4. CI 非 blocker。** 精确表述:唯一失败步骤是 Create Release,错误 `Resource not accessible by integration`,系 fork PR 的 GITHUB_TOKEN 无 release 写权限的环境限制;构建、缓存、PyInstaller、全部打包与 artifact 上传均成功,与本 diff 无因果。

**5. 需要玩家介入,但不阻塞本地其他任务。** 授权记录缺失不能由 PR 存在倒推补齐;必须在下次与玩家交互时明示该缺口(5.1),取得追认或指示。在此之前对 #215 零外发动作;其余本地任务照常。

**6. 修改后检查:**
```
grep -rn "not an upstream PR\|has not been submitted\|unsubmitted PR text\|obtain final user semantic confirmation, and obtain outward authorization" openspec/ | grep -v fable-
grep -rln "pull/215" openspec/   # 应含 5+1 份文档
```
并确认两份 fable-*-20260714 文件 `git diff` 为空。
```
