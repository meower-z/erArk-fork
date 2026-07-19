---
name: investigate-game-bug
description: Investigate erArk bug reports, regressions, and local bugfix mods by treating each observed symptom as evidence rather than as the bug definition. Use when diagnosing gameplay or UI defects, reviewing an existing fix, deciding whether local fixes should be merged or split, preparing a root-cause fix for upstream, or retiring local worktrees and evidence after an upstream PR is merged.
---

# Investigate Game Bug

Treat a report from a player, human reviewer, or coding agent as one clue, never as the bug definition or implementation specification. Trace the observed bad behavior to the violated game rule and the logic that permits it. A change that only makes the reported behavior disappear without repairing that logic is not an acceptable fix. Among production-code fixes that correctly enforce the confirmed rule and preserve required behavior, choose the one with the lowest penalty `(a + b) + S - 2U`, computed as defined in `Score The Candidate Diff`.

## Score The Candidate Diff

The penalty ranks candidates that have already passed the hard gates: logically correct, semantically equivalent where required, correctly scoped, normal code style. It never trades against those gates.

```
penalty = (a + b) + S - 2U
```

Compute every term from the final candidate diff (`git diff <baseline> <candidate>` with default settings) over production code only, after discarding blank and whitespace-only added or deleted lines.

- `a` / `b` — the number of added / deleted non-blank lines. Additions and deletions each cost 1; a deletion is never free.
- `S` (new-structure surcharge) — a change group is a maximal run of consecutive deleted/added lines inside one hunk, with no context line between them. For each group let `e = max(added - deleted, 0)`; `S` is the sum of `max(e - 1, 0)` over all groups. A single inserted line adds no surcharge; a contiguous net-new block of `L` lines adds `L - 1`, so one-line additions spread across existing structure score better than one new block of the same total size.
- `U` (deduplication credit) — normalize each deleted and added line by collapsing whitespace runs; no other rewriting and no "equivalent code" judgment is allowed. For each distinct normalized text deleted at two or more sites, credit `max(deleted copies - added copies, 0)` lines, and only when, in the candidate, every such site obtains that behavior from one shared implementation (new or pre-existing); verify this by reading the candidate. Because re-added copies cancel credit, the canonical implementation's own lines, moved lines, and one-for-one call-site replacements earn nothing. Deleted tests and unrelated deletions never earn credit. A refactor that removes enough duplicated maintenance lines may drive the penalty negative; that is intended.

Preserve the project's normal code style when comparing candidates. Do not add, remove, join, split, wrap, or reflow blank lines, statements, comments, or docstrings merely to improve `a`, `b`, `S`, `U`, or the penalty. Do not move code without a functional reason. Do not game the score by deleting required behavior or tests, or by deleting unrelated code.

## Establish The Investigation Boundary

1. Read the named handoff, the owning `.scratch/` ticket/spec, mod README, and actual implementation before forming a theory.
2. Check the current branch, dirty files, worktrees, and active related tasks. Do not overlap a fix or PR already owned elsewhere.
3. Inventory active upstream PRs that replace an in-scope mod responsibility. For an assumed-upstream development baseline, record each exact PR commit, apply it to core first, and disable the matching mod responsibility so a wrapper cannot hide whether the core fix works.
4. Record the exact source revision, enabled mods, renderer, save or fixture, and player-visible symptom.
5. Separate four statuses: reported clue, reproduced failure, confirmed cause, and verified fix. Never collapse one into another.

## Isolate Every Upstream Candidate

Prepare each upstream candidate in a new linked worktree owned by the main erArk repository. Fetch current `upstream/master`, create one `codex/<candidate>` branch from that ref, and use `git worktree add`; do not create another independent clone. Keep unrelated candidates, local integration commits, and central knowledge-base edits (`.scratch/`, `CONTEXT.md`, `docs/adr/`) out of that worktree.

