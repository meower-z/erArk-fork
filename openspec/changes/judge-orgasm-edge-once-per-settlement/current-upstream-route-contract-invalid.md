# Current-upstream Tk route contract: only one real wait

Static input-flow tracing plus the attempt4 frame hashes prove that the former 38-input route did not execute six `[6001]` waits. It executed the first wait once, then remained inside the result `WaitDraw` confirmation.

After player settlement draws the yellow result, `character_behavior.py` enters `WaitDraw`. `askfor_wait()` exits only on empty input or a mouse confirmation. A nonempty `6001` submission is consumed without breaking that pause loop; the Return handler does not independently set the mouse-confirmation flag. Therefore the five later `6001` submissions in attempt4 never began new waits.

The six supposed post-wait frames provide direct corroboration: all are exactly 830,208 bytes with identical PNG SHA-256 `00f5d13c45e2fd43a8a9612dbaa9c70e0de06abf1800cf0ca3acf495708bc2e5`. Attempt7's corresponding first result has a different PNG encoding but the exact same 2100×1079 decoded RGB raster SHA-256 `a16009f709c1885cd214e66f60bf99faeb0c997f3843dc0e23f29ef875987536`.

The diagnostic wrapper's entry predicate was correct: depth 0, update depth 1, behavior `wait`, duration 5. Its `finally` never ran because the same call remained blocked in result confirmation. Flushing before `WaitDraw` would omit later NPC work and cannot answer diagnostic A.

The smallest normal-player correction is one empty Return after each settled result frame before the next `6001`. For six real waits this adds six physical inputs, changing the route total from 38 to 44. No corrected run has been started.
