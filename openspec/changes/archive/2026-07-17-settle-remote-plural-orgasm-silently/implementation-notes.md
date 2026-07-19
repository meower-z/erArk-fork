# Investigation and Implementation Notes

## Evidence Status

- Reported clue: confirmed from the player's screenshots and report. Waiting for an unrelated five-minute action can show another room's orgasm or double-orgasm output; one observed character then reaches the player and opens the group-sex discovery panel.
- Reproduced failure: automated red and real Tk baseline reproduction confirmed at `upstream/master` `06fc59c1e71d092224375fc4a096b956aea2ad63`.
- Confirmed cause: automated production-path test and static writer/reader trace agree that `plural_orgasm_2` through `plural_orgasm_11` do not enter the remote must-settle list and remain pending.
- Verified fix: focused automated green and real Tk A/B are complete; fable-5 accepted the final cause, scope, evidence, and CSV-only submission boundary. Artifact review: PASS (recorded below).

## Fixed Boundary

- Candidate worktree: `/home/ubuntu/games/erArk-pr-remote-plural-orgasm`
- Branch: `codex/settle-remote-plural-orgasm-silently`
- Base: `upstream/master` `06fc59c1e71d092224375fc4a096b956aea2ad63`
- Production change: append `997` to exactly ten `plural_orgasm_2` through `plural_orgasm_11` rows in `data/csv/Behavior_Effect.csv`.
- Local-only regression excluded from the submitted diff: `tests/test_remote_plural_orgasm_settlement.py`.
- Excluded known defects: `extra_orgasm`, `b_orgasm_to_milk`, and `u_orgasm_to_pee` remain outside the candidate because their effect functions draw directly.

## Automated Red and Green

The first test execution was invalid because the test reader treated every configured effect as an integer even though production accepts `CVE_*` strings. The reader was corrected to match the existing loader's integer-or-string rule before accepting any red evidence.

Valid baseline run:

```text
python -m pytest -q tests/test_remote_plural_orgasm_settlement.py
11 failed, 2 passed
```

All ten parameterized remote behaviors remained at pending value `1`; the nearby-display and excluded-derivative inverse cases passed.

Candidate run:

```text
python -m pytest -q tests/test_remote_plural_orgasm_settlement.py
13 passed in 0.57s
```

The regression executes the real `character_get_second_behavior`, remote `second_behavior_effect`, `must_settle_check`, and `handle_plural_orgasm` function bodies. It verifies that effects 13 and 15 receive positive values, the behavior is cleared without talk, later proximity does not replay it, nearby display remains, excluded derivatives retain no `997`, and the existing group-discovery entry can draw without a stale plural-orgasm behavior.

`python buildconfig.py` completed successfully. Its unrelated generated PO and config-definition rewrites were excluded; upstream convention submits the source CSV and rebuilds configuration in CI.

## Runtime Evidence Setup

- Baseline runtime: `/tmp/erark-remote-plural-baseline-20260714`
- Candidate runtime: `/home/ubuntu/games/erArk-pr-remote-plural-orgasm`
- Candidate and baseline config: Tk (`web_draw = 0`), `debug = 0`, font size 21.
- Candidate and baseline source ref: `06fc59c1e71d092224375fc4a096b956aea2ad63`, with only the candidate's ten CSV markers differing.
- First explored save: slot 7 copied from the player workspace.
- Slot 7 metadata hash: `c63c3e3985c671da84f9a6ea95dda71c2650ef503f3537feabf19f0afcc6d143`.
- Slot 7 state hash: `4fc46c3260505fa14b6a8c86691f5b254333209a993e468a8c4e2071ecc7180f`.
- Python `random` seed: `99720260714`.
- NumPy seed and `PYTHONHASHSEED`: `936012906` (`99720260714 % 2**32`).
- Evidence launcher hash: `0354a18d5567ec49b5e54f369ce85b756329779687f75a60a45e6c500c5d419d`.
- Enabled mods in the upstream worktrees: none.

