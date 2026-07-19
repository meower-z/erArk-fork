# Fable-5 Supervision Record

Every prompt and verdict below is reproduced verbatim. All invocations used:

`claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence "<prompt>"`

The first scope invocation used the same prompt as the successful scope adjudication below but hit the local 60-second process timeout before producing a verdict; the successful retry is recorded. The identical prompt is reproduced once.

## Scope adjudication

### Prompt

`````text
/investigate-game-bug

# Authority and task

Act as the architecture and scope adjudicator for an erArk OpenSpec proposal. Do not write implementation code or PR prose. Decide the smallest upstream-reviewable change boundary that faithfully captures the player's accepted intent below.

Apply these local project rules:
- Treat observed output as evidence, not automatically as the bug definition.
- A proposal may merge symptoms only when they share the same behavioral contract, logical owner, and lifecycle. Otherwise split them.
- Name the violated rule, logical owner, current interface, sibling and inverse cases, alternatives, causal radius, and non-goals.
- Prefer a deep module: a small interface at a clean seam, with behavior and tests concentrated behind it. Do not introduce a hypothetical abstraction merely to unify unrelated code.
- The future PR must be a narrow, independently testable behavioral contract. Its Chinese title/body will later explain player-visible problem, confirmed cause, and fix in that order; private worktree/OpenSpec/agent narrative and local-only proof cannot be PR claims.
- Every behavior-changing PR will later need a representative real-Tk before/after player flow. That evidence requirement affects reviewability, but this task does not create evidence.
- Resolve scope before edits. Return PASS only if your recommendation makes the scope implementable without silently deciding unresolved gameplay policy.

# Verified current behavior and owners

1. Script/Design/update.py game_update_flow(add_time) advances cache.game_time once, then calls character_behavior.init_character_behavior(). Nested update calls are guarded by cache.game_update_flow_running.
2. character_behavior.init_character_behavior() creates cache.over_behavior_character = set(), settles the player first, then loops through all NPCs until complete. Ordinary idle NPC action generation is reached through handle_npc_ai.find_character_target(); group-sex type-1/type-2 generation is reached earlier through handle_npc_ai_in_h.judge_character_h_obscenity_unconscious() and npc_ai_in_group_sex().
3. Script/Design/settle_behavior.py appends "\n\n {add_time}分钟过去了\n" to every non-empty actor settlement panel. Therefore one physical player click can show that line once per actor even though global time advanced only once. The preview string "该行动将持续{add_time}分钟" is a separate exchange/preview path.
4. Script/Design/second_behavior.py orgasm_settle() is the authoritative actual-release path after time-stop accumulation and successful edging have already continued without releasing. A single call may settle multiple body-part orgasms and a plural orgasm.
5. Existing scheduler architecture notes already prefer a stable PlayerActionWindow with per-actor claims for repeated group masturbation intent, but the broader 60-minute action frequency/duration, unavailable-target retry, and general nested scheduling rules remain unresolved.
6. A prior regression established that converting an idle group-H NPC to WAIT can skip judge_character_status() and second-stage settlement. Any block must preserve passive/realtime/persistent settlement and completion.

# Player-confirmed intent

There are two user-visible problems from one click:
A. Display: actor panels misleadingly repeat "5分钟过去了". Actor panels should show actor changes only. The outermost physical player-action settlement window should show exactly one actual elapsed-time line after all player/NPC settlement. Nested settlement must not emit another line; time-stop rollback must not claim elapsed time when none remains. Action-duration preview remains separate.
B. Same-click active orgasm chain: no persistent 10-minute recovery. During one top-level physical player click, keep a non-serialized local set of NPC IDs that actually released an orgasm. After an NPC's first actual release in that window, prevent only further autonomous action generation for that NPC for the remainder of the same window. Passive settlement continues: the NPC stays in the group/template, can receive stimulation, pleasure can rise, passive orgasms may still happen, and the same release transaction's multiple body parts settle normally. The player is unaffected. Successful edging and time-stop accumulation do not enter the set. A nested update caused by the same physical click reuses the outer set; only the outermost finally clears it. A blocked NPC must still complete the scheduler tail and enter over_behavior_character. The next physical player click starts with an empty set; nothing is saved.
The player explicitly accepts the consequence that repeated one-minute clicks can permit activity each click, while one sixty-minute click can leave the NPC passive after the first release for the rest of that click. This is per-click active-chain gating, not physiological recovery.

# Explicit non-goal

Do not solve the general endpoint/backfill causality of the scheduler or redesign the game to advance minute by minute. This proposal should prevent repeated autonomous post-release chains within one player click and correct the elapsed-time presentation ownership only.

# Alternatives to adjudicate neutrally

A. One OpenSpec change centered on an explicit outermost player-action settlement window, with two separately specified capabilities: single elapsed-time presentation and per-window NPC active-chain gating.
B. Two independent OpenSpec changes because presentation ownership and NPC generation policy have different logical owners/failure mechanisms, even if they share an outer lifecycle.
C. Scope only the active-chain rule now and leave the display fix for a later change.

# Required output

Return:
1. VERDICT: PASS, REVISE, or BLOCKED.
2. SCOPE DECISION: choose A, B, or C and explain against same-contract/same-owner/same-lifecycle criteria.
3. Recommended change name(s) and one-sentence player-facing goal per change.
4. The logical owner and smallest interface/seam; say whether an explicit PlayerActionWindow module/context is earned or would be over-engineering.
5. Normative requirements and scenario list, including nested calls, exceptions, inverse cases, and completion/no-hang.
6. Implementation task slices and the tests/evidence each slice must eventually expose to an upstream reviewer.
7. Non-goals and unresolved questions that must not be silently decided.
8. Any wording corrections: especially whether "recovery", "stun", "one minute at a time", or "deduplicate display strings" are misleading.

Keep the answer concrete enough to generate proposal.md, design.md, specs, and tasks.md without guessing.
`````

### Verdict

`````text
## VERDICT: PASS

Scope is implementable without silently deciding gameplay policy, provided the two changes below are kept separate and the flagged design points are recorded (not left implicit).

## SCOPE DECISION: B — two independent OpenSpec changes

Test against the merge criteria:

- **Same lifecycle?** Yes — both key off "outermost physical player click" (already detectable via the existing `cache.game_update_flow_running` guard in `update.py`).
- **Same logical owner?** No. The elapsed-time line is owned by player-action settlement *presentation* (`game_update_flow` / `settle_behavior` panel assembly). The orgasm gate is owned by NPC autonomous-action *admission* (`handle_npc_ai` / `handle_npc_ai_in_h` generation entries).
- **Same behavioral contract?** No. One is "exactly one truthful elapsed-time line per click"; the other is "no autonomous action generation after first actual release within a click." Different failure mechanisms, different tests, independently revertable.

Shared lifecycle alone doesn't merge them. Option A would bundle two unrelated review discussions into one PR; option C leaves a confirmed, cheap presentation fix stranded for no reason. Reject both.

Each change independently detects "outermost" from the existing nesting guard — no shared new module is required, so there is no coupling argument for A.

## Change names and player-facing goals

1. **`fix-elapsed-time-line-ownership`** — One physical click shows exactly one truthful "N分钟过去了" line after all settlement; actor panels show only that actor's changes.
2. **`add-per-click-orgasm-chain-gate`** — Within one click, an NPC that actually climaxed initiates no further autonomous actions for the rest of that click, while still receiving stimulation and settling passively.

## Logical owner and seam

**Change 1:** Owner is `game_update_flow` (the only place that actually advances `cache.game_time` once). Seam: delete the per-actor append in `settle_behavior.py`; emit one line at the end of the *outermost* `game_update_flow`, guarded by "net elapsed time > 0" (covers time-stop rollback). Preview string untouched.

**Change 2:** Two-point seam behind one transient set:
- *Lifecycle:* set created at outermost `game_update_flow` entry, cleared in `finally` only at outermost; nested calls reuse it. Non-serialized (module/cache-transient field excluded from saves).
- *Write:* `orgasm_settle()` actual-release path adds NPC id (never player), after the full release transaction (all body parts + plural orgasm) settles.
- *Read:* admission check at the autonomous generation entries — `find_character_target()` and the group-sex type-1/type-2 generation in `handle_npc_ai_in_h` — returning the safe idle fallback that still runs `judge_character_status()`, second-stage settlement, and reaches `over_behavior_character`.

**Is an explicit PlayerActionWindow module earned? No — over-engineering now.** Each change needs one flag or one set with `try/finally` at an existing function that already marks the boundary. Extract a named PlayerActionWindow context only when a third consumer arrives (the deferred scheduler work is the obvious candidate). Record this as a deliberate deferral in design.md.

## Normative requirements and scenarios

**Change 1:**
- R1: `settle_behavior` never appends the elapsed line to actor panels.
- R2: Outermost update emits exactly one line, after all player+NPC settlement, showing actual advanced time.
- R3: Nested updates emit nothing.
- R4: Zero net elapsed time (full time-stop rollback) → zero lines.
- R5: "该行动将持续…" preview path unchanged.

Scenarios: one click with ≥2 NPC settlement panels → one trailing line; nested update within the click → still one; time-stop full rollback → none; partial rollback → truthful amount; empty panels unaffected.

**Change 2:**
- R1: Set lives exactly one outermost update; `finally`-cleared even on exception; nested reuse; next click starts empty; never serialized.
- R2: Player never added, never gated.
- R3: Successful edging and time-stop accumulation do not register.
- R4: The registering release transaction itself settles fully (multi-part + plural) before the gate has any effect.
- R5: Gate blocks only autonomous generation; passive settlement, stimulation receipt, pleasure rise, and passive orgasms continue; NPC stays in group/template.
- R6: Gated NPC still runs `judge_character_status()` and second-stage settlement and enters `over_behavior_character` — explicit regression guard against the known WAIT-conversion skip (fact 6). No loop hang.

Scenarios: 60-min click, release at minute 5 → passive thereafter, loop completes; two NPCs, one releases → only that one gated; edging → ungated; accumulation → release only after actual release; exception mid-update → set cleared; player orgasm → no effect; save/load → no trace.

## Task slices and reviewer-facing evidence

**Change 1:**
1. Remove per-actor append; add outermost emission with zero-elapsed guard. *Test:* scripted settlement counting emitted lines across multi-NPC / nested / time-stop cases through the real settlement path.
2. *Evidence:* one representative Tk before/after — a click producing multiple NPC panels: repeated lines before, single trailing line after.

**Change 2:**
1. Set lifecycle in `game_update_flow` (`try/finally`, outermost-only clear).
2. Registration in `orgasm_settle()` actual-release path (NPC-only, post-transaction).
3. Admission checks at the three generation entries, using the settlement-preserving fallback.
4. Regression test for R6 completion (the fact-6 skip).
*Tests:* real-function checks — release registers / edging doesn't / gated NPC generates nothing but completes / nested reuse / finally clears.
*Evidence:* one Tk before/after 60-min click flow: repeated post-release chains before; single release then passivity after, click completing normally.

## Non-goals and unresolved questions (do not silently decide)

- General scheduler endpoint/backfill causality, 60-minute frequency/duration policy, unavailable-target retry, minute-by-minute redesign — all out of scope, per the player.
- A generalized PlayerActionWindow abstraction — deferred, recorded.
- **One design point to record explicitly, not decide silently:** the intent says "prevent only further autonomous action generation." I read this as *all* autonomous generation for that NPC (both idle and group-sex paths), consistent with "leave the NPC passive." The exact fallback behavior ID (e.g., remain-in-template idle vs `SHARE_BLANKLY`) is an implementation choice, but it must be named in design.md with the R6 settlement guarantee — because the fact-6 regression shows the fallback choice is where this design historically breaks.

## Wording corrections

- **"recovery" — misleading, ban it.** This is per-click active-chain gating; nothing physiological, nothing persistent. Use "同一次玩家行动内的主动行为限制" framing.
- **"stun" — wrong.** The NPC continues passive settlement; a stun implies frozen state. Do not use.
- **"one minute at a time" — not a mechanic.** It's an accepted consequence of the design, stated once as a trade-off in design.md; never present it as intended behavior or a workaround recommendation.
- **"deduplicate display strings" — misleading.** The fix is ownership relocation (one authoritative emission point), not string deduplication. "Dedup" would invite a wrong implementation that filters repeated identical panel text.
`````

