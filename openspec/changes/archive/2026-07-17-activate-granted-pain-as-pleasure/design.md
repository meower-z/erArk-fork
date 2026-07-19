## Context

The group hypnosis boost intentionally sets persistent enhancement flags without changing `sp_flag.unconscious_h`. The UI and instruction premises also describe `hypnosis.pain_as_pleasure` as enabled directly. The local pain patch is the sole outlier: it additionally requires `unconscious_h` in `{4,5,6,7}` and temporarily disables the raw flag otherwise. Later group participants commonly remain conscious, so the displayed grant and the settlement result disagree.

Positive pain enters through a shared common-settlement function and four direct second effects. The shared function is imported into default, second-effect, realtime, and item modules, which makes registry and alias replacement part of the runtime contract.

## Goals / Non-Goals

**Goals:**

- Make the raw granted flag sufficient for positive pain conversion while the character is awake and conscious, without requiring an active hypnosis unconscious code.
- Cover all positive pain entry points and record converted target changes under psychological pleasure.
- Restore ordinary pain immediately after cancellation or reset clears the flag.
- Preserve decreases and unrelated guards unchanged.

**Non-Goals:**

- Automatically changing hypnosis type or unconscious state.
- Converting zero or negative pain changes into pleasure.
- Changing boost eligibility or the amount calculated by upstream pain effects.

## Decisions

### Use one activation predicate

`bool(character.hypnosis.pain_as_pleasure)` SHALL be the only feature-activation predicate. Adding group-mode or hypnosis-code checks would recreate source-dependent behavior and contradict a persistent visible grant. This does not decide whether the downstream state-23 settlement guard still suppresses posting while a character is asleep or unconscious; that separate rule remains an open question below.

### Intercept at the two real settlement families

The common pain handler and direct effects 270, 283, 296, and 408 are the two real positive-pain families. The current worktree hand-writes the common conversion and wraps the direct effects, but that implementation is not accepted. For common positive pain, delegating to upstream state-17 settlement with the raw flag visible may preserve more existing math and guards; direct writers still require explicit conversion. The final approach depends on the state-23 decision below.

### Delegate non-positive and inactive settlement upstream

When the flag is false or the computed pain change is non-positive, the original handler remains authoritative. Temporary flag suppression is allowed only to prevent recursive conversion while delegating a negative upstream settlement; the flag is restored in `finally`.

## Risks / Trade-offs

- **[Changed saved-flag meaning]** Existing conscious characters with the flag begin converting immediately -> this aligns saves with the existing UI and boost contract; cancellation remains the explicit off switch.
- **[Alias drift]** A later import or mod can retain an old function object -> assert all five aliases and registry handlers after the full mod load order.
- **[Double accounting]** Converted target changes could be written to both states -> verify real character state and `target_change` contain pleasure only for the converted amount.

## Current Implementation Disposition

The raw-flag predicate change is written, as are common-alias/direct-effect wrappers and tests, but none are runtime-verified. `implementation-notes.md` records the set/clear/mutation inventory, prior-spec conflict, formula differences, cap accounting, and limits of the connected tests.

## Open Questions

Resolved with the user on 2026-07-10:

1. **Intentional exception.** Converted psychological pleasure posts even while the target is asleep or unconscious. The delta spec explicitly overrides the upstream state-23 sleep/unconscious guard for this conversion path only; other psychological-pleasure sources keep the upstream guard.
2. **Requested value.** At the 99999 cap, change records report the upstream-compatible requested value, not the clamped actual delta.
3. Consequence of 1: full delegation through upstream state-17 recursion cannot express the guard override, so the custom conversion remains, but it must mirror upstream math — including the consecutive-instruction reduction that upstream applies during the state-17-to-state-23 recursion — in everything except the sleep/unconscious guard.
4. Accepted: the conscious-participant contract supersedes the 2026-07-07 dormant-state rule. Synchronize the main spec and the overlapping open change only after the implementation is verified.
