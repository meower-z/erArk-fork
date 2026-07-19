## Why

群交结算中存在两个相邻的本地修复缺口：闲置 NPC 被群交 AI 反复导向自慰时，同一次玩家点击可能多次显示同一角色寸止；疲劳或体力归零的群交参与者退出后，又可能立刻触发“发现群交”面板，并被邀请加入后马上再次退出。

这些问题都发生在当前启用的 `local_bugfix` mod 已经接管的群交/H 状态边界中，因此应继续以 mod 层修复记录和实现，避免直接修改核心游戏文件。

## What Changes

- 为群交 H 状态下 `masturebate == 3` 的 `default91` 自慰导向增加“同一玩家行动切片只消费一次”的约束。
- 保留下一次玩家行动继续触发群交自慰的能力，避免把自动自慰永久禁用。
- 在群交发现 H 面板绘制前识别疲劳、困倦或体力归零的发现者。
- 对疲劳发现者跳过“发现群交/邀请加入”按钮面板，直接复用原版 `SEE_H_AND_LEAVE` 行为。
- 保持非疲劳的新发现者、邀请加入、拒绝加入、结束 H 等原有面板逻辑不变。
- 通过 `mod/local_bugfix` 的 wrapper/registry patch 实现；核心 `Script/` 文件和 CSV 数据保持不变。
- 补充回归测试和 README 记录，说明根因、修复策略和验证方式。

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `local-bugfixes`: 扩展群交自动自慰和疲劳发现群交的本地 bugfix 行为契约。

## Impact

- Affected mod: `mod/local_bugfix/scripts/local_bugfix.py`
- Affected tests: `mod/local_bugfix/tests/test_local_bugfix_mod.py`
- Affected documentation: `mod/local_bugfix/README.md`
- Affected runtime paths by hook only:
  - `Script.Design.handle_npc_ai.find_character_target`
  - `Script.System.Sex_System.sex_be_discovered_panel.Sex_Be_Discovered_Panel.draw`
- Core game files and generated CSV/JSON data remain unchanged.
