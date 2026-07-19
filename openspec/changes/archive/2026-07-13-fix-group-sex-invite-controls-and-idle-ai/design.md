## Context

### 全员催眠增强的规格/实现分歧

主规格 `group-sex-extension` 定义“完全催眠”为 talent 73 或 `hypnosis_degree >= 200`。运行时 `_get_complete_hypnosis_character_ids()` 除此之外还调用 `_is_active_hypnosis()`，要求 `sp_flag.unconscious_h in {4,5,6,7}`。因此 200% 只是永久催眠深度，若角色当前没有激活催眠态，就不会计入按钮 premise。

直接邀请路径 `group_sex_panel.invite_npc()` 只设置 `go_to_join_group_sex`、赋予邀请二段并执行移动；加入群交行为设置 H/群交相关状态，但没有“因催眠度达到 200% 自动激活 unconscious_h”的职责。于是“先单人 H，再邀请第二人”的来源差异可以让两个 200% 角色中只有一个仍处于活跃催眠态，按钮被静默隐藏。

这不是简单 UI 丢按钮，而是资格概念不一致：增强字段 `increase_body_sensitivity` 与 `pain_as_pleasure` 是可持久保留的催眠强化设置，命令本身又明确不得改变当前催眠状态，因此用“当前是否激活催眠态”作为可见门槛缺少规格依据。

### 群交自慰调度的早退顺序

`npc_ai_in_group_sex()` 当前先读取 `count_group_sex_character_list()`，若角色已在模板中便立即返回；“仅自慰/全员自慰”AI 类型 1 的分支位于该早退之后。结果是：

```text
受邀角色已进入群交模板
  -> template member early return
  X  never evaluates npc_ai_type_1
  X  never sets masturebate = 3
  X  local_group_masturbation_intent_fix has no marker to route
```

`local_group_masturbation_intent_fix` 只负责把已经生成的 `masturebate == 3` 路由到 `default91`，并保证每玩家行动至多一次；它不能补救上游根本没有生成意图。因此在 AI 类型 1 下，模板成员身份与“全员自慰”语义冲突。

另外，玩家等待 5 分钟属于一个原子行动窗口，NPC 结算文本在窗口执行过程中不一定逐分钟可见；“途中没有逐分钟文字”本身不是 bug。需要断言的是窗口结束时每名符合条件的参与者是否确实生成并结算了一次正式 `MASTUREBATE` 行为。

## Goals / Non-Goals

**Goals:**

- 200% 催眠度或 talent 73 的群交参与者，无论是初始进入还是后续直接邀请，都按同一规则计入全员催眠增强。
- “全员催眠增强”只设置强化字段，不隐式激活、切换或清除当前催眠态。
- 群交 AI 类型 1 明确覆盖模板成员身份：每个 H 中参与者在每玩家行动窗口生成至多一次自慰意图，并由既有补丁路由为正式行为。
- 用测试区分原子窗口的延迟显示与真正未结算行为。

**Non-Goals:**

- 不要求所有群交 AI 类型都让所有参与者自慰；本 change 的强制语义只针对类型 1。
- 不改变直接邀请的实行值、疲劳门禁、移动或群交模板布局。
- 不改变催眠深度增长、催眠类型选择或 `unconscious_h` 生命周期。

## Decisions

### 1. 完全催眠资格不再混入“当前激活态”

按钮 premise 与执行目标均以 `_is_complete_hypnosis` 为准：talent 73 或 degree >= 200。`unconscious_h` 只决定强化当前是否实际生效，不决定是否可以预先设置强化字段。

替代方案是邀请时自动恢复催眠态，但这会给邀请行为增加隐式控制效果，并与“命令不改变催眠状态”的既有契约冲突，因此否决。

### 2. 参与者来源统一由群交上下文解析器负责

继续复用 `_get_group_sex_character_ids()` 合并模板成员与当前场景 `is_h` NPC；测试必须加入“先单人 H、再直接邀请第二人”的来源组合，不能只用手工 stub 的固定 ID 列表。

### 3. AI 类型 1 在模板成员早退之前判定

类型 1 的“仅自慰”是全局行动策略，应先于“已在模板则不重新分配位置”的布局保护。目标顺序：先验证 H/群交/束缚等硬门禁，再处理类型 1 自慰意图，最后才对其他 AI 类型应用模板成员早退。

不让 intent fix 自行扫描所有模板成员并伪造 marker，因为生成意图属于群交 AI 的所有权；补丁只负责 marker 生命周期和正式行为路由。

### 4. 以窗口终态而非中途绘制判断自慰是否发生

回归记录每个角色在一个新的 `over_behavior_character` 窗口内：marker 生成次数、`default91` 路由次数、正式 `MASTUREBATE` 行为和效果次数。允许文本在窗口末尾统一出现，但不允许零行为或重复行为。

## Risks / Trade-offs

- **[离线设置强化]** 非活跃催眠角色也会获得持久强化字段 → 这是命令“不改变当前催眠态”与永久强化语义的直接结果；实际效果仍由催眠态门控。
- **[模板动作被覆盖]** 类型 1 提前判定会让已占模板位置的角色改为自慰 → 这是“仅自慰”模式的预期；切换到其他 AI 类型后模板布局仍按原逻辑处理。
- **[观察条件不完整]** playtest 未记录当时 `npc_ai_type` → 测试先分别固定类型 1 与非类型 1；仅前者必须全员自慰，避免把普通模式误判为 bug。
- **[同窗口重复]** 提前生成 marker 可能被追时间多次遇到 → 继续依赖现有 action-key 去重，并断言每角色每窗口至多一次。

## Open Questions

- 手动复现时实际选择的群交 AI 类型尚未从截图确认；这不影响类型 1 的已确认早退缺陷，但会影响该次“无人自慰”现象是否完全由此解释。
