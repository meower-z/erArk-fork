## 0. Supersede the Rejected Experiment

- [x] 0.1 Preserve the 2026-07-10 global-wrapper and premise experiment as rejected investigation history in `implementation-notes.md`
- [x] 0.2 Remove the rejected five-file hidden-session teardown candidate from consideration
- [x] 0.3 Confirm that a later different eligible witness remains allowed and that PR #206 owns only the same-witness-before-movement rule

## 1. Prove and Implement Settlement Ownership

- [x] 1.1 Trace the NPC state-machine caller and direct hidden-discovery caller and prove why neither caller can be the sole settlement owner
- [x] 1.2 Put all explicit discoverer reactions through one panel-owned synchronous settlement helper (superseded by 1.9)
- [x] 1.3 Return a settlement flag through the NPC state-machine path and skip only the reaction already consumed by the panel
- [x] 1.4 Preserve the existing outer settlement for the production `MOVE` follow-up while keeping the direct caller's no-NPC-round boundary
- [x] 1.5 Keep player group-conversion or interruption follow-ups after the discoverer reaction
- [x] 1.6 Replace the custom result protocol with a boolean flag and one local `MOVE` case while preserving both caller boundaries (superseded by 1.9)
- [x] 1.7 Re-evaluate the final diff under the `3a - b` rule and retain only a strictly lower-penalty, logically equivalent implementation
- [x] 1.8 Recount only non-blank lines and restore project-normal formatting without changing the boolean settlement boundary
- [x] 1.9 Replace the unified helper with explicit per-case settlement and set the outer-skip result only in the four non-`MOVE` cases
- [x] 1.10 Skip a no-route `WAIT` successor after the visible discovery response while preserving same-round settlement of a real `MOVE`

## 2. Verify the Retained Candidate

- [x] 2.1 Run the focused behavior matrix covering both production callers, explicit and no-explicit choices, follow-up ordering, the `MOVE` case, and later different-witness behavior
- [x] 2.2 Retain the user-approved clean static Tk A/B for the standalone settlement bug and prove both crops are pixel-identical to their raw Tk frames
- [x] 2.3 Reuse the user-approved clean static A/B and generate the two-PNG PR draft with Fable 5 at high effort; the user explicitly waived the fresh independent artifact review after two no-verdict attempts
- [x] 2.4 Confirm that no upstream PR or remote discovery-settlement branch already owns this work
- [x] 2.5 Keep the one-image same-NPC hard gate scoped to repeated-discovery PRs; use the accepted A/B for this separately approved settlement scope
- [x] 2.6 Re-run the 28-case behavior matrix, recount non-blank lines, and review the final ad-hoc diff against the accepted boundary
- [x] 2.7 Replay the approved Tk route on PR #218's exact base/head, compare the observed frames with the two images already in the PR, and record the result without editing the PR

## 3. Publication

- [x] 3.1 Obtain separate user authorization to publish compliant, approved evidence and replace the PR-draft URL placeholder
- [x] 3.2 Obtain separate user authorization to push the candidate branch
- [x] 3.3 Obtain separate user authorization to open the upstream PR

## 4. Maintainer-requested `SPECIAL_FLAG` revision

- [x] 4.1 Create an isolated candidate from current `upstream/master` and preserve the return contract of `constant.handle_state_machine_data`
- [x] 4.2 Replace the return pass-through with the explicit per-case panel marker, delayed `SPECIAL_FLAG` write, and one-round scheduler consumption
- [x] 4.3 Rebuild and run a focused red-capable behavior matrix; recount the final production penalty and obtain a fresh code review
- [x] 4.4 Run a fresh deterministic real-Tk before/after replay, inspect and archive the evidence, without changing the upstream PR

## 归档收尾（2026-07-17）

本 change 已完结并归档：对应上游 PR #218「修复「H中被发现」面板中发现者反应漏结算与重复结算的问题」已合并（上游提交 1b8b8555b），并已包含维护者要求的 SPECIAL_FLAG 改版（tasks.md 第 4 节）。发现者反应「恰好结算一次」的归属修复已交付上游，目录仅作历史记录保留。
