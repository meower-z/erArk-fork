# h-orgasm-settlement Specification

## Purpose
Define the local bugfix contract for batching H orgasm settlement, display, human-power output, and H interruption ordering.
## Requirements
### Requirement: Implement batch settlement as a local bugfix component
The system SHALL implement the H orgasm batch settlement fixes through an enabled split local bugfix component rather than direct edits to core game files or the retired monolithic `local_bugfix` mod.

#### Scenario: Core game files remain untouched
- **WHEN** the H orgasm batch component is installed
- **THEN** the replacement behavior is registered from the component's own mod manifest
- **AND** core files such as `Script/Design/second_behavior.py` and `Script/Design/handle_npc_ai.py` do not need direct edits for this fix

#### Scenario: Component loads without unrelated bugfixes
- **WHEN** the H orgasm batch component is enabled with only its declared dependencies
- **THEN** the component SHALL load successfully through the mod loader
- **AND** H orgasm batch tests SHALL NOT require unrelated split bugfix components to be enabled

### Requirement: Batch NPC orgasm events during H settlement
The system SHALL treat all NPC orgasm events detected during one orgasm settlement pass as a single batch before executing display and effect settlement.

#### Scenario: One body part reaches multiple orgasm strengths in one batch
- **WHEN** a body part generates multiple orgasm behavior IDs in the same batch, such as `c_orgasm_small`, `c_orgasm_normal`, and `c_orgasm_strong`
- **THEN** the batch records every distinct generated behavior ID for effect settlement
- **AND** the batch selects only the strongest behavior ID for that body part's visible talk

#### Scenario: Repeated same behavior ID occurs in one batch
- **WHEN** the same orgasm behavior ID is generated more than once in the same batch (for example a pending edge release with count N, or several rolls landing on the same strength)
- **THEN** the batch records the occurrence count for that behavior ID
- **AND** that behavior ID's configured effects are settled once per recorded occurrence, so no rolled orgasm loses its attribute settlement
- **AND** visible talk for that body part is still shown only once for the batch

### Requirement: Show only representative orgasm talk
The system SHALL separate orgasm effect settlement from orgasm talk display so that non-representative orgasm events can settle silently.

#### Scenario: Single-part multi-orgasm display
- **WHEN** one body part has multiple orgasm events in the same batch
- **THEN** the system displays at most one part orgasm info line and at most one part orgasm talk for that body part
- **AND** the displayed part orgasm is the strongest event selected for that part

#### Scenario: Multi-part orgasm display
- **WHEN** two or more body parts orgasm in the same batch
- **THEN** the system first displays the matching original multiple-orgasm info and talk
- **AND** the system displays each orgasming body part exactly once in the following body-part detail output
- **AND** no more than three representative body parts use the original part-orgasm info-and-talk format
- **AND** body parts outside those three representatives display short strength text only in one grouped line
- **AND** representative body parts do not receive an additional duplicate strength-only line

#### Scenario: Representative part info keeps compact spacing
- **WHEN** a representative body part displays its original-format strength info followed by orgasm talk
- **THEN** the strength info and following talk are separated by exactly one blank line
- **AND** the compact formatting does not add extra blank lines before the next representative body part

#### Scenario: Remaining body parts are summarized on one line
- **WHEN** body parts outside the representative limit need strength-only display
- **THEN** the system groups body-part names by orgasm strength
- **AND** the remaining body-part summary is displayed as one line in the form `{character name} <parts> 强绝顶，<parts> 绝顶，<parts> 小绝顶`

#### Scenario: Representative body parts are selected by importance
- **WHEN** more than three body parts orgasm in the same batch
- **THEN** the system selects representatives from the highest orgasm strength first
- **AND** when multiple body parts tie at the same strength, the tied representatives are chosen randomly

### Requirement: Preserve existing orgasm effects and values
The system SHALL preserve existing configured effects for part orgasms, plural orgasms, extra orgasms, milk release, urine release, exposure checks, experience gains, and human-power generation.

#### Scenario: Lower-strength orgasms are hidden but still settled
- **WHEN** a lower-strength distinct orgasm behavior is not selected for visible talk because a stronger orgasm happened in the same body part batch
- **THEN** effects configured for the lower-strength behavior still execute
- **AND** status changes are accumulated into the same settlement change data as the visible representative orgasm

#### Scenario: Plural orgasm effects are applied
- **WHEN** a batch contains orgasms from at least two body parts
- **THEN** the system applies the matching `plural_orgasm_N` effects
- **AND** the system updates the plural orgasm body-part set used by existing plural-orgasm premises

### Requirement: Aggregate human-power display without changing generation
The system SHALL keep existing human-power generation settlement calls and values while displaying only one generated-power prompt for a multi-orgasm batch.

