# Current-upstream diagnostic attempt 6: invalid probe field

Attempt 6 has no diagnostic-A result. It reached physical input 28/38—the first `[6001]` and its Return—then the evidence probe raised `AttributeError` before settlement by reading nonexistent `character_data.sp_flag.group_sex_mode`.

That field is global `cache.group_sex_mode` on this baseline, not part of per-character `SPECIAL_FLAG`. It was an extra before/after snapshot field and is unrelated to Fable's required orgasm input dictionaries, `orgasm_edge_count`, `orgasm_level`, or the target-601 `premise_data`. The remaining five waits were not entered.

The captured error page is 2100x1079 with SHA-256 `b251956bac3d9360b921939a291d4eb5782eb45812b7b745946f260778e03ca5`, not the required no-disturbance frame hash `00f5d13c45e2fd43a8a9612dbaa9c70e0de06abf1800cf0ca3acf495708bc2e5`; the hard gate correctly invalidated the run.

The game error handler rewrote the isolated runtime's save copies. Those contaminated files were retained with the diagnostic package and will not be reused. The authoritative source save remained unchanged at `6bcd68f4e9a14460206c7e29f61980c27d9b1fce41f25d03aa44dd40d44e59cf` and `534ba3960ebe29bb020cad68499b1622b9f8f4a54669dd4b79c49ed525b26b63`.

The retained `INVALID.md` has SHA-256 `edf2f5af103b714f8fb21ac945d8b6fb99b949b97172e0d5bfe44d70509ddfee` under `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt6/`. Allocator, runtime, control files, and disposable worktree registration were cleaned.
