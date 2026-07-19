# Fable prompt: final program-document quality review

Invocation contract: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

--- BEGIN EXACT PROMPT ---
/investigate-game-bug

你是 erArk 本地 bugfix 计划的最终怀疑型文档质量监督者。下面提供的是 Codex 实施你 2026-07-14 DOC RECONCILIATION PASS WITH PATCH 后的真实当前文档内容，不是摘要。请审查是否让一个刚进入项目、懂游戏术语但不熟代码结构的人得到准确、可执行、互不矛盾的状态。不要因为三项 openspec strict validate 和 git diff --check 已通过而降低语义标准；不要因为文本来自你的草案就默认正确。只指出会误导任务选择、所有权、完成状态、玩家介入点或外发边界的问题；纯风格偏好不要扩大工作。

一手事实必须保持：
- PR #212 OPEN at 21261e9；PR #213 OPEN at e1a9378，远端仍让睡眠和直接取消都保留 pain_as_pleasure。
- 本地已选但未外发的目标是两条退出都清除；唯一一行 core fix 只属于 clear-pain-as-pleasure-on-hypnosis-cancel，未 commit/push/改 PR/发布。
- PR #214 MERGED at 2026-07-14T10:32:51Z and upstream/master@abebf33 includes it；停止 movement-talk 实现，只剩本地对账与经授权清理。
- T2 是 local-review-ready；固定数日试玩门槛已由你本轮裁定取消，但 PR 创建前仍需用户最终语义确认、post-#214 refresh/reverify、每项外发授权。
- pain composition change 只能消费上述 one-line fix、退役同方向旧 wrapper、验证组合；不能重复拥有 core edit。
- 当前队列是 T4 → T5 elapsed-time → T6 per-click chain → T7 两个 talk leak 默认拆两 PR；depth restoration 是依赖，不单独发 PR。
- 当前 T4 不是旧六-NPC路线。真实 route 是：林4080在四轮口交后保留 deferred counts {0:1,21:2} 和 shoot_position_body=2，正常 UI 切当前目标到惊蛰306，再解除时停。attempt3 formal invalid。attempt4 run1 已证明 target switch/sample2，但回翻旧输出页的 [4115] 可见却 callback 失效。你最新裁定 ROUTE A PASS with mandatory fresh disposable run2：删除 post-switch 可读证明循环，run2 从头到 sample2 后直接点底部活跃 [4115]；run2 尚未启动。因此 docs 可以写“run2 endpoint rehearsal pending”，不能写 formal A/B complete。

我已注意到 program-task-map T4 仍提 six deferred body-part orgasms / six-NPC scene / batch mod both disabled and enabled，这可能是过期边界；请你独立判定，并给精确替换，不要只说“更新一下”。

请给：
1. `FINAL DOC PASS`、`FINAL DOC PASS WITH PATCH` 或 `REVISE`。
2. 按严重性列出所有必须修的问题，逐个给文件、现句问题、精确替换意图。确认哪些历史文字可保留。
3. 特别核对 #212/#213/#214 四态、T2 gate、pain owner、T4 当前证据边界、T4-T7 顺序、local-complete vs upstream-published、玩家介入点。
4. 如果 patch 后不必再问你，请明确“按列出的机械 patch + validate 即可”；如果必须复审，说明理由。
5. 是否需要玩家现在介入。这里不改生产代码、不外发。

以下是实际当前文件内容：

===== CURRENT program-task-map.md =====
# Remaining Local Fix Program

## What this document is

This is the short, current map for the remaining local-fix program. It replaces the old umbrella task list as the place to answer three questions:

1. Which player problem is actually proven?
2. What is the next small reviewable change?
3. Does work need a gameplay choice before an upstream PR?

The detailed investigation history remains in the owning OpenSpec changes. A green mod test or a polished README is not enough to promote a local patch into this queue.

## Current upstream boundary (2026-07-14)

- PR #212 is **OPEN** at head `21261e9` and owns signed pain routing and direct positive-pain effects.
- PR #213 is **OPEN** at head `e1a9378`. Its remote code does not clear `pain_as_pleasure`, so the current GitHub behavior still preserves the flag through both sleep and direct hypnosis cancellation.
- The locally selected target for #213 is different and has **not** been sent outward: the user chose to clear `pain_as_pleasure` on both paths. `clear-pain-as-pleasure-on-hypnosis-cancel` owns the accepted one-line change in shared `clear_hypnosis_sub_states()`. Thirteen checks, `py_compile`, real Tk A/B, and final evidence review pass, but the worktree change is uncommitted; it has not been pushed, used to edit #213, or accompanied by published images. Revising #213 still needs separate outward authorization.
- PR #214 is **MERGED** as of `2026-07-14T10:32:51Z` and is present in `upstream/master@abebf33`. Stop all movement-talk implementation work. Only local overlay/mod/worktree reconciliation and separately authorized cleanup remain.
- PRs #204-207 and #210-211 are merged.

Do not reimplement #212 or #214 locally. Do not describe the locally selected #213 correction as live on GitHub until it is actually sent outward.

## Ready local candidates

| Task | Player-visible proof | Local state | Remaining gate |
| --- | --- | --- | --- |
| T1 Discovery reaction settlement | Matched Tk A/B: a successful dismissal skips Closure's existing departure, `气力 -15`, and five-minute settlement on baseline; the candidate shows them once before the interrupted H action resumes. | Four-file candidate `5d360f71e`, focused tests, code/evidence review, Fable evidence review, and Fable PR-text review all pass. | Technical work is complete. Evidence publication, push, and PR creation each remain separately authorized outward actions. No gameplay choice is needed. |
| T2 One edge decision per ordinary settlement | Reviewed real Tk A/B and focused candidate prove one multi-part settlement is collected, judged once, and applied once. | One-file candidate `579b7c475`; 11 submitted tests and 11 near-real/local checks pass, the artifact audit is `PASS`, and publication state is `local-review-ready`. The test mod remains enabled for passive local coverage. | The 2026-07-14 Fable document-reconciliation ruling cancels the fixed several-day playtest gate. Passive play is optional clue gathering and reopens the task only if it finds a new problem. Before PR creation, the user gives final semantic confirmation, the candidate is refreshed and reverified against upstream after #214, and outward authorization is obtained. No outward action has occurred. The earlier choice to play for a few days remains historical context, not the current gate. |
| T3 Compact settlement values | Matched ordinary Tk `看电影` A/B: the same player learn settlement is shown as the impossible `+3M` on baseline and the corrected `+3K` on the candidate; every target exact field and all other text remain identical. | Two-file candidate `cd28b2b21`; 15 focused tests, strict OpenSpec validation, Fable evidence/document/code/PR-text review, and fresh PR-artifact review pass. | Technical work is complete and `local-review-ready`. Evidence publication, push, and PR creation each remain separately authorized outward actions. No gameplay choice is needed. |

These outward gates do not stop local work on later tasks.

## Ordered small-PR queue

### T4 Attribute time-stop release changes to each NPC

- **Why it is a bug candidate:** the existing release loop records NPC release values on the player's root change object instead of that NPC's `TargetChange`. The values in an earlier player screenshot match the existing formula for six deferred body-part orgasms, but the six-NPC scene has not yet been replayed as baseline/candidate runtime evidence.
- **Current state:** still in evidence work, not complete. Attempt 3 is formally invalid because its pre-registered viewport prerequisite was wrong; an isolated rehearsal is in progress.
- **Next work:** finish that rehearsal, then run the real loader with the batch mod both disabled and enabled, verify actual applied values and caps, and produce pristine-baseline versus candidate Tk evidence for the six-NPC release.
- **Done when:** root/target ownership, zero/one/multiple/remote NPC cases, actual applied values, Tk output, independent Web collection, and review all pass. The shared settlement-output path feeds both renderer adapters, so the Web check is an inverse collection check rather than separate PR-facing visual evidence.
- **Player decision:** none; ownership follows the character whose values changed.

### T5 Show one elapsed-time line per player click

- **Owner and state:** `fix-elapsed-time-line-ownership`, 0/12, ready after T4.
- **Rule:** one player click displays one “minutes passed” line. This is display ownership, not a gameplay-balance choice.
- **Dependency:** it consumes `fix-game-update-depth-restoration`; this first real consumer also supplies that dependency's missing player-visible validation.
- **Player decision:** none.

### T6 Gate orgasm chaining once per player click

- **Owner and state:** `add-per-click-orgasm-chain-gate`, 0/17, ready after T5.
- **Confirmed rule:** the gate is per click, not a physiological cooldown. Passive stimulation, orgasm, and settlement continue normally.
- **Dependency:** it also consumes `fix-game-update-depth-restoration`, but its change surface is larger than T5's.
- **Player decision:** already made for local implementation; any outward action still needs separate authorization.

