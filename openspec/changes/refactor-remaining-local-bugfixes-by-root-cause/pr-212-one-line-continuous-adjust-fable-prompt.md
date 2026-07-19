/investigate-game-bug

请审核 erArk PR #212 在 reviewer 反馈后的最小候选。用户明确要求保留前一版 PR 的 helper、所有调用点和行为，只修复重复应用的倍率，并限定生产 diff 为一行删除。不要提出扩大范围的重构；只判断这一行是否准确修复已证实的问题，是否会改变 direct writers 或其他既有语义。

当前基点与候选：
- upstream/master: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`
- 旧 PR commit 已 rebase 为: `c72d25a54`
- candidate worktree: `/home/ubuntu/games/erArk-pr-212-one-line`

旧版已保留的设计：
- `route_pain_delta(character_id, pain_value, continuous_adjust=1)` 对非正值或未开启苦痛快感化返回 state 17 原值。
- 开启且正值时，用 `chara_feel_state_adjust(character_id, 23, ability[36])` 将最终苦痛值转换为 state 23。
- common state 17 在进入 helper 前已经把连续指令系数乘进 `final_adjust`，然后把 `continuous_adjust` 再传给 helper。
- small/middle/large pain 与 extra orgasm 调用 helper 时不传第三参数，因此默认值为 1。

旧版问题：common 路径先执行 `final_adjust *= continuous_adjust`，helper 又执行 `final_adjust *= continuous_adjust`，连续指令系数被应用两次。心理快感能力 `ability[36]` 本身只调用一次；reviewer 将其描述为能力加成重复，但代码证据表明真正重复的是 continuous adjustment。

唯一生产改动：

```diff
diff --git a/Script/Settle/common_default.py b/Script/Settle/common_default.py
@@
     final_adjust = chara_feel_state_adjust(character_id, 23, character_data.ability[36])
-    final_adjust *= continuous_adjust
     final_value = int(pain_value * final_adjust)
```

红绿检查直接加载生产 `route_pain_delta`：
- rebase 后旧版 `route_pain_delta(1, 100, continuous_adjust=0.4)` 返回 `(23, 80)`，测试失败。
- candidate 返回 `(23, 200)`，测试通过。
- candidate 两个生产文件可编译，`git diff --check` 通过。
- 本地测试文件不进入 PR。

请输出：
1. `PASS` 或 `REVISE`。
2. 说明 common 路径是否由两次 continuous adjustment 变为一次。
3. 说明 direct writers（默认参数 1）是否保持数值不变。
4. 说明 ability[36] 是否仍恰好计算一次。
5. 若 REVISE，只能指出这一行删除本身的具体错误；不要提出用户未授权的清理、参数删除、helper 重写或调用点变更。
