/investigate-game-bug

你是 erArk 上游 PR #212 的 PR 文案作者。请只根据下面已经核验的事实，为 maintainer 写一份新的中文 PR 草稿，不要照抄旧 PR 文案，也不要替 reviewer 背书。输出必须严格包含四个块：

TITLE_BEGIN
一行标题
TITLE_END
BODY_BEGIN
完整 Markdown 正文
BODY_END
REVIEW_REPLY_BEGIN
对 unresolved review thread 的简短中文回复
REVIEW_REPLY_END

目标：清楚说明这次不是只修复负向苦痛被错误改道的问题，还要保住所有正向苦痛来源的苦痛快感化，包括绕过通用 state 17 入口的 small/middle/large pain 和 extra orgasm。代码选择一个很窄的 helper 作为统一转换边界；helper 自己不计算心理快感能力系数，而是恰好一次调用 canonical state 23 结算，所以不存在重复计算能力加成。

不要在 PR 文案里写本地测试数量、本地路径、OpenSpec、agent/Fable 工作流或内部调查经过。不要声称 CI 已通过。图片使用下面的占位 URL。正文建议按“问题 / 原因 / 修复 / 验证”组织，但以 reviewer 易读为先。

已核验的 reviewer thread 原文：
“直接在这里判断苦痛是否为正就可以了，不需要再单独构建函数，以及单独构建的那个函数的里会导致重复计算两遍心理快感的能力加成”

独立代码审计结论：
1. 旧 helper 并没有调用两次心理快感能力修正；reviewer 很可能把 common 路径原有的连续结算倍率与心理快感能力系数混在了一起。
2. 但直接只在 common state 17 分支加正值判断也不完整，因为 small/middle/large pain 和 extra orgasm 会直接写 state 17，绕过 common 入口。
3. 最终 helper 接收“来源自身修正完成后的有符号最终苦痛值”。值 <= 0 或苦痛快感化未开启时返回 False；正值且开启时只调用一次 canonical `base_chara_state_common_settle(... state_id=23, ability_level=ability[36], tenths_add=False, ...)`，并返回 True。helper 不调用 `chara_feel_state_adjust`，不自行计算能力系数。
4. common state 17 在自身既有修正后调用 helper；负值留在 state 17，修复原错误改道。
5. small/middle/large pain 和 extra orgasm 在各自既有来源公式之后调用同一 helper；helper 接管后不再直接写 state 17，修复正向来源绕过转换的问题。
6. extra orgasm 无论是否转换仍结算恐怖并清零计数；提示文本根据实际结算显示“心理快感和恐怖”或“苦痛和恐怖”。
7. helper 返回的是“转换路径已接管”，即使 canonical state 23 因睡眠或无意识提前返回，也不得回落写入 state 17。
8. common 路径原有的 continuous/repeat tuning 没有改变；helper 没有递归环，也不会重复记录 state 17/state 23。

最终 diff（base `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`，head `5a4a87e8ecbba7cedf0b976b1f176593304f209c`）：