The candidate worktree may contain only the intended public source/tests plus local untracked evidence needed to reproduce it. Knowledge-base artifacts (`.scratch/` tickets, `CONTEXT.md`, `docs/adr/`) and project-local skills under `.codex/skills/` are shared coordination state: edit them only in the main worktree on branch `main`, never from a candidate worktree, and serialize those edits so only one session writes them at a time. Store authoritative task status there. Never push, publish screenshots, or create/edit a GitHub PR without the user's separate authorization.

## Build A Red-Capable Reproduction

Create one deterministic check that fails on the reported behavior before studying fixes in detail. Prefer, in order:

1. A focused test through the real function and state path.
2. A near-real loader or save-based scenario with unrelated mods disabled.
3. A manual Tk and Web reproduction when the defect is renderer- or interaction-visible.

Assert the exact wrong state or output, not merely that the game does not crash. Minimize the setup until every remaining condition is necessary. If no faithful test seam exists, record that design problem instead of substituting a mocked test that cannot fail on the real bug.

Before accepting a patched branch, prove that production can emit the trigger value by tracing serialized data or configuration through its loader and caller into the patched function. Reject a test-only trigger protocol that no production path emits.

### Freeze Randomness In Runtime Evidence

When an A/B route contains a chance gate, freeze every project RNG before the first game import instead of retrying until the desired outcome appears. Use the same integer seed and the same evidence-only startup overlay in pristine baseline and candidate runtimes:

```python
if __name__ == "__main__":
    import random
    import numpy

    random.seed(EVIDENCE_SEED)
    numpy.random.seed(EVIDENCE_SEED)

    import auto_build_config
```

Place the seed calls before `auto_build_config` because startup imports and initialization may consume random values. Launch both game processes with the same explicit `PYTHONHASHSEED` in the supervised controller; this value must be set in the process environment before Python starts and cannot be repaired from inside `game.py`.

Keep this overlay out of the proposed production diff. Record the integer seed, `PYTHONHASHSEED`, overlay location and hash, baseline/candidate source refs, and pre/post save hashes in the local runtime manifest. Verify that both sides reach the same trigger after the same physical inputs. If the trigger character, trigger count, or pre-response frame differs, invalidate the pair even when both runs used the same seed. A fixed seed controls chance; it does not excuse different player actions, blind input, save mutation, or mismatched runtime overlays.

### Construct A Reproduction Save By Playing Forward

When no existing save reaches the trigger through a short route, do not conclude the behavior is unprovable and do not edit save bytes or inject state to fabricate one. If static tracing shows the trigger is reachable by ordinary play, build a reproduction save: start from an existing save and perform only normal player actions in the real renderer until the game reaches a state from which one short, replayable route triggers the behavior, then save to a **new** slot. This is legitimate precisely because every step is reachable gameplay; the forward-play is setup, and the trigger still occurs through the real production path.

Follow these constraints:

- **Normal actions only.** Reach the state by in-game player choices the renderer offers. Never hand-edit the save file, mutate runtime state before saving, or overwrite the original save. Write a new slot and keep the source save untouched.
- **Minimize the A/B route, not the setup.** Aim for a constructed save from which a **single** player action (often one wait or one interaction) fires the trigger, so baseline and candidate differ by the smallest possible input. Spend the length budget on the forward-play setup, not on the compared route.
- **Two distinct routes, recorded separately.** The *construction route* (source save → forward-play actions → new save) is provenance. The *A/B route* (new save → the one short action) is the evidence route replayed identically in baseline and candidate. Record both, and hash the new save; only the A/B route length is bounded by the comparability rules above.
- **Prove determinism from the new save.** With the frozen seed and `PYTHONHASHSEED`, confirm the new save plus the A/B route reproduces the same trigger character, count, and pre-response frame on repeat runs before using it for A/B. If the trigger depends on chance, the seed must pin it identically on both sides.
- **Keep it local.** Saves are never committed. Record the source save id and hashes, the exact forward-play action log, the new slot id and its pre/post hashes, seed controls, and the A/B route in the local runtime manifest. The reproduction save is local evidence provenance, not a PR deliverable.
- **Reachability blocker, not injection.** If forward-play cannot reach the trigger because the required state is genuinely unreachable by normal play from any available save, record a reachability blocker and stop. Do not substitute a hand-built or state-injected save to force the frame.

