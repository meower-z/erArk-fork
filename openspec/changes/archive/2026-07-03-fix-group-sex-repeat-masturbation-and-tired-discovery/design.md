## Context

群交 NPC 行为由 `character_behavior.init_character_behavior()` 的 NPC 循环追赶玩家行动时间片。H 状态 NPC 通常不会继续走普通 AI，但 `local_bugfix` 之前为了修复群交中“仅自慰/无空位则自慰”的傻站问题，在 `find_character_target()` 里把群交 H 状态且 `masturebate == 3` 的 NPC 导向 `default91`，让正式自慰行为结算消费该标记。

新的重复寸止现象发生在同一玩家点击内：群交 AI 可以在 NPC 自慰行为完成并回到空闲后，再次把闲置 NPC 设置为 `masturebate == 3`。戴玩具或其他二段效果会放大快感，导致同一时间片里多次自慰、重复触发寸止提示。这里的重复来源不是 `default91` 不清标记，而是群交 AI 在同一玩家行动 catch-up 中重新生成自慰意图。

疲劳发现群交问题来自另一条边界：群交疲劳退出会清理该 NPC 的 H 状态和群交模板占位，但当前群交仍在继续；发现 H 面板只按实行值判断能否邀请群交，没有把低体力、疲劳或困倦作为加入限制。于是刚退出的角色或新的疲劳路过角色都可能打开“发现群交”面板，被邀请后马上再次因疲劳退出。

用户要求修复继续以 mod 形式存在，因此实现边界限定在 `mod/local_bugfix`，不直接修改 `Script/` 核心文件或 CSV 数据。

## Goals / Non-Goals

**Goals:**

- 同一个 NPC 在同一次玩家行动结算中最多执行一次群交自动自慰导向。
- 下一次玩家行动仍允许该 NPC 再次因为群交 AI 进入自动自慰。
- 疲劳、困倦或体力归零的发现者在群交中不弹出邀请加入按钮。
- 旧参与者疲劳退出后不会立刻用“发现群交”打扰当前群交。
- 新的疲劳路过角色也不会被邀请进入一个自己无法持续参与的群交。
- 非疲劳发现者、邀请成功/拒绝、结束 H 等既有逻辑保持不变。
- 所有变更通过 `local_bugfix` wrapper/registry patch 实现，并增加回归测试。

**Non-Goals:**

- 不重写群交 AI 的补位策略。
- 不修改 `default91` 或自慰行为本身的效果配置。
- 不改变群交邀请的实行值判定公式。
- 不新增 CSV 前提或编辑 `data/target/default/target.csv`。
- 不改变普通单人 H、隐奸、露出模式下的发现 H 面板逻辑。

## Decisions

### 1. 在 `find_character_target()` 的 mod wrapper 中限制同一玩家行动内的自慰导向

`patched_find_character_target()` 保留原有判断：只有群交 H 状态且 `masturebate == 3` 时才拦截并搜索 `default91`。新增的消费记录以角色 ID 为键，以当前玩家行动切片为值；命中已消费时，不再执行 `default91`，而是把该 NPC 加入 `cache.over_behavior_character`，结束本轮 NPC catch-up。

Rationale: 重复来源发生在 `find_character_target()` 被反复调用的边界，这里是最小且最靠近现有本地修复的拦截点。直接修改群交 AI 的 `masturebate = 3` 生成逻辑更容易误伤“下一次玩家行动仍可自慰”的正常行为。

Alternative considered: 结算后强制清理 `masturebate` 并阻止群交 AI 再设置。这个方案会和原版自慰行为效果 `456` 的清理语义重叠，而且无法区分“同一玩家行动重复”和“下一次玩家行动再次自慰”。

### 1.1 只清理被本地 wrapper 抑制的自慰意图

当 wrapper 因“本行动已消费”而拒绝第二次 `default91`，或 `default91` 当前不可用时，它会清理 `sp_flag.masturebate` 并调用异常 flag settle 通知。这不是替代正式自慰结算的效果 `456`：第一次成功执行 `default91` 时仍由原版行为效果清理；只有本地 wrapper 主动丢弃的重复/失败意图才被清理。

Rationale: 如果重复意图被压掉后仍保留 `masturebate == 3`，它会泄漏到下一次玩家行动。下一轮即使群交 AI 因出现空位而没有重新选择自慰，wrapper 仍会看到旧 marker 并错误导向 `default91`。窄清理能避免 stale marker，又不影响正常成功自慰路径。

