## MODIFIED Requirements

### Requirement: Keep pain-as-pleasure scoped and consistent
The local bugfix layer SHALL activate `pain_as_pleasure` whenever its granted flag is set, regardless of the character's sleep or unconscious state, SHALL apply it consistently to positive direct pain increases only, and SHALL restore ordinary pain settlement as soon as that flag is cleared.

Pain-as-pleasure is an intentional, explicit exception to the upstream rule that psychological pleasure does not settle while a character is asleep or unconscious: converted psychological pleasure SHALL post even for a sleeping or unconscious character. This override applies only to the pain conversion path; every other psychological-pleasure source keeps the upstream guard.

#### Scenario: Hypnosis is cancelled
- **WHEN** hypnosis cancellation settles for a character whose target has `pain_as_pleasure`
- **THEN** the target's `pain_as_pleasure` flag is cleared
- **AND** a later positive pain settlement increases ordinary pain rather than psychological pleasure

#### Scenario: Awake granted character has no active hypnosis unconscious state
- **WHEN** an awake, conscious character carries `pain_as_pleasure` while `unconscious_h == 0`
- **THEN** positive pain settles as psychological pleasure
- **AND** ordinary pain does not increase
- **AND** settlement does not change the character's unconscious or hypnosis state

#### Scenario: Sleeping or unconscious granted character takes positive pain
- **WHEN** a positive pain settlement occurs for a sleeping or unconscious character while `pain_as_pleasure` is active
- **THEN** the converted amount posts as psychological pleasure despite the upstream sleep/unconscious guard
- **AND** ordinary pain does not increase

#### Scenario: Pain decreases while pain-as-pleasure is active
- **WHEN** a pain state settlement has a non-positive final pain change
- **THEN** that change settles through the ordinary pain path
- **AND** the granted flag remains active afterward

#### Scenario: Common pain aliases settle positive pain
- **WHEN** default, second-effect, realtime, or item settlement invokes the shared positive pain handler for an awake, conscious character while `pain_as_pleasure` is active
- **THEN** every alias uses the same converted handler
- **AND** the amount is recorded under psychological pleasure rather than pain

#### Scenario: Direct second effect adds pain
- **WHEN** a direct second effect would add small, middle, large, or extra-orgasm pain to an awake, conscious character while `pain_as_pleasure` is active
- **THEN** the positive pain amount is settled as psychological pleasure instead of direct pain

#### Scenario: Later group participant receives and uses the grant
- **WHEN** a conscious NPC joins group sex after discovery or direct invitation, the group participant resolver includes that NPC, and hypnosis boost grants `pain_as_pleasure`
- **THEN** the NPC's next positive pain settlement converts to psychological pleasure
- **AND** the connected path does not depend on manually constructing the final character state

#### Scenario: Enhancement is toggled or fully reset off
- **WHEN** the ordinary toggle, hypnosis cancellation, full hypnosis cleanup, or local hypnosis-state reset clears `pain_as_pleasure`
- **THEN** the next positive pain settlement follows ordinary pain behavior
- **AND** no patched alias or direct effect retains a hidden active copy of the grant

#### Scenario: Repeated instruction adjustment applies
- **WHEN** positive common pain is converted during a repeated instruction sequence
- **THEN** its psychological-pleasure amount follows the accepted upstream-equivalent adjustment sequence
- **AND** the conversion does not silently omit or double-apply an adjustment

#### Scenario: Converted value reaches the status cap
- **WHEN** converted psychological pleasure would exceed 99999
- **THEN** stored state remains within the configured cap
- **AND** the change record reports the upstream-compatible requested value consistently for both root and target-owned records

#### Scenario: Existing entry-specific death behavior applies
- **WHEN** a common or direct positive-pain entry is invoked for a dead character
- **THEN** the conversion preserves that entry's upstream early-return behavior
- **AND** the fix does not invent a universal guard that changes another entry's semantics