## Orgasm-chain artifact audit

### Prompt

`````text
/investigate-game-bug

# Authority and scope

Audit one erArk OpenSpec change as a clean architecture/spec reviewer. Do not edit files, write implementation code, or draft PR prose. Review every supplied artifact, not just proposal.md.

Apply these project rules:
- A symptom is evidence. Require one named behavioral rule, logical owner, and independently reviewable lifecycle.
- Merge only same contract/owner/lifecycle; do not absorb elapsed-time presentation or general scheduler redesign.
- Prefer a deep existing seam and a small interface. Reject persistent cooldown state, process-global identity tricks, copied scheduler loops, and speculative full PlayerActionWindow infrastructure.
- Check the authoritative release write point, all autonomous-generation read points, sibling/inverse paths, idempotence, exceptions, nesting, save behavior, causal radius, and completion/no-hang.
- The future behavior-changing PR must expose red/green automated proof and a repeatable real-Tk before/after player flow. PR prose will later be Chinese and Fable-written from PR-visible material.
- A format-valid OpenSpec is not enough. Return PASS only if implementation can proceed without silently choosing gameplay policy.

# Verified source facts

- update.game_update_flow increments cache.game_update_flow_running, allows one nested level while rejecting depth >=2, and currently resets the flag to zero in every finally rather than restoring the previous depth.
- character_behavior.init_character_behavior resets over_behavior_character, settles player, then calls NPC prechecks. Group type-1/type-2 generation can occur in handle_npc_ai_in_h before ordinary idle find_character_target.
- Ordinary H idle fallback may add an NPC to over_behavior_character and return. A prior real regression proved that forcing a group-H idle NPC to WAIT can skip judge_character_status and second-stage settlement.
- second_behavior.orgasm_settle is the actual release authority. Time-stop accumulation and successful edging continue before the actual-release body. One call can settle several body parts, plural orgasm, milk/urine derivatives, achievements, experience, and other effects.
- Existing broader architecture work has not decided general 60-minute behavior frequency, unavailable-target retry, or endpoint/backfill causality.
- The player explicitly chose: per physical click, nonserialized NPC-only active-generation gating after first actual release; passive stimulation and passive orgasms continue; next click resets immediately; repeated 1-minute versus one 60-minute clicks may differ.
- A separate change owns the elapsed-time line. This change must not absorb presentation.

# Audit questions

1. Are the contract, logical owner, and smallest interface coherent and narrow?
2. Does the proposed transient lifecycle work under the verified broken nesting-depth reset, including multiple sequential nested calls and exceptions?
3. Is "after the complete release transaction" precise enough to avoid truncating multi-part/plural/derived effects, including early-return failed-edge release and time-stop release?
4. Do all ordinary and group autonomous-generation entrances read the gate before mutation while preserving passive settlement and over_behavior_character completion?
5. Are passive orgasm, two-NPC isolation, player inverse, save/load, next-click reset, 1-min/60-min asymmetry, and no-hang fully specified?
6. Are tasks red-capable and future PR/Tk evidence reviewable under the strict project rules?
7. Does this change have an undeclared dependency on repairing update depth, the elapsed-time change, or a broader PlayerActionWindow abstraction?

# Required verdict

Return exactly one leading verdict: PASS, REVISE, or BLOCKED.
Then provide:
- contract / owner / seam;
- findings by severity with exact artifact and heading;
- missing scenarios and inverse cases;
- dependency and overlap verdict relative to the elapsed-time change;
- task/evidence audit;
- concise readiness reason.

For REVISE, prescribe exact document edits. For BLOCKED, name the missing player/source decision. Do not propose implementation beyond the smallest authorized seam.

# Artifacts


===== proposal.md =====
## Why

一次较长的玩家行动结算中，NPC 实际高潮后仍可能立即生成下一轮主动行为，从而在同一次点击内反复主动行动并再次高潮。玩家确认需要的是仅限本次点击的主动行为链阻断，而不是可保存、按游戏分钟恢复的眩晕或生理冷却。

## What Changes

- 在一次最外层玩家点击期间，临时记录已经实际高潮释放的 NPC。
- NPC 在本次点击首次实际释放后，不再生成新的自主行为；下一次玩家点击重新允许其自主行动。
- 被阻断的 NPC 仍留在原群交关系和模板中，继续受到玩家或其他角色刺激，并完成被动数值、持续状态、二段效果与高潮结算。
- 成功寸止和时停蓄积不计为实际释放；玩家不受该规则影响；一次释放事务内的多部位和多重绝顶完整结算。
- 嵌套更新复用最外层点击的临时记录，异常退出也清理记录；该状态不写入存档。

## Capabilities

### New Capabilities

- `per-click-orgasm-chain-gate`: 定义 NPC 实际释放后在同一次玩家点击内的自主行为准入、被动结算和临时状态生命周期。

### Modified Capabilities

无。

## Impact

- 影响最外层游戏更新生命周期、NPC 普通与群交主动行为生成入口，以及实际高潮释放的权威结算路径。
- 不改变高潮数值公式、群交模板成员关系、存档格式或通用 NPC 分钟调度策略。
- 后续实现需要覆盖普通与群交生成入口、被动结算、循环完成、嵌套更新、异常清理和真实 Tk 前后对比证据。

===== design.md =====
## Context

一次玩家行动先推进游戏时钟，再在同一结算调用中处理玩家和所有 NPC。NPC 可在普通 AI 入口或群交 type-1/type-2 入口生成新行为；实际高潮释放则由 `orgasm_settle()` 在寸止成功和时停蓄积分支之后统一结算。当前缺少一个仅限本次玩家点击的事实来阻止“已经实际释放的 NPC 又主动发起下一轮行为”，因此一次长行动可能形成连续主动行为和高潮链。

玩家拒绝持久的十分钟恢复或眩晕，确认接受按点击而非按游戏分钟划分的规则：一次长点击中首次释放后保持被动，下一次点击立即重新允许主动行为。该规则不处理调度器把终点状态回填到整段时间的一般因果问题。

## Goals / Non-Goals

**Goals:**

- 用一次最外层玩家点击内的临时事实阻止已实际释放 NPC 的后续自主行为生成。
- 只在权威实际释放事务完整结算后登记 NPC，不截断同批多部位、多重绝顶或派生效果。
- 保留被阻断 NPC 的被动刺激、数值、持续状态、二段效果、被动高潮和循环完成。
- 让普通 AI 与群交 type-1/type-2 生成入口遵守同一准入结果，并覆盖嵌套调用和异常清理。

**Non-Goals:**

- 不增加十分钟恢复、眩晕、疲劳或任何按游戏时间保存的角色状态。
- 不限制玩家行动，也不阻止 NPC 接受刺激或发生后续被动高潮。
- 不改变高潮阈值、次数、寸止概率、时停蓄积、多部位事务或群交模板成员关系。
- 不决定一小时行动应拆成多少次 NPC 行为、目标不可用时是否重试或调度器的一般终点回填规则。
- 不建立通用 `PlayerActionWindow` 模块；当前用现有最外层更新生命周期和一个窄接口即可。

## Decisions

### 1. 最外层更新拥有非持久的已释放 NPC 集合

最外层游戏更新开始时创建空集合，嵌套更新复用同一集合，最外层 `finally` 清理。集合不属于角色数据或存档数据，异常、下一次玩家点击和读取存档后都不得留下成员。

对其他模块只暴露两个窄操作：登记某 NPC 在当前点击已经实际释放，以及查询某 NPC 是否应被拒绝新的自主行为。调用者不需要知道集合生命周期或存储方式。这个接口把跨模块状态集中在现有更新所有者内，但不引入完整窗口对象、ID、起止时间或声明协议。

备选方案“角色保存十分钟恢复状态”被拒绝，因为它改变跨点击玩法和存档语义。备选方案“用 `over_behavior_character` 集合对象身份充当窗口 ID”被拒绝，因为该集合是完成追踪，可能在嵌套流程重建，不能同时承担玩家点击身份。备选方案“现在建立通用 `PlayerActionWindow`”被拒绝，因为两个操作和一个集合尚不足以证明额外模块接口的价值。

### 2. 完整实际释放事务之后才登记

权威写入点位于 `orgasm_settle()` 的实际释放路径，且在当前调用的全部部位、复数绝顶和派生结算已经形成之后。只登记 NPC。成功寸止仅累积寸止账本，时停路径仅累积待释放计数，二者都不登记；寸止失败或时停解放只有在真正进入普通释放结算后才登记。

登记按角色幂等：同一点击内的后续被动高潮可以继续完整结算，再次登记不改变结果。该集合只限制未来主动行为准入，不作为高潮事务内部的提前退出条件。

### 3. 在所有自主生成入口读取同一准入事实

普通空闲 AI 和群交 type-1/type-2 AI 在生成或选择新行为之前查询准入。命中后不得创建新的目标、自慰意图、模板占位或其他主动行为，但也不得把角色转为会绕过正常结算的 `WAIT`。

被阻断角色保持一个能继续进入现有 `judge_character_status()` 的空闲/群交被动路径，然后继续 realtime、persistent-state、interrupt、time-over、talent 和 completion 尾部。具体行为常量由实现依据可失败回归选择，但必须满足：不生成主动行为、不移出群交关系、被动结算继续、最终加入 `over_behavior_character`。

### 4. 按点击划分是明确的玩法上限

一次六十分钟点击中，NPC 首次实际释放后在该点击剩余结算内保持被动；玩家随后进行新的一分钟点击时，集合已重建，NPC 可以再次主动。这是玩家确认的行为，不表述为生理恢复或推荐玩家拆分操作。

## Risks / Trade-offs

- **[阻断位置过晚]** → 普通和群交两个生成入口分别建立可失败回归，并断言命中时没有生成目标、自慰意图或模板写入。
- **[错误使用 WAIT 跳过二段结算]** → 增加已知 sibling 回归，断言被阻断 NPC 仍调用状态/二段结算并完成，且调度循环不挂起。
- **[登记过早截断同一高潮批次]** → 测试同一调用的多部位与多重绝顶全部结算后才影响下一次行为准入。
- **[临时集合泄漏到下一点击或异常路径]** → 测试正常结束、嵌套复用和异常 `finally` 清理；不把集合放入角色或可序列化缓存结构。
- **[现有嵌套深度标志不足以表达物理点击]** → 先锁定真实嵌套调用的当前行为；若无法稳定识别最外层，暂停重新审计，不在本 change 中顺带改写通用调度器。
- **[一分钟与六十分钟点击结果不同]** → 在规格和真实 Tk 证据中明确这是按点击规则的已接受取舍，不把它包装成按分钟公平性。

## Migration Plan

1. 建立可失败的真实函数回归：实际释放登记；成功寸止和时停蓄积不登记；普通与群交入口均阻断生成；被动结算和完成继续。
2. 在最外层更新所有者中加入非持久集合生命周期和窄查询/登记接口，覆盖嵌套与异常清理。
3. 在实际释放事务结束处登记 NPC，并保持玩家、寸止与时停分支不登记。
4. 在普通 AI 与群交 type-1/type-2 生成入口接入准入查询，使用结算安全的被动路径。
5. 运行聚焦、群交、高潮、嵌套和存档 sibling 回归，并完成真实 Tk 的长行动前后对比。

回退时先移除所有读取点，再移除写入和生命周期，避免保留无消费者的临时状态。没有存档迁移。

## Open Questions

无。普通与群交入口命中后的具体空闲行为表示可由实现选择，但必须由“被动结算继续且循环完成”的规格和回归约束；若现有行为模型没有满足这些条件的表示，应暂停并重新讨论 scope，而不是引入持久恢复状态。

===== specs/per-click-orgasm-chain-gate/spec.md =====
## ADDED Requirements

### Requirement: 每次最外层玩家点击独立记录已实际释放的 NPC
系统 SHALL 为每次最外层玩家点击创建独立、非持久的已释放 NPC 记录；同一点击内的嵌套更新 MUST 复用该记录，最外层正常或异常结束后 MUST 清理记录，下一次点击 MUST 从空记录开始。

#### Scenario: 嵌套更新发生在同一次点击内
- **WHEN** NPC 已在外层玩家点击中实际释放，随后结算触发嵌套游戏更新
- **THEN** 嵌套更新继续把该 NPC 视为本次点击已释放

#### Scenario: 下一次玩家点击开始
- **WHEN** 已有 NPC 在上一次玩家点击中实际释放且该点击已经结束
- **THEN** 新点击的记录为空
- **AND** 该 NPC 可以重新通过自主行为准入

#### Scenario: 结算过程异常退出
- **WHEN** 最外层玩家点击在结算期间抛出异常
- **THEN** 本次点击的临时记录仍被清理
- **AND** 后续点击不继承本次记录

#### Scenario: 保存和读取游戏
- **WHEN** 游戏在玩家点击之间保存并重新读取
- **THEN** 存档中不存在已释放 NPC 的点击内记录

### Requirement: 只有 NPC 的实际高潮释放登记主动行为阻断
系统 SHALL 只在 NPC 的实际高潮释放事务完整结算后登记该 NPC；玩家高潮、成功寸止和时停中的高潮蓄积 SHALL NOT 登记。

#### Scenario: NPC 完成多部位实际释放
- **WHEN** NPC 在同一个高潮事务中发生多个部位高潮并触发多重绝顶及派生效果
- **THEN** 系统先完整结算本事务的全部部位、多重绝顶和派生效果
- **AND** 随后幂等登记该 NPC 为本次点击已实际释放

#### Scenario: NPC 成功寸止
- **WHEN** NPC 的高潮跨级被成功寸止并只写入寸止累计
- **THEN** 该 NPC 不因本次跨级被登记
- **AND** 仍可在本次点击生成后续自主行为

#### Scenario: 时停中只累计高潮
- **WHEN** NPC 的高潮仅计入时停待释放计数而未实际释放
- **THEN** 该 NPC 不被登记

#### Scenario: 玩家实际高潮
- **WHEN** 玩家在本次点击实际高潮
- **THEN** 玩家不会被加入 NPC 已释放记录
- **AND** 该记录不限制玩家行为

### Requirement: 已实际释放 NPC 不再生成本次点击的自主行为
系统 MUST 在普通空闲 AI 和群交 type-1/type-2 AI 的所有自主行为生成入口拒绝已登记 NPC 的新行为，并 MUST NOT 因该拒绝创建新目标、自慰意图、群交模板占位或其他主动行为。

#### Scenario: 普通空闲 AI 尝试生成行为
- **WHEN** 已登记 NPC 在同一次点击内到达普通自主行为生成入口
- **THEN** 系统拒绝该 NPC 的新自主行为

#### Scenario: 群交 NPC 尝试生成行为
- **WHEN** 已登记 NPC 在同一次点击内到达群交 type-1 或 type-2 自主行为生成入口
- **THEN** 系统拒绝新的群交主动行为、自慰意图和模板写入
- **AND** NPC 仍保留现有群交参与关系和模板位置

#### Scenario: 两名 NPC 中只有一名已经释放
- **WHEN** NPC A 已登记而 NPC B 尚未实际释放
- **THEN** 本次点击只拒绝 NPC A 的自主行为生成
- **AND** NPC B 继续按既有规则生成行为

### Requirement: 主动行为阻断不妨碍被动结算和循环完成
已登记 NPC SHALL 继续接受玩家或其他角色的刺激，并 SHALL 继续运行状态、二段效果、实时变化、持续状态、中断、行为结束、素质与完成结算；系统 MUST 使该 NPC 最终进入本次调度的完成集合且不得造成循环挂起。

#### Scenario: 被阻断 NPC 继续受到群交刺激
- **WHEN** 已登记 NPC 在本次点击剩余结算中被玩家或其他角色继续刺激并增加身体或心理快感
- **THEN** 对应数值与二段效果继续结算
- **AND** NPC 不因主动行为阻断被移出群交关系或模板

#### Scenario: 被动刺激再次触发高潮
- **WHEN** 已登记 NPC 的被动快感继续上升并再次跨过高潮阈值
- **THEN** 后续被动高潮仍完整结算
- **AND** 幂等登记不恢复或新增该 NPC 的主动行为

#### Scenario: 被阻断 NPC 完成本次调度
- **WHEN** 已登记 NPC 没有新的自主行为可生成
- **THEN** 系统仍执行其正常结算尾部并把该 NPC 加入完成集合
- **AND** 玩家点击能够正常结束

### Requirement: 主动行为阻断按玩家点击而非游戏分钟恢复
系统 SHALL 把规则限定在一次最外层玩家点击内，不建立按游戏分钟倒计时的恢复状态。

#### Scenario: 一次长点击中首次释放
- **WHEN** NPC 在一次六十分钟玩家点击的中途实际释放
- **THEN** 该 NPC 在这次点击剩余结算内不再生成自主行为

#### Scenario: 长点击结束后的新短点击
- **WHEN** 上述六十分钟点击已经结束且玩家开始新的一分钟点击
- **THEN** NPC 可在新点击中重新生成自主行为

===== tasks.md =====
## 1. 可失败回归与权威事件

- [ ] 1.1 用真实高潮结算函数建立回归，证明 NPC 实际释放后会在同一次点击再次进入普通或群交自主行为生成，并让旧实现先失败。
- [ ] 1.2 分别覆盖实际释放、同事务多部位与多重绝顶、成功寸止、时停蓄积和玩家高潮，锁定唯一登记条件与登记时机。
- [ ] 1.3 建立普通 AI、群交 type-1/type-2、两名 NPC 隔离、被动再次高潮和完成集合回归，特别证明不能用跳过 `judge_character_status()` 的 `WAIT` 路径阻断。
- [ ] 1.4 建立嵌套更新、异常退出、下一点击重置和保存/读取回归；若现有更新深度无法稳定表示最外层物理点击，暂停并回到设计审计。

## 2. 点击内临时状态

- [ ] 2.1 在现有最外层游戏更新所有者内实现非持久的已释放 NPC 集合，并提供登记与准入查询两个窄操作。
- [ ] 2.2 让嵌套更新复用外层集合，最外层 `finally` 在正常与异常路径清理，并确认集合不进入角色数据、缓存序列化或存档。

## 3. 实际释放登记

- [ ] 3.1 在权威高潮实际释放路径的完整事务结束后幂等登记 NPC，保证同批全部部位、多重绝顶和派生效果已形成。
- [ ] 3.2 保持玩家、成功寸止和时停蓄积分支不登记，并覆盖寸止失败或时停解放只有在真正释放后才登记。

## 4. 自主行为准入与被动完成

- [ ] 4.1 在普通空闲 AI 生成入口拒绝已登记 NPC 的新目标和新行为，同时让其继续正常状态与调度尾部结算。
- [ ] 4.2 在群交 type-1/type-2 生成入口拒绝新自慰意图、模板占位和其他主动行为，不移除现有参与关系或模板位置。
- [ ] 4.3 验证被阻断 NPC 仍接受刺激、累计身体与心理快感、结算二段效果和被动高潮，并最终进入 `over_behavior_character`，无循环挂起。

## 5. 自动化验证

- [ ] 5.1 运行聚焦真实函数回归、相关群交与高潮测试、嵌套/异常测试、存档 sibling 回归和 Python 语法检查。
- [ ] 5.2 运行相邻的寸止、时停释放、多部位绝顶、群交模板和普通 NPC 行为测试，确认数值公式、成员关系与非目标调度语义未改变。
- [ ] 5.3 明确验证一次六十分钟点击中首次释放后保持被动，而下一次新点击立即重新允许主动行为。

## 6. 上游可见证据与审计

- [ ] 6.1 由本地视觉执行者在真实 Tk、同一存档和同一路线下捕获长行动的修复前后完整帧序列，证明同次点击的释放后主动链被阻断且结算正常结束。
- [ ] 6.2 让 Fable-5 依据本地项目写作规则生成中文 PR 标题和正文，只使用拟提交 diff、已提交测试和准备公开的 Tk 证据支持声明。
- [ ] 6.3 对完整拟提交 diff、PR 文本和证据执行 fresh-context PR artifact 审计，达到 `local-review-ready` 后再请求任何提交、推送或发布授权。

`````

