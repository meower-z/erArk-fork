# Audit Verdict

## 1. Upstream defect shape: **Confirmed — both defects existed**

Verified directly at parent `3a1c9e620` (via the diffs' context lines and current source):

- **Duplicate settlement path**: upstream `character_behavior.py` unconditionally ran `judge_character_status()` after `find_character_target()`, while `_invite_find_char_to_join` (JOIN, REFUSE) and `_end_current_h` (INTERRUPT) already called `judge_character_status()` themselves inside the panel. Two settlement calls for one reaction on the scheduler path.
- **Missed settlement path**: `hidden_sex_panel.py:249` invokes the panel directly, outside the scheduler, so no outer settlement exists there; upstream's non-self-settling branches (DECEIVED, IGNORE, LEAVE, DISCOVER_OTHER_SEX_AND_JOIN) left those reactions un-settled on that path.

## 2. Full behavioral equivalence: **Rejected**

The two candidates are not identical in every case. Confirmed from source: 32-case differential result is consistent with the code — three no-route effect-1721 divergences plus one draw-exception ordering divergence. Any equivalence claim to the maintainer must be withdrawn or qualified.

## 3. The three no-route WAIT differences: **acceptable semantic choice, but disclose — do not claim equivalence**

Key fact the audit prompt understates: **neither candidate preserves upstream in all three cases, because upstream itself was inconsistent.** Verified from source:

- Upstream REFUSE (self-settling): inner judge settles the reaction → effect 1721 (`Settle/default.py:2656` → `general_movement_module`, no-route fallback WAIT/1 at `StateMachine/default.py:58-63`) installs the successor → outer judge settles it same pass. Sequence `[refuse, wait]`.
- Upstream DECEIVED/LEAVE (non-self-settling): outer judge settles the reaction; the successor waits until the next tick. Sequence `[deceived]`.

The **current** candidate harmonizes all three to upstream's already-correct REFUSE semantics (`[reaction, successor]`). The **helper** harmonizes to `[reaction]`-only for WAIT, which *changes upstream's REFUSE behavior* — it is the helper, not the current candidate, that deviates from the one upstream case whose exactly-once semantics were already right.

WAIT settlement is not a no-op (verified: WAIT→effect 9999/NOTHING is `pass`, but `judge_character_status` still runs talk and events; `talk.py:597` sets `have_shown_waiting_in_now_instruct`). So this is a real, player-visible one-tick timing difference — a **contract-relevant mismatch for the equivalence claim**, but the current candidate's side of it is the better-grounded semantics.

## 4. Draw-exception ordering: **non-blocking**

Verified: upstream `_let_find_chara_away` assigned behavior *before* drawing. The current candidate preserves that upstream order exactly (assign → draw → judge); the helper reordered assignment after the draw. On a draw exception, both upstream and current leave a pending unsettled reaction; the helper leaves `SHARE_BLANKLY`. A draw exception is not a designed game path and propagates out of the scheduler in all three versions anyway. The current candidate is upstream-faithful here; no block.

## 5. Change current before PR review? **No.**

The current ad-hoc candidate should go to PR review as-is, because:

- Its uniform rule (reaction settles exactly once at the panel; the outer pass settles whatever successor 1721 installed, MOVE or WAIT) matches the one upstream branch that already had correct semantics.
- Checked the one structural risk in its missing `or behavior_id == MOVE` clause: none of the flag=True reactions (`join_group_sex`, `discover_other_sex_and_join`, `see_h_and_interrupt`, `see_h_but_ignore` — `Behavior_Effect.csv:171-188`) carry effect 1721 or any movement effect, so no same-pass successor MOVE can be orphaned. The clause the helper needed is unnecessary in the current design.
- Smaller diff, no public interface change (helper changes `draw() -> bool`, a caller-visible contract), preserves upstream exception ordering. Penalty: current ≈ 3·20−4 vs helper ≈ 3·31−28 — current wins on the skill's metric too.

Required non-code action: the change record / PR-facing material must state the one intentional upstream delta — on the no-route path, DECEIVED/LEAVE successors now settle in the same scheduler pass (as REFUSE always did) instead of the next tick.

## 6. Verified facts vs design judgment

**Verified by direct source inspection this session:** both diffs vs `3a1c9e620`; upstream's unconditional outer judge and the mixed self-settling callbacks; the two panel call sites; effect 1721's handler and its WAIT/1 no-route fallback; WAIT=effect 9999=NOTHING with `pass` handler; `talk.py:597` flag write; effect tables showing 1721 only on `refuse/deceived/leave` and no movement effects on flag=True reactions.

**Taken from the supplied differential audit (not independently re-executed):** the exact 28/32 identical-case tally and the settlement-sequence traces. The traces are consistent with everything I verified statically, and the regression harness passing on both candidates corroborates them.

**Design judgment:** classifying the WAIT delta as acceptable, the exception delta as non-blocking, and the recommendation to ship current unchanged with disclosure.