## Find The Root Cause

1. Trace every writer, reader, reset, and owner of the state involved in the clue.
2. Map the full lifecycle: entry, mutation, settlement, interruption, cleanup, serialization, and display where applicable.
3. Generate several falsifiable explanations. For each one, state what observation would disprove it, then test one variable at a time.
4. Search sibling paths and inverse cases. A cause is not established if it explains only the reported path while the same broken rule survives elsewhere.
5. Name the violated rule in one sentence and identify the function or module that should own it.

Call a cause confirmed only when it explains the original symptom, predicts nearby cases, survives counterexamples, and is supported by the red-capable reproduction or direct runtime evidence. Static code reading may produce a candidate cause, not runtime proof.

## Design supervision (Fable)

Fable (claude-fable-5) is the decision supervisor for this program. Invoke it exactly as:

```
claude -p --model claude-fable-5 --effort high --no-session-persistence "<prompt>"
```

**Skill loading (explicit, mandatory).** Codex MUST begin every Fable prompt with the relevant project skill slash invocation(s) — always including `/investigate-game-bug` for this program — before the neutral task payload. Keep Claude Code's normal tool access available; do not pass `--tools ""`.

**When to consult.** Consult Fable whenever direction is unclear, a difficulty changes the plan, evidence for a suspected bug is assembled, or a documentation artifact is ready for acceptance. Do not consult before gathering evidence: every prompt must supply verified facts, alternatives considered, uncertainties, constraints, and relevant artifacts. Fable may inspect referenced artifacts with its tools, but Codex must supply the verified facts rather than delegating the evidence gathering.

**Prompt discipline.** Write neutral prompts that do not steer toward a preferred answer. Resolve factual questions against primary evidence (code, logs, reproduced behavior), never by Fable's opinion; Fable cannot override verified primary evidence.

**What Fable decides.**
- Whether player-visible evidence is strong enough to convince a human reviewer that a behavior is a real bug worth fixing. If Fable judges evidence weak, it names the next evidence question or route; continue working — weak evidence is not a stop.
- Classification of locally patched behavior as bug fix vs. game-experience enhancement, proposal of fixes the user did not name, and PR task boundaries and priority — only when concrete evidence shows an effect on normal gameplay.
- Provisional gameplay semantics: Fable may pick the most likely reasonable semantics and authorize completing a local candidate under that choice. The user still gives final semantic confirmation before any upstream PR submission.
- Acceptance of all program documentation: task maps, evidence assessments, ticket problem/design/task records, PR-task boundaries. A document is not accepted until Fable passes it.

**Disagreement.** If Codex disagrees with a Fable verdict, send exactly one follow-up containing the counterargument and its supporting evidence. Fable's answer to that follow-up is final for reversible design and workflow decisions. Facts are never subject to this vote.

**Stopping rule.** Stop for player input only when a Fable verdict explicitly states that player input is required. In every other case, choose the next available task or investigation and proceed.

**Limits.** Fable cannot override user goals, safety rules, or repository rules, and cannot grant outward-action authorization — publishing assets, pushing, and creating or editing a PR each need their own separate authorization.

**Records.** Preserve every Fable prompt and verdict verbatim in the owning change's record.

## Approve The Boundary Before Editing Production Code

After the reproduction and cause investigation, stop before changing production code. Write a short design record that names:

1. the violated rule and its logical owner;
2. the current interface or state model that permits the failure;
3. two or more plausible correct fix boundaries, including the smallest direct fix, each with its `a`, `b`, `S`, and `U` counts and penalty `(a + b) + S - 2U`;
4. sibling paths the chosen boundary should repair, inverse behavior it must preserve, and explicit non-goals;
5. why the chosen boundary is the lowest-penalty candidate that is logically correct and correctly scoped, or why a user-requested refactor is appropriate.

For a non-trivial fix, give the reproduction, production trace, and design record to a fresh-context critic before implementing. Ask whether the chosen boundary is logically correct and correctly scoped, whether a correct candidate with a lower `(a + b) + S - 2U` penalty exists, and whether the fix changes public game semantics. Resolve actionable objections first. Production edits may begin only after the owning `.scratch/` ticket records the chosen boundary and unresolved semantic choices are either answered or declared blockers.

