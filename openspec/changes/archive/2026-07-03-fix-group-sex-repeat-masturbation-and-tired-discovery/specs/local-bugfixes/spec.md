## ADDED Requirements

### Requirement: Limit group-mode automatic masturbation to one routing per player action
The local bugfix layer SHALL prevent the same group-mode NPC from being routed to automatic masturbation more than once during one player action settlement pass.

#### Scenario: Same NPC returns to idle during the same player action
- **WHEN** group mode is active and an H-state NPC with `sp_flag.masturebate = 3` has already been routed to `default91` during the current player action settlement pass
- **THEN** a later target-selection pass for the same NPC in the same player action SHALL NOT execute `default91` again
- **AND** the duplicate masturbation marker SHALL be cleared so it cannot leak into a later player action
- **AND** the NPC SHALL be marked complete for that NPC catch-up pass

#### Scenario: NPC receives masturbation marker in a later player action
- **WHEN** a new player action settlement pass begins and group AI again sets the same NPC to `sp_flag.masturebate = 3`
- **THEN** the local bugfix layer SHALL allow that NPC to be routed to `default91` again
- **AND** automatic masturbation SHALL NOT be permanently disabled for that NPC

#### Scenario: Automatic masturbation target is unavailable
- **WHEN** group mode is active, an H-state NPC has `sp_flag.masturebate = 3`, and `default91` cannot be selected
- **THEN** the local bugfix layer SHALL mark the NPC complete for the current NPC catch-up pass
- **AND** the unavailable masturbation marker SHALL be cleared
- **AND** no duplicate settlement output SHALL be produced from that failed routing

#### Scenario: Stale marker is absent when group AI does not choose masturbation again
- **WHEN** a duplicate group-mode masturbation marker was suppressed and cleared in one player action
- **AND** a later player action begins without group AI setting `sp_flag.masturebate = 3` again
- **THEN** the local bugfix layer SHALL fall back to upstream target selection
- **AND** it SHALL NOT route the NPC to `default91` because of a stale marker

### Requirement: Auto-leave tired discoverers during group sex
The local bugfix layer SHALL avoid showing the group-sex discovery choice panel to characters who are too exhausted to join or negotiate the current group sex.

#### Scenario: Tired former participant discovers ongoing group sex
- **WHEN** group sex remains active after a participant exits because of low hit points, tired flag, or tired level at least two
- **AND** that character would trigger the H discovery panel for the same ongoing group sex
- **THEN** the local bugfix layer SHALL skip the discovery choice buttons
- **AND** the character SHALL receive the existing `SEE_H_AND_LEAVE` behavior

#### Scenario: New tired character discovers ongoing group sex
- **WHEN** a character who is not currently participating in the group sex discovers it while having low hit points, tired flag, or tired level at least two
- **THEN** the local bugfix layer SHALL skip the invitation UI
- **AND** the character SHALL receive the existing `SEE_H_AND_LEAVE` behavior instead of being inviteable into an immediate tired-exit loop

#### Scenario: Non-tired character discovers ongoing group sex
- **WHEN** group sex is active and a non-tired character triggers the H discovery panel
- **THEN** the original discovery panel behavior SHALL remain available
- **AND** existing options such as inviting the character to join group sex SHALL keep their original judgement flow

#### Scenario: Auto-leave preserves discovery side effects
- **WHEN** a tired discoverer is auto-routed to `SEE_H_AND_LEAVE`
- **THEN** the local bugfix layer SHALL preserve the original discovery setup side effects, including recording the interrupting character name, targeting the player, and setting the see-H flag
- **AND** the active panel SHALL return to the in-scene panel state
