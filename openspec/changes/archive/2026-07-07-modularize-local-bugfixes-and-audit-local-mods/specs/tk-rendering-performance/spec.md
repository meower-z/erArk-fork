## ADDED Requirements

### Requirement: Keep Tk performance optimization one verifiable maintained mod
The Tk rendering performance optimization SHALL remain a single local mod whose rendering and input-wait behavior is verifiable without split local bugfix components.

#### Scenario: Performance mod is not split
- **WHEN** the performance optimization is packaged and loaded
- **THEN** `local_performance` SHALL remain a single mod containing queue-rendering coalescing and fresh-input wait behavior
- **AND** its tests SHALL treat both patches as one maintained Tk performance and stale-input safety optimization

#### Scenario: Loader smoke verifies replacement targets
- **WHEN** `local_performance` is enabled without split local bugfix components
- **THEN** it SHALL replace the intended Tk normal-mode functions successfully
- **AND** it SHALL NOT require `local_bugfix`, `group_sex_extension`, or any split bugfix component to load

#### Scenario: BDD wait flow is recorded
- **WHEN** the performance mod's wait behavior is verified
- **THEN** a BDD verification scenario SHALL record a real or near-real action flow where a command is followed by settlement output and a wait prompt
- **AND** the expected result SHALL prove one user action cannot accidentally advance both the command and the trailing wait
