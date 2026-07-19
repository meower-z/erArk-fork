## MODIFIED Requirements

### Requirement: Keep pain-as-pleasure scoped and consistent
The local bugfix layer SHALL keep the `pain_as_pleasure` effect scoped to active hypnosis states while treating the granted flag as a permanent, hypnosis-gated grant.

#### Scenario: Granted flag stays dormant outside hypnosis
- **WHEN** a character carries `pain_as_pleasure` while not in a hypnosis unconscious state (`unconscious_h` not in `{4,5,6,7}`)
- **THEN** positive pain settles as ordinary pain with the conversion suppressed for that settlement
- **AND** the flag itself is preserved rather than cleared, so it reactivates in the character's next hypnosis state
- **AND** only explicit hypnosis cancellation (or the upstream full hypnosis-flag reset) removes the flag

## ADDED Requirements

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
