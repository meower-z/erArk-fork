# group-sex-extension Specification

## Purpose
Define the feature contract for the `group_sex_extension` maintained local mod: batch group-mode arts commands (edge, toys, hypnosis boost), their gating premises, and the mod's packaging/verification boundary.
## Requirements
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
The group-mode extension SHALL expose hypnosis boost when at least two group-mode NPCs are completely hypnotized. Complete hypnosis SHALL mean talent `73` is present or hypnosis degree is at least `200`; current `unconscious_h` activation SHALL NOT be an additional visibility or target-count requirement.

#### Scenario: Fewer than two complete hypnosis targets exist
- **WHEN** fewer than two group-mode NPCs have talent `73` or hypnosis degree at least `200`
- **THEN** the hypnosis boost premise fails

#### Scenario: Two complete targets came from different admission paths
- **WHEN** one completely hypnotized NPC began the original H interaction and a second completely hypnotized NPC was directly invited into the active group sex
- **THEN** both NPCs are counted by the same group-context eligibility rule
- **AND** the hypnosis boost command is visible even if either NPC's current hypnosis unconscious flag is not active

#### Scenario: Hypnosis boost is applied
- **WHEN** the player uses "全员催眠增强"
- **THEN** every complete hypnosis NPC in the group context receives `increase_body_sensitivity`
- **AND** every complete hypnosis NPC in the group context receives `pain_as_pleasure`
- **AND** the command does not activate, change, or clear the current hypnosis state or unconscious flag
- **AND** incomplete hypnosis targets remain unchanged

#### Scenario: Complete but currently inactive hypnosis target is enhanced
- **WHEN** a group participant has talent `73` or hypnosis degree at least `200` but `unconscious_h` is not one of the active hypnosis flags
- **THEN** the participant is still eligible for the batch enhancement fields
- **AND** whether those fields currently affect settlement remains controlled by the ordinary hypnosis-state gate

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