### Verdict

`````text
**REVISE**

## Contract / owner / seam

- **Contract:** after an NPC's first *actual* orgasm release within one outermost player click, that NPC generates no further autonomous behavior for the remainder of that click; passive stimulation, passive orgasms, second-stage settlement, and loop completion continue; the record is transient, nested-shared, exception-safe, non-serialized, and reset at the next click.
- **Owner:** the existing outermost game-update lifecycle (`update.game_update_flow`) owns the set; `second_behavior.orgasm_settle`'s actual-release tail is the sole write point; ordinary idle AI and group type-1/type-2 entrances are the read points.
- **Seam:** two narrow operations (register / query-admission). Correctly rejects persistent cooldowns, `over_behavior_character` identity tricks, and a speculative `PlayerActionWindow`. Coherent and narrow.

## Findings by severity

**HIGH — design.md · Risks "[现有嵌套深度标志不足以表达物理点击]" and tasks.md 1.4.** The change's entire lifecycle guarantee ("最外层创建、嵌套复用、最外层 finally 清理") hangs on identifying the outermost call, but a **verified fact** already establishes that `game_update_flow`'s `finally` resets the depth flag to zero instead of restoring the prior depth. Consequence: after the *first* nested update returns, the flag reads zero while still inside the outer click; a *second sequential* nested call is misclassified as outermost — it would recreate an empty set (wiping registrations mid-click) and its `finally` would clear the record before the click ends. The design treats this as a contingent risk ("若无法稳定识别最外层，暂停重新审计"), but the contingency has already fired: the flag *is* known unable to express the outermost click today. Deferring this to implementation means implementation would silently choose lifecycle policy — the exact thing that forbids PASS. This is currently an **undeclared dependency** (audit question 7: yes, on update-depth repair).

**MEDIUM — specs/per-click-orgasm-chain-gate/spec.md · "只有 NPC 的实际高潮释放登记主动行为阻断".** The negative scenarios (成功寸止, 时停蓄积) are present, but the two positive inverse scenarios named in design.md §2 and tasks 3.2 are missing from the spec: **寸止失败后进入实际释放 → 登记** and **时停解放进入实际释放结算 → 登记**. Since edging and time-stop accumulation early-return *before* the actual-release body, these are the two paths most likely to be wired wrong, and the spec — the reviewable contract — is silent on them.

**MEDIUM — spec.md · "每次最外层玩家点击独立记录…" · nested scenario.** The nested scenario covers one nested update. The known failure mode (per the HIGH finding) is *multiple sequential* nested updates in one click. Add a scenario asserting the record survives a nested update's completion and is still honored by a subsequent nested update in the same click, and that an exception inside a *nested* update does not clear the outer record.

**LOW — design.md §3 vs. verified fact "ordinary H idle fallback may add an NPC to over_behavior_character and return".** Design bans the `WAIT` bypass but does not name this existing early-return fallback as either an acceptable passive path or a forbidden one. The regression constraints ("被动结算继续、最终加入完成集合") probably bound it, but one sentence classifying that fallback would close the ambiguity.

## Missing scenarios / inverse cases

1. 寸止失败 → 实际释放 → 登记 (spec).
2. 时停解放 → 实际释放结算 → 登记 (spec).
3. 同一点击内两次先后嵌套更新，记录不被第二次嵌套重建或清理 (spec).
4. 嵌套更新内部异常：外层记录保留至外层结束 (spec — current exception scenario only covers the outermost throw).

Everything else asked in question 5 is specified: passive re-orgasm ✓, two-NPC isolation ✓, player inverse ✓, save/load ✓, next-click reset ✓, 1-min/60-min asymmetry as an accepted per-click trade-off ✓, completion/no-hang ✓.

## Dependency and overlap verdict vs. elapsed-time change

No overlap. Proposal/design consistently exclude elapsed-time presentation and general scheduler policy (60-minute splitting, retry, endpoint backfill). Boundary is clean. The only real dependency problem is the update-depth one above, which is internal to this change's owner, not to the elapsed-time change.

## Task / evidence audit

Tasks are red-capable and ordered correctly: 1.1 explicitly requires the old implementation to fail first; 1.3 encodes the known WAIT sibling regression; 5.x covers causal radius (edging, time-stop, multi-part, group templates, non-target scheduling); 6.1 real-Tk before/after under same save/route; 6.2 Fable-written Chinese PR prose from PR-visible material only; 6.3 fresh-context artifact audit before any outward action. Only defect: 1.4's "若…暂停并回到设计审计" is a conditional that verified facts have already resolved — it must become a concrete task, not an escape hatch.

## Prescribed edits

1. **design.md — replace the risk row "[现有嵌套深度标志不足以表达物理点击]" with a Decision.** State the verified fact (every `finally` zeroes the flag instead of restoring prior depth) and decide now: the outermost-click identity requires the depth flag's `finally` to save-and-restore the previous depth. Scope this as a minimal lifecycle repair *at the same owner this change already modifies* — it is not scheduler redesign, and one nested level remains the allowed maximum. If instead the author wants a different outermost signal, name it explicitly; do not leave the choice to implementation.
2. **proposal.md — Impact:** add one line declaring the depth save/restore repair inside `game_update_flow` as in-scope, so the dependency is declared rather than silent.
3. **spec.md:** add the four scenarios listed under "Missing scenarios" (two registration inverses under the second requirement; sequential-nested and nested-exception under the first requirement).
4. **tasks.md 1.4:** replace the pause clause with concrete regressions — two sequential nested updates preserve and honor the record; nested-update exception preserves the outer record; outermost exception clears it — plus a red-first test that the current zero-reset misclassifies a second nested call (this is the red proof for edit 1).
5. **design.md §3 (optional but cheap):** one sentence classifying the existing ordinary-H idle early-return fallback as acceptable-passive or forbidden.

## Readiness reason

The contract, owner, write point, read points, and evidence plan are all sound and narrow, and the elapsed-time boundary is clean. But the transient lifecycle — the core of the change — is specified against an outermost-click identity that verified facts show does not exist today, and the documents defer that resolution to implementation. Implementation cannot proceed without silently choosing lifecycle policy, so this cannot PASS until the depth-identity decision and the four inverse/nesting scenarios are written into the documents. No missing player decision — the player's per-click choice fully determines the needed edits — so REVISE, not BLOCKED.
`````

