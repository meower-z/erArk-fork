# PR #212 maintainer-review revision

> **Historical exploration, superseded.** This reviewer-following sign-guard-only design was rejected after independent reassessment because it leaves the direct positive-pain bypass unresolved. It is not the current PR implementation or draft. See `pr-212-session-closure-20260715.md`.

## Reported clue and reproduction

PR [#212](https://github.com/Godofcong-1/erArk/pull/212) currently changes `base_chara_state_common_settle` and four direct second-effect pain writers through a new shared router. The unresolved maintainer thread at commit `21261e951` asks to remove that function and test positivity directly at the existing common-settlement conversion branch because the separate calculation repeats the psychological-pleasure ability adjustment.

Against `upstream/master` `abebf33b52ebf51424f71365946eb8df1f75a23c`, a focused production-function probe confirms:

- with `pain_as_pleasure` active, a final negative state-17 delta is recursively posted as negative state 23 instead of reducing state 17;
- with the same flag active, a final positive state-17 delta already follows the existing state-23 recursion.

This record treats the old two-file branch as a disposable candidate and does not use its implementation shape as the accepted boundary.

## Violated rule and owner

`苦痛快感化` changes the interpretation of pain gain. A final pain delta that is zero or negative must remain ordinary state-17 settlement. "Ordinary" includes the existing state-17 storage, change records, and `extra_feel_settle` call; when ability 36 is at least 5, that downstream owner may still add its normal masochism-derived psychological pleasure and experience. The existing conversion branch in `base_chara_state_common_settle`, after `final_value` is computed, owns only the admission decision between this ordinary path and the pain-as-pleasure recursion.

The current upstream interface permits the failure because the conversion condition checks the state and flag but not the sign of the final delta. No new routing interface is required to enforce the rule.

## Candidate boundaries

1. **Final-value guard at the existing conversion branch (chosen):** require `final_value > 0` alongside state 17 and the existing `handle_hypnosis_pain_as_pleasure` predicate. Preserve the original recursive state-23 settlement without reimplementing its adjustment, caps, records, or guards. When the guard rejects zero or negative values, fall through to the complete ordinary state-17 path, including its existing `extra_feel_settle` side effect.
2. **Shared signed-delta router plus direct-writer migration (rejected for this PR revision):** the current PR broadens ownership to `Second_effect.py` and calculates the state-23 destination outside the existing recursive path. The maintainer explicitly rejected this function, and the original visible defect does not require the direct-writer migration.
3. **Raw-input guard before final-value calculation (rejected):** `add_time` or `add_time + base_value` is not the settled sign after state adjustment, tenths contribution, and integer conversion, so it does not enforce the actual rule.

## Causal radius and non-goals

The revised candidate must prove active negative and zero final deltas stay on state 17, active positive final deltas still use the existing state-23 recursion, and the inactive case remains unchanged. It must cover ability 36 below and at least 5 so the accepted fallthrough preserves the ordinary masochism-derived psychological-pleasure and experience side effect rather than being misreported as a complete absence of psychological change. Direct second-effect pain writers, sleep or unconscious semantics, hypnosis-flag lifetime, tuning the `extra_feel_settle` formula, and extra-orgasm text are outside this revised PR boundary and must not be claimed in its draft or evidence.

Because the submitted behavior and visible candidate result change, all PR-facing Tk baseline/candidate evidence will be captured fresh. Previously published #212 images are historical only.
