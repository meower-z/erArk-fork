## 1. Reproduction Baseline

- [ ] 1.1 Record fresh screenshots or notes for title startup at non-maximized and maximized window sizes.
- [ ] 1.2 Reproduce save-list first-page previous, last-page next, empty-slot click, and valid-slot confirmation flows.
- [ ] 1.3 Reproduce settings-group expansion and confirm whether old controls remain highlighted or actionable.
- [ ] 1.4 Reproduce disabled AI dialogue flow and confirm whether return controls appear only after an unlabeled keypress.

## 2. UI Panel Stability

- [ ] 2.1 Identify the smallest panel or flow-control hook that can distinguish active controls from historical output.
- [ ] 2.2 Patch save-list pagination so boundary commands clamp or disable instead of silently wrapping.
- [ ] 2.3 Add empty-save-slot feedback and keep save navigation and return controls visible afterward.
- [ ] 2.4 Patch save-slot read/delete/confirm rendering so confirmation controls appear in the active panel area without stale page competition.
- [ ] 2.5 Patch settings expansion so repeated expansion updates one current settings panel instead of appending duplicate full-panel copies.
- [ ] 2.6 Patch disabled optional integration panels so the disabled message and return or continue command draw together.
- [ ] 2.7 Address title startup usability with either a visible small-window command, explicit affordance, or documented minimum/maximized window behavior.

## 3. Verification

- [ ] 3.1 Run syntax or import validation for modified UI hooks.
- [ ] 3.2 Manually replay title, save-list, settings, and AI-disabled flows in the game window.
- [ ] 3.3 Document any remaining broad core-code-only UI limitation before requesting approval for non-hook edits.