### T7 Restore temporary talk state after use

- **Why it is a bug candidate:** common-talk rendering temporarily overwrites the player's interaction target without a `finally` restoration; a second path expands a global paper-doll candidate list in place, so repeated rendering changes future selection weights.
- **Next work:** build red tests for normal, exception, and consecutive-NPC calls; restore the target in a scoped `finally`; copy candidate lists before combining them; capture representative Tk evidence.
- **PR boundary:** default to two small PRs. Merge them only if investigation proves both defects violate the same rule and belong to the same lifecycle operation in the same logical owner.
- **Player decision:** none; both changes restore state isolation rather than choose new game behavior.

T5 precedes T6 because it is smaller, affects only display, needs no player choice, and is the fastest real consumer proof for depth restoration. T7 is independent of that dependency and follows them.

## Local-complete or dependency work outside the ordered PR queue

- `fix-game-update-depth-restoration` is 6/6 locally complete at commit `80a711603` on a fork side branch. It is dependency/local maintenance, not a standalone PR; validate it through T5 and T6.
- `clear-pain-as-pleasure-on-hypnosis-cancel` is 10/10 locally complete. It waits for authorization to revise #213; its selected local target is not yet the remote PR behavior.
- `settle-remote-plural-orgasm-silently` is 14/14 locally complete at candidate `364ac6d9f` on a fork side branch. A pushed side branch is not an upstream PR. Before submission, refresh and reverify against post-#214 upstream, obtain final user semantic confirmation, and obtain outward authorization.

## Later evidence-led records, not part of the current T4-T7 order

### Group-sex admission eligibility

- **Why it is a bug candidate:** real-loader BDD shows exhausted or seriously fatigued characters can still be offered or admitted through normal discovery/invitation entry points. Player-visible Tk A/B is still required.
- **Next work:** capture an exhausted-character baseline through a real discovery or invitation route, then put the shared eligibility check at the premise owner instead of copying UI callers.
- **Provisional rule:** exhausted or seriously fatigued characters cannot receive a new invitation or be confirmed as new participants. A character who became fatigued after being invited remains visible only so the player can cancel that invitation; the character cannot be confirmed into the activity.
- **Done when:** Tk A/B, one shared predicate, inverse cases, and review pass.
- **Player decision:** confirm the provisional rule before an upstream PR, not before local evidence and implementation.

### Split hypnosis state-loss problems by mechanism

- **Why it may be a bug:** a default type or exact sanity exhaustion may erase an existing hypnosis unconscious state, and the common talk gate may treat hypnosis unconsciousness as ordinary sleep and suppress its dialogue.
- **Next work:** first make faithful red tests and one Tk route for each mechanism. Do not implement the mode-switch-immediacy claim until its own normal route fails.
- **PR boundary:** state erasure and talk-gate selection are separate changes. Implement only a mechanism whose red evidence succeeds.
- **Done when:** a normal route proves the loss, the narrow owner-level fix passes inverse cases, Tk evidence and review pass.
- **Player decision:** none for preventing state erasure; confirm any change to dialogue-selection policy before that PR.

### Isolate Tk skip leakage into the next wait

- **Why it may be a bug:** mod-on Tk evidence shows a chat wait after cross-area movement stays put for eight seconds and advances only on a fresh click, but no matched mod-off baseline proves the upstream failure yet.
- **Next work:** capture the missing mod-off A/B. If the old skip really advances the later wait, extract only that ownership fix from `local_settlement_input_fix` and remove its dependency on the 30 ms input-age patch.
- **Done when:** mod-off failure is reproduced, a narrow fix passes, and matched Tk evidence plus review pass. If the baseline does not fail, freeze the task.
- **Player decision:** none for one prompt consuming only its own input.

## Local maintenance, not new PR work

- Treat sleep and direct hypnosis cancellation clearing `pain_as_pleasure` as the selected local target. The one-line core fix belongs only to `clear-pain-as-pleasure-on-hypnosis-cancel`.
- The disabled pain mod's cancel-clear wrapper points in the same semantic direction. Do not delete it as wrong; after the core fix is locally integrated, retire it as replaced and verify that composition does not double-clear or otherwise change behavior. The BDD expectation is “cancellation clears”.
- Keep `activate-granted-pain-as-pleasure` limited to local composition and mod-retirement checks. It does not own the one-line core fix. PR #212 still owns signed routing and direct positive-pain effects.
- Keep the T2 test mod enabled until its candidate is upstreamed or rejected; passive play may provide new clues but is not a gate.

## Frozen or retained work

| Area | Disposition | Reopen condition |
| --- | --- | --- |
| Group masturbation intent | Freeze. The current global active set and action-window identity are not an upstream boundary. | A deterministic normal trace shows the same intent consumed twice or leaking into the next player action, followed by an explicit duration/retry rule. |
| Group edge release and the rest of the large orgasm batch | Freeze and do not upstream the package. | Re-derive owners after T2 lands; reproduce one exit dropping a nonzero pending edge before choosing exit visibility or discard semantics. |
| Tk queue scrolling | Retain only as an experience/performance candidate. Freeze the 30 ms input-age guess and whole-queue drains. | Player-representative evidence for the batch-scroll change, kept separate from input correctness. |
| H movement interruption | Withdraw to investigation history. | A normal production route demonstrates stale movement continuing after H/group entry. |
| Private font registration | Freeze. | Clean Windows development and packaged-build evidence proves fallback and verifies the actual registered family. |
| Psychological-pleasure curve | Keep as balance-feature backlog. | Measure the current range and obtain a separately reviewed curve contract. |
| `group_sex_extension` | Keep as an independent feature. | Adapt only after shared participant and orgasm owners exist; do not merge its commands into bugfix PRs. |
| `easy_mode` / `semen_boost` | Keep feature / disabled example; no bugfix task. | Explicit feature work. |

## Documentation migration

1. The discovery owner is now `fix-discovered-reaction-settlement`; every existing supervision prompt and verdict stays verbatim, and the broader experiments remain clearly rejected history.
2. `fix-group-sex-admission-eligibility` remains a later evidence-led owner rather than putting admission semantics back into the discovery change.
3. `fix-compact-value-formatting` and `fix-time-stop-release-attribution` now separate the former mixed time-stop change into T3 and T4.
4. Keep the #213 one-line correction in `clear-pain-as-pleasure-on-hypnosis-cancel`; narrow `activate-granted-pain-as-pleasure` to local composition and replaced-mod retirement, then archive it when those checks finish.
5. Keep `fix-game-update-depth-restoration` as a T5/T6 dependency rather than a standalone PR.
6. `fix-elapsed-time-line-ownership` and `add-per-click-orgasm-chain-gate` own T5 and T6. `fix-talk-common-state-leaks` is T7's investigation owner and must split its two defects into separate PR owners unless the merge condition above is proven.
7. The umbrella `tasks.md` is now an index of these owners and frozen records; its original checklist remains in `legacy-tasks.md`. Detailed implementation tasks belong only in each small change.

## Stop rule

There is no current player-input stop. T2 needs final semantic confirmation before its upstream PR; `settle-remote-plural-orgasm-silently` needs final semantic confirmation before submission; later admission or dialogue-policy work keeps its own named confirmation gate. T6's per-click rule is already confirmed. Missing outward authorization pauses only that outward action, not local evidence or reversible implementation elsewhere in the queue.

===== CURRENT umbrella tasks.md =====
## 1. Program documentation

- [x] 1.1 Preserve the original 160-item umbrella checklist as `legacy-tasks.md` and its one-owner disposition as `task-migration.md`
- [x] 1.2 Establish the Fable-reviewed current queue and stop rules in `program-task-map.md`
- [x] 1.3 Rename the discovery owner to `fix-discovered-reaction-settlement` without changing its documents or losing supervision history
- [x] 1.4 Complete Fable quality review for the split T3, T4, and T6 OpenSpec artifacts
- [x] 1.5 Narrow `activate-granted-pain-as-pleasure` to local composition and replaced-mod retirement without giving it ownership of the #213 one-line correction

## 2. Ready candidates awaiting later semantic or outward gates

- [ ] 2.1 `fix-discovered-reaction-settlement` owns T1; technical review is complete and only separately authorized outward actions remain
- [ ] 2.2 `judge-orgasm-edge-once-per-settlement` owns T2; under the 2026-07-14 Fable document-reconciliation ruling it is `local-review-ready` and the fixed several-day gate is removed, while passive play remains optional clue gathering; before PR creation it still needs final user semantic confirmation, post-#214 upstream refresh/reverification, and outward authorization
- [ ] 2.3 `fix-compact-value-formatting` owns T3; its local code and evidence are complete and only separately authorized outward actions remain
- [ ] 2.4 `clear-pain-as-pleasure-on-hypnosis-cancel` is 10/10 locally complete and owns the one-line correction that makes sleep and direct hypnosis cancellation both clear `pain_as_pleasure`; the remote #213 still preserves it, and revising that PR has not been authorized or performed
- [ ] 2.5 `settle-remote-plural-orgasm-silently` is locally complete at `364ac6d9f` on a fork side branch; before an upstream PR it needs post-#214 refresh/reverification, final user semantic confirmation, and outward authorization

