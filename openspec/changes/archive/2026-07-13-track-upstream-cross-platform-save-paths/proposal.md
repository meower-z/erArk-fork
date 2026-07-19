## Why

Save files persist game room addresses using the source operating system's separator, so loading them on another operating system can make valid scenes look obsolete and discard their character registrations. The archived audit records the original investigation, while upstream PR #207 now provides a focused ordinary-load fix that needs a current behavioral contract and a safe local-mod retirement gate.

## What Changes

- Define cross-platform loading for the enumerated structured room-address fields in save data.
- Normalize those fields immediately after deserialization and before version migrations and map reconciliation.
- Preserve already-native addresses and avoid rewriting dialogue, descriptions, or other ordinary strings.
- Record upstream PR #207's merge and the verified retirement of `local_cross_platform_save_fix` after the normal post-load compatibility checks passed.

## Capabilities

### New Capabilities

- `save-portability`: Covers loading saves whose structured room addresses use a different operating-system separator without losing scene or map state.

### Modified Capabilities

None.

## Impact

- Upstream patch point: `Script/Core/save_handle.py`.
- Former transitional local owner: `mod/local_cross_platform_save_fix` (retired after upstream adoption).
- Upstream review: `Godofcong-1/erArk#207` from `meower-z:codex/fix-cross-platform-save-paths`.
- The save format is unchanged; compatibility work remains at the load boundary.
- Upstream PR #207 merged as `16960e1b89e72da0d5a31ef5e716c0368cd0b924` on 2026-07-13. Current `main` matches the merged source file, and the duplicate local mod and configuration entries have been removed.
