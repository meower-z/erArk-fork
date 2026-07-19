---
name: rebase-fork-to-upstream
description: Rebuild the erArk working tree onto the latest upstream plus every currently-open proposed PR, keeping all local non-code (docs, knowledge base, .codex, personal mods), and reconciling each local bugfix-mod against its PR status. Use only when the user explicitly asks to rebase, resync, or reset the fork to upstream + open PRs.
---

# Rebase fork to upstream + open PRs

Rebuild the code onto `upstream/master` plus the heads of all currently-open PRs, while
preserving every local non-code artifact and pruning local mods that upstream (or an open
PR) now covers.

## Mental model

- `upstream` = `Godofcong-1/erArk` (read-only, default branch `master`). `origin` = `meower-z/erArk`.
- Local fixes ship as **runtime mods** under `mod/` (each a `mod_info.json` + `scripts/` that
  monkey-patch game functions via `Script/Core/mod_manager.py`). Most fix-mods were once proposed
  as a PR to upstream; personal mods (`easy_mode`, `local_fontfix`, `local_performance`,
  `group_sex_extension`) never were. `mod/semen_boost` and an empty `mod/mod_config.json` are
  upstream's own.
- `CONTEXT.md` + `docs/adr/` (domain knowledge) and `.scratch/` (local tickets/specs, see
  `docs/agents/issue-tracker.md`) are the local knowledge base tracking each fix and PR outcome.
  `mod/LOCAL_BUGFIX_MIGRATION.md` is the hand-maintained mod↔PR table — treat it as a lead, not
  ground truth; it drifts.
- Goal: **code** follows `upstream/master` + open PRs; **everything else local is kept**.

## Preconditions

- `gh` auth is often broken here. Do **not** rely on it. Read PR status from the GitHub **public
  API** (unauthenticated, ~60 req/hr): `curl -s https://api.github.com/repos/Godofcong-1/erArk/pulls/<N>`
  → `.state` (`open`/`closed`) and `.merged` (`true`/`false`).
- Never push. Never touch `upstream`. This skill only rewrites the local tree.

## Procedure

### 1. Fetch and classify PRs
- `git fetch upstream` (and `git fetch origin`).
- Enumerate the fork author's PRs on upstream (numbers appear in `mod/LOCAL_BUGFIX_MIGRATION.md`,
  `.scratch/`, and `docs/adr/`; sweep a range if unsure). For each, record from the public API:
  - **merged** (`state=closed, merged=true`) — fix is now in `upstream/master`.
  - **rejected** (`state=closed, merged=false`) — fix is NOT in upstream (unless re-done there later).
  - **open** (`state=open`) — still proposed; fetch its head:
    `git fetch upstream pull/<N>/head:refs/pr/<N>`.

### 2. Classify each local mod (fan out — one analysis agent per fix-mod)
For each `mod/<name>` fix-mod, an agent reads `mod_info.json` + `README.md` + `scripts/*.py`,
finds its PR number(s) via the migration table and `.scratch/`/`docs/adr/`, and — crucially — checks whether
the fix **is already present in `upstream/master`** by reading the patched upstream function
(`git show upstream/master:<path>`) and comparing behavior. Output per mod: `mapped_prs`,
`covered_by_upstream` (yes/partial/no), `disposition`, evidence.

**Disposition rules:**
| Condition | Action |
| --- | --- |
| Maps to a **merged** PR, OR behavior already in `upstream/master` (covered) | **DELETE** mod |
| Maps to an **open** PR | **DELETE** mod (the PR code merges in separately) |
| Otherwise (rejected PR or purely local) AND not covered by upstream | **KEEP** on disk |

For KEEP mods, the user's rule is "keep **and enable**". Apply it, **except** do not flip a mod
the maintainer deliberately disabled without confirming — surface those and ask. Personal mods
(no PR) are kept untouched; leave their enabled state as-is.

