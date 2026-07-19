## ADDED Requirements

### Requirement: Settle discovered group admission exactly once
The local bugfix layer SHALL settle a discoverer's group admission or refusal exactly once, independent of whether the discovery panel was opened by the NPC behavior loop or by a direct hidden-discovery call.

#### Scenario: Initial H converts to group sex from NPC discovery
- **WHEN** an NPC behavior dispatch discovers a single-target H scene and accepts the group invitation
- **THEN** `DISCOVER_OTHER_SEX_AND_JOIN` settles before the nested player group-conversion update
- **AND** the discoverer is in H state when that nested update evaluates participants
- **AND** the later outer NPC settlement does not replay the admission behavior

#### Scenario: Existing group sex accepts a discoverer
- **WHEN** group mode is already active and an NPC behavior dispatch accepts a discoverer's invitation
- **THEN** `JOIN_GROUP_SEX` settles exactly once
- **AND** selecting that NPC as the player target exposes the normal group-sex action interface

#### Scenario: Direct hidden-discovery call accepts a discoverer
- **WHEN** the discovery panel is opened directly outside the NPC behavior loop and the discoverer accepts
- **THEN** the admission behavior settles before the panel returns
- **AND** the implementation does not wait for an outer NPC settlement that will never occur

#### Scenario: Discoverer refuses or interrupts
- **WHEN** a discoverer refuses an active group invitation or ends the H scene
- **THEN** the selected refusal or interruption behavior settles exactly once
- **AND** no stale admission or suppression state affects a later NPC action

### Requirement: Evaluate every scene character for group invitation eligibility
The local bugfix layer SHALL report that a scene is entirely outside H only after checking every non-player character in that scene.

#### Scenario: A later scene character is already in H
- **WHEN** the first inspected NPC is not in H but any later NPC is in H
- **THEN** the `place_all_not_h` premise fails
- **AND** the ordinary "invite group sex" start control is not shown alongside controls for an active group scene

#### Scenario: Every scene NPC is outside H
- **WHEN** at least two characters are present and every non-player character is outside H
- **THEN** the `place_all_not_h` premise succeeds

#### Scenario: Registered premise is evaluated
- **WHEN** instruction judgement resolves `place_all_not_h` through the runtime premise registry
- **THEN** it invokes the corrected full-scene implementation rather than an import-time stale function

### Requirement: Present a coherent interface for the admitted participant
After discovered admission settles, the local bugfix layer SHALL make the admitted NPC's participant state and the player's available controls agree.

#### Scenario: Player selects the newly admitted NPC
- **WHEN** a discoverer accepts, the admission has settled exactly once, and the player switches the selected target to that NPC
- **THEN** the normal group-sex action interface for that participant is available
- **AND** the ordinary invite-group start control is absent
- **AND** the valid end-group control remains available

### Requirement: Scope any early-settlement suppression to one dispatch
If admission is settled before a later outer NPC settlement, the local bugfix layer SHALL bind suppression to that exact character dispatch and SHALL NOT suppress any later or unrelated behavior.

#### Scenario: Expected outer settlement never occurs
- **WHEN** a path settles admission early but exits without the expected matching outer settlement
- **THEN** no suppression state survives to a later behavior

#### Scenario: Nested and interleaved NPC work occurs
- **WHEN** the same NPC is re-entered or another NPC is processed before the original dispatch completes
- **THEN** only the exact already-consumed admission can be skipped
- **AND** every other behavior settles normally

#### Scenario: Target search exits exceptionally
- **WHEN** target search or a discovery callback raises, catches, or returns early
- **THEN** dispatch ownership is cleaned without consuming a later behavior

### Requirement: Compose with other target-selection wrappers
The admission fix SHALL preserve every independently installed `find_character_target()` wrapper regardless of supported mod load order or repeated loading.

#### Scenario: Group intent and admission wrappers are both enabled
- **WHEN** `local_group_masturbation_intent_fix` and this component are loaded in either supported order
- **THEN** both wrappers execute with their intended behavior
- **AND** reload does not duplicate, bypass, or reorder effects into an invalid chain
