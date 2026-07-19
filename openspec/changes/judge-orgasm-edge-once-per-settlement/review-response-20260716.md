# Review response: k-th-power multi-part difficulty refinement (2026-07-16)

Record of a code-review exchange on PR [#221](https://github.com/Godofcong-1/erArk/pull/221) (`Godofcong-1/erArk`, "修复寸止结果在一次高潮结算中重复显示、高潮等级重复推进"). The PR implements the once-per-settlement edge decision described in `proposal.md` and `design.md`. On 2026-07-16 the maintainer objected to the shared-decision model, the author counter-proposed a difficulty refinement, and that refinement was implemented and pushed to the PR branch.

## State change

- PR head branch: `codex/fix-edge-settlement-shared-decision` on `meower-z/erArk-fork` (git remote `pr-fork`). PR state: OPEN.
- Previous head: `9f1a5109d2e9f332b9262206879a155d353035c8` — the once-per-settlement change only, exactly as described in `pr-readiness.md` and the design docs.
- New head: `6de9eb5620c57e4763fd5b760fdade401657dcb4`, one commit on top of the previous head, pushed to the fork branch. It adds the k-th-power difficulty refinement described below. All docs in this change dir written before this note describe only the parent commit's state.

## Maintainer objection (Godofcong-1, repo owner)

1. **Per-part edge behavior is intentional.** Multi-part edge-denial (寸止) is meant to be much harder, reflecting that the player must control each part separately in a flustered state. Collapsing to a single shared roll removes intended difficulty.
2. **The duplicate display is an incomplete-information problem, not a duplication problem.** The maintainer's preferred fix is to name the specific body part in each message — `成功寸止了A角色的B部位绝顶` — so players are not misled, rather than deduplicating to one line.
3. **The re-settlement / level-inflation bug came from insufficiently rigorous flow, not from lacking a shared decision.** A later-part failure is intended to produce a 功亏一篑 all-parts-fail settlement. The maintainer's proposed fix: before settlement, copy the original climax data; if not edge-denying, or edge-denying with all parts passing, proceed normally; if edge-denying and any part fails, restart from the copied data and settle the whole batch as one edge-denial failure.

## Author counter-proposal (meower-z)

- Core argument: one `orgasm_settle()` invocation is logically simultaneous, so sequential per-part settlement does not fit the semantics; all parts crossing at that checkpoint should share one judgment.
- To still reflect increased difficulty when several parts cross at once: raise the edge-denial success probability to the power of `k`, where `k` is the number of parts newly crossing the climax threshold in this settlement.
- Difference from the maintainer's per-part model: each crossed part still effectively contributes one judgment, but every part uses the *same* success probability, derived from the combined count of all parts (the existing square-sum difficulty over `candidate_orgasm_edge_count`, which already includes prior held counts plus the whole current batch). Example: if parts A and B cross simultaneously, both are judged at one combined "harder" difficulty raised to the power 2, rather than A getting an easier roll followed by B a harder roll.
- Claimed advantage over the maintainer's backup-and-recompute flow: no backup or restart; the refinement is a single exponentiation at the decision point.

## Implemented refinement (commit `6de9eb562`)

Single file, `Script/Design/second_behavior.py`, 9 insertions / 2 deletions.

- In `orgasm_settle()`, inside the existing pre-mutation collection loop that builds `candidate_orgasm_edge_count`: a counter `crossed_part_count` is incremented once for each supported part that has any `normal`, `extra`, or `un_count` work this settlement. It is passed as a new third argument to `judge_orgasm_edge_success()`.
- `judge_orgasm_edge_success()` gained a backward-compatible parameter `crossed_part_count: int = 1`. Existing one- and two-argument callers are unaffected; only core settlement passes it.
- The exponentiation applies only in the probabilistic branch (`over_count < 0`, already past the skill limit): the single-part success probability `1 - fail_rate` is raised to `crossed_part_count`, then converted back to a total failure rate — `success_rate = max(0.0, 1 - fail_rate) ** crossed_part_count; fail_rate = 1 - success_rate`.
- The guaranteed-success branch (`over_count >= 0`, within the skill limit) is intentionally unchanged, because `1 ** k == 1`. Plainly: while the player is within the edge-denial skill limit, multiple simultaneous parts introduce no failure chance; the power only bites once the roll is already probabilistic.

### Clamp hazard

The original `fail_rate = 0.2 * over_count * -1` can exceed 1.0 when `over_count` is strongly negative — a state that already always fails. If `1 - fail_rate` (a negative base) were raised to an even power directly, the result would be positive and would spuriously *lower* the total failure rate, turning an always-fail case into a sometimes-succeed case as `k` grows. Clamping the single-part success to `[0, 1]` via `max(0.0, ...)` before exponentiation prevents this. The transform was checked to satisfy: at `k = 1` it reproduces the original (clamped) behavior; total failure rate is monotonically non-decreasing in `k`; and an always-fail input (`fail_rate >= 1`) stays always-fail for every `k >= 2`.

## Scope

`design.md` set a review budget of roughly 45-55 touched production lines for the once-per-settlement change and asked to stop for renewed design review if the difficulty model changed. This refinement is a deliberate, review-driven extension of that budget: it adds ~9 lines and changes the multi-part difficulty model in direct response to the maintainer's point 1. It is not silent scope creep.

## Standing status and open threads

- The refinement is pushed to the PR branch; the PR remains open and unmerged. The author posted a reply comment on the PR presenting the k-th-power approach and asking whether the maintainer finds it acceptable. As of 2026-07-16 the maintainer has not responded to that reply.
- Only the difficulty model (point 1) was addressed. The maintainer's display concern (point 2 — naming the body part in the message) and the maintainer's backup-and-recompute flow (point 3) were *not* adopted; the author's shared-decision structure plus the k-th-power difficulty is the standing counter-position.
- Open question for follow-up: whether "multi-part is harder" should also affect the within-skill-limit guaranteed-success branch. The current implementation leaves it untouched (`1 ** k == 1`); making difficulty apply inside the skill limit would be additional work beyond commit `6de9eb562`.
