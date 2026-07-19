/investigate-game-bug

This is the single permitted follow-up to your read-only minimal-boundary review of T4, time-stop release attribution. The project investigation skill's diff-scoring rule changed after that review; use the current skill text and the new `(a + b) + S - 2U` rule. Please make the final decision. Do not edit files.

Factual correction: the two-line candidate you chose has a first source line of 203 characters including its 8-space indentation, not 196. This project uses Black with line width 200, so that exact line violates the repository style boundary.

The required behavior remains:
- When at least one deferred time-stop orgasm count is positive, pass the NPC-owned `TargetChange` to `orgasm_settle` so visible gains belong to that NPC.
- When every deferred count is zero, preserve the existing root `change_data` call so no empty NPC section is created.
- Keep this fix local to `handle_time_stop_orgasm_release`.

Writer/lifecycle evidence on current upstream 72e28051e:
- `time_stop_orgasm_count` starts as `{}`.
- migration and character recalculation only add/copy values or zeroes.
- the sole gameplay writer is `second_behavior.orgasm_settle`: it reaches the time-stop write only when normal, extra, or uncounted orgasm data is positive; it then adds `climax_count = normal_orgasm_data + un_count_orgasm_data`.
- release/reset paths write zero.
- No production writer of a negative count was found. However, copied/deserialized legacy values are not explicitly clamped.

Two style-compliant choices:

A. Preserve the explicit positive-count condition through an alias. The production diff has one change group: `a=3`, `b=1`, net expansion 2 so `S=1`, `U=0`; penalty `(a+b)+S-2U = 5`. Line lengths are 70, 172, 105:

    release_counts = character_data.h_state.time_stop_orgasm_count
    settlement_change = change_data.target_change.setdefault(chara_id, game_type.TargetChange()) if any(count > 0 for count in release_counts.values()) else change_data
    second_behavior.orgasm_settle(chara_id, settlement_change, un_count_orgasm_dict = release_counts)

B. Use truthiness of the values directly. The production diff has one change group: `a=2`, `b=1`, net expansion 1 so `S=0`, `U=0`; penalty `(a+b)+S-2U = 3`. Line lengths are 180, 136:

    settlement_change = change_data.target_change.setdefault(chara_id, game_type.TargetChange()) if any(character_data.h_state.time_stop_orgasm_count.values()) else change_data
    second_behavior.orgasm_settle(chara_id, settlement_change, un_count_orgasm_dict = character_data.h_state.time_stop_orgasm_count)

B is smaller, but a negative legacy value would count as active whereas A would not. Choose the final hunk under the investigation skill's correctness-first then minimum-penalty rule. State which option wins and why; if neither is acceptable, give one concrete style-compliant replacement and its `a`, `b`, `S`, `U`, and penalty.