Reject a design whose contract is merely “the observed output changes from bad to good.” The accepted contract must name the violated rule, state where the fix enforces it, and explain why the same mechanism cannot produce the nearby failures found during investigation. Among designs that meet this contract, choose the one with the lowest `(a + b) + S - 2U` penalty; testing, evidence, and root-cause requirements are unchanged.

Tests and temporary probes may be written during investigation, but do not let an already-written patch choose the abstraction. If production code was edited before this gate, treat it as a disposable candidate and re-derive the boundary without assuming its shape is correct.

## Design The Preventive Fix

Choose a local refactor only when the user asks for one, when a narrow fix cannot correctly enforce the rule, or when removing enough duplicated code gives the refactor a lower `(a + b) + S - 2U` penalty than every narrow correct fix. Require a stable operation identity and defined nested or re-entrant behavior before using an exactly-once design.

When a refactor passes that gate, prefer:

- one shared predicate at the admission or premise owner instead of repeated caller filters;
- one lifecycle operation that starts, settles, and clears state instead of scattered cleanup hooks;
- a scoped temporary-context helper using `try/finally` instead of leaked global mutation;
- an explicit input generation or command identity instead of timing windows and queue drains;
- a narrow direct upstream change instead of a mod that copies or replaces an entire function;
- a returned result or explicit context object instead of hidden global flags when the surrounding code permits it.

Do not refactor merely to make the flow cleaner or more preventive. Keep a narrow fix when the owner is already clear and the current interface can enforce the rule; when existing casework has exactly one wrong case, prefer fixing only that case. Pause rather than silently deciding unrelated game semantics.

### Comment The Code, Not The Patch

Any comment a fix adds must explain the code as a permanent part of the codebase — what that code does and its role in the surrounding logic — read as if the diff never existed. It must not narrate the patch: no reference to what was changed, added, or previously wrong, and no reference to the bug, the old behavior, or "now also…", "to fix…", "avoid re-doing…", "already handled elsewhere". A future reader who never saw the diff must find every added comment accurate and self-standing. Describe the line's purpose and contract (e.g. "settle and apply the hypnosis state to the target per the current type; abort if it does not qualify"), not the reason it appears in this changeset. This holds regardless of comment language; the project writes comments in Chinese.

## Re-evaluate Existing Mod Boundaries

Do not preserve one-mod-per-historical-symptom boundaries by default.

For a multi-mod audit, freeze production edits while investigating, inventory every in-scope mod, and divide independent lifecycle or owner traces among reviewers using the output format below. Synthesize the results across mods only after each trace has identified its evidence status, violated rule candidate, owner, and unresolved semantics.

When an existing upstream PR is treated as accepted for local development, build and verify that overlay before regrouping the remaining mods. Retire only the exact responsibility replaced by the PR: disable or remove a whole mod only when all of its live behavior is covered, and strip a narrow wrapper instead when the mod still owns unrelated behavior. Keep each upstream commit identity and overlay rollback boundary distinct inside the single local `main` integration branch; do not create a separate `dev` branch solely for assumed-upstream work.

For every existing patch, compare three behaviors: the upstream revision it was written against, current upstream without the patch, and current upstream with the patch. Exercise at least an A/B matrix with the mod disabled, enabled alone, and composed with directly related mods. Record when the old base cannot be reconstructed instead of assuming the copied implementation still has the intended semantic delta.

Merge fixes only when they enforce the same behavioral contract, at the same logical owner, across one state lifecycle. Prove that contract through a coherent test matrix; choose code, commit, and PR boundaries separately from the number of test surfaces involved.

Split fixes when they have different owners or different failure mechanisms, even if they share a file, UI screen, character flag, or player report. Extract unrelated feature behavior from bugfix work.

For every runtime mod wrapper or function replacement, check:

