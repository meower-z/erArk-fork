# Session closure record — 2026-07-15

## Upstream publication state

- Upstream PR: `Godofcong-1/erArk#218`
- State observed immediately before the final Tk run: open and ready for review (`draft=false`)
- Base: `master@94d586840484adf21fcf746dba0444551dd6a5a1`
- Head: `meower-z:codex/fix-discovery-settlement-ad-hoc@4e226f4f587b82a87368a3d7976650593323a7b4`
- The session-closing verification was read-only. It did not edit the PR body or title, add a comment, change draft state, push a branch, or otherwise mutate the PR.

## Final Tk result

The final real-Tk replay followed the 38-input approved route on the exact PR base and head. It reached the same successful Closure discovery while the player was in H with Dobermann.

- Baseline: Closure's selected response is absent; output continues directly with Dobermann's H text.
- Candidate: Closure's explanation and departure, stamina `-15`, and `5分钟过去了` each appear exactly once; Dobermann's H text then continues.
- New baseline versus PR before: `AE=0`, `RMSE=0`, pixel-identical.
- New candidate versus PR after: `AE=0`, `RMSE=0`, pixel-identical.
- Different PNG byte hashes are encoding/metadata differences only.
- Both save files are unchanged after the replay.
- Four transient partial redraws were allowed to settle without input before the next action.
- The route verifies the PR's main missing-reaction claim. It does not exercise the separate no-route `WAIT` branch.

The append-only evidence archive is `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/`; its complete checksum file validates and has SHA-256 `db107e95e2b5a9fb28420134cfce090ab03fb091d027145280b43a4a5a31aef7`.

## Final review and cleanup

Fable 5 returned PASS after independently reading the final OpenSpec record and evidence archive. Its sole required finding was that the two contracted disposable roots had not yet been removed. That finding is resolved:

- `/tmp/erark-pr218-final-tk-rerun-20260715/` is absent;
- `/tmp/erark-pr-images/discovery-settlement/pr218-final-rerun-20260715/` is absent;
- both linked worktree registrations are absent after `git worktree prune`;
- the append-only archive remains present and its complete checksum validates after cleanup;
- allocator status no longer lists the replay owner; one unrelated busy owner was left untouched.

The exact first Fable prompt and verdict are preserved in `fable-session-closure-record-review-prompt-20260715.md` and `fable-session-closure-record-review-verdict-20260715.md`. After the cleanup and focused-test-contract preservation, a narrow follow-up returned PASS with no required finding; its exact prompt and verdict are preserved in `fable-session-closure-cleanup-followup-prompt-20260715.md` and `fable-session-closure-cleanup-followup-verdict-20260715.md`.

## Durable design and verification knowledge

The authoritative local record for this change is this OpenSpec directory on the repository's main worktree. It includes:

- the rejected global/helper experiments and why they were superseded;
- the final explicit per-case settlement design;
- the caller and settlement-ownership audit;
- the user-confirmed `MOVE` versus no-route `WAIT` boundary;
- the exact 29-case focused verification contract in `focused-test-matrix-20260715.md` and code-size accounting;
- the Fable prompts, verdicts, timeouts, and user-waived artifact-review gate;
- fork branch, evidence publication, PR creation, and live PR provenance;
- the final exact-base/head Tk replay contract and result.

No new production-code change was made during the closing replay. No unique final-run knowledge is intentionally left only inside either disposable PR #218 runtime worktree. The two old discovery investigation worktrees contained task-owned, untracked test directories; their accepted behavioral contract and rejected-fixture provenance are preserved in `focused-test-matrix-20260715.md`, after which those untracked directories were removed. The clean PR candidate worktree and its pushed branch were not changed.

## Main-worktree persistence limitation

These OpenSpec files are present in `/home/ubuntu/games/erArk`, the main worktree. They cannot be committed into `main` history during this session without interfering with unrelated pre-existing repository state: the main worktree has an active cherry-pick (`CHERRY_PICK_HEAD=767562b83cf05c288208034f39d281e1a3a4a2f2`) and unresolved conflicts in `Script/Settle/Second_effect.py` and `Script/Settle/common_default.py`. Git refuses a partial commit during that state. The closing work does not resolve, abort, stage, or otherwise alter that unrelated cherry-pick. Therefore “recorded in the main worktree” is verified; “committed in main branch history” is not claimed.
