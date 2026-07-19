## Why

The current repeated-discovery requirement is narrower than the behavior actually protected: duplicate discovery is possible whenever hidden-sex discovery is evaluated again before the player moves, not only after a particular panel choice or during a multi-orgasm action. Upstream PR #206 now carries the root fix, so the durable contract and the eventual removal of the overlapping local patch need an explicit record.

## What Changes

- Define `see_pl_h` as preventing the same character from discovering the player again while the player remains at the current location.
- Preserve the eligibility and ordering of other characters who have not yet discovered the player.
- Restore a character's discovery eligibility only through the existing movement reset boundary.
- Record upstream PR #206's merge and remove only the overlapping hidden-sex candidate filter from the local participant-admission component after verifying the merged source behavior.

## Capabilities

### New Capabilities

- `hidden-sex-discovery`: Defines discoverer deduplication at the player's current location and the movement reset boundary independently of temporary local-mod ownership.

### Modified Capabilities

- `local-bugfixes`: Remove the repeated-discovery requirement after upstream adoption because the source game, rather than a retained local patch, will own that behavior.

## Impact

- Upstream patch point: `Script/System/Sex_System/hidden_sex_panel.py`.
- Former transitional owner for this rule: `mod/local_group_participant_admission_fix`; the component remains for its independent participant-admission behavior.
- Upstream review: `Godofcong-1/erArk#206` from `meower-z:codex/fix-hidden-sex-witness-dedup`.
- Upstream PR #206 merged as `e8a865c4a11d496bc11d29f8af2c9a1a617af9ad` on 2026-07-13. Current `main` matches the merged source file, and the overlapping candidate filter and dedicated claims have been removed from the retained local component.
