## ADDED Requirements

### Requirement: Attribute deferred release effects to their NPC
The system SHALL record each NPC's deferred time-stop orgasm release in that NPC's target-owned settlement change object.

#### Scenario: One NPC releases several body-part orgasms
- **WHEN** `TIME_STOP_OFF` releases non-zero deferred orgasm counts for one NPC
- **THEN** the generated status, point, and experience changes are stored under `target_change[npc_id]`
- **AND** the player's root status and experience maps do not receive those NPC changes
- **AND** settlement levels and labels are calculated from the NPC's values

#### Scenario: Several NPCs release in one action
- **WHEN** two or more NPCs have deferred orgasm counts
- **THEN** each NPC receives a distinct target-owned change block
- **AND** no NPC's effects are merged into another NPC or the player

#### Scenario: Web collects release changes
- **WHEN** Web mode collects the `TIME_STOP_OFF` settlement
- **THEN** each released NPC's values are emitted with that NPC's character ID
- **AND** the values are not silently dropped as player-root floating changes

### Requirement: Settle a deferred release exactly once
The system SHALL preserve exactly-once ownership between synchronous H-orgasm batch settlement and the later generic NPC second-stage pass.

#### Scenario: Batch mod owns generated orgasm effects
- **WHEN** the enabled H-orgasm batch mod synchronously settles release-generated second behaviors
- **THEN** its ownership marker is stored on the same NPC `TargetChange` received by the later generic pass
- **AND** the generic pass consumes the marker once without replaying those behaviors
- **AND** unrelated queued second behaviors still settle normally

#### Scenario: NPC has no deferred orgasm count
- **WHEN** an NPC has zero deferred counts at time resume
- **THEN** that NPC is not marked `time_stop_release`
- **AND** no empty orgasm batch is generated
- **AND** unconscious clothing and semen recovery cleanup still runs

#### Scenario: Batch mod is disabled
- **WHEN** a release generates second behaviors while the H-orgasm batch mod is disabled
- **THEN** the ordinary generic second-stage pass settles those behaviors once into the NPC's target-owned change
- **AND** no synchronous-owner marker suppresses them

#### Scenario: Batch mod is enabled with unrelated queued effects
- **WHEN** the batch mod synchronously owns release-generated effects and the NPC also has unrelated queued second behaviors
- **THEN** the mod removes and marks only the release-generated work it consumed
- **AND** the generic pass skips only that owned work and settles the unrelated queue once

#### Scenario: Player ID appears in the NPC set
- **WHEN** the NPC iteration source unexpectedly contains character ID 0
- **THEN** the release pass excludes ID 0 without mutating the shared NPC set
- **AND** every actual NPC remains eligible for cleanup and release

#### Scenario: Deferred NPC is outside the player's current scene
- **WHEN** a registered remote NPC has deferred release state
- **THEN** ownership, counter clearing, cleanup, and mod-on or mod-off second-stage behavior follow the same exactly-once rules

### Requirement: Format compact signed values with the correct unit
The system SHALL choose compact suffixes from the absolute numeric magnitude and apply the sign independently.

#### Scenario: Thousand boundary
- **WHEN** values from 1000 through 999999 are formatted compactly
- **THEN** they use the K suffix rather than M

#### Scenario: Million boundary
- **WHEN** an absolute value is at least 1000000 and below 1000000000
- **THEN** it uses the M suffix

#### Scenario: Negative value below one thousand
- **WHEN** a value such as -500 is formatted
- **THEN** it remains a signed numeric value such as `-500`
- **AND** it is not reduced to a bare suffix such as `-M`

#### Scenario: Positive and negative compact values
- **WHEN** positive and negative values have the same absolute magnitude
- **THEN** they use the same significant digits and suffix with only the sign differing

#### Scenario: Shared formatter is used outside time-stop release
- **WHEN** core state, core experience, or batch window-end output calls the compact formatter
- **THEN** the same absolute-magnitude and independent-sign rules apply
- **AND** the fix does not rely on time-stop-specific caller state
