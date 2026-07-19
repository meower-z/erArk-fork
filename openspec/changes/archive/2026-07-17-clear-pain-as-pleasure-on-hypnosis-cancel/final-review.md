# Final Local Review

## Verdict

The maintainer's literal claim that the player otherwise has no way to remove `苦痛快感化` is false because effect 1230 is an independently repeatable toggle. The requested lifecycle is nevertheless reasonable: the direct cancellation cleanup predates the field, later sleep cleanup includes it, and the maintainer has now confirmed the intended upstream semantics.

The selected repair remains the narrow shared-helper option: add only `target_character_data.hypnosis.pain_as_pleasure = False` to `clear_hypnosis_sub_states()`. Caller-specific unconscious-state boundaries, abnormal-flag settlement, air hypnosis, second-stage settlement, and generic H state remain outside the helper.

## Verification

- Focused regression suite: `13 passed`.
- `python -m py_compile Script/Design/hypnosis_state.py`: passed.
- `git diff --check`: passed.
- Real Tk A/B used the same latest base, reproduction save, display geometry, and visible player actions.
- Before frames and instruction-result frames were byte-identical across A/B.
- Baseline after retained `<催眠(200%)(痛→快感)>`; corrected candidate after showed `<催眠(200%)>`.
- All retained evidence and replay material was verified under `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-213/local/hypnosis-cancel-narrow-20260714/` before the two temporary runtimes and capture directory were removed.
- Fable's final evidence acceptance found the A/B chain sufficient, accepted the one-line helper boundary, and judged a third replay unnecessary despite the documented split into two serial supervised commands.

## Remaining Local Integration Impact

- `/home/ubuntu/games/erArk-pr-hypnosis-target-runtime` still contains the uncommitted one-line helper correction and untracked focused tests.
- The remote PR head, title, body, and public images still describe the now-rejected preservation semantics.
- A local mod previously depended on preservation after direct cancellation; reconciling that local behavior is a separate task and is not part of this upstream fix.
- No commit, push, asset publication, or GitHub PR edit was performed.
