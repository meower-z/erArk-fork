## ADDED Requirements

### Requirement: Explicit Web waits remain real waits
The maintained settlement-input mod SHALL publish an explicit Web `WaitDraw` before blocking, consume one accepted wait response, and prevent the completed wait from re-arming when the next state is rendered.

#### Scenario: Web wait completes once
- **WHEN** an explicit non-empty `WaitDraw` is reached in Web mode without an outer skip owner
- **THEN** its text is published before the server blocks
- **AND** one accepted response releases it
- **AND** the completed element is not left active in the next published state

#### Scenario: Outer skip owner bypasses wait only within its scope
- **WHEN** an explicit wait is reached while map, navigation, or timed-wait skip ownership is active
- **THEN** the text remains displayable without arming a Web wait
- **AND** the owner restores the prior skip state when its operation exits

### Requirement: Event and talk boundaries retain pacing
The maintained settlement-input mod SHALL preserve each direct Web event or talk boundary that upstream represents as a waiting draw.

#### Scenario: Main dialog boundary
- **WHEN** a direct event or talk adds an input-requiring main-dialog entry
- **THEN** settlement does not advance past that boundary until the dialog queue and visible waiting page are acknowledged

#### Scenario: Minor dialog boundary
- **WHEN** a direct event or talk adds a minor-dialog entry corresponding to an upstream waiting draw
- **THEN** the mod introduces one real wait boundary unless an outer skip owner is active

### Requirement: Skip flags have bounded ownership
The maintained settlement-input mod SHALL restore the incoming skip and right-click state after local waits, map movement, navigation movement, timed waits, and waiting text-list panels.

#### Scenario: Fresh local skip is cleaned
- **WHEN** the wrapped operation starts without skip active and creates a skip state
- **THEN** it clears that skip and right-click state on normal return or exception

#### Scenario: Outer skip is preserved
- **WHEN** the wrapped operation starts with skip already active
- **THEN** it leaves ownership and final restoration to the outer operation

### Requirement: Upstream files remain clean
The local settlement-input behavior SHALL be delivered without modifying tracked upstream `Script/`, `static/`, or shared BDD-driver files.

#### Scenario: Mod-only diff
- **WHEN** the migration is complete
- **THEN** implementation changes are confined to the maintained mod, its tests, mod configuration, and documentation
