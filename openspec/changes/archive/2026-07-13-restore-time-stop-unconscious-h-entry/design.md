## Context

Before `b206249a5d`, instruction 5052 required a target, non-H state, the ordinary hidden-interface gate, any nonzero unconscious flag, and sufficient player stamina. The regression commit added `NO_TARGET_OR_TARGET_CAN_COOPERATE_OR_IMPRISONMENT_1` to prevent unconscious H against parturient or postpartum targets.

That composite expresses the wrong facts. Its cooperation branch requires an awake/cooperative target and therefore rejects sleeping, time-stopped, drugged, and hypnotically unconscious targets. Its imprisonment branch succeeds without proving that the target is not parturient or postpartum. The action becomes unavailable for valid unconscious targets while the intended pregnancy protection remains incomplete.

The same premise chain is used regardless of ordinary room, so the defect is not specific to the Central Lounge.

## Goals / Non-Goals

**Goals:**

- Restore instruction 5052 for valid unconscious targets, including `unconscious_h == 3` during time stop.
- Block parturient and postpartum targets independently of imprisonment.
- Preserve all other existing instruction gates.
- Produce a one-line upstream production diff with normal Tk before/after evidence.

**Non-Goals:**

- Clearing `show_non_h_in_hidden_sex` after H reset.
- Adding a generic Web stale-button dispatch check.
- Changing the Web waiting or panel-generation protocol.
- Changing unconscious-state values, consent/cooperation rules for other actions, map data, or the unconscious-H handler.
- Shipping generated JSON, saves, screenshots, local mods, or OpenSpec artifacts in the public branch.

## Decisions

### Use independent premises

Instruction 5052 keeps `T_UNCONSCIOUS_FLAG` and replaces the cooperation-or-imprisonment composite with `T_PARTURIENT_0` and `T_POSTPARTUM_0`. Every configured premise must pass, so imprisonment cannot bypass either pregnancy guard.

### Preserve every registered unconscious source

The fix restores the pre-regression contract for unconscious states 1 through 7. Time stop remains state 3; the change does not rewrite it as hypnosis or introduce a time-stop-only handler branch.

### Keep the public diff premise-only

The earlier private commit also contained player reset and Web dispatch changes. Those are separate defects with separate evidence requirements. They are excluded so the upstream review can evaluate one root cause and one configuration line.

### Treat generated data as verification evidence

`data/data.json` is ignored by Git but is the runtime configuration consumed by the game. Local verification must rebuild it in the clean worktree, inspect instruction 5052 structurally, and prove protected PO files are byte-identical before and after. The generated file does not belong in the PR.

## Risks / Trade-offs

- **Premise alias semantics:** A premise name may not mean what its label suggests. Verify each registered handler against current upstream source and cover the full state matrix.
- **Generated-data drift:** A CSV-only inspection can pass while runtime JSON remains stale. Verify the compiled record before gameplay.
- **Overbroad evidence setup:** A save or debug setup could accidentally bypass premises. Use normal Tk interaction and record the exact visible state before and after.
- **Adjacent regressions remain:** Hidden-interface reset and Web stale dispatch are not fixed here. State that boundary plainly rather than bundling them.

## Verification Plan

1. Create a clean worktree from current `upstream/master`.
2. Add a focused regression that proves the old composite rejects a valid time-stopped target and that the orthogonal chain accepts it while preserving negative cases.
3. Apply only the instruction 5052 CSV edit.
4. Rebuild runtime data without changing protected PO files and inspect the compiled premise list.
5. Capture normal Tk before/after evidence using the same gameplay setup.
6. Review the public diff against `upstream/master`; production scope must remain one CSV line.