#### Scenario: Multiple human-power calls occur in one multi-orgasm batch
- **WHEN** part orgasm effects and the plural orgasm path each call `store_power_by_human_power()` during one multi-orgasm batch
- **THEN** each original generation call still executes
- **AND** individual generated-power prompts are suppressed during the batch
- **AND** one prompt is displayed after aggregation

#### Scenario: Aggregated prompt uses original plural text
- **WHEN** the batch displays the aggregated generated-power prompt
- **THEN** the prompt uses the original plural-orgasm generated-power text format
- **AND** only the generated-power number is replaced with the batch total

### Requirement: Finish orgasm batch before H exhaustion interruption
The system SHALL complete all orgasm batch effects while the character is still considered in H before processing HP or fatigue based H interruption.

#### Scenario: Orgasm effects reduce HP to exhaustion during H
- **WHEN** an orgasm batch causes the player or target character HP to reach the exhaustion threshold
- **THEN** all effects in that orgasm batch are settled before H reset or H end behavior runs
- **AND** any orgasm count, experience, mark, max HP/MP growth, and H-scoped statistics from the batch are counted as H-internal results

#### Scenario: H interruption runs after batch completion
- **WHEN** an orgasm batch has finished and the character is exhausted
- **THEN** the existing H exhaustion interruption behavior may run
- **AND** the interruption uses the final post-batch HP, fatigue, orgasm count, and H-state data

### Requirement: Keep existing data compatibility
The system SHALL continue using existing orgasm behavior IDs and configured second effects.

#### Scenario: Existing CSV data is loaded
- **WHEN** game configuration is rebuilt from CSV
- **THEN** existing behavior IDs such as `c_orgasm_strong`, `plural_orgasm_4`, `extra_orgasm`, `b_orgasm_to_milk`, and `u_orgasm_to_pee` remain valid
- **AND** existing talk files for those behavior IDs remain usable for representative talk selection

### Requirement: Keep local batch implementation runtime-safe
The system SHALL keep the local batch implementation from shadowing runtime helpers that are needed later in the same settlement.

#### Scenario: Achievement flow runs after batch orgasm settlement
- **WHEN** orgasm batch settlement reaches achievement flow after iterating orgasm counts
- **THEN** the translation helper remains callable for translated achievement labels
- **AND** batch settlement does not raise a `TypeError` caused by a loop variable shadowing the translation function

#### Scenario: Playtest log regression is guarded
- **WHEN** local H orgasm batch settlement reaches the achievement flow after multi-part or repeated orgasm settlement
- **THEN** `achievement_panel.achievement_flow(_("绝顶"), 1221)` or its equivalent SHALL execute with `_` still bound to the translation helper
- **AND** the component SHALL NOT raise `TypeError: 'int' object is not callable`
- **AND** the regression test SHALL cover the settlement path that produced the playtest `error.log` traceback

### Requirement: Clear same-batch legacy orgasm queue entries
The system SHALL prevent orgasm second behaviors generated in one batch from remaining queued after the batch has displayed and settled.

#### Scenario: Old orgasm filter list does not include newly generated orgasm behaviors
- **WHEN** orgasm settlement generates new part orgasm behaviors after a previous orgasm filter list has already been captured
- **THEN** the new behaviors are still displayed or settled by the current batch as appropriate
- **AND** none of those same-batch part orgasm behaviors remain queued for a later update

#### Scenario: Plural orgasm is followed by later update
- **WHEN** a multiple-orgasm batch has already displayed its plural orgasm output and representative part outputs
- **THEN** a later second-behavior update does not display a leftover single body-part orgasm from that same batch

### Requirement: Expose batch flush state to dependent components
The H orgasm batch component SHALL expose its batch flush state so declared dependent components can coordinate cleanup safely.

#### Scenario: Batch state is visible to dependent cleanup
- **WHEN** another declared component needs to detect whether H orgasm batch settlement is currently flushing effects
- **THEN** the H orgasm batch component SHALL expose a documented function or registered hook for that state
- **AND** the dependent component SHALL declare the dependency instead of importing hidden implementation details

### Requirement: Verify H orgasm batch with isolated and integrated flows
The H orgasm batch component SHALL be verified both alone and with any declared dependent components.

#### Scenario: Isolated batch verification runs
- **WHEN** only the H orgasm batch component and its dependencies are enabled
- **THEN** unit tests SHALL cover same-part display dedupe, same-batch queue clearing, human-power aggregation, remote draw suppression, hypnosis-state second talk, and achievement runtime safety

#### Scenario: Integration with group edge release runs
- **WHEN** the group edge release component declares and uses the H orgasm batch component
- **THEN** integration tests SHALL confirm pending edge release is not double-flushed
- **AND** multi-count edge release SHALL preserve the expected orgasm count and plural effect behavior


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