## 3. Active small changes

- [ ] 3.1 `fix-time-stop-release-attribution` owns T4 and remains in evidence work; attempt 3 is formally invalid because its pre-registered viewport prerequisite was wrong, and the isolated rehearsal is still in progress
- [ ] 3.2 `fix-game-update-depth-restoration` is a 6/6 locally complete dependency at `80a711603`, not a standalone PR; its remaining program obligation is player-visible validation through its first real consumers T5 and T6
- [ ] 3.3 `fix-elapsed-time-line-ownership` is the ready 0/12 T5 owner after T4; it is the smaller, display-only first consumer of depth restoration and needs no player semantic choice
- [ ] 3.4 `add-per-click-orgasm-chain-gate` is the ready 0/17 T6 owner after T5; it also consumes depth restoration, and the user has already confirmed the per-click, non-physiological gate while passive settlement continues
- [ ] 3.5 `fix-talk-common-state-leaks` owns T7 after T6; split its two leaks into two small PRs unless investigation proves one violated rule, one logical owner, and one lifecycle operation
- [ ] 3.6 Keep `fix-group-sex-admission-eligibility`, the two evidence-first hypnosis mechanisms, and a possible narrow Tk skip-leak owner as later evidence-led work outside the current T4-T7 order

## 4. Frozen and feature records

- [ ] 4.1 Keep group masturbation intent, group-edge exit, and the remaining large orgasm-batch semantics frozen until the reopen evidence named in `program-task-map.md` exists
- [ ] 4.2 Keep H movement interruption withdrawn and private font registration frozen pending their named production/platform evidence
- [ ] 4.3 Keep the psychological-pleasure curve, `group_sex_extension`, `easy_mode`, and `semen_boost` in feature or example ownership rather than bugfix PRs
- [ ] 4.4 Keep `activate-granted-pain-as-pleasure` only as the local composition and replaced-mod retirement owner; it must not duplicate the one-line #213 correction owned by `clear-pain-as-pleasure-on-hypnosis-cancel`

## 5. Umbrella closure

- [ ] 5.1 Confirm every active or frozen row above has one valid owning change or evidence record and no duplicate upstream PR responsibility
- [ ] 5.2 Archive this umbrella only after its current documentation obligations are complete; do not use it to track implementation details from the small changes

===== CURRENT task-migration authority and ending =====
# Umbrella Task Migration

## Purpose

This ledger splits every task in `tasks.md` as needed and assigns each resulting obligation to exactly one durable destination before the oversized umbrella change is rewritten or archived. It changes no game code and does not approve any unresolved gameplay rule.

The five states mean:

- **completed**: keep only as history or an already-established workflow rule;
- **upstream-owned**: the responsibility is tracked by an exact open or merged upstream PR, not this umbrella; an open PR is conditional ownership until merge, and a PR closed unmerged sends its rows to a named `re-file, revise, or withdraw` decision record;
- **current**: move the obligation to the named active owner;
- **deferred**: retain evidence and wait for a named gameplay, platform, or readiness decision;
- **withdrawn**: preserve the diagnosis/candidate as history, but do not continue it unless the user explicitly reopens it.

Migration-only suffixes such as `2.3k.a` split one mixed source task into separately owned obligations. Removing those suffixes still yields the original 160 task IDs exactly. Creating, renaming, splitting, or archiving OpenSpec changes is a later step.

## Current Status Supersessions (2026-07-14)

### PR #214 is merged

PR #214 merged at `2026-07-14T10:32:51Z` and is present in `upstream/master@abebf33`. Every row below that calls #214 open, live, or waiting for merge is preserved as investigation and migration history from its own date; it is not the current status. The current rule is to stop movement-talk implementation and leave only local overlay/mod/worktree reconciliation plus separately authorized cleanup. In the migration table, `upstream-owned` for #214 now means ownership by that exact **merged** PR.

### PR #213 remote state and selected local target differ

PR #213 remains open at `e1a9378`; its remote code preserves `pain_as_pleasure` through sleep and direct hypnosis cancellation. The later, locally selected target is for both paths to clear the flag. The accepted one-line shared-helper correction belongs only to `clear-pain-as-pleasure-on-hypnosis-cancel`; it is locally complete but uncommitted and has not been pushed, used to edit #213, or accompanied by published images. `activate-granted-pain-as-pleasure` owns only local composition and retirement of the same-direction mod wrapper after core integration. Any historical table row that treats remote preservation as the selected local contract, or treats #213 merge alone as sufficient reason to retire that wrapper, is superseded by this paragraph.

### T2 current gate

`judge-orgasm-edge-once-per-settlement@579b7c4` is `local-review-ready`: code, focused and near-real checks, matched Tk A/B, and artifact review pass. The 2026-07-14 Fable document-reconciliation ruling cancels the fixed several-day playtest gate; passive play is optional clue gathering. Before an upstream PR is created, the user must give final semantic confirmation, the candidate must be refreshed and reverified against upstream after #214, and outward authorization must be obtained. The earlier choice to play for a few days remains history rather than the current gate.

## Migration Table

| Original task | State | Destination | Migration note |
| --- | --- | --- | --- |
| `0.1` | completed | umbrella archive | Preserve the ownership exclusions as audit history. |
- PR #213 remotely preserves `pain_as_pleasure` through sleep and direct cancellation, but the selected local target is now for both paths to clear it. `clear-pain-as-pleasure-on-hypnosis-cancel` exclusively owns that locally complete one-line correction and waits for authorization to revise #213. `activate-granted-pain-as-pleasure` owns only local composition and retirement of the same-direction wrapper after core integration; its BDD expectation is that cancellation clears. PR #212 still owns signed routing and direct positive-pain effects.
- `curve-derived-psychological-pleasure` remains an independent, unapproved balance-design change.
- `judge-orgasm-edge-once-per-settlement` remains the protected narrow batch-decision candidate, distinct from the deferred deeper orgasm transaction. It is `local-review-ready`; before PR creation it needs final user semantic confirmation, post-#214 upstream refresh/reverification, and outward authorization, while passive play is optional clue gathering rather than a gate.
- `fix-discovered-reaction-settlement` is now narrowed in its active documents to the local-review-ready discovery-settlement slice. It has no playtest gate and no upstream PR; evidence publication, push, and PR creation remain separately authorized outward actions.
- The superseded combined time-stop change is archived without spec sync. `fix-compact-value-formatting` now owns global formatter call-site and Tk display verification; `fix-time-stop-release-attribution` owns real-loader identity, actual-delta/cap, Tk attribution, and independent Web collection. Candidate code remains on local `main`, but each new owner must isolate and prove its own upstream diff.
- `fix-game-update-depth-restoration` is 6/6 locally complete at `80a711603` on a fork side branch. It is a dependency/local-maintenance owner, not a standalone PR; T5 and T6 provide its real-consumer validation.
- `fix-elapsed-time-line-ownership` is the ready T5 owner after T4. It is the smaller, display-only first consumer of depth restoration and needs no player semantic choice.
- `add-per-click-orgasm-chain-gate` is the ready T6 owner after T5. It also consumes depth restoration; the user has already confirmed a per-click, non-physiological gate while passive settlement continues.
- `settle-remote-plural-orgasm-silently` is 14/14 locally complete at `364ac6d9f` on a fork side branch, which is not an upstream PR. Before submission it needs post-#214 refresh/reverification, final user semantic confirmation, and outward authorization.

## Post-Migration De-duplication Checkpoint (2026-07-14)

- Discovery settlement must not be re-investigated as a fresh task. Use candidate `5d360f71e`, its 35-test run, deterministic Tk A/B, and completed review packet. PR #206 is adjacent same-witness history, not ownership of this candidate.
- Pain-as-pleasure work must distinguish the remote #213 preservation behavior from the selected local clear-on-both-paths target. Keep the one-line core correction in `clear-pain-as-pleasure-on-hypnosis-cancel`; retire the same-direction mod wrapper only as replaced after local core integration, and keep the BDD expectation on clearing.
- Time-stop release work is verification of code already on local `main`, not permission for a second implementation. Rewrite only when a named check fails.
- The current global order is T4 `fix-time-stop-release-attribution` evidence/rehearsal, then T5 `fix-elapsed-time-line-ownership`, T6 `add-per-click-orgasm-chain-gate`, and T7's two talk-state leaks. Default T7 to two small PRs; combine them only if investigation proves one violated rule, one logical owner, and one lifecycle operation. Depth restoration is a dependency rather than a standalone queue item.

