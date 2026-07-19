/investigate-game-bug

Perform a fresh read-only design/minimality review of T2 `judge-orgasm-edge-once-per-settlement` under the investigation skill's current `(a + b) + S - 2U` rule. Do not edit files and do not assume the existing candidate is good merely because it was previously reviewed.

Verified current facts:
- Current upstream is `72e28051ebaaabb069d06059b4633fda90b0b621`; PR #214 and #216 are already merged. There is no upstream PR for T2 and no other active agent owns it.
- The protected old candidate was cherry-picked without conflict into a fresh worktree `/home/ubuntu/games/erArk-pr-edge-shared-settlement-current`, branch `codex/fix-edge-shared-settlement-current`, commit `66db398e4` on current upstream.
- Current-upstream baseline fails the focused real-`orgasm_judge` chain because settlement is called more than once; the refreshed candidate passes all 11 tests in `tests/test_orgasm_edge_settlement.py`. `py_compile` and `git diff --check` pass.
- The old inspected Tk A/B and semantic record are in `/home/ubuntu/games/erArk/openspec/changes/judge-orgasm-edge-once-per-settlement/`. That evidence showed one character can receive several edge messages in one settlement, and mixed per-part success/failure can replay already-processed level changes.
- Confirmed rule: one eligible synchronous `orgasm_judge()` -> `orgasm_settle()` invocation for one character is one edge-decision batch. All supported parts in that invocation must contribute to the decision before any part is committed, then share one success/failure branch. Separate invocations remain independent. Time-stop, non-edge, and explicit-release paths preserve their existing meanings.
- Current candidate diff is production-only in `Script/Design/second_behavior.py`: after excluding blank lines, `a=39`, `b=17`. The diff has `S=30`, no normalized line is deleted at two or more sites, so `U=0`; penalty is `86`.
- Most of that score is one 30-line pre-loop collect/decide/failure-preparation block. The candidate also removes the four-line caller replay, replaces per-part time-stop/edge routing with captured flags, and adds an optional read-only count mapping to `judge_orgasm_edge_success()`.

Previously considered boundaries:
1. Decide on the first crossing and reuse it: smaller, but incorrect because later parts do not contribute to the probability.
2. Temporarily install provisional counts into the live `orgasm_edge_count`, call the existing judge, then restore with `try/finally`: potentially smaller, but it makes uncommitted counts observable and creates alias/rollback obligations. The old design rejected it; re-evaluate whether that is a hard correctness/scope failure or only a preference.
3. Move the decision into `orgasm_judge()`: wrong owner because direct `orgasm_settle()` paths and replacement policies exist.
4. Current explicit local snapshot passed to the judge: keeps provisional counts out of live state and preserves one-argument callers, but scores 86.
5. Larger plan/result object or transaction: higher scope and cannot roll back downstream effects.

Please inspect the current upstream source, the refreshed diff, tests, and the owning design. Decide whether candidate 4 remains the lowest-penalty logically correct and correctly scoped fix. Actively search for a lower-penalty correct candidate, including a more compact expression of the same local-snapshot boundary. If one exists, give a concrete style-compliant production hunk or precise pseudodiff, explain why it preserves every stated inverse path and failure-release behavior, and compute `a`, `b`, `S`, `U`, and the penalty from the proposed production diff. If the current candidate wins despite 86, explain why every lower-scoring boundary fails a hard gate. Identify any public gameplay semantic choice that still requires the user's final pre-PR confirmation.
