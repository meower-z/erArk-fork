## REMOVED Requirements

### Requirement: Auto-leave tired discoverers during group sex
**Reason**: This requirement mixes discoverer narration, invitation eligibility, and current-participant exit behavior in a discovery-specific local wrapper. Discovery settlement now has a separate owner, while new admission needs one shared eligibility contract.

**Migration**: Use the new `Gate new group-sex admission by eligibility` requirement for issuing and confirming invitations. The local auto-leave behavior is intentionally removed from the active contract until a separate normal-player reproduction proves which tired-witness response is missing. Current-participant tired exit remains frozen under the group scheduler/exit record named in `refactor-remaining-local-bugfixes-by-root-cause/program-task-map.md`; this admission change does not decide it.

## ADDED Requirements

### Requirement: Gate new group-sex admission by eligibility
The group-sex admission layer SHALL use one shared character predicate before issuing or confirming a new invitation.

The thresholds and cancellation-only rule below are provisional gameplay semantics selected by Fable for local implementation. They require user confirmation before an upstream PR.

#### Scenario: Exhausted character is considered for a new invitation
- **WHEN** a character has hit points at or below 1, an active tired flag, or tired level at least 2
- **AND** a discovery, invitation-list, direct-invite, or group-start path considers that character for new admission
- **THEN** the character is not offered or confirmed as a new participant
- **AND** no caller substitutes its own fatigue threshold

#### Scenario: Eligible character is considered
- **WHEN** a character does not meet any group-sex ineligibility condition
- **THEN** existing execution-value, normal-state, location, and group-sex checks continue unchanged
- **AND** the new predicate does not itself admit the character

#### Scenario: Existing invitation becomes ineligible
- **WHEN** an already invited character becomes exhausted or seriously fatigued before confirmation
- **THEN** the character remains reachable only through the cancellation control
- **AND** the invitation cannot be confirmed into participation

#### Scenario: Player cancels an ineligible existing invitation
- **WHEN** the player cancels an invitation for a now-ineligible character
- **THEN** the existing invitation flag, waiting behavior, and cancellation feedback are cleared through the normal cancellation path
- **AND** no new admission is attempted

### Requirement: Keep admission separate from discovery settlement and current-participant exit
The admission fix SHALL NOT change the ownership of discoverer-reaction settlement or decide how an already participating tired character exits group mode.

#### Scenario: Discovery panel settles a reaction
- **WHEN** a discovery response assigns an explicit discoverer behavior
- **THEN** the separate panel-owned discovery-settlement contract remains responsible for settling it exactly once
- **AND** admission eligibility only decides whether a new participant may be invited or confirmed

#### Scenario: Current participant becomes tired
- **WHEN** a character already participating in group sex becomes tired or exhausted
- **THEN** this admission contract does not choose an exit transition, scheduler priority, or pending-edge policy
