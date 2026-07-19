## ADDED Requirements

### Requirement: Merge orgasm edge judgment per player action window
The system SHALL perform at most one orgasm edge success/failure roll per character within one player action window (one player instruction click), reusing that roll's result for every later orgasm-level crossing by the same character in the same window.

#### Scenario: Multiple parts cross in one settlement pass
- **WHEN** a character under active edging has two or more body parts cross an orgasm level in the same orgasm settlement pass
- **THEN** the system rolls edge success exactly once for that character
- **AND** every crossing part's climax count is added to that part's `orgasm_edge_count` on success

#### Scenario: Later settlement passes in the same player action window
- **WHEN** the same character crosses an orgasm level again in a later settlement pass of the same player action window (for example through ambient group-sex pleasure growth or masturbation settlement)
- **THEN** the system does not roll again and reuses the window's stored result
- **AND** on a stored success the new crossing parts' climax counts are still merged into `orgasm_edge_count` (merged, not skipped)

#### Scenario: New player action window resets the roll
- **WHEN** the player issues the next instruction (a new `over_behavior_character` action slice begins)
- **THEN** the next orgasm-level crossing rolls edge success anew
- **AND** the roll uses the accumulated `orgasm_edge_count` values, preserving the declining success rate across actions

#### Scenario: Edge failure path is never suppressed
- **WHEN** the single per-window roll fails
- **THEN** the character's `orgasm_edge` is set to 3 and the existing failure-release settlement runs unchanged
- **AND** the window cache does not block or alter the failure-release path in later settlement passes

#### Scenario: Time-stop edging path is unaffected
- **WHEN** a character is under the time-stop unconscious state (`unconscious_flag_3`)
- **THEN** crossings are recorded into `time_stop_orgasm_count` as before and never enter the per-window edge judgment

### Requirement: Show one edge prompt and one representative edge talk per window
The system SHALL display at most one edge success/failure prompt per character per player action window, and at most one representative `{part}_orgasm_edge` talk when multiple parts merge under one judgment.

#### Scenario: Single-part edge display is unchanged
- **WHEN** exactly one part crosses under edging in the window's rolling settlement pass
- **THEN** the original success / at-limit / failure prompt is shown once
- **AND** that part's `{part}_orgasm_edge` talk plays as today

#### Scenario: Multi-part merged edge display
- **WHEN** two or more parts merge under one edge judgment in the same settlement pass
- **THEN** the original prompt is shown once followed by one part-list line naming all merged parts
- **AND** only one representative part's `{part}_orgasm_edge` talk plays, chosen by highest merged climax count with ties broken randomly

#### Scenario: Silent merge in later passes shows nothing
- **WHEN** a later settlement pass in the same window merges additional crossings into a stored success
- **THEN** no additional prompt or edge talk is displayed for those crossings
- **AND** the merged counts are still fully reflected in the eventual edge release settlement
