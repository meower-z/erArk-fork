# Final focused behavior matrix — 2026-07-15

## Purpose and provenance

This document preserves the behavioral knowledge carried by the local-only focused test seam before its task-owned copies are removed from old investigation worktrees. The accepted final fixture was `test_discovery_settlement_ownership.py`, 919 lines, SHA-256 `99212543f4791eb61f7a0f47cc2f1ec4606c776970f5c6a7a2cd8e33d6a87c6e`. It was never part of the production diff or PR #218.

The final run expanded to 29 cases. All 29 passed against candidate `4e226f4f587b82a87368a3d7976650593323a7b4`.

## Exact case accounting

1. Six group-discovery cases: NPC and direct callers crossed with join an existing group, refuse an existing group, and convert an initial two-person scene into group H. Each selected discoverer behavior settles exactly once; conversion settles before its player follow-up.
2. One NPC route-success refusal case: settlements are exactly `[refuse_join_group_sex, move]`; every configured refusal effect runs once; route finding runs once; the discoverer movement progresses in the same round.
3. One NPC no-route refusal case: settlements are exactly `[refuse_join_group_sex]`; route finding runs once; the successor remains `WAIT` with duration 1 and is not settled again.
4. One direct-call refusal case: settlement is exactly `[refuse_join_group_sex]`; no NPC round is fabricated to resume the successor.
5. Six non-group explicit-reaction cases: NPC and direct callers crossed with deceived, ignore under successful exhibitionism judgment, and leave after failed exhibitionism but successful H-mode judgment. Each selected discoverer reaction settles exactly once. Only the NPC caller settles a real `MOVE` successor after deceived or leave.
6. Four interruption cases: NPC and direct callers crossed with single-H end and group-H end. `see_h_and_interrupt` settles exactly once and before the existing player-scene follow-up.
7. Four successful mode-switch cases: NPC and direct callers crossed with conversion to hidden sex and conversion to exhibitionism. No explicit discoverer reaction is invented. The NPC path retains its ordinary outer `SHARE_BLANKLY` settlement; the direct path has no outer settlement. The expected follow-up and achievement occur.
8. One panel-result case: `panel.draw()` retains its upstream `None` return while `panel.skip_outer_settlement` stores `True` even though the UI command layer discards callback return values.
9. One return-chain case: discovery state-machine 40 and `find_character_target()` return the stored true settlement flag unchanged.
10. One scheduler-tail case: the true flag skips only the already-consumed outer status settlement. Tiredness, movement restriction, assistant, follow, H guard, realtime, persistent-state, interruption, time-over, and talent tail phases each still run once.
11. Two ordinary-state-machine cases: `None` and `False` dispatch results both retain the ordinary outer `SHARE_BLANKLY` settlement.
12. One consumed-replacement case: a true result whose nested flow already consumed the replacement is not replayed by the outer scheduler.

Total: `6 + 1 + 1 + 1 + 6 + 4 + 4 + 1 + 1 + 1 + 2 + 1 = 29`.

## Rejected local fixture

An older helper/global-owner investigation worktree retained a different 1,097-line fixture with SHA-256 `47ad2410e06dce9fe534afb31f9d6de2c01e8a879f7c8fbaab425cb0b09d5b23`. It belongs to the superseded helper/global experiment, not the accepted per-case design. Its relevant historical conclusions and rejection reasons are preserved in `implementation-notes.md`; it is not a source of final behavior claims.
