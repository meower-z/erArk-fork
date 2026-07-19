## Why

Upstream commit `b206249a5d` added `NO_TARGET_OR_TARGET_CAN_COOPERATE_OR_IMPRISONMENT_1` to instruction 5052 to block parturient or postpartum targets. That composite contradicts an unconscious action: sleeping and time-stopped targets fail its awake/cooperation branch, while imprisonment bypasses the intended pregnancy protection. Current `upstream/master` still carries this regression.

## What Changes

- Replace the contradictory cooperation-or-imprisonment composite on instruction 5052 with independent premises for unconscious state, parturient exclusion, and postpartum exclusion.
- Preserve every registered unconscious source (`unconscious_h` 1 through 7), including time stop (`3`), without special-casing a location.
- Verify the source CSV, rebuilt runtime data, and normal Tk visibility/entry behavior while preserving unrelated localization files.

## Capabilities

### New Capabilities

- `time-stop-unconscious-h-entry`: Defines when instruction 5052 is available for unconscious targets.

### Modified Capabilities

- None.

## Impact

The upstream production diff is limited to instruction 5052 in `data/csv/InstructConfig.csv`. Ignored generated `data/data.json` is rebuilt only for local verification and is not part of the public diff.

Player H-reset cleanup, generic Web dispatch rechecks, waiting/input protocols, and unrelated interface behavior are explicitly outside this change.

## Current Status

Completed and published as upstream PR [#211](https://github.com/Godofcong-1/erArk/pull/211) on 2026-07-11 from `meower-z:codex/restore-time-stop-unconscious-h-entry`. The PR was created as a Draft and then marked ready for review by the user. It contains one source commit and changes only instruction 5052 in `data/csv/InstructConfig.csv`; the two approved Tk screenshots are served from commit-pinned URLs on the public fork's append-only `assets` branch. Earlier private reset and Web changes remain outside this change's public boundary.
