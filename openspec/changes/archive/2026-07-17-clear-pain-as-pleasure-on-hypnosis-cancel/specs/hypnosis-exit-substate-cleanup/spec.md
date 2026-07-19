## ADDED Requirements

### Requirement: Hypnosis exit clears the shared continuous sub-states
The system SHALL clear `increase_body_sensitivity`, `blockhead`, `active_h`, `roleplay`, and `pain_as_pleasure` through one shared cleanup operation when either direct hypnosis cancellation or sleep cleanup ends those sub-states.

#### Scenario: Direct hypnosis cancellation
- **WHEN** direct `解除催眠` settles for a target with all five shared sub-states active
- **THEN** all five sub-states SHALL be inactive after settlement

#### Scenario: Sleep cleanup
- **WHEN** sleep behavior runs effect 489 for a character with all five shared sub-states active
- **THEN** all five sub-states SHALL be inactive after settlement

### Requirement: Caller-specific behavior remains owned by each caller
The shared cleanup operation SHALL NOT mutate unconscious-state matching, abnormal-flag settlement, air-hypnosis state, second-stage settlement, `h_state.npc_active_h`, `hypnosis_degree`, or `force_ovulation`.

#### Scenario: Direct and sleep paths use the helper
- **WHEN** either caller invokes the shared cleanup operation
- **THEN** that caller SHALL retain its existing path-specific predicates and side effects outside the helper

### Requirement: Evidence comes from the corrected candidate
The verification workflow SHALL capture a comparable real-Tk direct-cancellation A/B using the corrected candidate source, the same reproduction save, and the same visible player actions.

#### Scenario: Direct cancellation is compared
- **WHEN** `[4004]解除催眠` completes in baseline and corrected-candidate runs that start with `(痛→快感)` active
- **THEN** baseline SHALL retain `(痛→快感)` and the corrected candidate SHALL remove it while both retain the displayed hypnosis degree

### Requirement: Evidence survives temporary-runtime cleanup
The workflow SHALL archive retained media and the minimum replay package under `~/games/archive` and verify the archived copies before deleting task-owned temporary runtimes.

#### Scenario: Capture work completes
- **WHEN** the final evidence has been inspected and the supervised runtimes have stopped
- **THEN** archived media hashes SHALL match their source files before task-owned `/tmp` runtime and disposable capture directories are removed
