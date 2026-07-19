## Why

One `orgasm_settle()` invocation can contain climax work for several body parts. Core has no separate batch-decision phase: it decides edge success inside the per-part application loop, then communicates a post-mutation failure through hidden state to `orgasm_judge()`, which replays non-idempotent original inputs. Earlier parts can therefore be committed as held before a later part fails and consumes the same inputs again. The underlying defect is not one bad state value or dictionary merge; those are consequences of the missing batch-decision boundary.

The intended rule is that one settlement invocation first decides one result for the complete batch, then applies that result to every part without replay.

## What Changes

- Reshape core edge settlement into three local phases: collect the complete current batch, decide edge success once, then apply one shared result.
- Let `judge_orgasm_edge_success()` accept an optional explicit count snapshot. Existing one-argument callers continue reading the committed held ledger; core settlement supplies a local candidate snapshot containing prior held counts plus the complete current batch.
- Keep `orgasm_edge_count` limited to committed successful holds; do not temporarily write provisional counts into live character state.
- On shared success, retain every current supported count and queue the existing part-specific edge behaviors. On shared failure, release the prior held counts and current batch through the existing ordinary settlement path without caller replay or newly queued edge behavior.
- Remove the internal state-`3` failure handshake and the caller retry.
- Preserve non-edge settlement, time-stop accumulation, explicit release, existing effect batching, and the local mod's separate player-action-window policy.

## Capabilities

### New Capabilities

- `core-orgasm-edge-settlement`: Defines one complete edge decision and one shared outcome within a single core `orgasm_settle()` invocation.

### Modified Capabilities

None.

## Impact

The upstream production change remains local to `Script/Design/second_behavior.py` plus focused submitted tests. `judge_orgasm_edge_success()` gains a backward-compatible optional input; all existing in-repository production callers that omit it retain current behavior. The change intentionally replaces per-part rolls with one roll per settlement invocation, but does not aggregate separate invocations into one player action.
