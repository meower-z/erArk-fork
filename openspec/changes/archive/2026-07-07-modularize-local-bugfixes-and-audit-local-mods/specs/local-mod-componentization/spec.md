## ADDED Requirements

### Requirement: Split bugfixes by audited root cause
The local mod system SHALL replace the monolithic `local_bugfix` active implementation with smaller bugfix mod components whose boundaries are selected after root-cause audit.

#### Scenario: Component boundary is selected
- **WHEN** an old `local_bugfix` behavior is considered for extraction
- **THEN** its component assignment SHALL be justified by root cause, upstream patch point, affected invariant, and test evidence
- **AND** the split SHALL NOT rely only on the historical README symptom heading

#### Scenario: Related symptoms share one root cause
- **WHEN** multiple observed symptoms are traced to the same root cause or must share the same invariant to be correct
- **THEN** they MAY be implemented in the same bugfix component
- **AND** the component documentation SHALL explain the shared root cause and covered symptoms

#### Scenario: Independent roots are unrelated
- **WHEN** two fixes have no logical dependency and no shared root-cause invariant
- **THEN** they SHALL be separate installable components
- **AND** enabling either component alone SHALL NOT require the other component

### Requirement: Preserve the current local baseline by default
The replacement bugfix components SHALL preserve the current default local behavior when all replacement components are enabled.

#### Scenario: Default configuration enables replacement components
- **WHEN** the split bugfix components are the active local bugfix implementation
- **THEN** the default `mod/mod_config.json` SHALL NOT enable the monolithic `local_bugfix`
- **AND** it SHALL enable all replacement bugfix components needed to match the previous enabled local baseline

#### Scenario: Deprecated backup remains available
- **WHEN** the old monolithic implementation is retired
- **THEN** it SHALL be moved under a deprecated backup location
- **AND** it SHALL NOT remain active in default `enabled_mods` or `load_order`
- **AND** the backup location SHALL NOT be discovered by the mod loader's top-level scan

### Requirement: Verify each component in isolation
Each split bugfix component SHALL pass verification with only itself and its declared dependencies enabled.

#### Scenario: Unit tests run for one component
- **WHEN** a split bugfix component has been extracted
- **THEN** it SHALL have unit tests that reproduce the root-cause invariant before relying on implementation behavior
- **AND** those tests SHALL run without importing unrelated split bugfix components

#### Scenario: Real-loader smoke runs for one component
- **WHEN** a split bugfix component is tested through the mod loader
- **THEN** the test setup SHALL enable only that component and its declared dependencies
- **AND** loading SHALL succeed without hidden dependency on disabled local mods

#### Scenario: BDD verification is recorded
- **WHEN** a split bugfix component is considered complete
- **THEN** at least one real-game or near-real-game BDD scenario SHALL be documented for the component
- **AND** the scenario SHALL state setup, action, expected visible or state outcome, and whether it is automated or manual
- **AND** a near-real-game harness SHALL load the component through the real mod loader against unmocked game modules and real configuration data
- **AND** manual scenarios SHALL record execution evidence instead of only a checklist entry

### Requirement: Enforce declared component dependencies
The mod system SHALL make declared dependencies reliable for split local components.

#### Scenario: Dependency is required
- **WHEN** a component declares another mod in `dependencies`
- **THEN** the required dependency SHALL be enabled and loaded before the dependent component
- **AND** verification SHALL fail if the dependency is missing or ordered after the dependent component

#### Scenario: Dependency is absent
- **WHEN** an enabled component depends on a disabled or missing mod
- **THEN** the loader or verification harness SHALL produce a clear diagnostic identifying the component and missing dependency
- **AND** the dependent component SHALL NOT silently run with partial behavior

#### Scenario: Components are independent
- **WHEN** a component has no declared dependencies
- **THEN** it SHALL load in isolation after core game modules are available
- **AND** it SHALL NOT read functions, globals, or test helpers from unrelated local mod directories

#### Scenario: Unrelated mods keep their configured order
- **WHEN** enabled mods have no declared dependency relationship with each other
- **THEN** dependency-aware ordering SHALL NOT reorder them relative to the configured `load_order`

### Requirement: Document each maintained local mod
Every maintained local mod SHALL have documentation that supports future maintenance and testing.

#### Scenario: Split bugfix documentation exists
- **WHEN** a new bugfix component is created
- **THEN** it SHALL include documentation describing the bug symptom, root cause, affected patch points, fix invariant, tests, BDD scenario, dependencies, and known limitations

#### Scenario: Existing maintained mod is audited
- **WHEN** `group_sex_extension` or `local_performance` is audited
- **THEN** its documentation or verification notes SHALL identify the behavior being protected
- **AND** it SHALL list the tests or BDD scenarios that guard against regressions