## Final dependency reconciliation

### Prompt

`````text
/investigate-game-bug

# One final reconciliation follow-up

Your initial scope verdict split the work into:
1. fix-elapsed-time-line-ownership
2. add-per-click-orgasm-chain-gate

You then audited each draft. Both audits returned REVISE because the verified implementation of update.game_update_flow increments cache.game_update_flow_running but every finally sets it to zero instead of restoring the caller's prior depth. Both audit prescriptions said each change should put the same save/restore repair in scope at the same owner.

This creates a conflict with the project's strict architecture rule:
- Changes may be separate only when independently reviewable/revertable.
- Two proposed PRs should not each claim or implement the same update-depth repair.
- Shared lifecycle alone did not justify merging elapsed-time presentation and orgasm admission.
- No existing OpenSpec change/spec owns game_update_flow_running depth restoration; repository search found only the source/cache/save fields.
- The user asked for proposals for the two player-visible fixes, isolated from ongoing main work, and wants strict upstream architecture.

# Verified constraints

- Both behaviors require a stable identity for one outermost physical player click across multiple sequential nested updates and nested exceptions.
- The recursion policy currently rejects calls at depth >=2; repairing finally to restore the prior depth can preserve that policy.
- The repair has a standalone invariant: a nested game update restores its caller's depth on normal and exceptional return; only the outermost return restores zero.
- Neither player-visible change should redesign scheduler timing, minute cadence, endpoint/backfill behavior, or introduce a full PlayerActionWindow module.
- A third change is acceptable only if it is a real independently testable enabling contract, not process overhead or a speculative abstraction.
- If a dependency is chosen, artifacts must say exactly which change depends on which, and tasks must avoid duplicating implementation/testing ownership.

# Alternatives

A. Create a third narrow prerequisite OpenSpec change, e.g. fix-game-update-depth-restoration. It owns only balanced depth restoration and regression tests; both player-visible changes declare it as prerequisite and test only their own use of the stable outermost lifecycle.
B. Put depth restoration only in fix-elapsed-time-line-ownership, and make add-per-click-orgasm-chain-gate explicitly depend on that entire presentation change.
C. Put depth restoration only in add-per-click-orgasm-chain-gate, and make elapsed-time ownership depend on the gameplay change.
D. Keep two changes with duplicated depth repair language/implementation.
E. Merge the two player-visible changes after all, despite different contracts/owners.
F. Another smaller owner arrangement, but state it concretely and show why it does not duplicate lifecycle logic.

# Required final ruling

This is the single disagreement follow-up permitted by the local project skill. Give a final, unambiguous ruling; it will be treated as final.

Return:
1. FINAL VERDICT: PASS, REVISE, or BLOCKED.
2. Choose A-F.
3. Exact change names and dependency graph.
4. For each change: one contract, logical owner, files/areas affected, normative scenarios, and what it must not duplicate.
5. Exact edits required to the two existing proposals/designs/specs/tasks, plus artifacts required for any third change.
6. Explain why the result satisfies same-contract/same-owner/same-lifecycle and independent review/revert criteria.
7. State whether the original player request is now represented by two proposals plus one enabling proposal, and how to explain this without implying the user asked for extra gameplay scope.

Do not write implementation code or PR prose. Do not revisit the player's already-confirmed per-click semantics.
`````

### Verdict

`````text
FINAL VERDICT and ruling below. This is final.

## 1. FINAL VERDICT: REVISE

REVISE, not BLOCKED — the repair path is clear and requires no player input. The two existing drafts are revised as specified below; they PASS once these edits land.

## 2. Choice: A

Create a third narrow prerequisite change. B and C are rejected because each forces one player-visible change to depend on the *entirety* of an unrelated player-visible change — the audits already established the two behaviors share only the lifecycle, not a contract or owner, so an artificial whole-change dependency fails the independent-revert test (reverting the presentation change would silently break the gameplay gate, or vice versa). D duplicates implementation ownership, which both audits and the architecture rule forbid. E re-litigates a settled split. A is not process overhead: the depth-restoration invariant is a real, standalone, independently falsifiable contract (nested update restores caller's depth on normal and exceptional return; only the outermost return restores zero) with its own regression tests and its own clean revert boundary.

## 3. Change names and dependency graph

```
fix-game-update-depth-restoration        (new, no prerequisites)
        ▲                    ▲
        │                    │
