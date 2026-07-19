## Current candidate

- Base: `upstream/master` at `72e28051ebaaabb069d06059b4633fda90b0b621`.
- Worktree: `/home/ubuntu/games/erArk-pr-time-stop-release-attribution-current`.
- Production scope: one effect-527 hunk in `Script/Settle/default.py`; compact formatting, waiting protocol, generic second-stage guards, and local mod code are excluded.
- Zero-count behavior is intentionally preserved. `time_stop_release` remains true and the original no-op call still occurs because the flag is read by talk selection, unconscious experience conversion, and later second-behavior logic.

## Real-loader red and green evidence

The probe loads the real `Script.Settle` registry, real effect 527, real `Character` structures, real `second_behavior.orgasm_settle`, and real Web value collector. It does not extract the function with AST or replace orgasm settlement with a fake. It directly sets `shoot_position_body = 2` as a code-level trigger that makes `orgasm_settle` write a distinguishable synchronous value to the supplied change object. This proves routing at the effect boundary, not normal player reachability.

On untouched upstream, one NPC with one deferred skin orgasm and `shoot_position_body = 2` produced:

```text
root_exp_111 1
target_ids []
npc_exp_111 1
queued ['s_orgasm_small']
counter 0
release True
```

The NPC's actual experience and queued behavior changed, but its experience record landed on the player's root object.

With the attribution candidate, the same setup produced:

```text
root_exp_111 0
target_ids [1]
target_exp_111 1
npc_exp_111 1
queued ['s_orgasm_small']
counter 0
release True
```

`tests/test_time_stop_release_attribution.py` packages the probe as a subprocess test and covers zero, one, two, and remote NPC cases. A thin tracing wrapper records object identity and then calls the real orgasm function. It verifies actual stored experience, that one injected unrelated queue item remains present immediately after effect 527, zero/nonzero cleanup of body semen, clothing semen and stolen clothes, and Web collection under NPC IDs without using `settlement_input`. It does not execute or characterize the later generic pass.

The local focused test failed on untouched upstream and passed on the candidate:

```text
upstream: owner_identity was false for a positive release and the experience record remained on the root object
candidate: 1 passed in 0.71s
```

`python -m py_compile` and `git diff --check` also pass.

## Local batch-mod compatibility smoke

The unpublished `local_h_orgasm_batch_fix` was supplied as a local overlay and loaded through the real `ModManager` against the isolated attribution candidate. One remote NPC had one positive deferred skin-orgasm count plus an unrelated queued behavior. The first harness attempt exposed only a missing synthetic scene entry; after supplying two ordinary scene objects, the real mod load and settlement completed:

```text
mod_errors []
orgasm_module mod_local_h_orgasm_batch_fix
root_exp_111 0
target_ids [1]
target_exp_111 1
npc_exp_111 1
marker {1: {'s_orgasm_small'}}
unrelated_queued 1
counter 0
```

This proves the local mod accepts the direct `TargetChange`, stores its synchronous-consumption marker on that same NPC object, and leaves unrelated queued work intact at effect 527. It does not claim to verify how the later generic pass settles that queue. No mod code is included in the upstream candidate, and no compatibility edit was required.

## Historical Fable scope ruling

Before the matched Tk route was completed, Fable's code/spec ruling was `CODE PASS / DOCS NARROW`: the production hunk remained limited to effect 527's synchronous ownership, while follow-up generic settlement, remote silent settlement, and射精位置 lifetime stayed outside this change. The registry test was sufficient for that code boundary after its helper docstring was fixed.

That ruling revoked the earlier one-NPC Tk route. `judge_before_pl_behavior()` clears the current target's `shoot_position_body` before effect 527, while all non-shoot-position orgasm effects are queued and use a target block in both baseline and candidate. Therefore the one-NPC release could not display the ownership difference. It required a multi-target route that preserved NPC A's positive deferred counts and qualifying射精位置 after switching the current target to NPC B; the later attempt-11 route below satisfied that requirement.

