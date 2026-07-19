# Save 99 state-machine diagnosis for target-scope evidence

## Deterministic seed-0 result

A single complete current-upstream run reproduced all six checkpoints from the earlier seed-0 log: the same RNG hashes at seed/startup/load/setting/pre-command/command-complete, time 11:52→11:57, player target CID 3 throughout, Theresa V 803→840, Lin V 5379→5416, and unchanged save hashes.

The added observation was positive rather than inferred from silence:

- Theresa (56) and Lin (4080) each selected target `default9`, state machine 2, and behavior `wait`; their masturbation flag was 3.
- The effect dispatcher recorded `(cid, behavior)=(56|4080, wait)` and effect sequence `[9999]` for each. Neither selected behavior 418, so effect 524 correctly did not run.
- The target-91 prerequisite cache showed group on and same-place true, but its masturbation-flag-3 entry was missing because the type-12 search containing target 91 was not entered.

The previous observer did not miss an effect-524 call; the earlier static claim that target 91 must be searched was wrong. The accepted log is `/tmp/erark-t7-seed-search-20260715/seed-00-state-machine-diagnostic.log` with SHA-256 `e4587c298b909dab33fdf4d71d70da0c3bac29a8dfbef32ff7c0f55afd72c6df`.

## Why target 91 was not searched

Before NPC target search, group-sex AI type 1 sets the masturbation flag to 3 and resets the behavior to `SHARE_BLANKLY`. The normal-1 gate that admits the special type-12 target group does not treat flag 3 alone as abnormal; it accepts flag 1/2 or the separate `npc_masturebate_for_player` reverse flag. With only flag 3, target 91 is outside the searched target type. Theresa and Lin instead matched normal target 9, whose state machine waits in place and cancels following.

There is no masturbation type-0 event that suppresses effect 524. If behavior 418 enters ordinary instruction settlement, its production effects include 456, 458, and 524.

## Candidate normal route condition

The code path toward target 91 would first require a later normal target search to choose target 86 after target 9 clears following. Target 86 requires normal target 1267, desire at least 100, no sexual ignorance, and masturbation not forbidden. State machine 91 then has a fall-level-dependent random branch that can set `npc_masturebate_for_player=True` while leaving the masturbation flag at 3.

On the next NPC pass, group-sex type 1 writes flag 3 again but does not clear the reverse flag. That reverse flag makes the normal-1 gate abnormal, so type-12 search is entered; targets 87–90 require flag 1/2 and fail, while target 91 accepts group on, same place, and flag 3. State machine 92 then selects behavior 418, whose effect 524 is mandatory though the chosen body part remains random.

The reverse flag's production clear paths do not occur in the same continuous group/type-1/same-place route before this transition. Direct flag-0 writers either require behavior 418 itself, reset H state and leave the route, or are production-unreachable. The similarly numbered second effect 412 dispatches through a different registry and cannot invoke character-online reset.

This establishes a valid code entry condition, not a concrete player route. The subsequent bounded lifecycle trace proved that the save-99 wait-only route exits before any of the nine candidates can satisfy it: seven leave through earlier normal chains, and the remaining two leave for work after their first midnight desire increase is only 8–16. There is no finite wait number for this save and input route. See `target-scope-save99-wait-only-route-closed.md`. No seed scan or Tk run may continue from the rejected route.
