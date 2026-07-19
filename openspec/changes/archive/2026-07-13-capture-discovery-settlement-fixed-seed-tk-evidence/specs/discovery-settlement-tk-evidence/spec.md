## ADDED Requirements

### Requirement: Fixed-seed A/B parity
The evidence preparation SHALL use the explicit seed `20260712` for both baseline and candidate runtimes, with identical save bytes, Tk configuration, and player inputs.

#### Scenario: Matching deterministic runtimes
- **WHEN** the baseline and candidate runtimes are prepared
- **THEN** their copied save hashes, seed value, seed injection location, renderer configuration, and intended player route are recorded as matching

### Requirement: Visual-only game interaction
The evidence capture MUST be performed by a local visual agent operating the real Tk interface by inspecting a current captured frame, choosing one next action from those pixels, performing only that action locally with `xdotool`, and inspecting a new frame before choosing again. It MUST NOT use prerecorded coordinates, blind or batched input, network desktop relays, debug controls, or direct save-state mutation.

#### Scenario: Valid player operation
- **WHEN** either A/B route is executed
- **THEN** every game choice follows the inspect-one-frame, perform-one-action, inspect-again cycle on an isolated local X display

### Requirement: Comparable discovery frames
The evidence set SHALL contain baseline and candidate trigger frames at the same discovery event and outcome frames at the same completed-draw stopping point.

#### Scenario: Matching trigger
- **WHEN** Leizi discovers the Doctor and Closure during the fixed repeated `[6201]身体爱抚` sequence
- **THEN** both trigger frames identify Leizi, Closure, the hidden-sex scene, and the `[1]用花言巧语支开对方` choice at the same discovery count

#### Scenario: Player-visible outcome difference
- **WHEN** choice `[1]用花言巧语支开对方` completes on both runtimes without another player action
- **THEN** the candidate frame shows Leizi's default persuaded-and-left reaction exactly once and the baseline frame lacks that reaction after all current text has drawn

### Requirement: Evidence inspection and locality
All four original-resolution images MUST be inspected for readability, fairness, absence of errors, and the claimed visible difference, and SHALL remain local until the user separately authorizes publication.

#### Scenario: Evidence acceptance
- **WHEN** the four frames have been captured
- **THEN** an independent visual inspection confirms that the text is readable, no debug or error window is present, the stopping points are comparable, and the behavior difference is understandable without private code context

#### Scenario: Invalid or blocked capture
- **WHEN** the Tk window cannot be operated faithfully or any parity condition fails
- **THEN** no image is called valid evidence and the blocker is recorded without publishing, pushing, or creating or editing a PR
