## Current Verification Status (2026-07-14)

The candidate code is already on local `main` through commit `0b3f1c1a9`. The following focused command passed on 2026-07-14:

```text
.venv/bin/python -m pytest tests/test_time_stop_release_settlement_output.py mod/local_h_orgasm_batch_fix/tests/test_local_h_orgasm_batch_fix_mod.py -q
58 passed in 4.49s
```

This verifies the current focused component expectations only. No real enabled-ModManager identity trace, real Tk settlement inspection, independent Web check, actual-delta/cap proof, or global formatter call-site audit is claimed. The next action is to perform those checks against the existing code and rewrite only if a check fails.

## Historical Worktree Status (2026-07-10)

This is the strongest narrow candidate, but it is not verified. Static root-cause analysis and candidate edits are written; no focused test, enabled-mod integration, Tk/Web render check, game launch, or manual playthrough has run. Checked task boxes mean "audited or written", not "runtime passed". Cross-change branch and protected-file state are in `../continue-local-bugfix-audit/design.md`.

## Confirmed Root-Cause Reconstruction

Effect 527 releases each NPC's deferred time-stop orgasm counts but previously passed the player's root `CharacterStatusChange` to `orgasm_settle()`. NPC state was mutated by `character_id`, while display/accounting accumulated under the player object. The later generic second-stage pass used `change_data.target_change[npc_id]`, splitting one NPC release between two owners.

The screenshot is consistent with six deferred body-part orgasms: six small-orgasm effects account for MP -360 and six experience points, while `plural_orgasm_6` accounts for the larger happiness/submission and pain/aversion changes. The evidence does not require an elapsed-time multiplier.

The compact formatter had an independent sign/index defect: its suffix array begins at K but four digits selected index 1, producing M; the minus sign was counted as a digit, so `-500` could be sliced to `-` and printed as `-M`.

## Candidate Implementation Written

- Effect 527 creates or reuses `change_data.target_change[chara_id]` and passes that exact `TargetChange` to NPC orgasm release.
- Release-specific work and the `time_stop_release` marker run only when at least one deferred count is positive.
- Counter clearing plus unconscious clothing/semen/stolen-item recovery remains active for every relevant NPC, including zero-count NPCs.
- The later time-stop-off second-stage loop uses `cache.npc_id_got.copy()` and `discard(0)`. This defensively excludes an anomalous player ID without mutating the global NPC set while iterating.
- `local_h_orgasm_batch_fix` accepts a direct `TargetChange` owner and uses a marker that the generic pass can consume.
- `get_value_text()` formats sign from absolute magnitude and maps groups to K/M correctly.

The related diffs are mixed with other active changes: `h_orgasm_batch.py` also contains Web-recording edits from the waiting experiment, and `settle_behavior.py` also contains settlement-ledger edits. Those unrelated lines are not required by this release fix and must not be treated as part of the narrow patch when splitting or reviewing it.

## Required Mod-Off and Mod-On Paths

### Batch mod disabled

Release-generated second effects remain queued through the original route, then the ordinary generic second-stage pass consumes them into the same NPC `TargetChange`. Nothing should be synchronously marked as already consumed.

### Batch mod enabled

The batch override synchronously settles generated second behaviors, removes only the queue entries it owns, and writes its marker on the same NPC `TargetChange`. The generic pass consumes that marker exactly once while still settling unrelated queued second behaviors. Marker creation and consumption must be proved by object identity, not only equal values.

Remote NPCs, zero-count NPCs, several NPCs, a polluted `npc_id_got` containing 0, and unrelated pre-existing second behaviors all need both mod-off and mod-on simulation. The earlier task claimed remote enumeration, but no runtime or near-real evidence exists yet.

## Formatter Scope

`get_value_text()` is a global formatter, not a time-stop-only helper. Current call sites include core state display, core experience display, and the batch mod's window-end output. Boundary verification must therefore ensure the K/M/sign correction is appropriate at every call site and does not alter unrelated value meaning.

## Focused Verification And Remaining Limits

`tests/test_time_stop_release_settlement_output.py` contains formatter cases and AST-plus-mock settlement cases. The release portion extracts/executes code and mocks orgasm settlement; it is not a real core plus enabled-mod integration and does not exercise a real Tk panel. The Web collection case also asserts `settlement_input.mark_visible_output`, coupling this narrow change to the unresolved waiting change. That assertion should be split before it is used as release evidence.

The component test in `mod/local_h_orgasm_batch_fix/tests/` covers direct-marker handling. Both focused files now pass together (58 tests on 2026-07-14), but their AST/mock boundary remains unchanged.

Still required:

- Verify stored-state actual deltas and cap behavior rather than only requested change values.
- Verify mod-off and mod-on ownership/marker traces for one, multiple, zero-count, remote, and unrelated-queue cases.
- Verify real enabled ModManager load order and object identity.
- Inspect actual Tk settlement text and Web value-change collection independently of the waiting protocol.
- Run focused and relevant time-stop/H regressions only after static traces agree, then perform a fresh diff review.
