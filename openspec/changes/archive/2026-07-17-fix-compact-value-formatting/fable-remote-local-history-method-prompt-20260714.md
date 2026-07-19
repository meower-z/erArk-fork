/investigate-game-bug
/review-erark-pr-artifacts

Determine the logically correct Git operation for updating the fork branch for the compact-value-formatting upstream candidate. Do not perform any mutation. Distinguish verified Git facts from workflow preference and give one recommended operation with exact safety checks.

Verified repository facts:

- Candidate worktree: `/home/ubuntu/games/erArk-pr-compact-value-formatting`.
- Upstream base is currently `upstream/master@3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`.
- Original local candidate `cd28b2b219d4d7a8f89875cb9be1111a9505110d` was based on `06fc59c1e71d092224375fc4a096b956aea2ad63`. It already contained the formatter production change, the 50-line focused formatter tests, and the large `test_real_settlement_callers_keep_compact_self_and_exact_target_values` production-path test.
- Rebase onto current upstream produced `91939e9ad5e5076070ea708b6744506235c57823`, whose parent is exactly `3a1c9e620`. The stable patch ID before and after rebase is identical: `40e843b9b1a3ec02c0687982daa5a093375bcc35`. The candidate production and test file contents are byte-identical between `cd28b2b21` and `91939e9ad`.
- `91939e9ad` was pushed by this workflow to `pr-fork/codex/fix-compact-value-formatting` at 2026-07-14 19:59 UTC. A fresh fetch confirms that the live remote ref is still exactly `91939e9ad`; there is no later remote change.
- The user then required PR-submitted tests to stay small. Locally, only the large test and its three dedicated imports were deleted, removing 93 lines. The production file is byte-identical between remote and local.
- The deletion was folded into the candidate with `git commit --amend`, producing local `7fd521bb6d98fcaa0841cce79e6d82ecf9c04b82`. Its parent is also exactly `3a1c9e620`. Thus remote `91939e9ad` and local `7fd521bb6` are sibling commits on the same rebased upstream base; neither is an ancestor of the other.
- The local candidate has 14 passing focused cases, passes `py_compile`, and passes `git diff --check`.
- Desired public history: one reviewable candidate commit on current upstream, containing the production formatter fix and only the 50-line focused test file. No PR exists yet.
- No push is currently authorized by this prompt. Publishing requires separate user confirmation.

Evaluate these approaches:

1. Replace remote `91939e9ad` with local `7fd521bb6` using an exact expected-value lease, `--force-with-lease=refs/heads/codex/fix-compact-value-formatting:91939e9ad5e5076070ea708b6744506235c57823`.
2. Preserve remote `91939e9ad` and add a second ordinary commit that deletes the large test.
3. Rebase or merge one sibling candidate commit onto the other.

State which approach best matches the desired history, whether the large test on the remote was caused by rebase or by the earlier candidate content, what must be rechecked immediately before and after the operation, and whether any unresolved fact requires user input. Return a concise Chinese verdict.