## Closure Rule

The umbrella can be rewritten or archived only after every source task has one or more explicit migration obligations and every obligation has one named, checkable destination. Each **current** obligation must appear in exactly one existing OpenSpec owner; each **deferred** obligation must point to one decision or evidence record that states its unblocker; each **upstream-owned** obligation must link to the exact PR and remain tracked until merge, reverting to a named `re-file, revise, or withdraw` decision if the PR closes unmerged. Completed and withdrawn material must remain reachable as history without presenting a rejected candidate, stale draft, or unverified local gate as active or review-ready work.

===== CURRENT pain proposal.md =====
## Why

Open PRs #212 and #213 own two independently reviewable core areas, but remote #213 does not yet express the accepted local exit lifecycle. PR #212 owns positive-pain routing. Remote PR #213 currently preserves `pain_as_pleasure` through sleep and direct hypnosis cancellation. The later locally selected target is that both exits clear the flag; the one-line shared-helper correction for that target is complete under `clear-pain-as-pleasure-on-hypnosis-cancel`, but it has not been committed, pushed, or applied to the remote PR.

This change remains the local composition and mod-retirement owner. It must first consume the separately owned local exit-lifecycle correction in the integration baseline, then retire the disabled mod's matching cancel-clear wrapper because corrected core supersedes it, and prove that the corrected exit lifecycle composes with #212 through normal grant-to-settlement paths.

## What Changes

- Treat PR #212 as the owner of signed routing, direct positive-pain effects, and raw granted-flag activation.
- Record remote PR #213's current preservation behavior separately from the locally selected, not-yet-published target where sleep and direct cancellation both clear the flag.
- Leave the one-line `clear_hypnosis_sub_states()` correction exclusively to `clear-pain-as-pleasure-on-hypnosis-cancel` and consume that correction only as a local integration dependency.
- After that correction is integrated locally, retire the disabled old mod's direct-cancel clearing wrapper because core supersedes it, not because its clearing semantics are wrong.
- Keep the BDD contract aligned with the selected lifecycle: both sleep and direct cancellation clear the granted flag.
- Verify real loader alias identity and connected direct-invitation/discovery grant-to-pain conversion without reimplementing either PR.
- Preserve the user's accepted rules: converted pleasure posts while asleep/unconscious, and capped change records use the requested value.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `local-bugfixes`: Reconciles local mod retirement and connected composition with PR #212 and the separately owned corrected local exit lifecycle.

## Impact

This change affects only the disabled `local_pain_as_pleasure_fix`, its tests/documentation, maintained-mod load-order checks, and connected integration evidence. It does not own the core helper edit or any remote PR update. It remains substantive work until the corrected core baseline is integrated locally, the redundant wrapper is retired, and composition verification is complete.

===== CURRENT pain tasks.md =====
## 1. Reconcile local artifacts with the corrected core baseline

- [ ] 1.1 Pin the exact local overlays for open PR #212 and remote PR #213, record that remote #213 currently preserves the flag on both exits, and record the fallback action if either PR closes unmerged
- [ ] 1.2 Confirm that the local integration baseline consumes the accepted one-line correction from `clear-pain-as-pleasure-on-hypnosis-cancel`; do not modify `clear_hypnosis_sub_states()` in this change
- [ ] 1.3 Only after task 1.2, remove the disabled pain mod's direct-cancel clearing wrapper because the corrected core supersedes it, then compare wrapper-on and wrapper-off behavior to rule out a composition difference
- [ ] 1.4 Keep or revise the BDD cases so direct cancellation and sleep both clear the granted flag under the corrected local baseline

## 2. Verify maintained composition

- [ ] 2.1 Load the maintained mod set through the real ModManager and assert the default, second-effect, realtime, and item aliases plus direct effects resolve to the #212 contract exactly once
- [ ] 2.2 Exercise inactive flag, positive conversion, non-positive pain, death guards, sleep/unconscious posting, requested-value cap accounting, both hypnosis-exit clears, and explicit toggle/full-reset inverse cases
- [ ] 2.3 Connect the stable direct-invitation grant path to real positive-pain settlement, then connect discovery after `fix-discovered-reaction-settlement` is available

## 3. Review and complete local owner work

- [ ] 3.1 Run focused and near-real BDD suites, inspect the final local cleanup diff, and record skipped or PR-head-dependent checks
- [ ] 3.2 Give the updated proposal, design, spec, tasks, and cleanup evidence to Fable and resolve every documentation finding
- [ ] 3.3 Record the completed composition and mod-retirement boundary; do not create a new upstream PR for responsibilities already owned by #212 or `clear-pain-as-pleasure-on-hypnosis-cancel`

===== CURRENT pain design.md =====
## Context

PR #212 carries signed pain routing and direct positive-pain effects. Remote PR #213 currently makes sleep and direct hypnosis cancellation preserve `pain_as_pleasure`. Both open PR heads are overlaid on local `main`, and the old pain mod is disabled.

The later locally selected target is different from remote #213: sleep and direct cancellation both clear `pain_as_pleasure`. `clear-pain-as-pleasure-on-hypnosis-cancel` exclusively owns the accepted one-line addition to the shared `clear_hypnosis_sub_states()` helper. That candidate and its evidence are locally complete, but the edit is uncommitted and has not been pushed or applied to PR #213. The disabled mod's direct-cancel wrapper already clears the flag, so its semantics agree with the selected target; it becomes redundant only after the corrected helper is present in the local integration baseline.

The user already decided that the raw granted flag activates conversion, converted psychological pleasure posts while asleep or unconscious, and capped change records report the upstream-compatible requested value.

## Goals / Non-Goals

**Goals:**

- Integrate the separately owned local exit-lifecycle correction without taking ownership of its core helper edit or implying that remote PR #213 already contains it.
- Retire the disabled direct-cancel wrapper only after core supersedes it, and prove wrapper removal does not change the selected clearing behavior.
- Keep local BDD expectations aligned with the selected rule that sleep and direct cancellation both clear the flag.
- Prove the real loader exposes one #212 conversion owner through every maintained alias and direct effect.
- Connect ordinary invitation/discovery grant paths to real positive-pain settlement without hand-constructing the final character state.

**Non-Goals:**

- Modify `clear_hypnosis_sub_states()` or reproduce the one-line `pain_as_pleasure = False` fix; that production edit belongs exclusively to `clear-pain-as-pleasure-on-hypnosis-cancel`.
- Reimplement or widen open PR #212.
- Commit, push, publish evidence for, or edit remote PR #213 from this change.
- Reopen the user's sleep/unconscious or cap-accounting decisions.
- Change group-sex admission semantics, hypnosis-mode transitions, or pain formulas.

## Decisions

### Retire the wrapper only after corrected core integration

The disabled direct-cancel wrapper clears `pain_as_pleasure`, which matches the locally selected target and is not semantically wrong. Removing it while the local baseline still contains the remote #213 preservation behavior would regress direct cancellation back to preservation. The wrapper must therefore remain until the separately owned helper correction is integrated locally.

After that dependency is present, core performs the clear for both sleep and direct cancellation. The wrapper can then be retired because it is a redundant hook around an already-correct owner. Wrapper-on and wrapper-off checks must agree, and the BDD contract must continue to expect clearing on both exits.

### Verify identity through the real loader

The common handler is imported into default, second-effect, realtime, and item modules, while direct effects use registry entries. Composition verification must assert the actual loaded callable identities and exercise settlement; source inspection alone cannot prove that a stale alias is not active.

### Keep connected paths as integration proof

Direct invitation is the first stable path from participant resolution through grant to real settlement. Discovery follows after the separate discovery-settlement owner is available. These tests prove composition only; ownership remains with #212, `clear-pain-as-pleasure-on-hypnosis-cancel`, and the admission/discovery changes.

## Risks / Trade-offs

- **[An open PR changes before merge]** → pin verification to the exact overlaid heads and re-file only the affected responsibility if a PR closes unmerged.
- **[The wrapper is removed before corrected core is present]** → make local integration of the separately owned helper correction an explicit prerequisite and prove both exits clear before removing the hook.
- **[A redundant wrapper masks a composition difference]** → compare wrapper-on and wrapper-off behavior after corrected core integration and inspect the final maintained load order.
- **[Connected tests accidentally own admission semantics]** → assert only that an already granted flag reaches real pain settlement; leave eligibility and discovery choices to their owners.

===== CURRENT pain implementation-notes.md =====
## Upstream Core Split (2026-07-13)