fix-elapsed-time-line-ownership    add-per-click-orgasm-chain-gate
```

The two player-visible changes remain independent of each other. Each declares `fix-game-update-depth-restoration` as its sole prerequisite.

## 4. Per-change contracts

**fix-game-update-depth-restoration**
- Contract: `game_update_flow` maintains a balanced update-depth counter — every entry increments, every exit (normal or exceptional) restores the caller's prior depth; zero is restored only by the outermost exit. The existing depth≥2 rejection policy is preserved unchanged.
- Logical owner: `update.game_update_flow` (the sole writer of `cache.game_update_flow_running`).
- Files/areas: the `update` module's flow entry/exit (`try/finally` save-restore), plus regression tests for nested normal return, nested exceptional return, and outermost return.
- Normative scenarios: (a) nested update raising an exception leaves the caller at its own depth, not zero; (b) sequential nested updates within one outermost click all observe a nonzero depth until the outermost exit; (c) the depth≥2 rejection still fires at the same boundary as today.
- Must not duplicate: nothing — it must not test or specify elapsed-time presentation, orgasm admission, scheduler timing, or any consumer semantics of the stable outermost identity.

**fix-elapsed-time-line-ownership**
- Contract: unchanged from its accepted draft (elapsed-time line emitted exactly once by its presentation owner per outermost player click).
- Must not duplicate: any depth save/restore implementation, tests of nested-exception depth balance, or restatement of the depth invariant beyond citing the prerequisite. Its tests exercise only its own consumption of the stable outermost lifecycle.

**add-per-click-orgasm-chain-gate**
- Contract: unchanged from its accepted draft (per-click admission gate keyed to the outermost click identity; per-click semantics already confirmed and not revisited).
- Must not duplicate: same exclusions as above — no depth-repair implementation, tests, or spec language beyond the prerequisite declaration.

## 5. Required edits and artifacts

New change `fix-game-update-depth-restoration`: full artifact set — `proposal.md` (problem: `finally` zeroes instead of restoring prior depth; invariant as stated above), `design.md` (owner = `update.game_update_flow`; boundary = save/restore in `try/finally`; non-goals = no scheduler/cadence/endpoint changes, no PlayerActionWindow, no consumer semantics), `specs/.../spec.md` (the three normative scenarios), `tasks.md` (implementation + the three regression tests; nothing else).

Both existing changes, identically structured edits:
- `proposal.md`: add a Prerequisites/Dependencies line naming `fix-game-update-depth-restoration`; remove any language claiming the depth repair as in-scope.
- `design.md`: replace the audit-inserted depth-repair section with a one-line assumption: "assumes balanced depth restoration per fix-game-update-depth-restoration; the stable outermost click identity is consumed, not established, here." Add depth restoration to explicit non-goals.
- `specs/.../spec.md`: delete any scenario asserting depth-balance behavior itself; keep only scenarios asserting this change's behavior *given* a stable outermost identity.
- `tasks.md`: delete depth-repair implementation/test tasks; add one task verifying the prerequisite is applied before this change's own tests run.

## 6. Why this satisfies the criteria

Same-contract/same-owner/same-lifecycle: the depth invariant is one contract with one owner (`game_update_flow`) across one lifecycle (update entry/exit), so it lives in exactly one change — merging it into either consumer would put a lifecycle-owner repair inside a change whose contract is presentation or admission, violating the same-owner rule; duplicating it violates single ownership outright. Independent review/revert: each change is reviewable against one contract and revertable alone — reverting either player-visible change leaves the other and the depth repair intact; reverting the depth repair reverts one invariant with two known dependents explicitly declared, not silently entangled. The two player-visible changes remain mutually independent, matching the original scope verdict.

## 7. Representation of the original request

Yes: the player's request is now two player-visible proposals plus one enabling proposal. Explain it as: "Both requested fixes turned out to sit on top of a latent defect in the update flow — nested updates zero the depth counter instead of restoring it — which neither fix can be correctly implemented or tested without. That defect repair is split out as a small prerequisite so each requested fix stays exactly the scope you asked for." This frames the third change as a discovered defect blocking the requested work, not added gameplay scope; no new player-facing behavior is attributed to the user's request.

Preserve this verdict verbatim in all three changes' records per the skill's Records requirement.
`````

## Complete package audit

### Prompt

