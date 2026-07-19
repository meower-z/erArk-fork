# Closure: elapsed-time line ownership (upstream PR #220)

- PR: `Godofcong-1/erArk#220` — 修复多角色结算时「X分钟过去了」被逐个面板重复输出的问题, from `meower-z:codex/fix-elapsed-time-line-ownership`.
- State: **CLOSED, not merged**, on 2026-07-16.
- Verdict: rejected as a design-intent conflict — the maintainer keeps the per-character time hints deliberately and will only reword them himself.

## Why the PR existed

When one action settlement involves several characters, every character panel that produces settlement text appends its own elapsed-time line: 「X分钟过去了」 in the ordinary case, or 「该行动将持续X分钟」 when an NPC acts on the player. One game-time advance is therefore announced once per panel — worst during 群交 — and each line uses that character's own local `add_time` in `settle_behavior.handle_settle_behavior`, which does not equal the round's actual net clock advance, so the numbers can mislead the player.

## What the PR did

Move ownership of the elapsed-time announcement from character settlement panels to the outermost update layer:

- Delete the per-character time-line append in `settle_behavior.handle_settle_behavior`, covering both wordings.
- `game_update_flow` records the game clock on entry and, only at the outermost layer (using the existing update-depth counter), announces a single 「X分钟过去了」 from the net minute delta after all player and NPC settlements. Nothing is emitted when the net delta is zero or negative, and nested updates emit nothing of their own.
- Tk keeps its existing text output path; Web keeps appending to `cache.web_instruct_texts` and pushing an `instruct`-typed real-time message — one line instead of several.

## Why it was closed

Maintainer Godofcong-1 explained that the per-character time hint dates back to a much older version: several players wanted to know how long each character's single action took, so the line was added deliberately. He agreed the current wording can mislead and will adjust the text description himself, but keeps the feature itself; he closed the PR and welcomes reopening if other issues arise. The deduplication behavior was therefore rejected on design-intent grounds — per-panel hints stay, only their wording will change — not on any defect in the diff.

## Design conclusions worth keeping

- Both wordings are the same violation. 「该行动将持续X分钟」 is not a pre-action preview: it is emitted from the same panel-tail branch and the same local `add_time` as 「X分钟过去了」, at settlement time. If per-panel time lines are ever removed again, removing only one wording leaves the same defect alive on the exchange sibling path — the two must go together (this was the deciding point in the design reassessment, which picked the remove-both candidate).
- Web delivery is a hard boundary. In Web mode `character_behavior.py` skips panel drawing (`if cache.web_mode: pass`), so the time line's only route to the player is `cache.web_instruct_texts` plus `emit_realtime_text(..., "instruct")`. Any reimplementation must keep that channel; routing through `io_init.era_print` would switch to the drawing-element channel and change Web behavior.
- Evidence gap at close. No Tk screenshot taken under the final commit showed the single merged line without 「该行动将持续」; the archived "after" frames came from an intermediate build that still printed that wording. The evidence review rated the package `BLOCKED` for ready-for-review status, so the published PR carried before/after screenshots for the per-panel removal only and disclosed the pending final frame.

## Artifacts

Preserved next to this file under `artifacts/`:

- `artifacts/local-evidence/` — the design reassessment (`design-reassessment-20260715.md`, the candidate comparison that chose removing both wordings), the Fable boundary and evidence reviews with their prompts, the PR-artifact review, and the proposed and screenshot-embedded PR title and body (`pr-title-proposed.md`, `pr-body-proposed.md`, `pr-body-with-screenshots-20260715.md`).
- `artifacts/test_elapsed_time_line_ownership.py` — local regression test pinning that character panels emit no time lines (including the exchange wording), the outermost update announces exactly one line from the positive net clock delta, nested updates and exceptions fold into it, midnight rollover works, and Web history records the line exactly once.

The fork branch `codex/fix-elapsed-time-line-ownership` on `meower-z/erArk-fork` is deleted; this record and the artifacts are the surviving copy of the work.
