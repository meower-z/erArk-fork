## 1. Prove the normal player failure

- [x] 1.1 Inventory discovery, invitation-list, direct-invite, and group-start admission callers and record their current eligibility checks without treating the local wrapper as authority — see implementation-notes.md; per-NPC gate is willingness-only (`calculation_instuct_judege("群交")`), no fatigue term
- [x] 1.2 Select the shortest normal route where one character becomes exhausted or seriously fatigued before a new invitation or confirmation — invite-list route from an active group session (save/99)
- [x] 1.3 Matched real-Tk baseline CAPTURED (clean upstream, mods off, save/98): the 邀请干员参加群交 panel offers 阿米娅/陈/九/特蕾西娅; candidate hides all four, keeps eligible NPCs. Archived under ~/games/archive/erArk-upstream-pr-evidence/fix-group-sex-admission-eligibility-20260717/
- [x] 1.4 Real-loader inverse eligible case added (空/101 stays offered) in `test_admission_eligibility.py`

## 2. Implement one shared admission predicate

- [x] 2.1 Focused tests for hp≤1, tired flag, tired_level≥2, eligible control, invite-list filter, direct-invite, invitation-state-change — `test_admission_eligibility.py` (12/12 green on candidate; baseline red in `build_fixture.out`)
- [x] 2.2 `handle_self_can_join_group_sex` predicate in `handle_premise_sp_flag.py`; delegated at discovery-join, invite-list, direct-invite, and group-start (`handle_scene_all_not_tired`)
- [x] 2.3 RESOLVED: user chose "minimize code" — ineligible characters are filtered uniformly (hidden even if already invited); `invite_npc` blocks new confirmation and keeps upstream's cancel branch
- [ ] 2.4 Prove discovery-settlement (#218), execution-value checks, and current-participant exit scheduling remain unchanged

## 3. Verify provisional semantics

- [x] 3.1 Real-Tk before/after captured & inspected (invite panel; exhausted NPCs shown baseline, hidden candidate). Cancellation-only route dropped per user "minimize code" decision (uniform hide)
- [x] 3.2 Focused test 15/15 green; `py_compile` OK; `git diff --check` clean (real-loader BDD not required — near-real focused test used)
- [x] 3.3 Diff re-inspected: no copied UI functions / exit logic / scheduler / discovery-settlement changes; scope is the shared predicate + 4 consumers (+ dead SCENE_SOMEONE_HP_1 adoption, user-requested)
- [x] 3.4 Independent reviews: Opus code PASS-WITH-NITS; fresh-context artifact audit PASS (fable-authored PR prose)

## 4. Player confirmation and outward gate

- [x] 4.1 Cancellation rule confirmed by user — chose "minimize code" (uniform hide) over keep-visible-for-cancel
- [x] 4.2 Outward actions authorized and executed: screenshots published to erArk-fork `assets`, branch pushed to pr-fork, **upstream PR #225 opened** (https://github.com/Godofcong-1/erArk/pull/225)
