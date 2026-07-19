# local-bugfixes Specification

## Purpose
Define the behavior contract for the split local bugfix components under `mod/`: the invariants each retained fix protects (group-mode AI, movement interruption, masturbation routing, tired discovery, pain-as-pleasure, hypnosis persistence, group edge release), and the audit/test standards that keep the fixes root-cause-justified.
## Requirements
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

#### Scenario: Group-H NPC without masturbation marker still settles idle H effects
- **WHEN** group mode is active and an H-state NPC does not have `sp_flag.masturebate = 3` after group AI runs
- **THEN** the local bugfix layer SHALL leave the NPC in the idle H target-selection path that marks H-state NPCs complete without assigning ordinary AI
- **AND** the NPC SHALL still reach normal status settlement for second-stage effects such as body item or toy effects

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
The local bugfix layer SHALL keep the `pain_as_pleasure` effect scoped to active hypnosis states, SHALL apply it consistently to positive direct pain increases only, and SHALL treat the granted flag as a permanent, hypnosis-gated grant.

#### Scenario: Hypnosis is cancelled
- **WHEN** hypnosis cancellation settles for a character whose target has `pain_as_pleasure`
- **THEN** the target's `pain_as_pleasure` flag is cleared

#### Scenario: Granted flag stays dormant outside hypnosis
- **WHEN** a character carries `pain_as_pleasure` while not in a hypnosis unconscious state (`unconscious_h` not in `{4,5,6,7}`)
- **THEN** positive pain settles as ordinary pain with the conversion suppressed for that settlement
- **AND** the flag itself is preserved rather than cleared, so it reactivates in the character's next hypnosis state
- **AND** only explicit hypnosis cancellation (or the upstream full hypnosis-flag reset) removes the flag

#### Scenario: Pain decreases while pain-as-pleasure is active
- **WHEN** a pain state settlement has a non-positive final pain change
- **THEN** the pain-as-pleasure flag is temporarily disabled for that upstream settlement
- **AND** the flag is restored afterward

#### Scenario: Direct second effect adds pain
- **WHEN** a direct second effect would add small, middle, large, or extra-orgasm pain while `pain_as_pleasure` is active
- **THEN** the positive pain amount is settled as psychological pleasure instead of direct pain

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

### Requirement: Decompose local bugfix behavior into independent components
The local bugfix capability SHALL be delivered by split bugfix components instead of one active monolithic `local_bugfix` mod.

#### Scenario: Component ownership is traceable
- **WHEN** a retained local bugfix behavior is inspected
- **THEN** exactly one split component SHALL own that behavior or provide it to dependents as a declared dependency
- **AND** the owning component's documentation SHALL identify the upstream patch points and covered scenarios

#### Scenario: Component behavior remains equivalent
- **WHEN** all replacement local bugfix components are enabled together
- **THEN** the externally visible bugfix behavior SHALL match the previous enabled `local_bugfix` bundle for all retained fixes, as pinned by the migrated regression tests
- **AND** existing passing regression tests SHALL either remain passing or be migrated to the responsible component test suite

#### Scenario: Component is disabled
- **WHEN** a split bugfix component is disabled while unrelated split components remain enabled
- **THEN** unrelated bugfix components SHALL continue to load and function
- **AND** the disabled component's behavior SHALL be absent unless another declared dependency intentionally provides it

### Requirement: Justify retained fixes by root-cause evidence
The local bugfix capability SHALL justify each retained fix with verified root-cause evidence rather than historical symptom reports alone.

#### Scenario: Existing fix only addresses a surface symptom
- **WHEN** analysis finds that an existing local fix prevents one observed symptom but leaves related states or flows broken
- **THEN** the responsible component SHALL expand its root-cause fix and tests to cover the related scenario
- **AND** the component documentation SHALL record the broader root cause

#### Scenario: Historical bug cannot be reproduced
- **WHEN** an old bug observation or playtest note cannot be reproduced on the current codebase
- **THEN** the component documentation SHALL record the attempted reproduction and current evidence
- **AND** any retained guard SHALL be justified by a still-valid invariant or removed from active behavior

#### Scenario: Multiple patches share one invariant
- **WHEN** several local bugfix patches all protect the same invariant, such as movement interruption, group participant cleanup, hypnosis state persistence, or settlement queue safety
- **THEN** they SHALL be evaluated as one candidate component before deciding whether to split further

### Requirement: Preserve hypnosis persistence and talk safety
The split local bugfix components SHALL preserve the existing hypnosis mode persistence and hypnosis-state talk safety fixes that are already part of `local_bugfix`.

#### Scenario: Normal hypnosis mind-control state persists
- **WHEN** a normal-scene hypnosis flow selects mind-control mode and then exits later mind-control submenus
- **THEN** the target's high-level hypnosis unconscious state SHALL remain the selected mind-control state
- **AND** exiting a mind-control submenu SHALL NOT leave the target in an unset or stale hypnosis state
- **AND** later scene status and valid actions SHALL observe the same mode

#### Scenario: H-mode hypnosis mind-control state persists
- **WHEN** an H-mode hypnosis flow selects `切换催眠模式` and then `心控`
- **THEN** the target's selected mind-control state SHALL survive second-level or third-level submenu exits
- **AND** submenu exits SHALL NOT leave the target in an unset or stale hypnosis state
- **AND** H-mode actions that require the selected hypnosis state SHALL observe the same mode

#### Scenario: Hypnosis-state talk bypass remains scoped
- **WHEN** talk matching the current action is checked for a target under hypnosis unconscious flags
- **THEN** the hypnosis-specific unconscious gate bypass SHALL allow valid hypnosis-state talk
- **AND** ordinary unconscious states SHALL keep their existing blocking behavior

### Requirement: Keep split local bugfix tests isolated from feature mods
The local bugfix test suite SHALL verify split components without relying on `group_sex_extension`, `local_performance`, or other feature mods unless declared as dependencies.

#### Scenario: Component unit test runs
- **WHEN** a split local bugfix unit test is executed
- **THEN** it SHALL load only the component script or a declared dependency under test
- **AND** fake modules or fixtures SHALL model upstream game behavior rather than importing unrelated mod code

#### Scenario: Full local regression suite runs
- **WHEN** all replacement bugfix components are enabled together
- **THEN** the migrated local bugfix regression suite SHALL pass
- **AND** it SHALL include coverage for group-mode target preservation, movement interruption, automatic masturbation routing, tired discovery auto-leave, pain-as-pleasure consistency, hypnosis persistence, and group edge release

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
