# Fable Supervision Record

## Invocation

Every call used the project-required command and no tools or persistent session:

```text
claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence "<prompt>"
```

## Project Skill Protocol Draft

### Prompt

```text
<authority>
Draft a new reusable section for the existing erArk project skill investigate-game-bug. The user has explicitly delegated supervision of non-trivial investigation, refactor-boundary, consolidation, and architecture decisions to claude-fable-5.
</authority>

<context>
The skill already requires root-cause evidence, red-capable reproduction, explicit logical ownership, comparison of symptom patches with preventive refactors, and a fresh-context critic before production edits. It is written in concise imperative English and is currently 185 lines. The new section must change agent behavior without repeating those existing gates.
</context>

<required_behavior>
- Invoke the Claude CLI exactly as: claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence "<prompt>".
- Use Fable as a skeptical design supervisor after enough concrete evidence has been collected, not as the worker that performs repository inventory or other heavy legwork.
- Give Fable raw decision-relevant evidence, alternatives, uncertainties, and constraints. Do not praise the current plan, call it strong, frame it as nearly accepted, disclose the preferred verdict as a desired answer, or ask merely for confirmation.
- Ask it to look for wrong ownership, shallow fixes, hidden policy choices, incomplete causal radius, unnecessary complexity, and reasons to reject or split the proposal. Leave room for a materially different design.
- If Codex and Fable disagree, Codex may make one follow-up call that adds missing evidence and states its counterargument without asking Fable to defer. Fable's answer to that follow-up is final for the reversible design/workflow decision in scope.
- Fable cannot override user-stated goals or gameplay decisions, verified repository facts, safety rules, approval requirements, or outward-action gates. A factual conflict must be resolved against primary evidence rather than by vote.
- Preserve the Fable prompt, initial verdict, any rebuttal, and final verdict in the owning investigation or change record when that record exists.
</required_behavior>

<draft_request>
Choose the section title, placement logic, and most economical structure. Return only the ready-to-insert Markdown section. Keep it concise enough for the main SKILL.md; no rationale, examples, provenance notes, or surrounding diff.
</draft_request>
```

### Result

Fable returned the `Design supervision (Fable)` section now present verbatim in `.codex/skills/investigate-game-bug/SKILL.md`.

## Migration Audit

The audit prompts embedded the complete source `tasks.md` and the then-current `task-migration.md` after the fixed prompt text recorded below. This keeps the source wording available to Fable instead of asking it to trust a summary.

### Initial Prompt

```text
Act as the skeptical final design supervisor for an erArk OpenSpec umbrella-task migration. The repository inventory and classification legwork have already been done. Do not assume the ledger is sound. Look for reasons to reject it, split destinations, or change ownership.

Verified facts: the source and ledger each cover 160 unique IDs; PR #212, #213, and #214 are open at their verified heads; PR #214 has commit-pinned public Tk A/B images and a one-file diff; the seven-change OpenSpec list and zero-legacy-session allocator state were supplied; this is planning only and may not decide gameplay semantics or perform outward actions.

Audit every row for wrong ownership, unfinished work marked complete, broad tasks assigned to narrow PRs, hidden gameplay choices, mixed causal radii, non-durable destinations, and rows that must be split. Return VERDICT, exact blocking task IDs and required replacements, nonblocking notes, and a final migration rule. A 160-row match is not evidence that ownership is correct.

[The complete source tasks and initial migration ledger followed verbatim.]
```

### Initial Verdict: REVISE

Fable identified four blockers:

1. Discovery settlement was assigned to a proposed `settle-discovery-behavior-once` name while the existing `fix-discovered-group-participant-admission` change already owned the slice.
2. `2.3k` mixed merged PR #206 same-witness history with stale-hidden-flag/effect-411 evidence belonging to the retained discovery candidate.
3. `3.5`, `4.5`, `5.5`, `7.4`, and `8.1`–`8.4` used plural placeholder destinations instead of named owners; `8.2` also mixed deferred Windows font evidence into current work.
4. Open-PR ownership had no fallback if a PR closed unmerged.

It also required `8B.10`–`8B.12` to avoid implying that unchecked historical local gates had passed.

### Revision

The ledger was revised without disputing those findings:

