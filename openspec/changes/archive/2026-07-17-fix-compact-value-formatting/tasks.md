## 1. Isolate and prove the formatter defect

- [x] 1.1 Enumerate every production `get_value_text()` caller, separately inventory the target-side exact-number calls in the same panel, and record which display contract owns each field
- [x] 1.2 Run the focused boundary matrix against untouched `upstream/master` and the existing local candidate, proving exact red/green output through the `1000000000` boundary and signed counterparts including `-500`
- [x] 1.3 Extract the formatter-only hunk from local commit `0b3f1c1a9` into a fresh linked worktree based on current `upstream/master`, excluding time-stop attribution and waiting-protocol changes

## 2. Verify presentation-only behavior

- [x] 2.1 Add small submitted tests for the signed boundary contract and fractional truncation; keep the larger production settlement assembly probe local-only
- [x] 2.2 Run representative acting-character state and experience callers plus the local batch compatibility probe, confirming that target settlement remains exact and stored values are unchanged
- [x] 2.3 Capture and inspect one matched real-Tk before/after case from the same prepared save and written player route, whose wrong suffix is understandable without local investigation context

## 3. Review and prepare the local PR package

- [x] 3.1 Re-open the exact candidate diff and remove every line unrelated to the shared formatter contract
- [x] 3.2 Run focused tests, relevant existing regressions, `py_compile`, and `git diff --check`, recording any skipped verification
- [x] 3.3 Give the exact proposal, design, spec, tasks, diff, and inspected evidence to Fable for documentation/PR-text review, then pass `review-erark-pr-artifacts`
- [x] 3.4 Publish the approved commit-pinned screenshots, update the reviewed fork branch, open upstream PR #217 as ready, and stop all further PR operations at the user's instruction

## 归档收尾（2026-07-17）

本 change 已完结并归档：对应上游 PR #217「修正：自身状态与经验结算数值的缩写单位错误」已合并（上游提交 dd7dfaa7f）。共享紧凑数值格式化的符号/单位修正已交付上游，目录仅作历史记录保留。
