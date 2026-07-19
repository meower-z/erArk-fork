## Why

2026-07-07 playtesting on the live group-sex save (slot 99) confirmed a repeat-edging bug that also exists in vanilla: the edging (寸止) success/failure roll and its prompt are scoped to "each settlement pass × each crossing body part", while the player-perceived window is "one button click". In group sex one click produces 100+ settlement passes across participants, and pleasure meters keep rising between passes (ambient shame/psychic growth, toys, masturbation effects), so one character gets several independent edge rolls and several success/failure prompts per click — the reported screenshot showed 陈 receiving both a success and a failure prompt in the same round.

## What Changes

- Aggregate edging judgment per player action window: within one player action (one click), each character gets at most ONE edge success/failure roll. The first orgasm-level crossing rolls; every later crossing by the same character in the same window reuses that result.
- Merge, don't skip: on success, every crossing part still adds its climax count to `orgasm_edge_count[part]`, so pending-release totals are unchanged from today. On failure, the existing `orgasm_edge = 3` failure-release path runs unchanged and is never suppressed.
- One prompt per character per window: the success / at-limit / failure system prompt is shown once, naming all merged parts, instead of once per part per settlement pass.
- Redesign multi-part edge talk (口上) display: when several parts merge under one edge judgment, show one representative part's `{part}_orgasm_edge` talk instead of one talk per part, consistent with the existing batch orgasm display scheme (representative parts + grouped one-line summary).
- The roll formula, time-stop edging path, and edge release settlement (effect 529, group-sex end) are untouched.
- Implemented inside the existing `local_h_orgasm_batch_fix` mod component (which already owns the patched `orgasm_settle`); no core file edits.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `h-orgasm-settlement`: add requirements scoping edge judgment and edge prompts to one per character per player action window, merged per-part edge counting, and representative-talk display for multi-part edge events.

## Impact

- `mod/local_h_orgasm_batch_fix/scripts/h_orgasm_batch.py` — edge branch of `patched_orgasm_settle` (per-part roll → per-window roll cache keyed on `cache.over_behavior_character` object identity, same technique as `local_group_masturbation_intent_fix`).
- BDD regression test on live save 99 (陈 id=10 with state thresholds placed below level boundaries) converted from the diagnosis feedback loop.
- No changes to core `Script/Design/second_behavior.py`, CSV data, or talk files.