- discovery rows now use the existing change, explicitly narrowed to discovery settlement;
- `2.3k` and every broad multi-owner task are split into suffixed, single-destination obligations;
- open PR rows remain conditional until merge and revert to a named `re-file, revise, or withdraw` decision if closed unmerged;
- old PR #214 notes no longer infer unverified local gate completion;
- source coverage now consists of 219 unique obligations which normalize to exactly the original 160 IDs.

### Revised-Ledger Prompt

```text
Act as the final skeptical supervisor for the revised migration. Re-test the four initial blockers, reject aliases without a checkable existing owner or named decision/evidence record, look for new blockers introduced by splitting, and return a final ACCEPT or REVISE. The complete original tasks and revised migration ledger follow verbatim.
```

### Revised-Ledger Verdict: REVISE On A Factual Premise

Fable agreed that all four design blockers were resolved, but claimed that five named owners were archived and that only the umbrella and discovery change were active. It therefore rejected current obligations pointing to those supposed archived owners.

That claim contradicted primary evidence and could not come from a repository lookup because the call had `--tools ""`:

- `openspec list --json` showed all seven active changes;
- `stat` succeeded for all six non-umbrella active directories;
- the archive search found no matching archived directory;
- `git ls-tree` listed all six directly under `openspec/changes/`;
- the edge change was 21/23 with a live player-test gate, not the superseded visual-evidence blocker;
- the curve change was 0/12 with an explicit measurement and user-approval gate, not an archived 7/7 change.

## One Allowed Evidence Follow-up

### Prompt

```text
This is the single evidence-and-counterargument follow-up allowed by the project supervision protocol. Your answer is final for this migration step. Resolve factual claims against supplied primary repository evidence.

The prior archived-owner premise conflicts with fresh `openspec list --json`, `stat`, an empty matching archive search, and `git ls-tree`. All six non-umbrella changes are active. The current edge tasks leave only user playtest and the later accept/reopen/publication decision unchecked; the old save99 blocker is superseded by completed matched Tk A/B evidence. The current curve change is 0/12 and begins with measurement plus explicit user approval.

Therefore the prior three blockers rest on a false archived-owner premise. Re-evaluate after applying this correction and return FINAL VERDICT, exact blocking obligations or None, concise rationale, and a retirement decision that distinguishes accepting the ledger from retiring the umbrella now.

[The complete revised migration ledger followed verbatim.]
```

### Final Verdict: ACCEPT

Fable found no remaining blocking issue. It accepted the ledger's ownership, suffix accounting, semantic gates, open-PR fallback, withdrawal history, and live edge/curve destinations.

Its retirement decision was narrower: acceptance applies only to the migration ledger. The umbrella cannot be retired until the later rewrite creates the named decision/evidence records, moves every current obligation into its active owner, performs the discovery narrowing and time-stop split, and confirms upstream tracking links.

## Remaining Bugfix De-duplication Review (2026-07-14)

### Initial Prompt

```text
Act as the skeptical final supervisor for the remaining erArk bugfix queue. The repository and GitHub legwork is complete. Do not assume the proposed queue is correct; look for duplicate work, stale documents, hidden gameplay decisions, wrong ownership, and a reason to stop or reorder work.

Verified evidence supplied:
- Upstream PR #206 is merged and owns only exclusion of the same witness before movement. No upstream PR or remote branch owns discovery settlement, and a later different eligible witness remains allowed.
- Discovery candidate `5d360f71e` is a four-file panel-owned typed-result protocol. Thirty-five focused tests pass; deterministic real-Tk A/B and logic, implementation, evidence, and artifact reviews pass. The draft still has an unpublished GIF placeholder.
- PR #212 owns signed pain routing. PR #213 makes sleep and direct hypnosis cancellation preserve `pain_as_pleasure`. Local main overlays both, the old pain mod is disabled, and the active pain documents/mod wrapper/BDD still contain the obsolete cancellation-clears expectation.
- Orgasm-edge candidate `579b7c475` has 11 focused tests, matched real-Tk A/B, and passing reviews. Its remaining gates are user playtest acceptance and later publication authorization.
- Time-stop release code is already on local main through `0b3f1c1a9`; its two focused files pass together (58 tests). Real loader/object identity, actual delta/cap, real Tk/Web, unrelated queues, and global formatter call sites remain unverified.
- `fix-talk-common-state-leaks` owns two still-unimplemented state leaks: temporary player target is not restored, and a global configured candidate list is mutated with `+=`.
- Type-1 ordering, invitation lifecycle, H-entry movement, atomic new registration, and the tired-exit candidate are rejected or withdrawn. NPC cadence, zero/one-survivor scheduler policy, broad prompt/reconnect policy, the pleasure curve, and deeper orgasm transaction/chaining/exit policy are gameplay/product questions and must stay frozen.

Return: (1) verdict; (2) work that must not be repeated; (3) exact documentation corrections; (4) the ordered plain-bugfix queue; (5) gameplay items to freeze; (6) only questions that genuinely require the user now; and (7) risks. Do not treat local polish as proof and do not infer missing gates.
```

