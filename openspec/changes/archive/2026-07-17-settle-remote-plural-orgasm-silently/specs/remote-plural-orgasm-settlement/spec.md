## ADDED Requirements

### Requirement: Settle remote plural orgasms without showing their talk
The system SHALL settle `plural_orgasm_2` through `plural_orgasm_11` when the character is away from the player, and SHALL NOT show that remote character's plural-orgasm talk to the player.

#### Scenario: Remote character receives a plural-orgasm behavior
- **WHEN** a character away from the player receives any behavior from `plural_orgasm_2` through `plural_orgasm_11`
- **THEN** the configured effects for that behavior are settled during the remote second-behavior pass
- **AND** the configured plural-orgasm value changes are applied rather than discarded
- **AND** the behavior is cleared from the character's pending second-behavior state
- **AND** no plural-orgasm talk for that remote behavior is displayed

#### Scenario: Remote character later reaches the player
- **WHEN** a remote plural-orgasm behavior has already settled and the character later enters the player's location
- **THEN** the previously settled behavior does not display delayed plural-orgasm talk
- **AND** its configured effects are not settled a second time

#### Scenario: Nearby character receives a plural-orgasm behavior
- **WHEN** a character in the player's location receives any behavior from `plural_orgasm_2` through `plural_orgasm_11`
- **THEN** the existing plural-orgasm talk is displayed
- **AND** the configured effects are settled once

#### Scenario: Character approaches and discovers ongoing group sex
- **WHEN** a character's remote plural-orgasm behavior has already settled and that character later reaches the player during ongoing group sex
- **THEN** the existing group-sex discovery flow remains available under its original premises
- **AND** discovery does not require a stale plural-orgasm second behavior to remain queued

### Requirement: Keep directly drawn orgasm derivatives outside the marker-only fix
The system MUST NOT treat `extra_orgasm`, `b_orgasm_to_milk`, or `u_orgasm_to_pee` as covered by this marker-only change.

#### Scenario: Reviewing the marker-only configuration change
- **WHEN** the proposed behavior-effect configuration diff is inspected
- **THEN** `997` is added only to `plural_orgasm_2` through `plural_orgasm_11`
- **AND** the three directly drawn derivative behaviors remain unchanged
- **AND** their analogous remote-delay behavior remains a known unresolved defect rather than being claimed as fixed
