## Context

The prototype is preserved at commit `4ee74f87f` on `codex/temp-settlement-input-boundaries-backup-20260711`. The active branch must keep upstream `Script/` and `static/` files clean. The mod loader can replace Python functions and methods after their modules load, but it cannot directly replace `static/game.js`; the migrated design therefore avoids requiring the prototype's browser change.

The investigation also found an independent upstream defect: `code_text_to_draw_text()` formats every paper-doll placeholder with player character 0. For NPC `{move}` output this turns many different NPC moves into repeated lines claiming that the Doctor moved at the player's current scene. That fix belongs in its own component.

## Goals / Non-Goals

**Goals:**

- Preserve real Web `WaitDraw` and direct event/talk boundaries.
- Scope right-click/map/navigation/timed-wait skip flags to their owning operation.
- Correct NPC `{move}` formatting without changing other paper-doll behaviors.
- Keep upstream source and browser assets byte-identical to the active branch HEAD.
- Provide focused tests, direct Tk GUI evidence, rollback instructions, and future upstream patch guidance.

**Non-Goals:**

- Reintroducing the abandoned output-ledger or panel-generation protocol.
- Treating ordinary recorded text as a new semantic wait.
- Using the scripted Web BDD driver as behavioral evidence.
- Changing the protected localization files.

## Decisions

### Split by root cause

`local_settlement_input_fix` owns wait publication, per-event pacing, and skip ownership. `local_npc_move_talk_context_fix` owns only NPC `{move}` formatting. This keeps either fix independently disableable and follows the repository's componentization contract.

### Wrap upstream functions where possible

Map, navigation, timed waits, and draw methods are wrapped in `try/finally`; the wrapper calls the loader-provided original function and restores only state created by that call. Direct talk/event pacing is added after the original draw function by observing whether the main or minor dialog queue gained an entry. This avoids copying large upstream functions.

### Replace only the shallow Web adapter boundary

The Web `WaitDraw` adapter is small and must publish before blocking, so the mod replaces that method. After the response it removes the exact active wait element before republishing. This avoids the prototype's `await_input:false` browser contract and therefore requires no `static/game.js` edit. When an outer skip owner is active, the adapter publishes ordinary text and does not arm a wait.

### Preserve explicit waits during recording

The `io_web.append_current_draw_element` wrapper temporarily disables text recording only while delegating explicit `wait` elements, so they reach the real Web wait adapter rather than becoming ordinary history text. Empty `line_wait` elements are represented with a newline for the upstream non-empty filter.

### Correct only NPC movement paper-doll context

The movement-context mod replaces `code_text_to_draw_text`. For an NPC and exactly `{move}`, it first expands the paper-doll template with the original NPC id, then delegates the expanded literal to upstream formatting. All other inputs delegate unchanged.

### GUI evidence is human-like, not scripted BDD

Focused unit/component tests may automate pure logic and loader checks. Any BDD claim must come from a subagent directly operating the real Tk GUI, capturing screenshots, and visually inspecting the rendered text and interaction pacing.

## Risks / Trade-offs

- [Queue-delta wrappers can be affected by another mod changing dialog behavior] -> Declare load order, assert installed patch points, and test with the full enabled-mod set.
- [Removing the completed Web wait element changes history/current-state symmetry] -> Preserve the history copy and test that the next panel does not re-arm the completed wait.
- [Restoring skip state can expose latent upstream output bugs] -> Keep the NPC movement-context fix separate and document any further exposed output rather than suppressing it globally.
- [The mod loader has no browser-asset override] -> Do not migrate behavior that requires `static/game.js`; record it as intentionally omitted.
- [Tk GUI verification can be environment-sensitive] -> Record viewport, exact actions, screenshots, and observed text; do not substitute launch success for visual inspection.

## Migration Plan

1. Preserve the prototype on the temporary branch and return the active branch to HEAD-clean upstream code.
2. Add both local mods, component tests, manifests, and enabled load order.
3. Verify upstream source cleanliness and run focused automated tests.
4. Have a subagent operate Tk directly and inspect screenshots for waits, map movement, and NPC movement text.
5. Record evidence and residual gaps in the mod READMEs and this change.

Rollback disables the two mod ids and removes their directories; no upstream file restoration is required.

## Open Questions

- Web GUI behavior remains a separate manual verification target; this turn's required BDD method explicitly targets Tk.
- A future upstream PR may choose to generalize paper-doll ownership beyond `{move}`, but this local fix intentionally does not.
