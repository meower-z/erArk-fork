## Why

Normal discovery and invitation entry points can still offer or admit a character who is exhausted or seriously fatigued, only for later group-sex logic to reject or remove that character. The existing local mod duplicates eligibility across UI callers and also embeds an unapproved cancellation-list policy, so it is not a suitable upstream boundary.

## What Changes

- Prove the player-visible failure through a matched real-Tk discovery or invitation route before changing production behavior.
- Give new group-sex admission one shared eligibility predicate owned by the premise/admission layer.
- Prevent exhausted or seriously fatigued characters from receiving or confirming a new invitation while preserving ordinary eligible flows.
- Provisionally keep an already invited character visible only so the player can cancel the invitation; require user confirmation of this gameplay rule before an upstream PR.
- Keep discovery-reaction settlement, group scheduling, and tired participant exit outside this change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `local-bugfixes`: Replace duplicated tired-discovery/invitation wrappers with one evidence-backed admission-eligibility contract and a provisional cancellation-only rule.

## Impact

This change affects group-sex discovery/invitation UI, admission premises, the temporary `local_group_participant_admission_fix` responsibility, and focused real-loader/Tk verification. It does not change current-participant exit scheduling or the separate discovery-settlement candidate.
