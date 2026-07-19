## Context

`TIME_STOP_OFF` runs effect 527 after clearing the time-stop unconscious flag. Effect 527 iterates NPCs and asks `second_behavior.orgasm_settle()` to turn each NPC's deferred per-part counts into normal orgasm effects. It currently passes the outer player's `CharacterStatusChange` to every call. The enabled batch mod correctly mutates the NPC selected by `character_id`, but faithfully records those changes in the supplied player object. The later generic NPC second-stage loop uses `change_data.target_change[npc_id]`, producing two different owners for one NPC release.

The screenshot's units come from a separate formatter defect. The suffix array starts at K, but the current index for a four-digit number is 1, so thousands are labeled M. It also counts the minus sign as a digit; `-500` is treated as a four-character compact value, sliced to `-`, and emitted as `-M`.

The observed values match six deferred body-part orgasms: six small-orgasm effects explain MP -360 and six experience points, while `plural_orgasm_6` explains the larger happiness/submission and pain/aversion reduction. The formulas are not evidence of an elapsed-time multiplier.

## Goals / Non-Goals

**Goals:**

- Attribute every deferred NPC release effect and follow-up second effect to the same NPC change object.
- Preserve batch-mod exactly-once markers when their owner is a `TargetChange` directly.
- Avoid setting release state on NPCs with no deferred orgasm count.
- Produce correct compact suffixes and readable negative values.

**Non-Goals:**

- Changing orgasm effect formulas, counts, levels, or time-stop duration.
- Applying an arbitrary value cap to conceal output.
- Treating unrelated `.seconds` uses as the cause of this screenshot.

## Decisions

### Pass the target-owned object at the release source

Effect 527 creates or reuses `change_data.target_change[chara_id]` and passes that `TargetChange` to `orgasm_settle`. This is preferable to moving values after settlement because synchronous batch markers and effects must share object identity with the later `check_second_effect(chara_id, target_change, pl_to_npc=True)` call.

### Gate only the release marker, not unconscious recovery cleanup

`time_stop_release` and `orgasm_settle` run only when at least one deferred count is positive. Counter clearing and `settle_unconscious_semen_and_cloth()` still run for every NPC so clothing, semen, and stolen-item recovery cannot be lost.

### Compute compact units from absolute magnitude

Formatting separates sign from `abs(value)`, uses group `(digits - 1) // 3`, maps group one to K, and prepends the sign afterward. Values below 1000 retain their unabridged representation.

### Iterate a defensive NPC snapshot

The second-stage release loop copies `cache.npc_id_got` and discards character ID 0 from the copy. This prevents an anomalous player ID from being treated as an NPC without mutating the global set during iteration.

### Preserve both batch-disabled and batch-enabled ownership

With the batch mod disabled, release effects remain queued and the generic pass consumes them into the NPC owner. With the batch mod enabled, the mod settles only its generated queue entries synchronously, writes a marker on that same `TargetChange`, and the generic pass consumes the marker while continuing to settle unrelated queue entries. Neither path may replay or discard effects from the other.

## Risks / Trade-offs

- **[Marker consumed twice]** Changing object ownership can separate batch and generic passes -> verify the marker is created and consumed on the exact same `TargetChange` and unrelated queued effects still run once.
- **[Zero-count cleanup skipped]** Gating the whole loop could lose unconscious recovery -> gate only release-specific steps and retain cleanup for all NPCs.
- **[Formatter compatibility]** Correct K output changes previously wrong visible text -> table-test boundaries and preserve the existing integer truncation style.

## Current Verification State

The candidate code and tests are written but unexecuted. The formatter is global and affects core state, core experience, and batch-mod output. Current release tests use AST extraction and mocks rather than a true core plus enabled-mod flow, and the Web test is coupled to the separate settlement-input experiment. Remote NPC, actual-delta/cap, mod-off/mod-on, real Tk, and independent Web behavior remain open. Full details are in `implementation-notes.md`.
