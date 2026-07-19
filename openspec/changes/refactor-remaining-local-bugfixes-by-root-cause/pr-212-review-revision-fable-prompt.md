/investigate-game-bug

You are supervising the design revision for erArk upstream PR #212. Decide whether the supplied root-cause record and revised task boundary are accepted. Do not invent repository facts, edit files, or decide outward-action authorization.

Verified facts:

- The live PR head is `21261e951` and currently changes `Script/Settle/common_default.py` plus `Script/Settle/Second_effect.py` through a new `route_pain_delta` helper.
- The only unresolved maintainer thread is on `common_default.py`: “直接在这里判断苦痛是否为正就可以了，不需要再单独构建函数，以及单独构建的那个函数的里会导致重复计算两遍心理快感的能力加成”.
- Latest `upstream/master` is `abebf33b52ebf51424f71365946eb8df1f75a23c`.
- In upstream `base_chara_state_common_settle`, `final_value` is computed after state adjustment, optional tenths contribution, and integer conversion. The existing conversion condition then recursively calls the same function for state 23 whenever `state_id == 17` and the pain-as-pleasure premise is true; it does not check the sign.
- A focused probe that executes the production function confirms the upstream baseline fails the active-negative case: negative state 17 is not reduced and psychological pleasure is reduced instead. The same probe confirms active positive state 17 already uses the existing state-23 recursion.
- The current PR's old Tk images cover the broader two-file candidate. They will not be reused. A fresh real-Tk baseline/candidate pair will be captured for the revised code.
- The user asked to revise the PR and PR draft according to the maintainer's new design.

Proposed violated rule and owner:

`苦痛快感化` changes the interpretation of pain gain. A final pain delta that is zero or negative remains ordinary state-17 settlement. The existing conversion condition in `base_chara_state_common_settle`, after `final_value` is computed, owns this admission rule.

Alternatives considered:

1. Chosen: add `final_value > 0` to the existing conversion condition, preserve the original state-23 recursive call, and revert every `Second_effect.py` change and the helper/type-import changes.
2. Current PR: shared router plus direct second-effect migration. Rejected for this revision because the maintainer rejected the helper and the reported visible defect does not require direct-writer migration.
3. Guard raw `add_time` or `add_time + base_value`. Rejected because that is not necessarily the sign of the final settled integer.

Required causal radius:

- active negative and zero final deltas stay on state 17;
- active positive final deltas still use the existing state-23 recursion exactly once;
- inactive state-17 behavior is unchanged;
- direct second-effect writers, sleep/unconscious semantics, hypnosis-flag lifetime, balance tuning, and extra-orgasm text are outside this revised PR and must be removed from PR claims.

The durable design record is `openspec/changes/refactor-remaining-local-bugfixes-by-root-cause/pr-212-review-revision.md` and contains the same verified facts and alternatives.

Questions:

1. Is the existing conversion condition the correct logical owner, and is the one-condition change the smallest coherent root-cause fix under the maintainer's instruction?
2. Must all `Second_effect.py` and shared-helper changes be removed from this PR?
3. Does this revision preserve the positive inverse while avoiding duplicate psychological-pleasure calculation?
4. Is the design record accepted for implementation, or what exact evidence/design gap remains?
5. Is player input required before implementation?

Return a concise verdict beginning with ACCEPT, REVISE, or BLOCKED. Name any required change and explicitly state whether player input is required.
