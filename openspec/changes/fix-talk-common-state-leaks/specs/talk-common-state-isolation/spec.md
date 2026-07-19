## ADDED Requirements

### Requirement: Temporary talk target is scoped to one expansion
The common-talk renderer SHALL allow NPC-triggered paper-doll premise evaluation to use that NPC as the player's temporary target, and SHALL restore the player's previous target after the expansion finishes or raises an exception.

#### Scenario: NPC common talk expands successfully
- **WHEN** an NPC-triggered common-talk placeholder requires the player target to be that NPC during premise evaluation
- **THEN** the placeholder is evaluated with that temporary target
- **AND** the player's previous target is restored before control returns to the caller

#### Scenario: NPC common talk expansion fails
- **WHEN** common-talk premise evaluation or replacement raises after the temporary target is installed
- **THEN** the player's previous target is restored before the exception leaves the expansion boundary

#### Scenario: Player-triggered common talk expands
- **WHEN** the player triggers common talk without requiring an NPC target override
- **THEN** the renderer does not change the player's target

### Requirement: Talk expansion does not mutate common-talk configuration
The common-talk renderer SHALL construct per-call candidate collections without modifying lists or dictionaries stored in the global common-talk configuration.

#### Scenario: Short body-part candidates include common alternatives
- **WHEN** a short body-part placeholder combines its configured A candidates with common short-form A candidates
- **THEN** the combined per-call candidates include both sources
- **AND** neither source list in global configuration changes

#### Scenario: The same placeholder is expanded repeatedly
- **WHEN** the same common-talk placeholder is expanded multiple times
- **THEN** the global candidate collections and their multiplicities remain identical to their pre-call state
- **AND** later selection weights do not depend on how many earlier renders occurred
