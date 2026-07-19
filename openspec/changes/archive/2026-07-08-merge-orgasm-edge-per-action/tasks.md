## 1. Regression Test First (red)

- [x] 1.1 Add `mod/tests/bdd/test_bdd_save_edge_window_merge.py` (near-real layer, save 99, skip-if-missing): boot via `boot_game_once`, stub `get_wait_response`, load slot 99, seed RNG, place 陈(10) thresholds (`status_data[23]=990/orgasm_level[23]=2`, `status_data[4]=990/orgasm_level[4]=2`), instrument `judge_orgasm_edge_success` call count per character, drive `handle_wait_1_hour()`.
- [x] 1.2 Assert per-character roll count ≤ 1 per player action window; run and confirm it goes RED on current code (杜宾 same-settle 2×, 陈 cross-settle 2×).
- [x] 1.3 Add merged-counting assertion: 陈's `orgasm_edge_count` delta equals the sum of all crossing parts' climax counts (merged, not skipped).
- [x] 1.4 Add failure-path scenario with the roll stubbed to fail: `orgasm_edge == 3` and failure-release settlement still runs in later passes.

## 2. Implement Window-Merged Edge Judgment

- [x] 2.1 In `mod/local_h_orgasm_batch_fix/scripts/h_orgasm_batch.py`, add module-level edge window cache (`_EDGE_WINDOW_OVER_OBJECT`, `_EDGE_WINDOW_RESULTS`) keyed on `cache.over_behavior_character` object identity (pattern from `local_group_masturbation_intent_fix`).
- [x] 2.2 Rework the edge branch of `patched_orgasm_settle` (currently lines 579-590) into two phases: collect `edge_crossed_parts` (part → climax_count) inside the part loop; judge once after the loop.
- [x] 2.3 First crossing in a window: call `judge_orgasm_edge_success` once (draw governed by existing `_suppress_draw_when_needed`), store result and parts in the window cache; later crossings reuse the stored result silently.
- [x] 2.4 On success, add every merged part's climax count to `orgasm_edge_count`; on failure, set `orgasm_edge = 3`, flush the batch, and return (existing behavior, unsuppressed).
- [x] 2.5 Keep the time-stop (`unconscious_flag_3`) branch, roll formula, and edge release settlement (effect 529 / group-sex end) untouched.

## 3. Implement Multi-Part Display Scheme

- [x] 3.1 When multiple parts merge in the rolling settlement pass, draw one part-list line after the original prompt (part names via `ORGASM_PART_NAME_BY_PREFIX`), same suppression rules as the prompt; single-part display stays byte-identical to today.
- [x] 3.2 Queue exactly one representative `{part}_orgasm_edge` second behavior via `_queue_second_behavior` (highest merged climax count, ties random); no edge talk for other merged parts or for silent later-pass merges.

## 4. Verification and Cleanup

- [x] 4.1 Run the new BDD test and confirm GREEN; run the full `mod/tests/` suite including save-99 E2E full flow (wait → group_sex_end → rest) with no error.log growth. (Near-real BDD 6 passed; web E2E 4 passed on host — codex sandbox could not bind ports, host run succeeded.)
- [x] 4.2 Re-run the original diagnosis scenario (un-minimised) and confirm no character rolls or prompts more than once per click.
- [x] 4.3 Update `mod/local_h_orgasm_batch_fix` README/mod_info description to document the per-window edge merge semantics.
- [x] 4.4 Delete `debug_edge_loop.py`; grep `[DEBUG-edg1]` to confirm no instrumentation remains.
