## ADDED Requirements

### Requirement: Honor all-masturbation group AI before template membership
When group-sex NPC AI type 1 (all/only masturbation) is active, the local behavior stack SHALL allow every eligible H-state group participant to generate the temporary group masturbation intent even if that participant is already present in the current group-sex body template.

#### Scenario: Invited participant is already in the template
- **WHEN** an NPC was directly invited into group sex, is now an H-state template participant, and group AI type 1 is active
- **THEN** template membership does not return before the type-1 policy is evaluated
- **AND** the NPC receives `sp_flag.masturebate = 3` for the current player action window

#### Scenario: Intent reaches one formal action
- **WHEN** a template participant receives the type-1 masturbation intent
- **THEN** the existing `local_group_masturbation_intent_fix` routes it through `default91` to a formal `MASTUREBATE` behavior
- **AND** the behavior duration follows the current player action slice
- **AND** the NPC settles that behavior at most once in that player action window

#### Scenario: Non-masturbation AI retains template protection
- **WHEN** group AI type 1 is not active and an NPC is already assigned in the group-sex template
- **THEN** the existing template-member early return remains available
- **AND** this change does not force an unrelated masturbation action

#### Scenario: Window output is delayed but behavior is not missing
- **WHEN** the player waits for several minutes as one atomic player action
- **THEN** the system may present NPC action text at the action-window settlement boundary rather than once per simulated minute
- **AND** window-end state and effect records still prove that each eligible type-1 participant completed one formal masturbation action
