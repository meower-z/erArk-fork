## ADDED Requirements

### Requirement: Sleep exit preserves pain-as-pleasure
The sleep-driven hypnosis exit SHALL leave `hypnosis.pain_as_pleasure` unchanged while performing its existing cleanup of other hypnosis exit state.

#### Scenario: Sleep exit with pain-as-pleasure enabled
- **WHEN** `HYPNOSIS_FLAG_TO_0` runs for a character whose `hypnosis.pain_as_pleasure` is true
- **THEN** the value SHALL remain true after the exit completes

#### Scenario: Sleep exit with pain-as-pleasure disabled
- **WHEN** `HYPNOSIS_FLAG_TO_0` runs for a character whose `hypnosis.pain_as_pleasure` is false
- **THEN** the value SHALL remain false after the exit completes

### Requirement: Direct exit remains unchanged
The direct `解除催眠` path SHALL retain its existing behavior, including preserving `hypnosis.pain_as_pleasure` and performing its path-specific cleanup and settlement.

#### Scenario: Direct exit with pain-as-pleasure enabled
- **WHEN** direct `解除催眠` runs for a target whose `hypnosis.pain_as_pleasure` is true
- **THEN** the value SHALL remain true and the path's existing hypnosis cleanup SHALL still complete

### Requirement: Hypnosis exit does not own NPC initiative
Neither hypnosis exit path SHALL modify `h_state.npc_active_h`.

#### Scenario: NPC initiative is active before either exit
- **WHEN** either hypnosis exit path runs while `h_state.npc_active_h` is true
- **THEN** `h_state.npc_active_h` SHALL remain true

#### Scenario: NPC initiative is inactive before either exit
- **WHEN** either hypnosis exit path runs while `h_state.npc_active_h` is false
- **THEN** `h_state.npc_active_h` SHALL remain false

### Requirement: Minimum implementation boundary
The production change SHALL remove the sleep path's clearing of `hypnosis.pain_as_pleasure` and SHALL extract only the four sub-state resets already shared by both paths into a common helper.

#### Scenario: Candidate diff is reviewed
- **WHEN** the corrected candidate is compared with its upstream base
- **THEN** its helper SHALL reset only `increase_body_sensitivity`, `blockhead`, `active_h`, and `roleplay`, while both callers retain their existing unconscious matching, abnormal-flag recalculation, and path-specific operations

#### Scenario: Helper is compared with existing code
- **WHEN** an upstream reviewer reads the new helper
- **THEN** its state mutations SHALL be a direct extraction of the four assignments already present in the direct `解除催眠` path, without new cleanup responsibilities

### Requirement: Representative Tk evidence
The preparation workflow SHALL provide one repeatable real-Tk A/B comparison for the sleep-driven exit using the same save, Tk configuration, and player route.

#### Scenario: Upstream and corrected candidate are compared
- **WHEN** the visual subagent captures the state before and after sleep-driven hypnosis exit
- **THEN** both runs SHALL show `苦痛→快感` before exit, upstream SHALL lose it after exit, and the corrected candidate SHALL retain it

### Requirement: Local frame-by-frame visual interaction
The evidence workflow MUST use a visual agent on an isolated local X display, inspecting the current Tk frame before choosing and performing each single local action.

#### Scenario: Visual route is operated
- **WHEN** the visual agent advances the real Tk flow
- **THEN** it SHALL use `import -window`, `view_image`, and one visually selected `xdotool` action at a time without blind batches or network desktop exposure

### Requirement: Reviewer findings remain clues
Fresh review findings SHALL be evaluated as investigation clues and SHALL NOT become implementation tasks merely because the reviewer raised them.

#### Scenario: Reviewer raises a concern
- **WHEN** the reviewer identifies a possible wider issue or alternative boundary
- **THEN** the concern SHALL be recorded with its evidence and assessed against the confirmed rule before any task or code change is proposed

### Requirement: Separate publication authorization
The workflow MUST NOT push, upload, publish, or create or edit a PR without separate user authorization for that outward-facing action.

#### Scenario: Corrected local artifacts are ready
- **WHEN** implementation, verification, evidence, and PR drafting complete locally
- **THEN** the workflow SHALL stop before outward-facing changes and wait for authorization
