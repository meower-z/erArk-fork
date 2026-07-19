## 1. 催眠增强资格回归

- [x] 1.1 新增组件红测：先有一名 H 目标、再通过直接邀请加入第二名目标；两人 degree 均为 200、其中一人 `unconscious_h = 0` 时，按钮 premise 仍应通过
- [x] 1.2 新增执行红测：完全催眠但当前未激活催眠态的受邀参与者获得 `increase_body_sensitivity` 与 `pain_as_pleasure`，且 `unconscious_h` 原值不变
- [x] 1.3 修改 `group_sex_extension` 的资格收集，使完全催眠计数与主规格一致，不再额外过滤当前活跃催眠态

## 2. 全员自慰调度回归

- [x] 2.1 用插桩/实机状态确认 playtest 当时的 `npc_ai_type`；记录类型 1 与非类型 1 的预期差异，不把普通模式无自慰误判为 bug
- [x] 2.2 新增红测：AI 类型 1 下，已在群交模板中的初始与后续受邀参与者都在模板早退前获得一次 `masturebate = 3`
- [x] 2.3 调整 `npc_ai_in_group_sex` 判定顺序：保留 H/群交/束缚硬门禁，类型 1 优先生成自慰意图，其他类型继续使用模板成员早退
- [x] 2.4 集成 `local_group_masturbation_intent_fix` 回归：每角色每玩家行动只路由一次 `default91`，正式 `MASTUREBATE` duration 与玩家窗口一致，下一窗口可再次生成

## 3. 验证与文档

- [x] 3.1 近真实群交回归覆盖“先单人 H → 直接邀请第二人 → 全员催眠增强 → 切换全员自慰 → 等待 5 分钟”的完整状态与输出终态（驱动真实邀请回调/输出、场景移动原语、加入行为、模板、指令前提/执行、角色行为与结算；明确不声称驱动邀请列表点击或逐格旅行 UI）
- [x] 3.2 重跑 `group_sex_extension`、`local_group_masturbation_intent_fix`、split manifest 与存档 99 群交 AI 测试
- [x] 3.3 更新两个 mod README，说明完全催眠资格不要求当前激活态，以及 AI 类型 1 相对模板布局的优先级
- [x] 3.4 `openspec validate --strict` 与 `git diff --check` 通过