### 2. 行动切片 key 使用本轮 NPC catch-up token

消费 key 使用本地递增的 action serial。每当 `cache.over_behavior_character` 换成新的 set 对象时，说明一次新的行为结算循环开始，local bugfix 递增 serial 并清空上一轮自慰消费表；同一个 set 对象存续期间，所有 NPC catch-up 调用共享同一个 serial。

Rationale: `init_character_behavior()` 在每次行为结算入口都会重建 `cache.over_behavior_character`，而同一玩家行动的 NPC 追赶阶段会共享该 set。把它作为本地 action token 的边界，比混合 `game_time`、玩家历史和行为字段更可解释，也避免零耗时或不推进时间的连续行动产生误去重。

Alternative considered: 使用 `cache.game_time`、玩家行为起点/持续时间和最近行为记录组成启发式 key。该方案在正常流程下可用，但对零耗时、时停或对象 id 复用边界不够直接。最终改为持有上一轮 over set 对象引用并递增 serial。

### 3. 在发现 H 面板绘制入口做疲劳发现者兜底

`Sex_Be_Discovered_Panel.draw` 是发现 H 状态机最终弹 UI 的入口。`_patch_sex_be_discovered_panel()` 保存原方法并替换为 wrapper：当玩家处于群交模式且发现者疲劳、困倦或体力归零时，跳过原按钮面板，执行自动离开；否则调用原方法。

Rationale: 这个点能同时覆盖旧参与者疲劳退出后重新发现群交、以及新的疲劳角色路过发现群交。只隐藏“邀请加入”按钮仍会保留不必要的发现面板；只在 `_invite_find_char_to_join()` 中拒绝则仍会让玩家看到无效选项。

Alternative considered: 修改 target 前提，让疲劳角色不触发 `SEE_H_AND_MOVE_TO_DORMITORY`。这对 upstream 可能更干净，但在本地 mod 中改 CSV/目标前提侵入更大，也更容易和生成数据冲突。

### 4. 自动离开复用原版 `SEE_H_AND_LEAVE`

自动离开流程复用被发现面板进入时的通用副作用：记录发现者名字、清理逆推标记、目标转玩家、设置目击 H flag，然后赋予 `SEE_H_AND_LEAVE` 行为和配置持续时间，并把面板恢复到 `IN_SCENE`。

Rationale: 这保持了“她确实看见了，但因为疲劳不会交涉/加入”的语义，也复用原版离开行为的气力、心情和移动效果。直接静默忽略会绕过已有目击 H 状态结算。

Alternative considered: 使用 `SEE_H_BUT_IGNORE`。疲劳角色逻辑上更像无法参与、选择离开；`SEE_H_AND_LEAVE` 也避免她停在现场继续触发同一类交互。

## Risks / Trade-offs

- [Risk] 消费 token 依赖 `cache.over_behavior_character` 在行为结算入口被重建的约定。 -> Mitigation: 这是 `init_character_behavior()` 的现有入口语义；测试覆盖同一 over set 内重复生成自慰意图被阻止、换新 over set 后可再次执行。
- [Risk] 面板层兜底仍会产生一次“目击 H”副作用。 -> Mitigation: 这是有意保留的原版发现语义；只是跳过疲劳角色无法有效处理的邀请 UI。
- [Risk] 未来 upstream 给 target 前提加入疲劳限制后，本地 wrapper 可能变成冗余。 -> Mitigation: wrapper 只在面板实际打开且发现者疲劳时运行，未来无触发时自然 no-op。
- [Risk] 疲劳新路过角色不再给玩家选择“邀请加入”。 -> Mitigation: 她本来会马上退出，因此该选择是无效循环；非疲劳角色仍保留完整选项。

## Migration Plan

1. 在 `mod/local_bugfix/scripts/local_bugfix.py` 中加入群交自慰行动切片消费记录。
2. 在 `patched_find_character_target()` 的 `masturebate == 3` 分支中应用去重。
3. 在 `local_bugfix` registry patch 阶段替换 `Sex_Be_Discovered_Panel.draw`。
4. 为疲劳发现者实现自动 `SEE_H_AND_LEAVE` 路径。
5. 更新 `mod/local_bugfix/tests/test_local_bugfix_mod.py` 覆盖两个 bug。
6. 更新 `mod/local_bugfix/README.md` 记录根因、修复和验证。
7. 运行 local bugfix 测试、多重绝顶回归测试和语法编译检查。
