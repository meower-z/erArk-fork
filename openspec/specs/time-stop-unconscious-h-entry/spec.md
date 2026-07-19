# time-stop-unconscious-h-entry Specification

## Purpose
TBD - created by archiving change restore-time-stop-unconscious-h-entry. Update Purpose after archive.
## Requirements
### Requirement: Expose unconscious H for valid unconscious targets
The system SHALL expose and execute instruction 5052 when the selected target has any registered nonzero unconscious state and every independent configured requirement is valid.

#### Scenario: Valid time-stopped target
- **WHEN** time stop is active, the selected NPC has `unconscious_h == 3`, neither character is already in H, and all other configured requirements pass
- **THEN** instruction 5052 is visible in the obscenity action interface
- **AND** selecting it enters the existing unconscious-H flow

#### Scenario: Location does not alter the premise
- **WHEN** the same valid target and player state exists in the Central Lounge or another ordinary room
- **THEN** instruction visibility and execution follow the same premise chain

#### Scenario: Other registered unconscious sources
- **WHEN** the selected target has `unconscious_h` state 1, 2, 4, 5, 6, or 7 and every other requirement is valid
- **THEN** instruction 5052 remains available

### Requirement: Apply pregnancy guards independently of imprisonment
The system SHALL block instruction 5052 for parturient and postpartum targets without using cooperation or imprisonment as a proxy.

#### Scenario: Parturient target
- **WHEN** the selected unconscious target is parturient
- **THEN** instruction 5052 is unavailable

#### Scenario: Postpartum target
- **WHEN** the selected unconscious target is postpartum
- **THEN** instruction 5052 is unavailable

#### Scenario: Imprisonment cannot bypass pregnancy guards
- **WHEN** a parturient or postpartum unconscious target is also imprisoned
- **THEN** instruction 5052 remains unavailable

### Requirement: Preserve the existing independent action gates
The premise correction SHALL retain target selection, non-H state, hidden-interface presentation, and player stamina requirements.

#### Scenario: No selected target
- **WHEN** no target is selected
- **THEN** instruction 5052 is unavailable

#### Scenario: Target is already in H
- **WHEN** the selected unconscious target is already in H
- **THEN** instruction 5052 is unavailable

#### Scenario: Hidden non-H interface is active
- **WHEN** the existing `NOT_SHOW_NON_H_IN_HIDDEN_SEX` premise fails
- **THEN** instruction 5052 is unavailable

#### Scenario: Player cannot pay the action requirement
- **WHEN** the player fails the configured stamina requirement
- **THEN** instruction 5052 is unavailable

### Requirement: Verify source and runtime instruction data safely
The change SHALL verify instruction 5052 from rebuilt runtime data while preserving unrelated localization work.

#### Scenario: Source changed but runtime data is stale
- **WHEN** `InstructConfig.csv` has the accepted orthogonal premise chain but ignored `data/data.json` still has the old composite
- **THEN** the change is runtime-incomplete
- **AND** source inspection alone is not acceptance evidence

#### Scenario: Runtime data is rebuilt
- **WHEN** local verification regenerates the runtime configuration
- **THEN** protected PO files remain byte-identical
- **AND** a structured read of `data/data.json` proves instruction 5052 contains `T_UNCONSCIOUS_FLAG`, `T_PARTURIENT_0`, and `T_POSTPARTUM_0`
- **AND** the old cooperation-or-imprisonment composite is absent from that instruction
