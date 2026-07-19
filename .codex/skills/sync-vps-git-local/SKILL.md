---
name: sync-vps-git-local
description: Synchronize the erArk repository across the local worktree, `ssh vps` at `~/games/erArk`, and the private Git origin. Use only when the user explicitly asks to sync, synchronize, or reconcile VPS-Git-local state.
---

# Sync VPS-Git-Local

Keep all three copies on the same branch and commit without losing unique commits or unrelated dirty files.

## Workflow

1. Inspect before changing anything:
   - Record the current branch, HEAD, status, and remotes locally and on `ssh vps`.
   - Fetch the private `origin` in both worktrees.
   - Confirm `origin` points to `meower-z/erArk`; treat public `upstream` as fetch-only.
   - Compare ancestry and divergence among local, VPS, and `origin/<branch>`.

2. Protect work:
   - Preserve all unrelated dirty files, especially generated PO files.
   - Never clean, reset, force-push, or overwrite unique commits.
   - If local and VPS contain conflicting unique work, stop and report the divergence instead of guessing.

3. Reconcile conservatively:
   - Push the authoritative ahead commit to the private origin when it is a fast-forward.
   - Fast-forward the lagging VPS or local worktree from the private origin.
   - Create a normal merge only when both histories must be retained and the merge is unambiguous; otherwise ask the user.
   - Do not synchronize saves, run tests, start remote Codex, create handoffs, or use tmux unless separately requested.

4. Verify and report:
   - Confirm local HEAD, VPS HEAD, and the private origin branch resolve to the same commit.
   - Recheck protected dirty-file hashes and status.
   - Report the branch, final commit, synchronization direction, and any remaining dirty or divergent state.
