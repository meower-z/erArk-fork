# Save 99 V-orgasm reachability hypothesis and runtime falsification

## Status

The arithmetic model below was a static route hypothesis, not a verified player route. A complete seed-0 production run later falsified its load-bearing scheduling premise: Theresa and Lin received no masturbation-part selection or effect-524 application during the first `[6001]`. Do not use the two-settlement calculation as evidence that this route is reachable.

## Population correction

Save 99 contains eleven characters in the scene: the player plus ten NPCs. Kal'tsit is both one of those ten NPCs and the current interaction target A, so there are nine different-NPC B candidates, not ten.

## Rejected scheduling premise: why the model expected two settlements

The rejected model treated effect settlement as if it occurred when the saved 11:45 masturbation behavior reached its 11:55 end, then treated the same wait as selecting and settling masturbation again. Current-upstream code does not work that way: NPC effects settle when a newly selected behavior starts through `judge_character_status()`, while group-sex type-1 logic overwrites the saved masturbation behavior with `SHARE_BLANKLY` before that settlement point. The old saved behavior's effects had already settled when it began before the save.

The model therefore predicted two effect-524 calls during the first wait; the seed-0 production run proved that scheduling premise false. It observed zero calls for Theresa and Lin.

## Rejected static two-candidate model

This calculation assumed both real effect-524 random part selections occurred and chose V. The arithmetic conditional on that assumption is retained to show why the route looked plausible, but runtime later showed that the two selections did not occur.

### Theresa (CID 56)

- Initial V pleasure: 803; recorded level: 2; next threshold: 1000.
- Ability coefficients from A4=2 and A30=2 are both 1.25. Five equipped tokens add 0.05; the eleven-person group adds `(11 - 2) * 0.02 = 0.18`; difficulty setting 4 multiplies by 1.25.
- Final adjustment: `(sqrt(1.25 * 1.25) + 0.05 + 0.18) * 1.25 = 1.85`.
- Each V settlement has base `int((10 + 50) * 1.85) = 111` before the existing one-tenth current-pleasure term.
- First settlement: `803 + int(111 + 803 / 10) = 994`, still below 1000.
- Second settlement: `994 + int(111 + 994 / 10) = 1204`, crossing 1000.
- V has nonzero production selection weight in both rounds: 100/879, then 101/880.

### Lin (CID 4080)

- Initial V pleasure: 5379; recorded level: 4; next threshold: 6000.
- The same verified adjustment gives base 111. The existing one-tenth term is capped at 333.
- First settlement: `5379 + int(111 + 333) = 5823`, still below 6000.
- Second settlement: `5823 + int(111 + 333) = 6267`, crossing 6000.
- V has nonzero production selection weight in both rounds: 151/428, then 152/429.

Both conditional calculations require two V selections. Because the real seed-0 flow produced zero such selections, they do not establish a one-wait player route. Other NPC waiting counts were not retained.

## Runtime falsification

A complete production seed-0 diagnostic used normal startup and save loading, changed CID 213 from 30% to 100% through seven real setting callbacks without changing RNG state, executed one `[6001]`, and answered both discovery panels with the normal `[4]邀请加入群交` callback. The run completed at 11:57 with the player target still Kal'tsit.

- Closure and Ch'en used ordinary `join_group_sex` behavior talk, not Talk_Common; target remained CID 3 before and after both panels.
- Theresa's V pleasure changed only from 803 to 840; Lin's changed only from 5379 to 5416.
- Neither character entered `handle_masturebate_add_adjust`, had a masturbation part selected, crossed an orgasm threshold, or produced an active second behavior.
- The command completed in 18.28 seconds with unchanged save hashes. The full diagnostic log has SHA-256 `c48d4d108c53406262af98bffc9bcc908e11e8a3fc42e7ce478f226d161d1aec` at `/tmp/erark-t7-seed-search-20260715/seed-00-choice4-bound.log`.

This is direct counterevidence to the static claim that the first wait necessarily settles the old masturbation behavior twice. A random seed cannot select V on a call that production does not make. Seed scanning is paused until the actual lifecycle explains why those effect-524 calls are absent and identifies a falsifiable normal trigger.
