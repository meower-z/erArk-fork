## 1. Preserve and classify the prototype

- [x] 1.1 Commit the existing non-PO settlement-input work on a temporary backup branch and return to the original branch
- [x] 1.2 Record the prototype commit, mod-only boundary, migration map, and intentionally omitted browser change in the design

## 2. Implement independent local mods

- [x] 2.1 Create `local_settlement_input_fix` with wrapper-based Web wait publication, direct event/talk pacing, and scoped skip ownership
- [x] 2.2 Create `local_npc_move_talk_context_fix` that preserves NPC identity for exactly `{move}` and delegates all other paper-doll formatting
- [x] 2.3 Enable both mods with explicit load order and document patch points, dependencies, rollback, and upstream migration guidance

## 3. Add focused verification

- [x] 3.1 Add component tests for Web wait single-consumption, recording behavior, dialog pacing, skip ownership, and exception cleanup
- [x] 3.2 Add component tests proving several NPC `{move}` calls retain distinct NPC names while player and non-movement formatting delegate unchanged
- [x] 3.3 Run loader checks, focused component tests, broader maintained-mod tests, syntax checks, and verify upstream source/browser files remain clean

## 4. Direct GUI behavior review

- [x] 4.1 Have a subagent operate the real Tk GUI directly, exercise representative movement and wait flows, and inspect screenshots without a scripted BDD driver
- [x] 4.2 Record exact GUI actions, screenshots, observed behavior, residual gaps, and final maintenance guidance in the mod documentation and OpenSpec notes
- [x] 4.3 Perform a fresh diff review against the request and run strict OpenSpec validation
