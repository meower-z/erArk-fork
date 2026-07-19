## Why

The remaining local bugfix mods were mostly divided by historical reports and patch points, so several now infer lifecycle boundaries through global flags, object identity, timing windows, or copied upstream functions. A report is evidence of a defect, not its definition; the remaining work needs to be regrouped around confirmed violated rules and the code that should own them.

## What Changes

- Require every bug investigation to distinguish the reported clue, reproduction, confirmed cause, and verified fix.
- Reject behavior-only patches derived directly from a reported symptom; require the smallest local refactor that centralizes the violated rule and prevents the same mechanism from producing sibling failures.
- Maintain one local `main` integration branch containing the assumed-upstream overlays, and prepare every new upstream candidate in a fresh linked worktree from `upstream/master` rather than another clone.
- Reclassify each remaining bugfix mod as retain, split, merge, replace with a direct fix, or freeze pending evidence based on its logical owner and invariant rather than its current directory or symptom label.
- Prefer a local refactor at the owner of the violated rule when that removes the mechanism that produced the reported and sibling failures.
- Replace timing-, load-order-, and object-identity-based lifecycle guesses with explicit action, settlement, state-transition, or input ownership where the audit proves that ownership is missing.
- Keep unrelated fixes separate even when they share a file or feature area, and require independent tests with unrelated mods disabled.
- Require every direct upstream candidate to leave a local PR draft, repeatable reproduction/evidence, and a fresh-context human-reviewability pass before it is presented to the user.
- Let chance-dependent player reproductions be discovered through recorded manual Tk exploration rather than guessed entirely from static routing, then freeze the successful save, action route, and complete random environment for comparable baseline/candidate evidence.
- Require a pre-implementation design gate: compare plausible boundaries, choose the smallest owner-level local refactor, and have a fresh-context critic challenge it before production code is edited.
- Preserve current active upstream work as coordination exclusions: commission display, cross-platform save paths, group-AI target restoration, hidden-sex witness deduplication, scene-wide premise loops, and time-stop instruction 5052.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-mod-componentization`: Strengthen root-cause evidence, local-refactor evaluation, component-boundary, and causal-radius verification requirements for bugfix work.
- `tk-font-registration`: Narrow the unproved generic font-scanning promise to the configured bundled Sarasa asset, Tk-only bootstrap ownership, resolved-family verification, and a required Windows development/package evidence gate.

## Impact

- Affects the remaining `mod/local_*` bugfix implementations, their tests, the Tk font bootstrap contract, and future direct upstream replacements.
- Adds a repo-local investigation skill and a root-cause consolidation plan; it does not itself publish, push, or modify any active upstream PR.
- Large runtime changes will be split into follow-on changes after each behavioral contract has a red-capable reproduction and a confirmed owner.