`````text
/investigate-game-bug

# Final compliance audit

Audit the complete three-change OpenSpec package below after the prescribed revisions. This is a compliance verification of the final reconciliation ruling, not an invitation to revisit the player's confirmed semantics or merge the two player-visible changes.

Do not edit files, write code, or draft PR prose. Review every artifact in all three changes.

# Binding architecture ruling

- fix-game-update-depth-restoration is the sole owner of balanced game-update depth restoration. It has no prerequisite and must preserve the current depth>=2 rejection policy.
- fix-elapsed-time-line-ownership and add-per-click-orgasm-chain-gate are independent consumers. Each depends only on fix-game-update-depth-restoration and must not implement or test the depth invariant itself.
- The two consumer changes remain independent because presentation and NPC autonomous-action admission have different contracts and owners.
- No full PlayerActionWindow, minute-by-minute scheduler, endpoint/backfill redesign, persistent cooldown, or PR-facing worktree narrative is allowed.

# Previously required corrections

Verify that:
1. The depth change contains the normal nested, nested exception, sequential nested, outermost-zero, and unchanged depth>=2 scenarios, with tasks limited to that invariant.
2. Elapsed-time artifacts declare the prerequisite, remove conditional depth repair, cover multi-actor, no panels, nested consumption, zero/partial rollback, cross-midnight ordering, post-exception next click, Tk/Web single occurrence, and preview inverse.
3. Orgasm-gate artifacts declare the prerequisite, remove conditional depth repair, cover sequential nested reuse, nested exception retention, outer exception cleanup, next-click reset, save inverse, actual release after full transaction, failed-edge release, time-stop release, successful edge/time-stop accumulation negatives, player inverse, ordinary and group read points, two-NPC isolation, passive repeat orgasm, completion/no-hang, and 1-minute/60-minute trade-off.
4. Neither consumer duplicates depth implementation/tests; each only verifies its own behavior given the prerequisite.
5. Tasks are red-capable, ordered, narrow, and the player-visible changes include real-Tk, Fable-written Chinese PR prose, PR-visible evidence, and fresh-context artifact review gates.
6. The enabling depth change has no standalone player-visible claim. Decide whether its automated invariant proof is sufficient under the local rule requiring real-Tk evidence for every behavior-changing candidate, or whether the proposal must record a publication blocker/combined-evidence requirement. Base this only on whether the proposed diff itself has an honestly visible behavior; do not invent synthetic Tk evidence.

# Verdict format

Lead with exactly PASS, REVISE, or BLOCKED.

PASS only if:
- every change has one contract and owner;
- the dependency graph is explicit and nonduplicative;
- the three changes are independently reviewable/revertable according to the final ruling;
- all prior actionable findings are resolved;
- implementation can begin without guessing;
- future evidence tasks do not promise dishonest or non-PR-visible proof.

If not PASS, list exact file/heading edits. Then report:
- per-change contract/owner/seam verdict;
- dependency and duplication audit;
- scenarios and inverse audit;
- task/red-proof audit;
- strict PR/Tk evidence classification for each change;
- final readiness sentence.

# Artifacts


######## CHANGE fix-game-update-depth-restoration ########

===== fix-game-update-depth-restoration/design.md =====
## Context

`update.game_update_flow()` 是 `cache.game_update_flow_running` 的唯一写入者。入口在深度小于 2 时递增，退出时却无条件写零；因此嵌套更新返回后，尚未结束的外层调用失去了自己的深度，随后同一外层调用中的另一次嵌套更新会被误识别为最外层。

这个缺陷有独立于任何消费者的生命周期不变量，也同时阻塞时间提示唯一所有权和每点击高潮主动链阻断。它必须由一个窄前置 change 单独修复，两个消费者只依赖稳定深度，不重复拥有修复。

## Goals / Non-Goals

**Goals:**

- 每次获准进入的游戏更新在正常或异常退出时恢复调用者进入前的深度。
- 只有最外层更新退出后深度恢复为零。
- 同一外层调用中的多次先后嵌套更新都能观察到调用者仍处于外层更新中。
- 保持现有深度达到 2 时拒绝继续递归的策略。

**Non-Goals:**

- 不显示或修改“分钟过去了”等文本。
- 不记录高潮、限制 NPC 行为或定义任何消费者的玩家点击语义。
- 不改变游戏时间推进、角色结算顺序、NPC 行为频率、嵌套调用来源或递归上限。
- 不引入 `PlayerActionWindow`、窗口 ID、每角色声明或新的持久状态。

## Decisions

### 1. 深度写入者成对恢复进入前的值

每次获准进入 `game_update_flow` 时保存调用者深度，再递增为当前深度；`finally` 恢复保存值，而不是写死为零。这样正常和异常路径使用同一所有者、同一恢复规则，且最外层调用保存值本来就是零。

备选方案“只在嵌套返回时减一”可以得到相同结果，但保存并恢复进入值更直接地表达调用者所有权，也避免未来入口逻辑增加早退后产生不对称。备选方案“让每个消费者各自维护最外层布尔值”被拒绝，因为会复制生命周期逻辑并使消费者之间产生不同的物理点击身份。

### 2. 递归准入策略保持原样

深度达到 2 的调用仍在递增和 `try/finally` 之前直接返回。本变更只保证已获准调用的进入/退出成对，不改变允许的一层嵌套、不补做被拒绝调用，也不解释嵌套调用的 gameplay 语义。

## Risks / Trade-offs

- **[测试只覆盖一次嵌套会漏掉归零缺陷]** → 回归必须在同一外层调用中执行两次先后嵌套，并在两次之间观察深度仍属于外层。
- **[异常测试在错误层级断言]** → 分别覆盖嵌套异常由外层捕获后恢复外层深度，以及最外层异常退出后恢复零。
- **[消费者行为混入前置修复]** → 测试只断言深度和原有 depth≥2 拒绝边界，不断言显示、高潮或 NPC 行为。

## Migration Plan

1. 建立当前实现可失败的两次先后嵌套与嵌套异常回归。
2. 把退出时写零改为恢复调用者进入深度。
3. 验证最外层正常/异常返回为零，并验证 depth≥2 拒绝策略不变。

回退只恢复原退出赋值。没有存档迁移；读取存档仍把非持久运行深度初始化为零。

## Open Questions

无。

===== fix-game-update-depth-restoration/proposal.md =====
## Why

嵌套游戏更新退出时当前会把更新深度直接重置为零，而不是恢复调用者进入前的深度，导致外层更新尚未结束时后续嵌套调用被误认为新的最外层调用。两个玩家可见修复都需要稳定识别同一次最外层点击，因此先把这个独立、可失败验证的更新生命周期缺陷交还给唯一写入深度的流程入口。

## What Changes

- 游戏更新正常或异常退出时恢复调用者进入前的更新深度。
- 只有最外层游戏更新退出后深度才恢复为零。
- 保持现有“深度达到 2 时拒绝继续递归”的策略和所有游戏时间、角色结算语义不变。

## Capabilities

### New Capabilities

- `game-update-depth-restoration`: 定义游戏更新入口与退出之间成对、异常安全的嵌套深度生命周期。

### Modified Capabilities

无。

## Impact

- 只影响游戏更新入口维护 `game_update_flow_running` 的方式及对应回归测试。
- 是 `fix-elapsed-time-line-ownership` 与 `add-per-click-orgasm-chain-gate` 的共同前置条件，但不包含两者的展示或玩法规则。
- 不改变存档格式、递归上限、NPC 调度频率、时间推进、玩家行动或渲染。

===== fix-game-update-depth-restoration/specs/game-update-depth-restoration/spec.md =====
## ADDED Requirements

### Requirement: 游戏更新退出时恢复调用者深度
每次获准进入的游戏更新 MUST 在正常或异常退出时把更新深度恢复为调用者进入前的值；只有最外层调用退出后深度 SHALL 为零。

#### Scenario: 嵌套更新正常返回
- **WHEN** 外层游戏更新以深度 1 调用一层获准的嵌套更新
- **THEN** 嵌套更新运行期间深度为 2
- **AND** 嵌套更新返回后调用者深度恢复为 1
- **AND** 外层更新返回后深度恢复为 0

#### Scenario: 嵌套更新异常返回
- **WHEN** 一层获准的嵌套更新抛出异常且外层更新继续处理
- **THEN** 嵌套更新的退出清理把调用者深度恢复为 1
- **AND** 外层更新最终正常或异常退出后深度恢复为 0

#### Scenario: 同一外层更新依次调用多个嵌套更新
- **WHEN** 第一个嵌套更新已经返回且同一外层更新随后调用第二个嵌套更新
- **THEN** 两次嵌套调用之间的深度保持为 1
- **AND** 第二个嵌套调用仍从外层调用者深度进入

### Requirement: 保持现有递归准入上限
系统 SHALL 保持游戏更新深度达到 2 时拒绝继续递归的现有准入规则，深度恢复修复 MUST NOT 使更深调用获得执行。

#### Scenario: 深度达到上限后再次调用
- **WHEN** 当前游戏更新深度已经为 2 并再次请求游戏更新
- **THEN** 新请求仍按现有规则直接返回
- **AND** 当前调用链的深度不被递增、清零或以其他方式改变

===== fix-game-update-depth-restoration/tasks.md =====
## 1. 可失败的深度生命周期回归

- [ ] 1.1 建立同一外层更新依次调用两个嵌套更新的真实入口回归，先证明当前实现会在第一个嵌套返回后错误归零。
- [ ] 1.2 建立嵌套更新正常返回和抛出异常的回归，分别断言返回调用者深度为 1、最外层最终深度为 0。
- [ ] 1.3 建立当前深度达到 2 时更深更新仍被拒绝且不改变现有深度的回归。

## 2. 成对恢复实现与验证

- [ ] 2.1 在 `game_update_flow` 入口保存调用者深度，并在已获准调用的 `finally` 中恢复该值，保持现有准入条件和流程顺序不变。
- [ ] 2.2 运行三组聚焦回归和 Python 语法检查，确认正常、异常、先后嵌套及 depth≥2 路径全部满足规格。

######## CHANGE fix-elapsed-time-line-ownership ########

===== fix-elapsed-time-line-ownership/design.md =====
## Context

`game_update_flow(add_time)` 是一次游戏更新实际推进 `cache.game_time` 的入口，随后由角色行为循环依次结算玩家与 NPC。当前经过时间文本却由角色结算面板组装函数按角色追加，因此一个时钟推进事实会被多个角色面板重复宣告；嵌套更新和时停回退还使传入的 `add_time` 不一定等于本次玩家点击最终留下的净经过时间。

本变更把实际经过时间的展示归还给最外层游戏更新入口。它与“同次点击内高潮后的 NPC 主动行为阻断”共享生命周期，但不共享行为契约、失败机制或验证证据，因此按 Fable-5 的 scope 裁定拆成独立 change。

本变更以前置 change `fix-game-update-depth-restoration` 提供的成对深度恢复为假设：这里只消费稳定的最外层更新身份，不建立或修复该身份。

## Goals / Non-Goals

**Goals:**

- 一次最外层玩家点击最多显示一条实际经过时间。
- 该文本在所有玩家与 NPC 结算完成后显示，并反映最外层入口前后游戏时钟的净正向差值。
- 角色面板只拥有角色变化；行动预览继续拥有预计持续时间。
- 普通、嵌套与时停回退路径使用同一个可测试的显示规则。

**Non-Goals:**

- 不改变玩家或 NPC 的行动时长、结算顺序、行为频率或分钟调度方式。
- 不通过渲染后的字符串去重隐藏重复文本。
- 不建立通用 `PlayerActionWindow` 模块；当前只有一个展示消费者，现有最外层更新入口已经是足够的 seam。
- 不实现或测试更新深度的成对恢复；该生命周期不变量由前置 change 独立拥有。
- 不改动“该行动将持续若干分钟”的预览文本或其显示时机。

## Decisions

### 1. 最外层游戏更新拥有实际经过时间

在前置 change 已提供稳定嵌套深度的条件下，进入最外层 `game_update_flow` 时记录游戏时钟，在角色行为结算和可能的时间回退完成后再次读取时钟。仅最外层入口根据两者的净分钟差决定是否输出，嵌套入口不输出。

选择时钟净差而不是原始 `add_time`，因为时停会回退时间，嵌套流程也可能改变最终时钟。选择最外层更新入口而不是角色结算面板，是因为前者拥有一次推进事实和完整生命周期，后者只拥有单个角色的变化。

备选方案“保留每个面板的文本并在最后去重”被拒绝：它让错误所有权继续存在，并依赖渲染内容相同。备选方案“固定显示外层 `add_time`”被拒绝：它在时间回退后可能继续报告未实际经过的时间。

### 2. 角色变化与行动预览保持独立

角色变化面板移除实际经过时间后，不改变其数值、经验、事件或 Web 回溯收集。`exchange_flag` 对应的“该行动将持续若干分钟”仍是预计持续时间，不归入实际经过时间的唯一输出规则。

### 3. 不提前抽象玩家行动窗口

实现只需要在现有更新入口识别最外层调用并形成局部前后快照。当前不增加新模块或可保存状态。若以后第三个独立消费者需要稳定窗口 ID、起止时间或每角色声明，再单独评估更深的 `PlayerActionWindow` 模块。

## Risks / Trade-offs

- **[前置深度修复未应用或发生漂移]** → 实现和验证前确认 `fix-game-update-depth-restoration` 已应用；本变更只测试显示消费者在稳定最外层身份下的行为。
- **[只测试文本计数会漏掉输出顺序]** → 自动化测试同时断言文本位于全部角色结算之后，真实 Tk 证据使用同一存档和同一路线比较前后顺序。
- **[跨日或嵌套推进使净差不同于按钮标称时长]** → 以游戏时钟净差为权威，显示真实结果而不是按钮参数。
- **[Tk 与 Web 的缓冲方式不同]** → 通过现有抽象绘制路径输出，分别验证 Tk 可见顺序和 Web 文本回溯中只出现一次。

## Migration Plan

1. 确认前置深度恢复 change 已应用，再用现有多 NPC 结算路径建立可失败的文本计数与排序回归，并覆盖嵌套更新和时停回退。
2. 从角色面板组装中移除实际经过时间，只在最外层游戏更新末尾按净分钟差输出。
3. 更新仍断言每个角色面板含“分钟过去了”的旧测试，使其改为断言角色面板不拥有该文本、整个点击只拥有一条末尾文本。
4. 运行聚焦测试、相关结算与 Web 回溯回归，并完成真实 Tk 前后对比。

回退时同时恢复原角色面板输出并移除顶层输出，避免两个所有者并存。没有存档迁移。

## Open Questions

无。

===== fix-elapsed-time-line-ownership/proposal.md =====
## Why

一次玩家点击只推进一次游戏时间，但当前每个非空角色结算面板都会各自追加“若干分钟过去了”，让同一段时间看起来被重复推进。经过玩家确认，本修复只纠正时间提示的归属和真实性，不改变角色结算内容或时间调度规则。

## What Changes

- 角色结算面板只显示该角色的数值与事件变化，不再自行宣告经过时间。
- 最外层玩家行动结算完成后，只显示一次实际经过的游戏分钟数。
- 同一玩家点击内的嵌套更新不额外显示经过时间；时停等回退使净经过时间为零时不显示经过时间。
- 保留“该行动将持续若干分钟”的行动预览语义，不把预览和实际经过时间合并。

## Capabilities

### New Capabilities

- `elapsed-time-line-ownership`: 定义一次玩家点击中实际经过时间的唯一显示所有者、嵌套更新和时间回退行为。

### Modified Capabilities

无。

## Dependencies

- `fix-game-update-depth-restoration`: 必须先提供成对、异常安全的更新深度恢复；本变更只消费稳定的最外层更新身份，不重复实现该修复。

## Impact

- 影响顶层游戏更新时间推进和角色结算结果的文本组装。
- 不改变存档格式、角色数值结算、NPC 行为频率或 Tk/Web 输入协议。
- 后续实现需要覆盖普通多角色结算、嵌套更新、时停回退，并提供真实 Tk 前后对比证据。

===== fix-elapsed-time-line-ownership/specs/elapsed-time-line-ownership/spec.md =====
## ADDED Requirements

### Requirement: 最外层玩家行动唯一显示实际经过时间
系统 SHALL 由一次最外层玩家行动更新统一显示该行动最终产生的游戏时钟净正向变化，并 SHALL 在所有玩家与 NPC 结算完成后最多显示一次；单个角色的结算面板 SHALL NOT 自行追加实际经过时间。

#### Scenario: 多个角色产生结算面板
- **WHEN** 一次玩家点击推进五分钟并产生玩家及多个 NPC 的非空结算面板
- **THEN** 各角色面板只显示各自变化
- **AND** 全部角色结算完成后只显示一次“5分钟过去了”
- **AND** Tk 可见输出与 Web 文本回溯均只记录这一条实际经过时间

#### Scenario: 没有非空角色变化面板
- **WHEN** 一次玩家点击实际推进了正数分钟但没有角色变化面板
- **THEN** 系统仍在本次最外层结算结束时显示一次实际经过时间

### Requirement: 嵌套更新共享外层时间展示
同一次最外层玩家行动内的嵌套游戏更新 SHALL NOT 各自显示经过时间；最外层结束时 SHALL 根据进入前与全部嵌套结算完成后的游戏时钟差统一显示。

#### Scenario: 玩家行动触发嵌套更新
- **WHEN** 一次玩家点击的结算过程内部再次调用游戏更新
- **THEN** 嵌套更新不显示独立的“分钟过去了”
- **AND** 外层结算结束后整个点击最多显示一条净经过时间

### Requirement: 时间回退后只显示净正向经过时间
系统 SHALL 以最外层更新入口前后的游戏时钟净分钟差为显示依据；净差为零或负数时 SHALL NOT 显示“分钟过去了”。

#### Scenario: 时停完整回退本次推进
- **WHEN** 一次时停行动先推进时间并在结算结束前完整回退
- **THEN** 本次点击不显示“分钟过去了”

#### Scenario: 结算只保留部分正向推进
- **WHEN** 一次玩家点击经过嵌套推进或回退后仍留下正数净分钟差
- **THEN** 系统只显示一次该净分钟数

#### Scenario: 结算跨过午夜
- **WHEN** 一次玩家点击从午夜前开始并在全部角色与新一天结算后结束
- **THEN** 系统按跨日后的游戏时钟净差显示一次实际经过分钟数
- **AND** 该文本位于本次点击的全部角色和新一天结算之后

#### Scenario: 上一次结算异常后开始新点击
- **WHEN** 上一次玩家点击在结算中异常退出且随后开始一次成功推进正数分钟的新点击
- **THEN** 新点击仍只在全部结算结束后显示一次自己的实际经过时间

### Requirement: 预计持续时间保持独立
系统 MUST 保留“该行动将持续若干分钟”的行动预览语义，且该预…1571 tokens truncated…按角色幂等：同一点击内的后续被动高潮可以继续完整结算，再次登记不改变结果。该集合只限制未来主动行为准入，不作为高潮事务内部的提前退出条件。

### 3. 在所有自主生成入口读取同一准入事实

普通空闲 AI 和群交 type-1/type-2 AI 在生成或选择新行为之前查询准入。命中后不得创建新的目标、自慰意图、模板占位或其他主动行为，但也不得把角色转为会绕过正常结算的 `WAIT`。

被阻断角色保持一个能继续进入现有 `judge_character_status()` 的空闲/群交被动路径，然后继续 realtime、persistent-state、interrupt、time-over、talent 和 completion 尾部。具体行为常量由实现依据可失败回归选择，但必须满足：不生成主动行为、不移出群交关系、被动结算继续、最终加入 `over_behavior_character`。

普通 H 空闲入口已有的“加入 `over_behavior_character` 后返回给调用者”路径只有在角色仍保持可让调用者继续执行 `judge_character_status()` 的空闲状态时才是可接受的被动路径；任何改为 `WAIT` 并跳过该调用的变体都不允许。

### 4. 按点击划分是明确的玩法上限

一次六十分钟点击中，NPC 首次实际释放后在该点击剩余结算内保持被动；玩家随后进行新的一分钟点击时，集合已重建，NPC 可以再次主动。这是玩家确认的行为，不表述为生理恢复或推荐玩家拆分操作。

## Risks / Trade-offs

- **[阻断位置过晚]** → 普通和群交两个生成入口分别建立可失败回归，并断言命中时没有生成目标、自慰意图或模板写入。
- **[错误使用 WAIT 跳过二段结算]** → 增加已知 sibling 回归，断言被阻断 NPC 仍调用状态/二段结算并完成，且调度循环不挂起。
- **[登记过早截断同一高潮批次]** → 测试同一调用的多部位与多重绝顶全部结算后才影响下一次行为准入。
- **[临时集合泄漏到下一点击或异常路径]** → 测试正常结束、嵌套复用和异常 `finally` 清理；不把集合放入角色或可序列化缓存结构。
- **[前置深度修复未应用或发生漂移]** → 实现和验证前确认 `fix-game-update-depth-restoration` 已应用；本变更只测试临时集合消费者在稳定最外层身份下的行为。
- **[一分钟与六十分钟点击结果不同]** → 在规格和真实 Tk 证据中明确这是按点击规则的已接受取舍，不把它包装成按分钟公平性。

## Migration Plan

1. 确认前置深度恢复 change 已应用，再建立可失败的真实函数回归：实际释放登记；成功寸止和时停蓄积不登记；普通与群交入口均阻断生成；被动结算和完成继续。
2. 在最外层更新所有者中加入非持久集合生命周期和窄查询/登记接口，覆盖嵌套与异常清理。
3. 在实际释放事务结束处登记 NPC，并保持玩家、寸止与时停分支不登记。
4. 在普通 AI 与群交 type-1/type-2 生成入口接入准入查询，使用结算安全的被动路径。
5. 运行聚焦、群交、高潮、嵌套和存档 sibling 回归，并完成真实 Tk 的长行动前后对比。

回退时先移除所有读取点，再移除写入和生命周期，避免保留无消费者的临时状态。没有存档迁移。

## Open Questions

无。普通与群交入口命中后的具体空闲行为表示可由实现选择，但必须由“被动结算继续且循环完成”的规格和回归约束；若现有行为模型没有满足这些条件的表示，应暂停并重新讨论 scope，而不是引入持久恢复状态。

===== add-per-click-orgasm-chain-gate/proposal.md =====
## Why

一次较长的玩家行动结算中，NPC 实际高潮后仍可能立即生成下一轮主动行为，从而在同一次点击内反复主动行动并再次高潮。玩家确认需要的是仅限本次点击的主动行为链阻断，而不是可保存、按游戏分钟恢复的眩晕或生理冷却。

## What Changes

- 在一次最外层玩家点击期间，临时记录已经实际高潮释放的 NPC。
- NPC 在本次点击首次实际释放后，不再生成新的自主行为；下一次玩家点击重新允许其自主行动。
- 被阻断的 NPC 仍留在原群交关系和模板中，继续受到玩家或其他角色刺激，并完成被动数值、持续状态、二段效果与高潮结算。
- 成功寸止和时停蓄积不计为实际释放；玩家不受该规则影响；一次释放事务内的多部位和多重绝顶完整结算。
- 嵌套更新复用最外层点击的临时记录，异常退出也清理记录；该状态不写入存档。

## Capabilities

### New Capabilities

- `per-click-orgasm-chain-gate`: 定义 NPC 实际释放后在同一次玩家点击内的自主行为准入、被动结算和临时状态生命周期。

### Modified Capabilities

无。

## Dependencies

- `fix-game-update-depth-restoration`: 必须先提供成对、异常安全的更新深度恢复；本变更只消费稳定的最外层更新身份，不重复实现该修复。

## Impact

- 影响最外层游戏更新生命周期、NPC 普通与群交主动行为生成入口，以及实际高潮释放的权威结算路径。
- 不改变高潮数值公式、群交模板成员关系、存档格式或通用 NPC 分钟调度策略。
- 后续实现需要覆盖普通与群交生成入口、被动结算、循环完成、嵌套更新、异常清理和真实 Tk 前后对比证据。

===== add-per-click-orgasm-chain-gate/specs/per-click-orgasm-chain-gate/spec.md =====
## ADDED Requirements

### Requirement: 每次最外层玩家点击独立记录已实际释放的 NPC
系统 SHALL 为每次最外层玩家点击创建独立、非持久的已释放 NPC 记录；同一点击内的嵌套更新 MUST 复用该记录，最外层正常或异常结束后 MUST 清理记录，下一次点击 MUST 从空记录开始。

#### Scenario: 嵌套更新发生在同一次点击内
- **WHEN** NPC 已在外层玩家点击中实际释放，随后结算触发嵌套游戏更新
- **THEN** 嵌套更新继续把该 NPC 视为本次点击已释放

#### Scenario: 同一次点击依次触发多个嵌套更新
- **WHEN** 已登记 NPC 经历第一个嵌套更新返回，随后同一外层点击又触发第二个嵌套更新
- **THEN** 两次嵌套更新都复用同一已释放 NPC 记录
- **AND** 第二次嵌套不得重建或提前清理该记录

#### Scenario: 嵌套更新异常但外层继续
- **WHEN** 已登记 NPC 所在的嵌套更新异常退出且外层结算捕获异常后继续
- **THEN** 外层记录继续保留该 NPC 直到最外层点击结束

#### Scenario: 下一次玩家点击开始
- **WHEN** 已有 NPC 在上一次玩家点击中实际释放且该点击已经结束
- **THEN** 新点击的记录为空
- **AND** 该 NPC 可以重新通过自主行为准入

#### Scenario: 结算过程异常退出
- **WHEN** 最外层玩家点击在结算期间抛出异常
- **THEN** 本次点击的临时记录仍被清理
- **AND** 后续点击不继承本次记录

#### Scenario: 保存和读取游戏
- **WHEN** 游戏在玩家点击之间保存并重新读取
- **THEN** 存档中不存在已释放 NPC 的点击内记录

### Requirement: 只有 NPC 的实际高潮释放登记主动行为阻断
系统 SHALL 只在 NPC 的实际高潮释放事务完整结算后登记该 NPC；玩家高潮、成功寸止和时停中的高潮蓄积 SHALL NOT 登记。

#### Scenario: NPC 完成多部位实际释放
- **WHEN** NPC 在同一个高潮事务中发生多个部位高潮并触发多重绝顶及派生效果
- **THEN** 系统先完整结算本事务的全部部位、多重绝顶和派生效果
- **AND** 随后幂等登记该 NPC 为本次点击已实际释放

#### Scenario: NPC 成功寸止
- **WHEN** NPC 的高潮跨级被成功寸止并只写入寸止累计
- **THEN** 该 NPC 不因本次跨级被登记
- **AND** 仍可在本次点击生成后续自主行为

#### Scenario: NPC 寸止失败后实际释放
- **WHEN** NPC 的寸止判定失败并随后进入实际释放结算
- **THEN** 系统完整结算释放事务后登记该 NPC

#### Scenario: 时停中只累计高潮
- **WHEN** NPC 的高潮仅计入时停待释放计数而未实际释放
- **THEN** 该 NPC 不被登记

#### Scenario: 时停蓄积随后实际解放
- **WHEN** NPC 的时停高潮蓄积进入实际释放结算
- **THEN** 系统完整结算释放事务后登记该 NPC

#### Scenario: 玩家实际高潮
- **WHEN** 玩家在本次点击实际高潮
- **THEN** 玩家不会被加入 NPC 已释放记录
- **AND** 该记录不限制玩家行为

### Requirement: 已实际释放 NPC 不再生成本次点击的自主行为
系统 MUST 在普通空闲 AI 和群交 type-1/type-2 AI 的所有自主行为生成入口拒绝已登记 NPC 的新行为，并 MUST NOT 因该拒绝创建新目标、自慰意图、群交模板占位或其他主动行为。

#### Scenario: 普通空闲 AI 尝试生成行为
- **WHEN** 已登记 NPC 在同一次点击内到达普通自主行为生成入口
- **THEN** 系统拒绝该 NPC 的新自主行为

#### Scenario: 群交 NPC 尝试生成行为
- **WHEN** 已登记 NPC 在同一次点击内到达群交 type-1 或 type-2 自主行为生成入口
- **THEN** 系统拒绝新的群交主动行为、自慰意图和模板写入
- **AND** NPC 仍保留现有群交参与关系和模板位置

#### Scenario: 两名 NPC 中只有一名已经释放
- **WHEN** NPC A 已登记而 NPC B 尚未实际释放
- **THEN** 本次点击只拒绝 NPC A 的自主行为生成
- **AND** NPC B 继续按既有规则生成行为

### Requirement: 主动行为阻断不妨碍被动结算和循环完成
已登记 NPC SHALL 继续接受玩家或其他角色的刺激，并 SHALL 继续运行状态、二段效果、实时变化、持续状态、中断、行为结束、素质与完成结算；系统 MUST 使该 NPC 最终进入本次调度的完成集合且不得造成循环挂起。

#### Scenario: 被阻断 NPC 继续受到群交刺激
- **WHEN** 已登记 NPC 在本次点击剩余结算中被玩家或其他角色继续刺激并增加身体或心理快感
- **THEN** 对应数值与二段效果继续结算
- **AND** NPC 不因主动行为阻断被移出群交关系或模板

#### Scenario: 被动刺激再次触发高潮
- **WHEN** 已登记 NPC 的被动快感继续上升并再次跨过高潮阈值
- **THEN** 后续被动高潮仍完整结算
- **AND** 幂等登记不恢复或新增该 NPC 的主动行为

#### Scenario: 被阻断 NPC 完成本次调度
- **WHEN** 已登记 NPC 没有新的自主行为可生成
- **THEN** 系统仍执行其正常结算尾部并把该 NPC 加入完成集合
- **AND** 玩家点击能够正常结束

### Requirement: 主动行为阻断按玩家点击而非游戏分钟恢复
系统 SHALL 把规则限定在一次最外层玩家点击内，不建立按游戏分钟倒计时的恢复状态。

#### Scenario: 一次长点击中首次释放
- **WHEN** NPC 在一次六十分钟玩家点击的中途实际释放
- **THEN** 该 NPC 在这次点击剩余结算内不再生成自主行为

#### Scenario: 长点击结束后的新短点击
- **WHEN** 上述六十分钟点击已经结束且玩家开始新的一分钟点击
- **THEN** NPC 可在新点击中重新生成自主行为

===== add-per-click-orgasm-chain-gate/tasks.md =====
## 1. 可失败回归与权威事件

- [ ] 1.1 用真实高潮结算函数建立回归，证明 NPC 实际释放后会在同一次点击再次进入普通或群交自主行为生成，并让旧实现先失败。
- [ ] 1.2 分别覆盖实际释放、同事务多部位与多重绝顶、成功寸止、时停蓄积和玩家高潮，锁定唯一登记条件与登记时机。
- [ ] 1.3 建立普通 AI、群交 type-1/type-2、两名 NPC 隔离、被动再次高潮和完成集合回归，特别证明不能用跳过 `judge_character_status()` 的 `WAIT` 路径阻断。
- [ ] 1.4 确认前置 change `fix-game-update-depth-restoration` 已应用；建立两次先后嵌套仍复用记录、嵌套异常不清理外层记录、最外层异常清理、下一点击重置和保存/读取的消费者回归，不重复深度修复本身的测试。

## 2. 点击内临时状态

- [ ] 2.1 在现有最外层游戏更新所有者内实现非持久的已释放 NPC 集合，并提供登记与准入查询两个窄操作。
- [ ] 2.2 让嵌套更新复用外层集合，最外层 `finally` 在正常与异常路径清理，并确认集合不进入角色数据、缓存序列化或存档。

## 3. 实际释放登记

- [ ] 3.1 在权威高潮实际释放路径的完整事务结束后幂等登记 NPC，保证同批全部部位、多重绝顶和派生效果已形成。
- [ ] 3.2 保持玩家、成功寸止和时停蓄积分支不登记，并覆盖寸止失败或时停解放只有在真正释放后才登记。

## 4. 自主行为准入与被动完成

- [ ] 4.1 在普通空闲 AI 生成入口拒绝已登记 NPC 的新目标和新行为，同时让其继续正常状态与调度尾部结算。
- [ ] 4.2 在群交 type-1/type-2 生成入口拒绝新自慰意图、模板占位和其他主动行为，不移除现有参与关系或模板位置。
- [ ] 4.3 验证被阻断 NPC 仍接受刺激、累计身体与心理快感、结算二段效果和被动高潮，并最终进入 `over_behavior_character`，无循环挂起。

## 5. 自动化验证

- [ ] 5.1 运行聚焦真实函数回归、相关群交与高潮测试、嵌套/异常测试、存档 sibling 回归和 Python 语法检查。
- [ ] 5.2 运行相邻的寸止、时停释放、多部位绝顶、群交模板和普通 NPC 行为测试，确认数值公式、成员关系与非目标调度语义未改变。
- [ ] 5.3 明确验证一次六十分钟点击中首次释放后保持被动，而下一次新点击立即重新允许主动行为。

## 6. 上游可见证据与审计

- [ ] 6.1 由本地视觉执行者在真实 Tk、同一存档和同一路线下捕获长行动的修复前后完整帧序列，证明同次点击的释放后主动链被阻断且结算正常结束。
- [ ] 6.2 让 Fable-5 依据本地项目写作规则生成中文 PR 标题和正文，只使用拟提交 diff、已提交测试和准备公开的 Tk 证据支持声明。
- [ ] 6.3 对完整拟提交 diff、PR 文本和证据执行 fresh-context PR artifact 审计，达到 `local-review-ready` 后再请求任何提交、推送或发布授权。

`````

