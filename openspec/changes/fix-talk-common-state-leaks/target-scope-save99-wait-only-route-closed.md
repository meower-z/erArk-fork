# Save 99 wait-only target-scope route closure

## Verdict

The normal save-99 route that repeats only `[6001]等待五分钟` has no finite wait number at which any of the nine non-target NPC candidates can reach target 86 while remaining in the same group-sex scene. Its later target-86 probability is zero. The previously recorded target86 → reverse flag → target91 chain remains a valid code path, but this save and input route exits before its entry premises can hold.

## Desire lifecycle

All nine candidates start with `desire_point=0`. Along this wait-only route, the only positive production writer found is the new-day update: after refreshing entertainment it adds `randint(ability[33], 2 * ability[33])`. The NPC target-search loop runs before that new-day update.

The apparent global 12:02 meal interruption is not immediate because the meal premise reads each NPC's `behavior.start_time.hour`, not global time. Once an NPC later enters the meal chain, its type-12 meal targets take precedence and do not return it to target 86 in the same group route.

Seven candidates leave earlier through their normal work, rest, or entertainment chains. Once an NPC is outside the player's scene, `handle_npc_ai_in_h` clears its H state and gives it an end-H behavior, so it no longer performs the same group-sex target search.

## Last two candidates

CID 241 and 4122 remain temporarily in the scene because target 462 selects state machine 612, but the training-locker-room lookup finds no matching destination and therefore writes no movement behavior. They remain at local start time 11:46 with zero duration until the first midnight crossing.

On wait 146, their NPC search still happens before the new-day update, so desire is still zero. The update then resets `sp_flag.swim` and adds only 8–16 desire because both have ability 33 level 8. On wait 147, target 86's `desire_point >= 100` premise must fail. Both are sex trainees with assigned exercises, no obedience fall, and not in their dormitories; the workday target 802 therefore selects state machine 502 and moves them to their dormitories. Their next NPC pass is outside the player's scene and clears H state.

No later wait in this route can reconsider target 86 for either character. The counterfactual calculation that permanent external retention could first permit desire 100 around wait 1875 is not a player route and must not be used as evidence.

## Falsification boundary

This closure would be wrong if production can, before wait 147, write either remaining character's desire directly to at least 100; if the new-day update does not reset the swimming flag; if any target-802 premise is false for the serialized save; if state machine 502 does not leave the player's scene; or if leaving the scene preserves H and the same group target search. The writer trace, serialized values, target ordering, one unseeded production state-machine sample, and the cited movement/H cleanup paths each reject those alternatives.

The saved Fable review prompt actively challenged this closure, but the required high-effort invocation timed out without a verdict. Under the user's fallback authorization, the route is frozen from the verified source and runtime facts; the timeout is not recorded as approval.