Upstream PR [#212](https://github.com/Godofcong-1/erArk/pull/212) replaces only the signed-delta routing and direct positive-pain portion of the experimental implementation described below. Its pure router returns the destination state and adjusted value without taking over storage, caps, or change-record ownership. Positive pain that reaches the router converts under the raw flag; zero and negative pain remain state 17. Direct effects 270, 283, 296, and 408 use the same rule.

The final two-file proposed diff is commit `21261e951`, based on upstream commit `06fc59c1e`. It passed 27 focused local tests. The accepted real Tk A/B evidence and fresh artifact review cover the same byte-identical proposed production diff captured before the final parent-only rebase; they are not evidence of the broader group-admission, sleep/unconscious, cancellation/reset, or maintained-mod load-order contract.

The sections explicitly labeled as historical preserve the 2026-07-10 investigation record. Their custom local-mod implementation and unresolved connected-path work are not made current or accepted by PR #212.

## Hypnosis Exit Split And Current Local Contract (2026-07-14)

Remote PR [#213](https://github.com/Godofcong-1/erArk/pull/213) at head `e1a9378b` currently makes sleep and direct hypnosis cancellation clear the same four hypnosis-owned sub-states while both preserve `pain_as_pleasure`. Local `main` carries that remote head together with the PR #212 overlay, and `local_pain_as_pleasure_fix` is disabled. This is the current remote and overlay state, not the accepted local target.

The later user/Fable decision selected a different exit contract: sleep and direct cancellation both clear `pain_as_pleasure`. `clear-pain-as-pleasure-on-hypnosis-cancel` exclusively owns the accepted one-line addition to `clear_hypnosis_sub_states()`. Its code and evidence are locally complete, but the edit remains uncommitted and has not been pushed, published, or applied to remote PR #213.

The disabled mod's direct-cancel wrapper already clears `pain_as_pleasure`, so its semantics agree with the selected target. This change must consume the separately owned core correction in the local integration baseline before retiring that wrapper as redundant. Its BDD contract must expect both sleep and direct cancellation to clear. Wrapper retirement, maintained load-order verification, and connected grant-to-settlement composition remain substantive work owned here; this change is not ready to archive. Full hypnosis cleanup and other local reset paths still require source-and-runtime ownership verification, but they do not reopen the settled two-exit clearing rule.

## Historical Worktree Status (2026-07-10)

The reported root was local and confirmed, but the then-current conversion implementation was not accepted because it duplicated upstream state-23 settlement with unresolved guard and accounting differences. No component, BDD, loader-order, or gameplay test had run after those edits. Cross-change branch and protected-file state were recorded in `../continue-local-bugfix-audit/design.md`.

## Confirmed Root and Contract History

`group_sex_extension._set_hypnosis_boost()` sets `hypnosis.pain_as_pleasure = True` without changing `sp_flag.unconscious_h`. UI and premise checks read that persistent flag directly. The previous local pain component then imposed its own extra gate, requiring `unconscious_h in {4,5,6,7}` and temporarily hiding the raw flag outside those states. A conscious participant who joined later could therefore display "pain to pleasure" as enabled while settlement still added ordinary pain.

At that checkpoint, the proposed interpretation conflicted with the main specification, which said that the flag was persistent but dormant outside active hypnosis states. The then-open `fix-group-sex-invite-controls-and-idle-ai` change, however, granted the enhancement to complete-hypnosis participants without changing their current unconscious state. The bug report requested that a conscious later joiner actually receive the displayed effect, so this change proposed superseding the old dormant-state rule. At this historical checkpoint, the main spec was not to be synced and the contract was not to be declared settled until the remaining state-23 choice below was discussed with the user. That choice was later resolved as recorded in `State-23 Semantics (resolved 2026-07-10)`.

## Enumerated Runtime Paths

### Historical Activation And Clearing Inventory

- The ordinary 1230 toggle and group hypnosis boost can set the persistent flag.
- At this historical checkpoint effect 1213 cancellation, effect 489 full-hypnosis cleanup, `local_hypnosis_state_fix` full reset, and ordinary toggle/off paths appeared to clear it. Remote PR #213 later superseded that checkpoint in its published candidate by making sleep and direct cancellation preserve the flag. The still later 2026-07-14 local decision superseded the preservation interpretation: both exits should clear. The one-line core correction belongs to `clear-pain-as-pleasure-on-hypnosis-cancel` and is not yet externally published. The remaining reset paths still require ownership verification.
- The group boost intentionally does not mutate `unconscious_h`.

### Historical Common Positive Pain

At that checkpoint, the shared `base_chara_state_common_settle()` alias was used from `Script.Settle.default`, `Script.Settle.Second_effect`, `Script.Settle.realtime_settle`, and `Script.Settle.item_effect`. Upstream already had a raw-premise pain-to-pleasure recursion at state 17. The old local state gate was what made the raw flag dormant. PR #212 now owns the accepted signed routing for these paths.

### Historical Direct Positive Pain

At that checkpoint, second effects 270, 283, 296, and 408 wrote positive pain without using the common handler and would have needed explicit conversion if the flag-driven contract were accepted. PR #212 now owns and implements that accepted direct-effect routing. The direct `originium_arts.py` write found by the audit assigned zero and was a reset, not a positive settlement path.

### Historical Non-Positive Pain And Guards

At that checkpoint, negative or zero pain continued through upstream pain settlement with temporary recursion suppression and `finally` restoration. Existing death behavior differed by entry: common settlement and effect 408 had guards; 270/283/296 did not all share that same upstream guard. PR #212's accepted scope preserves those per-entry boundaries; this composition owner does not reopen them.

## Historical Experimental Implementation Present but Unaccepted (2026-07-10)

The historical semantic diff removed the `unconscious_h` gate and made `_has_pain_as_pleasure()` read only the raw flag. It retained the existing custom common conversion, negative delegation, cancellation cleanup, and wrappers for 270/283/296/408. The cancellation clear later became the selected semantic target; its wrapper becomes redundant only after the separately owned core correction is integrated. Component and BDD tests were expanded, but at that checkpoint none had run.

At that checkpoint, the common implementation calculated positive pain itself, then called `_settle_direct_psychological_pleasure()` to write state 23 directly. A safer candidate for common positive pain was to delegate to the upstream state-17 function with the raw flag visible, because upstream already performed the state-17-to-state-23 recursion. That would preserve upstream math and guards. Direct effects would still need explicit handling. This was an analysis option only, not an authorized implementation change.

## State-23 Semantics (resolved 2026-07-10)

Upstream `base_chara_state_common_settle()` refuses psychological pleasure while the target is unconscious or asleep. The user chose contract 2: pain-as-pleasure is an intentional exception. Psychological pleasure is recorded even while unconscious/asleep, and the delta spec explicitly overrides the upstream rule for this conversion path only. The manual state-23 writer's guard bypass is therefore the intended behavior, but it must become formula-equivalent to upstream in every other respect (see gap 1 below).

## Formula and Accounting Gaps

1. Resolved 2026-07-10: `_settle_direct_psychological_pleasure` now takes `apply_repeat_adjust`, and the common path passes it so the consecutive-instruction reduction is applied a second time exactly as upstream's state-17-to-state-23 recursion does. The shared reduction formula lives in `_get_consecutive_instruct_adjust`. Regression: `test_repeated_instruction_applies_second_reduction_like_upstream` (0.55 × 0.55 double reduction verified). Direct effects intentionally do not apply the reduction — upstream never routes them through the recursion.
2. Accepted as the intended contract 2026-07-10 (requested-value recording): at 99998 with request +100, stored state rises by 1 while both record owners keep +100, matching upstream. Regression: `test_cap_keeps_requested_value_in_change_records`.
3. Resolved 2026-07-10: change records report the upstream-compatible requested value at the cap, not the actual clamped delta. The spec says so explicitly; the remaining work is verifying both record owners follow it consistently.
4. Passing both `change_data` and `change_data_to_target_change` can create two records unless the ownership contract is explicit.
5. Alias installation catches import exceptions and continues. A module or later mod can retain an earlier function object; identity checks must run after the complete maintained-mod load order.

## Historical Written but Unexecuted Verification (2026-07-10)

- Historical component coverage was expanded for inactive flag, cancellation clearing, negative pain, common aliases, direct effects, and some death behavior. Clearing was unexecuted at that checkpoint but later became the selected contract; the separate `clear-pain-as-pleasure-on-hypnosis-cancel` change has since verified the core one-line fix, while this owner still lacks wrapper-retirement and composition verification.
- `mod/tests/bdd/test_bdd_pain_as_pleasure.py` adds a conscious late-participant case, but it manually sets `pain_as_pleasure=True` and `is_h=True`; it does not drive discovery admission, participant resolution, or the group boost.
- The group admission component has a fake connected case, not a near-real ModManager/NPC-state-machine flow.
- The discovered-admission connection is blocked by the unresolved group settlement-ownership change. A stable direct-invitation route could independently verify resolver to boost to pain settlement first.
- The component file's direct `main()` runner omits `test_dead_character_positive_pain_delegates_to_original`; pytest would discover it, the README-style Python command would not.

At that checkpoint, the missing checks were sleeping/unconscious state-23 behavior, cap with actual delta 0/1, both recording objects, repeated-instruction formula equivalence, each direct effect's own death semantics, toggle/full-reset restoration, alias/load-order behavior, and a real admission-to-boost-to-settlement trace. This list is preserved as investigation history rather than a current completion claim. The current outstanding work owned here is the corrected-core integration dependency, redundant-wrapper retirement, maintained load-order verification, and connected grant-to-settlement composition.

===== CURRENT pain delta spec =====
## MODIFIED Requirements

### Requirement: Keep pain-as-pleasure scoped and consistent
With the PR #212 core overlay and the separately owned local exit-lifecycle correction integrated locally, the system SHALL activate `pain_as_pleasure` whenever its granted flag is set, regardless of the character's sleep or unconscious state, SHALL apply it consistently to positive direct pain increases only, SHALL clear the flag when either sleep cleanup or direct hypnosis cancellation exits the relevant hypnosis sub-states, and SHALL restore ordinary pain settlement after an approved exit, off, or reset owner clears the flag.

Remote PR #213 at head `e1a9378b` currently preserves the flag on both exits; that is a remote-state fact, not the locally selected target. The sole production correction belongs to `clear-pain-as-pleasure-on-hypnosis-cancel` and has not been externally published. This change SHALL NOT modify `clear_hypnosis_sub_states()` or reproduce its one-line correction. After that correction is present in the local integration baseline, the local bugfix layer SHALL retire the disabled cancel-clear wrapper because core supersedes it, keep BDD expectations on the clearing contract, and verify through the real loader and connected grant-to-settlement paths that the maintained mod set composes without a second behavioral owner.

Pain-as-pleasure is an intentional, explicit exception to the upstream rule that psychological pleasure does not settle while a character is asleep or unconscious: converted psychological pleasure SHALL post even for a sleeping or unconscious character. This override applies only to the pain conversion path; every other psychological-pleasure source keeps the upstream guard.

#### Scenario: Hypnosis is cancelled directly
- **WHEN** direct hypnosis cancellation settles for a target with `pain_as_pleasure`
- **THEN** the target's `pain_as_pleasure` flag is cleared by the corrected shared core cleanup
- **AND** a later positive pain settlement follows ordinary pain behavior unless the flag is granted again
- **AND** the retired local wrapper is not required to produce that result

#### Scenario: Character exits hypnosis through sleep
- **WHEN** sleep cleanup settles for a character with `pain_as_pleasure`
- **THEN** the character's `pain_as_pleasure` flag is cleared by the corrected shared core cleanup
- **AND** sleep and direct cancellation agree on the exit-clears rule

#### Scenario: Awake granted character has no active hypnosis unconscious state
- **WHEN** an awake, conscious character carries `pain_as_pleasure` while `unconscious_h == 0`
- **THEN** positive pain settles as psychological pleasure
- **AND** ordinary pain does not increase
- **AND** settlement does not change the character's unconscious or hypnosis state

#### Scenario: Sleeping or unconscious granted character takes positive pain
- **WHEN** a positive pain settlement occurs for a sleeping or unconscious character while `pain_as_pleasure` is active
- **THEN** the converted amount posts as psychological pleasure despite the upstream sleep/unconscious guard
- **AND** ordinary pain does not increase

#### Scenario: Pain decreases while pain-as-pleasure is active
- **WHEN** a pain state settlement has a non-positive final pain change
- **THEN** that change settles through the ordinary pain path
- **AND** the granted flag remains active afterward

#### Scenario: Common pain aliases settle positive pain
- **WHEN** default, second-effect, realtime, or item settlement invokes the shared positive pain handler for an awake, conscious character while `pain_as_pleasure` is active
- **THEN** every alias uses the same converted handler
- **AND** the amount is recorded under psychological pleasure rather than pain

#### Scenario: Direct second effect adds pain
- **WHEN** a direct second effect would add small, middle, large, or extra-orgasm pain to an awake, conscious character while `pain_as_pleasure` is active
- **THEN** the positive pain amount is settled as psychological pleasure instead of direct pain

#### Scenario: Later group participant receives and uses the grant
- **WHEN** a conscious NPC joins group sex after discovery or direct invitation, the group participant resolver includes that NPC, and hypnosis boost grants `pain_as_pleasure`
- **THEN** the NPC's next positive pain settlement converts to psychological pleasure
- **AND** the connected path does not depend on manually constructing the final character state
- **AND** the direct-invitation path is verified first, while the discovery branch is verified only after `fix-discovered-reaction-settlement` is available in the test baseline

#### Scenario: Enhancement is explicitly toggled off
- **WHEN** the ordinary toggle clears `pain_as_pleasure`
- **THEN** the next positive pain settlement follows ordinary pain behavior
- **AND** no patched alias or direct effect retains a hidden active copy of the grant

#### Scenario: Repeated instruction adjustment applies
- **WHEN** positive common pain is converted during a repeated instruction sequence
- **THEN** its psychological-pleasure amount follows the accepted upstream-equivalent adjustment sequence
- **AND** the conversion does not silently omit or double-apply an adjustment

#### Scenario: Converted value reaches the status cap
- **WHEN** converted psychological pleasure would exceed 99999
- **THEN** stored state remains within the configured cap
- **AND** the change record reports the upstream-compatible requested value consistently for both root and target-owned records

#### Scenario: Existing entry-specific death behavior applies
- **WHEN** a common or direct positive-pain entry is invoked for a dead character
- **THEN** the conversion preserves that entry's upstream early-return behavior
- **AND** the fix does not invent a universal guard that changes another entry's semantics

===== CURRENT T2 design tail =====

Submitted regression coverage should stay in one focused file with shared setup and table-driven inverse cases where practical. The expected test diff is at most roughly 250–300 lines. If proving the invariant needs several bespoke files or substantially more test code, stop and simplify the harness or revisit the boundary rather than encoding each reviewer clue as a separate fixture.

Key implementation risks are double-counting paired normal/extra input, merging provisional current counts into the failure release a second time, accidentally including unsupported keys, re-evaluating routing per part, or letting local replacement mods mask core verification. Focused tests and final diff review must target those risks without promoting them into new player-facing rules.

## Current PR Readiness

The candidate code, submitted tests, deterministic Tk evidence, Fable-written Chinese PR text, code-quality audit, and fresh artifact audit are complete. The durable record is [pr-readiness.md](pr-readiness.md), with the inspected evidence copied under [evidence/](evidence/).

On 2026-07-13, the user chose to exercise the same player-visible rule through `local_orgasm_settle_edge_fix` for several days before deciding whether to submit it upstream. This remains part of the decision history, but the fixed-days completion gate was superseded without being completed by the [2026-07-14 Fable program-document reconciliation ruling](../refactor-remaining-local-bugfixes-by-root-cause/fable-program-doc-reconciliation-20260714.md). The candidate remains `local-review-ready`; passive play is now optional and serves only as a source of new clues, any of which reopens the candidate.

Before an upstream PR is created, the user must give final confirmation of the shared-result gameplay rule, each outward action must receive separate authorization, and the candidate must be refreshed and retested against upstream after PR #214's merge. None of those pre-PR gates blocks further local program work.

===== CURRENT T2 tasks gate =====
## 4. Verification And PR Readiness

- [x] 4.1 Run the focused submitted regression, relevant existing core tests, `py_compile`, and `git diff --check`; separately run existing active local orgasm-batch/group-release tests for private confidence and exclude them from submitted tests and PR-facing proof
- [x] 4.2 Re-open the implementation, submitted tests, and complete upstream diff to confirm the live held ledger never contains provisional counts, one invocation has one decision and one application branch, failure cannot trigger caller replay, and unrelated paths remain unchanged
- [x] 4.3 Complete a deterministic normal Tk A/B route with `local_h_orgasm_batch_fix` and dependent `local_group_edge_release_fix` disabled; align exact revisions, mod configuration, save, route, and seed, then inspect the final 2070x1070 images
  - Completed on 2026-07-13 after the earlier blocked route was superseded. Baseline and candidate used save 99, seed `0`, the same six-wait route, and the same Tk geometry. The baseline shows duplicate results for 清流 and 特蕾西娅; the candidate shows one shared result for each. Durable copies and provenance are under `evidence/`.
- [x] 4.4 Use `fable-5` at medium effort for Chinese PR prose, apply the code-quality audit's comment-precision findings, then pass a fresh `review-erark-pr-artifacts` audit using only the exact proposed diff, submitted tests, and inspected PR-facing evidence
  - The fresh artifact audit returned `PASS` with `publication_state: local-review-ready`; the only remaining draft placeholders are the two image URLs, pending an authorized upload.
- [x] 4.5 Present the final local diff, verification, draft, and images to the user; request separate authorization before publishing evidence, pushing, or creating or editing a PR
  - The user reviewed the ready package and chose to test the behavior locally for several days before deciding whether to submit it upstream.

## 5. Historical Player-Test Gate And Current PR Gates

- [x] 5.1 Disable `local_h_orgasm_batch_fix` and its dependent `local_group_edge_release_fix`, then enable `local_orgasm_settle_edge_fix` on local development `main` so normal play exercises the candidate rule without applying the upstream core diff to `main`
- [x] 5.2 Preserve the candidate branch and local PR package: commit `579b7c47504038b6523decf71a565029ba76860a` on `pr-fork/codex/fix-edge-settlement-shared-decision`, with the exact proposed diff, tests, evidence, audits, and PR text recorded in this change
- [ ] 5.3 **Superseded without execution; not completed.** The former requirement to play the enabled test mod for several days was replaced by the [2026-07-14 Fable program-document reconciliation ruling](../refactor-remaining-local-bugfixes-by-root-cause/fable-program-doc-reconciliation-20260714.md). Passive play is optional and only supplies new clues; any new clue reopens the candidate.
- [ ] 5.4 **Superseded without execution; not completed.** The former accept-or-revise step coupled the fixed-days playtest to publication. Use the current pre-PR gates in 5.5–5.7 instead.
- [ ] 5.5 Before creating an upstream PR, obtain the user's final semantic confirmation that one settlement batch is collected, judged once, and given one shared result
- [ ] 5.6 Before creating an upstream PR, refresh the candidate against upstream after PR #214's merge and rerun the affected tests and review checks
- [ ] 5.7 Obtain separate authorization for each outward action, including publishing the two evidence images, pushing the refreshed branch, and creating or updating the upstream PR

===== CURRENT T2 readiness status and checklist =====
# PR Readiness Record

## Status

As of 2026-07-14, the candidate code and PR package remain `local-review-ready`. On 2026-07-13, the user chose to play the enabled local test mod for several days before deciding whether to submit the candidate; that historical choice was not completed. The fixed-days gate was then superseded without being marked complete by the [2026-07-14 Fable program-document reconciliation ruling](../refactor-remaining-local-bugfixes-by-root-cause/fable-program-doc-reconciliation-20260714.md). Passive play is now optional and serves only as a source of new clues, any of which reopens the candidate.

- Candidate worktree: `/home/ubuntu/games/erArk-pr-edge-shared-settlement`
- Candidate branch: `codex/fix-edge-settlement-shared-decision`
- Candidate commit: `579b7c47504038b6523decf71a565029ba76860a`
- Candidate base: `0268fe5719749b984a4a4b1ff69a94b42661f7ca` (`upstream/master` at the final rebase)
- Fork branch: `pr-fork/codex/fix-edge-settlement-shared-decision` on `https://github.com/meower-z/erArk-fork`
- Publication state: `local-review-ready`
- Upstream PR state: not created or updated by this work; image evidence has not been uploaded
- Current pre-PR gates: user final semantic confirmation; separate authorization for each outward action; refresh and retest against upstream after PR #214's merge
- Local playtest state: development `main` commit `fe3b67b318c9c46761cbb2778d1c7f76a65b2fa3`, pushed to `origin/main`

Local development `main` uses `local_orgasm_settle_edge_fix` to exercise the same player-visible settlement rule. The older player-action-window implementation `local_h_orgasm_batch_fix` and its dependent `local_group_edge_release_fix` are retained but disabled. The local test mod is not part of the upstream diff.

## Submitted Diff

---

## Publication Checklist

- [x] Candidate code and submitted tests ready
- [x] Fable PR text ready
- [x] Deterministic Tk evidence ready and inspected
- [x] Fresh artifact audit passed
- [ ] Historical several-day playtest completion — superseded without execution and not a current gate
- [ ] User final semantic confirmation obtained before upstream PR creation
- [ ] Candidate refreshed and retested against upstream after PR #214's merge
- [ ] Evidence images uploaded with user authorization
- [ ] Image placeholders replaced with final URLs
- [ ] Branch pushed and upstream PR created or updated with separate authorization for each outward action

===== CURRENT T4 proposal/design/tasks/notes =====
## Why

When `orgasm_settle` writes a distinguishable synchronous value inside effect 527, the old path mutates the NPC but records that direct change on the player's root settlement object. The code-level trigger proves the owner mismatch; normal-game reachability and a visible wrong heading still require a matched Tk route.

## What Changes

- Record the changes written directly by each nonzero effect-527 deferred release on that NPC's `TargetChange`.
- Preserve the original zero-count release marker, no-op call, and unconscious-state recovery. Effect 527 does not consume or replace queued second behaviors; the later generic pass is unchanged and outside this change's verification boundary.
- Verify actual stored experience and remote NPC effect-boundary ownership through the real core path, Web ownership through the real collection function, and normal-game reachability through a matched player-path Tk A/B when a discriminating route is proven.
- Run one local compatibility smoke with `local_h_orgasm_batch_fix`; keep that unpublished mod outside the upstream candidate.
- Keep compact-number formatting outside this change.

## Capabilities

### New Capabilities

- `time-stop-release-attribution`: Defines an NPC-owned settlement record for changes written directly by effect 527 for each nonzero deferred release.

### Modified Capabilities

None.

## Impact

This change affects time-stop effect 527 and settlement output collection. It does not change orgasm formulas, deferred counts, the zero-count release marker, time-stop instruction availability, the pre-action lifetime of射精位置, or the existing remote silent second-stage path.
## Context

Time-stop effect 527 iterates deferred NPC orgasm counts. The old path mutates the NPC selected by `character_id` but supplies the player's root `CharacterStatusChange` to orgasm settlement. When that call writes a synchronous value directly, the record therefore uses a different owner from the NPC being mutated. The attribution-only candidate is isolated from the earlier mixed local change, and its focused test now loads the real settlement registry and orgasm function in a subprocess.

The earlier player screenshot is consistent with six deferred body-part orgasms, but the six-NPC scene has not been replayed as matched runtime evidence.

## Goals / Non-Goals

**Goals:**

- Give effect 527's direct nonzero release changes a target-owned change object for the released NPC.
- Leave the later generic second-stage pass untouched; at the effect-527 boundary, confirm that this effect does not consume or overwrite an existing queue.
- Confirm in one non-blocking local ModManager smoke that the unpublished batch mod accepts the NPC-owned object.
- Prove actual stored experience, zero/multiple/remote NPC effect-boundary behavior, and renderer collection through real code paths.

**Non-Goals:**

- Change orgasm formulas, deferred counts, release multiplicity, or time-stop instruction premises.
- Change the existing lifetime of `shoot_position_body` or `shoot_position_cloth` before a player action.
- Refactor the remote silent second-stage path in `must_settle_check()` or make it share effect 527's change object.
- Correct compact K/M formatting; that is an independent change.
- Import unrelated Web waiting-protocol edits from the current local mixed diff.

## Decisions

### Create or reuse the target-owned object at effect 527

Effect 527 is the first point that knows which NPC's deferred state is being released. For a positive deferred count, it therefore creates or reuses `change_data.target_change[npc_id]` and passes that object to the synchronous `orgasm_settle` call. The generic pass remains unchanged and outside this decision boundary.

Alternative considered: move values from the player object after settlement. Rejected because formulas, caps, labels, and later second effects may already have read the wrong owner.

### Keep the unpublished batch mod outside the upstream candidate

The upstream candidate does not contain `local_h_orgasm_batch_fix`, and that component is disabled in local normal play. One real-ModManager smoke checks that the local component still accepts the NPC-owned object. Any compatibility edit belongs to a separate local component change, not this upstream PR.

Alternative considered: make the full mod-on matrix block the upstream PR. Rejected because an upstream reviewer cannot load or review that unpublished component.

### Preserve the zero-count release lifecycle

`time_stop_release` is read by talk selection, unconscious experience conversion, and later second-behavior logic. The candidate therefore preserves the original `time_stop_release = True` assignment and the original no-op `orgasm_settle` call when every deferred count is zero. Only calls with a positive deferred count switch to the NPC-owned `TargetChange`. Counter clearing and unconscious clothing/semen/stolen-item recovery remain unchanged.

The empty call itself does not create a target block. The later generic pass may still create an empty target entry for that NPC, as it did before this change; that behavior is outside the effect-527 assertion.

### Treat Web as an inverse collection check

The shared settlement record feeds both renderers. If a discriminating normal-game route is proven, matched Tk supplies the PR-facing player evidence. Web independently proves the effect-527 direct target-owned record is collected with the correct character ID and is not coupled to the frozen waiting protocol.

## Risks / Trade-offs

- **[Mock tests hide object-identity failure]** → add real-loader traces that assert identity, not merely equal dictionaries.
- **[Local batch mod rejects a direct target owner]** → run one real-ModManager compatibility smoke locally and keep any mod edit separate.
- **[Recorded experience differs from stored experience]** → compare the real NPC experience before/after with the emitted target-owned record.
- **[A code-level trigger is mistaken for a player route]** → describe `shoot_position_body = 2` only as an effect-boundary owner probe, and require a separate normal-UI Tk A/B before calling this a player-visible bug.
- **[Mixed local files widen the PR]** → isolate only the release-attribution hunks and independently inspect the final diff.
- **[Defensive player-ID exclusion lacks a production trigger]** → exclude that guard from the upstream candidate unless a real runtime trace first shows character ID 0 in the NPC iteration source.
## 1. Isolate the attribution candidate

- [x] 1.1 Reconstruct the attribution-only production diff from local commit `0b3f1c1a9` in a fresh linked worktree based on current `upstream/master`, excluding formatter and waiting-protocol edits
- [x] 1.2 Re-run the existing focused ownership cases and record which assertions execute extracted/mocked code rather than the real loader
- [x] 1.3 Through the real loader, compare each NPC's stored experience before/after with the values recorded on that NPC's settlement object

## 2. Close real runtime ownership

- [x] 2.1 Run the zero, one, multiple, and remote NPC identity matrix first on untouched `upstream/master` through the real loader and record the exact red effect-boundary failure where the code-level `shoot_position_body = 2` trigger records NPC release changes on the player's root `CharacterStatusChange`; then run the same matrix on the candidate with `local_h_orgasm_batch_fix` disabled and prove it turns green
- [x] 2.2 As a non-PR-blocking local compatibility check, load `local_h_orgasm_batch_fix` through the real ModManager and run one positive-count ownership smoke; keep any required mod edit in a separate local task
- [x] 2.3 Verify counter clearing and unconscious clothing, semen, and stolen-item recovery for zero-count as well as nonzero NPCs
- [x] 2.4 Through the real Web collection function, verify each target-owned experience record keeps the NPC character ID independently of `settlement_input`; do not change production waiting protocol in this change
- [ ] 2.5 If section 3 proves a normal player route that preserves the discriminating state until effect 527, use its matched Tk A/B to prove the displayed experience line visibly keeps the NPC identity

## 3. Produce player-facing evidence

- [x] 3.1 Prove or disprove a normal UI route in which NPC A gains positive deferred counts and a qualifying射精位置, the player switches the current target to NPC B without clearing A's state, and then releases time stop
- [ ] 3.2 If that route is reachable, build or recover one normal loadable checkpoint and capture matched pristine-baseline and attribution-candidate Tk output with the same save, seed, and physical actions; pre-release observation must show A's deferred counts and qualifying射精位置 still present while B is the current target
- [ ] 3.3 Inspect the full-resolution result frames and require a visibly identified experience owner plus conserved total values; do not use the superseded one-NPC route or an ambiguous screenshot
- [ ] 3.4 If the multi-target route and all other production paths cannot preserve a discriminating value until effect 527, return to Fable and retain the candidate only as a local synthetic-state fix, without preparing an upstream bug PR

## 4. Review and prepare the local PR package

- [ ] 4.1 Re-open the exact attribution diff, run focused and relevant time-stop/H regressions, `py_compile`, and `git diff --check`, and record skipped or coupled checks
- [ ] 4.2 Give all OpenSpec documents, the exact diff, and inspected evidence to Fable; apply required documentation corrections and obtain independent code/artifact PASS
- [ ] 4.3 Stop only the outward action pending separate authorization for evidence publication, push, and PR creation; continue the program queue meanwhile
## Current candidate

- Base: `upstream/master` at `06fc59c1e71d092224375fc4a096b956aea2ad63`.
- Worktree: `/home/ubuntu/games/erArk-pr-time-stop-release-attribution`.
- Production scope: one effect-527 hunk in `Script/Settle/default.py`; compact formatting, waiting protocol, generic second-stage guards, and local mod code are excluded.
- Zero-count behavior is intentionally preserved. `time_stop_release` remains true and the original no-op call still occurs because the flag is read by talk selection, unconscious experience conversion, and later second-behavior logic.

## Real-loader red and green evidence

The probe loads the real `Script.Settle` registry, real effect 527, real `Character` structures, real `second_behavior.orgasm_settle`, and real Web value collector. It does not extract the function with AST or replace orgasm settlement with a fake. It directly sets `shoot_position_body = 2` as a code-level trigger that makes `orgasm_settle` write a distinguishable synchronous value to the supplied change object. This proves routing at the effect boundary, not normal player reachability.

On untouched upstream, one NPC with one deferred skin orgasm and `shoot_position_body = 2` produced:

```text
root_exp_111 1
target_ids []
npc_exp_111 1
queued ['s_orgasm_small']
counter 0
release True
```

The NPC's actual experience and queued behavior changed, but its experience record landed on the player's root object.

With the attribution candidate, the same setup produced:

```text
root_exp_111 0
target_ids [1]
target_exp_111 1
npc_exp_111 1
queued ['s_orgasm_small']
counter 0
release True
```

`tests/test_time_stop_release_attribution.py` packages the probe as a subprocess test and covers zero, one, two, and remote NPC cases. A thin tracing wrapper records object identity and then calls the real orgasm function. It verifies actual stored experience, that one injected unrelated queue item remains present immediately after effect 527, zero/nonzero cleanup of body semen, clothing semen and stolen clothes, and Web collection under NPC IDs without using `settlement_input`. It does not execute or characterize the later generic pass.

The submitted test failed on untouched upstream and passed on the candidate:

```text
upstream: owner_identity was false for a positive release and the experience record remained on the root object
candidate: 1 passed in 0.71s
```

`python -m py_compile` and `git diff --check` also pass. Tk A/B remains open.

## Local batch-mod compatibility smoke

The unpublished `local_h_orgasm_batch_fix` was supplied as a local overlay and loaded through the real `ModManager` against the isolated attribution candidate. One remote NPC had one positive deferred skin-orgasm count plus an unrelated queued behavior. The first harness attempt exposed only a missing synthetic scene entry; after supplying two ordinary scene objects, the real mod load and settlement completed:

```text
mod_errors []
orgasm_module mod_local_h_orgasm_batch_fix
root_exp_111 0
target_ids [1]
target_exp_111 1
npc_exp_111 1
marker {1: {'s_orgasm_small'}}
unrelated_queued 1
counter 0
```

This proves the local mod accepts the direct `TargetChange`, stores its synchronous-consumption marker on that same NPC object, and leaves unrelated queued work intact at effect 527. It does not claim to verify how the later generic pass settles that queue. No mod code is included in the upstream candidate, and no compatibility edit was required.

## Fable scope ruling

Fable's later code/spec ruling is `CODE PASS / DOCS NARROW`: the production hunk remains limited to effect 527's synchronous ownership, while follow-up generic settlement, remote silent settlement, and射精位置 lifetime stay outside this change. The registry test is sufficient for that code boundary after its helper docstring is fixed.

The same ruling revoked the earlier one-NPC Tk route. `judge_before_pl_behavior()` clears the current target's `shoot_position_body` before effect 527, while all non-shoot-position orgasm effects are queued and use a target block in both baseline and candidate. Therefore the one-NPC release cannot display the ownership difference. A normal multi-target route must preserve NPC A's positive deferred counts and qualifying射精位置 after switching the current target to NPC B. Until that route is proven, the real-loader evidence establishes a synthetic effect-boundary defect but not yet a reviewer-ready normal-game bug.

## Multi-target route checkpoint

A normal-UI exploration from `save/8` proved the required state is reachable without injection. Four oral actions against Lin (4080), with the fourth choosing the normally presented ejaculation option, produced deferred counts `{0: 1, 21: 2}` and `shoot_position_body = 2`. Clicking Jingzhe (306) in the visible current-scene character list changed only `target_id`: a post-switch observer retained Lin's complete trigger object byte-for-byte, and `[4115]` remained visibly available. The exploration stopped before release and therefore is route evidence only, not a baseline result.

Fable returned `FORMAL ROUTE PASS` and froze the current-upstream matched replay: Lin is A, Jingzhe is B, the fourth oral action must present and use the ejaculation option, and both sides must reach the exact post-switch gate before `[4115]`. The formal replay uses the shorter matched viewport sequence approved by Fable and must be discarded if either side differs in action count, trigger state, target, time-stop/H state, or fourth-action prompt.
--- END EXACT PROMPT ---

