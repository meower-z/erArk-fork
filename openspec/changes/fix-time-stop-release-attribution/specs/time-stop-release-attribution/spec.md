## ADDED Requirements

### Requirement: Attribute effect 527's direct release changes to each NPC
When an NPC has any positive deferred count, the system SHALL record the changes written directly by effect 527's release settlement in `root_change.target_change[npc_id]`. Effect 527 SHALL NOT consume or replace the later generic second-stage pass; that pass keeps its existing behavior.

#### Scenario: One NPC releases several body-part orgasms
- **WHEN** `TIME_STOP_OFF` releases nonzero deferred orgasm counts for one NPC
- **THEN** changes written directly by effect 527's release-settlement calls are stored under `target_change[npc_id]`
- **AND** the player's root maps do not receive those NPC changes
- **AND** the experience recorded there matches the experience actually stored on that NPC

#### Scenario: Several NPCs release in one action
- **WHEN** two or more NPCs have deferred counts
- **THEN** each NPC receives a distinct target-owned change block
- **AND** no effect-527-direct changes are merged into another NPC or the player

#### Scenario: Renderer adapters collect effect 527's direct records
- **WHEN** Tk displays or Web collects effect 527's direct target-owned records
- **THEN** those direct values remain associated with the released NPC's character ID
- **AND** those target-owned direct values are not dropped or reclassified as player-root changes
- **AND** Web verification may be an automated collection-layer assertion rather than separate player-visible evidence

### Requirement: Preserve the release lifecycle
The system SHALL change settlement ownership without changing the deferred release lifecycle or dropping unrelated work.

#### Scenario: Effect 527 encounters unrelated queued second behaviors
- **WHEN** effect 527 releases an NPC that already has unrelated queued second behaviors
- **THEN** effect 527 does not consume, remove, or overwrite those queued behaviors
- **AND** this scenario makes no claim about how the later generic pass settles them

#### Scenario: NPC has no deferred count
- **WHEN** an NPC has no nonzero deferred orgasm count at time resume
- **THEN** the original `time_stop_release` marker and no-op orgasm-settlement call are preserved
- **AND** effect 527 does not itself create a target-owned change block solely for that empty call
- **AND** the later generic pass may still create an empty target entry under its existing logic, outside this scenario's assertion boundary
- **AND** counter clearing and unconscious-state recovery cleanup still run

#### Scenario: Remote NPC has deferred state
- **WHEN** a registered NPC outside the player's current scene has deferred release state
- **THEN** effect 527's direct release changes use that NPC's target-owned block
- **AND** counter clearing and unconscious-state recovery cleanup still run
- **AND** the existing remote silent second-stage path through `must_settle_check()` is unchanged and outside this change's scope
