## ADDED Requirements

### Requirement: One edging attempt for one character's detected climax group
While active edging is in effect and time-stop accumulation is not, all eligible body-part climaxes detected together for one character SHALL share one edging attempt. That attempt's difficulty SHALL include both that character's previously held climaxes and all eligible climaxes detected for that character in the current group.

#### Scenario: Several body parts climax together
- **WHEN** one character's detected group contains eligible climaxes for several body parts
- **THEN** the whole group receives one edging result
- **AND** every current eligible climax contributes to that attempt's difficulty

#### Scenario: A body part has prior held climaxes
- **WHEN** one body part has prior held climaxes and climaxes again in the current group
- **THEN** its prior and current counts combine when determining the shared difficulty

#### Scenario: Climaxes are detected in separate groups
- **WHEN** the same character has eligible climaxes in two separately detected settlement groups
- **THEN** each group receives its own edging attempt
- **AND** the result of the first group is not reused for the second

### Requirement: The whole detected group shares one outcome
After the group-level edging attempt, the system SHALL either hold the whole current group or release the whole current group together with previously held climaxes. One group SHALL NOT be partly held and partly released.

#### Scenario: The shared edging attempt succeeds
- **WHEN** the group-level edging attempt succeeds
- **THEN** every eligible climax in the current group is held
- **AND** each current normal or extra climax advances its existing level once
- **AND** an uncounted-only climax does not advance its level
- **AND** no climax in the group is treated as released

#### Scenario: The shared edging attempt fails
- **WHEN** the group-level edging attempt fails
- **THEN** no climax in the current group remains held
- **AND** the current group and previously held climaxes are released together once
- **AND** each current normal or extra climax advances its existing level once
- **AND** prior held and current uncounted-only release counts do not advance levels again
- **AND** no body part in the failed group is reported or treated as successfully held

### Requirement: Preserve other orgasm-settlement rules
The system SHALL preserve existing behavior when no group-level edging attempt is required, including ordinary orgasm settlement, time-stop accumulation, explicit release, level semantics, visible behaviors, and downstream effect batching.

#### Scenario: No eligible climax is detected
- **WHEN** a settlement group contains no eligible climax
- **THEN** no edging attempt occurs
- **AND** edging state remains unchanged

#### Scenario: Active edging is not in effect
- **WHEN** climaxes are detected while active edging is not in effect
- **THEN** they follow the existing ordinary settlement behavior

#### Scenario: Time-stop accumulation is active
- **WHEN** climaxes are detected during the existing time-stop accumulation state
- **THEN** they follow the existing time-stop accumulation behavior
- **AND** no active-edging attempt occurs

#### Scenario: Previously held climaxes are explicitly released
- **WHEN** the existing explicit-release action releases held climaxes
- **THEN** it follows the existing explicit-release behavior
- **AND** it does not make a new edging attempt
