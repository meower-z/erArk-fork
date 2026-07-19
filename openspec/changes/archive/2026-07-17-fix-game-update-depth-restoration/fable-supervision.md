# Fable-5 Supervision Record

Every prompt and verdict that owns or audits this enabling change is reproduced verbatim. All invocations used:

`claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence "<prompt>"`

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

## Final implementation and deferred-queue audit — 2026-07-14

### Prompt

`````text
/investigate-game-bug

请审计 erArk OpenSpec change `fix-game-update-depth-restoration` 的已实现候选，以及用户刚确认的 deferred follow-up 记录。你没有文件工具；以下事实均来自 Codex 对当前源、候选 diff、测试输出和 OpenSpec 的直接核对。

用户最终选择：先实施最小深度恢复修复；把“以后取消嵌套，改用最外层循环和待执行请求队列”列为独立后续工作，不在本 change 实现。

当前已接受的 change contract：
1. `update.game_update_flow()` 是 `cache.game_update_flow_running` 的唯一写入者。
2. depth >= 2 的请求继续直接返回。
3. 每个获准调用保存进入前深度，进入时加一，正常或异常退出时恢复进入前深度；只有最外层退出后为零。
4. 不改变游戏时间推进、角色结算顺序、NPC 行为频率、显示、高潮规则或存档。

基线生产实现：depth < 2 时 `game_update_flow_running += 1`，然后推进游戏时间、运行完整角色结算、聚焦输入；finally 无条件把深度写成 0。

红测试通过真实 `game_update_flow()` 入口、以隔离的真实依赖接口运行：
- 同一外层依次发起两个嵌套更新，期望观察深度 [1,2,1,2,1]；基线实际 [1,2,0,1,0]，失败。
- 嵌套更新抛出异常且由外层捕获，期望 [1,2,1]；基线实际 [1,2,0]，失败。
- 最外层异常退出恢复 0，基线通过。
- depth 已为 2 时请求不推进时间、不结算、不聚焦且深度保持 2，基线通过。

候选生产 diff 仅在准入检查之后：
- 保存 `caller_depth = cache.game_update_flow_running`；
- 写入 `caller_depth + 1`；
- finally 恢复 `caller_depth`，不再写死 0。
没有其他生产修改。候选结果：4 tests passed；`py_compile` 通过；`git diff --check` 通过；`openspec validate fix-game-update-depth-restoration --strict` 通过。

新增 design 的 deferred follow-up 原文：
“以后用独立 change 评估把同步嵌套的 `game_update_flow()` 改为‘最外层更新循环 + 临时待执行请求队列’，使当前结算完整结束后再按请求顺序推进后续时间。本 change 不实现或预留该队列，因为它会改变当前效果链、二段结算与实时结算之间的执行顺序，不属于深度恢复修复。

后续设计必须先明确：队列项保存分钟还是完整待执行行为；同一点击内多个请求的顺序与显示累计方式；当前 depth>=2 时被拒绝的请求是否改为补做；异常时未执行请求如何清理；以及延迟执行前玩家和 NPC 行为状态由谁保存、恢复。只有在把‘角色结算不得重入’确认为独立游戏更新规则并完成真实调用链回归后，才进入实现。”

本 change 明确不能单独声称上游发布就绪；它只能随实际消费者 diff 和真实 Tk 证据进入发布审计。

请给出 PASS 或 REVISE，并分别判断：
A. 候选是否精确满足当前深度恢复 contract，未改变准入和结算语义；
B. 测试是否足以反驳原 bug 并保护正常、异常、顺序嵌套和 depth 上限；
C. deferred follow-up 是否清楚、可发现且没有把队列偷渡进当前 scope；
D. 当前是否可以把实现任务全部标记完成，同时保留“不可单独发布就绪”的限制。
如 REVISE，只列必须修改项，不建议无关重构。
`````

### Verdict

`````text
**PASS。**

**A — 满足 contract。** 候选把无条件写 0 改为保存/恢复进入前深度，恰好落在 contract 第 3 条上；准入检查（depth ≥ 2 直接返回）和检查之后的结算流程均未触碰，第 2、4 条由“diff 仅在准入检查之后、无其他生产修改”保证。第 1 条（唯一写入者）不是这个 diff 能证明的属性——接受它是基于你此前对当前源的核对，这个依据在记录里要写明是源级核对结论，不是测试结论。

**B — 测试足够。** 四个用例正好覆盖四个失效面：顺序嵌套（[1,2,0,1,0] 反驳原 bug 的核心表现——第二个嵌套在深度已被清零后被当作最外层）、嵌套异常传播、最外层异常归零、depth 上限拒绝且无副作用。红→绿都经真实入口，观察点是深度序列而非“不崩溃”。没有必须补的用例。

**C — 界限清楚。** deferred 原文明确“不实现或预留该队列”，并给出了不做的理由（会改变效果链/二段结算/实时结算顺序）和后续设计必须先回答的五个问题，还设了“角色结算不得重入确认为独立规则 + 真实调用链回归”的进入门槛。没有队列结构、标志位或占位接口偷渡进当前 diff。放在 design 里可发现。

**D — 可以全部标记完成，附一个条件。** 实现任务可标完成；但“不可单独声称上游发布就绪、须随消费者 diff 和真实 Tk 证据进入发布审计”这条限制必须以未勾选任务或显式 blocker 的形式留在 tasks.md/OpenSpec 记录里，而不是只存在于本次对话——否则下一个读 tasks 的会话会把全勾解读为可发布。

无必须修改项（D 的条件是记录位置要求，不是候选修改）。
`````