### Initial Verdict: ACCEPT EVIDENCE, WITH THREE BOUNDARY CORRECTIONS

Fable agreed that the documented candidates and live PRs must not be repeated. It ordered documentation reconciliation first, then time-stop verification, then the two talk-state fixes, then remaining pain connected-path verification. It kept discovery and orgasm-edge out of new implementation and froze all listed gameplay/product decisions. It found no user question needed before the plain-bugfix queue.

Fable initially inferred an extra discovery playtest gate and proposed deleting the old global-wrapper history plus editing the stale pain wrapper/BDD during the documentation pass. Those three points conflicted with supplied primary boundaries: the artifact review names publication approval as discovery's next gate, rejected history must remain reachable, and OpenSpec explore mode permits documents but not production/test edits.

### One Allowed Evidence Follow-up

```text
This is the single evidence-and-counterargument follow-up allowed by the project supervision protocol. Your answer is final for this queue decision.

Correction 1: the discovery artifact review explicitly says the candidate can proceed to human publication approval; there is no discovery playtest gate. The unpublished GIF URL, push, and PR creation are the remaining separately authorized outward actions.

Correction 2: preserve the old global-wrapper experiment as clearly superseded/rejected history rather than deleting it.

Correction 3: this turn is OpenSpec explore work. Update OpenSpec and README truth now, but do not edit production code or tests. Record removal of the obsolete pain cancel-clear wrapper and revision of its BDD expectation as later implementation tasks under the fixed PR #213 contract.

Re-evaluate only these points and return FINAL VERDICT, final documentation actions, final discovery gate, final user questions now, and the next plain bugfix after documentation.
```

### Final Verdict: ACCEPT CORRECTION

Fable accepted all three corrections. Its final decision is:

- discovery has no playtest gate; only separately authorized evidence publication, push, and PR creation remain;
- preserve the old wrapper experiment as superseded/rejected history;
- record the stale pain wrapper/BDD cleanup as later implementation work;
- keep the plain-bugfix queue and frozen gameplay list unchanged;
- ask the user no question now;
- after document reconciliation, verify the existing time-stop fix before implementing the new talk-state leak fixes.

## Expanded Program Authority Draft (2026-07-14)

### Prompt

```text
<authority>
The erArk user has expanded claude-fable-5 from a design critic into the decision supervisor for the remaining local-bugfix program. Draft a concise replacement for the existing SKILL.md section titled Design supervision (Fable). The section is execution-facing project instruction, not a provenance record.
</authority>

<existing_behavior>
The current section invokes exactly:
claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence "<prompt>"
It requires evidence before consultation, neutral prompts, one evidence-and-counterargument follow-up when Codex disagrees, final Fable authority for reversible design/workflow decisions, fact resolution against primary evidence, and preservation of prompts/verdicts in the owning change record.
</existing_behavior>

<new_user_delegation>
- Fable judges whether player-visible evidence is strong enough to convince a human reviewer that a behavior is a real bug worth fixing. If evidence is weak, it chooses the next evidence question or route; work continues.
- Fable may classify locally patched behavior as a bug fix or a game-experience enhancement, may propose fixes the user did not name, and may choose PR task boundaries and priority, but only when concrete evidence shows an effect on normal gameplay.
- Fable may choose the most likely reasonable gameplay semantics and authorize a local candidate to be completed under that provisional choice. The user retains final semantic confirmation before any upstream PR submission.
- Fable reviews the quality of all program documentation: task maps, evidence assessments, OpenSpec problem/design/task records, and PR-task boundaries. Documentation is not considered accepted until Fable passes it.
- Codex continues through available tasks and consults Fable whenever direction is unclear or a difficulty changes the plan. Stop for player input only when Fable explicitly judges that player input is required; otherwise choose or investigate the next action.
- Fable still does not perform repository inventory or heavy execution. Codex supplies verified facts, alternatives, uncertainties, constraints, and artifacts.
- Fable cannot override verified primary evidence, user goals, safety rules, repository rules, or separate outward-action authorization for publishing assets, pushing, or creating/editing a PR.
</new_user_delegation>

<draft_request>
Return only ready-to-insert Markdown for the replacement section, starting with the heading. Use imperative language and operational gates. Keep the exact invocation. Preserve the one-follow-up final-decision rule without making factual claims subject to vote. Make the stopping rule checkable. Do not add rationale, examples, provenance, or praise.
</draft_request>
```