- whether upstream already changed underneath a copied implementation;
- whether load order can bypass or double-apply the fix;
- whether a stable dispatch or operation identity exists across nested and re-entrant calls;
- whether exceptions restore temporary state;
- whether the mod imports optional systems or mutates registries at import time;
- whether the tests load the real mod independently;
- whether disabling unrelated mods changes the result.

Classify each current patch as retain, merge, split, replace with a direct fix, or freeze pending evidence.

## Verify The Causal Radius

Before calling the fix complete, test:

1. The original minimized clue.
2. Every sibling entry and cleanup path found during tracing.
3. Boundary and inverse cases that must remain unchanged.
4. The component with unrelated local mods disabled.
5. Real mod-loader composition when wrappers or registry patches remain.
6. Nested and re-entrant entry when the fix claims exactly-once behavior.
7. Tk behavior when the change affects input, waiting, panels, or visible settlement. Web checks are supplementary unless the PR itself changes Web behavior.
8. Inspected, comparable before-and-after images from one representative, easy-to-understand real Tk player flow for every behavior-changing candidate. One main case is sufficient even when the same fix covers additional sibling cases.

### Repeated H-discovery before-fix evidence hard gate

For a candidate whose claimed bug is that the same NPC repeatedly triggers `H中被发现`, before-fix player-visible evidence is valid only when one full-resolution static Tk screenshot visibly contains two consecutive `H中被发现` panels naming the same NPC. Both discoveries and the repeated NPC identity must be legible in that single image. A GIF, separate frames, scrollback showing different NPCs, logs, hashes, tests, or source tracing cannot substitute for this screenshot. If the screenshot cannot be obtained, mark the evidence invalid, withdraw every readiness claim, and stop publication work for that candidate.

Do not apply this repeated-discovery gate to a separately approved bug whose visible symptom is a missing or duplicated discoverer reaction settlement. That scope follows the normal requirement for inspected, comparable real-Tk before-and-after evidence showing the claimed reaction difference.

Re-open the changed source and confirm the rule is enforced at the intended owner. Review the final diff against the requested scope. Report which checks were static, automated, or manually observed, and list any unresolved semantic choice.

## Operate Tk Through A Local Visual Agent

Tk evidence is a same-machine workflow performed by a visual subagent. The established local toolchain is an isolated X display, the real Tk game, `xdotool` for one visually chosen action, ImageMagick `import -window` for capture, and `view_image` for pixel inspection. Do not expose the desktop through VNC/noVNC/Websockify, a browser relay, a tunnel, a host address, or any other network route.

Before building a controller, read [the known-good Tk evidence profile](references/tk-evidence-known-good.md) and start from its allocator, geometry, launcher, capture, and provenance settings. Vary only the task-specific runtime, save, route, seed, and evidence names.

