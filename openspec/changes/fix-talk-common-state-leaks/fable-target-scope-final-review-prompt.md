/investigate-game-bug

请作为新鲜、怀疑性的最终实现审查者，审查 erArk 的 T7 临时目标作用域候选。不要假设先前设计裁决或实现是正确的；你可以否决。

权威位置：
- 当前上游基线：/home/ubuntu/games/erArk-pr-talk-common-target-scope 的 upstream/master，SHA 72e28051ebaaabb069d06059b4633fda90b0b621
- 最终生产 diff：该工作树相对 upstream/master 的 Script/Design/talk.py（只有这个生产文件）
- 本地红绿测试：该工作树 tests/test_talk_common_target_scope.py
- 既有相关本地回归：/home/ubuntu/games/erArk/tests/test_movement_talk_actor_context.py
- 中央设计与证据：/home/ubuntu/games/erArk/openspec/changes/fix-talk-common-state-leaks/design.md 和 target-scope-implementation-notes.md
- 先前设计 prompt/ruling 已原样保存在同目录，但请独立读代码与 diff，不以先前结论代替审查。

已报告结果：基线 3 failed/2 passed；候选的两组测试合计 15 passed；py_compile 和 candidate git diff --check 通过。新版评分按实际 skill 定义报告为 a=17,b=1,S=15,U=0,penalty=33（numstat 19/1 中有两条新增空行）。

请重点质疑：
1. 公开 code_text_to_draw_text 包装、私有 _code_text_to_draw_text 的边界是否完整且不会改变当前展开文本；正常和异常是否都恢复。
2. 函数定义顺序、递归/全局名字解析、调用者、monkeypatch 与本地 mod call_original 是否引入未记录问题。
3. 无通用占位符时无条件同值写回是否可能遮蔽合法持久更新；请核对生产写者而不是信任说明。
4. Web 小对话框测试是否真实经过 handle_talk_draw 的路由读点，并且待玩家确认的可见语义是否准确。
5. 测试是否过拟合 mock，是否还缺一条能阻止明显错误实现的最小回归。
6. 用当前 SKILL.md 的真实 S/U 定义复核 penalty=33。
7. PR scope 是否严格独立于 part_dict 候选列表污染修复。

先给 PASS 或 FAIL。若 FAIL，请给最小必要修改；若 PASS，请清楚列出仍未完成但不阻止代码候选成立的证据/发布事项。不要写 PR 文案。
