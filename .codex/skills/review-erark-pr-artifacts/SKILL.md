---
name: review-erark-pr-artifacts
description: Audit erArk upstream PR drafts and PR-facing evidence against the actual proposed diff and the repository's investigate-game-bug writing rules. Use before calling a candidate ready, when a draft or evidence file changes, or when checking for local-only tests, paths, investigation details, unsupported claims, and reviewer-hostile wording.
---

# Review erArk PR Artifacts

Act as a clean-context upstream reviewer. The proposed diff is the boundary of what the PR can claim. A local test, probe, screenshot, benchmark, OpenSpec note, agent review, or worktree fact is not PR-visible merely because it helped the investigation.

Read `.codex/skills/investigate-game-bug/SKILL.md`, especially `Write The Upstream PR Draft`, before reviewing. Its writing rules remain authoritative; this skill supplies the verification procedure.

## Build The Review Package

Require four inputs:

1. the candidate worktree and exact base/head refs;
2. the complete proposed diff, including submitted tests and generated-data changes;
3. the PR title/body draft;
4. every artifact intended as PR evidence, such as screenshots, interaction steps, tables, or state output.

Do not use private investigation narrative to make an unclear draft seem understandable. If the exact proposed diff cannot be identified, return `BLOCKED` rather than guessing which local files will be submitted.

## Build A Visibility Ledger

Inspect `git diff --name-status <base>...<head>` and classify every claimed proof before reading the prose sympathetically:

- **PR-visible implementation context:** relevant upstream-base code and proposed production changes.
- **PR-submitted automated proof:** its test or benchmark logic and required fixtures are present in the proposed diff.
- **PR-visible external evidence:** an approved artifact that is already attached or linked in the PR draft.
- **Pending-publication visual evidence:** an inspected local image or recording intended for the PR but not uploaded because publication still awaits user authorization.
- **Local-only:** absent test files, temporary probes, `/tmp` output, local worktree paths, unpublished commits or branches, OpenSpec notes, agent reviews, private benchmarks, and screenshots that will not be published.

For every command, count, screenshot, and behavioral assertion in the draft or evidence, record which ledger entry supports it. Unsupported items fail the review.

## Run A Cumulative Prefix Audit

A prefix is the cumulative text from the title through a given heading, paragraph, list item, or evidence block. It is not one isolated sentence. Read the artifact from the beginning and stop after every such boundary. Assume the reviewer has played erArk and knows its existing gameplay terms, but has not seen this bug or the proposed code.

For each prefix, record:

1. the new player concept, project term, identifier, example, or qualification introduced at that boundary;
2. where the preceding prefix already gave the reader enough context to understand it;
3. whether a later paragraph is being relied on to define, narrow, correct, or justify the current wording.

Fail the prefix when understanding it requires text that appears later. In particular:

- the title must state a player-visible problem or literal change without relying on an unexplained internal term;
- the opening paragraph must identify the exact feature or scene and the wrong behavior without explaining erArk or teaching familiar gameplay systems;
- a term used directly by the game code or dialogue may stand unexplained; any coined or private term must be defined before use or removed;
- cause and implementation terms appear only after the observed behavior they explain;
- an example cannot be the reader's first definition of a general rule;
- verification cannot introduce a new behavioral scope that the problem and fix sections never established;
- a later limitation or non-goal cannot retroactively make an earlier over-broad claim accurate.

After any edit, restart this audit from the title. A draft fails even when every individual sentence is grammatical if any cumulative prefix still depends on later rescue text.

## Audit The Draft

Apply every rule below:

