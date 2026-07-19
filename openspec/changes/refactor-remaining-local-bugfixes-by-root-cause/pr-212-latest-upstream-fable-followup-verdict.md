**PASS**

- The blocking ambiguity is resolved and I verified it against the repo: `base_chara_state_common_settle` at `Script/Settle/base_normal_settle.py:59` computes `time_base_value = add_time + base_value`, and the helper (`Script/Settle/common_default.py:666`) passes `pain_value` as the positional `add_time` and `0` as `base_value` — so the forwarded delta is exactly `pain_value`, with no hidden +30 default.
- The psychological adjustment is applied once, inside canonical state-23 settlement, not duplicated in the helper — no double-adjustment risk, and `tenths_add=False` keeps the conversion 1:1 before the canonical multipliers.
- The 28 focused tests run the extracted real production functions and assert both the forwarded delta and a single canonical adjustment call, which falsifies the two failure modes that mattered (wrong base offset, double adjustment).
- The two-group Tk A/B plan (trait present vs. absent, same seed/route) is the right comparison surface for this behavior change; no revision needed.

One non-blocking housekeeping note: the working tree currently holds this helper inside an unresolved merge conflict (`common_default.py` and `Second_effect.py` are both `UU`; the reviewed code is the HEAD side of the `<<<<<<<` block). The conflict must be resolved before the candidate is shippable, but it doesn't change the semantic verdict.
