## ADDED Requirements

### Requirement: Implement batch settlement as a local bugfix mod
The system SHALL implement the H orgasm batch settlement fixes through the enabled `local_bugfix` mod rather than direct edits to core game files.

#### Scenario: Core game files remain untouched
- **WHEN** the change is installed
- **THEN** the replacement behavior is registered from `mod/local_bugfix/mod_info.json`
- **AND** core files such as `Script/Design/second_behavior.py` and `Script/Design/handle_npc_ai.py` do not need direct edits for this fix

### Requirement: Batch NPC orgasm events during H settlement
The system SHALL treat all NPC orgasm events detected during one orgasm settlement pass as a single batch before executing display and effect settlement.

#### Scenario: One body part reaches multiple orgasm strengths in one batch
- **WHEN** a body part generates multiple orgasm behavior IDs in the same batch, such as `c_orgasm_small`, `c_orgasm_normal`, and `c_orgasm_strong`
- **THEN** the batch records every distinct generated behavior ID for effect settlement
- **AND** the batch selects only the strongest behavior ID for that body part's visible talk

#### Scenario: Repeated same behavior ID occurs in one batch
- **WHEN** the same orgasm behavior ID is generated more than once in the same batch
- **THEN** the system preserves the original second-behavior switch semantics
- **AND** that behavior ID is settled once in the batch, matching the original `Character.second_behavior` behavior

### Requirement: Show only representative orgasm talk
The system SHALL separate orgasm effect settlement from orgasm talk display so that non-representative orgasm events can settle silently.

#### Scenario: Single-part multi-orgasm display
- **WHEN** one body part has multiple orgasm events in the same batch
- **THEN** the system displays at most one part orgasm info line and at most one part orgasm talk for that body part
- **AND** the displayed part orgasm is the strongest event selected for that part

#### Scenario: Multi-part orgasm display
- **WHEN** two or more body parts orgasm in the same batch
- **THEN** the system first displays the matching original multiple-orgasm info and talk
- **AND** the system displays each orgasming body part exactly once in the following body-part detail output
- **AND** no more than three representative body parts use the original part-orgasm info-and-talk format
- **AND** body parts outside those three representatives display short strength text only in one grouped line
- **AND** representative body parts do not receive an additional duplicate strength-only line

#### Scenario: Representative part info keeps compact spacing
- **WHEN** a representative body part displays its original-format strength info followed by orgasm talk
- **THEN** the strength info and following talk are separated by exactly one blank line
- **AND** the compact formatting does not add extra blank lines before the next representative body part

#### Scenario: Remaining body parts are summarized on one line
- **WHEN** body parts outside the representative limit need strength-only display
- **THEN** the system groups body-part names by orgasm strength
- **AND** the remaining body-part summary is displayed as one line in the form `{character name} <parts> 强绝顶，<parts> 绝顶，<parts> 小绝顶`

#### Scenario: Representative body parts are selected by importance
- **WHEN** more than three body parts orgasm in the same batch
- **THEN** the system selects representatives from the highest orgasm strength first
- **AND** when multiple body parts tie at the same strength, the tied representatives are chosen randomly

### Requirement: Preserve existing orgasm effects and values
The system SHALL preserve existing configured effects for part orgasms, plural orgasms, extra orgasms, milk release, urine release, exposure checks, experience gains, and human-power generation.

#### Scenario: Lower-strength orgasms are hidden but still settled
- **WHEN** a lower-strength distinct orgasm behavior is not selected for visible talk because a stronger orgasm happened in the same body part batch
- **THEN** effects configured for the lower-strength behavior still execute
- **AND** status changes are accumulated into the same settlement change data as the visible representative orgasm

#### Scenario: Plural orgasm effects are applied
- **WHEN** a batch contains orgasms from at least two body parts
- **THEN** the system applies the matching `plural_orgasm_N` effects
- **AND** the system updates the plural orgasm body-part set used by existing plural-orgasm premises

### Requirement: Aggregate human-power display without changing generation
The system SHALL keep existing human-power generation settlement calls and values while displaying only one generated-power prompt for a multi-orgasm batch.

#### Scenario: Multiple human-power calls occur in one multi-orgasm batch
- **WHEN** part orgasm effects and the plural orgasm path each call `store_power_by_human_power()` during one multi-orgasm batch
- **THEN** each original generation call still executes
- **AND** individual generated-power prompts are suppressed during the batch
- **AND** one prompt is displayed after aggregation

#### Scenario: Aggregated prompt uses original plural text
- **WHEN** the batch displays the aggregated generated-power prompt
- **THEN** the prompt uses the original plural-orgasm generated-power text format
- **AND** only the generated-power number is replaced with the batch total

### Requirement: Finish orgasm batch before H exhaustion interruption
The system SHALL complete all orgasm batch effects while the character is still considered in H before processing HP or fatigue based H interruption.

#### Scenario: Orgasm effects reduce HP to exhaustion during H
- **WHEN** an orgasm batch causes the player or target character HP to reach the exhaustion threshold
- **THEN** all effects in that orgasm batch are settled before H reset or H end behavior runs
- **AND** any orgasm count, experience, mark, max HP/MP growth, and H-scoped statistics from the batch are counted as H-internal results

#### Scenario: H interruption runs after batch completion
- **WHEN** an orgasm batch has finished and the character is exhausted
- **THEN** the existing H exhaustion interruption behavior may run
- **AND** the interruption uses the final post-batch HP, fatigue, orgasm count, and H-state data

### Requirement: Keep existing data compatibility
The system SHALL continue using existing orgasm behavior IDs and configured second effects.

#### Scenario: Existing CSV data is loaded
- **WHEN** game configuration is rebuilt from CSV
- **THEN** existing behavior IDs such as `c_orgasm_strong`, `plural_orgasm_4`, `extra_orgasm`, `b_orgasm_to_milk`, and `u_orgasm_to_pee` remain valid
- **AND** existing talk files for those behavior IDs remain usable for representative talk selection

### Requirement: Keep local batch implementation runtime-safe
The system SHALL keep the local batch implementation from shadowing runtime helpers that are needed later in the same settlement.

#### Scenario: Achievement flow runs after batch orgasm settlement
- **WHEN** orgasm batch settlement reaches achievement flow after iterating orgasm counts
- **THEN** the translation helper remains callable for translated achievement labels
- **AND** batch settlement does not raise a `TypeError` caused by a loop variable shadowing the translation function

### Requirement: Clear same-batch legacy orgasm queue entries
The system SHALL prevent orgasm second behaviors generated in one batch from remaining queued after the batch has displayed and settled.

#### Scenario: Old orgasm filter list does not include newly generated orgasm behaviors
- **WHEN** orgasm settlement generates new part orgasm behaviors after a previous orgasm filter list has already been captured
- **THEN** the new behaviors are still displayed or settled by the current batch as appropriate
- **AND** none of those same-batch part orgasm behaviors remain queued for a later update

#### Scenario: Plural orgasm is followed by later update
- **WHEN** a multiple-orgasm batch has already displayed its plural orgasm output and representative part outputs
- **THEN** a later second-behavior update does not display a leftover single body-part orgasm from that same batch