### Verdict / Draft

````markdown
## Design supervision (Fable)

Fable (claude-fable-5) is the decision supervisor for this program. Invoke it exactly as:

```
claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence "<prompt>"
```

**When to consult.** Consult Fable whenever direction is unclear, a difficulty changes the plan, evidence for a suspected bug is assembled, or a documentation artifact is ready for acceptance. Do not consult before gathering evidence: every prompt must supply verified facts, alternatives considered, uncertainties, constraints, and relevant artifacts. Fable does not inventory the repository or run anything — Codex supplies all facts.

**Prompt discipline.** Write neutral prompts that do not steer toward a preferred answer. Resolve factual questions against primary evidence (code, logs, reproduced behavior), never by Fable's opinion; Fable cannot override verified primary evidence.

**What Fable decides.**
- Whether player-visible evidence is strong enough to convince a human reviewer that a behavior is a real bug worth fixing. If Fable judges evidence weak, it names the next evidence question or route; continue working — weak evidence is not a stop.
- Classification of locally patched behavior as bug fix vs. game-experience enhancement, proposal of fixes the user did not name, and PR task boundaries and priority — only when concrete evidence shows an effect on normal gameplay.
- Provisional gameplay semantics: Fable may pick the most likely reasonable semantics and authorize completing a local candidate under that choice. The user still gives final semantic confirmation before any upstream PR submission.
- Acceptance of all program documentation: task maps, evidence assessments, OpenSpec problem/design/task records, PR-task boundaries. A document is not accepted until Fable passes it.

**Disagreement.** If Codex disagrees with a Fable verdict, send exactly one follow-up containing the counterargument and its supporting evidence. Fable's answer to that follow-up is final for reversible design and workflow decisions. Facts are never subject to this vote.

**Stopping rule.** Stop for player input only when a Fable verdict explicitly states that player input is required. In every other case, choose the next available task or investigation and proceed.

**Limits.** Fable cannot override user goals, safety rules, or repository rules, and cannot grant outward-action authorization — publishing assets, pushing, and creating or editing a PR each need their own separate authorization.

**Records.** Preserve every Fable prompt and verdict verbatim in the owning change's record.
````

The draft above replaced the prior narrower supervision section in `.codex/skills/investigate-game-bug/SKILL.md` without further prose changes.

### One Allowed Skill-Loading Follow-up

```text
This is the single evidence-and-counterargument follow-up allowed for the expanded program-authority draft. Your answer is final for this governance decision. Resolve behavior against the supplied direct CLI evidence.

New verified evidence:
1. All project skill directories are valid relative symlinks under .claude/skills and each resolves to a SKILL.md.
2. With the required --tools "" invocation, a bare prompt asking for visible skills returned: No project skills are visible to this session.
3. With the same model, effort isolation, --tools "", and no-session-persistence, a prompt beginning with /investigate-game-bug successfully loaded the symlinked skill and returned its exact prescribed Fable command.
4. Therefore links work, but project skills must be invoked explicitly by slash name in a tool-free Fable call; automatic discovery cannot be assumed.

Counterargument to the initial draft:
The draft says every prompt supplies facts but does not require loading the governing project skill. Without an explicit slash invocation, Fable cannot see the very rules the user asked to expose. The rule should require Codex to begin each Fable prompt with the relevant project skill slash invocation or invocations, always including /investigate-game-bug for this program, before the neutral task payload. Do not grant file tools or relax --tools "".

Return only FINAL VERDICT and a complete ready-to-insert replacement section. Preserve every accepted authority, evidence, documentation, disagreement, stopping, fact, semantic-confirmation, and outward-action rule from the initial draft. Add only the minimum operational language needed for explicit skill loading.
```

