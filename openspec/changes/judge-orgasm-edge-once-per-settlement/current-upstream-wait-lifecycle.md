# Current-upstream first-wait lifecycle map

## Attempt 8 correction

Attempt 8 did not show that its empty Return failed to submit. It exited one `WaitDraw` and immediately reached a later wait in the same outer update. Its two frames were not enough to identify the full sequence, and the earlier statement that the first page was the final player settlement pause was wrong.

## Bounded attempt 9

Attempt 9 ran unchanged current upstream `72e28051ebaaabb069d06059b4633fda90b0b621` with real Tk, pristine save 99, seed 0, and `PYTHONHASHSEED=0`. An evidence-only wrapper logged every `flow_handle.askfor_wait()` entry and exit with its production call stack, plus the first outer wait's entry/exit. Wrapper installation preserved Python and NumPy RNG fingerprints exactly.

The visual agent submitted exactly one `[6001]`, inspected every full-resolution page, and sent one empty Return only after recognizing an ordinary wait page. The trace recorded these nine completed waits:

1. `talk.second_behavior_info_text`: `凯尔希阴道小绝顶`;
2. `store_power_by_human_power`: its narration and 0.2 power;
3. `talk.second_behavior_info_text`: `凯尔希心理绝顶`;
4. `store_power_by_human_power`: its narration and 0.5 power;
5. `talk.second_behavior_info_text`: `凯尔希心理强绝顶`;
6. `store_power_by_human_power`: its narration and 1.0 power;
7. `talk.second_behavior_info_text`: `凯尔希双重绝顶`;
8. the player's `judge_character_status` result page, including `5分钟过去了`;
9. an NPC-phase `second_behavior_info_text` page containing 清流 settlement, `30分钟过去了`, 杜宾 action text, successful edging, and `杜宾肛肠绝顶寸止`.

After the ninth empty Return, wait 9 exited and the game displayed an `H中被发现` choice panel: Closure found the player's group sex, with choices `[1]`, `[4]`, and `[5]`. The contract declared any selection panel invalid, so no choice was sent. The trace contains `outer_wait_entry` 1 but no `outer_wait_exit` 1. No second `[6001]` or candidate code ran; save hashes remained unchanged.

The verified archive is `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/2026-07-15-orgasm-edge-first-wait-lifecycle-attempt9/`. It contains `RESULT.md`, `wait-sequence.md`, the call-stack trace, all inspected frames, action log, pristine save, probe/controller, and checksums. The disposable runtime, controller, and worktree were removed and the allocator was released.

## Consequence

One `[6001]` has a data-dependent sequence of ordinary wait pages and can then block on a normal gameplay choice panel before the outer update completes. A route that assumes one Return per command is invalid, but the first nine waits are now mapped and reproducible. The discovery panel is not itself evidence of failure; it was only outside attempt 9's predeclared scope.

Before another run, supervision must decide whether the next bounded route-discovery step may select the visible normal choice `[4]邀请对方加入群交` and continue mapping the same first outer wait. If allowed, the new contract must stop after the first `outer_wait_exit`, forbid a second `[6001]`, log every later wait/choice, and invalidate any choice panel other than the specifically predicted Closure panel or any failed/refused join outcome not fixed in advance.
