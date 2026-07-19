## ADDED Requirements

### Requirement: Settle every explicit discoverer reaction exactly once
The game SHALL settle an explicit reaction selected in the H-discovery panel exactly once, independent of whether the panel was opened by the NPC behavior loop or by a direct hidden-discovery call.

#### Scenario: NPC behavior dispatch selects an explicit reaction
- **WHEN** the NPC behavior loop opens the discovery panel and the selected response assigns an explicit discoverer behavior
- **THEN** the panel settles that behavior before it returns
- **AND** the outer NPC loop does not replay the settled behavior

#### Scenario: Direct hidden-discovery call selects an explicit reaction
- **WHEN** the panel is opened directly outside the NPC behavior loop and the selected response assigns an explicit discoverer behavior
- **THEN** the panel settles that behavior before it returns
- **AND** settlement does not depend on an outer NPC pass that will not occur

#### Scenario: Initial H converts to group sex
- **WHEN** a discoverer accepts and a single-target H scene converts to group sex
- **THEN** `DISCOVER_OTHER_SEX_AND_JOIN` settles before the nested player group-conversion update
- **AND** the player follow-up cannot erase the pending discoverer reaction

#### Scenario: Discoverer refuses, leaves, ignores, is deceived, or interrupts
- **WHEN** any explicit refusal, leave, ignore, deception, or interruption response is selected
- **THEN** its existing response branch settles the assigned discoverer behavior synchronously without routing through a unified settlement helper
- **AND** it settles no more and no less than once

### Requirement: Record and consume the completed discovery settlement through `SPECIAL_FLAG`
When an explicit reaction settles inside an NPC behavior dispatch, state-machine 40 SHALL record the completed panel operation in a dedicated discoverer `SPECIAL_FLAG` after the panel fully returns. The NPC scheduler SHALL consume and clear that flag without changing the return value of the state-machine dispatch.

#### Scenario: Scheduler consumes a completed flag
- **WHEN** state-machine 40 records a true discovery-settlement flag after the panel returns
- **THEN** it skips the already-settled reaction
- **AND** a real `MOVE` successor keeps the flag false so the original outer settlement processes that movement
- **AND** a no-route fallback to `WAIT` produces a true result so the outer loop does not add a second idle settlement after the visible discovery response

#### Scenario: Direct caller does not create a character flag
- **WHEN** a direct hidden-discovery caller completes a response outside an NPC round
- **THEN** the explicit reaction remains settled
- **AND** no discovery-settlement `SPECIAL_FLAG` is written
- **AND** any resulting `MOVE` stays pending for the discoverer's later normal turn

### Requirement: Keep settlement identity local to one panel operation
The discovery fix SHALL use the panel instance as the operation identity and SHALL NOT use process-global suppression, hidden-session teardown, or encounter-wide witness state to decide whether settlement is complete.

#### Scenario: One valid panel selection settles synchronously
- **WHEN** the panel executes the callback for one valid player selection
- **THEN** that callback settles at most one explicit discoverer reaction
- **AND** state-machine 40 reads the saved public result after the synchronous panel loop exits

#### Scenario: Settlement or player follow-up raises
- **WHEN** discoverer settlement or its later player follow-up raises
- **THEN** the exception propagates through the same synchronous callback
- **AND** no global or cross-operation suppression state survives to affect a later action

#### Scenario: Another eligible witness appears later
- **WHEN** a different eligible character witnesses the same encounter later
- **THEN** this settlement-ownership fix does not suppress that discovery
- **AND** merged PR #206 remains the separate owner of same-witness exclusion before movement
