## Context

The playtest exercised the Tkinter game window as a player would: title screen, load-save flow, main scene commands, settings, and optional AI dialogue. Several issues share the same shape: a new panel is appended below old content, stale buttons can still look selectable, and important feedback can fall outside the visible viewport unless the window is maximized.

UI fixes may need careful wrapping around existing panel functions because many affected panels are core UI panels.

## Goals / Non-Goals

**Goals:**

- Make active UI state unambiguous after panel transitions, nested menus, and pagination.
- Make save-list boundary and empty-slot behavior deterministic and visible.
- Make disabled optional features return to the previous panel without a hidden or delayed affordance.
**Non-Goals:**

- Rewriting the renderer, event loop, or save-file format.
- Changing game balance or H settlement values.
- Turning transcript history into a full scrollback redesign. Existing historical output can remain if it is clearly distinct from the active controls.

## Decisions

### Targeted panel hooks

Implement runtime fixes through targeted panel hooks where the target behavior can be patched safely. If a UI issue cannot be reliably patched from a narrow hook, document the exact core hook needed before changing core files.

Alternative considered: edit the affected core panels broadly. That is simpler for UI code but makes future upstream sync harder.

### Treat active panel state as the boundary, not the full screen buffer

The fix should not require every panel to clear all historical output. Instead, the active controls for the current panel must be visually scoped and old controls must not remain highlighted or actionable. Where panels already intend a modal transition, clearing or redrawing the active area is acceptable.

Alternative considered: clear the entire screen before every panel draw. That would be broad and may remove useful context in panels that intentionally show recent output.

### Save pagination should not silently wrap

The save list should either clamp boundary buttons or provide explicit wrap labels/feedback. The preferred behavior is clamping or disabling boundary commands because the current labels `上一页` and `下一页` imply local movement, not circular navigation.

Alternative considered: keep wraparound behavior. It is faster for expert users but caused immediate confusion in playtest and makes stale appended pages harder to reason about.

## Risks / Trade-offs

- Active-panel fixes may affect many panels -> Start with the panels reproduced in playtest and add a small shared helper only if duplicated logic appears.
- Wrappers around UI functions may be fragile across upstream updates -> Keep wrapper targets narrow and add tests or manual checklist steps tied to visible behavior.
- Save pagination tests may be hard without a UI harness -> Cover pure page-index logic with tests and retain a manual verification checklist for rendering.

## Migration Plan

1. Patch the smallest set of UI panel functions needed to stabilize the reproduced flows.
2. Run focused automated checks where practical and manually replay the title, save-list, settings, and AI-disabled flows in the game window.
3. If a broad core change is unavoidable, stop and document the proposed core hook before implementation.

## Open Questions

- Should save pagination boundary buttons be hidden, disabled, or kept visible with explicit boundary feedback?
- Should startup force a minimum/maximized window, or should the title screen provide scroll/continue affordances at smaller sizes?
- Which UI panels should preserve transcript history versus always redraw the active command area?
