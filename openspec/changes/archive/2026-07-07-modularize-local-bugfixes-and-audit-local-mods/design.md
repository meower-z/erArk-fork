## Context

The local mod set currently mixes different ownership shapes:

- `mod/local_bugfix` is a monolithic bundle containing unrelated bugfixes, H settlement changes, registry patches, and tests.
- `mod/group_sex_extension` is a maintained local feature mod with three closely related group-sex commands.
- `mod/local_performance` is a maintained local Tk performance and stale-input safety mod.
- `mod/easy_mode` is not locally maintained and is outside this change.

The mod loader already reads `dependencies`, `incompatible`, and `load_priority` from `mod_info.json`, but current loading is driven by `mod/mod_config.json` order and does not enforce dependency presence or dependency-before-dependent sorting. If split components depend on each other, relying only on manifest fields would be misleading.

`mod/local_bugfix`'s `mod_info.json` manifest declares only part of its patch surface: roughly half of its patches are installed imperatively at import time through `_install_registry_patches` (second-effect registry entries, panel draw hooks, state-machine handlers). The root-cause audit must therefore inventory code-level patch installation, not just manifest `functions` entries.

The in-progress `fix-playtest-corner-case-regressions` change contains some `local_bugfix`-relevant regression requirements and some lower-priority UI flow fixes. This change absorbs only the `local_bugfix`-relevant hypnosis and H orgasm batch safety items; title, save-list, settings, and disabled AI dialogue UI fixes are deferred. Once this change is accepted, the absorbed local-bugfixes and h-orgasm-settlement deltas should be trimmed from `fix-playtest-corner-case-regressions` so that change retains only the deferred UI panel scope and the two changes cannot archive overlapping requirements.

## Goals / Non-Goals

**Goals:**

- Replace `mod/local_bugfix` with smaller bugfix mods whose boundaries are based on root cause and behavioral invariants.
- Keep default local behavior equivalent by enabling all replacement bugfix components after the split.
- Make every split bugfix component independently explainable, installable, and testable with only itself and declared dependencies enabled.
- Add BDD verification scenarios that exercise real game loading or realistic game flows, not only isolated helper functions.
- Audit `group_sex_extension` and `local_performance` for regressions without splitting them.
- Preserve a deprecated backup of the current monolithic `local_bugfix` for comparison and rollback.

**Non-Goals:**

- Splitting `group_sex_extension`, `local_performance`, `local_fontfix`, `semen_boost`, or `easy_mode`.
- Implementing lower-priority UI flow fixes from `fix-playtest-corner-case-regressions`.
- Rewriting the renderer, event loop, save format, H settlement model, or mod system wholesale.
- Changing game balance or feature semantics beyond fixing confirmed bug roots.

## Decisions

### Audit before splitting

Each old `local_bugfix` behavior will first be grouped by suspected root cause, code patch point, and affected game invariant. Final component boundaries will be chosen after reading upstream functions, existing tests, README notes, and any relevant playtest evidence.

Alternative considered: split one mod per README heading immediately. That is fast, but it risks preserving weak historical boundaries and leaves related root causes fragmented.

### Components are mod directories, not submodules inside one mod

Each resulting bugfix component should be a `mod/<bugfix-id>/` directory with its own `mod_info.json`, scripts, tests, and README. This matches the current loader's install unit and gives the player a real enable/disable boundary.

Alternative considered: keep one mod directory and add internal switches. That would require a new component switch system and would not satisfy independent installation cleanly.

### Dependencies are explicit and verified

Components should avoid logical dependencies where practical. If a dependency is required, the dependent component must declare it in `mod_info.json`, and verification must confirm the dependency is enabled and loaded earlier. If the current loader cannot enforce this, implementation should add a narrow dependency validation and dependency-aware sort or fail-fast diagnostic.

Alternative considered: document manual load order only. That keeps implementation smaller but makes split components fragile and contradicts the manifest fields already exposed by the loader.

### Deprecated backup is read-only compatibility evidence

The existing `mod/local_bugfix` should be moved under a deprecated backup path and removed from active `enabled_mods` / `load_order`. The backup is for rollback, comparison, and historical documentation, not a second active implementation.

The backup path is `mod/deprecated/local_bugfix/`. The loader's `scan_mods` only checks immediate subdirectories of `mod/` for a direct `mod_info.json`, so one level of nesting reliably deactivates the backup. Renaming a top-level folder is not sufficient because the active mod id comes from `mod_info.json`, not the directory name.

Alternative considered: keep `local_bugfix` as an enabled aggregate wrapper. That reduces migration risk, but it obscures whether the split components are truly independent.

### Default config enables replacement components

The post-split default `mod/mod_config.json` should enable every replacement bugfix component, plus unchanged local mods that were already enabled. This preserves current player behavior while still allowing individual bugfix components to be tested alone.

Alternative considered: leave all split bugfix mods disabled until manually enabled. That makes installation explicit, but it changes the current local baseline and makes regression comparison harder.

### TDD and BDD are separate gates

Unit tests prove root-cause invariants in isolation. BDD scenarios prove that the component loads through the real mod system or a near-real harness and preserves behavior in a game-like flow. Both are required before a split component is considered complete.

A near-real-game harness means the component is loaded through the real `Script/Core/mod_manager.py` against unmocked `Script` modules and real configuration data, with game state driven through real cache and flow entry points; a heavily mocked module fixture counts as a unit test, not BDD. Manual BDD scenarios must record execution evidence (date, build, observed result), not only a checklist entry.

Alternative considered: rely on unit tests only. Existing coverage already shows why that is insufficient for flow, load-order, and interaction regressions.

## Risks / Trade-offs

- Component split may reveal shared helper code across bugfixes -> Prefer duplication for tiny helpers; introduce a dependency only when shared behavior is substantial and stable.
- Dependency sorting changes could affect existing user load order -> Keep sorting scoped to declared dependencies and report conflicts clearly.
- BDD game flows may be slow or hard to automate -> Start with deterministic load smoke and focused command/settlement harnesses, then add manual checklist steps only where full automation is not practical.
- Moving the old monolith can break ad-hoc local commands -> Keep a deprecated backup and document the migration path from old mod id to replacement component ids.
- Root-cause audit may merge or split the provisional groups differently from the old README -> Treat old bug observations as evidence, not as final component boundaries.

## Migration Plan

1. Inventory `mod/local_bugfix` functions, registry patches, manifest entries, README sections, and tests.
2. Build a root-cause matrix that maps symptoms, upstream patch points, current tests, and expected component ownership.
3. Add or adjust tests before moving code so the current behavior is pinned down.
4. Create split bugfix mod directories in small batches, starting with components that have no dependencies.
5. Add dependency declarations and loader validation or sorting only for components that genuinely require another component.
6. Update `mod/mod_config.json` to enable the replacement components and remove active `local_bugfix`.
7. Move current `mod/local_bugfix` into a deprecated backup directory after equivalent split components pass verification.
8. Run isolated component tests, full local mod tests, syntax/import validation, and BDD verification scenarios.

Rollback is to disable the replacement components, restore `local_bugfix` from the deprecated backup into active mod configuration, and rerun the old test suite for comparison.

## Open Questions

- Should dependency enforcement fail the entire mod load, skip only the dependent mod, or load with a visible diagnostic when a dependency is missing?
- Which BDD flows can be fully automated through a terminal/game harness, and which need a documented manual checklist?
