## Why

`mod/local_bugfix` has grown into a bundled patch set whose fixes have different root causes, different install value, and uneven test evidence. Splitting it into smaller self-contained bugfix mods will make each fix easier to explain, verify, disable, and maintain while preserving the current player-facing behavior when all replacement fixes are enabled.

## What Changes

- Split `mod/local_bugfix` into independently installable bugfix mod components after a root-cause audit, rather than mechanically splitting by the old README symptom list.
- Move the current monolithic `local_bugfix` implementation into a deprecated backup location and treat the new split components as the active source of truth.
- Require each split bugfix component to have standalone documentation, unit-test coverage, and a real-game or near-real-game BDD verification scenario.
- Minimize dependencies between split components; when a dependency is unavoidable, declare it and enforce or verify load order instead of relying on manual `mod_config.json` ordering.
- Keep all replacement bugfix components enabled by default so the default local setup remains behaviorally equivalent to the current enabled `local_bugfix` bundle.
- Audit `group_sex_extension` and `local_performance` without splitting them, adding missing TDD/BDD coverage where their behavior can introduce regressions.
- Absorb the `fix-playtest-corner-case-regressions` items that already belong to `local_bugfix`, specifically hypnosis persistence/talk safety and H orgasm batch runtime safety, and trim those absorbed deltas from that change so it retains only its deferred UI panel scope.
- Defer the lower-priority UI panel stability issues from `fix-playtest-corner-case-regressions`, including title startup, save pagination, settings duplication, and disabled AI dialogue recovery.

## Capabilities

### New Capabilities

- `local-mod-componentization`: Defines how local mods are split, documented, dependency-checked, default-enabled, deprecated, and verified with isolated TDD plus BDD scenarios.

### Modified Capabilities

- `local-bugfixes`: Requires root-cause-based decomposition of current `local_bugfix` behavior into independent bugfix components, with isolated tests and documentation for each resulting component.
- `h-orgasm-settlement`: Requires the H orgasm batch behavior to remain runtime-safe and verifiable as its own installable bugfix component or as an explicitly declared dependency.
- `group-sex-extension`: Adds audit and verification requirements for the existing group-sex extension without splitting its three related commands, and extends the hypnosis boost contract to leave incomplete-hypnosis targets unchanged.
- `tk-rendering-performance`: Adds audit and verification requirements for the local Tk performance optimization, including stale-input safety and mode-specific behavior.

## Impact

- Affected files will include `mod/local_bugfix`, new `mod/<bugfix-id>` directories, `mod/mod_config.json`, local mod tests, and OpenSpec documentation.
- `Script/Core/mod_manager.py` may need targeted changes if dependency validation or dependency-aware load ordering cannot be achieved safely through existing configuration.
- Existing `group_sex_extension` and `local_performance` implementations stay structurally intact but receive additional tests and BDD verification notes.
- No direct work is planned for title screen, save-list, settings-panel, or disabled-AI-dialogue UI bugs in this change.
- `openspec/changes/fix-playtest-corner-case-regressions` will be trimmed to its deferred UI panel scope; its `ui-panel-stability` delta is not affected.
