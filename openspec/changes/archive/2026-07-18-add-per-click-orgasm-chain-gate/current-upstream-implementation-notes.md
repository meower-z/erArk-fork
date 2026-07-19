# Current-upstream implementation notes

## Candidate identity

- Worktree: `/home/ubuntu/games/erArk-pr-per-click-orgasm-chain-gate`
- Branch: `codex/add-per-click-orgasm-chain-gate`
- Baseline: `upstream/master@72e28051ebaaabb069d06059b4633fda90b0b621`
- Production diff SHA-256: `2439b7c377872ee6a433a4a2c35eaea0b139958af77372707ec403f2a2e3a144`
- Production files: `Script/Design/update.py`, `second_behavior.py`, `handle_npc_ai.py`, `handle_npc_ai_in_h.py`
- Local-only regression: `tests/test_per_click_orgasm_chain_gate.py`; it is evidence in the candidate worktree, not part of the proposed production diff.

## Implemented boundary

`update.py` owns one module-private set for the active outermost click and exposes only NPC release registration and query operations. The outermost entry and `finally` clear the set; nested calls reuse it. `orgasm_settle()` registers an NPC only after the complete actual-release transaction. Ordinary and group type-1/type-2 AI query the same fact before creating a new action. The ordinary gate returns through the existing caller path, so `judge_character_status`, realtime, persistent, interrupt, time-over, talent and completion settlement still run.

No character, `Cache`, save format, cooldown, game-minute timer or type-3 dead path changed.

## Red and green proof

The final 16-test local suite on a fresh detached current-upstream source was `11 failed, 5 passed`. The same suite on the candidate was `16 passed`. The failures cover the missing actual-release registration, release-owner wiring, outer/nested lifecycle, ordinary and group admission and real completion-tail chain. Passing inverse cases cover the player, successful edging, time-stop accumulation, inactive-window writes, a second NPC, repeated registration, unregistered ordinary/group behavior and later passive orgasm settlement.

The test chain uses the real function bodies for both release owners, `orgasm_settle`, group admission, ordinary admission and `character_behavior`; peripheral rendering/config dependencies remain isolated. A separate game-order smoke initialized `Cache`, normal config and game config, then imported all four changed production modules successfully. `py_compile`, `git diff --check` and the 200-character added-line limit pass. Black is not installed in the available environment.

Both disposable baseline worktrees were removed after the red runs and their registrations verified absent. The game-order import created PO generation noise; the five exact generated files were restored to their prior clean `HEAD` state, leaving only the four intended production files and local tests dirty.

## Final score and review

After the hard style fixes, the production diff is `a=36`, `b=3`, `S=27`, `U=0`, penalty `66`. Fresh-context Standards and Spec review returned PASS with zero findings. No lower-penalty candidate was found that kept the two documented operations, module-private non-persistent state, outer-entry plus `finally` lifecycle, all three production owners and normal Chinese documentation.

Fable high design and code-review attempts each timed out after 300 seconds with no output; neither is counted as PASS. The player explicitly authorized self-direction when Fable is unavailable.

## Remaining gates

- Real Tk baseline/candidate evidence for one long player click and a following new click.
- Fable-authored Chinese PR title/body after evidence exists, or an explicit unavailable record under the player's fallback authorization.
- Fresh PR artifact audit over only the final production diff, public evidence and PR draft.
- User approval before any PR creation or other outward action.

## Tk route investigation

The first natural-save route, save 99 plus `[6001]等待五分钟`, is invalid. Its queued Kal'tsit orgasm text came from an earlier second behavior; the only newly traced `orgasm_settle` call had negative womb/vaginal callback values and no positive release. The exact diagnostic and cleanup are recorded in `tk-route-attempt6-invalid.md`. A Fable high route reassessment then timed out after 300 seconds with no verdict.

A bounded static real-loader investigation suggested a stronger normal route from save 99: click `[6213]体外子宫按摩` on the already selected Kal'tsit. Her womb pleasure advances from 498 at level 1 by 425 to 923 at level 2, producing a real `W=+1` release during player settlement. The same outer update then enters NPC scheduling under the player's group-AI type 1 policy. Its shortened probe predicted a later movement toward the Penguin Logistics safe house/out corridor, but that prediction was not valid player evidence.

Full real Tk with seed `20260715` proved the `W=+1` release and same-NPC re-entry, but contradicted the visible consequence: Kal'tsit entered group AI and ordinary AI, and both ultimately left her at `share_blankly`; she did not move or leave the scene. The shortened probe had used a different unstated seed, skipped full startup/save migration, and replaced talk handlers, so its RNG stream could not support a formal route. The exact real-Tk blocker is recorded in `tk-6213-visible-evidence-blocker.md`.

No exact full-startup seed is known that produces a human-readable baseline/candidate difference. The time-stop sibling remains excluded because it would mix this PR with T4's effect-527 attribution change. Under the skill's visible-evidence hard gate, upstream evidence work is stopped: the candidate remains local and uncommitted despite automated CODE PASS, and no PR prose or readiness claim is prepared.
