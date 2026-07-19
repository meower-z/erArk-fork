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

Static reconstruction and candidate edits/tests are written, but nothing has been executed. The test uses AST/mocks rather than a real enabled-mod/Tk flow, its Web assertion is coupled to the unresolved waiting change, and mod-off/mod-on marker identity plus actual-delta behavior remain unverified. See `implementation-notes.md`; checked tasks below mean written work, not runtime acceptance.
