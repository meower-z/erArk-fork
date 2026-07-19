**PASS**

Verified directly against the candidate worktree (`c72d25a54` + one commit-pending deletion; `git diff c72d25a54` shows exactly 1 file, 1 line deleted, nothing else).

1. **Verdict: PASS.** The deletion accurately fixes the confirmed double application and touches nothing else.

2. **Common path: two applications → one.** Confirmed in source: `bad_state_set = {18, 19, 20}` (common_default.py:211), so state 17 passes the `state_id not in bad_state_set` gate and the common path multiplies `continuous_adjust` into `final_adjust` before computing `final_value` (common_default.py:235-256). That already-adjusted value is what reaches `route_pain_delta` as `pain_value`. The old helper multiplied `continuous_adjust` a second time; the candidate helper now applies only `chara_feel_state_adjust(character_id, 23, ability[36])`. Exactly one continuous adjustment survives, matching the un-routed state 17 behavior (which also applies it once).

3. **Direct writers unchanged.** All four Second_effect.py call sites (1247, 1840, 2626, 3201) pass two arguments, so `continuous_adjust` defaults to 1. Old code multiplied by 1 (no-op); candidate skips the multiply. Numerically identical on every direct-writer path, positive or non-positive, pain_as_pleasure on or off.

4. **ability[36] computed exactly once.** The only place `ability[36]` enters the pain→pleasure conversion is the single `chara_feel_state_adjust(character_id, 23, ...)` call inside the helper (common_default.py:46). The common path's earlier `chara_base_state_adjust` uses state 17 and the caller-supplied ability level, not ability[36]/state 23. No duplication before or after the fix.

5. N/A — no defects found in the deletion.

One factual note for the PR record: the reviewer's wording ("能力加成重复") misnames the duplicated factor; the code evidence confirms your reading — the duplicate was the 连续指令系数, and ability[36] was never applied twice. Worth keeping the PR text on the correct factor. The now-unused `continuous_adjust` parameter is retained per your explicit constraint; it documents the routing contract and removing it was out of scope.
