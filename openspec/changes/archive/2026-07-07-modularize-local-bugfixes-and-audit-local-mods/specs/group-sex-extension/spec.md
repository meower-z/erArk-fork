## MODIFIED Requirements

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
- **AND** incomplete hypnosis targets remain unchanged

## ADDED Requirements

### Requirement: Keep group-sex extension one verifiable feature mod
The group-sex extension SHALL remain a single feature mod whose three related commands are verifiable without split local bugfix components.

#### Scenario: Extension is not split
- **WHEN** the group-sex extension is packaged and loaded
- **THEN** `group_sex_extension` SHALL remain a single mod containing the batch edge, batch toy, and hypnosis boost commands
- **AND** its tests SHALL treat the three commands as related group-mode feature behavior

#### Scenario: Command registration is verified
- **WHEN** `group_sex_extension` loads through the mod loader or a near-real registration harness
- **THEN** all three command IDs SHALL be registered in the expected group-mode arts category
- **AND** the custom hypnosis-boost premise SHALL be registered and usable by the command premise map

#### Scenario: Group context selection is verified
- **WHEN** the extension collects group-mode NPCs
- **THEN** tests or BDD verification SHALL cover participants discovered through group templates and current-scene H-state characters
- **AND** the player character SHALL NOT be included as an NPC target

#### Scenario: Split local bugfix components are disabled
- **WHEN** `group_sex_extension` is tested without split local bugfix components enabled
- **THEN** the extension's own command logic SHALL still behave according to its documented feature contract
- **AND** any optional interaction with bugfix components SHALL be documented instead of hidden
