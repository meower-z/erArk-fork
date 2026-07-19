## Context

Upstream has two hypnosis-exit paths. Direct `解除催眠` clears selected body/mind hypnosis fields but intentionally leaves `hypnosis.pain_as_pleasure` unchanged. The sleep-driven `HYPNOSIS_FLAG_TO_0` path performs nearly the same cleanup but additionally clears that field. The user has confirmed that `苦痛快感化` is designed to persist through both exits.

The current candidate `6e841e36b` extracts too much into one helper: it clears `hypnosis.pain_as_pleasure`, clears the generic H-state field `h_state.npc_active_h`, and moves unconscious-mode matching and abnormal-flag recalculation out of both callers. The helper shape is retained, but its responsibility must be narrowed to the four hypnosis-owned sub-state assignments that already exist in both upstream paths.

## Goals / Non-Goals

**Goals:**

- Make the sleep-driven exit preserve `苦痛快感化`.
- Centralize the four identical hypnosis-owned sub-state resets in a directly reviewable helper.
- Leave the direct exit behavior unchanged.
- Leave `npc_active_h` unchanged in both paths.
- Prove the changed sleep behavior and the unchanged direct behavior with the smallest useful checks.
- Produce replacement Tk evidence and PR prose that describe only this behavior.

**Non-Goals:**

- Making both exit functions textually identical.
- Changing which `unconscious_h` values each existing path clears.
- Changing the lifetime of sensitivity increase, blockhead, hypnosis inverse control, roleplay, hypnosis degree, forced ovulation, or any generic H state.
- Updating the already-public branch, images, or a PR without a new publication authorization.

## Decisions

### Extract only the common sub-state block

The helper will be formed by copying the existing direct-exit block that resets `increase_body_sensitivity`, `blockhead`, `active_h`, and `roleplay`, then changing only its input from the already-loaded target object to a character id lookup. Both exit paths replace those same four assignments with one helper call.

The sleep path's separate `pain_as_pleasure = False` assignment is removed rather than moved into the helper. The helper does not touch `npc_active_h`. This makes the intended preserved fields visible in the diff and keeps the copied logic familiar to upstream reviewers.

Unconscious-mode matching and abnormal-flag recalculation remain at each caller. The two paths have real differences: they operate on different subjects, direct cancellation handles air-hypnosis location and second-stage settlement, and their current unconscious-state checks are not identical. Keeping those operations outside the helper prevents the refactor from changing their semantics.

### Do not touch `npc_active_h`

`hypnosis.active_h` records the hypnosis sub-effect, while `h_state.npc_active_h` records current NPC initiative during H and can be entered without hypnosis. Although hypnosis can set both fields, hypnosis exit does not own the generic H-state lifetime. Both upstream exit paths already preserve it, so the fix leaves it untouched.

### Treat reviewer feedback as clues

The fresh reviewer evaluates whether the one-line boundary truly follows the production lifecycle and preserves inverse cases. Any concern is recorded as a clue with supporting evidence and assessed by the root agent; it is not automatically copied into `tasks.md` or implemented.

The fresh review of the earlier one-line proposal returned `PASS`: effect 489 is used by behavior 111 (`sleep`), and the only behaviorally violating writer is the assignment inside `handle_hypnosis_flag_to_0`. The user subsequently selected the narrow helper refactor because it copies an existing cleanup block and makes the shared preservation rule easy to review. The earlier review remains clue evidence rather than a binding task decision:

- The CSV phrase `持续性效果` does not by itself define a sleep boundary; the confirmed design, existing direct-exit behavior, and consumers that read the flag independently of `unconscious_h` provide the actual basis.
- Effect 489 runs as part of sleep without first requiring `unconscious_h` to be 4-7. The precise contract is therefore that sleep leaves `pain_as_pleasure` unchanged, which covers both true and false inputs.
- Historical commit `fa532c42f` moved a batch of hypnosis resets into each character's sleep settlement and added the `pain_as_pleasure` reset as part of that batch, without a field-specific design reason visible in the change.
- Candidate `6e841e36b` changes three unrelated behaviors through its broad helper: direct-exit matching, `npc_active_h`, and direct-exit `pain_as_pleasure`. The revised helper excludes all three changes rather than discarding the useful four-assignment extraction.

### Replace rather than reinterpret the old evidence

The retained direct-cancellation screenshots demonstrate the behavior opposite to the corrected goal and cannot support the new PR. A visual subagent will capture one comparable real-Tk sleep-exit A/B flow using the project skill's frame-by-frame local interaction rules. The evidence must show the same pre-exit `苦痛→快感` state, upstream losing it after sleep cleanup, and the corrected candidate retaining it.

## Risks / Trade-offs

- **The one-line patch may expose a hidden reason for sleep-only clearing** -> Trace all writers/readers and use the direct path plus the user's design decision as inverse evidence before implementation.
- **The helper accidentally absorbs path-specific behavior** -> Limit it to the four assignments copied from the existing direct-exit block and keep unconscious matching, flag recalculation, and settlement at the callers.
- **The old screenshots and prose are misleading after the semantic correction** -> Mark them stale and regenerate only the minimum sleep-path evidence.
- **Local proof is mistaken for permission to republish** -> Stop before every outward-facing update and request separate authorization.

## Open Questions

None. Reviewer findings remain investigation clues unless the user later changes the confirmed behavior.
