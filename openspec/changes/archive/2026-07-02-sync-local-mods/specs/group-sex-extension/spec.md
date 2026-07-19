## ADDED Requirements

### Requirement: Provide group-mode batch arts commands
The group-mode extension SHALL register batch arts commands for all current group-mode NPCs.

#### Scenario: Batch edge command is used
- **WHEN** the player uses the "全员寸止" command in group mode
- **THEN** every discovered group-mode NPC that is not already in edge mode enters edge mode
- **AND** the result text reports changed count and total target count

#### Scenario: Batch toy command is used
- **WHEN** the player uses the "全员戴上玩具" command in group mode
- **THEN** body item slots `0`, `1`, `2`, and `3` are ensured and equipped where absent
- **AND** the result text reports changed character count and item count

### Requirement: Gate and apply group hypnosis boost
The group-mode extension SHALL expose hypnosis boost only when at least two group-mode NPCs are completely hypnotized.

#### Scenario: Fewer than two complete hypnosis targets exist
- **WHEN** fewer than two group-mode NPCs have talent `73` or hypnosis degree at least `200`
- **THEN** the hypnosis boost premise fails

#### Scenario: Hypnosis boost is applied
- **WHEN** the player uses "全员催眠增强"
- **THEN** every complete hypnosis NPC in the group context receives `increase_body_sensitivity`
- **AND** every complete hypnosis NPC in the group context receives `pain_as_pleasure`
- **AND** the command does not change the current hypnosis state or unconscious flag
