## Why

OpenSpec was added after several local mods had already been implemented and loaded through `mod/mod_config.json`. This change backfills those local changes into OpenSpec so future work can see what behavior exists, why it was added, and which bugs it fixed.

The scope is the locally ignored mod set currently enabled in this workspace: `easy_mode`, `local_bugfix`, `group_sex_extension`, `local_fontfix`, and `local_performance`. Upstream-tracked mods are not included in this retrospective sync.

## What Changes

- Record the local bug fixes around movement, H-state interruption, group-mode AI target preservation, group-mode masturbation routing, tired/sleep rejudgement, active-H movement cancellation, and pain-as-pleasure settlement.
- Record the group-mode convenience commands added by `group_sex_extension`.
- Record the `easy_mode` tuning for hypnosis progress, sanity growth, and hotel room prices.
- Record the desktop Tk font registration fix.
- Record the desktop Tk rendering/input performance fixes.
- Mark the tasks as already implemented because this change documents existing local behavior rather than proposing new code.

## Capabilities

### New Capabilities

- `local-bugfixes`: Local movement, H-state, group-mode AI, and pain-settlement fixes loaded by `local_bugfix`.
- `group-sex-extension`: Group-mode batch commands loaded by `group_sex_extension`.
- `easy-mode-tuning`: Local tuning loaded by `easy_mode`.
- `tk-font-registration`: Windows private font registration loaded by `local_fontfix`.
- `tk-rendering-performance`: Tk rendering and wait-input fixes loaded by `local_performance`.

### Modified Capabilities

- None. The project had no OpenSpec specs before this retrospective sync.

## Impact

- Documents ignored local mod directories under `mod/`.
- Does not change game code.
- Does not add `.codex/`, `.claude/`, or `openspec/` to Git tracking; those paths remain locally excluded.
