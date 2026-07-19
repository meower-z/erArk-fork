REVISE — but with a hard caveat: I could not open the code. This session has no file/shell tools (only two unrelated OAuth connectors), so everything below is a desk review of your written summary, not verification against the worktree at 3a1c9e620.

**Blocking question (the reason for REVISE rather than PASS):**

- Your summary says the helper calls `base_chara_state_common_settle` with `state_id=23, base_value=0, ability_level=ability[36], tenths_add=False` — and `pain_value` appears nowhere in that call. As literally described, the converted psychological pleasure would be computed from a zero base and would not scale with the pain delta, violating contract 1 ("the positive, source-adjusted pain delta is converted"). If `pain_value` is in fact passed as the settle's base value and `base_value=0` in your summary refers to something else (e.g., an `extra_adjust`-style parameter), say so or show the exact call line; then this objection dissolves.

**Contract-consistent as described (no other objections):**

- Positive-only gate + hypnosis-inactive short circuit → contracts 1–2. Callers falling through to the old state-17 write on `False` keeps negative/zero pain falling normally.
- Common-path hook checks `state_id == 17` on `final_value` (post-source-adjustment) and returns on `True` — no state-17 double write, no recursion risk (state 23 never re-enters the 17 branch).
- Ability scaling lives only in canonical state-23 settlement; helper does not call `chara_feel_state_adjust` → contract 4, no double calculation.
- Unconditional `True` after the settle call gives contract 6's "handled even when the target sleeps/is unconscious, no state-17 fallback."
- Extra orgasm: unconditional terror + counter reset, text keyed on the helper's return → contract 7.
- Mutation search finding no other positive state-17 production writer covers contract 3's bypass concern, assuming that search ran on this worktree.

**Tk A/B evidence — yes, exactly those two groups:**

- (A) negative common pain reduction with conversion active — proves the regression the original bug introduced (pain stuck / wrongly converted) is gone and pain still falls on state 17.
- (B) one direct positive pain source with conversion active — baseline shows state 17 rising, candidate shows state 23 rising. One representative direct writer suffices; you don't need all three sizes plus extra orgasm on screen.

Next step: rerun this review in a session with repo access (or paste the helper body and the three call sites), resolving the `pain_value`/`base_value=0` question. If the delta is actually forwarded as the settle base, this flips to PASS on the described scope.
