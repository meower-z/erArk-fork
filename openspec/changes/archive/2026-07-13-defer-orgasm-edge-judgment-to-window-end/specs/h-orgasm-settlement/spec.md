## MODIFIED Requirements

### Requirement: Merge orgasm edge judgment per player action window
The system SHALL accumulate all orgasm edge crossings silently during a player action window and SHALL perform at most one orgasm edge success/failure roll per character at the end of that window (after every character has settled up to the window's target time and before control returns to the player), with the roll difficulty reflecting the window's full accumulated edge counts.

#### Scenario: Crossings accumulate silently during the window
- **WHEN** a character under active edging crosses an orgasm level at any settlement pass inside a player action window (including multiple parts in one pass and repeated crossings across passes)
- **THEN** each crossing part's climax count is immediately added to that part's `orgasm_edge_count`
- **AND** the character is recorded as pending window-end judgment together with the crossed parts and merged climax counts
- **AND** no edge roll, prompt, or edge talk occurs at crossing time

#### Scenario: Single roll at window end includes window accumulation
- **WHEN** the player action window's main behavior loop completes and a character has pending edge crossings and still satisfies the active-edging premise
- **THEN** the system rolls edge success exactly once for that character via the existing edge success formula
- **AND** the roll difficulty uses `orgasm_edge_count` values that already include this window's accumulated crossings
- **AND** on success the accumulated counts remain in place for later release settlement

#### Scenario: Window-end failure releases everything on the spot
- **WHEN** the window-end roll fails for a character
- **THEN** the character's entire pending `orgasm_edge_count` (prior accumulation plus this window's crossings) is converted into ordinary orgasm settlement immediately at window end, following the existing failure-release settlement semantics
- **AND** the character's `orgasm_edge_count` is cleared and `h_state.orgasm_edge` is reset afterwards so no pending or release state can settle later (matching the group edge release cleanup contract)
- **AND** the release's second-stage effects and value changes are drawn as part of the window-end output

#### Scenario: Characters who left H mid-window are skipped
- **WHEN** a character with pending edge crossings no longer satisfies the active-edging premise at window end (for example the existing exit-path release already settled and cleared their edge state mid-window)
- **THEN** the window-end judgment silently skips that character and discards the pending record
- **AND** the mid-window exit-path release behavior is left unchanged

#### Scenario: New player action window starts fresh
- **WHEN** the player issues the next instruction (a new `over_behavior_character` action window begins)
- **THEN** the pending-judgment records of the previous window are discarded
- **AND** the next window's crossings accumulate and judge anew, preserving the declining success rate across windows through the accumulated `orgasm_edge_count`

#### Scenario: Time-stop edging path is unaffected
- **WHEN** a character is under the time-stop unconscious state (`unconscious_flag_3`)
- **THEN** crossings are recorded into `time_stop_orgasm_count` as before and never enter the window-end edge judgment

### Requirement: Show one edge prompt and one representative edge talk per window
The system SHALL display at most one edge success/failure prompt per character per player action window, shown at window end, and at most one representative `{part}_orgasm_edge` talk whose part is chosen across all parts that crossed during the entire window.

#### Scenario: No mid-window edge display
- **WHEN** edge crossings occur at any settlement pass inside the player action window
- **THEN** no edge prompt, part-list line, or edge talk is displayed at crossing time
- **AND** the accumulated counts are still fully reflected in the eventual edge release settlement

#### Scenario: Single-part window display
- **WHEN** exactly one part crossed under edging during the whole window
- **THEN** the original success / at-limit / failure prompt is shown once at window end
- **AND** that part's `{part}_orgasm_edge` talk plays on success

#### Scenario: Multi-part window display
- **WHEN** two or more parts crossed under edging during the window (in one pass or across passes)
- **THEN** the original prompt is shown once at window end
- **AND** the yellow edge title embeds all crossed part names directly before “绝顶寸止”, joined with the Chinese enumeration delimiter `、`
- **AND** no separate white “寸止部位：...” line is displayed
- **AND** only one representative part's `{part}_orgasm_edge` talk plays on success, chosen by highest merged climax count across the whole window with ties broken randomly

#### Scenario: Multiple pending characters are output deterministically
- **WHEN** two or more characters have pending edge judgments at the same window end
- **THEN** their judgments and displays are processed in ascending character ID order

#### Scenario: Window-end output is visible in web text recording
- **WHEN** the game runs in web mode and window-end judgments produce prompts, talks, or release settlements
- **THEN** that output is emitted before the window's web text recording is closed

### Requirement: Complete window-end failure-release derivatives in the same action window
Manual verification on 2026-07-10 exposed a regression specific to the new window-end failure path: the release batch applies orgasm effects, but the normal post-orgasm mark and automatic-acquisition checks have already run for that character. Newly eligible mark output therefore remains pending until the next ordinary character settlement. The system SHALL complete results derived from a window-end failure release before control returns to the player, without replaying unrelated behavior-settlement stages.

#### Scenario: Failure release crosses a mark threshold
- **WHEN** a window-end edge failure releases enough orgasms to newly satisfy a mark threshold, including happy or unconscious marks
- **THEN** the mark ability change and its normally immediate mark second-behavior effect and visible output are settled in the same player action window
- **AND** the output follows the release batch that made the mark eligible rather than appearing at the start of the next player action

#### Scenario: No previous-window mark behavior leaks into the next action
- **WHEN** all mark results derived from a window-end failure release have been settled
- **THEN** no mark second behavior generated by that release remains active for the next ordinary `check_second_effect` call
- **AND** the next player action does not display mark talk or acquisition text belonging to the previous action window

