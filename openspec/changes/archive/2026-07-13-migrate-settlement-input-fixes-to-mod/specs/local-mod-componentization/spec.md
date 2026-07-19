## ADDED Requirements

### Requirement: Maintained local fixes leave upstream files clean
Maintained local bug fixes SHALL be implemented through independently loadable mod components and SHALL NOT require uncommitted edits to upstream game source or browser assets on the active development branch.

#### Scenario: Fix is representable by the mod loader
- **WHEN** a local bug fix can be implemented through a function or method patch
- **THEN** the implementation, tests, and maintenance documentation live under the owning mod component

#### Scenario: Fix is not representable by the mod loader
- **WHEN** a candidate fix requires an unsupported upstream or browser-asset change
- **THEN** it is documented as not migrated or prepared separately for upstream review
- **AND** it is not silently retained as a dirty core-file edit
