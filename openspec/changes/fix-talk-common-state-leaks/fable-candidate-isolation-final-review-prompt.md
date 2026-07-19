/investigate-game-bug

请以怀疑视角独立审查 erArk T7 的第二个、与临时目标恢复分开的候选：“通用口上短部位候选列表不得被一次渲染永久修改”。不要因为生产 diff 只有一行或测试通过而接受它；请用工具读取精确 diff、完整函数、加载器、测试与当前文档。

基线：`upstream/master` 的 `72e28051ebaaabb069d06059b4633fda90b0b621`
隔离候选：`/home/ubuntu/games/erArk-pr-talk-common-candidate-isolation`
生产 diff：该工作树的 `Script/Design/talk.py`
本地证据测试：该工作树的 `tests/test_talk_common_candidate_isolation.py`
相关回归：`/home/ubuntu/games/erArk/tests/test_movement_talk_actor_context.py`
当前记录：

- `/home/ubuntu/games/erArk/openspec/changes/fix-talk-common-state-leaks/design.md`
- `/home/ubuntu/games/erArk/openspec/changes/fix-talk-common-state-leaks/tasks.md`
- `/home/ubuntu/games/erArk/openspec/changes/fix-talk-common-state-leaks/candidate-isolation-implementation-notes.md`

确认的红灯：在当前上游的干净一次性 linked worktree 中运行两项聚焦测试得到 `2 failed`。第一次短部位展开把通用 A 候选原地追加到专属 A 列表；第二次的随机池从 `[1000, 2000]` 变成 `[1000, 2000, 2000]`，全局列表也永久增长。若组合后随机选择抛异常，全局列表仍被污染。

候选只把：

```python
part_dict = game_config.config_talk_common_cid_list_by_part[key]
```

改为：

```python
part_dict = {part: cid_list.copy() for part, cid_list in game_config.config_talk_common_cid_list_by_part[key].items()}
```

随后原有 `part_dict["A"] += common_s_A_list` 和随机选择流程不变。加载器在 `game_config.py` 中建立的是“类型字典 -> 部位字典 -> CID 列表”这一层嵌套；当前函数对 `part_dict` 或其中 CID 列表的唯一写入就是该 `+=`。生产数据中有 45 个通用口上 CSV 文件实际引用受影响的 12 类短部位占位符。

确认的绿灯：候选聚焦 2 项与移动口上相关回归 10 项共 `12 passed`；`py_compile` 与 `git diff --check` 通过。测试核对两次选择池完全相同、全局配置前后相同，以及随机选择异常后配置仍相同。

按当前 skill 的精确评分，最终生产 diff 是一个 1-for-1 change group：`a=1, b=1, S=0, U=0, penalty=2`。备选“两处改动：浅复制字典并把 A 改成非原地拼接”为 penalty 4；结束时回滚在重复元素或异常下不可靠；全量 deepcopy 扩大无必要复制。

尚未完成：真实 Tk 的重复展开 A/B、PR 文案、最终 artifact audit。不要把当前审查当作玩家可见证据 PASS，也不要起草 PR 文案。

请回答：

1. 这是否是正常游戏可达的全局配置污染 bug；一层列表浅复制是否修复正确逻辑所有者，并保留字典顺序、列表顺序、已有重复 CID 和随机权重？
2. 是否存在漏复制的可变层、别名、其他写入、异常或组合路径，会让该一行候选不正确？
3. `a=1,b=1,S=0,U=0,penalty=2` 是否精确，是否存在通过硬门槛且更低的正常风格候选？
4. 当前 design/tasks/implementation-notes 对这个独立 PR scope 是否准确、没有把尚未取得的 Tk 证据写成已完成，也没有与临时目标候选混为一个 PR？
5. 真实 Tk A/B 最少需要显示什么，才能让人类评审理解“历史渲染次数改变后续候选权重”；若随机文本难以在一组静态图中直接证明，请明确可接受的替代玩家证据边界。

请分别给出 `CODE PASS/REVISE`、`DOCS PASS/REVISE`，并单列 `TK EVIDENCE REQUIREMENT`。任何 REVISE 请给具体可执行修改，按严重性排序。不要修改文件。
