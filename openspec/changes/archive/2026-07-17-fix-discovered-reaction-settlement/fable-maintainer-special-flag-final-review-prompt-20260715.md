# Fable 5 final review prompt — maintainer `SPECIAL_FLAG` candidate

```text
/investigate-game-bug

只读 post-implementation 审查，不得修改任何文件。主仓为 /home/ubuntu/games/erArk；候选工作树为 /home/ubuntu/games/erArk-pr-discovery-settlement-special-flag，基线为 current upstream/master 58587deac62149d80c82b5a3c98ad29f51cfe2b4。审查当前未提交的四个 production 文件改动和本地聚焦测试。中央 OpenSpec 为 /home/ubuntu/games/erArk/openspec/changes/fix-discovered-reaction-settlement/。

Maintainer 明确要求：不得把这个 special case 编码为 constant.handle_state_machine_data 的返回值；新增 SPECIAL_FLAG 来记录/处理“该角色已经结算过 H 被发现反应”。同时必须保留用户已批准的逐 case 显式修补，不得引入统一 settlement helper。

请实际阅读 diff、两条 caller、嵌套 player update、state-machine 40、SPECIAL_FLAG 定义、调度器和测试，确认：
1. handle_npc_ai.find_character_target 和 state-machine dispatch 的返回合同没有改变，state 40 仍返回 None；
2. 七个显式发现者反应各同步结算恰好一次，四个原遗漏分支补齐；结算先于嵌套 player update；
3. panel-local marker 只在 draw 完成后由 state 40 写入角色 SPECIAL_FLAG，嵌套 game_update_flow 不会提前消费；
4. direct hidden_sex_panel caller 不写 marker；
5. scheduler 对 marked WAIT 跳过一轮、对 marked MOVE 仍结算并总是清标记；未标记 SHARE_BLANKLY 保持原结算；
6. 以非空行计数重算 a/b、change groups、重复删除 credit 与 penalty；
7. 重跑基线/候选聚焦测试、compileall 与 git diff --check。

输出明确 PASS 或 FAIL、实测计数、测试结果、必须修复 finding、残余风险，以及在这些约束下是否存在更小的正确方案。不要审查 PR 文案、不要改文件、不要执行 outward action。
```

Invocation:

```text
claude -p --model claude-fable-5 --effort high --no-session-persistence "$PROMPT"
```