### 3. Identify what to preserve vs. reset
- **Reset to upstream (code):** everything upstream tracks — `Script/`, `data/`, root build
  scripts, `.github/*` (upstream owns `.github/prompts` and `.github/skills` too), etc.
- **Keep local infra (shared files, restore explicitly):**
  - `Script/Core/mod_manager.py` — local version adds the `replace` patch engine and
    dependency/mutation handling that local mods require. **Always keep the local one.**
  - `mod/mod_config.json` — runtime enable/load list (reconciled in step 5).
- **Keep all pure-local files** = files present in `main` but absent in `upstream/master`.
  Compute, don't enumerate by hand:
  ```
  comm -13 <(git ls-tree -r --name-only upstream/master | sort) \
           <(git ls-tree -r --name-only main | sort)
  ```
  This is `CONTEXT.md`, `docs/`, `.scratch/`, `.codex/`, `.claude/` additions, `AGENTS.md`, local `mod/` subdirs, local
  `.github/skills` additions, `mod/LOCAL_BUGFIX_MIGRATION.md`, etc.
- **Sanity check** there is no *other* local edit to a shared file that a reset would drop:
  `git log --oneline upstream/master..main -- Script/ data/ ':(exclude)Script/Core/mod_manager.py'`
  — every commit listed must be a PR head/merge or a knowledge-base doc, never stray local authorship.
  Investigate anything else before proceeding.

### 4. Build the target tree (in an isolated worktree)
```
git branch backup/main-pre-rebase-<date> main        # safety net — always
git worktree add <wt> --detach upstream/master
cd <wt>
git merge --no-ff refs/pr/<open1> refs/pr/<open2> ... # + all proposed open PRs
git checkout main -- Script/Core/mod_manager.py mod/mod_config.json
comm -13 <(git ls-tree -r --name-only upstream/master|sort) \
         <(git ls-tree -r --name-only main|sort) | tr '\n' '\0' | xargs -0 git checkout main --
git rm -r <each DELETE mod dir>
```
Open PRs built on an older base may conflict with a refactored `upstream/master`; resolve or,
if messy, stop and report rather than guess.

### 5. Reconcile mod config and knowledge
- `mod/mod_config.json`: remove every deleted mod from `enabled_mods` **and** `load_order`.
  Add newly-kept-and-enabled mods per step 2 (respecting the deliberate-disable exception).
- `mod/LOCAL_BUGFIX_MIGRATION.md`: move newly-merged/covered PRs to the merged section, drop the
  deleted mods, update the open-PR list.
- Knowledge base: record outcomes for PRs that closed (merged or rejected) since last run — close the
  matching `.scratch/` ticket and, if a durable decision changed, update `CONTEXT.md`/`docs/adr/`.

### 6. Adopt and verify
- Commit the target tree on a temp branch, then adopt per the user's choice:
  - **Rewrite main in place:** `git -C <repo> reset --hard <temp>` (preserves untracked files:
    `.venv`, `save.bak`, `note_for_codex`, etc.). Then remove the worktree/temp branch.
  - **New branch:** leave `main` at the backup and hand over the new branch.
- Reapply the runtime `mod/mod_config.json` content in the real working dir if it differs from
  what was committed.
- Verify (never skip): `python buildconfig.py` must succeed; then boot the game and confirm the
  kept mods load without error (mod manager logs each load). Prefer the tk visual runner
  (up to 3 slots) for a real boot. Report exactly what you ran and saw.

## Guardrails
- Always create `backup/main-pre-rebase-<date>` before rewriting `main`.
- `replace`-type mods copy an upstream function body; if `upstream/master` changed that function,
  the mod would revert upstream's other edits. For kept `replace` mods, confirm the target
  function is unchanged upstream (the step-2 agents check this).
- Rejected-PR code with no mod (e.g. a withdrawn display fix) is simply dropped — that is correct;
  it is neither upstream nor an open PR.
