## Context

Hidden-sex settlement builds a nearby-character candidate list each time discovery is evaluated. The discovery panel already sets `sp_flag.see_pl_h`, and the existing movement flow resets that flag when the player changes location, but the hidden-sex candidate selection did not consult it. The local participant-admission component added that missing filter; upstream PR #206 applies the same root fix in the source module.

The main `local-bugfixes` specification currently describes only the talk-away reproduction and calls the flag a one-H marker. That wording misses other triggers and gives the wrong reset boundary. Once upstream owns the fix, the contract also no longer belongs under a capability limited to retained local bugfix components.

## Goals / Non-Goals

**Goals:**

- State the guarantee in terms of the player remaining at one location.
- Keep the fix at the final hidden-sex discovery selection point.
- Move the durable behavior contract from local-mod ownership to a source-level hidden-sex discovery capability.
- Record upstream ownership and remove the duplicate local patch only after merge verification.

**Non-Goals:**

- Change when `see_pl_h` is set or reset.
- Change nearby-character queries used by unrelated systems.
- Change ordinary H or exposure discovery logic, which already applies its own witnessed-player premise.
- Remove the other tired-character and participant-admission behavior from `local_group_participant_admission_fix`.

## Decisions

### Use movement as the reset boundary

The contract follows the existing lifecycle of `see_pl_h`: once a character has been handled as a discoverer, repeated hidden-sex checks exclude that character until player movement resets the marker. Trigger-specific alternatives such as “same climax” or “same panel visit” are rejected because several different actions can cause another discovery evaluation.

### Filter only the final hidden-sex candidate list

The source fix filters the list returned to `settle_discovered()` rather than broadening the shared nearby-character helper. This preserves the helper's existing meaning and avoids changing callers that do not use witness state.

### Retire only the overlap after verified upstream adoption

PR #206 merged on 2026-07-13 as `e8a865c4a11d496bc11d29f8af2c9a1a617af9ad`. Current `main` contains the merged source implementation. The overlapping hidden-sex candidate filter and its dedicated coverage were removed while the local component's independent tired-character and participant-admission behavior remains enabled.

### Move the contract when ownership moves

The final specification adds `hidden-sex-discovery` and removes the old repeated-discovery requirement from `local-bugfixes`. Merely rewording the local requirement is rejected because it would claim that a retained local component owns behavior supplied by the merged source game.

## Risks / Trade-offs

- **Upstream implementation changes during review** -> compare the merged diff and rerun the focused local scenarios before removing the patch.
- **Removing the whole local component drops unrelated fixes** -> delete only the hidden-sex witness filter, its dedicated tests, and its documentation claims.
- **A later movement reset changes** -> retain an explicit movement-reset scenario so the lifecycle remains visible.

## Migration Plan

1. Keep the current local filter while PR #206 is under review.
2. After merge, update the private branch from an upstream revision containing the fix.
3. Verify repeated evaluation before movement, another eligible witness, and eligibility after movement.
4. Remove only the now-duplicate local filter and its focused compatibility coverage.
5. Sync the new source-level capability and the removal from `local-bugfixes`, then archive the change.

Rollback is to restore the local filter if the upstream fix is reverted or fails the focused verification.

## Open Questions

The change remains active only because the full configured `mod/tests` suite is not green for two unrelated active-change failures recorded in the implementation notes.