### Final Verdict: ACCEPT THE COUNTERARGUMENT

Fable found the direct CLI evidence decisive: valid symlinks do not imply automatic skill discovery in a tool-free session, while the explicit `/investigate-game-bug` invocation loaded the skill successfully. Its final governance decision requires every Fable prompt in this program to begin with `/investigate-game-bug` plus any other relevant project skill slash invocation, without relaxing `--tools ""` or granting file tools.

Fable could not mechanically reproduce the entire replacement section because the follow-up prompt did not repeat that source text and the session had no file tools. It supplied the exact minimal paragraph now inserted into the skill; the initial accepted draft remains otherwise unchanged.

## Discovery Settlement Evidence Review (2026-07-14)

### Prompt

```text
/investigate-game-bug

你是 erArk 上游维护者的独立证据审查者。不要假设现有方案正确，也不要因为测试数量或先前评审通过就放宽标准。请判断下面的玩家可见证据，是否足以让一个第一次看到此 PR 的人类维护者相信：这是正常游戏里值得修的 bug，而不是作者偏好的文本顺序或刻意留白。

已核实场景：同一存档、同一输入、Python random 与 NumPy RNG 及 PYTHONHASHSEED 在启动前固定一致。博士在健身区与杜宾进行 H，可露希尔发现。玩家选择 [1] 用花言巧语支开对方，界面明确显示 对方的态度：接受，判定成功。

修复前截图的连续可见结果：接受判定后，画面直接显示杜宾的身体/动作文本；没有任何可露希尔接受解释、离开健身区或数值变化的反应。

候选截图的连续可见结果：接受判定后，显示 可露希尔半信半疑地听完了博士的解释，觉得自己大概是真的误会了，于是离开了健身区，不再打扰博士的要求；随后显示 可露希尔：气力 -15 和 5分钟过去了；之后才继续杜宾的身体/动作文本。该反应出现一次。

对照在玩家选择前完全一致；证据在上述发现者反应与随后原行动恢复处停止，没有拿后续其他发现者作证据。

已核实机制：同一个发现面板有两类生产调用方。NPC 状态机路径会在面板外补结算发现者；直接发现路径没有外层补结算。面板选项又不统一：部分选项自行结算发现者行为，部分只设置行为、依赖外层。因此明确的发现者行为在不同入口可能零次或两次结算。候选把每个明确发现者行为的一次提交收归面板，并返回一个带发现者 ID、已结算行为、替代行为的结果给调度器，防止外层重放；改 4 个生产文件，100 行新增、31 行删除。

相邻但不同的已合并 PR #206 只阻止玩家未移动时同一个见证者再次发现；本证据不声称修复见证者选择，只证明玩家已经得到接受判定后，当前发现者的明确反应被漏掉。

PR 拟写问题陈述：H中被其他角色发现时会弹出面板让玩家选择应对。修复前，发现者对玩家选择的明确反应可能整段缺失：本场景选择支开且成功后，画面直接继续杜宾的 H 文本，可露希尔接受解释、离开健身区的整段反应没有出现。

请给最终裁决：
1. PASS 或 FAIL：证据能否说服冷读的人类读者这是正常游戏中的、值得修的 bug。
2. 最强的反对解释是什么，例如这是刻意无文本、截图断点误导、或只影响内部数值。
3. 现有材料如何排除或没有排除该解释。
4. 若 FAIL，规定下一步最强且尽量小的取证路线；若 PASS，说明 PR 中必须保留的最小证据和措辞，以及必须删掉或弱化的过度主张。
5. 另行判断 4 文件/69 净增行的修复范围是否会让维护者觉得证据和改动不相称；若会，指出必须补充的接口级理由或需要缩小的边界。

不要提出需要玩家本人判断，除非仅凭仓库与正常游戏证据确实无法继续。你对这次证据门槛和可逆任务边界有最终决定权。
```

