# HOLD

**本 change 已暂缓。除 1.1 的文档保存外，任何任务都不得开始，直到用户明确恢复并完成 1.2–1.4。**

## 1. Resume Gate

- [x] 1.1 Persist the deferred decision, accepted architecture direction, feasibility analysis, specification, Fable review, and recovery conditions in this OpenSpec change
- [ ] 1.2 Obtain an explicit user decision that the expected benefit now justifies resuming the change
- [ ] 1.3 Re-audit current source paths and diff them against the 2026-07-14 design before relying on any saved code claim
- [ ] 1.4 Obtain maintainer direction approval for the refreshed responsibility boundary; do not treat this as live-cutover approval

## 2. Phase 0 Evidence Baseline

- [ ] 2.1 Build a complete producer/sink/clear/Socket inventory, including quick medicine, new-ui snapshots, polling fallback, client deduplication, Socket-only modals, and adapter installation order
- [ ] 2.2 Add non-mutating Tk tracing for producer, JSON enqueue/dequeue, draw completion, and wait/askfor entry and exit
- [ ] 2.3 Add non-mutating Web tracing for producer, buffer append, destructive read, clear, Socket emit, browser receipt, and visible render
- [ ] 2.4 Capture field/event-level baseline payloads and define written normalization rules for every dynamic value
- [ ] 2.5 Document the settlement-modal description dependency and select an explicit owner or prove exact compatibility behavior
- [ ] 2.6 Execute the approved Tk/Web scenario matrix and stop on every unexplained difference
- [ ] 2.7 Request separate live-cutover approval only after all Phase 0 blockers are closed

## 3. Module Skeleton and Shadow

- [ ] 3.1 Add the closed InformationFact types and module-owned factories without producing player-visible output
- [ ] 3.2 Implement validation, immutable snapshots, monotonic sequence allocation, and active-renderer single dispatch
- [ ] 3.3 Add Tk, Web compatibility, and recording adapter seams while preserving existing UI/flow ownership
- [ ] 3.4 Add the temporary `(producer, sink)` LEGACY/SHADOW/CUTOVER matrix and quiet-point assertions
- [ ] 3.5 Shadow StatusChange from the producer side without consuming or clearing any legacy buffer
- [ ] 3.6 Add contract tests for ordering, time rollback, snapshot immutability, adapter failure, and no automatic retry or fallback

## 4. First Live Sink Projection

- [ ] 4.1 Cut only settlement narration to the Web `instruct_texts` sink at an approved quiet point
- [ ] 4.2 Prove `game_state_update.instruct_texts` content, order, count, and clear timing match baseline
- [ ] 4.3 Prove the same producer's legacy `realtime_text`, Tk settlement narrative, and value changes remain unchanged
- [ ] 4.4 Exercise quiet-point rollback without replay or backfill

## 5. Complete Status Producers

- [ ] 5.1 Cut over Tk settlement narrative with exact text/style/line/wait-adjacency parity
- [ ] 5.2 Cut over settlement Web value changes while preserving per-character reads and 2-second/5-second/target-switch timing rules
- [ ] 5.3 Migrate each non-settlement status direct writer from the Phase 0 inventory one producer/sink cell at a time
- [ ] 5.4 Confirm every inventoried status writer is migrated or explicitly ruled outside this module

## 6. Talk and Narration

- [ ] 6.1 Publish Talk and Narration only after template, AI-text, actor/target, and style resolution is complete
- [ ] 6.2 Match Tk rich-text segmentation, line breaks, pagination, and wait adjacency
- [ ] 6.3 Match Web instruct history, realtime text, and main/minor dialog behavior

## 7. Event Text

- [ ] 7.1 Migrate child, DIY, and no-option event text to the existing direct dialog/history sinks
- [ ] 7.2 Map parent event text to `pending_event_text` while leaving option labels, modal input, history, and delayed consumption with the existing option flow
- [ ] 7.3 Verify pure-text, parent, child, DIY, settlement-modal, and event-modal paths against baseline

## 8. Explicit Notices and Cleanup

- [ ] 8.1 Inventory and migrate only explicit time-ordered notice producers; never infer notice semantics by globally intercepting draw primitives
- [ ] 8.2 Delete migrated producer-side Tk/Web branches and duplicate sink writes after each parity gate passes
- [ ] 8.3 Ensure every destructive read has one owner
- [ ] 8.4 Delete recording, route, and shadow migration facilities after all producers are complete
- [ ] 8.5 Re-run complete real Tk/Web parity evidence with mods disabled and document any intentionally normalized difference
- [ ] 8.6 Evaluate runtime draw patch replacement only as a separate future change