#### Scenario: Release crosses an automatic talent threshold
- **WHEN** a window-end failure release changes orgasm-related experience so that an automatic `gain_talent(..., now_gain_type=0)` condition becomes newly true, such as experience 111 reaching the drinking-climax talent threshold
- **THEN** the eligibility check and immediate talent acquisition state/output are not deferred solely because the release ran after the character's normal per-behavior talent check
- **AND** any follow-up talent second behavior retains the same timing semantics as the ordinary path rather than being broadly replayed at window end

#### Scenario: Derived settlement does not replay unrelated stages
- **WHEN** the system completes derivatives of a window-end failure release
- **THEN** it does not rerun first-meet, insert-position, item, base action, extra activity experience, or unrelated queued second behaviors
- **AND** it does not recursively judge or release the same orgasm batch again
- **AND** only behaviors newly generated by the release's required derivative checks are eligible for same-window consumption

### Requirement: Treat an explicit edge release as one atomic orgasm batch
The system SHALL treat the orgasms released by the explicit release instruction (effect 526) as one completed batch on the target's current change object and SHALL NOT immediately reinterpret the values produced by that batch as a second orgasm wave during the target's following second-stage closure.

#### Scenario: Multi-part explicit release uses the compact batch display
- **WHEN** an explicit edge release settles pending counts from more than three body parts
- **THEN** the system displays the matching plural-orgasm output first
- **AND** no more than three representative body parts use full part-orgasm talk
- **AND** all remaining body parts are represented by the existing grouped compact summary rather than full talk for every part

#### Scenario: Target closure follows an already completed explicit release
- **WHEN** effect 526 has completed an explicit release batch into a target change object and that same object is then passed to the target's `check_second_effect`
- **THEN** the target closure consumes a release-completed marker and skips the immediate `orgasm_judge` plus the broad second-behavior pass used only to consume that judge's new orgasm queue
- **AND** first-meet, position, item, mark, and mark-filtered stages retain their normal ordering
- **AND** the release-generated pleasure and status values do not produce a follow-up p2 orgasm wave

#### Scenario: Suppression is scoped to one change object
- **WHEN** the character later enters `check_second_effect` with a different change object
- **THEN** ordinary orgasm judgment runs normally
- **AND** no module-global release token suppresses a real orgasm from a later settlement or player action

### Requirement: Keep exhaustion output after the orgasm batch that caused it
When an H or group-sex settlement makes an NPC too exhausted to continue, the system SHALL finish that settlement's orgasm batch and its directly owned output before displaying the exhaustion/leave notice and applying visible interruption output.

#### Scenario: Orgasm effects cross the exhaustion boundary
- **WHEN** the current settlement's orgasm effects reduce an NPC to the exhaustion threshold
- **THEN** plural orgasm output, representative part talks, compact part summary, directly derived milk/urine output, and batch value changes are completed first
- **AND** the NPC's “太累了” / unable-to-continue / early-leave notice is displayed after that batch
- **AND** the NPC does not execute another H action after the interruption takes effect

#### Scenario: NPC was already exhausted before a new action
- **WHEN** an NPC is already ineligible to start another action before the current settlement begins
- **THEN** the pre-action exhaustion gate may still prevent the new action
- **AND** reordering batch-caused notices SHALL NOT grant an extra action to an already exhausted NPC

### Requirement: Failure release produces no lower-strength follow-up wave
The system SHALL treat a window-end or exit-path edge failure release as one atomic orgasm release for display and effect ownership. Once the batch has selected the strongest display behavior for each part and flushed all owned behaviors, the same release SHALL NOT later display a lower-strength orgasm for an already represented part or reapply its derivatives as a second wave.

#### Scenario: One released part contains several strength behaviors
- **WHEN** a failure release generates both strong and small orgasm behaviors for the same body part
- **THEN** only the strongest behavior is eligible for that part's full visible talk in the release batch
- **AND** lower-strength behavior effects may settle silently according to their recorded counts
- **AND** no lower-strength full talk from that release remains queued after the batch

#### Scenario: Release batch is followed by later closure stages
- **WHEN** the failure release batch has completed and later closure stages run in the same player action window
- **THEN** those stages do not call `orgasm_settle` again for the same released counts
- **AND** they do not consume a stale part-orgasm entry from `second_behavior`, `must_show_second_behavior_id_list`, or `must_settle_second_behavior_id_list`
- **AND** milk or urine output appears at most once as a derivative owned by the single release batch

#### Scenario: Diagnostic identifies the owner before implementation
- **WHEN** the observed “plural/strong batch followed by small part orgasm” regression is reproduced
- **THEN** instrumentation records each `orgasm_settle` call's sequence, change-object identity, normal/extra/un-count dictionaries, edge state, and relevant queued behaviors
- **AND** the selected fix targets the confirmed second-call or queue owner rather than hiding the later text

## ADDED Requirements

### Requirement: Take over the main behavior loop without altering unrelated behavior
The system SHALL implement the window-end judgment hook by replacing `character_behavior.init_character_behavior` with a component-owned copy, without modifying the core main-loop file and while preserving all unrelated main-loop behavior. Core-file diffs owned by other independent changes are outside this component requirement.

#### Scenario: Core main-loop file remains untouched
- **WHEN** the component is installed
- **THEN** this component introduces no diff to `Script/Design/character_behavior.py`
- **AND** unrelated core-file diffs owned by other changes do not violate this component-scoped requirement
- **AND** the replacement is registered through the existing mod patch registry

#### Scenario: Main-loop behavior is equivalent outside the hook
- **WHEN** the replaced main loop runs without any pending edge judgment
- **THEN** player settlement, NPC catch-up, new-day settlement, sleep auto-save, time-stop rollback, and achievement settlement behave identically to the original function

#### Scenario: Component is disabled
- **WHEN** the component is disabled
- **THEN** the original `init_character_behavior` and the original crossing-time edge judgment behavior are restored
