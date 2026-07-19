## 1. Baseline and Scope Control

- [x] 1.1 Confirm the deferred UI issues from `fix-playtest-corner-case-regressions` are excluded from implementation notes and task scope.
- [x] 1.2 Inventory current `mod/local_bugfix` manifest entries, script functions, registry patches, README sections, and tests.
- [x] 1.3 Inventory current `group_sex_extension` and `local_performance` manifests, script entry points, and tests for audit scope.
- [x] 1.4 Record the current `mod/mod_config.json` enabled mods and load order before migration.
- [x] 1.5 Run the current local mod test files as a baseline and record failures, skipped areas, and environment assumptions.
- [x] 1.6 Trim the absorbed hypnosis persistence and H orgasm batch deltas and related tasks from `fix-playtest-corner-case-regressions`, leaving that change scoped to only the deferred UI panel stability work.

## 2. Root-Cause Audit Matrix

- [x] 2.1 Build an audit matrix mapping each old `local_bugfix` symptom to upstream patch points, current tests, suspected root cause, and candidate component.
- [x] 2.2 Audit group-mode player target preservation and decide whether it is independent or part of a broader group AI state component.
- [x] 2.3 Audit player/NPC movement interruption fixes and decide whether stale movement cleanup is one component across H, group mode, and NPC active-H paths.
- [x] 2.4 Audit group-mode automatic masturbation marker routing and repeated-settlement prevention and decide whether they form one intent-lifecycle component.
- [x] 2.5 Audit tired group-sex discovery auto-leave and confirm whether it shares root cause with group participant cleanup or remains separate.
- [x] 2.6 Audit hypnosis mode persistence and hypnosis talk gate fixes, including normal-scene and H-mode mind-control flows.
- [x] 2.7 Audit pain-as-pleasure cancellation, non-positive pain handling, and direct second-effect pain conversion and decide whether they form one settlement-consistency component.
- [x] 2.8 Audit group-mode pending edge release before H reset, including one-NPC exits, group-to-H transition, unconscious recovery, stale template participants, and sleep-leak prevention.
- [x] 2.9 Audit H orgasm batch settlement behavior, including display batching, queue clearing, remote draw suppression, human-power aggregation, hypnosis second talk, and achievement runtime safety.
- [x] 2.10 Record reproduction attempts for historical symptoms that cannot be reproduced on the current codebase, and decide whether each retained guard is justified by a still-valid invariant or removed.
- [x] 2.11 Identify patches implemented as full upstream reimplementations rather than narrow wrappers (for example `judge_character_h_obscenity_unconscious`), and record their upstream-drift risk and re-sync strategy.
- [x] 2.12 Finalize the component boundary list and dependency graph from audit evidence before moving code.

## 3. Dependency and Loader Verification

- [x] 3.1 Add or identify a mod-loader smoke harness that can enable one mod plus declared dependencies without loading unrelated local mods.
- [x] 3.2 Verify current `ModManager` behavior for `dependencies`, `incompatible`, `load_priority`, and `load_order`.
- [x] 3.3 If dependencies are not enforced, implement narrow dependency diagnostics and dependency-before-dependent ordering for enabled mods.
- [x] 3.4 Add tests for missing dependency diagnostics, dependency load ordering, and independent no-dependency component loading.
- [x] 3.5 Ensure dependency changes do not alter load order for mods with no declared dependency relationship.

## 4. Split Local Bugfix Components

- [x] 4.1 Create the first no-dependency bugfix component from the finalized boundary matrix with its own `mod_info.json`, script, README, and tests.
- [x] 4.2 Migrate group-mode target preservation behavior into its responsible component or document why it merged with or split across other components.
- [x] 4.3 Migrate stale movement interruption behavior into its responsible component or document why it merged with or split across other components.
- [x] 4.4 Migrate group-mode masturbation marker lifecycle behavior into its responsible component or document why it merged with or split across other components.
- [x] 4.5 Migrate tired group-sex discovery auto-leave behavior into its responsible component or document why it merged with or split across other components.
- [x] 4.6 Migrate hypnosis mode persistence and talk-gate behavior into its responsible component or document why it merged with or split across other components.
- [x] 4.7 Migrate pain-as-pleasure settlement consistency behavior into its responsible component or document why it merged with or split across other components.
- [x] 4.8 Migrate group-mode pending edge release behavior into its responsible component, or document why it merged with or split across other components, including any dependency on the H orgasm batch behavior.
- [x] 4.9 Migrate H orgasm batch settlement behavior into its responsible component and, if the audit keeps dependent cleanup separate, expose any required batch-state hook through a declared dependency.

## 5. Component TDD Coverage

