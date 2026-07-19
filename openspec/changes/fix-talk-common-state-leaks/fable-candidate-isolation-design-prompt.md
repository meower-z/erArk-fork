/investigate-game-bug

请作为怀疑性的 erArk T7 第二 PR scope 设计裁决者。不要预设最短 diff 一定正确；先检查硬门槛，再按当前 SKILL.md 的真实 penalty 定义比较。

当前 upstream/master 72e28051e，问题位于 Script/Design/talk.py 的 talk_common_judge：
- 命中分段短词 key 时，part_dict 直接引用 game_config.config_talk_common_cid_list_by_part[key]。
- 对 `_s` 且非 penis/hair 的 key，执行 part_dict["A"] += game_config... ["common_s"]["A"]。
- 因而每次渲染都把通用 A cid 永久追加到全局专属 A 列表；重复渲染令候选重复数与随机权重持续增长，异常发生在追加之后也留下污染。

红灯证据在 /home/ubuntu/games/erArk-pr-talk-common-candidate-isolation/tests/test_talk_common_candidate_isolation.py，尚无生产改动。当前上游实跑 2 failed：两次展开观察到选择池 [1000,2000] 后变为 [1000,2000,2000]，全局 body_s/A 从 [1000] 变成 [1000,2000,2000]；random.choice 抛异常后也留下 [1000,2000]。玩家目标在夹具中已经是 NPC，因此这个测试与第一个临时目标 PR scope 无耦合。

候选：
A. 只把 `part_dict = global[key]` 一行替换成 `{part: cid_list.copy() for part, cid_list in global[key].items()}`，后续现有 `part_dict["A"] += common_s_A_list` 原样保留，但只修改本次所有部位列表副本。最终生产 diff 预计 a=1,b=1,S=0,U=0,penalty=2。保持 dict/list 顺序和 cid 重复数，只增加对该 key 所有一层列表的浅复制。
B. `part_dict = global[key].copy()`，并把 `part_dict["A"] += common` 改为 `part_dict["A"] = part_dict["A"] + common`，只复制字典且仅为 A 建新列表。两处单行替换，预计 a=2,b=2,S=0,U=0,penalty=4。
C. 保持全局 part_dict 只读，在 for part 循环内按 part==A 构造局部 talk_common_cid_list；需要搬动现有组合逻辑与多行条件，分数更高但复制更少。
D. 你认为更正确的其他边界。

请直接读取生产代码、配置加载器与红灯测试后裁决。重点检查：A 的浅复制是否足以隔离唯一写点；是否存在嵌套元素或别名使 A 仍污染；复制所有 part 列表会否改变随机顺序/语义或构成不合理运行成本；是否还有对 part_dict/list 的兄弟写点；异常路径；与临时目标独立 PR 的可拆分性；测试是否还缺反向或生产数据锚点。先给明确选择或否决，并复核 penalty。若通过，请列出实施前中央设计必须记录的事实和最小充分验证。不要写 PR 文案。