1. Spawn a dedicated visual subagent with the candidate worktree, starting save, seed controls, target visible state, evidence directory, and stopping condition. The subagent owns interaction and reports a chronological action log; the root agent coordinates the A/B setup and reviews its output.
2. Use `scripts/tk_capture_slots.py run --owner <thread:candidate> --runtime <isolated-runtime> -- <command>` to acquire one of three capture slots. The supervisor allocates an isolated Xvfb display, records owner/PID/runtime metadata, and holds the slot for the entire command lifetime. Keep one candidate's baseline and candidate sequence inside the same supervised command. A game started outside the allocator reserves one slot automatically, so sessions already running under the legacy workflow are not interrupted or overcommitted.
3. Start `python game.py` through that supervised command and verify the Tk process and assigned window locally. Use `scripts/tk_capture_slots.py status` before launching or diagnosing contention. Capture the current Tk window with ImageMagick `import -window`; use the window id when possible rather than an unrelated whole desktop.
4. Open the captured PNG with `view_image` and inspect its actual pixels. From that current image, choose one next click, key, or text entry. Perform only that action locally with `xdotool`, capture the resulting frame, and read it before choosing another action. Shell access is the transport for these local tools, not a substitute for visual decisions.
5. Do not use a prerecorded coordinate list, blind coordinate loop, or batch of assumed game commands during route discovery. Coordinates are acceptable only when selected from the current inspected frame. If the screen differs from the expected state, stop the planned sequence and reassess from a new screenshot.
6. Explore normal player interactions until the agent understands a short, repeatable route. The route need not be guessed before opening the game. Record every visible state and failed reachability assumption; failed exploration frames are diagnostic material, not PR evidence.
7. Once the route is known, write it down and replay it from pristine baseline and candidate copies with the same save, seed, display geometry, and player actions. Capture the trigger frame as well as the visible result when both are needed to make the comparison understandable.
8. For text or effects that disappear before a static capture, record the local X display with `ffmpeg`, extract candidate frames, and inspect them with `view_image`. Contact sheets or crops may help locate the right frame, but they do not replace inspection of the final full-resolution evidence image.
9. Re-open every final image with `view_image`. Confirm the relevant text and state are legible, the A/B setup is comparable, and no unrelated local content is exposed. Use `identify` for dimensions and hashes for provenance or accidental-duplicate checks; a successful capture command or existing file is not image verification.
10. Stop the supervised command, let the allocator terminate its Tk/Xvfb process groups and release the slot, then confirm `scripts/tk_capture_slots.py status` no longer lists that owner. Record a tool, window, or route blocker instead of substituting a network relay.
11. Archive the retained images and videos plus the minimum replay package—action log, written route, runtime manifest, reproduction save or fixture, and overlay hashes—under `~/games/archive/erArk-upstream-pr-evidence/PR-<number>/local/<candidate>/`. When no PR number exists, use a dated task directory under the same archive root. Re-open the archived media and compare its hashes with the source files before treating the archive as complete.
12. After the archive verifies, delete every task-owned `/tmp` runtime directory and disposable capture directory created for the run, then confirm those paths are gone. Leave shared or unrelated temporary paths untouched.

## Write The Upstream PR Draft

Write erArk PR titles and descriptions in Chinese unless the user explicitly requests another language.

Do not author or revise PR-facing prose yourself. Use an Agent/Workflow writer with model `fable-5` and effort `high` for every title, body, evidence caption, and later prose revision. Give it the exact upstream diff and only evidence intended for the PR. Preserve its output for audit.

Before drafting, read [the accepted upstream examples](references/pr-draft-examples.md).

1. Assume the reviewer has played erArk but has not seen this bug. Name the exact feature and scene; do not introduce erArk or teach familiar gameplay systems.
2. Use existing game terms. A term used directly by the game code or dialogue may stand unexplained; otherwise define it before use or remove it. Never coin a label such as “自动发起 H” and present it as an in-game effect.
3. Explain the visible problem, confirmed cause, and final fix in that order. Every cumulative prefix must make sense without later rescue text.
4. Include only reasoning needed to understand the submitted fix. Omit rejected designs, private investigation, local-only tests, file lists, and standalone non-goal inventories.
5. For a behavior change, show one representative real Tk before/after image pair or GIF sequence. Keep the exact route, seed, and reproduction save locally; do not put a full reproduction packet or save download in the PR.

For every behavior-changing fix, prepare a reproduction save and short written player steps starting from load, then follow `Operate Tk Through A Local Visual Agent`. A fixed random seed may stabilize chance, but the visual agent still performs the player actions. Keep the save and full route local; publish only the images or GIF and the minimum text needed to interpret them.

Before calling the candidate ready for human review, invoke `$review-erark-pr-artifacts` with a fresh-context reviewer and give it only the proposed diff, reproduction, PR-facing evidence, and PR draft. Send actionable revisions back through `fable-5` at `high` effort. Stop when the skill returns `PASS` or exposes a concrete blocker that requires user input.

The draft is complete only after this review gate and after re-reading it as a reviewer to confirm that every sentence helps explain the submitted fix or its visible verification.

## Retire Accepted Upstream Candidates

Run this branch only after the user authorizes local cleanup. Resolve current PR state from `Godofcong-1/erArk`; treat only `MERGED` as accepted. Preserve every `OPEN`, closed-but-unmerged, no-PR, or otherwise WIP branch and its local files.