## PR draft writing — 2026-07-14

### Prompt

`````text
/investigate-game-bug

请作为 erArk 上游 PR 文案作者，使用中文为下面这个精确候选 diff 写一个供用户审核的 PR title 和 body。输出只能包含：一行 `Title: ...`，然后 `Body:` 和完整 Markdown 正文。不要输出评审结论、解释或备选版本。

写作要求：
- 采用已接受上游 PR 的简洁高度，正文依次为 `## 问题`、`## 修复`、`## 验证`。
- 只声明 proposed diff 真正改变并由 submitted test 证明的行为。
- 不提本地分支、worktree、commit hash、OpenSpec、Fable、agent、私有调查、队列方案或尚未实现的消费者。
- 不声称修复了重复高潮、“分钟过去了”重复显示或任何其他玩家可见症状；这些不在 diff 中。
- 不写文件清单，不写独立的非目标/修改范围章节，不写 rejected design。
- 没有 Tk 截图或其他外部证据，不得虚构。
- 自动化测试文件会随 PR 一并提交，所以可以简洁描述它实际断言的四种情况；不要列本地命令、路径或本地运行环境。
- `game_update_flow_running` 是现有源码名，可以在原因和修复段出现，但标题应尽量用普通中文描述具体错误。

候选基线：当前 upstream/master。当前开放上游 PR 没有相同 scope。

Proposed production diff 的完整语义：
- 现有 `game_update_flow(add_time)` 在当前 `game_update_flow_running >= 2` 时仍直接返回，此准入规则不变。
- 获准进入时，旧实现直接 `game_update_flow_running += 1`。
- 旧 `finally` 无条件写 `game_update_flow_running = 0`。
- 候选在获准进入后保存 `caller_depth = game_update_flow_running`，写入 `caller_depth + 1`，并在 `finally` 恢复 `caller_depth`。
- 推进游戏时间、调用完整角色结算、聚焦输入的顺序完全不变。

Submitted automated regression 的完整可见证明：
1. 同一外层更新依次发起两个嵌套更新：每个嵌套运行时深度为 2，两次之间恢复为 1，外层最终恢复为 0。旧实现观察为 `[1, 2, 0, 1, 0]`，候选期望并得到 `[1, 2, 1, 2, 1]`。
2. 嵌套更新抛出异常并由外层捕获：返回外层后深度恢复为 1，外层最后恢复为 0。旧实现返回外层后为 0。
3. 最外层更新抛出异常：最终深度恢复为 0。
4. 当前深度已经为 2 时再次请求更新：仍不推进时间、不运行角色结算、不聚焦输入，深度保持 2。

可确认的源码事实：当前运行时只有 `game_update_flow()` 写 `game_update_flow_running`；存档加载只把这个非持久运行状态初始化为 0。这个所有权事实来自源码核对，测试只证明上述生命周期行为。

请写一份诚实、可逐段理解的 draft。不要把“为未来消费者提供稳定身份”当作当前 PR 的用户价值；只解释当前嵌套更新深度会在内层返回后错误清零，以及候选如何恢复调用者进入前深度并保持既有上限。
`````

### Output

`````text
Title: 修复游戏更新流程嵌套调用时运行深度被内层提前清零的问题

Body:

## 问题

`game_update_flow()` 用 `game_update_flow_running` 记录更新流程当前的运行深度，深度达到 2 时直接返回，以限制嵌套层数。但退出时的 `finally` 无条件把 `game_update_flow_running` 写回 0：当一次更新流程内部又触发一次更新时，内层返回后深度被直接清零，而不是恢复成外层进入时的 1。此时外层仍在运行，深度计数已经失真——外层随后再发起的嵌套更新会被当成全新的最外层调用，既有的两层上限实际失效。

## 修复

进入流程时先保存调用前的深度 `caller_depth = game_update_flow_running`，再写入 `caller_depth + 1`；`finally` 中恢复为 `caller_depth`，而不是固定写 0。深度已达 2 时直接返回的准入规则保持不变，推进游戏时间、执行角色结算、聚焦输入的顺序也完全不变。当前运行时只有 `game_update_flow()` 本身会写这个变量，存档加载仅把这个非持久的运行状态初始化为 0，因此恢复调用前深度不会影响其他代码。

## 验证

随 PR 提交自动化回归测试，断言以下四种情况：

1. 同一外层更新先后发起两个嵌套更新：每个嵌套运行期间深度为 2，两次嵌套之间恢复为 1，外层结束后回到 0。在外层运行、两次嵌套运行及其前后各观察点上，旧实现记录到 `[1, 2, 0, 1, 0]`，修复后为 `[1, 2, 1, 2, 1]`。
2. 嵌套更新抛出异常并被外层捕获：回到外层后深度恢复为 1，外层结束后回到 0。旧实现回到外层时深度已被清成 0。
3. 最外层更新抛出异常：深度最终恢复为 0。
4. 深度已为 2 时再次请求更新：不推进游戏时间、不运行角色结算、不聚焦输入，深度保持 2。
`````
