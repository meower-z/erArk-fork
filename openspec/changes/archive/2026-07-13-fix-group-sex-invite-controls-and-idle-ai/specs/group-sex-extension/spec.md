## MODIFIED Requirements

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
