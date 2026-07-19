## Closure Decision

On 2026-07-13 the user explicitly directed this tracker to be archived because the adopted upstream behavior and local cleanup will not change further. Task 2.5 remains intentionally unchecked: focused #207 compatibility coverage passed, while the unrelated full-suite failures are owned by other active changes and will not keep this tracker open.

## 1. Contract And Upstream Submission

- [x] 1.1 Define the structured save-address inventory, normalization order, and ordinary-text boundary
- [x] 1.2 Prepare the focused upstream source fix and ordinary Tk post-load evidence
- [x] 1.3 Open upstream PR #207 from the `meower-z` fork and record its immutable commit and screenshot references

## 2. Upstream Adoption

- [x] 2.1 Confirm PR #207 is merged and identify upstream merge revision `16960e1b89e72da0d5a31ef5e716c0368cd0b924`
- [x] 2.2 Update the private branch to an upstream revision containing the fix and rerun foreign-path, native-path, and ordinary-text verification
- [x] 2.3 Load a foreign-separator ordinary save and confirm the normal post-load scene retains its saved character registrations
- [x] 2.4 Remove `local_cross_platform_save_fix` and its default configuration entries after upstream verification passes
- [ ] 2.5 Run save-focused tests and the configured local mod suite without the retired replacement; focused coverage passes, but the full suite is blocked by two unrelated active-change failures recorded in `implementation-notes.md`

## 3. Specification Closure

- [x] 3.1 Sync the `save-portability` capability into the main specifications after upstream adoption
- [x] 3.2 Record the merged revision and final local cleanup evidence, then archive this change by explicit user decision
