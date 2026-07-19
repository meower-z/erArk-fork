/investigate-game-bug

这是对你先前 T7 临时目标作用域最终裁决的唯一一轮反驳复审。请保持怀疑视角；不要因为候选已经写出或测试通过而接受它。事实以你可直接读取的源码、diff 和测试为准。

先前裁决位置：
- /home/ubuntu/games/erArk/openspec/changes/fix-talk-common-state-leaks/fable-target-scope-final-review-ruling.md

其中你判定：把原 `code_text_to_draw_text` 改名为私有实现，再加公开 `try/finally` 包装，是通过硬门槛候选中的最低 penalty；该生产 diff 为 a=17,b=1,S=15,U=0,penalty=33。

新反例候选 D 的权威位置：
- worktree：/home/ubuntu/games/erArk-pr-talk-common-target-scope-d
- baseline：upstream/master = 72e28051ebaaabb069d06059b4633fda90b0b621
- production diff：该 worktree 的 Script/Design/talk.py 相对 upstream/master
- focused tests：该 worktree 的 tests/test_talk_common_target_scope.py
- related tests：/home/ubuntu/games/erArk/tests/test_movement_talk_actor_context.py

候选 D 的机制：
1. `code_text_to_draw_text` 在调用 `talk_common_judge` 前保存玩家原 target。
2. `try` 中运行整个 `talk_common_judge`，并在其正常返回后捕获它留下的 `common_target_character_id`。
3. `finally` 立刻恢复玩家原 target；所以 judge 内任何异常恢复，judge 之后任何异常发生时也已经恢复。
4. 后续 common_talk_flag 路径的 `target_data`、`PlayerTargetName` 都改读捕获 ID；`PlayerNickName` 的直接 target 判定仅在 common_talk_flag=True 时改读捕获 ID，flag=False 时仍读 NPC 自己的 target。
5. 因此全局临时 target 的必要生存期缩短为通用前提选择；judge 返回后的当前文本格式化由局部捕获的 B 对象/ID维持到最终 `.format`。候选没有改 `talk_common_judge` 的选择语义。

已验证事实：
- 当前 upstream 运行 focused tests：8 failed, 2 passed；两条 inverse（玩家自身、无通用占位符）通过，其余恢复断言失败。
- 候选 D：focused 10 项 + 相关 movement 10 项，共 20 passed。
- focused 覆盖：正常临时目标与恢复；judge 内前提异常；最终 `.format` KeyError；玩家自身；无通用占位符；common_talk_flag=False 的 NPC 通用占位符；Web 真实 handle_talk_draw 路由；连续 A→B→A 三次调用；原 target=0 时 PlayerNickName；TargetName、TargetNickName、TargetNickNameToPl、PlayerTargetName 和六个 Target*ClothName 一次性核对。
- production data/talk_common 当前有 68 个 CSV 文件含 `{TargetName}`；没有搜索到 `{PlayerTargetName}` 或 Target*ClothName，但格式化接口仍支持并已测试。
- py_compile、git diff --check 通过。
- 当前开放上游 PR 只有 #212、#217、#218，与本候选不重叠。

新版 score 按实际 diff 初算：
- 主 change group：删除原 judge 调用 1 行，增加 save/try/indented call/capture/finally/restore 6 行，a=6,b=1,e=5,S=4。
- 另有三处单行 1-for-1 replacement：target_data、PlayerNickName 条件、pl_target_id，共 a=3,b=3,S=0。
- 总计 a=9,b=4,S=4。三条删除文本均不同，也未在多点删除相同规范化文本，U=0。
- penalty=(9+4)+4-0=17。

Web 语义：D 和先前包装器一样，在 `handle_talk_draw` 的 Web 路由读取前已经恢复原 target，所以非当前目标 NPC 进入 minor dialog 且 wait_input=False；这是相对 baseline 的同一待玩家确认语义，不是 D 相对包装器的新变化。

旧本地 mod 组合事实：upstream/master 已合并 #214，worktree 中没有 `local_npc_move_talk_context_fix`，mod_config 为空；主本地树保留该 mod 但 enabled_mods 已禁用。若人为重新启用，mod 的替换函数只有两个参数，而当前生产调用传三个参数，会 TypeError；手动两参数 `{move}` 路径又会在进入 D 前直接调用 `talk_common_judge`，实测 target 从 2 泄漏到 1，D 只能保存已污染的 1。因此真实 A/B 必须使用 pristine upstream runtime，不得加载该废弃 mod。

请直接读取实际 diff、生产函数和测试后给最终 `PASS` 或 `FAIL`：
1. D 是否在硬门槛上与先前包装器语义等价，包括所有 common 展开、最终 `.format`、异常、flag=False、连续/嵌套调用；若不等价，请给一个具体可触发反例。
2. `penalty=17` 是否按当前 SKILL.md 精确无误，是否还存在更低且通过硬门槛的正常代码候选。
3. 立即恢复全局 target、用局部 target_data/ID 完成后半段，是否是比整函数包装更准确的逻辑 owner，还是把生命周期切得过碎。
4. Web minor-dialog 与废弃 mod 的结论是否准确。
5. 若 PASS，请明确先前“包装器最低分”的结论是否被 D 推翻，以及应保留 D 还是包装器。若 FAIL，只列最小必要修改或具体否决理由。

不要写 PR 文案，不要修改文件。
