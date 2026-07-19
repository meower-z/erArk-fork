# Closure: signed pain-as-pleasure routing (upstream PR #212)

- PR: `Godofcong-1/erArk#212` — 修复：开启苦痛快感化后，减少苦痛的结算会错误扣减心理快感, from `meower-z:codex/fix-signed-pain-routing`.
- State: **CLOSED, not merged**, on 2026-07-16.
- Verdict: superseded — the maintainer fixed both underlying issues directly upstream (`fbdda9d`, `8882a6a`) and the author agreed; not rejected on design grounds.

## Why the PR existed

With 苦痛快感化 enabled, settlements that should reduce 苦痛 instead wrongly reduced 心理快感. Example: `[4103]体控-强制高潮` used on an affected character should greatly reduce 苦痛, but instead drained 心理快感 to zero (observed as far as lv10→0) while 苦痛 actually rose.

## Root cause

The pain-as-pleasure conversion did not distinguish the direction of the 苦痛 change. While the switch was on, any 苦痛 delta in common state settlement — including negative, pain-reducing deltas — was rerouted to 心理快感 settlement, so "reduce pain" became "reduce psychological pleasure" and the pain reduction itself was skipped. Separately, entry points that add 苦痛 directly (small/medium/large pain settlement, and the extra 苦痛 appended by consecutive extra climaxes) bypassed conversion entirely, so pain still accumulated while the switch was on.

## What the PR did

Collapse the pain-as-pleasure decision into one shared routing rule: each entry point first computes its 苦痛 delta as before, then the rule decides the destination — only a positive 苦痛 increment converts to 心理快感 when the switch is on; zero and negative changes settle as ordinary 苦痛. All common-state and direct-pain entry points route through this one rule, and the consecutive-extra-climax prompt text switches to 「心理快感和恐怖」 when conversion actually happens. The change touched `Script/Settle/Second_effect.py` and `Script/Settle/common_default.py`.

## Why it was closed

The maintainer fixed both underlying issues directly on upstream `main`, and the author agreed to close:

- `fbdda9dd816bbe8f55268cfe352d1dbf4abc036d` (`fbdda9d`) added the positive-pain check to the conversion.
- `8882a6a27026d73765d46e1800fb34fbdc0e8505` (`8882a6a`) unified the second-settlement character-state settlement to go through the common function.

## Artifacts

Preserved next to this file under `artifacts/`:

- `artifacts/rejected-local-fix.patch` — the local branch's fix commit `767562b83`, "fix: route signed pain conversion consistently".
- `artifacts/tests/test_signed_pain_routing.py` and `artifacts/tests/test_direct_pain_conversion.py` — regression tests that load the real settlement functions from `Script/Settle/common_default.py` and `Script/Settle/Second_effect.py` in isolation and pin the routing rule: with the switch on, only a positive 苦痛 delta converts, exactly once, through the canonical 心理快感 settlement with its admission guards intact, while zero/negative deltas and the switch-off case take the ordinary 苦痛 path. They also pin that the direct-pain writers (small-pain settlement and consecutive extra climaxes) use that same single conversion owner without skipping 恐怖 or state resets.

## Discarded noise

The local worktree also carried massive regenerated localization files (`data/po/zh_CN/LC_MESSAGES/erArk_cook_question.po` and `erArk_csv.po`, on the order of 10^5 changed lines). These were accidental build-artifact regenerations, not knowledge, and were deliberately not preserved.

The fork branch `codex/fix-signed-pain-routing` on `meower-z/erArk-fork` and its copy on `meower-z/erArk` are deleted; this record and the artifacts are the surviving copy of the work.