### Verdict

`````text
**REVISE**

One edit required; everything else complies with the final ruling.

## Required edit

- **`fix-game-update-depth-restoration/proposal.md`** — add a short evidence/publication note (under `## Impact` or a new `## 发布证据` heading) recording the item-6 decision: this change has no standalone player-visible claim; its verification is the automated depth-invariant regression only; standalone upstream publication is blocked because no honest real-Tk before/after exists for the diff alone; its PR-visible proof is combined evidence — it ships alongside (or is exercised by) a consumer change whose Tk evidence depends on the restored outermost identity. Optionally mirror one sentence in `tasks.md` §2 so the task list doesn't imply the change is publish-ready after 2.2.

Rationale for the item-6 decision: the diff's only externally observable delta on its own is which double-nested calls hit the existing depth≥2 rejection — a corrected-admission effect with no reproduced player-visible symptom in any artifact. Automated invariant proof is therefore sufficient *locally*, and inventing a synthetic Tk demonstration would be dishonest; but the local rule requiring real-Tk evidence for behavior-changing candidates means the proposal must record the combined-evidence/publication-blocker status explicitly rather than stay silent. Currently it records nothing.

## Per-change contract / owner / seam

- **fix-game-update-depth-restoration** — one contract (paired, exception-safe depth restoration at the sole writer `game_update_flow`), one owner, no prerequisite, depth≥2 rejection explicitly preserved as its own requirement. ✓
- **fix-elapsed-time-line-ownership** — one contract (single net-elapsed-time line owned by the outermost update, after all settlement), one owner; seam is the existing outermost entry, no PlayerActionWindow. ✓
- **add-per-click-orgasm-chain-gate** — one contract (per-click released-NPC record: authoritative registration point, admission read points, passive settlement preserved, non-persistent lifecycle), one owner; two narrow operations, no window object. ✓

