## Closure Decision

On 2026-07-13 the user explicitly directed this tracker to be archived because the adopted upstream behavior and local cleanup will not change further. Task 2.4 remains intentionally unchecked: focused #206 and participant-admission coverage passed, while the unrelated full-suite failures are owned by other active changes and will not keep this tracker open.

## 1. Contract And Upstream Submission

- [x] 1.1 Define the player-has-not-moved witness contract, its movement reset boundary, and its final source-level specification ownership
- [x] 1.2 Prepare the focused upstream source fix and before/after Tk evidence
- [x] 1.3 Open upstream PR #206 from the `meower-z` fork and record its immutable commit and screenshot references

## 2. Upstream Adoption

- [x] 2.1 Confirm PR #206 is merged and identify upstream merge revision `e8a865c4a11d496bc11d29f8af2c9a1a617af9ad`
- [x] 2.2 Update the private branch to an upstream revision containing the fix and rerun repeated-evaluation, alternate-witness, and movement-reset verification
- [x] 2.3 Remove only the duplicate hidden-sex witness filter, tests, and claims from `local_group_participant_admission_fix`
- [ ] 2.4 Verify the remaining participant-admission component in isolation and through the configured local mod suite; focused coverage passes, but the full suite is blocked by two unrelated active-change failures recorded in `implementation-notes.md`

## 3. Specification Closure

- [x] 3.1 Sync the new `hidden-sex-discovery` capability and remove the migrated requirement from `local-bugfixes` after upstream adoption
- [x] 3.2 Record the merged revision and final local cleanup evidence, then archive this change by explicit user decision