### Verdict

```text
**裁决：PASS（附一项必须落实的核实/措辞条件）。**

**1. 结论**

证据足以让冷读的维护者相信这是正常游戏中值得修的 bug——前提是 PR 明确一件事：候选画面中的可露希尔反应文本与「气力 -15」结算来自**既有的生产文本与结算逻辑**，修复只是让它在直接发现路径上被执行一次，而没有新增任何对话内容。如果这一点不成立（反应文本是本次新写的），裁决降为 FAIL，因为"刻意留白"的辩护会重新成立。请在提交前核实这一点并写入问题陈述。

**2. 最强反对解释**

"刻意留白"：作者有意让支开成功后不给发现者反应文本，直接回到 H 场景，属于文本节奏偏好而非 bug。

**3. 现有材料如何排除它**

两点合力排除，缺一不可：

- **缺失的不只是文本，还有机制结算。** 修复前连「气力 -15」和时间消耗都没有——数值结算不是文风选择。一个行为被设置却从不结算，是状态机漏洞，不是留白。
- **同一面板选项在另一入口会结算。** 已核实 NPC 状态机路径会在面板外补结算发现者，直接发现路径没有。作者意图不会按调用入口不同而变化；同一选择在两个入口产生不同结果，只能是不一致，不能是设计。

第二点目前是代码级证据而非截图级，这可以接受——但 PR 里必须用一两句话把这个入口不对称说出来，否则冷读者只看到一对截图，"留白"解释无法被排除。

**4. PR 必须保留 / 删掉的内容**

保留（最小集）：
- 现有问题陈述（写得对：只声称"明确反应可能整段缺失"，不碰见证者选择）。
- 一对 Tk 前后截图（接受判定 → 修复前直接续 H 文本 / 修复后反应 + 气力 -15 + 时间 → 恢复 H）。
- 两句机制说明：同一发现面板有两类入口，一类外层补结算、一类没有；面板选项又不统一，导致明确的发现者行为在不同入口零次或两次结算。修复把结算收归面板执行恰好一次，并向调度器返回已结算标记防止重放。
- 一句声明：反应文本与数值结算均为既有内容，本修复不新增文本。

删掉或弱化：
- 种子、PYTHONHASHSEED、A/B 装置细节——留在本地记录。
- 与 PR #206 的对比不超过一句（"与 #206 的重复发现问题不同"即可）。
- 不要把"两次结算"写成已观察到的玩家可见 bug，除非确有截图；作为代码级风险陈述即可。
- 不要写非目标清单、调查历史、文件列表。

**5. 改动规模是否与证据相称**

4 文件 / 净增 69 行对一对截图，冷读者会问"为什么不是在直接发现路径补一行结算"。必须补的接口级理由（一段即可）：症状补丁会把"零次"修成"在某些入口两次"，因为外层补结算仍在；唯一能同时消除零次和两次的边界是把提交收归面板并返回已结算结果。只要这句话在 PR 里，规模是相称的，不需要再缩小边界。反之，如果 4 个文件里有任何与"结算恰好一次"契约无关的整理（重命名、顺带清理），从这个 PR 里剥出去。

不需要玩家本人介入；上述条件均可由仓库证据（确认反应文本在既有 talk 数据中）自行闭合。
```

### Condition Closure

The candidate base `06fc59c1e` already contains the generic `see_h_but_deceived` talk row, the five-minute behavior configuration, and effects `364 - 1512 - 1523 - 1721`. Effect `1512` is the existing small self mana-point cost, calculated as five minutes times three mana points to produce the visible `-15`. The candidate diff changes no talk, CSV, or settlement file. Therefore the candidate exposes existing production narration and settlement; it does not add them.

## Discovery Settlement PR Draft Review (2026-07-14)

### Initial Prompt

