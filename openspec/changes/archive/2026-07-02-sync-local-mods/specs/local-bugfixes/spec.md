## ADDED Requirements

### Requirement: Preserve player target during group-mode AI auto-fill
The local bugfix layer SHALL preserve the player's existing `target_character_id` whenever group-mode AI temporarily evaluates candidate NPC targets.

#### Scenario: Auto-fill mutates the player target
- **WHEN** group-mode AI auto-fill temporarily assigns a candidate NPC to the player target
- **THEN** the local wrapper restores the original player target before returning
- **AND** the original target is restored even if the upstream AI function raises

### Requirement: Stop group-mode H-state NPC movement
The local bugfix layer SHALL stop ordinary movement for NPCs that are in H state while group mode is active.

#### Scenario: Group-mode participant enters ordinary movement
- **WHEN** an H-state NPC in group mode attempts to start or continue movement
- **THEN** the NPC is returned to wait state
- **AND** movement source, target, and final target are cleared

### Requirement: Route group-mode masturbation markers to formal action settlement
The local bugfix layer SHALL route group-mode NPCs with the masturbation marker to the formal target/action path that consumes that marker.

#### Scenario: NPC receives masturbation marker in group mode
- **WHEN** a group-mode H-state NPC has `sp_flag.masturebate = 3`
- **THEN** target selection searches for the `default91` target
- **AND** the NPC either executes that target or is marked complete when it is unavailable

### Requirement: Clear player movement on H/group-mode interruption
The local bugfix layer SHALL clear player movement state when H state or group mode interrupts player movement.

#### Scenario: Player is interrupted while moving
- **WHEN** the player is moving and `move_stop`, player H state, or group mode becomes active
- **THEN** the movement loop stops
- **AND** `move_target` and `move_final_target` are cleared

### Requirement: Rejudge tired/sleep status for group-mode edge cases
The local bugfix layer SHALL re-run character status judgement after tired/sleep evaluation when a group-mode H/follow NPC crosses tired or sleep thresholds.

#### Scenario: Group-mode NPC reaches tired threshold
- **WHEN** a group-mode H/follow NPC has low hit points, tired flag, or tired level at least two
- **THEN** upstream tired/sleep judgement still runs
- **AND** character status is rejudged afterward

### Requirement: Cancel player movement when NPC active-H starts
The local bugfix layer SHALL remove the player's stale movement final target when an NPC active-H action starts.

#### Scenario: Active-H interrupts pending movement
- **WHEN** NPC active-H selects a valid behavior while the player has a pending movement final target
- **THEN** the player move is marked stopped
- **AND** the final movement target is cleared before the new behavior advances time

### Requirement: Keep pain-as-pleasure scoped and consistent
The local bugfix layer SHALL keep `pain_as_pleasure` scoped to active hypnosis effects and SHALL apply it consistently to positive direct pain increases only.

#### Scenario: Hypnosis is cancelled
- **WHEN** hypnosis cancellation settles for a character whose target has `pain_as_pleasure`
- **THEN** the target's `pain_as_pleasure` flag is cleared

#### Scenario: Pain decreases while pain-as-pleasure is active
- **WHEN** a pain state settlement has a non-positive final pain change
- **THEN** the pain-as-pleasure flag is temporarily disabled for that upstream settlement
- **AND** the flag is restored afterward

#### Scenario: Direct second effect adds pain
- **WHEN** a direct second effect would add small, middle, large, or extra-orgasm pain while `pain_as_pleasure` is active
- **THEN** the positive pain amount is settled as psychological pleasure instead of direct pain
