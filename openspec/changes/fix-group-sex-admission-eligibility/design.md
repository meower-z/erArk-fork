## Context

Group-sex admission is currently decided in several UI and premise paths. The local mod duplicates a fatigue check in discovery, invitation-list, direct-invite, and start-premise wrappers. Real-loader BDD demonstrates state-level inconsistency, but a matched real-Tk baseline is still required before production edits. Discovery-reaction settlement is already owned by a separate reviewed candidate and must not be recombined here.

## Goals / Non-Goals

**Goals:**

- Prove one normal player route that offers or admits an exhausted/seriously fatigued character.
- Give new admission one shared eligibility predicate used by every issuing/confirmation entry point.
- Preserve cancellation access for an already issued invitation without allowing an ineligible character to be confirmed.

**Non-Goals:**

- Decide current-participant tired exit, group scheduler epochs, or pending-edge release.
- Change discovery-reaction settlement or witness selection.
- Upstream the current mod's copied UI functions or global wrappers.

## Decisions

### Evidence precedes production implementation

The first task is a matched Tk baseline/candidate route through discovery or the invitation panel. State-only BDD remains supporting evidence. If the untouched baseline does not show the claimed player-visible failure, this change freezes rather than preserving the mod contract by assumption.

### One premise/admission predicate owns new eligibility

The shared predicate evaluates whether one character may receive or confirm a new group-sex invitation. UI lists and direct calls consume that result; they do not reimplement fatigue thresholds.

Alternative considered: keep wrappers at every caller. Rejected because callers can drift and direct calls can bypass a filtered list.

### Separate issuing from cancellation

Provisional gameplay rule: hit points at or below 1, an active tired flag, or tired level at least 2 makes a character ineligible for a new invitation or confirmation. If an invitation was already issued before eligibility changed, the character remains visible only so the player can cancel it; confirmation remains blocked.

Alternative considered: hide ineligible invited characters. Rejected provisionally because it removes the player's only obvious cancellation control. The user confirms this rule before an upstream PR.

### Keep discovery response outside admission ownership

A tired witness may require a separate narrative response, but this change only decides whether the character can be newly admitted. The reviewed panel-owned discovery settlement protocol remains untouched.

## Risks / Trade-offs

- **[UI route does not reproduce]** → freeze the task and retain BDD as a clue, not proof.
- **[Predicate changes ordinary non-group behavior]** → scope it to group-sex admission and add eligible/ineligible inverse cases at every consumer.
- **[Cancellation-only visibility is surprising]** → label the state clearly in evidence and obtain user semantic confirmation before PR creation.
- **[Existing local mod masks baseline]** → run matched evidence with the responsibility disabled on an untouched upstream base.
