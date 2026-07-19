## Why

The group hypnosis boost visibly grants `pain_as_pleasure` to later participants without changing their current `unconscious_h` state, but the local settlement patch silently requires an active hypnosis unconscious state before honoring that flag. A conscious later joiner can therefore show the feature as enabled while still gaining ordinary pain.

## What Changes

- Treat the granted `hypnosis.pain_as_pleasure` flag itself as sufficient activation for positive pain conversion, regardless of the character's sleep or unconscious state.
- Convert positive pain through every supported route, including common settlement aliases and direct second effects, without forcing or changing `unconscious_h`.
- Preserve ordinary negative pain reduction, dead-character guards, cancellation/reset clearing, and upstream-compatible requested-value change accounting.
- Cover later discovered and directly invited group participants through admission, participant resolution, boost application, and real pain settlement in one connected regression path.
- Post converted psychological pleasure even while the target is asleep or unconscious, as an explicit, documented exception to the upstream state-23 guard (user decision, 2026-07-10).

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-bugfixes`: Replaces the previous hypnosis-state gate with flag-driven activation while retaining clearing and non-positive settlement behavior.

## Impact

- Affects `local_pain_as_pleasure_fix`, its common-settlement aliases, direct pain effect wrappers, and group integration tests.
- Changes the documented meaning of an existing persistent flag; save data remains compatible and no CSV IDs change.

## Current Status

Upstream PR [#212](https://github.com/Godofcong-1/erArk/pull/212) now carries the independently reviewed core signed-delta routing slice: positive pain that reaches the router follows the raw `pain_as_pleasure` flag, non-positive pain remains pain, and direct positive-pain effects use the same destination rule. Its two-file production diff passed 27 focused local tests and real Tk A/B review.

That PR does not complete this broader local-mod change. Admission-to-boost coverage, the explicit sleep/unconscious exception, cancellation and full-reset behavior, and maintained-mod alias/load-order verification remain open. Do not mark this change complete or synchronize its broader contract into the maintained `local-bugfixes` specification solely because PR #212 is open.