```diff
diff --git a/Script/Settle/Second_effect.py b/Script/Settle/Second_effect.py
index 8585933a9..1ddffef2e 100644
--- a/Script/Settle/Second_effect.py
+++ b/Script/Settle/Second_effect.py
@@ -8,7 +8,7 @@ from Script.Design import (
 from Script.Core import cache_control, constant_effect, game_type, get_text
 from Script.Config import normal_config
 from Script.UI.Moudle import draw
-from Script.Settle.common_default import base_chara_experience_common_settle, base_chara_hp_mp_common_settle, base_chara_state_common_settle
+from Script.Settle.common_default import base_chara_experience_common_settle, base_chara_hp_mp_common_settle, base_chara_state_common_settle, try_settle_pain_as_pleasure
@@
     now_add_lust += now_lust / 20
     now_add_lust = int(now_add_lust)
+    if try_settle_pain_as_pleasure(character_id, now_add_lust, change_data):
+        return
     character_data.status_data[17] += now_add_lust
@@
     now_add_lust += now_lust / 10
     now_add_lust = int(now_add_lust)
+    if try_settle_pain_as_pleasure(character_id, now_add_lust, change_data):
+        return
     character_data.status_data[17] += now_add_lust
@@
     adjust = attr_calculation.get_mark_debuff_adjust(character_data.ability[15])
     now_add_lust *= adjust
+    if try_settle_pain_as_pleasure(character_id, now_add_lust, change_data):
+        return
     character_data.status_data[17] += now_add_lust
@@
-        # 结算苦痛和恐怖
-        character_data.status_data[17] += extra_pain
-        character_data.status_data[17] = min(99999, character_data.status_data[17])
-        change_data.status_data.setdefault(17, 0)
-        change_data.status_data[17] += extra_pain
+        # 结算苦痛快感化和恐怖
+        pain_as_pleasure_flag = try_settle_pain_as_pleasure(character_id, extra_pain, change_data)
+        if not pain_as_pleasure_flag:
+            character_data.status_data[17] += extra_pain
+            character_data.status_data[17] = min(99999, character_data.status_data[17])
+            change_data.status_data.setdefault(17, 0)
+            change_data.status_data[17] += extra_pain
         character_data.status_data[18] += extra_terror
@@
-        now_text = _("\n{0}因为第{1}次的连续额外绝顶而被迫感受到了更多的苦痛和恐怖\n").format(character_data.name, all_extra_count)
+        if pain_as_pleasure_flag:
+            now_text = _("\n{0}因为第{1}次的连续额外绝顶而被迫感受到了更多的心理快感和恐怖\n").format(character_data.name, all_extra_count)
+        else:
+            now_text = _("\n{0}因为第{1}次的连续额外绝顶而被迫感受到了更多的苦痛和恐怖\n").format(character_data.name, all_extra_count)
diff --git a/Script/Settle/common_default.py b/Script/Settle/common_default.py
index f917fa522..0ac6f239b 100644
--- a/Script/Settle/common_default.py
+++ b/Script/Settle/common_default.py
@@
+def try_settle_pain_as_pleasure(
+        character_id: int,
+        pain_value: float,
+        change_data: Optional[Union[game_type.CharacterStatusChange, game_type.TargetChange]] = None,
+        change_data_to_target_change: Optional[game_type.CharacterStatusChange] = None,
+        ) -> bool:
+    """
+    尝试将正向苦痛值交给心理快感通用结算
+    """
+    if pain_value <= 0 or not handle_premise.handle_hypnosis_pain_as_pleasure(character_id):
+        return False
+    character_data: game_type.Character = cache.character_data[character_id]
+    base_chara_state_common_settle(
+        character_id,
+        pain_value,
+        23,
+        0,
+        ability_level = character_data.ability[36],
+        tenths_add = False,
+        change_data = change_data,
+        change_data_to_target_change = change_data_to_target_change,
+    )
+    return True
@@
-    # 心控-苦痛快感化，将苦痛状态转化为快感状态
-    if state_id == 17 and handle_premise.handle_hypnosis_pain_as_pleasure(character_id):
-        base_chara_state_common_settle(character_id, final_value, 23, 0, ability_level = character_data.ability[36], tenths_add = False, change_data = change_data, change_data_to_target_change = change_data_to_target_change)
+    # 心控-苦痛快感化，将正向苦痛状态转化为快感状态
+    if state_id == 17 and try_settle_pain_as_pleasure(character_id, final_value, change_data, change_data_to_target_change):
         return
```

两组真实 Tk A/B 证据（两侧都开启“苦痛快感化”，每组 baseline/candidate 使用同一冻结存档、相同种子、相同操作）：

第一组：负向 common state 17 不应改道。
- 共同起点图：`{{GROUP_A_SETUP_URL}}`
- baseline：`{{GROUP_A_BEFORE_URL}}`，强制高潮后显示 `心理快感 -272586 (lv10→0)`、`苦痛 +3811`。
- candidate：`{{GROUP_A_AFTER_URL}}`，相同操作后显示 `心理快感 +3656`、`苦痛 -31028 (lv7→4)`。
- 这组证明负向苦痛变化留在 state 17，心理快感不再被反向清空。

第二组：直接 small pain 的正向苦痛不应绕过转换。
- 共同起点图：`{{GROUP_B_SETUP_URL}}`
- baseline：`{{GROUP_B_BEFORE_URL}}`，等待五分钟后显示 `苦痛 +20`，没有心理快感。
- candidate：`{{GROUP_B_AFTER_URL}}`，相同操作后显示 `心理快感 +43`，没有苦痛；两边均无高潮干扰。
- 这组证明原实现漏掉的 direct writer 现在也被统一转换，且没有 state 17/state 23 双记账。

review reply 要直接、克制：承认“正值才转换”的判断方向正确，但说明只在 common 分支判断会漏掉 direct writers；说明保留 helper 的具体理由，以及 helper 只委托 canonical state 23 一次，所以不会重复计算能力加成。不要说 reviewer “错了”，也不要长篇辩论。
