/investigate-game-bug

请审核 erArk PR #212 在 reviewer 反馈后的最小修订，并独立判断 reviewer 所说的“心理快感能力加成重复计算两遍”是否符合代码事实。

用户要求：保留前一版 PR 的 `route_pain_delta` 设计、small/middle/large pain 与 extra orgasm 调用点；修复真正重复的连续指令修正，并删除因此未使用的 helper 参数、文档和参数传递。不得扩大为 helper 重写或调用点重构。

候选：
- worktree: `/home/ubuntu/games/erArk-pr-212-one-line`
- base: rebase 后旧 PR commit `c72d25a54e7931e7475227b6e959496eb199f079`
- upstream/master: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`

完整生产 diff：

```diff
diff --git a/Script/Settle/common_default.py b/Script/Settle/common_default.py
@@
 def route_pain_delta(
         character_id: int,
         pain_value: float,
-        continuous_adjust: float = 1,
         ) -> Tuple[int, float]:
@@
     character_id -- 角色id
     pain_value -- 已计算完成的有符号苦痛增量
-    continuous_adjust -- 心理快感阶段的连续指令修正
@@
     final_adjust = chara_feel_state_adjust(character_id, 23, character_data.ability[36])
-    final_adjust *= continuous_adjust
     final_value = int(pain_value * final_adjust)
@@
         state_id, final_value = route_pain_delta(
             character_id,
             final_value,
-            continuous_adjust,
         )
```

生产 diff 统计：`0 additions / 4 deletions`，只改 `Script/Settle/common_default.py`。两个生产文件编译通过，`git diff --check` 通过。

实际路径与动态证据：
1. common state 17 先调用 `chara_base_state_adjust`，再在重复指令达到 5 次时执行一次 `final_adjust *= continuous_adjust`，此时 `continuous_adjust=0.4`。
2. 旧 PR 把已含 `0.4` 的 `final_value` 与同一 `continuous_adjust` 传入 helper；helper 又乘一次 `0.4`。
3. 本地测试直接加载生产 `route_pain_delta` 与 `base_chara_state_common_settle`，记录 base/feel adjustment 调用次数：
   - 旧版：输入 add_time=100、base adjust=1、continuous=0.4、feel adjust=2，最终 state 23 为 `32`；base adjustment 调用 1 次，`chara_feel_state_adjust(character_id, 23, ability[36])` 调用 1 次。
   - 候选：相同输入最终 state 23 为 `80`；base adjustment调用 1 次，心理快感 adjustment 调用仍为 1 次。
4. 四个 direct writers 都只以两个参数调用 helper；旧版第三参数默认 1，所以删除乘以 1 与删除参数传递不会改变其数值。
5. 全仓相关搜索只找到 helper 内这一处 `chara_feel_state_adjust(character_id, 23, character_data.ability[36])`；common 先前调用的是 state 17 的 `chara_base_state_adjust`，不是 state 23 的心理快感能力修正。

请输出：
- `PASS` 或 `REVISE`。
- reviewer 的“心理快感能力加成计算两遍”是否属实；明确区分 state 17 苦痛基础修正、state 23 心理快感修正、连续指令修正。
- 四行删除是否是完整且最小的清理，是否保持 direct writers 行为。
- 若 REVISE，只指出当前四行删除的具体正确性或范围问题，不提出未授权重构。
