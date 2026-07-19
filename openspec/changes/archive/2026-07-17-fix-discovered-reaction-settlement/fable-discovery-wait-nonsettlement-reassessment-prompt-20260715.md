/investigate-game-bug

Independently reassess one gameplay-semantics question for the current erArk discovered-reaction settlement candidate. Do not edit files.

Question
--------

The maintainer asks whether it is easy and reasonable to make all successor WAIT behaviors in the differing helper/current discovery cases not settle.

Scope
-----

Interpret "all WAIT" narrowly as WAIT produced after the H-discovery panel, especially the no-route fallback created by effect 1721 for `see_h_but_deceived`, `see_h_and_leave`, and `refuse_join_group_sex`. Do not recommend a global change to unrelated WAIT behavior unless the evidence requires it.

Current candidate
-----------------

- Worktree: `/home/ubuntu/games/erArk-pr-discovery-settlement-ad-hoc`
- Commit: `356c1e86ce205d09edda042bfee540095b65c420`
- Upstream parent: `3a1c9e620`

Previously established comparison
---------------------------------

- Current candidate settles `[reaction, WAIT]` in the same normal NPC scheduler pass when effect 1721 cannot find a route to the discoverer's dormitory.
- Previous helper candidate settles only `[reaction]` in that pass.
- Both finish the panel path with behavior `WAIT`, duration 1.
- Upstream was inconsistent: REFUSE already behaved like current; DECEIVED and LEAVE behaved like helper.
- A prior Fable verdict preferred current and described helper's WAIT as waiting until a later tick.

New verified lifecycle fact
---------------------------

The "later tick" description is incorrect.

- `Script/Design/character_behavior.py:169-178` only calls `judge_character_status()` for an NPC whose behavior is `SHARE_BLANKLY` or `MOVE`.
- An NPC already in `WAIT` does not enter either settlement branch.
- Every NPC pass still calls `judge_character_status_time_over()` at lines 179-187.
- `judge_character_status_time_over()` resets an expired non-MOVE behavior to a fresh `Behavior()` at lines 321-351; it does not call `judge_character_status()` first.
- Therefore, if the discovery path suppresses the immediate outer settlement of successor WAIT, that WAIT is never behavior-settled later. It eventually expires and is reset.
- WAIT's direct configured effect is `NOTHING`/9999 and its handler is `pass`, but a real WAIT settlement still goes through `judge_character_status()`, including behavior talk and pre/post event lookup. NPC WAIT talk can set `have_shown_waiting_in_now_instruct = True`.

Consequences
------------

- Current semantics: reaction effects settle once, then successor WAIT also gets its talk/event pipeline once in the same NPC pass.
- Helper-style semantics: reaction effects settle once, successor WAIT gets no behavior settlement at all; no WAIT talk, no WAIT events, no WAIT display flag. It merely expires/reset later.
- Successful-route successor MOVE remains settled in both designs.

Candidate implementation boundaries relative to the current candidate
---------------------------------------------------------------------

1. Keep current code: no production diff; WAIT is a real successor behavior and is settled.
2. Narrow one-line discovery-state-machine rule: replace `return now_panel.skip_outer_settlement` with a return that is also true when the discoverer's post-panel behavior is WAIT. This changes one nonblank line to one nonblank line (`a=1`, `b=1`, penalty `3a-b=2`). It affects only WAIT present after this discovery panel, allows MOVE to settle, and leaves unrelated state machines unchanged.
3. Add a WAIT check separately to each of the three reaction branches (`a=3`, `b=0`, penalty 9). More explicit casework but larger.
4. Add `behavior_id != WAIT` to the generic NPC scheduler guard (`a=1`, `b=1`, penalty 2), but this changes every target state machine that produces WAIT and is therefore broader than the question.

Please return a concise verdict:

1. Correct any factual error in the lifecycle analysis.
2. Is discovery-generated WAIT non-settlement a coherent and reasonable contract, or does it silently discard meaningful behavior?
3. Distinguish "easy to implement" from "semantically preferable."
4. If the maintainer chooses silent/non-settled discovery WAIT, identify the smallest logically coherent boundary among the options and explain why.
5. State whether this semantic choice requires explicit maintainer confirmation before code changes.
