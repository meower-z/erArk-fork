## RENAMED Requirements

- FROM: `### Requirement: Implement batch settlement as a local bugfix mod`
- TO: `### Requirement: Implement batch settlement as a local bugfix component`

## MODIFIED Requirements

### Requirement: Batch NPC orgasm events during H settlement
The system SHALL treat all NPC orgasm events detected during one orgasm settlement pass as a single batch before executing display and effect settlement.

#### Scenario: One body part reaches multiple orgasm strengths in one batch
- **WHEN** a body part generates multiple orgasm behavior IDs in the same batch, such as `c_orgasm_small`, `c_orgasm_normal`, and `c_orgasm_strong`
- **THEN** the batch records every distinct generated behavior ID for effect settlement
- **AND** the batch selects only the strongest behavior ID for that body part's visible talk

#### Scenario: Repeated same behavior ID occurs in one batch
- **WHEN** the same orgasm behavior ID is generated more than once in the same batch (for example a pending edge release with count N, or several rolls landing on the same strength)
- **THEN** the batch records the occurrence count for that behavior ID
- **AND** that behavior ID's configured effects are settled once per recorded occurrence, so no rolled orgasm loses its attribute settlement
- **AND** visible talk for that body part is still shown only once for the batch

> 2026-07-06 审计裁定：拆分组件的按次数结算是有意加深，与寸止释放动机一致
> （上游 0/1 开关语义会丢失同批次内第 N-1 次绝顶的属性结算）。旧的"settled
> once"场景在此被有意替换；`mod_info.json`/README 的描述已同步改写。

### Requirement: Implement batch settlement as a local bugfix component
The system SHALL implement the H orgasm batch settlement fixes through an enabled split local bugfix component rather than direct edits to core game files or the retired monolithic `local_bugfix` mod.

#### Scenario: Core game files remain untouched
- **WHEN** the H orgasm batch component is installed
- **THEN** the replacement behavior is registered from the component's own mod manifest
- **AND** core files such as `Script/Design/second_behavior.py` and `Script/Design/handle_npc_ai.py` do not need direct edits for this fix

#### Scenario: Component loads without unrelated bugfixes
- **WHEN** the H orgasm batch component is enabled with only its declared dependencies
- **THEN** the component SHALL load successfully through the mod loader
- **AND** H orgasm batch tests SHALL NOT require unrelated split bugfix components to be enabled

### Requirement: Keep local batch implementation runtime-safe
The system SHALL keep the local batch implementation from shadowing runtime helpers that are needed later in the same settlement.

#### Scenario: Achievement flow runs after batch orgasm settlement
- **WHEN** orgasm batch settlement reaches achievement flow after iterating orgasm counts
- **THEN** the translation helper remains callable for translated achievement labels
- **AND** batch settlement does not raise a `TypeError` caused by a loop variable shadowing the translation function

#### Scenario: Playtest log regression is guarded
- **WHEN** local H orgasm batch settlement reaches the achievement flow after multi-part or repeated orgasm settlement
- **THEN** `achievement_panel.achievement_flow(_("绝顶"), 1221)` or its equivalent SHALL execute with `_` still bound to the translation helper
- **AND** the component SHALL NOT raise `TypeError: 'int' object is not callable`
- **AND** the regression test SHALL cover the settlement path that produced the playtest `error.log` traceback

## ADDED Requirements

### Requirement: Expose batch flush state to dependent components
The H orgasm batch component SHALL expose its batch flush state so declared dependent components can coordinate cleanup safely.

#### Scenario: Batch state is visible to dependent cleanup
- **WHEN** another declared component needs to detect whether H orgasm batch settlement is currently flushing effects
- **THEN** the H orgasm batch component SHALL expose a documented function or registered hook for that state
- **AND** the dependent component SHALL declare the dependency instead of importing hidden implementation details

### Requirement: Verify H orgasm batch with isolated and integrated flows
The H orgasm batch component SHALL be verified both alone and with any declared dependent components.

#### Scenario: Isolated batch verification runs
- **WHEN** only the H orgasm batch component and its dependencies are enabled
- **THEN** unit tests SHALL cover same-part display dedupe, same-batch queue clearing, human-power aggregation, remote draw suppression, hypnosis-state second talk, and achievement runtime safety

#### Scenario: Integration with group edge release runs
- **WHEN** the group edge release component declares and uses the H orgasm batch component
- **THEN** integration tests SHALL confirm pending edge release is not double-flushed
- **AND** multi-count edge release SHALL preserve the expected orgasm count and plural effect behavior