The slot 7 baseline was replayed in real Tk from 21:17 through nine normal five-minute waits to 22:02. Every result frame was inspected and none showed remote plural-orgasm output or the later group-sex discovery panel. The save hashes remained unchanged because the run did not save. A subsequent read-only scan found no character in a relevant H state at the slot 7 save point, so these negative frames are excluded rather than presented as A/B evidence.

The same read-only predicate selected existing slot 99 as the next route. At 11:52 the player and ten NPCs, including Swire, are in the human-power room while those NPCs are running `masturebate`. Slot 99 contains one already-pending nearby `plural_orgasm_2`; this is useful only as the nearby-display control because a newly added configuration marker cannot retroactively change a queue stored in the save. Slot 99 source hashes are:

- Metadata: `6bcd68f4e9a14460206c7e29f61980c27d9b1fce41f25d03aa44dd40d44e59cf`.
- State: `534ba3960ebe29bb020cad68499b1622b9f8f4a54669dd4b79c49ed525b26b63`.

A read-only in-memory execution through the production behavior loop located a deterministic player route without changing either source save file:

1. Wait five minutes in the current group-sex scene, displaying and clearing the pre-existing nearby queue at 11:57. Clear the remaining saved settlement pages, then choose option 5 when Closure discovers the group-sex scene; this ends group sex and returns to normal play at 12:02.
2. Move normally to the power-area inner corridor, reaching it at 12:04. Normal map movement consumes two minutes; the earlier direct-state simulation omitted this and its 12:27 prediction was rejected.
3. Wait five minutes five times, reaching 12:29. A production-function trace through the corrected normal-movement route records fresh remote `plural_orgasm_2` admissions for Lin and Jingzhe in the Columbia cafe and Theresa in the Seven Cities restaurant while the player remains in the inner corridor.
4. Move normally to the Columbia cafe, reaching it at 12:42. The baseline queues for Lin and Jingzhe remain pending because both are in 30-minute `eat` behaviors; proximity alone does not complete those behaviors.
5. Wait five minutes three more times. Lin's behavior started at 12:26 and completes during the third wait at 12:57, which is the first point at which the baseline can display the delayed remote plural-orgasm talk. On the candidate, `997` should have settled and cleared the new queue remotely at 12:29, so the matched 12:57 result must not contain that talk.

Two real-Tk runs that stopped at arrival and after one cafe wait correctly produced no delayed talk and are retained only as diagnostics. The corrected route was then replayed independently on the pristine baseline and candidate. At 12:57 the baseline displayed `小满双重绝顶`, while the candidate returned to the same cafe scene without delayed plural-orgasm output; both sides still displayed the saved nearby `凯尔希阴道小绝顶` control at 11:57.

The final production-boundary Fable review accepted the ten-row `997` cause and scope, accepted removal of only the 21-pixel window-manager title bar from the preserved baseline outer-window image, and directed that the 211-line AST-based regression remain local-only evidence because upstream has no pytest suite or CI entry for it. It initially withheld the main A/B narrative because the prior logic trace named Lin and Jingzhe while the visible baseline line named Xiaoman.

A transparent baseline launcher then recorded real production `generated`, `effect`, and `talk` calls without changing the save, queue, values, or random sources. Its durable 12:29 snapshot has 31 lines and SHA-256 `05f18e870ef26d1259614f5f7a9e536c5590699332b0f69dadf8de7ae435bd55`. It records Xiaoman (cid 4122) receiving `plural_orgasm_2` in the Columbia cafe at 12:29 while the player is in the power-area inner corridor; Xiaoman's current `eat` behavior started at 12:26 and lasts 30 minutes. The instrumented run later reached the cafe at 12:42, but its one-hour allocator supervisor expired before the 12:57 talk. The visible 12:57 baseline frame and the admission trace therefore come from two independent runs with the same save, seed, geometry, and route; they must not be described as one session.

Fable-5's final verdict is `ACCEPT`. It judged the identity concern closed because the durable admission record, the behavior completion time, and the discriminating 997-only A/B together exclude a newly generated local orgasm as the source of the 12:57 line. It chose a CSV-only submission boundary; the 211-line regression remains local evidence. The exact final prompt and verbatim verdict are preserved in `fable-final-prompt.md` and `fable-final-verdict.md`, and the PR text as submitted in #215 is sourced from `pr-draft.md`.

