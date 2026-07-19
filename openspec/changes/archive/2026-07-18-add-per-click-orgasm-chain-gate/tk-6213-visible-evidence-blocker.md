# T6 `[6213]体外子宫按摩` baseline exploration blocker

- Status: invalid as formal before/after evidence; baseline runtime contradicted the prior static AI probe.
- Source: upstream `72e28051ebaaabb069d06059b4633fda90b0b621`.
- Renderer: real Tk (`web_draw = 0`), debug evidence config, allocator owner `/root/t6_6213_tk_ab:explore`, slot 0, `DISPLAY=:42`, geometry `2100x1100x24`.
- Random controls: Python `random`, NumPy, and `PYTHONHASHSEED` all `20260715`; the observer is read-only.
- Input save: repository `save/99/{0,1}` copied as runtime `save/0/{0,1}`. Pre/post hashes remained `6bcd68f4e9a14460206c7e29f61980c27d9b1fce41f25d03aa44dd40d44e59cf` and `534ba3960ebe29bb020cad68499b1622b9f8f4a54669dd4b79c49ed525b26b63`.
- Trigger: load slot 0, enter `[6213]体外子宫按摩`, then advance all visible settlement pages one at a time.
- Real trigger trace: character 3 凯尔希 entered `orgasm_settle` with `normal_orgasm_dict` key 7 equal to `+1`; the visible summary showed `子宫快感 +425 (lv1→2)`, `子宫绝顶经验+1`, and `5分钟过去了`.
- Frozen discovery choice: first `H中被发现` panel named 可露希尔; options were `[1]用花言巧语支开对方`, `[4]邀请对方加入群交`, `[5]尴尬地结束H`; chose `[1]`. A later panel named 陈 and was stopped after typing the same choice, before Return.
- Contradiction: the prior static probe predicted that baseline 凯尔希 would receive a group-sex AI action and then an ordinary AI movement plan toward Penguin Logistics. The full real player route instead traced `npc_ai_in_group_sex` from `masturebate` to `share_blankly`, then `find_character_target` from `share_blankly` back to `share_blankly` with duration 1, state 2, and target 3. No `move` behavior or visible departure occurred for 凯尔希.
- Consequence: this route cannot produce the required human-readable baseline failure, so no candidate phase or formal A/B was run.
- Logs: `baseline-trace.jsonl` SHA-256 `2da4e8784d8d01e750e5053a61b2f83960c815d435a2c96da8b0041954f16da7`; `action-log.tsv` SHA-256 `2f4db7966bb659cd0914d7761e165baa436a7c5316b1df7a4c9c6c645aba26ec`.
- Observer hashes: launcher `7aef58b832681223740e132aa467704fbc6c3d0ea6defdb26aa3d7ecba7e9a54`, evidence entry `caabba9aa9a71ce2038b2b6d015518009de73d440518044a19e9993ada20911c`, observer `7b0c86c9c1e95c2250628148f31eb5aeb94ce34abf648a377780efb10e5d4419`.
- Runtime logs contained no `Traceback`, `Exception`, `TclError`, `ERROR`, or game-initialization failure.
- Cleanup: allocator released all three slots; all known controller, game, Xvfb and supervisor PIDs were gone. The disposable linked runtime and registration were removed, save hashes remained unchanged, and no formal evidence archive was created.
