---
name: wrap-up-session
description: End-of-session cleanup for erArk. Use when the user says to "wrap up a session" (or wrap up / 收尾 the session). Commits this session's pending skill and docs updates to local `main`, pushes `main` to `origin/main`, removes this session's temporary worktree, and cleans up only this session's orphaned processes.
---

# Wrap Up Session

When the user asks to wrap up a session, perform the steps below in order. This machine is shared: the user's Windows machine pushes directly into this checkout (`receive.denyCurrentBranch=updateInstead`) and other Claude/codex sessions run concurrently with their own worktrees and Tk/Xvfb processes. Every step that commits, pushes, removes a worktree, or kills a process must first distinguish THIS session's artifacts from other sessions' and from the user's own commits. Never touch another session's worktree, processes, or uncommitted work.

## 1. Commit skill + docs updates to local `main`

- Confirm you are on `main` in the main worktree (`/home/ubuntu/games/erArk`), not a linked worktree.
- **Wiki fold check** — if this session landed any behavior change (commit, merged PR, mod enable/disable): scan `docs/wiki/INDEX.md` for pages whose facts the change touched, and run `/project-wiki` to fold them (rewrite as current truth, refresh `timestamp`) so the wiki update commits together with the session's docs. Skip only when the session changed no behavior.
- `main` HEAD may have advanced during the session (Windows pushes; other sessions commit skill/docs updates). Run `git log` and `git status` first — much of your work may already be committed. If a file you edited shows no diff against HEAD, verify the committed content actually contains your final edits (`git show HEAD:<path> | grep <marker>`) before assuming it is yours and current.
- Stage ONLY skill and docs changes that are yours this session:
  - `.codex/skills/**` (this is the tracked, canonical copy; `.claude/skills/**` is an untracked local mirror — keep both identical, but only `.codex/skills` is committed).
  - `CONTEXT.md`, `docs/adr/**`, `docs/agents/**`, `docs/wiki/**`, and `.scratch/**` files you changed (the local issue tracker, domain docs, and wiki; see `docs/agents/issue-tracker.md`).
  - agent definitions under `.codex/agents/**` you added.
- Do NOT stage, and restore with `git checkout -- <path>` if you dirtied them: `.codex-evidence/`, `.venv/`, `save/`, `save.bak/`, `note_for_codex`, generated `data/*.json`, `Script/Config/config_def.py`, `data/po/**` (buildconfig/buildpo noise), runtime `config.ini` and `mod/mod_config.json` (skip-worktree local config). If you set `config.ini web_draw=0` for Tk evidence, restore it to `1`.
- Leave other sessions' pending docs/ticket edits untouched. Commit surgically (one logical change) with identity `meower-z <299913659+meower-z@users.noreply.github.com>` and a `docs(...)`-style message.

## 2. Push `main` to `origin/main`

- Confirm the active GitHub account is `meower-z` (`gh api user -q .login`). Push ONLY to `origin` (meower-z/erArk); NEVER push `upstream`.
- `git push origin main`. If it is rejected as non-fast-forward (origin advanced, e.g. from the Windows machine), `git fetch origin` and reconcile (merge/rebase, preserving unique commits) before retrying. Do not force-push shared `main`.

## 3. Remove this session's temporary worktree

- `git worktree list`. Identify worktrees under THIS session's scratchpad path (its session-UUID directory under `/tmp/claude-*/…/scratchpad/`). Leave worktrees whose path contains a different session UUID.
- `git worktree remove <path>` (it refuses if dirty — reconcile first). Removal keeps the branch ref, which is correct: pushed branches and open PRs depend on the ref, not the worktree. Do not delete the branch unless separately asked.

## 4. Clean up only this session's orphaned processes

- Never blanket-kill by process name. For each candidate `Xvfb` / `openbox` / `game.py` / `xvfb-run` / scratch python process, read `/proc/<pid>/cwd`: kill ONLY those whose cwd is under THIS session's scratchpad path, plus any display you started that now has no clients. Leave every process whose cwd is another session's worktree.
- `xvfb-run -a` auto-allocates the lowest free display; after you free one (e.g. `:99`), another session may immediately grab it — re-check ownership by cwd before killing any `Xvfb :<n>`.
- Check `python .codex/skills/investigate-game-bug/scripts/tk_capture_slots.py status`; release only capture slots owned by this session.
- Remove this session's disposable `/tmp` scratch directories; leave shared or other-session paths.

## Report

State: what was committed (SHA + files) or that it was already committed; the `origin/main` push result; which worktree was removed (and that its branch ref survives); and which processes were killed vs deliberately preserved, naming the other-session ownership that spared them.