```text
/investigate-game-bug

你现在只做发现者结算 PR 文档的最终质量验收，不重新选择修复。上一轮你的证据裁决为 PASS，条件是核实反应文本与气力结算来自既有生产内容，并解释为什么不能在直接路径补一行。

已闭合事实：候选基线 06fc59c1e 已有 data/talk/sex/start_or_end/see_h_but_deceived.csv 的通用反应：发现者半信半疑听完解释、认为误会、离开当前场景；已有 Behavior_Data 中 5 分钟的 see_h_but_deceived；已有 Behavior_Effect 的 364 - 1512 - 1523 - 1721，其中 1512 是按每分钟 3 点减少自身气力，5 分钟得到 -15。候选 diff 不修改 data/talk、data/csv 或 Script/Settle。

待验收 PR 正文如下：

标题：修复「H中被发现」后发现者反应漏结算或重复结算的问题

问题：H中被其他角色发现时会弹出「H中被发现」面板让玩家选择应对。修复前，发现者对玩家选择的明确反应可能整段缺失：在健身区与杜宾H被可露希尔发现，选择 [1]用花言巧语支开对方 且判定成功后，画面直接继续杜宾的H文本，可露希尔接受解释、离开健身区的既有反应及对应的气力、时间结算完全没有出现。本修复不新增对话或数值规则，只让游戏已有的发现者行为正常结算。

原因：该面板有两类调用方：NPC行动调度路径会在面板外对发现者再补一次结算，而直接发现路径没有这层外层结算。面板内各选项又不一致——有的自己结算发现者行为，有的只设置行为、指望外层来结算。结算所有权不统一，已造成直接发现路径漏结算；从代码上看，其他入口也存在重复结算风险。

修复：把明确的发现者反应统一收到面板内部，在面板关闭时一次性提交结算，并把结算结果 DiscoverySettlementResult 返回给NPC调度器。调度器收到结果后跳过已在面板内结算完的原行为；只有当面板结算又产生了仍待处理的后继行为时，才在当前轮继续结算它。不能只在直接发现路径补一次结算，否则原本带外层结算的入口会重复执行；由面板统一提交并通知调度器，是同时避免漏结算和重复结算的最小接口边界。

验证：同一存档、同一输入下的Tk实机前后对比：修复前，选择支开对方已显示为接受，但可露希尔的接受、离开反应整段缺失，直接继续杜宾的H文本；修复后，可露希尔接受解释并离开健身区的完整反应出现一次，之后才继续杜宾的H文本。正文只嵌入两帧前后 GIF，不写种子装置、文件列表或调查历史。

请返回：PASS 或 FAIL；任何会削弱人类可信度的标题/措辞问题；若 FAIL 给出精确替换文案。文档只有 PASS 才算验收。不要要求玩家介入，除非仓库证据无法闭合。
```

### Initial Verdict

```text
**FAIL** — 两处措辞会削弱人类可信度，各给替换文案。

**1. 标题过度声明「重复结算」。** 实机证据只证明了漏结算；重复结算在正文里明确只是「从代码上看……存在重复结算风险」，从未被观测。标题把静态推断的风险与已验证的缺陷并列为已修复的问题，审阅者对照验证段会发现只演示了一半，反而怀疑另一半。修复防止重复结算是接口设计的收益，放在「修复」段陈述即可，不需要进标题。

替换标题：

> 修复「H中被发现」后发现者反应漏结算的问题

**2. 验证段末句是写作指令泄漏，不是给审阅者的内容。**「正文只嵌入两帧前后 GIF，不写种子装置、文件列表或调查历史」是对文档自身的元描述——审阅者读到这句会立刻意识到这是按清单生成的文本，且「不写……」列举了一堆他本不知道存在的东西。整句删除，替换为指向证据本身的一句：

> 前后对比 GIF 见下。

**次要（不阻塞，建议顺手改）：** 「修复前，选择支开对方已显示为接受」表意别扭——「已显示为接受」主语不明。建议改为「修复前，支开判定已提示成功」。

其余各段核对通过：问题段的反应文本与气力/时间结算均对应基线 06fc59c1e 的既有生产内容（see_h_but_deceived.csv 通用反应、5 分钟行为、效果 1512 每分钟 -3 气力共 -15），候选 diff 不触碰 data/talk、data/csv、Script/Settle，与「不新增对话或数值规则」的声明一致；「为何不能只在直接路径补一行」的解释（带外层结算的入口会重复执行）准确且是理解修复边界所必需的推理，保留。`DiscoverySettlementResult` 是 diff 中真实存在的代码接口名，出现在修复段合理。

按上述两处替换后即可 PASS，无需玩家介入。
```

