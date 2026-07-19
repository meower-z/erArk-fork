# Fable current-upstream score review timeout

The exact prompt is preserved in [fable-current-upstream-score-review-prompt.md](fable-current-upstream-score-review-prompt.md).

Two read-only calls were made from the main project worktree with the required command and normal tool access:

- `claude -p --model claude-fable-5 --effort high --no-session-persistence`: timed out after 120 seconds with exit 124 and no verdict.
- The same command and prompt: timed out after 300 seconds with exit 124 and no verdict.

No Fable ruling was produced. Under the user's explicit instruction to decide locally if Fable became unavailable, the refreshed cherry-pick was treated as disposable and the explicit read-only snapshot boundary was re-derived under the new score. The temporary-live-ledger alternative remained rejected because it would expose provisional counts and add rollback obligations. A fresh-context critic then found and verified a style-compliant compact form of the same boundary with penalty 49.
