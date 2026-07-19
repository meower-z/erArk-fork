## 验证结论（2026-07-17）：已解决，建议归档

**判定：本 change 关心的"群体催眠授予后、清醒入群者苦痛快感化不生效"问题，在当前 `main` 上已解决，无需再改码。**

机制不是上游给结算路径打了补丁，而是 2026-07-16 fork→upstream 重构删除了施加 `unconscious_h ∈ {4,5,6,7}` 门槛的本地 mod `local_pain_as_pleasure_fix`。该 mod 目录仅剩孤立 `__pycache__`、无 `mod_info.json`，加载器（`Script/Core/mod_manager.py:88-90`）直接跳过 → mod 不再生效。门槛移除后，苦痛→快感转换由上游原版路径接管，而原版就是本 change 想要的 raw-flag 语义。

逐路径核对：

- **结算转换**：`Script/Settle/common_default.py:243`，条件 `state_id==17 and final_value>0 and handle_hypnosis_pain_as_pleasure(cid)`。该 premise（`Script/Design/handle_premise/handle_premise_arts.py:884`）只读原始 `character_data.hypnosis.pain_as_pleasure`，无任何无意识/睡眠门槛；且直接递归进 state 23（无 state-23 睡眠 guard），与本 change 的 raw-flag 生效 + "睡眠/无意识仍产生快感"刻意例外（2026-07-10 决策）完全一致。此文件与 upstream `97c35826e` 逐字节相同（`git diff` 为空）。
- **授予**：`mod/group_sex_extension/scripts/group_sex_extension.py:205-206` 的 `_set_hypnosis_boost()` 仍设 `pain_as_pleasure=True` 且不动 `unconscious_h`，清醒后加入者保持清醒且照常获得转换。
- **清除/生命周期**：`Script/Design/hypnosis_state.py:21` `clear_hypnosis_sub_states()` 置 `False`（对应已合并的 #213 线）。

上游 `0e6c85655` 只放宽了指令**释放前提**（`handle_instruct.py` 中 `T_UNCONSCIOUS_FLAG_7`→`TARGET_HAS_BEEN_COMPLETE_HYPNOSIS`），未触及结算路径——印证方向，但不是本问题的修复来源。直接效果 270/283/296/408 的包裹是被删本地 mod 的功能设想、非本 bug 症状，上游本就不经 `pain_as_pleasure` 转换它们，不在收尾范围。

残留缺失：无。下方原始任务清单保留作历史记录。

---

## 0. Pause State and Contract Gate

- [x] 0.1 Record the confirmed state gate root, historical spec conflict, full known path inventory, experimental code, formula/accounting gaps, and unexecuted test state in `implementation-notes.md`
- [x] 0.2 Write the raw-flag candidate, alias/direct-effect candidates, and regression cases; they remain unaccepted and unexecuted
- [x] 0.3 Ask the user to choose upstream state-23 guard preservation versus an explicit unconscious/sleep exception — decided 2026-07-10: intentional exception; pleasure posts even while asleep/unconscious
- [x] 0.4 Ask the user to choose actual applied delta versus requested-delta compatibility at the status cap — decided 2026-07-10: requested value, upstream-compatible
- [ ] 0.5 After acceptance, reconcile this change with `openspec/specs/local-bugfixes/spec.md` and `fix-group-sex-invite-controls-and-idle-ai`

## 1. Audit Every Pain Route

- [ ] 1.1 Enumerate all positive and non-positive pain mutations, common aliases, direct effect registry entries, cancellation/reset paths, and later mod overrides
- [ ] 1.2 Trace discovered and directly invited participants through admission, group resolution, hypnosis boost, and pain settlement without hand-constructing the final state
- [ ] 1.3 Confirm the flag's UI and premise semantics and record the old dormant-state specification conflict
- [x] 1.4 Compare common conversion with upstream state-17 recursion, including the second consecutive-instruction adjustment, state-23 sleep/unconscious guard, cap, and both change-record owners — done 2026-07-10: line-by-line comparison against `common_default.base_chara_state_common_settle`; the missing second reduction was implemented (`_get_consecutive_instruct_adjust` + `apply_repeat_adjust`), the guard bypass is the accepted exception, cap recording matches upstream requested-value behavior
- [ ] 1.5 Verify each direct effect's own death/early-return behavior and full alias identity after supported mod load orders and repeated loading

## 2. Implement Flag-Driven Conversion

- [ ] 2.1 Make the raw granted flag the single activation predicate without mutating `unconscious_h`
- [ ] 2.2 Install the common conversion in default, second-effect, realtime, and item call paths and wrap direct effects 270, 283, 296, and 408
- [ ] 2.3 Preserve negative pain, dead guards, cancellation/reset clearing, and correct state-23 target-change accounting
- [x] 2.4 Split the independently reviewable core signed-delta routing and direct positive-pain effects into upstream PR [#212](https://github.com/Godofcong-1/erArk/pull/212); keep the remaining local-mod activation and lifecycle work in this change

## 3. Verify Connected Behavior

- [ ] 3.1 Add inactive-flag, cancel-then-pain, negative-pain, direct-effect, alias identity, and real target-change regressions
- [ ] 3.2 Add a connected later-participant regression from admission through boost to real common pain conversion while remaining conscious
- [ ] 3.3 After the full audit, run focused unit and near-real BDD suites, verify full mod load order, inspect the diff, and request permission before synchronizing maintained README/spec text outside this change
- [x] 3.4 Add cap/actual-delta 0 and 1 cases, sleep/unconscious cases, repeated-instruction equivalence, simultaneous change-object ownership, toggle/full-reset clearing, and per-entry death semantics — done 2026-07-10: `test_cap_keeps_requested_value_in_change_records` (both owners, requested value), `test_sleeping_or_unconscious_target_still_receives_converted_pleasure`, `test_repeated_instruction_applies_second_reduction_like_upstream` added and passing (14 component tests)
- [ ] 3.5 First connect the stable direct-invitation path from resolver through boost to real settlement; connect discovered admission only after the group ownership change is resolved
- [x] 3.6 Include the omitted death-delegation test in the direct `main()` runner or document pytest as the only complete runner before using the README command as evidence — done 2026-07-10: `test_dead_character_positive_pain_delegates_to_original` added to `main()`; direct runner and pytest both pass
