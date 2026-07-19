## Context

The previous split replaced one monolithic `local_bugfix` with directories named after historical symptoms. That improved install isolation, but it did not consistently move each rule to its real owner. Several current components still depend on copied upstream functions, import-time monkeypatches, process-global flags, queue drains, or the identity of `cache.over_behavior_character` to infer a lifecycle that the core does not represent explicitly.

This design is based on parallel source audits of the group/H, hypnosis/state, and input/UI areas. The audits compared the current branch with `upstream/master@0dcac14d`, inspected current mod tests and active OpenSpec changes, and kept ongoing PR work out of scope.

### Coordination exclusions

The following work already has a separate owner or PR path and SHALL NOT be absorbed here:

- commission reputation display formatting;
- cross-platform save path normalization;
- group-AI player-target restoration (upstream PR #210);
- hidden-sex witness deduplication;
- the `SCENE_ALL_NOT_H`, `SCENE_ALL_UNCONSCIOUS`, and `SCENE_ALL_NOT_TIRED` loop fixes;
- time-stop instruction 5052.

### Evidence status

Current focused suites are green but are treated as a baseline, not as proof that the current design is correct:

- group/H component suites: 104 passed;
- hypnosis, pain, and movement component suites: 38 passed;
- settlement-input and NPC-move component suites: 10 passed;
- `local_performance` and `local_fontfix` direct runners: passed;
- split-manifest and ModManager suites: 15 passed;
- pain-as-pleasure near-real BDD: 10 passed;
- hypnosis near-real BDD: 3 passed.

The group-AI save BDD did not complete within five minutes in this audit and is not current runtime evidence. No full Web game flow or Windows font validation was completed.

One result demonstrates why green tests are insufficient. Real movement talk uses templates such as `{NickName}来到了{SceneName}` in `data/talk/system/move.csv`. `talk.code_text_to_draw_text()` classifies any string that starts and ends with braces as a single common-talk token and then changes the actor to the player. `local_npc_move_talk_context_fix` instead intercepts the nonexistent production input `{move}`; its test fabricates that input and therefore cannot fail on the real bug.

A focused check through the real formatter and ModManager produced the same player-attributed output before and after loading that mod independently. Appending a newline to the same real template avoided the brace-shape branch and preserved the NPC actor, isolating the classifier. The compiled talk data contains 37 multi-placeholder templates with the same false-positive shape, including seven movement templates. This is function-level runtime evidence, not yet a full save/main-loop or Tk/Web visual reproduction.

## Goals / Non-Goals

**Goals:**

- Replace symptom and mod-directory boundaries with fixes organized by the rule and code that own the behavior.
- Identify small direct fixes that can become independent upstream PRs.
- Identify complex mods that must be frozen until an owner-level interface and red-capable reproduction exist.
- Remove lifecycle guesses based on timing, object identity, or unscoped global flags.
- Preserve explicit user decisions already recorded in active changes, including pain-as-pleasure semantics, without silently reopening them.
- Provide a migration order that keeps working local protections until an equivalent direct fix is verified.

**Non-Goals:**

- Implementing the runtime refactors in this analysis change.
- Combining all group/H behavior into one large module or PR.
- Publishing, pushing, or editing any active upstream PR.
- Treating current test success as proof that the reported player behavior is fixed.
- Deciding unresolved gameplay rules such as long-window masturbation frequency or repeated identical orgasm-effect multiplicity.

## Decisions

### 1. Use a four-stage evidence gate

Every fix moves through four separately recorded states:

1. **Clue:** the player or agent observation.
2. **Reproduction:** a minimal check that can fail on the exact observation.
3. **Cause:** a falsified-and-confirmed violated rule plus its logical owner.
4. **Verified fix:** the original and sibling paths pass after the owner-level change.

An implementation or README explanation does not promote a clue to a cause. Static control-flow evidence can establish a strong candidate for a deterministic branch defect, but the cause remains unconfirmed until a faithful reproduction runs and distinguishes it from competing explanations.

### 2. Replace current mod boundaries with owner-based workstreams

The table records the disposition of each remaining area. "Freeze" means no additional wrappers or upstreaming of the current implementation; it does not mean deleting a locally useful protection before its replacement exists.

| Current area | Root-cause finding | Disposition | Intended owner and shape |
| --- | --- | --- | --- |
| `local_npc_move_talk_context_fix` | The real multi-placeholder move template is misclassified as one common token; the mod intercepts a non-production `{move}` input. | Replace, then delete the mod. | In `talk`, parse an exact single token with a full match and known token key, or separate template expansion from actor formatting. This is a small direct fix. |
| `local_performance` | Queue rendering repeats `see_end()`, while its wait patch separately guesses input age with a 30 ms delay and whole-queue drains. | Split. Retain the rendering idea; remove the wait behavior after replacement. | Tk queue rendering owns one final scroll per drained batch. Core input owns prompt identity; performance code does not clear input. |
| `local_settlement_input_fix` | Web wait elements have a `wait_id`, but response, flow, and browser paths still consume an unscoped global boolean. Skip ownership and dialog completion are also inferred from global snapshots. | Freeze; do not upstream current wrappers. Proposed default disablement requires a separate implementation review. | Core flow owns a prompt record `{id, kind, allowed responses, state}`. Tk and Web are adapters; one game thread consumes a matching response once. |
| `local_fontfix` | Tk reports a named font object as loaded even when `Font.actual` resolves to a fallback family. | Temporarily retain, then direct-fix and delete. | Tk bootstrap resolves packaged resources, registers private platform fonts, and verifies the actual family. Windows proof is required. |
| `local_group_masturbation_intent_fix` plus the local type-1 ordering edit | Intent generation, action-window identity, behavior protection, duration, and successful consumption are spread across a core ordering edit and process globals. | Split and replace the token/active-set implementation. | Group AI creates a planned action. The NPC scheduler supplies an explicit action-window ID and commits consumption only after settlement succeeds. Keep type-1-before-template ordering as an independent small fix. |
| `local_group_participant_admission_fix` after coordination exclusions | Eligibility is repeated in UI callers, is not rechecked on arrival, and the discovery panel has two incompatible settlement-owner protocols. | Dissolve into separate fixes. | A group admission function evaluates list, click, and arrival transitions; cancellation remains available even after state changes. Discovery returns a resolution to a caller that owns exactly one settlement. Keep exact-once discovery postponed until that context is explicit. |
| `local_h_movement_interrupt_fix` | Movement is represented by several fields with no transition owner; the mod copies the player loop and patches consumers after stale `MOVE` state already exists. | Replace, not upstream as written. | A movement-plan operation cancels a plan at the transition into H/group state, preserves any historical `move_src` contract, and commits the new behavior once. |
| `local_hypnosis_state_fix` | Manual type `0`, active hypnosis, ordinary unconsciousness, derived abnormal flags, room side effects, and cleanup have no single transition owner. The talk gate is a separate predicate problem. | Split and rewrite. | `resolve_hypnosis_type`, `set_hypnosis_mode`, and `clear_hypnosis(reason)` own state transitions. A narrow talk-gate fix uses the authoritative hypnosis predicate without copying the UI method. |
| `local_pain_as_pleasure_fix` | Negative common pain and direct pain writers do not share one adjusted-delta path. Cancellation cleanup is lifecycle behavior, not numeric settlement. | Split. | Hypnosis cleanup clears the flag. Settlement computes the final signed delta once and routes positive converted pain plus all direct writers through one operation. Preserve the accepted flag/sleep/accounting contract from the active change. |
| `local_h_orgasm_batch_fix` | One 1093-line component mixes duplicate math fixes, repeated-delta detection, counted events, rendering, remote input suppression, human power, exhaustion, and window-end edge policy. | Split into correctness fixes and later domain refactor; freeze current implementation for upstreaming. | First fix duplicate settlement and repeated use of one change object. Then introduce a counted, atomic orgasm transaction. Rendering and window-end policy consume its result but are not part of the math fix. |
| `local_group_edge_release_fix` | Pending edge state can be erased by H reset because the orgasm domain has no required finalizer. A separate tired-transition overwrite is patched in the same mod. | Move finalization into the orgasm domain; move tired behavior to scheduler work. | `finalize_pending_edges(ids, reason, change_set, visibility)` succeeds before state reset. Exit paths call it; they do not discover, capture, or clear effects themselves. |
| `group_sex_extension` | This is a feature mod, but it duplicates participant resolution, swallows errors, and directly mutates edge state. | Keep independent as a feature; adapt later. | Consume the shared admitted-participant resolver and orgasm controller. Do not merge feature commands into bugfix PRs. |

### 3. Establish one assumed-upstream integration baseline

Local `main` is the only integration branch. It contains the exact production commits from upstream PRs 204, 205, 206, 207, and 210 plus the already-present PR 211 behavior. The temporary `dev` branch was fast-forwarded into `main` and deleted. This baseline models the game after those PRs are accepted; it does not claim that GitHub has merged them and it is not pushed without separate authorization.

| PR | Upstream head | Local overlay commit | Responsibility |
| --- | --- | --- | --- |
| 204 | `92cc96496` | `63735e668` | Commission reputation display |
| 205 | `b8fe52c24` | `bb522dc3a` | Full-scene premise traversal |
| 206 | `5928fbf81` | `adbc74fa5` | Hidden-sex witness deduplication |
| 207 | `2dd4e9d6b` | `7b688521b` | Cross-platform save-path normalization |
| 210 | `057334fbe` | `c6591f4b0` | Group-AI player-target restoration |
| 211 | `66e3d2b52` | already in `main` | Instruction 5052 premise correction |

Duplicate local behavior must be removed before testing the overlay:

- `local_commission_number_display_fix` is already disabled and can be retired under PR 204 semantics;
- `local_cross_platform_save_fix` and the live behavior of `local_group_target_context_fix` are disabled after PRs 207 and 210 are applied;
- `local_group_participant_admission_fix` remains enabled, but its `place_all_not_h` and hidden-witness wrappers are removed because PRs 205 and 206 now own those rules;
- its stronger group-admission fatigue policy remains local and delegates to the corrected core scene predicate instead of copying the upstream loop.

Each overlaid PR remains one local commit, so it can be reverted or replaced independently. The mixed participant-mod cleanup is a separate integration commit and must be reconsidered only when reverting PR 205 or 206.

The integration overlay verification completed with duplicate wrappers disabled: 16 focused core-overlay tests, 16 remaining participant-admission component tests, five default-config/ModManager tests, three near-real loader ownership tests, four near-real group-admission tests, six near-real cross-platform save tests, and three non-type-1 target-lifetime save tests passed. The five overlaid core files and remaining participant script also passed `py_compile`.

### 4. Isolate and review every direct upstream candidate

Every new candidate starts from current `upstream/master` in a linked worktree of the main repository, on its own `codex/<candidate>` branch. Independent clones are prohibited for ordinary PR work. The five historical PR clones and their ten linked evidence worktrees were removed after their source commits were preserved remotely and in the integration baseline.

The central OpenSpec change remains authoritative in `main`; candidate branches do not carry integration-only specs or unrelated mods. Before production edits, each candidate must compare the symptom patch with at least one owner-level local refactor, record the violated rule, owner, sibling cases, inverse cases, non-goals, and chosen boundary, then pass a fresh-context design critique. Only after that gate may implementation begin. Each candidate must then produce a faithful red/green reproduction, one representative repeatable Tk player flow, inspected comparable before/after images for its main easy-to-understand case, and a local Chinese PR draft authored by `fable-5` at medium effort. A fixed random seed and explored fixed action route may make chance-dependent evidence deterministic. State evidence may supplement but never replace the Tk images; sibling cases do not each require their own image sequence.

A different independent reviewer must judge the final title and body strictly in the upstream PR review context, using only the proposed upstream diff and evidence that will actually be included in the PR. The draft passes only when it has all three properties:

1. **Self-contained:** an erArk player who has not seen the reported bug or proposed code can understand every claim from the PR and its evidence. The opening names the exact feature or scene and wrong behavior without teaching familiar gameplay. Existing terms used by game code or dialogue may stand unexplained; coined or private terms must be defined first or removed. The text must not depend on local-only tests, `/tmp` paths, unpublished evidence, investigation notes, implementation drafts, assumed local overlays, or facts omitted from the submitted PR.
2. **No redundant information:** every sentence is necessary to understand the problem, root cause, chosen fix, review boundary, or submitted verification. Remove investigation history, repeated explanations, standalone non-goal inventories, file/line narration already obvious from the diff, and verification not represented by the PR.
3. **Every prefix is understandable:** the title and body introduce terms, context, and claims before using them, so every prefix read in order is coherent without relying on a later section to repair ambiguity or define an earlier statement.

Examples in tests, evidence, screenshots, and PR text should use standard operators and their canonical display names whenever the scenario permits. PR titles and bodies must not use child-operator names, nicknames such as `小兔子`, or local/custom character names as the reader's only example; those names add project-local context that an upstream reviewer should not have to reconstruct.

The independent reviewer receives no local investigation narrative that could silently fill gaps in the draft. Actionable feedback is revised and reviewed again. A passed review or a genuine blocker ends that candidate. No candidate is pushed, no screenshot is published, and no GitHub PR is created without user approval.

Current candidate ledger:

| Candidate | Confirmed status | Review state |
| --- | --- | --- |
| Movement-talk classification | Real `move.csv` templates reproduce actor-context corruption. Two independent design reviews agree that duplicated brace-shape guesses are the enabling logic, not movement itself. | Evidence-plan blocked. The `slot 10` recall route was disproved by breakfast priority and private-room admission. Discover a scheduler-reachable public-scene route through recorded manual Tk exploration, then freeze its save, actions, and complete random environment for one comparable baseline/candidate pair. |
| Type-1 group-AI ordering | The early return and candidate state difference reproduce, but the intended behavior is not confirmed. Player-facing settings text and premise documentation both restrict type 1 to NPCs outside the template. | Stopped as a semantic blocker after independent review. Keep the local candidate only as investigation evidence; do not present it as an upstream-ready fix. |
| Tk queue scrolling | Repeated per-item `see_end()` calls and their Tk cost reproduce without touching wait/input/Web code. | Blocked on an exact player operation and comparable real Tk image sequence for the response and scrolling change. The injected-error continuation behavior also lacks a normal player trigger and cannot use debug injection as PR evidence. |
| Ordinary edge failure | The caller replays a partially consumed climax delta after the settlement owner has already advanced levels and mutated the held ledger. | Blocked on one deterministic Tk case. Fix the random seed and explore body-part action routes until one sequence shows an earlier successful edge followed by a later failure before and after. |
| H-entry movement cancellation | Entering H leaves `move_final_target` as a live pre-H route commitment while `move_src` and `move_target` are settled-edge history. | Blocked on one normal player-or-operator route that enters H before a multi-segment journey ends, plus one representative Tk sequence. |
| Group invitation lifecycle | Production tracing rejected the broader route-ownership defect: upstream cancellation already replaces travel with WAIT, and arrival rechecks have no authoritative gameplay contract. The only surviving candidate was a narrow cancellation-visibility reorder for a pending invitation that reaches the player's scene at an exact action boundary. | Withdrawn from upstream PR preparation after discussion. Local commit `edcc951b5` is one file and one visibility rule, but the player impact is minor and the proposed exact-24-minute route shows how narrow the window is; further capture and PR work are not worth the cost. |
| Signed pain routing | Common settlement routes negative pain into negative psychological pleasure, while direct positive-pain effects bypass the same enabled conversion. | Complete and published for review. The two-file candidate uses a pure destination/value router, passed 27 focused local tests, and has inspected real Tk A/B evidence plus fresh code/artifact review. Commit `21261e951` is open as upstream PR [#212](https://github.com/Godofcong-1/erArk/pull/212). The accepted Tk evidence was captured against the same proposed production diff before the final parent-only rebase; no post-rebase Tk replay is claimed. The Windows workflow completes build, packaging, and artifact upload, then fails only when the fork PR tries to create an upstream release with `Resource not accessible by integration`; this is a publication-permission failure, not a candidate build failure. |
| Sleep-path hypnosis sub-state cleanup | Sleep effect 489 clears `pain_as_pleasure` even though direct cancel preserves it; an earlier candidate also incorrectly treated generic `npc_active_h` as hypnosis-owned. | Complete and published for review. PR [#213](https://github.com/Godofcong-1/erArk/pull/213) extracts only the four assignments already common to both paths, removes the sleep-only `pain_as_pleasure` clear, leaves `npc_active_h` and path-specific logic untouched, and has inspected sleep-exit Tk A/B evidence plus `fable-5` and fresh artifact review. |
| Discovery settlement ownership | One panel serves an NPC caller with an outer settlement and a direct hidden caller without one. | The four-file exact-once owner remains the candidate boundary. The later hidden-session teardown is rejected: current upstream already prevents the same witness from repeating, while another eligible witness discovering the same encounter is allowed gameplay rather than a defect. Withdraw the five-file visual package and redo current-upstream evidence around the missing or duplicated discoverer reaction only. |
| Current group membership | Tired survivor classification counts every healthy scene resident, so a non-H bystander can drive the current group reduction. The candidate's membership query fixes that clue, but its one-survivor behavior has no transition effect and simultaneous unavailable members are filtered without all being settled. | Blocked on a confirmed candidate defect and unresolved gameplay semantics. Group reduction must move out of re-entrant per-character fatigue checks into one scheduler-epoch plan; zero-survivor desire handling requires user discussion before implementation or images. |
| Atomic declared-new registration | `type: new` publishes to the loader registry before its `register_to` target succeeds, then swallows target errors and reports the mod loaded. | Withdrawn from upstream PR preparation. The root cause and narrow declaration-level fix are understood, but no direct, decisive Tk evidence exists; the available indirect fixture is not worth the capture and review cost for this small loader defect. |
| Tired group exit | The fatigue check can schedule an exit that later H-state handling replaces with waiting, but the rejected candidate has no reliable current-member source and can submit an NPC exit after nested group transitions have already changed the scene. | Rejected pending redesign. Define current membership and the owner of zero-member, one-member, and continuing-group transitions before any replacement implementation or image capture. |

Movement-talk, type-1 ordering, and Tk queue scrolling were implemented before this design gate was made explicit, so their first production edits were treated as disposable hypotheses. The completed second audit started from production data flow, compared smaller and deeper boundaries, and produced the classifications recorded in the ledger and task 8.5 rather than trusting the original drafts.

Movement-talk pre-implementation boundary record:

- **Violated rule:** ordinary format templates retain the caller's actor; only a standalone, registered common-talk token may select the common-talk actor context.
- **Owner:** one private parser in `Script/Design/talk.py`, shared by `handle_talk_draw()` and `code_text_to_draw_text()` instead of two brace-shape guesses.
- **Rejected smaller patch:** special-casing `move` or counting braces leaves sibling templates and rule drift intact.
- **Rejected wider refactor:** a structured talk-selection object would remove string inference entirely but would migrate too many callers for this defect.
- **Required proof:** a production-reachable standalone token, a real NPC-capable non-movement sibling, malformed/unknown token inverses, and unchanged Tk/Web-independent formatted output.
- **Non-goals:** common-talk premise calculation, target mutation, event routing, and a wholesale talk result model.

Movement-talk runtime evidence and PR-completion plan:

1. **Freeze the candidate boundary.** Record `upstream/master` as the baseline, candidate `6a8547f7` as the proposed production change, the exact Python version and Tk renderer, enabled mods, and current worktree state. Apply cross-platform-save PR commit `2dd4e9d6b` identically to both local evidence runtimes when loading a Windows checkpoint; it is an evidence-environment overlay and SHALL NOT enter the movement-talk proposed diff. Treat the existing untracked tests and every `/tmp` artifact as local-only unless deliberately added to the proposed diff. Retire the invalid Doctor-room route and its frames from all PR-facing material.
2. **Explore before claiming a route.** Start from copied, otherwise untouched saves loaded through the shared cross-platform-save overlay when required, and use the real Tk interface manually. A trial may consist of only a few player actions. After each action, record game time, player scene, relevant NPC scene, visible behavior/talk, and whether a higher-priority need, work, entertainment, admission rule, or route cancellation won. Failed trials are evidence about scheduler reachability, not failed screenshot attempts. Use those observations to choose the next public destination, NPC, time window, or normal player action.
3. **Keep exploration bounded and truthful.** Prefer a public scene, a short route, and an NPC whose immediate need/work chain is already complete or naturally carries the NPC to the destination. Recall/follow is optional; a normal scheduled arrival is equally valid. Do not edit NPC behavior, position, hunger, target, route, talk weights, or completion state to manufacture the case. A checkpoint save may be copied after reaching it through normal play.
4. **Control the full random environment.** Use the same interpreter, set `PYTHONHASHSEED` before interpreter start, then seed Python `random` and NumPy immediately after loading the checkpoint and before the first recorded player action. Apply the same local evidence-only launcher and seed hook to baseline and candidate. The hook may set random state but must not operate the UI or mutate gameplay state. Record the values and prove on two baseline repetitions that the route, scheduler choices, and selected arrival template repeat. A process-start random seed alone is insufficient if startup consumes random values before the checkpoint.
5. **Promote only an observed case.** A route becomes the reproduction case only after normal scheduler execution reaches the chosen public scene, selects one affected multi-placeholder movement template such as `{NickName}来到了{SceneName}` or `{Name}来到了{SceneName}`, and repeats from the same checkpoint with the same actions and random environment. Static path length and target eligibility alone do not satisfy this gate.
6. **Prepare the visual package.** Preserve pristine copies of the same checkpoint for untouched baseline and candidate, write the exact player-visible route from load through arrival, and give the route plus seed controls to a local visual subagent. The subagent captures the local Tk window, inspects the current pixels, chooses one next action, performs that action with local `xdotool`, and captures again before deciding further. Prerecorded coordinate lists, blind command batches, direct gameplay-state mutation, and every VNC/noVNC or network relay are prohibited.
7. **Capture and inspect A/B evidence.** Capture the minimum legible baseline/candidate arrival pair, plus preceding context frames only if needed to identify the scene and action. Re-open both images and verify the same save, time, scene, NPC action sequence, and arrival template. The intended changed field is actor attribution: baseline shows the player identity where the moving NPC belongs, while the candidate shows the actual NPC. Any other material divergence invalidates the pair and returns the work to exploration.
8. **Verify the proposed diff.** Run the focused formatter/classifier regression on baseline and candidate, decide explicitly whether the focused test belongs in the submitted diff, run syntax and diff checks, re-open `talk.py`, and review the exact `upstream/master...6a8547f7` boundary. PR prose may cite automated proof only when that proof is included in the proposed diff.
9. **Replace stale PR artifacts.** After the images and proposed diff are fixed, give `fable-5` at medium effort only the exact diff and PR-visible evidence. Require a Chinese title/body and evidence captions that explain the visible problem, cause, fix, and inspected A/B result without the invalid Doctor-room route, local paths, private trials, or unsupported test claims.
10. **Review, then stop at the publication gate.** Run the fresh-context PR-artifact review from the title, including visibility and cumulative-prefix ledgers, and revise through `fable-5` until `PASS` or a concrete blocker. Present the final local draft and inspected images to the user. Publishing images, pushing the branch, and creating or editing a PR remain three separate outward actions requiring explicit user authorization.

Tk evidence concurrency uses three bounded capture slots rather than one global lock. Each slot owns one isolated Xvfb display, one supervisor process, one candidate runtime sequence, and an owner record for the full process lifetime. Baseline and candidate for one PR remain sequential inside the same slot, while up to three unrelated PR evidence tasks may run concurrently. A pre-existing game not launched by the allocator consumes one slot until it exits, allowing migration without interrupting active agents. OpenSpec and `.codex/skills` remain single-writer coordination state in the main worktree even while candidate code and Tk evidence run in parallel.

Tk queue pre-implementation boundary record:

- **Violated rule:** a Tk consumer transaction owns automatic viewport movement; leaf renderers must not independently repeat the same scroll, and the consumer must not use concurrent `Queue.empty()` as a logical batch boundary.
- **Owner:** a bounded `main_frame` queue-drain operation using `get_nowait()` and a fixed maximum message count per tick. The drain alone tracks pending scroll and flushes at transaction end or before a viewport-changing non-scroll operation.
- **Rejected smaller patch:** deleting selected leaf `see_end()` calls or deferring an unbounded `while not queue.empty()` drain leaves sibling renderers, thread timing, and event-loop starvation unresolved.
- **Rejected wider refactor:** producer batch IDs or envelopes have no existing logical flush boundary and would require protocol and panel/flow migration far beyond this performance defect.
- **Required proof:** FIFO and one-scroll behavior for text/command/image-command runs; direct leaf inverses; clear, standalone-image, and actual text-trim barriers; fixed-cap and late/concurrent producer behavior; render/JSON/scroll exception behavior; Tk smoke evidence. Metadata operations that cannot affect the viewport are not new batch identities.
- **Non-goals:** Web rendering, input/wait semantics, manual-scroll locking, bad-message recovery, and unrelated tooltip or drawing refactors.

Tk font fallback has a clear owner but not yet a confirmed Windows cause. Core `load_local_fonts()` enumerates Tk named fonts, creates a named object whose requested family is `@<font path>`, and treats absence of an exception as successful file loading. Later widgets do not consume that named object; they independently request the configured family `等距更纱黑体 SC`. A real Linux Tk probe showed the create command succeeding while both the named font and a font requesting that alias resolved to `Noto Sans`. This confirms that the success criterion is invalid, but it does not prove the Windows fallback clue or the proposed Win32 repair.

The local mod points toward the platform mechanism but owns it in the wrong place. It calls `AddFontResourceExW(..., FR_PRIVATE, ...)` as an optional import-time side effect before the renderer is selected, so Web mode receives an unnecessary GDI mutation and disabling the mod restores the broken core claim. Its Linux runner uses fake GDI and its real Tk assertion returns early outside Windows. It also scans every supported extension, can add the same path again across calls, and does not establish that Sarasa was absent globally. A green local runner is therefore call-shape evidence only.

The preferred future boundary is a Tk-only bootstrap operation that resolves the explicit bundled `static/fonts/等距更纱黑体.ttf` from the source tree in development or beside `sys.executable` in the one-file package, registers it privately and idempotently before `root = Tk()`, retains it for the full Tk process lifetime, and verifies after root creation that `Font.actual("family")` case-insensitively matches an accepted internal name such as `等距更纱黑体 SC` or `Sarasa Mono SC`. Web CSS, generic third-party font discovery, `emoji.ttf`, global installation, widget-level retries, and a general asset framework are non-goals.

No font candidate worktree is approved yet. A faithful gate needs a clean Windows host without globally installed Sarasa; untouched upstream with the mod disabled must reproduce a non-Sarasa actual family, then development and real PyInstaller layouts must prove the candidate under normal and Unicode paths. Missing/corrupt resources must warn without claiming success or crashing; repeated registration must be idempotent; Web must make zero GDI calls; Full and Lite archives must retain the asset; and the globally installed inverse must remain unchanged. Until that matrix is available, the logical boundary is a candidate cause, not a verified fix, and `local_fontfix` remains enabled.

### 5. Introduce explicit lifecycle identities only where the audits found real consumers

Two different missing identities must not be collapsed into one generic token:

- **Player action window:** created by the character scheduler with an ID, start, end, and duration. Group masturbation and deferred edge policy are real consumers.
- **Input prompt:** created by core flow with an ID, kind, allowed responses, and one-shot state. Tk and Web responses must carry that ID.

The current use of `over_behavior_character` object identity as an action token and a 30 ms delay as an input token are implementation guesses, not contracts.

Alternative considered: keep separate global counters inside each mod. Rejected because they cannot prove retry, nested call, reload, or exception behavior and make cross-mod composition load-order dependent.

Movement planning has a narrower confirmed identity that can be repaired independently. `move_src` and `move_target` describe the last physically settled edge and remain live history for talk, events, and premises. `move_final_target` alone is the unfinished multi-edge route commitment. Entering H must revoke that commitment without erasing the settled edge; otherwise NPC continuation premises and the player movement loop can resume the pre-H route after the transition.

Two independent design traces selected an idempotent `cancel_movement_plan(character_id)` owned by movement code and called by the canonical false-to-true H transition plus any proven direct `is_h` writer. It clears only `move_final_target` and never writes WAIT or history. The player loop must re-read the commitment after each settled edge rather than rely on `move_stop`, whose only consumer is the player loop and whose out-of-loop writes can cancel a future unrelated route. Group mode alone is not a cancellation signal because remote invitees intentionally move while not yet in H. A save-visible route object, pathfinding changes, and copied whole-function wrappers are non-goals.

Hypnosis cleanup has a narrower confirmed invariant than the earlier broad candidate assumed. Sleep effect 489 and direct cancel share exactly four hypnosis sub-state assignments: `increase_body_sensitivity`, `blockhead`, hypnosis `active_h`, and `roleplay`. The accepted helper owns only those four assignments. Sleep no longer clears `pain_as_pleasure`; both paths leave generic `h_state.npc_active_h` untouched; unconscious matching, abnormal-flag recalculation, air-hypnosis cleanup, and residual settlement remain with their existing callers. Single/group sanity exhaustion, multi-target air position, and door provenance remain separate unresolved defects. The published slice must not claim to unify the complete hypnosis lifecycle.

Pain-as-pleasure has a separate signed-delta owner. Upstream common settlement incorrectly converts negative pain into negative psychological pleasure, while four direct positive-pain effects bypass conversion. The accepted contract already makes the raw flag authoritative, permits conversion while sleeping or unconscious, preserves requested-value cap records, and requires common repeated-instruction equivalence. Two independent traces selected a bool-returning router in `common_default`: it consumes only a positive final pain delta when the raw flag is active, applies the state-23 adjustment and an explicit common-path repeat factor, writes requested values to both existing record owners, and returns whether ordinary pain settlement must be skipped. Zero, negative, inactive, and common extra-feel paths remain upstream-owned. Effects 270/283/296 retain their original formulas and lack of death guards; effect 408 retains its fear, draw, counter, and death ordering while routing only pain. Positive input whose pleasure adjustment becomes zero is still consumed, matching the existing common recursion. A general state-settlement rewrite and copied per-effect formulas are rejected.

Prompt identity is confirmed missing in both renderers: Tk uses one untyped FIFO and Web uses process-global response slots that accept values without an active prompt ID. Production probes reproduced stale, duplicate, wrong-kind, concurrent, and cross-client consumption. A renderer-neutral one-shot prompt registry is the preferred owner, but even a wait-only vertical slice changes Web protocol atomically and cannot accept ID-less compatibility responses. Implementation is blocked until disconnect/reconnect, multi-tab authority, panel/load/skip cancellation, concurrent instruction, and dialog ownership semantics are decided. The 30 ms queue drain and wait wrappers remain local mitigations, not upstream designs.

### 6. Make NPC preconditions return one transition decision

Current NPC pre-checks can overwrite a behavior chosen by an earlier check. This connects two apparently different symptoms: a running group masturbation behavior being changed to `WAIT`, and a tired group-exit behavior requiring manual re-settlement in the edge mod.

The scheduler should evaluate preconditions into one prioritized transition decision, then commit that transition and its settlement owner once. Individual checks should not mutate behavior opportunistically and then rely on later wrappers to restore it.

This scheduler work is shared infrastructure, but the gameplay policies remain separate tests and commits.

The first confirmed scheduler slice is tired group exit. The tired guard configures the five-minute `GROUP_SEX_NPC_HP_0_END` behavior, but configuration does not execute its four-effect cleanup chain. Because the scheduler ignores guard return values, the later H guard overwrites it with `WAIT`, and the normal NPC dispatcher never commits the exit. Two production-function probes selected a narrow decision returned only for this configured transition. The scheduler owns `judge_character_status()` exactly once, skips only the remaining pre-behavior guards, then continues realtime, persistent-state, interruption, time-over, talent, and completion processing. Settling inline inside the tired guard is rejected because the same guard is called from state settlement and would create re-entry; converting every guard to a pure decision is too broad.

The first implementation candidate at `e4823cb62` is rejected pending redesign. Its zero-remaining-participant branch calls the real group-end instruction and then commits the NPC exit. Group end already advances a nested five-minute scheduler epoch and settles scene-wide growth, H reset, clothing, insertion cleanup, and mode shutdown; replaying the NPC exit repeats growth/cleanup entry points and resumes outer tail phases against the stale pre-nested time and completion set. Stubbed group-end tests did not represent those effects. Zero participants must use group end as the sole lifecycle owner; whether fatigue additionally zeros the last NPC's desire is an unresolved gameplay choice, not permission to replay the whole NPC-exit chain. The redesign must also account for the three HP/MP settlement callers that currently invoke the mutating tired check and ignore its returned decision.

Further production probes show that this is a batch and epoch problem, not a missing boolean return. Low-level HP/MP settlement can advance time through a nested group-end update, reset the outer completion set, and resume the old frame against the new time. Two exhausted NPCs plus one survivor can also settle narration-only behavior 375 twice because it neither closes group mode nor provides a stable reduction identity. The eventual owner must make low-level settlement record only tired facts, derive one group exhaustion plan from a participant snapshot, and let the current scheduler epoch return a continuation before any new five-minute epoch begins. That implementation is blocked until gameplay decides zero-survivor desire handling, whether 375 becomes a real transition out of group mode, simultaneous follow-plus-H priority, and whether already-tired participants are intercepted before the current player window.

Participant identity is a separate owner and may be fixed independently. A reproduced sibling failure retargets the player to a healthy non-H bystander because the tired guard counts all healthy scene residents. Two independent traces selected a no-argument group-sex-owned `get_current_group_sex_npc_ids()` query: current admitted membership is the conjunction of active group mode, the player's current scene, and NPC `sp_flag.is_h`. Body templates are action layout, `go_to_join_group_sex` is pending admission, and player target is only focus. The tired caller must first prove that the triggering NPC belongs to this set, then keep fatigue eligibility caller-owned while applying its full existing exhausted rule, including tired level. This first consumer may fix participant selection only; it does not own duplicate 375, its no-op transition, exit submission, or nested group-end scheduling. The current candidate violated that boundary by selecting 1/0 transitions inside the re-entrant tired guard, so it is not a valid membership-only slice. Group bonuses, type-3 AI, group-end scene effects, and stale-template cleanup are recorded sibling consumers with different or unresolved semantics and are not silently migrated.

Group masturbation shares the missing action-window identity but not the same behavioral contract. Production can route and settle the same automatic intent repeatedly in one player catch-up window. A stable `PlayerActionWindow` with per-actor claims is the preferred eventual owner, but implementation is blocked until the 60-minute frequency/duration rule, unavailable-target retry, and nested-window behavior are explicit. Type-1 template membership and pending-edge exit settlement remain separate policies.

2026-07-18 re-audit correction: the repeated settlement is not reachable through normal group-sex play. Every group-sex/H player instruction, including `RUN_GROUP_SEX_TEMPLE`, resolves to a 10-minute window (`chara_handle_instruct_common_settle(... duration=10)` → `game_update_flow(10)`), and the auto-masturbation state machine is also fixed at 10 minutes, so a single click settles the intent exactly once. Duplication requires a single window longer than 10 minutes co-occurring with active group-sex masturbators; no group-sex instruction produces that, and the player cannot pick a >10-minute non-H action while `is_h` in group sex. The only path to a longer effective window is a nested `game_update_flow` firing mid-click (e.g. a participant's fatigue group-end update resetting the completion set and re-advancing time), which is a compound edge case that was not tied to a concrete reachable normal-play sequence. Per the user's "not reachable ⇒ do not fix" decision, the `local_group_masturbation_intent_fix` component was removed from `main` (commit `19c78b149`) and no upstream fix was pursued. Tasks 4.1a/4.1b/4.3/4.5 are closed as won't-fix; the previously-considered per-character-flag fix (branch `fix-group-masturbation-intent`, since deleted from `origin`) was correct and passed independent review but addressed only this unreachable condition.

### 7. Separate H settlement calculation, commit, and presentation

The orgasm work is not one bug:

1. A narrow duplicate-calculation defect in ordinary failed edge settlement.
2. Re-running detection against an already-consumed cumulative change object.
3. The absence of counted second-behavior events and an atomic commit result.
4. Presentation choices such as compact output, remote visibility, and representative text.
5. A gameplay policy that defers edge judgment to the end of a player action window.

Only the first item is currently confirmed as a narrow correctness candidate. The caller retries the same normal/extra delta after `orgasm_settle` has already advanced levels and partially filled the edge ledger, which replays earlier parts, can drop uncounted work, and leaves released ledger entries live. Two independent traces selected one call-owned state machine inside `orgasm_settle`: materialize per-part work once, roll edges until the first failure, then release the prior ledger plus failing and later parts exactly once, clear the ledger, and return an explicit outcome so the caller never retries. Preserve state `2`, because existing release premises consume it; resetting release state is a separate semantic question. Presentation, action-window policy, explicit effect 526, and full transaction modeling are non-goals.

The effect-526 repeated-detection clue remains blocked. The ordinary second-effect pipeline deliberately allows newly generated pleasure to feed later detection, so suppressing a second climax from the same cumulative change object would choose gameplay semantics rather than prove duplicate consumption. A later counted `OrgasmBatch` may own calculation and commit only after those semantics are decided. Exit finalization uses that interface. Presentation receives a result and cannot monkeypatch every draw/input function to suppress remote output.

Executable production-function probes now separate the two inputs. Recalling level-10 detection with an unchanged cumulative `CharacterStatusChange` re-adds the same delta, confirming that a presentation accumulator is incorrectly acting as consumable input. But release derivatives such as `b_orgasm_to_milk` and `u_orgasm_to_pee` add fresh B/U pleasure before the normal closure, and that new delta can legitimately cross another threshold. A same-object marker suppresses both cases and therefore cannot be the owner. The upstream 0/1 second-behavior map also collapses identical occurrences while duplicate must-settle entries preserve occurrence intent; the local counted batch chooses the opposite numeric policy without authority. On exceptions, upstream retries can repeat already-mutated effects, while both local mods clear queues and edge ledgers in `finally`, losing unfinished work. A claimed stale post-detection filter bug was not reproduced in current core because initialization and old-save migration prepopulate every configured second-behavior key.

No smaller behavior-changing candidate survives those counterexamples. The eventual orgasm module needs fresh deltas, counted occurrence identity, separate confirmed edges and unjudged window crossings, calculation/commit results, and a transition-supplied `finalize_pending_edges` call before summary/reset. It cannot promise blind retry until numeric mutation is separated from fallible talk/presentation. Implementation remains blocked on release chaining, identical-effect multiplicity, per-exit visibility or intentional discard, window-before-exit handling, and whether a failed finalization aborts, remains pending, or is explicitly discarded. The ordinary failed-edge candidate remains independent and does not claim this transaction.

Alternative considered: upstream the current batch component wholesale. Rejected because it copies the main behavior loop, temporarily replaces global UI and input functions, manually replays downstream phases, and silently includes gameplay changes not implied by the original bug clues.

### 8. Keep group admission and discovery settlement separate

Invitation cancellation and new-member admission are separate lifecycles. The investigation initially proposed treating a pending invitation as one owned operation whose flag, queued `be_invited_join_group_sex` text, travel start, cancellation, and group-ended arrival would be managed together. That broader contract was a design hypothesis, not a confirmed upstream defect.

The first lifecycle candidate was rejected after fresh review produced two counterexamples. Comparing `MOVE` plus `move_final_target` with the player's mutable position does not identify invitation-owned travel: a player move hides the real route, while an unrelated route to the same place is falsely canceled. A persisted route-owner redesign was also rejected after production tracing showed upstream cancellation already replaces the journey with WAIT, leaving no normal canceled route to resume. Do not add route identity for this clue.

The broader candidate at local commit `baabcfb4b` therefore kept ownership inside the pending invitation: start created the flag and acceptance text, clear removed both, cancellation preserved the existing WAIT transition, failed route creation rolled the invitation back, and group-ended arrival reused the local cleanup. Later review did not establish normal player-visible failures for the added queue cleanup, route-failure rollback, or group-ended cleanup, so those responsibilities were removed rather than upstreamed on the strength of local state tests alone.

The remaining candidate at local commit `edcc951b5` changes only the invitation panel: it checks an existing invitation before applying same-scene, implementation-value, and normal-state gates that belong to issuing a new invitation. Its code review passed, but the only proposed player route requires a movement finishing at an exact 24-minute action boundary before the next time-advancing action selects JOIN. After discussion, the user judged this cancellation-visibility window too minor to justify further runtime capture and upstream review. Keep the branch and investigation as local reference; do not resume evidence, prose, push, or PR work unless the decision is explicitly reopened.

Shared admission and arrival recheck are blocked rather than assumed. Existing upstream text establishes consent/implementation value at invitation time but does not define whether fatigue, normal state, implementation value, or all three re-evaluate on arrival, nor the rejection message, behavior, or second-talk cleanup. Adding only a target premise can strand the invitation flag with no matching transition. Do not create the evaluator until those semantics are authoritative.

Discovery settlement cannot be repaired by another global suppression set. A paired production-function probe now shows the same panel entering incompatible caller protocols: existing-group accept/refuse settle twice through the NPC state-machine caller, while initial group conversion settles the discoverer zero times through both callers and direct hidden deception also settles zero times. Nested player updates can erase the discoverer behavior before the outer scheduler observes it. The violated rule is that an explicit discoverer behavior must settle once before its player follow-up, independent of caller.

The first declarative `DiscoveryResolution` plan is rejected as too broad: it tried to encode player follow-ups and achievements yet could not represent “discoverer settled, follow-up failed” or partial-settlement exceptions. Two independent reviews instead selected a smaller dispatch result. The panel owns one-shot commit of every explicit discoverer behavior and records a frozen `DiscoverySettlementResult(discoverer_id, settled_behavior_id, replacement_behavior_id)` after successful settlement but before the existing player follow-up. Its state distinguishes not-started, started-or-failed, and successfully handled without inventing a retry transaction. The state-machine/find-target path passes only that exact type; the scheduler validates the discoverer ID, skips only the already settled behavior, and settles a replacement behavior produced by that commit only when it is still pending. Direct hidden discovery needs no separate caller protocol because the shared panel commit already settles the behavior. Settlement exceptions prevent follow-up and forbid reuse of the same panel instance; follow-up exceptions preserve the recorded result and do not replay discoverer settlement. Successful hidden/exhibition switches currently define no discoverer behavior and remain characterized, not silently repaired. Achievements, nested selectors, admission, witness choice, and later scheduler phases keep their existing owners and order.

The fixed-seed direct-hidden route later exposed a separate historical clue. Hidden-mode entry writes the same nonzero mode to player and target, while `settle_discovered()` clears only the player. On the pre-#206 base, the target's small-orgasm second effect 411 can read that stale flag, re-enter hidden discovery during the same player settlement, and select the same witness again because that selector did not read `see_pl_h`. The repeated same-witness frame remains a useful record of the old defect that upstream PR #206 subsequently fixed.

The proposed extension in `hidden_sex_panel.py` is rejected after the gameplay rule was clarified. Its shared selector and paired teardown prevent a different eligible bystander from discovering the encounter after the first witness, but that sequence is allowed. Static state asymmetry is not enough to redefine discovery as a one-witness session. Keep the rejected implementation and its tests only as local investigation history; do not include `hidden_sex_panel.py`, the second local commit, or the Nine-versus-no-second-prompt images in the upstream candidate.

Upstream PR #206 merged during this work as commit `e8a865c4a` and is present in current `upstream/master` `06fc59c1e`. It owns the same-witness rule while the player has not moved. The corrected discovery-settlement candidate therefore uses the four-file production diff through local commit `5d360f71e`; local commit `e281ebdda` and the five-file package are rejected. The replacement A/B fixes Python `random`, NumPy RNG, and `PYTHONHASHSEED` identically before game startup and stops at the discoverer reaction: current upstream skips Closure's accepted dismissal and departure, while the candidate shows that complete reaction once before Dobermann's action continues. No later witness was advanced or used as evidence. The replacement Fable draft and fresh artifact review both passed for local review; publication remains separately gated.

The user later clarified that the desired strong package for the repeated-discovery issue is the same-witness case itself, not the separate four-file settlement-ownership result. Its canonical before frame shows Closure twice in one screen after the first response was accepted. The matched fixed frame from upstream containing PR #206 shows Closure first and Nine second: Closure is excluded until movement resets eligibility, while a different eligible witness remains allowed. The fixed-seed before/after package and its Fable draft passed fresh evidence and artifact review at `/tmp/erark-pr-images/discovery-settlement/repeated-witness-pr206-20260713/`; it documents the already-merged one-file PR #206 fix and must not be used to claim that the four-file ownership candidate fixed same-witness repetition.

### 9. Stop adding undeclared import-time monkeypatches

Several manifests declare `functions: []` while their scripts mutate functions, classes, and registries during `exec`. ModManager snapshots only manifest-declared mutations, so a partial installer failure can leave a failed mod active in part. Its replacement chaining also saves only the first original function, so later `call_original` calls can bypass earlier wrappers.

No new fix in this program should add that pattern. A temporary local mod must either declare every mutation through a transactional loader interface or remain isolated until replaced by a direct core fix. A loader transaction change is an enabling change, not part of any gameplay PR.

The enabled-mod inventory confirms that this is not a missing-manifest-entry cleanup. Four enabled mods mutate only their declared load surfaces, eight self-install Python or external-process changes during script execution, and one installs a delayed runtime patch. At least 89 Python writes are outside manifest declarations. The four valid `type: new` registrations must remain supported: `easy_mode.cheaper_room` and the orgasm batch component's three `second_behavior` hooks, which the group-edge component actively consumes. A bootstrapped real-loader smoke loaded all thirteen enabled mods successfully; this inventory therefore describes failure integrity, not a current startup failure or proof of any gameplay rule.

Real-loader probes split four independent defects. A failed script can leave undeclared module, class, and registry writes live; a data row merged before a later script failure survives even when the asset alias rolls back; a second replacement wrapper bypasses the first because both `call_original` calls jump to the first core implementation; and a `type: new` entry aimed at a missing `register_to` module is retained in `_mod_functions` while the mod is reported successfully loaded. These do not share one honest small transaction boundary.

The last defect has a narrow owner-level invariant that does not depend on gameplay or local `main`'s later snapshot support: one declared new-function registration with `register_to` has two publication surfaces, and either both must contain the new callable or both must retain their prior values while the mod load fails. The local candidate resolves the target before mutation, treats module assignment failure as an exception, and locally restores both the prior module attribute and prior internal registry entry on partial failure. Registry-only `type: new` entries remain unchanged. Existing collision behavior for successful registrations remains unchanged. Arbitrary script effects, data merges, class/registry self-installers, dependency skipping, unload/reload semantics, and wrapper composition are explicit non-goals.

The reviewed candidate at local commit `8d5a582e3` records the known narrow fix, but the user decided not to file an upstream PR for it. The real Mod details panel rescans definitions when opened and discards the startup load result, so the baseline and candidate cannot be truthfully distinguished there; console output cannot substitute for game images, and the available fixture shows only an indirect downstream gameplay effect. Keep the diagnosis and candidate as local reference, and do not resume capture, PR drafting, or publication unless the priority is explicitly reconsidered.

A future loader transaction remains conditional on a retained runtime mod needing further development. Its honest boundary is only loader-registered staged operations, not arbitrary Python `exec`. The smallest credible design validates a complete plan before commit, journals loader-owned attribute/mapping/set/asset operations, reverses applied operations in strict reverse order, and gives composable wrappers an explicit lexical `next_call` without redefining legacy `call_original` base semantics. `group_sex_extension` is the preferred future canary because it is a retained feature with registry installation, while temporary bugfix wrappers should continue shrinking through direct core fixes. This larger infrastructure change is not approved for implementation in the current candidate.

### 10. Verify the real causal radius

Each workstream needs:

- a red check using the real input or state path, not a fabricated helper protocol;
- the original clue and every sibling entry/cleanup path found during tracing;
- inverse cases whose behavior must not change;
- independent loading with unrelated local mods disabled if a mod remains;
- real loader composition for any wrapper or registry mutation;
- Tk and Web checks for input, panels, waits, or visible settlement;
- explicit retry and exception cases for state that must not be lost before commit.

The `local_npc_move_talk_context_fix` test is the regression-design counterexample: it proves an invented `{move}` protocol rather than the move templates used by the game.

### 11. Keep PR claims inside the proposed diff

Investigation evidence and PR evidence are different artifacts. A local test, probe, benchmark, worktree, OpenSpec note, agent verdict, or temporary output can guide a fix without becoming visible to an upstream reviewer. A PR draft or PR-facing evidence file may name an automated test, command, count, result, or test-derived conclusion only when that test logic and every required fixture are present in the proposed diff. Renaming a local test as a reproduction or script does not change this boundary.

Every candidate now passes through the separate `review-erark-pr-artifacts` skill. PR-facing prose and every revision must first be authored by `fable-5` at medium effort; the reviewer then builds a visibility ledger from the exact base/head diff and checks the Chinese draft and intended evidence without using private investigation narrative to fill gaps. Local-only material is removed rather than relabeled. Every behavior-changing fix requires inspected comparable before/after images from one representative real Tk case; there is no non-visual exemption, but sibling cases do not each need separate images. Images awaiting user-authorized publication may support a local-review-ready result after inspection, while publication-ready status requires approved public URLs. No audit may upload evidence or edit an existing upstream PR.

The user-facing HTML review bundle is a readiness artifact, not a blocker dashboard. It includes only candidates whose representative Tk sequence has been inspected, whose current PR-facing prose was written by Opus, and whose fresh-context cumulative-prefix audit passed. Blocked investigations remain in OpenSpec and private evidence records rather than filling the review page.

The authoritative audit set contains only the twelve drafts newly created by this workstream: nine currently blocked on evidence or semantics, two blocked on confirmed candidate defects, and one rejected pending redesign. PRs the user already reviewed and opened upstream, their local draft copies, superseded copies, and handoff notes are excluded. A blocked candidate must remain labelled blocked after artifact cleanup; prose quality cannot promote an unconfirmed behavioral contract.

Candidate PR diffs are production-only (user decision, 2026-07-12). Upstream has no `tests/` directory and its CI does not run pytest, every PR the user already opened upstream is production-only, and a several-hundred-line test file cannot be meaningfully human-reviewed there. Each candidate's regression test therefore stays in its worktree as an untracked local verification artifact. Under the visibility rule above this makes every test name, pytest command, pass/fail count, and test-derived conclusion local-only: PR drafts and PR-facing evidence must instead use repeatable player flows, inspected before/after images, and only the minimum exact state assertions needed to explain what those images cannot expose internally.

## Risks / Trade-offs

- **[Large refactor temptation]** Shared missing ownership can encourage one giant PR -> land owner primitives and one behavior migration at a time; keep each player-visible contract independent.
- **[Deleting local protection too early]** Some complex mods currently prevent known crashes -> keep them locally frozen until an equivalent direct path passes the original reproduction.
- **[Green tests encode the patch]** Existing fake-module tests can reinforce a wrong path -> require at least one real-input or near-real regression before migration.
- **[Unresolved gameplay semantics]** A refactor can silently choose behavior frequency, multiplicity, or visibility -> record the choice and obtain user confirmation before implementation.
- **[Concurrent PR overlap]** Active agents may modify nearby specs or source -> preserve the coordination exclusions and use clean worktrees for each eventual upstream fix.
- **[Loader debt]** Direct fixes will take time while import-time monkeypatches remain fragile -> no new undeclared patches; add loader transaction coverage only as a separate enabling change.

## Migration Plan

1. Keep one local `main` integration branch with the assumed-upstream overlays and no duplicate mod responsibilities.
2. Create one linked worktree from current `upstream/master` for each direct candidate; never create an independent PR clone.
3. Prepare the first clear candidates in parallel: real movement-talk token classification, type-1 group-AI ordering, and Tk queue scroll coalescing.
4. For each candidate, finish red/green tests, evidence, local PR draft, and fresh-context review before presenting it to the user; do not push or publish.
5. Preserve remaining local protections and record failing-first reproductions for each deeper workstream. Do not delete a protection solely from this static audit.
6. Add owner-level state operations for movement and hypnosis, then migrate one caller at a time. Move hypnosis-cancel cleanup out of the pain component.
7. Add the shared signed pain-delta settlement path and migrate common and direct writers under the already accepted pain-as-pleasure contract.
8. Add explicit action-window context and one-transition NPC scheduling, then replace group masturbation and tired-exit wrapper state.
9. Fix the two narrow orgasm correctness defects, then add the orgasm transaction and edge finalizer before removing the batch and edge mods.
10. Design and implement the cross-renderer prompt protocol as its own change. Only then remove the frozen settlement-input mod and related experimental core protocol edits.
11. Integrate verified private font registration into Tk bootstrap after Windows proof, then remove `local_fontfix`.
12. After each stream, disable only the replaced mod responsibility, rerun focused plus sibling tests, inspect Tk/Web evidence where applicable, and update migration documentation. Roll back one stream by restoring its mod responsibility, not by restoring the monolith.

## Open Questions

1. Should a 60-minute player action create one 60-minute group masturbation action or repeated shorter actions?
2. If the same orgasm second-behavior ID is generated multiple times in one transaction, should its numeric effect apply once or once per occurrence?
3. Which pending-edge exit reasons settle visibly, settle silently, or intentionally discard state after leaving the player context?
4. When hypnosis type `0` requires manual choice, what should happen for group hypnosis targets that cannot open an individual selector?
5. What is the accepted Windows evidence matrix for private font registration in development and packaged builds?
6. Which prompt kinds share one response-generation contract, and which cancellation/reconnect semantics should Web expose?
7. When a tired group batch has zero survivors, should full group end keep normal desire handling or hard-clear desire for every exhausted leaver?
8. Should `GROUP_SEX_TO_H` remain narration while group mode stays active, or become the real transition that closes group mode and clears its action template?
9. When the same NPC is both following and in H, should one fatigue checkpoint only stop following or also exit H?
10. Should participants already tired before a player action be intercepted before that action, or should the player-first window remain unchanged and exit them only before the next normal action?
11. May fresh pleasure generated by a release derivative trigger another climax in the same closure, and if so does the closure run one generation or to a fixed point?
12. Should repeated identical orgasm behavior IDs apply numeric effects once per occurrence or collapse all semantics to one while retaining only repeated presentation?
13. When pending-edge finalization fails, should the owning exit abort, remain pending, or explicitly discard the ledger with a recorded reason?
