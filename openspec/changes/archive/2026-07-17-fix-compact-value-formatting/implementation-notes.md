## Production caller inventory (corrected 2026-07-14)

Repository-wide search found two distinct settlement display rules. They must not be described as one shared path:

| Owner | Production expression | Display contract | T3 scope |
| --- | --- | --- | --- |
| Acting character state | `attr_text.get_value_text(int(change_data.status_data[status_id]))` | Compact signed value | In scope |
| Acting character experience | `attr_text.get_value_text(int(change_data.experience[experience_id]))` | Compact signed value | In scope |
| Interaction target state | `text_handle.number_to_symbol_string(int(target_change.status_data[status_id]))` | Exact signed value | Out of scope; preserve |
| Interaction target experience | `text_handle.number_to_symbol_string(int(target_change.experience[experience_id]))` | Exact signed value | Out of scope; preserve |
| Interaction target HP, MP, favorability, trust, hypnosis | `text_handle.number_to_symbol_string(...)` | Exact signed value or percentage | Out of scope; preserve |
| Local orgasm-batch status output | `attr_text.get_value_text(...)` in the private mod | Compact signed value | Compatibility check only; no mod code enters the upstream candidate |

`tests/test_time_stop_release_settlement_output.py` is not a production caller. Web structured value collection transports numeric values separately and does not call the compact formatter. No formatter caller reads time-stop-specific state.

The earlier inventory incorrectly generalized the acting-character calls to the target half of the same panel. The prepared-save player route below exposed that omission. Fable ruled that the exact target display is valid upstream behavior, not another instance of the compact-suffix bug; T3 must not change it or unify the two presentation contracts.

## Candidate provenance and corrected contract

Fresh worktree `/home/ubuntu/games/erArk-pr-compact-value-formatting` started at untouched `upstream/master` `06fc59c1e` on `codex/fix-compact-value-formatting`. The original isolated commit was `cd28b2b21`.

Rebasing onto upstream `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5` produced `91939e9ad`. Its patch ID matched the original and its candidate files were byte-identical, proving that the rebase changed ancestry rather than adding the large production-path test. After that rebased commit was pushed, the user asked to remove `test_real_settlement_callers_keep_compact_self_and_exact_target_values` because its setup was too large for maintainer review. Amending the 93-line test deletion produced the final sibling commit `7fd521bb6d98fcaa0841cce79e6d82ecf9c04b82` with the same upstream parent. The fork branch was replaced using an exact expected-value lease: the update could proceed only while the remote still equaled the previously verified `91939e9ad`, so it would not overwrite an unexpected third-party change. The last verified fork head in this session was the final commit.

Local commit `0b3f1c1a9` mixed a formatter hunk with unrelated time-stop attribution work. T3 copied neither the commit nor its unrelated files. The isolated candidate changes only `Script/Design/attr_text.py` plus one submitted regression file.

Untouched upstream derives a suffix index from signed string length and then indexes a suffix list beginning with `K`. Direct calls therefore produce wrong groups such as:

```text
1000 -> +1M
-999 -> -M
-1000 -> -1M
999999 -> +999M
-999999 -> -G
1000000 -> +1G
-1000000 -> -1G
1000000000 -> +1T
-500 -> -M
```

Fable withdrew the earlier exception for values at or above one billion: it retained the same off-by-one defect and had no separate gameplay meaning. The approved contract newly defines integer truncation at the formatter entry, derives the group from absolute magnitude, applies the sign independently, and uses the existing suffix list at every supported magnitude. Required boundaries are:

```text
±999 -> ±999
±1000 -> ±1K
±999999 -> ±999K
±1000000 -> ±1M
±999999999 -> ±999M
±1000000000 -> ±1G
```

Fractional inputs are newly defined to truncate at entry (`999.9 -> +999`). This changes the direct helper's former sub-thousand decimal behavior, but both production settlement call sites already wrap their values in `int(...)`, so it does not change production display or settlement semantics.

## Production-path verification

The submitted regression contains a 12-point signed boundary matrix plus fractional truncation checks and loads the formatter source directly. It is intentionally small enough to review beside the production change.