## Multi-target route checkpoint

A normal-UI exploration from `save/8` proved the required state is reachable without injection. Four oral actions against Lin (4080), with the fourth choosing the normally presented ejaculation option, produced deferred counts `{0: 1, 21: 2}` and `shoot_position_body = 2`. Clicking Jingzhe (306) in the visible current-scene character list changed only `target_id`: a post-switch observer retained Lin's complete trigger object byte-for-byte, and `[4115]` remained visibly available. The exploration stopped before release and therefore is route evidence only, not a baseline result.

Fable returned `FORMAL ROUTE PASS` and froze the current-upstream matched replay: Lin is A, Jingzhe is B, the fourth oral action must present and use the ejaculation option, and both sides must reach the exact post-switch gate before `[4115]`. The formal replay uses the shorter matched viewport sequence approved by Fable and must be discarded if either side differs in action count, trigger state, target, time-stop/H state, or fourth-action prompt. This endpoint was later superseded as recorded below.

## Accepted matched Tk A/B (2026-07-15)

Attempts before 11 remain invalid diagnostic history and are not PR evidence. Attempt 11 used one supervised baseline/candidate command, the same normal checkpoint, seed controls, geometry and frozen physical inputs. All 31 corresponding pre-result frames (`b00..b30` and `c00..c30`) are byte-identical; two state samples on each side match, the save hash is unchanged, and neither log contains a traceback, exception or Tcl error.

The full-resolution baseline result visibly gives the Doctor `无意识绝顶经验+1` and `饮精绝顶经验+1`, while Lin receives `无意识绝顶经验+2`. The candidate removes the Doctor block and gives Lin `无意识绝顶经验+3` and `饮精绝顶经验+1`; the two experience points are conserved with no loss or duplication, and all other visible values are unchanged. The root agent independently reopened and inspected both archived images.

Archive: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/2026-07-15-time-stop-release-attribution-attempt11/`

- Baseline image: `baseline/frames/b31-final.png`, SHA-256 `1fe03fa3bbd3fe939795cb9579080e1e7ef53bb746dd04bda537b86b1f799e5f`
- Candidate image: `candidate/frames/c31-final.png`, SHA-256 `d8281a34eb7f3ab62152d56bcce880d1858879fc174bd4b189d26ec9fa968646`
- Manifest: `manifest.md`, SHA-256 `c84dc8edab9694e7ea7a1646ca91dad473a97f4fffb9838aabdba0f3f5f98e25`
- Candidate production diff SHA-256: `8b55cbcf81d7f8b357779117a9f66c7a88205bdd67f2474163b3ae0aacbbb015`

The attempt-11 runtime, captures, observer/controller and allocator owner were removed after the archive hashes matched; all three capture slots were free. Invalid attempt 9/10 diagnostics remain local and excluded from PR-facing evidence.

## Final local readiness

The candidate is committed locally as `8257fee9e844fffee869ab6d25c279e63c4a439c` and changes only `Script/Settle/default.py` with `a=2`, `b=1`, `S=0`, `U=0`, penalty 3. The final focused real-loader test is `1 passed`; `py_compile` and `git diff --check` pass. The evidence test remains untracked and local-only.

Fable's combined evidence/docs/code call produced no output before the 300-second timeout. Under the user's explicit fallback authorization, a fresh-context reviewer returned `EVIDENCE PASS`, `CODE PASS`, then `DOCS PASS` after stale conditional wording was corrected. Fable high authored the Chinese PR draft and performed the one requested prose deletion. A second fresh-context artifact reviewer returned `PASS` with `publication_state: local-review-ready`.

The only remaining publication blocker is outward authorization: replace `{{BEFORE_IMAGE_URL}}` and `{{AFTER_IMAGE_URL}}` after an approved evidence upload, then push and create the PR only with separate approval. No image was published, no branch was pushed, and no PR was created.
