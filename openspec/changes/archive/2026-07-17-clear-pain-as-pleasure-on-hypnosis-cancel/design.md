## Context

The direct `解除催眠` cleanup predates `hypnosis.pain_as_pleasure`; when that field was introduced, its independent toggle was added but the older cancellation cleanup was not updated. Sleep effect 489 was added later with the complete sub-state list and already clears the field. The maintainer has now confirmed that direct cancellation should clear it too.

PR #213 already extracts the four assignments common to both paths into `clear_hypnosis_sub_states`. Its current semantic change removes the sleep-path pain cleanup. The corrected candidate must reverse only that interpretation without restoring duplicated cleanup or absorbing path-specific operations.

## Goals / Non-Goals

**Goals:**

- Make direct `解除催眠` and sleep cleanup clear the same five continuous hypnosis sub-states.
- Express the five-field list once in the existing helper.
- Keep sleep behavior unchanged from upstream and change only direct cancellation behavior.
- Produce fresh real-Tk evidence from the corrected candidate and archive its replay package before removing temporary runtimes.

**Non-Goals:**

- Merging the two callers or changing their unconscious-state predicates.
- Moving abnormal-flag settlement, air-hypnosis cleanup, or second-stage settlement into the helper.
- Changing `h_state.npc_active_h`, `hypnosis_degree`, `force_ovulation`, the pain toggle, or pain-conversion formulas.
- Pushing a commit, publishing evidence, or editing PR #213.

## Decisions

### Add one assignment to the existing helper

Add `target_character_data.hypnosis.pain_as_pleasure = False` to `clear_hypnosis_sub_states`. Both callers already delegate the other four fields to that helper, so this is the smallest change that fixes the historical omission and prevents the two cleanup lists from diverging again.

Adding only one line to `handle_hypnosis_cancel` was rejected because it would restore two copies of the same five-field rule. Reusing candidate `6e841e36b` was rejected because its broader helper also owns unconscious-state transitions, abnormal-flag recalculation, and `h_state.npc_active_h`.

### Re-record direct-cancellation evidence

The prior direct-cancellation save and route remain valid preparation material, but the old candidate images came from the broader `6e841e36b` diff. Replay both baseline and corrected candidate from the archived slot-9 save through `[4004]解除催眠`, using comparable Tk sessions and inspecting each final image. The evidence contract is upstream retaining `(痛→快感)` after cancellation and the corrected candidate removing it while retaining the hypnosis degree.

### Archive before cleanup

Archive final media, the action log, route, runtime manifest, reproduction save, and overlay hashes under `~/games/archive/erArk-upstream-pr-evidence/PR-213/local/` and verify the archived media and hashes. Remove only task-owned `/tmp` runtime and disposable capture directories after that verification.

## Risks / Trade-offs

- **A wider helper silently changes neighboring state** → Keep the production diff to the single field assignment and assert path-specific fields separately.
- **Old evidence is mistaken for proof of the new diff** → Re-record from the corrected candidate and record its exact source revision.
- **Cleanup destroys replay provenance** → Verify the archive copy and hashes before deleting any task-owned temporary directory.
- **The corrected local result is mistaken for publication authorization** → Stop before every push, asset publication, or GitHub PR edit.
