## ADDED Requirements

### Requirement: Release group-mode edge orgasms before end reset
The local bugfix layer SHALL release pending edge orgasms before full group-sex end resets H state or before a scoped group-sex exit can carry pending edge state into later settlement.

#### Scenario: Normal group sex ends with pending edge counts
- **WHEN** group mode is active and group sex ends while one or more group participants have `h_state.orgasm_edge == 1` with non-zero `orgasm_edge_count`
- **THEN** every pending edge count is converted into ordinary orgasm settlement before H state reset runs
- **AND** the participant's pending edge counters are cleared

#### Scenario: Group end summary includes released edge orgasms
- **WHEN** pending edge counts are released during group-sex end
- **THEN** the generated second-stage orgasm effects are synchronously executed before the original group-sex end HP/MP max summary reads `h_state.orgasm_count`
- **AND** the group-sex end HP/MP max summary includes the released orgasm counts
- **AND** the release happens before the group end H-state reset effect clears `h_state`

#### Scenario: Player HP zero interrupts group sex with pending edge counts
- **WHEN** group mode ends through the player-HP-zero group-sex interruption path while participants have pending edge counts
- **THEN** the same pre-reset edge release behavior is applied before group H state is reset

#### Scenario: Discovered interrupt ends group sex with pending edge counts
- **WHEN** a discovered-interrupt path sets `GROUP_SEX_END` and calls group-sex end handling while participants have pending edge counts
- **THEN** the same full group-sex pre-reset edge release behavior is applied through the group-end effect wrapper

#### Scenario: Group sex reduces to one remaining participant
- **WHEN** the game assigns `group_sex_to_h` because only one NPC remains
- **THEN** the local bugfix layer does not rely on the global `9999` no-op effect to run cleanup
- **AND** it derives participants that have just left the group context from the pre-transition group participant set, excluding the continuing target
- **AND** it releases pending edge counts only for those leaving participants
- **AND** it leaves the continuing target unchanged so existing game behavior controls the subsequent one-target interaction

#### Scenario: Single NPC exits group sex
- **WHEN** one NPC exits through `group_sex_npc_hp_0_end` while other participants remain in group sex
- **THEN** any pending edge release is scoped only to the exiting NPC before the original `END_H_ADD_HPMP_MAX` (`528`) and `SELF_H_STATE_RESET` (`403`) path
- **AND** the exiting NPC's own HP/MP max settlement includes the released orgasm counts
- **AND** the local bugfix layer does not release pending edge counts for unrelated participants who remain in group sex
- **AND** the cleanup is not implemented by globally wrapping shared effect `DESIRE_POINT_TO_0` (`1503`)

#### Scenario: Unconscious recovery directly shuts down group sex
- **WHEN** `recover_from_unconscious_h()` handles unconscious H recovery while group sex mode is active
- **THEN** the local bugfix layer captures the pre-recovery group participant set
- **AND** it releases pending edge counts for participants leaving the group context before group templates are cleared
- **AND** it releases pending edge counts before group mode is turned off
- **AND** it preserves the existing recovery flow for any continuing interaction with the recovered target

#### Scenario: Pending edge release clears all edge state
- **WHEN** a group-mode participant's pending edge counts are released by the local bugfix layer
- **THEN** the participant's `orgasm_edge_count` is cleared
- **AND** the participant's `h_state.orgasm_edge` is reset so no pending or release state can be settled later during sleep

#### Scenario: Participant filtering prevents accidental release
- **WHEN** group-mode cleanup evaluates scene characters and group template participants
- **THEN** it follows the participant-discovery semantics used by the group-sex extension
- **AND** it only releases existing NPC/operator participants that are in H state or are present in the group context, have `h_state.orgasm_edge == 1`, and have non-zero pending edge counts
- **AND** it leaves all other characters unchanged

#### Scenario: Template-only participant cleanup does not promise summary inclusion
- **WHEN** a pending-edge participant exists only in stale group-template context and is not a current-scene participant read by the original group-end HP/MP max summary
- **THEN** the local bugfix layer may release or clear that participant's pending edge state to prevent later sleep settlement leakage
- **AND** it does not require the original group-end HP/MP max summary to include that off-scene participant

#### Scenario: Group sex ends without pending edge counts
- **WHEN** group sex ends and no group participant has pending edge counts
- **THEN** the local bugfix layer leaves the existing group-sex end behavior unchanged

#### Scenario: Release flush is scoped to release-generated second effects
- **WHEN** the local bugfix layer releases pending edge counts without relying on the local H orgasm batch immediate flush
- **THEN** it executes only the second-stage orgasm effects generated by that release before continuing
- **AND** it does not run a broad second-effect pass that applies unrelated queued item, insert, mark, or orgasm-judge effects

#### Scenario: Batch immediate flush is not applied twice
- **WHEN** the local H orgasm batch replacement already synchronously flushes the second-stage orgasm effects generated by a pending edge release
- **THEN** the local bugfix layer does not reapply those same release-generated second effects
- **AND** the participant's orgasm counts reflect exactly one release settlement for the pending edge counts
- **AND** the local bugfix layer detects batch availability at release time after mod replacements are installed
