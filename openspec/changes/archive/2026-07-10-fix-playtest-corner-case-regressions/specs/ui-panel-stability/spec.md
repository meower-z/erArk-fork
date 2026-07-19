## ADDED Requirements

### Requirement: Keep active panel controls unambiguous
The UI SHALL ensure that only controls belonging to the current active panel appear actionable after a panel transition.

#### Scenario: Nested panel opens over a previous panel
- **WHEN** the player opens a nested panel from the main scene, settings, movement, or save-load flow
- **THEN** stale controls from the previous panel SHALL NOT remain visually highlighted or actionable
- **AND** the current panel's return or confirmation controls SHALL be visible in the active viewport when the panel is drawn

#### Scenario: Returning from a nested panel
- **WHEN** the player returns from a nested panel
- **THEN** the previous active panel SHALL be redrawn or restored without duplicate copies of the same command group
- **AND** obsolete controls from the nested panel SHALL NOT remain selectable

### Requirement: Startup menu is playable without hidden controls
The title/startup UI SHALL expose a visible way to start, load, configure, or exit the game without relying on an unannounced maximized window.

#### Scenario: Title screen opens below maximized size
- **WHEN** the game opens at a window size smaller than the maximized desktop window
- **THEN** at least one primary title command or an explicit continue/scroll affordance SHALL be visible
- **AND** the player SHALL NOT need out-of-game knowledge that the window must be maximized to reveal the menu

### Requirement: Save list navigation is deterministic and visible
The save/load panel SHALL keep pagination, empty-slot feedback, and confirm prompts deterministic and visible.

#### Scenario: Previous page selected on first save page
- **WHEN** the save/load panel is on the first page
- **AND** the player selects the previous-page command
- **THEN** the panel SHALL either remain on the first page with boundary feedback or show the command as disabled
- **AND** it SHALL NOT silently append the last page below the old first page

#### Scenario: Next page selected on last save page
- **WHEN** the save/load panel is on the last page
- **AND** the player selects the next-page command
- **THEN** the panel SHALL either remain on the last page with boundary feedback or show the command as disabled
- **AND** it SHALL NOT silently append the first page below the old last page

#### Scenario: Empty save slot selected
- **WHEN** the player selects an empty save slot
- **THEN** the panel SHALL show explicit feedback that the slot cannot be loaded
- **AND** it SHALL keep the save/load panel in a usable state with visible navigation and return controls

#### Scenario: Save load confirmation appears
- **WHEN** the player selects a valid save slot and reaches the read/delete/confirm flow
- **THEN** the confirmation controls SHALL appear in the active panel area
- **AND** old save-list pages SHALL NOT obscure or visually compete with the confirmation controls

### Requirement: Optional disabled integrations provide immediate return
Panels for disabled optional integrations SHALL provide immediate visible recovery controls.

#### Scenario: Text-generation AI dialogue is disabled
- **WHEN** the player opens the AI dialogue command while text-generation AI is disabled
- **THEN** the panel SHALL show the disabled-state message and a visible return or continue command in the same draw
- **AND** the player SHALL NOT need to press an unlabeled key before the return command appears

### Requirement: Repeated expansion does not duplicate whole panels
Expandable UI sections SHALL update their current section state without appending duplicate full-panel copies.

#### Scenario: Settings section is expanded
- **WHEN** the player opens system settings and expands a settings group
- **THEN** the settings panel SHALL show one current copy of the settings command list
- **AND** prior collapsed or expanded copies SHALL NOT remain as active-looking controls above or below the current panel
