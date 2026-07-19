## 0. Pause State and Contract Gate

- [x] 0.1 Record the confirmed state gate root, historical spec conflict, full known path inventory, experimental code, formula/accounting gaps, and unexecuted test state in `implementation-notes.md`
- [x] 0.2 Write the raw-flag candidate, alias/direct-effect candidates, and regression cases; they remain unaccepted and unexecuted
- [x] 0.3 Ask the user to choose upstream state-23 guard preservation versus an explicit unconscious/sleep exception — decided 2026-07-10: intentional exception; pleasure posts even while asleep/unconscious
- [x] 0.4 Ask the user to choose actual applied delta versus requested-delta compatibility at the status cap — decided 2026-07-10: requested value, upstream-compatible
- [x] 0.5 Reconcile the hypnosis-exit contract with PR #213 — sleep and direct cancellation preserve `pain_as_pleasure`; the former cancellation-clears expectation is obsolete
- [ ] 0.6 After acceptance, reconcile this change with `openspec/specs/local-bugfixes/spec.md` and `fix-group-sex-invite-controls-and-idle-ai`

## 1. Audit Every Pain Route

- [ ] 1.1 Enumerate all positive and non-positive pain mutations, common aliases, direct effect registry entries, cancellation/reset paths, and later mod overrides
- [ ] 1.2 Trace discovered and directly invited participants through admission, group resolution, hypnosis boost, and pain settlement without hand-constructing the final state
- [ ] 1.3 Confirm the flag's UI and premise semantics and record the old dormant-state specification conflict
- [x] 1.4 Compare common conversion with upstream state-17 recursion, including the second consecutive-instruction adjustment, state-23 sleep/unconscious guard, cap, and both change-record owners — done 2026-07-10: line-by-line comparison against `common_default.base_chara_state_common_settle`; the missing second reduction was implemented (`_get_consecutive_instruct_adjust` + `apply_repeat_adjust`), the guard bypass is the accepted exception, cap recording matches upstream requested-value behavior
- [ ] 1.5 Verify each direct effect's own death/early-return behavior and full alias identity after supported mod load orders and repeated loading

## 2. Implement Flag-Driven Conversion

- [ ] 2.1 Make the raw granted flag the single activation predicate without mutating `unconscious_h`
- [ ] 2.2 Install the common conversion in default, second-effect, realtime, and item call paths and wrap direct effects 270, 283, 296, and 408
- [ ] 2.3 Preserve negative pain, entry-specific dead guards, persistence across sleep/direct cancellation, and correct state-23 target-change accounting
- [x] 2.4 Split the independently reviewable core signed-delta routing and direct positive-pain effects into upstream PR [#212](https://github.com/Godofcong-1/erArk/pull/212); keep the remaining local-mod activation and lifecycle work in this change
- [x] 2.5 Split the independently reviewable hypnosis-exit preservation into upstream PR [#213](https://github.com/Godofcong-1/erArk/pull/213); local `main` carries the overlay and the old pain mod is disabled
- [ ] 2.6 Remove the disabled mod's obsolete direct-cancel clearing wrapper and revise its BDD expectation to the PR #213 persistence contract during the next implementation step

## 3. Verify Connected Behavior

- [ ] 3.1 Add inactive-flag, cancel-preserves-then-pain-converts, negative-pain, direct-effect, alias identity, and real target-change regressions
- [ ] 3.2 Add a connected later-participant regression from admission through boost to real common pain conversion while remaining conscious
- [ ] 3.3 After the full audit, run focused unit and near-real BDD suites, verify full mod load order, inspect the diff, and request permission before synchronizing maintained README/spec text outside this change
- [x] 3.4 Add cap/actual-delta 0 and 1 cases, sleep/unconscious cases, repeated-instruction equivalence, simultaneous change-object ownership, historical toggle/full-reset cases, and per-entry death semantics — done 2026-07-10: the named cap, sleep/unconscious, and repeat-adjustment cases passed in a 14-test component run; the historical reset cases do not override the later PR #213 persistence contract
- [ ] 3.5 First connect the stable direct-invitation path from resolver through boost to real settlement; then connect discovered admission through the now-resolved panel-owned discovery candidate
- [x] 3.6 Include the omitted death-delegation test in the direct `main()` runner or document pytest as the only complete runner before using the README command as evidence — done 2026-07-10: `test_dead_character_positive_pain_delegates_to_original` added to `main()`; direct runner and pytest both pass
- [ ] 3.7 Audit full hypnosis cleanup and local reset callers from current production state; verify their actual owner before preserving or changing any clearing behavior