1. The title and body are Chinese unless the user requested another language.
2. The body explains the user-visible problem, confirmed cause, and final fix in that order.
3. Every sentence is understandable from the upstream base, proposed diff, PR-visible evidence, and any inspected pending-publication visual evidence available at that point in the text.
4. Remove rejected designs, private deliberation, local branch/worktree details, agent activity, OpenSpec state, and file-by-file narration already visible in the diff.
5. Do not add a `修改范围` section that restates the diff.
6. Do not add standalone `不包含`, `非目标`, or similar inventories. Keep only a boundary required to make an adjacent behavioral claim accurate.
7. An automated test or benchmark may be named, counted, or quoted only when its test logic and required fixtures are in the proposed diff. Existing upstream tests and local tests are not exceptions. If the proof is absent from the diff, remove its name, command, count, result, and conclusions that rely solely on it from both draft and PR-facing evidence.
8. Do not convert a local-only test into acceptable evidence by calling it a reproduction, script, probe, or manual check. Visibility depends on what the PR includes, not the label.
9. A test included in the diff may support only the behavior its assertions actually inspect. Re-run it and verify any claimed count.
10. Every bug fix that changes game behavior requires one repeatable representative player flow and inspected, comparable before-and-after images from the real Tk renderer. One main, easy-to-understand case is sufficient even when the fix covers siblings. State assertions are supplemental. If the behavior needs several frames to expose the trigger and outcome, require the full sequence. If honest Tk images cannot show any representative changed behavior, return `BLOCKED`; there is no non-visual exemption.
11. Local image paths are allowed only as pending-publication placeholders and must be clearly excluded from copy-paste-ready PR text. Their exact images must still be inspected before a local-review-ready pass. A candidate becomes publication-ready only after user-approved public URLs replace them.
12. Confirm the PR-facing title/body, initial PR-evidence prose, and every later prose revision were produced by an Agent/Workflow writer using `fable-5` at `medium` effort. If not, return `BLOCKED` and require a Fable rewrite before continuing the prefix audit.
13. Confirm Tk evidence was produced by a local visual subagent operating the real window from a prepared save and written player route. The accepted workflow captures the current local Tk frame, inspects its pixels, chooses one next action, issues that action locally with `xdotool`, and captures again. Reject blind coordinate or command batches, direct gameplay-state mutation, VNC/noVNC, and every network relay.

## Audit PR Evidence

Treat a file named `evidence` as material intended for the upstream reviewer unless the user explicitly classifies it as a private investigation log.

- Keep only evidence that will accompany the PR and that a reviewer can interpret without local filesystem or conversation context.
- Remove local red/green logs, local-only test commands, private benchmark output, temporary probe paths, agent verdicts, and claims based only on them.
- Ensure before/after evidence uses the same save, Tk setup, written player route, and screenshot-led local visual interaction. A fixed random seed is allowed when it stabilizes chance.
- Reject diagrams, synthetic comparison cards, debug-only probes, console text detached from the game flow, and unrelated screenshots as substitutes for behavior evidence.
- Ensure screenshots show the relevant state legibly and do not reveal unrelated local or custom content.
- Ensure text/state evidence quotes only the minimum exact values needed to prove the submitted behavior.
- Do not require or publish a reproduction save or full reproducibility packet. Keep those local; the PR needs the inspected image or GIF evidence and only the short player flow needed to interpret it.
- If useful local investigation material must be retained, move it to a separately named private investigation record; do not leave it in the PR evidence artifact.

## Preserve Good Existing Prose

Before requesting a Fable revision, preserve the exact pre-review draft/evidence text and require Fable to produce a before/after diff. Tell the writer that artifact cleanup is surgical:

- delete or narrow the exact unsupported claim first;
- do not rewrite titles, headings, examples, reproduction steps, or surrounding explanations that already pass both audits;
- restructure prose only when the finding cannot be fixed locally, and state why the move is necessary;
- reject a revision that fixes visibility but makes any prefix less understandable, less concrete, or more dependent on project-private context.

The review report must distinguish deletions required by visibility from optional writing preferences. Do not apply edits yourself and do not send optional preferences to Fable during a compliance cleanup.

## Return A Verdict

Lead with one of:

- `PASS`: every claim maps to submitted material or inspected pending-publication visual evidence. Report `publication_state: local-review-ready` when approved uploads are still pending, otherwise report `publication_state: publication-ready`.
- `REVISE`: exact draft/evidence edits can resolve the findings without changing code or public scope.
- `BLOCKED`: the proposed diff or required publishable evidence is missing, or the draft depends on proof that cannot be made PR-visible.

List actionable findings by severity with artifact line references. Include the cumulative prefix ledger and the visibility ledger for every automated test, benchmark, screenshot, or external evidence item. Pending-publication images may support a local-review-ready `PASS`, but never a publication-ready one. When asked to fix the artifacts, send only the actionable findings and visible material to `fable-5` at `medium` effort; then inspect its before/after diff, re-open the files from the title, and run this review again with a fresh-context reviewer. Do not edit the prose yourself, push, upload evidence, or create/edit a PR.

Completion criterion: the final fresh-context verdict is `PASS`, or a concrete `BLOCKED` condition is recorded without calling the candidate ready.
