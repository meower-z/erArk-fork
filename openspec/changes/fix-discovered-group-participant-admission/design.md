## Context

`Sex_Be_Discovered_Panel` is entered from two materially different call sites. The normal NPC state-machine path returns to `character_behavior()`, which performs an outer status settlement; hidden-sex discovery calls the panel directly and has no such outer settlement. The upstream callback also starts a nested player update when converting single H to group mode. That update can reset the discoverer's pending behavior before the outer NPC settlement consumes it.

The current local patch partly guesses which caller owns settlement from `group_sex_mode`. That is not a reliable ownership boundary: active group mode can also be reached by the direct hidden-discovery call, and initial conversion still returns to an outer NPC settlement after its required early settlement.

Separately, the registered `place_all_not_h` premise returns success from inside its loop, so only the first non-player character is inspected. This explains the contradictory invite and end controls once a later scene character is already in H.

## Goals / Non-Goals

**Goals:**

- Give every discovery decision exactly one effect settlement independent of its caller.
- Settle initial group conversion before its nested player update can erase the discoverer's behavior.
- Prevent the later outer NPC settlement from replaying an already consumed discovery behavior.
- Make scene-level H eligibility inspect every non-player character.

**Non-Goals:**

- Redesigning the group template or NPC group-sex AI.
- Changing acceptance calculations, fatigue rules, or hidden-sex discovery selection.
- Treating a character as a template member merely because `is_h` is true.

## Decisions

### Represent settlement ownership explicitly

The discovery call context SHALL distinguish a panel opened inside NPC target selection from a direct panel call. A one-shot "outer settlement expected" context is preferable to inferring ownership from group mode or behavior ID. If a callback must settle early, it records a suppression token that is consumed only by the immediately following outer settlement in that same NPC dispatch.

Alternative: always settle in the panel and replace the behavior with `WAIT`. This is rejected because the outer settlement would still run event and second-effect machinery for a fabricated behavior and could change timing.

Alternative: let the outer loop settle every path. This is rejected because direct hidden discovery has no outer loop and initial conversion must settle before a nested update.

### Keep behavior assignment and effect consumption atomic

Acceptance and refusal callbacks assign the intended behavior and either leave it to the known outer owner or settle it immediately. An early-settled behavior cannot remain available for replay. The token is scoped to the character and current dispatch, not stored as an unbounded persistent character flag.

### Patch the premise registry and implementation alias

`place_all_not_h` is dispatched through the premise registry, so the corrected full-loop function replaces both the registry entry and the defining module attribute. Success is returned only after all non-player scene characters have been inspected.

## Risks / Trade-offs

- **[Stale suppression token]** An exception or direct caller could leave a later action suppressed -> scope the token to the active NPC dispatch and clear it in `finally`.
- **[Nested update re-entry]** The player update may evaluate the same NPC -> consume the discoverer's admission before starting the nested update and make suppression idempotent.
- **[Existing double settlement elsewhere]** Other panel choices also manually settle -> audit every callback, but keep implementation edits limited to discovery decisions whose ownership is proven by the regression paths.

## Current Implementation Disposition

The desired dispatch-scoped token described above is not what the worktree currently implements. The candidate uses a global character-ID set and global wrappers around target selection and status settlement. It therefore cannot yet prove dispatch-local consumption or safe coexistence with other wrappers. The exact call graph, experimental code, adjacent uncovered paths, and written-but-unexecuted tests are recorded in `implementation-notes.md`.

## Open Questions

Resolved with the user on 2026-07-10:

1. **Postpone.** The exact-once settlement portion is postponed and the global wrapper experiment is removed from the worktree. Only the narrow full-scene `place_all_not_h` premise fix is retained and verified now.
2. Deferred to the future ownership design, together with the non-admission hidden-discovery paths, which remain explicitly out of scope.
3. Deferred to the future ownership design.

The double/lost-settlement behavior remains a real, documented defect; its call graph and risks in `implementation-notes.md` are the starting point for that future change.