## Dependency and duplication audit

Both consumers declare the single dependency in `proposal.md ## Dependencies` and in design Context. Both carry explicit non-goals ("不实现或测试更新深度的成对恢复") and their prerequisite tasks (elapsed 1.3, orgasm 1.4) are phrased as "confirm applied, test only consumer behavior" — the conditional-depth-repair language is gone. Orgasm-gate's sequential-nested and exception scenarios assert record reuse/cleanup, not depth values; elapsed-time's nested scenarios assert display counts, not depth values. No duplication. The two consumers do not reference each other. ✓

## Scenarios and inverse audit

- **Depth change**: normal nested, nested exception, sequential nested, outermost-zero (asserted in both normal and exception scenarios), depth≥2 unchanged — all present. ✓
- **Elapsed-time**: multi-actor with Tk/Web single occurrence, no-panels, nested consumption, full rollback (zero), partial positive, cross-midnight with end-ordering, post-exception next click, preview inverse — all present. ✓
- **Orgasm-gate**: sequential nested reuse, nested-exception retention, outer-exception cleanup, next-click reset, save inverse, full-transaction-then-register, failed-edging release, time-stop release, successful-edging negative, time-stop-accumulation negative, player inverse, ordinary + group type-1/type-2 read points, two-NPC isolation, passive repeat orgasm with idempotent registration, completion/no-hang, 1-minute/60-minute trade-off — all present. ✓

## Task / red-proof audit

All three change task lists open with red-capable regressions against the real entry points ("先证明当前实现…错误归零" / "先证明…重复出现" / "让旧实现先失败"), ordered red → implement → focused verification → adjacent-behavior inverse runs. Tasks stay inside each contract; no scheduler, backfill, persistent cooldown, or worktree narrative appears. The orgasm-gate WAIT-bypass sibling is pinned in both design and task 1.3. ✓

## PR / Tk evidence classification

- **fix-elapsed-time-line-ownership**: player-visible; tasks 4.1–4.3 promise real-Tk same-save/same-route before/after frames, Fable-written Chinese PR prose from committed diff + public evidence only, and a fresh-context artifact audit gate. Honest and PR-visible. ✓
- **add-per-click-orgasm-chain-gate**: player-visible; tasks 6.1–6.3 same structure, with the long-action frame sequence as evidence and the per-click trade-off explicitly surfaced rather than hidden. Honest and PR-visible. ✓
- **fix-game-update-depth-restoration**: no player-visible claim, no Tk promise (honest), but publication status unrecorded — the single REVISE item above.

## Readiness

The package matches the binding ruling in ownership, dependency shape, scenario coverage, and evidence honesty; after the one proposal.md publication-note edit to the depth change, implementation can begin without guessing and the audit would PASS.
`````

## Final post-edit compliance check

### Prompt

`````text
/investigate-game-bug

# Final post-edit compliance check

The prior complete-package audit returned REVISE with exactly one required edit:

"fix-game-update-depth-restoration/proposal.md — add a short evidence/publication note recording that this change has no standalone player-visible claim; automated depth-invariant regression is sufficient locally; standalone upstream publication is blocked because no honest real-Tk before/after exists for the diff alone; PR-visible proof must be combined with a consumer diff whose real Tk evidence depends on restored outermost identity. Optionally mirror this in tasks.md."

The complete package otherwise passed contract/owner/seam, dependency/nonduplication, all scenarios/inverses, red-proof tasks, and the two consumer Tk/PR gates.

The edit now present verbatim is:

## 发布证据

- 本 change 不提出可独立观察的玩家可见变化；本地实现验证只使用自动化深度不变量回归，不制作虚假的 Tk 对比。
- 按本仓库对行为修复的真实 Tk 证据要求，它不能单独宣称达到上游发布就绪。只有当某个消费者 change 的拟提交 diff 同时包含此前置修复，且该消费者的真实 Tk 前后证据确实依赖并覆盖稳定的最外层身份时，才可随该消费者进入发布审计。

tasks.md also now adds:

- [ ] 2.3 记录本地自动化验证结果但不把此前置修复单独标为上游发布就绪；发布审计必须由实际包含该修复的消费者 diff 和真实 Tk 证据共同覆盖。

OpenSpec strict validation passes for this updated change.

Do not revisit any settled architecture or player semantics. Verify only whether this exact edit resolves the sole prior finding without creating a contradiction.

Lead with exactly PASS, REVISE, or BLOCKED. Then give at most five concise bullets covering:
- whether the publication/evidence classification is now explicit and honest;
- whether it preserves the three-change dependency ruling;
- whether any required edit remains;
- final implementation-readiness status.

Do not edit files, write code, or draft PR prose.
`````

### Verdict

`````text
PASS

- **Publication/evidence classification is now explicit and honest.** The 发布证据 section states plainly that this change makes no standalone player-visible claim, that local verification rests solely on the automated depth-invariant regression, and that no fabricated Tk comparison will be produced — exactly the honesty the prior finding demanded.
- **Standalone-publication block is correctly conditioned.** Upstream readiness is denied for the diff alone and granted only when a consumer change's proposed diff bundles this prerequisite *and* that consumer's real-Tk before/after evidence actually depends on and covers stable outermost identity — this matches, not merely paraphrases, the required note.
- **Three-change dependency ruling preserved.** Nothing in the new text reopens the settled architecture or consumer relationships; it reinforces the ruling by routing publication audit through the consumer diffs rather than around them.
- **No required edit remains.** Task 2.3 mirrors the proposal note consistently (local automated verification recorded, no standalone upstream-ready marking, audit via consumer diff + real Tk evidence), and OpenSpec strict validation passing means the addition introduced no structural regression.
- **Implementation-ready.** The sole prior finding is resolved without contradiction; the package may proceed to implementation, with upstream publication of this change gated as written — only alongside a qualifying consumer change.

Note on verification scope: this session has no file access (tools disabled), so the verdict rests on the quoted edit text supplied in the prompt, taken as an accurate transcription of the current files.
`````
