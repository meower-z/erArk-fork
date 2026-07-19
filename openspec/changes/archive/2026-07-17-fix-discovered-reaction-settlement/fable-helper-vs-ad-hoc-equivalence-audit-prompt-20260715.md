/investigate-game-bug

You are independently auditing two candidate implementations of the erArk discovered-reaction settlement fix. Do not edit files. Judge semantics from the evidence below and, where useful, inspect both worktrees directly.

Question from the maintainer
----------------------------

Did upstream originally contain both missed settlement and duplicate settlement? Are the current ad-hoc candidate and the previous helper candidate behaviorally identical in every case?

Candidates
----------

- Previous helper candidate: `/tmp/erark-discovery-helper-audit-20260715`, detached commit `884b2fa30`.
- Current ad-hoc candidate: `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc`, branch `codex/fix-discovery-settlement-ad-hoc`, commit `356c1e86ce205d09edda042bfee540095b65c420`.
- Their common upstream parent is `3a1c9e620`.

Established upstream defect shape
---------------------------------

- The upstream NPC idle scheduler always called `find_character_target(character_id, now_time)` and then unconditionally called `judge_character_status(character_id)`.
- Some discovered-reaction panel callbacks already called `judge_character_status()` themselves. The unconditional outer call could therefore settle the same reaction twice.
- Other callbacks did not settle the reaction. A direct hidden-discovery caller invokes the panel without going through the NPC idle scheduler, so those reactions could be left un-settled there.
- Initial group-sex conversion also has a nested NPC update that could overwrite the pending reaction before the intended settlement.

Focused regression harness
--------------------------

- The same production-definition harness passes on both candidates.
- Helper: 27 passed, 1 current-interface-only test deselected because helper intentionally uses the older `draw() -> bool` interface.
- Current: 28 passed.

Structured differential audit
------------------------------

A differential probe executed the real AST-extracted production functions from each candidate through 31 normal combinations plus one draw-exception case. It compared drawn events, exact settlement sequence, final behavior/duration/state, movement path, sex-mode/group state, follow-up calls, effect calls, and scheduler-tail execution.

Twenty-eight of 32 cases were identical. These included successful movement, every direct hidden-discovery call, JOIN existing group, initial group conversion with a nested tick, DISCOVER, IGNORE, INTERRUPT, explicit end single/group H, hidden-mode conversion, exhibitionism-mode conversion, and movement failure outside the three cases below.

Three normal NPC-scheduler cases differ only when effect 1721 tries to move the discoverer to her dormitory but no route exists:

1. `see_h_but_deceived`: helper settlements `[see_h_but_deceived]`; current settlements `[see_h_but_deceived, wait]`.
2. `see_h_and_leave`: helper settlements `[see_h_and_leave]`; current settlements `[see_h_and_leave, wait]`.
3. `refuse_join_group_sex`: helper settlements `[refuse_join_group_sex]`; current settlements `[refuse_join_group_sex, wait]`.

In all three, final behavior is `WAIT`, duration 1, in both candidates. The difference is whether that successor WAIT is settled immediately in the same NPC scheduler pass.

Why the difference exists
-------------------------

- Helper returns a public `discoverer_reaction_settled` flag for every explicit reaction and its scheduler uses `if not discoverer_reaction_settled or behavior_id == MOVE: judge_character_status(...)`. Therefore a successor MOVE is settled, but a successor WAIT is not.
- Current uses an ad-hoc `skip_outer_settlement` flag. It sets the flag for cases whose reaction remains current, but deliberately leaves it false for the three effect-1721 reactions so the outer scheduler settles their successor. This settles either MOVE or WAIT.

WAIT is not semantically invisible
----------------------------------

- `Behavior_Effect.csv` gives WAIT effect 9999, and `constant_effect.BehaviorEffect.NOTHING` is 9999; its direct numerical handler is `pass`.
- However `judge_character_status()` still runs behavior pre/post event lookup and `settle_behavior.handle_settle_behavior()`.
- `handle_instruct_data()` calls `talk.handle_talk()` before the NOTHING effect.
- NPC WAIT talk sets `action_info.have_shown_waiting_in_now_instruct = True` when it is first eligible for output.
- Therefore immediate WAIT settlement can change visible text, event timing, and the waiting-text suppression flag even though the direct numerical effect is empty.

One exception-path difference
-----------------------------

When the success-result panel draw raises during `see_h_but_deceived`:

- Helper has not yet assigned the reaction, leaving `SHARE_BLANKLY`, duration 1, with no settlement.
- Current assigns `SEE_H_BUT_DECEIVED`, duration 5 before drawing, leaving that pending reaction with no settlement.

This does not arise on a normal successful draw, but it is another reason the candidates are not identical in literally every execution.

Please return a concise but rigorous verdict addressing all of the following:

1. Confirm or reject the statement that upstream had both missed settlements and duplicate settlements.
2. Confirm or reject full behavioral equivalence between helper and current candidates.
3. Classify the three no-route WAIT differences: harmless implementation detail, acceptable semantic improvement, or contract-relevant mismatch that must be presented to the maintainer before claiming equivalence.
4. Classify the draw-exception ordering difference and whether it should block this gameplay fix.
5. State whether the current ad-hoc candidate should be changed before PR review. If so, describe the smallest logically coherent change; if not, state why the semantic delta is acceptable.
6. Explicitly distinguish verified facts from design judgment.