### Recheck Prompt

```text
/investigate-game-bug

这是发现者结算 PR 文档的复验。上一轮你判 FAIL，并要求：标题删去未经实机证明的重复结算；验证段删除写作指令泄漏，改成前后对比 GIF 见下；把已显示为接受改成支开判定已提示成功。三项已逐字落实。

现稿：
标题：修复「H中被发现」后发现者反应漏结算的问题

问题：H中被其他角色发现时会弹出「H中被发现」面板让玩家选择应对。修复前，发现者对玩家选择的明确反应可能整段缺失：在健身区与杜宾H被可露希尔发现，选择 [1]用花言巧语支开对方 且判定成功后，画面直接继续杜宾的H文本，可露希尔接受解释、离开健身区的既有反应及对应的气力、时间结算完全没有出现。本修复不新增对话或数值规则，只让游戏已有的发现者行为正常结算。

原因：该面板有两类调用方：NPC行动调度路径会在面板外对发现者再补一次结算，而直接发现路径没有这层外层结算。面板内各选项又不一致——有的自己结算发现者行为，有的只设置行为、指望外层来结算。结算所有权不统一，已造成直接发现路径漏结算；从代码上看，其他入口也存在重复结算风险。

修复：把明确的发现者反应统一收到面板内部，在面板关闭时一次性提交结算，并把结算结果 DiscoverySettlementResult 返回给NPC调度器。调度器收到结果后跳过已在面板内结算完的原行为；只有当面板结算又产生了仍待处理的后继行为时，才在当前轮继续结算它。不能只在直接发现路径补一次结算，否则原本带外层结算的入口会重复执行；由面板统一提交并通知调度器，是同时避免漏结算和重复结算的最小接口边界。

验证：同一存档、同一输入下的Tk实机前后对比：修复前，支开判定已提示成功，但可露希尔的接受、离开反应整段缺失，直接继续杜宾的H文本；修复后，可露希尔接受解释并离开健身区的完整反应出现一次，之后才继续杜宾的H文本。

前后对比 GIF 见下。

请只判断上述要求是否落实且文档现在能否 PASS。若仍 FAIL，指出新的实质问题；不要为了风格偏好制造新门槛。
```

### Final Verdict

```text
**PASS。三项要求已落实，无新的实质问题。**

逐项核对：

1. **标题**：现为「修复『H中被发现』后发现者反应漏结算的问题」，只声明实机证明过的漏结算，重复结算已移出标题。✓
2. **验证段**：以实机前后对比事实收尾，「前后对比 GIF 见下」是对读者的正常指引，无写作指令泄漏。✓
3. **措辞**：改为「支开判定已提示成功」，准确限定在游戏实际提示的内容，不再声称发现者「已显示为接受」。✓

整体复核（非新门槛，仅确认无回退）：

- 重复结算在正文中的表述是「从代码上看，其他入口也存在重复结算风险」，明确标注为代码层面推断，与实机证明的漏结算区分清楚，且在修复段作为设计理由使用是正当的——这正是解释「为什么不能只补一次结算」所必需的推理。
- 问题→原因→修复的顺序成立，每个前缀独立可读，不依赖后文补救。
- 「H中被发现」「花言巧语支开对方」「气力」均为游戏既有用语；`DiscoverySettlementResult` 是提交代码中的实际类型名，可直接出现。

文档可以进入下一步（配合 GIF 实物一并提交人审）。注意本 PASS 仅覆盖文档文本；GIF 本身仍需按证据规则用 `view_image` 逐帧确认可读且 A/B 可比后再随稿发布。
```

### GIF Verification

The local GIF contains exactly two `1200x972` frames, each displayed for 2.5 seconds. Both frames were extracted and inspected at original resolution with `view_image`. The first is the accepted-dismissal baseline with no Closure reaction before Dobermann's action resumes. The second is the matched candidate frame with Closure's existing departure narration, `气力 -15`, and `5分钟过去了` before the same action resumes. The labels, game text, and difference are readable; no later witness is shown.
