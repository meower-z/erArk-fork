## Why

`苦痛快感化` was added after the direct `解除催眠` cleanup block, so direct cancellation leaves that sub-state active even though the maintainer has confirmed that cancellation should remove it. PR #213 initially interpreted the old omission as intentional and therefore needed a local semantic correction before further publication.

## Current Status

As of 2026-07-14, the corrected code, revised PR text, and replacement evidence have been published to [PR #213](https://github.com/Godofcong-1/erArk/pull/213). The PR is open, non-draft, and waiting for maintainer merge. No further code, evidence, branch, comment, or PR-text action is required while it remains open.

An open PR is not treated as accepted or merged. Preserve its candidate worktree and archived evidence; any post-merge local cleanup requires a fresh live-state check and separate user authorization.

## What Changes

- Add `pain_as_pleasure` to the shared hypnosis sub-state cleanup already introduced by PR #213.
- Keep sleep cleanup behavior unchanged while making direct `解除催眠` clear all five shared continuous hypnosis sub-states.
- Preserve each caller's existing unconscious-state boundary, abnormal-flag settlement, air-hypnosis cleanup, second-stage settlement, and generic H state.
- Replace the current sleep-preservation evidence locally with a fresh real-Tk direct-cancellation A/B from the corrected candidate.
- Stop before pushing the candidate, publishing replacement evidence, or editing PR #213.

## Capabilities

### New Capabilities

- `hypnosis-exit-substate-cleanup`: Defines the five-field cleanup shared by sleep and direct hypnosis cancellation, its path-specific non-goals, and the verification contract.

### Modified Capabilities

None.

## Impact

The production change is one additional assignment in `Script/Design/hypnosis_state.py`; both existing callers in `Script/Settle/default.py` continue to use that helper without further restructuring. Focused local checks and real Tk evidence must be updated. No public API, save format, dependency, remote branch, asset branch, or GitHub PR is changed by this local work.

The later publication step was separately authorized: PR head `fe57f98a08368bb2247605d6362cbdc2475edc1d` and evidence-assets commit `619d313c020af38c014e338a24b9bdbf59bb0efe` are the retained publication records.
