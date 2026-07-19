## 0. Pause State and Resume Gate

- [x] 0.1 Record the complete call graph, experimental implementation, wrapper risks, adjacent paths, and unexecuted test state in `implementation-notes.md`
- [x] 0.2 Write the narrow full-scene `place_all_not_h` candidate and replace its registry/module aliases; it remains unverified
- [x] 0.3 Write the experimental exact-once ownership candidate and component tests; they remain unaccepted and unexecuted
- [x] 0.4 Discuss global wrapper versus explicit core ownership versus postponement with the user before changing the exact-once implementation — decided 2026-07-10: postpone; remove the global wrapper experiment, keep only the `place_all_not_h` premise fix
- [x] 0.5 Decide whether non-admission hidden-discovery choices belong to this change or remain explicitly out of scope — decided 2026-07-10: out of scope, deferred to the future ownership design

## 1. Prove Settlement Ownership

- [ ] 1.1 Build a near-real NPC state-machine reproduction that records the discovery callback, nested player update, outer NPC settlement, behavior IDs, and `is_h` transitions
- [ ] 1.2 Build the corresponding direct hidden-discovery reproduction with no outer NPC settlement
- [ ] 1.3 Audit acceptance, refusal, interruption, tired auto-leave, and exception exits for dropped, doubled, or stale settlement state
- [ ] 1.4 Prove behavior for direct `find_character_target()` callers, no-outer-settlement returns, caught exceptions, same-NPC nesting, different-NPC interleaving, and hot/repeated mod loading
- [ ] 1.5 Prove wrapper composition with `local_group_masturbation_intent_fix` in both load orders without relying only on `__module__`

## 2. Implement Admission and Premise Fixes

- [ ] 2.1 Introduce an explicitly scoped discovery-settlement ownership context and one-shot suppression for early settlement
- [ ] 2.2 Settle initial conversion before the nested update and make existing-group acceptance/refusal work in both caller contexts exactly once
- [ ] 2.3 Correct `place_all_not_h` to inspect the full scene and replace both the runtime premise registry entry and implementation alias

## 3. Verify Connected Behavior

- [ ] 3.1 Add failing-then-passing regressions for both panel callers, including exact effect counts and exception cleanup
- [ ] 3.2 Connect admitted `is_h` state to player target switching, normal group controls, participant resolution, and the absence of a contradictory invite control
- [ ] 3.3 Run focused component and near-real group tests only after the path audit is complete, then inspect the actual diff and run relevant group regression suites
- [ ] 3.4 Add the two omitted critical component tests to the direct `main()` runner or document pytest as the only complete runner before using the README command as evidence
