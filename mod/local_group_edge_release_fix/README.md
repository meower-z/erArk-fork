# 本地群交寸止释放修复

## 症状

群交参与者在体力耗尽、群交转单人H、无意识恢复或群交结束时，待释放寸止计数可能在模板或H状态清理前丢失，导致寸止绝顶没有结算。

## 根因

寸止计数属于参与者H状态，但多个退出路径会先移除群交上下文，再进入普通结算。需要在这些清理动作之前同步释放计数并结算释放产生的二段行为。

## 修复范围

- 替换 `Script.Design.handle_npc_ai.judge_character_tired_sleep`。
- 替换 `Script.Design.handle_npc_ai_in_h.recover_from_unconscious_h`。
- 运行时包裹行为效果 `528` 和 `529`。
- 群交转单人H时释放离开群交上下文的角色。
- 无意识恢复和群交结束前释放仍在群交上下文中的参与者。
- 批处理中的绝顶结算会通过 `local_h_orgasm_batch_fix_is_settling` 跳过疲劳睡眠重判。
- 疲劳参与者的行为中补结算仅在原逻辑事后确实分配了 `GROUP_SEX_NPC_HP_0_END` 时触发（2026-07-06 加深：事前条件会对未获新行为的疲劳跟随者造成多余结算）。

## 有意保留与已知限制（2026-07-06 审计裁定）

- **离场自结束H的清理仅清理**：不在玩家场景的寸止NPC被上游判定自行结束H（`handle_npc_ai_in_h` 对离场NPC设 `END_H` 且目标为自身）时，其待释放计数随状态重置清零、不做结算。与"过期模板参与者仅清理"的处理一致：离开玩家上下文的角色不产生可见结算。
- **监制波次与≥3次奖励已迁移**：旧单体mod的按波次释放与≥3次释放的奖励绝顶并未丢失，而是移交给绝顶批处理的 `climax_count >= 3` 路径；由 `test_real_h_orgasm_batch_release_preserves_multi_count_edges` 与 `..._preserves_three_count_bonus` 固定（审计核对结论）。

## 依赖

依赖 `local_h_orgasm_batch_fix`，用于查询绝顶批处理状态并避免释放流程打断批处理。

## 验证

```bash
python mod/local_group_edge_release_fix/tests/test_local_group_edge_release_fix_mod.py
```

## BDD待补充

后续BDD场景需要覆盖一名NPC离开群交、群交转单人H、无意识恢复、群交结束、模板参与者已过期和睡眠路径不泄漏寸止计数。
