## Why

2026-07-04 manual playtesting of the maximized Tkinter game window found several corner-case regressions where UI state, save-list navigation, and optional AI messaging become ambiguous. These issues are easy to miss in isolated unit tests because they appear after navigating across nested panels.

## What Changes

- Define a UI panel stability contract so active panels redraw or scope themselves clearly, stale controls do not look actionable, and small-window startup has an explicit playable affordance.
- Make save-slot pagination and empty-slot interactions deterministic, including boundary behavior, feedback, and confirmation placement.
- Require disabled optional integrations, such as text-generation AI dialogue, to provide an immediate visible return or continue affordance.
- Keep implementation focused on UI panel stability; direct core-game changes require explicit approval if later implementation cannot be safely achieved from narrow panel hooks.

## Capabilities

### New Capabilities

- `ui-panel-stability`: Covers active-panel redraw semantics, stale-control visibility, save-list navigation feedback, startup layout affordances, and disabled optional-feature return flows.

## Impact

- Affected areas include title/startup UI, save/load panels, nested settings panels, movement command panels, and optional AI dialogue panel.
- Expected implementation should prefer targeted panel hooks to avoid broad renderer rewrites.
- Verification should combine focused automated checks where practical with manual playthrough checks for panel transitions that are difficult to model in pure tests.