## Post-review scope correction

The user's review identified that the first local-review-ready draft defined the bug through the Xiaoman cafe reproduction rather than through the actual affected rule. The implementation boundary did not change: every `plural_orgasm_2` through `plural_orgasm_11` admission is affected whenever it is generated away from the player, regardless of NPC, location, player action, or gameplay source. The stale behavior remains queued until that NPC later enters the player's vicinity and completes a behavior; the cafe wait is only one representative visible example.

Fable-5 rewrote the title and problem statement at the general rule level and moved Xiaoman/cafe entirely into the representative verification section. The exact prompt and output are preserved in `fable-scope-revision-prompt.md` and `fable-scope-revision.md`. The revised draft must pass a new fresh-context artifact audit before regaining `local-review-ready` status.

The subsequent fresh-context artifact audit returned `PASS` with `publication_state: local-review-ready`. It independently confirmed from the upstream base that the ten plural-orgasm behaviors share one generation and remote-settlement path without NPC, location, or gameplay-source restrictions; the draft's general scope is therefore supported by PR-visible implementation context. It also confirmed that the cafe wait appears only as a representative visual verification and that the draft does not expand to excluded orgasm derivatives.

Current local image files and hashes are:

- Preserved baseline outer window: `before-full-window.png`, 2100x1100, `eca0c5f72011bd9c71062b3829bc01d6d58d4359884f49036fe17a471adafab7`.
- Baseline native Tk client area after removing only the 21-pixel window-manager title bar: `before.png`, 2100x1079, `12d663a7734b51418a8571bbd93c0447a6f3d9ba543b1bf64a8cba980faccd0d`.
- Candidate native Tk client area: `after.png`, 2100x1079, `3b9aca0c7dc455ccdfc23f7bf2f09ad909235aa73bb5622c513e672495deb07a`.
- Nearby baseline control: `nearby-before.png`, `03cd9dcb5e675b31efbd5727dd975a862b65fb6dc54d3ef21c3d641fd3a53131`.
- Nearby candidate control: `nearby-after.png`, `00f5d13c45e2fd43a8a9612dbaa9c70e0de06abf1800cf0ca3acf495708bc2e5`.

## PR #215 submission record (2026-07-14)

PR #215 is OPEN, non-draft, unmerged, and has no reviews or comments. URL: https://github.com/Godofcong-1/erArk/pull/215. Its head is `364ac6d9f`; the sole production diff is `Behavior_Effect.csv`, with `plural_orgasm_2` through `plural_orgasm_11` each gaining `997` (10 additions / 10 deletions). The PR base is `abebf33b` and live master is `3a1c9e620`; the CSV blob is identical on both and on the candidate parent, and merge-tree against current master is clean.

CI built configuration and cache, ran PyInstaller, completed all packaging, and uploaded the artifact. Only Create Release failed with `Resource not accessible by integration`; this is a fork-PR token release-permission limitation, not a failure caused by this diff.

At submission review time, no durable post-4.4 record of player semantic confirmation or per-item outward authorization was found. No further outward action on #215 was permitted until that gap was raised with the player; the next section records its resolution.

## Player confirmation and current status (2026-07-14)

The player reviewed the handoff and live PR summary, accepted PR #215 as implementation-complete, and instructed that the current upstream PR and its remote silent-settlement semantics be retained. This resolves the confirmation gap recorded above; no rollback or other corrective action is requested.

The implementation, verification, evidence, and public PR are complete, while PR #215 remains OPEN and unmerged. There is no actionable work in this change. The earlier label `open-upstream-tracking` describes a passive external state; it does not authorize polling, repeated verification, or continued implementation.

Future conditions are triggers for new bounded work, not pending tasks here. On an explicit user request for current status, refresh the PR once using read-only access and stop. A future authorized PR update or merge preparation may require a fresh merge-tree and CSV-blob comparison. After #215 is verified MERGED, separately authorized retirement must be created as a new cleanup task. Any edit, push, comment, close, publication, or cleanup action still requires fresh authorization.
