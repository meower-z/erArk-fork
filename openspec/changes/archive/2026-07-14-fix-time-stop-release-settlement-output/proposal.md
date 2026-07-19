## Why

When time resumes, deferred NPC orgasm effects are accumulated into the player's root change object, so NPC values are printed under `博士博士` and compared against the wrong character. The compact formatter then labels thousands as millions and can reduce a negative three-digit value to bare `-M`, making a correct six-part release look like catastrophic corruption.

## What Changes

- Route each NPC's time-stop orgasm release into that NPC's `TargetChange`, where the normal follow-up second-stage settlement already records NPC effects.
- Mark `time_stop_release` only for NPCs with a non-zero deferred orgasm count while still settling unconscious clothing/semen recovery for every NPC.
- Preserve exactly-once ownership between the enabled H-orgasm batch mod's synchronous release and the later generic second-stage pass.
- Correct compact value formatting so K/M/etc. suffixes use the right group and negative signs do not affect digit counting.
- Verify Tk settlement text and Web value-change collection with one and multiple NPCs.

## Capabilities

### New Capabilities

- `time-stop-release-settlement-output`: Defines ownership, attribution, and numeric presentation for deferred time-stop release changes.

### Modified Capabilities

- None.

## Impact

- Affects effect 527 in `Script/Settle/default.py`, compact settlement formatting in `Script/Design/attr_text.py`, and integration with `local_h_orgasm_batch_fix` markers.
- Does not change action duration, time rollback, orgasm count generation, or underlying effect formulas.

## Current Status

**Superseded as an implementation owner on 2026-07-14.** The display-only responsibility now belongs to `fix-compact-value-formatting`, and deferred-release ownership belongs to `fix-time-stop-release-attribution`. This combined change preserves the original diagnosis and candidate provenance but must not drive a mixed PR or synchronize its mixed delta spec.

The candidate code is already present on local `main` through commit `0b3f1c1a9`. The two focused files now pass together: 58 tests passed on 2026-07-14. This confirms the current component-level ownership and formatter expectations, but it is not end-to-end proof.

All remaining work has moved. `fix-compact-value-formatting` owns formatter call-site enumeration, signed K/M boundaries, and representative Tk display. `fix-time-stop-release-attribution` owns release-diff isolation, real-loader object identity with the batch mod off and on, zero/multiple/remote/unrelated-queue cases, actual-applied deltas and caps, Tk attribution, and independent Web collection. This combined change authorizes no further production or test edits.
