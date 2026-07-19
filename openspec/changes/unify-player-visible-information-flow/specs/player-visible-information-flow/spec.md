## ADDED Requirements

### Requirement: Explicit resume gate
The change SHALL remain documentation-only until the user explicitly resumes it. Phase 0 evidence work, implementation, tests, OpenSpec apply, PR preparation, and maintainer submission MUST NOT begin while the change is deferred.

#### Scenario: Change remains deferred
- **WHEN** no later user decision explicitly resumes the change
- **THEN** the repository behavior remains unchanged and no implementation task is executed

#### Scenario: User resumes the change
- **WHEN** the user explicitly decides that the expected benefit justifies renewed work
- **THEN** the team first refreshes source evidence and requests direction approval before any live cutover

### Requirement: Typed player-visible information facts
The system SHALL accept time-ordered player-visible information through one producer interface using a closed set of Talk, Narration, Notice, EventText, and StatusChange facts.

#### Scenario: Domain producer reports an occurrence
- **WHEN** a talk, narration, explicit notice, event body, or visible status change occurs
- **THEN** the producer submits a semantic fact without selecting a Tk or Web sink

#### Scenario: Snapshot UI content is produced
- **WHEN** a panel, layout, button, input prompt, map, or other rebuildable UI snapshot is produced
- **THEN** that content remains outside the player-visible information fact interface

### Requirement: Monotonic in-process ordering and single dispatch
The system SHALL assign a monotonic in-process sequence after a fact passes validation and SHALL synchronously invoke only the active renderer adapter once for that accepted fact.

#### Scenario: Game time moves backward
- **WHEN** time-stop behavior rolls back the game clock after a fact was accepted
- **THEN** the fact keeps its assigned order and is not withdrawn or re-emitted

#### Scenario: Web mode is active
- **WHEN** an accepted fact is published in Web mode
- **THEN** the system invokes the Web adapter and does not also invoke the Tk adapter

#### Scenario: Adapter writes multiple legacy sinks
- **WHEN** an adapter projects one fact to more than one existing sink
- **THEN** the sequence constrains the adapter call but does not claim transactional sink writes or browser exactly-once delivery

### Requirement: Immutable status occurrence context
The system MUST freeze every StatusChange input and the visibility context needed to render it before publication.

#### Scenario: Mutable settlement objects change later
- **WHEN** a producer mutates the original CharacterStatusChange, target, draw settings, or character data after publication
- **THEN** the accepted fact retains the subject, target, name, style, visibility, perspective, and delta values captured for that occurrence

### Requirement: Renderer-neutral core boundary
The core fact model MUST NOT contain Web payload keys, Socket event names, HTML/CSS, Tk JSON, draw classes, button or panel identifiers, wait state, clear policy, reconnect policy, or mod metadata.

#### Scenario: Web projection is required
- **WHEN** a Web fact must enter an existing history, dialog, modal, or value-change sink
- **THEN** only the Web compatibility adapter maps the renderer-neutral fact to that sink representation

#### Scenario: Input is required after information
- **WHEN** the existing flow must wait for a command or continue action after displaying a fact
- **THEN** the existing UI/flow owner performs the wait and the information module does not own or advance input state

### Requirement: Preserve current Tk behavior
The Tk adapter SHALL preserve the current text, style, line breaks, pagination, draw enqueue order, and wait adjacency for every migrated producer.

Web payload compatibility MUST NOT impose Web fields, Socket semantics, flush or clear ownership, or any other additional constraint on the Tk adapter beyond preserving the established Tk behavior.

#### Scenario: Tk producer projection is migrated
- **WHEN** a producer/sink cell changes from LEGACY to CUTOVER in Tk mode
- **THEN** captured Tk output and the adjacent wait sequence match the approved pre-migration baseline

#### Scenario: Web payload remains frozen
- **WHEN** the Web adapter must retain a legacy payload or Socket behavior
- **THEN** the Tk adapter contract remains unchanged and does not acquire that Web-specific representation or lifecycle

### Requirement: Preserve current Web behavior
The Web adapter SHALL preserve existing payload fields, array order, Socket events, send and clear timing, dialog/history behavior, status-float loss rules, reconnect behavior, and client-side duplicate suppression for every migrated producer.

#### Scenario: Status value change is projected
- **WHEN** a StatusChange reaches the current Web status panel path
- **THEN** per-character reads, the 2-second visible filter, the 5-second cleanup, and target-switch timestamp refresh retain their baseline behavior

#### Scenario: Client reconnects
- **WHEN** the Web client reconnects after information was already destructively consumed
- **THEN** the system retains the current best-effort behavior without adding ack, cursor, or reliable replay guarantees

#### Scenario: Duplicate text reaches browser history
- **WHEN** existing client logic suppresses a repeated type-and-text entry
- **THEN** migration parity treats that suppression as baseline behavior rather than silently fixing it

### Requirement: Per-producer per-sink migration ownership
Migration SHALL assign each `(producer, legacy sink)` cell exactly one writer in LEGACY, SHADOW, or CUTOVER state.

#### Scenario: Cell is in SHADOW
- **WHEN** a candidate projection is compared with legacy output
- **THEN** legacy remains the only player-visible writer and the recording path does not read or clear any destructive legacy buffer

#### Scenario: Cell is switched to CUTOVER
- **WHEN** the prior buffer has completed its existing flush and clear, no producer or adapter call is in flight, and the next fact has not started
- **THEN** only future facts use the new writer and the old path suppresses only that cell

#### Scenario: Cell is rolled back
- **WHEN** a CUTOVER cell returns to LEGACY at the next quiet point
- **THEN** only future facts return to the legacy writer and no prior fact is replayed or backfilled

### Requirement: Evidence gate before live cutover
The team MUST NOT perform a live cutover until Phase 0 has produced reproducible Tk/Web traces, a closed producer/sink/clear/Socket inventory, field/event payload captures, written normalization rules, and an explicit settlement-modal description dependency decision.

#### Scenario: Runtime ordering remains unexplained
- **WHEN** a Tk/Web difference, destructive read, direct-write producer, or Socket-only path is missing from the baseline evidence
- **THEN** live cutover remains blocked

#### Scenario: Phase 0 closes all blockers
- **WHEN** the evidence is reproducible and every observed difference has an approved explanation
- **THEN** the team requests a separate live-cutover approval rather than treating direction approval as implementation authorization

### Requirement: Parent event compatibility path
The Web adapter SHALL map an option-bearing parent EventText fact to the existing pending-event representation while the existing event-option flow remains the sole delayed consumer.

#### Scenario: Parent event has options
- **WHEN** a parent event body is followed by selectable child events
- **THEN** the adapter records the pending event text and the existing option flow continues to write the body and option labels to history and realtime output and to own modal input

### Requirement: No mod compatibility contract
Validation for this change SHALL use clean upstream behavior with mods disabled and SHALL NOT require a compatibility shim, legacy patch point, deprecation window, registry, or mod smoke gate.

#### Scenario: Existing mod patches an old display function
- **WHEN** future implementation removes or bypasses that legacy patch point
- **THEN** the change is not rejected for mod incompatibility provided clean-upstream behavior satisfies this specification