1. Inventory every linked worktree under `~/games`, recording path, branch, HEAD, dirty files, and matching upstream PR. Refresh GitHub state immediately before deletion instead of inferring acceptance from directory names, local ancestry, or an old handoff.
2. Inspect dirty files in each accepted worktree. Use `git worktree remove --force` only when the user's authorization explicitly discards those contents; otherwise stop before losing unique work. Remove the worktree through Git, then verify its path and registration are gone. Keep the local branch ref unless branch deletion was separately requested. Run `git worktree prune` only for registrations whose worktree paths are already absent.
3. Before stopping evidence processes, run `scripts/tk_capture_slots.py status` and inspect process CWDs and process groups. Terminate only owners or legacy processes whose runtime belongs to an accepted PR. Leave allocator owners, runtimes, and files for unaccepted or WIP work untouched.
4. Delete the accepted PR's numbered directory under `~/games/archive/erArk-upstream-pr-evidence/`, its exact task-owned `/tmp` runtimes, captures, logs, drafts, handoffs, and clean one-use assets clones. For a mixed assets clone, first prove that every unaccepted or WIP asset has another verified local copy; otherwise remove only the accepted subdirectories. Do not alter the remote assets branch, PR, or other GitHub state without separate outward-action authorization.
5. Update the archive index and checksum manifest to describe only retained evidence. Re-run every retained checksum, scan the archive and `/tmp` for accepted-PR paths, and re-read live PR state after cleanup.

Cleanup is complete only when no registered worktree maps to a merged PR, no identified local evidence for an accepted PR remains, retained evidence verifies, allocator status shows that WIP owners were preserved, repository working files outside the authorized targets are unchanged, and before/after `du` and `df` measurements quantify the result.

## Reclaim Stale Tk Temporary Storage

Run this branch only after the user authorizes local temporary-storage cleanup. It applies only to erArk task-owned paths under `/tmp`; it does not authorize deleting generic `/tmp` entries, system-private directories, or files owned by another project.

1. Set an inactivity cutoff from the user's instruction; use 120 minutes when they give no other value. A path is fresh when it or any descendant is newer than that cutoff. Before deletion, record `df -h /tmp`, top-level `du`, `scripts/tk_capture_slots.py status`, registered `/tmp` worktrees, and processes whose CWD or open descriptors point into `/tmp`.
2. Keep every fresh path, registered worktree, active allocator runtime or control directory, and path referenced by a live process. Do not infer inactivity from an `erark-*` name, a stale top-level timestamp, or a missing controller alone. Recheck freshness and process references immediately before deleting each target.
3. A dormant Tk runtime, control, capture, or frame directory may be removed only after identifying it as task-owned. If its exact runtime is still held by stale processes, inspect their CWD, PID, PGID, and task ownership first; terminate only that exact completed or accepted-task group. Never use a broad process-name kill, and leave WIP owners untouched.
4. Before removing a Tk target with extracted evidence, copy the evidence—not its full game runtime—into `~/games/archive/erArk-upstream-pr-evidence/PR-<number>/local/<candidate>/` or a dated task directory when no PR exists. Preserve screenshots or video plus available action log, route, manifest, fixture or save, and hashes. Keep the original basename, write a manifest with the cutoff and source paths, and verify source and archive hashes or a tree comparison. Do not mistake runtime resource folders such as `image/` for captured evidence.
5. After the archive verifies, delete the target runtime and its disposable captures. Verify that each intended path is absent, retained allocator owners and worktrees remain, archive hashes still match, and before/after `df` and `du` quantify the actual reclaimed space. Report permission-limited system paths separately instead of treating an incomplete `du` scan as a cleanup failure.

## Investigation Output

Leave a concise root-cause record containing:

- the original clue and minimized reproduction;
- evidence and rejected explanations;
- the confirmed or candidate violated rule;
- the current fix's failure mode;
- the chosen correct fix, its owner, and its `a`, `b`, `S`, `U`, and `(a + b) + S - 2U` penalty;
- merge or split decisions for related fixes;
- tests that can falsify the design;
- runtime gaps and coordination exclusions.

Do not propose a public PR until this record supports a narrow, independently testable behavioral contract.
