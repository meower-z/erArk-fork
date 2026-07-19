# npc-move-talk-context-fix Specification

## Purpose
TBD - created by archiving change migrate-settlement-input-fixes-to-mod. Update Purpose after archive.
## Requirements
### Requirement: NPC movement text retains NPC ownership
The NPC movement-context mod SHALL format NPC `{move}` paper-doll output using the moving NPC and that NPC's scene context rather than player character 0.

#### Scenario: Several NPCs move during player travel
- **WHEN** several NPC movement settlements occur while the player travels
- **THEN** their movement text names the corresponding NPCs
- **AND** the output does not manufacture repeated lines claiming the Doctor moved at the player's unchanged scene

### Requirement: Other paper-doll behavior is unchanged
The NPC movement-context mod SHALL delegate player movement and every non-movement paper-doll input to upstream behavior unchanged.

#### Scenario: Player movement
- **WHEN** player character 0 produces `{move}` output
- **THEN** upstream player formatting remains authoritative

#### Scenario: Non-movement paper-doll text
- **WHEN** any character produces a paper-doll placeholder other than exactly `{move}`
- **THEN** the mod delegates the original input and character id unchanged