- [x] 5.1 Move or rewrite existing `test_local_bugfix_mod.py` coverage into the responsible split component test suites.
- [x] 5.2 Move or rewrite existing `test_group_sex_edge_release_mod.py` coverage into the responsible split component test suite.
- [x] 5.3 Move or rewrite existing `test_h_orgasm_batch_mod.py` coverage into the H orgasm batch component test suite.
- [x] 5.4 Add missing unit tests discovered during audit for any surface-only historical fixes.
- [x] 5.5 Ensure each component unit test can run without importing unrelated split components.
- [x] 5.6 Run each component unit test suite independently and record the command in the component README.
- [x] 5.7 Ensure the H orgasm batch regression tests reproduce the settlement path recorded in the playtest `error.log` traceback, covering multi-part or repeated orgasm settlement reaching the translated achievement call.

## 6. BDD Verification Scenarios

- [x] 6.1 Define a BDD template for local mod verification with setup, enabled mods, action, expected state or visible result, automation status, and evidence.
- [x] 6.2 Add a BDD scenario for each split bugfix component using real game loading or a near-real harness.
- [x] 6.3 Add a BDD scenario for hypnosis mind-control persistence in normal scene flow.
- [x] 6.4 Add a BDD scenario for hypnosis mind-control persistence in H-mode flow.
- [x] 6.5 Add a BDD scenario for H orgasm batch runtime safety covering the translated achievement path.
- [x] 6.6 Add a BDD scenario for dependency failure or ordering behavior when a dependent component is enabled without its dependency.

## 7. Audit Existing Maintained Feature Mods

- [x] 7.1 Expand `group_sex_extension` tests to verify command registration for all three commands and the custom hypnosis premise.
- [x] 7.2 Expand `group_sex_extension` tests or BDD coverage for participant collection from group templates and current-scene H-state characters.
- [x] 7.3 Confirm `group_sex_extension` works without split local bugfix components enabled unless a dependency is explicitly declared.
- [x] 7.4 Expand `local_performance` loader smoke coverage for replacement targets without split local bugfix components enabled.
- [x] 7.5 Add or record a `local_performance` BDD wait-flow scenario proving stale input is drained without swallowing fresh next-panel input.
- [x] 7.6 Confirm `local_performance` web-mode and benchmark-mode behavior remains scoped as documented.
- [x] 7.7 Add or expand tests verifying `全员催眠增强` applies sensitivity and pain-as-pleasure boosts to complete-hypnosis targets while leaving their hypnosis unconscious state and all incomplete-hypnosis targets unchanged.

## 8. Migration and Deprecated Backup

- [x] 8.1 Move the current `mod/local_bugfix` implementation into `mod/deprecated/local_bugfix/` after equivalent split components pass tests.
- [x] 8.2 Remove active `local_bugfix` from default `enabled_mods` and `load_order`.
- [x] 8.3 Add all replacement bugfix component ids to default `enabled_mods` and `load_order` in dependency-safe order.
- [x] 8.4 Update documentation to describe the mapping from deprecated `local_bugfix` to replacement component ids.
- [x] 8.5 Confirm the deprecated backup is not scanned as an active mod by default.

## 9. Final Verification

- [x] 9.1 Run isolated unit tests for every split bugfix component.
- [x] 9.2 Run initial loader/config smoke tests for every split bugfix component with only itself and declared dependencies enabled.
- [x] 9.3 Run full local maintained mod tests for replacement bugfix components, `group_sex_extension`, `local_performance`, and unchanged enabled local mods.
- [x] 9.4 Run syntax/import validation for all new or moved mod scripts.
- [x] 9.5 Document all BDD scenarios and record manual/full-flow coverage that remains pending.
- [x] 9.6 Historical strict validation was recorded before the follow-up audit; rerun is tracked below.

## 10. Follow-up Audit Fixes

- [x] 10.1 Replace the initial manifest/sort smoke with real `ModManager.load_all_enabled_mods()` coverage for each split component and declared dependencies.
- [x] 10.2 Harden `ModManager` diagnostics for enabled-but-missing mods, duplicate `mod_id`s, and failed-load rollback of declared function/asset mutations.
- [x] 10.3 Fix split component runtime invariants for movement-plan cleanup, hypnosis talk predicate use, stale group-edge cleanup-only release, and stale group participant filtering.
- [x] 10.4 Harden `local_performance` dynamic cache/web-mode scoping and fail-closed replacement validation while keeping broad input-token redesign out of scope.
- [x] 10.5 Fix fake module leakage in focused split/local performance tests.
- [x] 10.6 Add focused regression tests for the follow-up fixes.
- [x] 10.7 Run the feasible targeted pytest/direct Python verification commands and record unavailable tooling.
- [x] 10.8 Execute full manual BDD/game-flow scenarios in a running game session. (2026-07-06/07: executed automated in a real running game session — web driver over a live game.py process with the user's real Windows saves, covering load→group-AI→group_sex_end→rest full flows; evidence per scenario in bdd-scenarios.md. Tier-3 Windows manual playtest remains a user-side follow-up outside this change.)
- [x] 10.9 Rerun `openspec validate modularize-local-bugfixes-and-audit-local-mods --strict` in an environment with the OpenSpec CLI available.
