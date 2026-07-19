## Why

The sleep-driven hypnosis exit path clears `苦痛快感化`, although the direct `解除催眠` path preserves it and the confirmed game design requires that effect to remain. The current candidate also clears `npc_active_h`, which represents the current H initiative state rather than hypnosis-owned state, so the candidate must be narrowed before it can be proposed upstream.

## What Changes

- Preserve `hypnosis.pain_as_pleasure` when the sleep-driven `HYPNOSIS_FLAG_TO_0` path exits hypnosis, matching the existing direct `解除催眠` behavior.
- Leave `h_state.npc_active_h` unchanged in both hypnosis exit paths because it is not owned by the hypnosis lifecycle.
- Extract the four hypnosis-owned sub-state resets already shared by both paths (`increase_body_sensitivity`, `blockhead`, `active_h`, and `roleplay`) into one helper copied from the existing direct-exit block.
- Preserve every other established difference and side effect of the two exit paths; the helper SHALL NOT own unconscious-mode matching, abnormal-flag recalculation, air-hypnosis cleanup, second-stage settlement, `pain_as_pleasure`, or generic H state.
- Verify the direct exit as an unchanged inverse case and the sleep-driven exit as the changed case.
- Replace the old direct-cancellation screenshots and PR prose with real Tk evidence centered on the sleep-driven path: upstream clears `苦痛→快感`, while the corrected candidate retains it.
- Keep local tests, saves, routes, and investigation material private, and do not push, upload, publish, or create or edit a PR without separate user authorization.

## Capabilities

### New Capabilities

- `hypnosis-target-runtime-pr-artifacts`: Defines the hypnosis-exit preservation rule, its minimum implementation boundary, and the local evidence and review contract for preparing the corrected candidate.

### Modified Capabilities

None.

## Impact

The intended gameplay impact is limited to the sleep-driven hypnosis cleanup: it must stop clearing `hypnosis.pain_as_pleasure`. The production refactor adds a narrow shared helper for the four already-common hypnosis sub-state assignments and replaces those assignments at both callers without moving path-specific logic. The direct `解除催眠` behavior, `h_state.npc_active_h`, unrelated hypnosis fields, unconscious-mode matching, and public interfaces remain unchanged. Local tests, Tk evidence, and PR-facing artifacts must be regenerated against the corrected diff; previously published assets and the public fork branch are stale and are not updated by this change.

## Completion

The corrected sleep-exit A/B, `fable-5` PR text, and fresh artifact review passed. After separate user authorization, source commit `e1a9378b140f99cd62f9c678c3a1113981e4e342` and assets commit `3d7dfc2748a0d5cdb962244088378fdada7471c7` were published and upstream PR [#213](https://github.com/Godofcong-1/erArk/pull/213) was opened ready for review on 2026-07-13. The public PR changes only the corrected four-assignment helper boundary and the sleep-path preservation rule described above.
