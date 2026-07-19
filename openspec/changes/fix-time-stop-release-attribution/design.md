## Context

Time-stop effect 527 iterates deferred NPC orgasm counts. The old path mutates the NPC selected by `character_id` but supplies the player's root `CharacterStatusChange` to orgasm settlement. When that call writes a synchronous value directly, the record therefore uses a different owner from the NPC being mutated. The attribution-only candidate is isolated from the earlier mixed local change, and its focused test now loads the real settlement registry and orgasm function in a subprocess.

The earlier player screenshot is historical corroboration only. The accepted normal-UI attempt 11 uses Lin (4080) as the deferred-release NPC and Jingzhe (306) as the switched current target. Thirty-one corresponding pre-result frames are byte-identical; the final baseline and candidate frames visibly separate the wrong player-owned experience block from the corrected Lin-owned block while conserving both experience totals.

## Goals / Non-Goals

**Goals:**

- Give effect 527's direct nonzero release changes a target-owned change object for the released NPC.
- Leave the later generic second-stage pass untouched; at the effect-527 boundary, confirm that this effect does not consume or overwrite an existing queue.
- Confirm in one non-blocking local ModManager smoke that the unpublished batch mod accepts the NPC-owned object.
- Prove actual stored experience, zero/multiple/remote NPC effect-boundary behavior, and renderer collection through real code paths.

**Non-Goals:**

- Change orgasm formulas, deferred counts, release multiplicity, or time-stop instruction premises.
- Change the existing lifetime of `shoot_position_body` or `shoot_position_cloth` before a player action.
- Refactor the remote silent second-stage path in `must_settle_check()` or make it share effect 527's change object.
- Correct compact K/M formatting; that is an independent change.
- Import unrelated Web waiting-protocol edits from the current local mixed diff.

## Decisions

### Create or reuse the target-owned object at effect 527

Effect 527 is the first point that knows which NPC's deferred state is being released. For a positive deferred count, it therefore creates or reuses `change_data.target_change[npc_id]` and passes that object to the synchronous `orgasm_settle` call. The generic pass remains unchanged and outside this decision boundary.

Alternative considered: move values from the player object after settlement. Rejected because formulas, caps, labels, and later second effects may already have read the wrong owner.

The final current-upstream hunk uses `any(time_stop_orgasm_count.values())` before selecting the NPC-owned object. The lifecycle admits only non-negative production values, so this is equivalent to testing each count for `> 0`. Its production diff has `a=2`, `b=1`, `S=0`, `U=0`, for penalty 3 under `(a + b) + S - 2U`. The explicit-positive alias alternative has `a=3`, `b=1`, `S=1`, `U=0`, for penalty 5; its only behavioral difference requires a negative value that no production path emits. A one-line inline alternative would score 2 but violates the project's 200-character style gate.

### Keep the unpublished batch mod outside the upstream candidate

The upstream candidate does not contain `local_h_orgasm_batch_fix`, and that component is disabled in local normal play. One real-ModManager smoke checks that the local component still accepts the NPC-owned object. Any compatibility edit belongs to a separate local component change, not this upstream PR.

Alternative considered: make the full mod-on matrix block the upstream PR. Rejected because an upstream reviewer cannot load or review that unpublished component.

### Preserve the zero-count release lifecycle

`time_stop_release` is read by talk selection, unconscious experience conversion, and later second-behavior logic. The candidate therefore preserves the original `time_stop_release = True` assignment and the original no-op `orgasm_settle` call when every deferred count is zero. Only calls with a positive deferred count switch to the NPC-owned `TargetChange`. Counter clearing and unconscious clothing/semen/stolen-item recovery remain unchanged.

The empty call itself does not create a target block. The later generic pass may still create an empty target entry for that NPC, as it did before this change; that behavior is outside the effect-527 assertion.

### Treat Web as an inverse collection check

The shared settlement record feeds both renderers. The accepted discriminating normal-game route supplies matched Tk PR-facing player evidence. Web independently proves the effect-527 direct target-owned record is collected with the correct character ID and is not coupled to the frozen waiting protocol.

## Risks / Trade-offs

- **[Mock tests hide object-identity failure]** → add real-loader traces that assert identity, not merely equal dictionaries.
- **[Local batch mod rejects a direct target owner]** → run one real-ModManager compatibility smoke locally and keep any mod edit separate.
- **[Recorded experience differs from stored experience]** → compare the real NPC experience before/after with the emitted target-owned record.
- **[A code-level trigger is mistaken for a player route]** → describe `shoot_position_body = 2` only as an effect-boundary owner probe; use the accepted attempt-11 normal-UI Tk A/B as the player-visible proof.
- **[Mixed local files widen the PR]** → isolate only the release-attribution hunks and independently inspect the final diff.
- **[Defensive player-ID exclusion lacks a production trigger]** → exclude that guard from the upstream candidate unless a real runtime trace first shows character ID 0 in the NPC iteration source.
