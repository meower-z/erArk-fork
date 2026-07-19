## 1. Mod Integration

- [x] 1.1 Keep core game files restored and implement the fix under `mod/local_bugfix`.
- [x] 1.2 Add `scripts/h_orgasm_batch.py` and register it from `mod/local_bugfix/mod_info.json`.
- [x] 1.3 Reuse the existing `local_bugfix` replacement of `judge_character_tired_sleep()` instead of creating a second mod that would replace the same function.

## 2. Settlement Batch Model

- [x] 2.1 Add a local orgasm batch data structure that records distinct effect behavior IDs, display representatives, plural behavior ID, plural body-part set, and human-power display state.
- [x] 2.2 Add helper functions to parse orgasm behavior IDs, compare orgasm strength, and choose representative body-part displays by highest strength with random tie-breaking.
- [x] 2.3 Add a helper that applies configured second behavior effects without drawing talk.
- [x] 2.4 Preserve original `Character.second_behavior` 0/1 semantics so identical behavior IDs in the same batch are not newly multiplied.

## 3. Orgasm Settlement Integration

- [x] 3.1 Replace `orgasm_settle()` through the mod so normal, extra, and uncounted orgasm inputs populate and flush an orgasm batch.
- [x] 3.2 Preserve existing special paths for edge release, time-stop release, extra orgasm, B orgasm milk release, U orgasm urine release, achievements, and plural orgasm effects.
- [x] 3.3 Clear or bypass legacy queued orgasm second behaviors after the batch flush so the old loop cannot double-settle or later display the same orgasm event.
- [x] 3.4 Replace `check_second_effect()` through the mod so NPC orgasm settlement no longer uses a stale pre-orgasm filter list.

## 4. Display Behavior

- [x] 4.1 Display only the strongest representative behavior per body part.
- [x] 4.2 Display the original multiple-orgasm info and corresponding talk before body-part detail in batches with at least two body parts.
- [x] 4.3 Display each orgasming body part exactly once, using original-format info-and-talk for up to three representatives and strength-only text for the rest.
- [x] 4.4 Keep existing talk selection for chosen representative behavior IDs so character-specific and common talk data remain reusable.
- [x] 4.5 Ensure a representative part's yellow strength prompt and following talk are separated by only one blank line.
- [x] 4.6 Display non-representative remaining parts as one grouped line ordered by strength.

## 5. Human Power Display

- [x] 5.1 Replace `store_power_by_human_power()` through the mod with a wrapper that normally delegates to the original function.
- [x] 5.2 During a multi-orgasm batch, suppress individual human-power draw calls, preserve original settlement calls and return values, and display one accumulated result.
- [x] 5.3 Use the original plural-orgasm human-power text format and replace only the generated power number with the batch total.

## 6. H Interruption Ordering

- [x] 6.1 Add a batch-in-progress guard that prevents HP/fatigue H interruption from resetting H while orgasm batch effects are still settling.
- [x] 6.2 Use `try/finally` cleanup so the guard is always cleared after batch flush.
- [x] 6.3 Verify the tired-sleep wrapper returns early while a target is in orgasm batch settlement.

## 7. Runtime Safety

- [x] 7.1 Avoid using `_` as a local loop variable in `h_orgasm_batch.py` where it would shadow the translation helper.
- [x] 7.2 Add a regression test proving achievement flow can still call the translated `"绝顶"` label after batch settlement.

## 8. Verification

- [x] 8.1 Add mod tests for one body part producing multiple strengths; verify only the strongest display representative remains and all distinct effects are recorded.
- [x] 8.2 Add mod tests for the stale NPC orgasm filter bug.
- [x] 8.3 Add mod tests for human-power display aggregation.
- [x] 8.4 Add mod tests for H interruption guard behavior.
- [x] 8.5 Add mod tests for compact part info spacing and grouped one-line summary.
- [x] 8.6 Run `python mod/local_bugfix/tests/test_local_bugfix_mod.py`.
- [x] 8.7 Run `python mod/local_bugfix/tests/test_h_orgasm_batch_mod.py`.
- [x] 8.8 Run `python -m py_compile` on modified mod scripts and tests.
- [x] 8.9 Validate `mod/local_bugfix/mod_info.json` with `python -m json.tool`.