Before publication, a larger local-only subprocess probe initialized the compiled game configuration, created a real `CharacterStatusChange`, and called the production `handle_settle_behavior()` text assembly. Its acting-character state and experience values of `2025` both rendered as `+2K`; a target state value of `2025` remained `+2025`. The probe replaced only the behavior-effect producer and final rich-text sink, exercised the real assembly and record classes, and did not alter stored values. It established scope during investigation but was removed from both PR code and PR text under the reviewer-sized test rule.

## Supporting injected Tk evidence

An earlier matched real-Tk pair called the real core settlement entry with an injected fixed `CharacterStatusChange`. It visibly demonstrated upstream wrong suffixes and candidate corrected suffixes, but Fable ruled it ineligible as final PR evidence because the run itself constructed gameplay state rather than starting from a prepared save and written player route. It remains supporting renderer evidence only:

- `/tmp/erark-pr-evidence/compact-value-formatting/final/baseline.png`, SHA-256 `aceb62e15792402e488611af99d004c169c27b12facd14781f5a556f412ba8cc`
- `/tmp/erark-pr-evidence/compact-value-formatting/final/candidate.png`, SHA-256 `4b2c9f93c8c421078a2a508a8cae8e7310edcb1c45dae42bc4cd12c05748f1f1`

Those frames cannot satisfy task 2.3. The listed `/tmp` locations are historical capture paths and were later removed; this supporting pair was not part of the retained PR #217 archive.

## Prepared-save target-path counterexample

A compliant player route used byte-identical prepared saves in untouched upstream and the candidate:

- Save SHA-256: `67d81ba0205e84cccc80ddcb58f106cb76f1eded634e3e7b6d92cfa0571dde38`.
- Preparation placed the player and Kal'tsit in the same dormitory, set Kal'tsit's desire to `50000`, kept every pleasure state at zero, and left her in a normal interactive state.
- Written route: load slot 0, enter command `5003` (`摸胸`), inspect the requirement panel (`需要性爱实行值至少为200`, current value `1635`), then confirm the action.
- One allocator-supervised controller ran baseline and candidate sequentially on display `:25`, slot 0, with the same launcher seed and one inspected screenshot after every input.

Both final screens were byte-identical and displayed target desire as `+2025`:

- Baseline: `/tmp/erark-pr-evidence/compact-value-formatting/player-flow/baseline/frames/11-confirm-touch-breast.png`, SHA-256 `dbabdf7a730b21098ada1cf7a8e9eab6f1483fe5fd6d7889e41e1c887f3f17e6`
- Candidate: `/tmp/erark-pr-evidence/compact-value-formatting/player-flow/candidate/frames/11-confirm-touch-breast.png`, SHA-256 `dbabdf7a730b21098ada1cf7a8e9eab6f1483fe5fd6d7889e41e1c887f3f17e6`

This pair invalidated the earlier caller inventory and proved that T3 preserves the target's exact-value contract. It is negative scope evidence, not the final visual proof of the formatter fix. The listed `/tmp` locations are historical capture paths and were later removed; the findings and hashes remain the durable record.

The controller exited normally and allocator slot 0 was released. An unrelated session owned slot 1 and was not touched.

## Candidate verification after Fable's corrected ruling

The current candidate contains one 10-line replacement in `Script/Design/attr_text.py` and one focused test file. No time-stop, target-display, settlement-owner, Web, mod, generated-data, or prepared-save file is in the candidate diff.

Final verification on `/home/ubuntu/games/erArk-pr-compact-value-formatting`:

- `pytest -q tests/test_compact_value_formatting.py` -> `14 passed in 0.06s`
- `python -m py_compile Script/Design/attr_text.py tests/test_compact_value_formatting.py` -> passed
- `git diff --check` -> passed

The generated PO changes produced while launching the game were restored and are absent from the candidate diff.

## Final prepared-save positive Tk evidence

A second prepared save put the player and Kal'tsit in the ordinary multimedia room. The player was in a normal state with technique level 10 and current learn state 50000; Kal'tsit was also in a normal interactive state. Both runtimes received byte-identical metadata and data files:

- Metadata SHA-256: `86af8eac74202ffc3f23e19b99c270eb3f952bbdb4a6d2248f768cff3183bebb`
- Data SHA-256: `ce39fecccf2439cf81a41861b4d75879d2548d8460e56f179e0d0d5f5420ab39`

The written route was: load slot 0, return to the ordinary interaction screen, enter command `3008` (`看电影`), and submit once. Baseline and candidate received the same ten physical inputs under Python/NumPy seed and `PYTHONHASHSEED` `20260714`.

The pre-action frames are byte-identical (SHA-256 `58e1a0fdfff7650c013ae4d5b6e2a76bba5085a109496a36d2f4202de57671c3`). They show the same room, player and target values, and available `3008 看电影` command. The inspected final frames are retained locally at:

- Baseline: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-217/local/fix-compact-value-formatting/evidence/baseline/frames/10-submit-watch-movie.png`, SHA-256 `2f86df157d0bb0198d8d06ab0d10ecf7a7fb5f0fac9d51944b311230c3c1cf0e`
- Candidate: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-217/local/fix-compact-value-formatting/evidence/candidate/frames/10-submit-watch-movie.png`, SHA-256 `a22e148ad7ba657f0999e7366ef0d2d0bcc360331d9f47ae076f9bf72aeefd3b`

Untouched upstream visibly reports the acting player's learn change as `习得 +3M`; the candidate reports `习得 +3K`. The target's exact-number fields remain identical on both sides: `好感 +852`, `信赖 +9.06%`, and `好意 +666 (lv0->2)`. Player costs, action prose, experience gain, and elapsed-time text also match. Only 143 pixels differ across the full `2100x1079` frames.

The initial route estimate of `+2400` did not include every normal difficulty and character-progress adjustment. The actual deterministic route lands in the three-thousand range on both sides. This strengthens rather than changes the contract under test: the stored settlement is the same and only the baseline's wrong `M` suffix becomes the candidate's correct `K` suffix.

The allocator ran baseline and candidate sequentially on display `:25`, slot 0, under supervisor `479859`, controller `479870`, baseline game `479874`, and candidate game `482435`. The chronological action log and replay package are archived under `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-217/local/fix-compact-value-formatting/`. Slot 0 was confirmed free afterward; an unrelated slot 1 owner was not touched. The task-owned runtime, capture, and assets-clone paths under `/tmp` were deleted only after the archive was verified.

Fable gave the evidence, corrected OpenSpec documents, code boundary, and final PR prose a PASS after requiring two factual documentation corrections and one screenshot/probe wording separation. The first independent PR-artifact review required one surgical deletion because the verification paragraph introduced target behavior outside the draft's earlier scope. Fable made only that deletion. A second fresh-context review returned `PASS`, `publication_state: local-review-ready`, with no required or optional prose changes. After the commit-pinned public images replaced local placeholders, a final fresh review returned `PASS`, `publication_state: publication-ready`.

## Publication closure

- Upstream PR: `https://github.com/Godofcong-1/erArk/pull/217`, opened ready rather than draft, title `修正：自身状态与经验结算数值的缩写单位错误`.
- Base: `Godofcong-1/erArk:master`; base commit at creation: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`.
- Head: `meower-z:codex/fix-compact-value-formatting`; final commit: `7fd521bb6d98fcaa0841cce79e6d82ecf9c04b82`.
- Public evidence asset commit: `2334724784041c99e9adc498c08f6fa9b29e4c25`.
- Before image: `https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/before-watch-movie.png`.
- After image: `https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/after-watch-movie.png`.
- Both public URLs were verified as HTTP 200 `image/png`, without `Content-Disposition`, and their hashes matched the inspected originals.
- The final PR has one commit and two files: a 10-line formatter replacement and a 50-line focused regression file. The large production-settlement test is absent from both code and PR text.
- At the last automated status read before the stop instruction, `build-windows` was still in progress and GitHub reported mergeable state `unstable`; this was not a verified failure. Per the user's instruction, no later status was fetched and no monitoring continues.
- The user reviewed and approved the final diff and PR draft, then authorized opening the PR. The user has now confirmed that PR #217 is open and explicitly requires no further PR edits, checks monitoring, pushes, or publication actions in this session.
