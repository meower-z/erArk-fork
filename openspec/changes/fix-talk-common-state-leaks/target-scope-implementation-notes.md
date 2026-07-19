# 临时目标作用域实现记录

## Scope

- PR scope：只恢复一次口上格式化期间临时改写的玩家交互目标。
- 当前上游基线：`72e28051ebaaabb069d06059b4633fda90b0b621`。
- 候选工作树：`/home/ubuntu/games/erArk-pr-talk-common-target-scope-d`。
- 候选分支：`codex/fix-talk-common-target-scope-d`。
- 本地生产提交：`145ad51084c780e7ffc927a0ab472606802755a4`；只含 `talk.py` 的 9 增 4 删，测试与 Fable 原始记录保持未跟踪、本地证据状态。
- 不包含同一 OpenSpec 的通用候选列表污染修复；后者保留为独立 PR scope。

## Baseline failure

本地回归文件 `tests/test_talk_common_target_scope.py` 在未改生产代码的当前上游上得到 `8 failed, 2 passed`：

1. 正常 NPC 纸娃娃地文的当前文本正确显示“目标是阿米娅”，前提计算也看到临时目标 1，但返回后玩家目标仍错误为 1，而不是原目标 2。
2. 前提计算抛出 `RuntimeError` 后，玩家目标同样错误留在 1。
3. 最终格式化异常、连续 A→B→A 调用、原目标为玩家、`common_talk_flag=False` 和各种目标占位符进一步暴露或约束同一状态边界。
4. Web 路由在泄漏影响下未满足“恢复后进入 NPC 小对话框”的断言。

玩家自身触发和无通用占位符的 NPC 文本在基线上已通过，用作反向保护。

## Production trace

- `talk_common_judge()` 在通用占位符命中、NPC 与玩家同场景时，把玩家目标写成该 NPC。
- 同函数内的前提判断从全局缓存读取该临时目标。
- `code_text_to_draw_text()` 在通用展开返回后，仍要用临时目标完成 `{TargetName}`、`{PlayerTargetName}` 和目标衣物等占位符格式化。
- `handle_talk_draw()` 的 Web 分支在格式化返回后读取玩家目标，决定主对话框或 NPC 小对话框。
- 上游 `talk.py` 内只有上述通用展开写点；`handle_premise` 包没有写入 `target_character_id`。

## Candidate

在现有 `talk_common_judge()` 调用前保存玩家原目标；`try` 中完成通用选择并捕获本次 NPC ID，`finally` 立即恢复。后续 `target_data`、玩家称呼判断和 `pl_target_id` 改读捕获值，最终格式化不再依赖泄漏的全局状态。

最终生产 diff 评分：`a=9`、`b=4`、`S=4`、`U=0`，`penalty=17`。生产 diff SHA-256 为 `0a0c1ba644429f129c7aa41e46f6673cef91d6720e7df7b016ede99b9f21f579`。Fable 的反驳复审确认它与包装器保持所需语义，但把全局状态生存期缩短到真正需要它的通用前提选择阶段，因此保留本候选并弃用 `penalty=33` 的包装器。

## Verification

- `python -m pytest -q tests/test_talk_common_target_scope.py /home/ubuntu/games/erArk/tests/test_movement_talk_actor_context.py`：`20 passed`。
- `python -m py_compile Script/Design/talk.py`：通过。
- `git diff --check`：候选工作树通过。
- OpenSpec strict validate：通过。

回归测试是本地证据，不进入上游生产 PR。真实 Tk A/B、玩家 Web 语义确认、PR 文案和新鲜 artifact audit 仍待完成。真实 Tk 必须使用未加载废弃 `local_npc_move_talk_context_fix` 的 pristine upstream runtime；该 mod 会在候选进入前先污染目标。

后续限定搜索更正了场景人数：save 99 中有玩家和十名 NPC，凯尔希既是其中一名 NPC，也是当前交互目标 A，因此不同 NPC B 候选实际有九名。H 模式下可用的是 `[6001]等待五分钟`，而 `[1001]` 受 `NOT_H` 前提限制。九名候选的首段自慰文本不含 Talk_Common 占位符，但其二段 V 绝顶行为可以命中 Talk_Common。

固定 seed `20260715`、`PYTHONHASHSEED=0` 的先前只读生产结算在 300 秒内没有返回；当时没有诊断它停在输入等待还是计算路径，因此该超时不是否定证据。随后一度提出“特蕾西娅或林会在第一次等待内结算两次自慰并跨过 V 阈值”的静态算术路线，但完整 seed-0 生产运行已推翻其调度前提：两人都没有进入自慰部位选择或 effect 524，V 只分别从 803 增至 840、5379 增至 5416，没有绝顶。完整反证见 [target-scope-save99-v-reachability.md](target-scope-save99-v-reachability.md)。随机 seed 不能补救一个未发生的调用，因此 seed 扫描已暂停。

一次性 seed-0 状态机诊断已解释 effect-524 缺失：特蕾西娅和林实际选中 `default9`/状态机2/`wait`，effect 序列只有 `[9999]`。群交 flag3 本身不让 normal-1 进入包含 target91 的 type-12 搜索；先前的静态必经判断错误。六个 RNG 检查点、时间、目标、V 值和存档哈希全部复现，详见 [target-scope-save99-state-machine-diagnostic.md](target-scope-save99-state-machine-diagnostic.md)。

任务 3.2 继续保持 open 和 `TK EVIDENCE BLOCKER`，但 save99 的重复 `[6001]` 路线现已冻结，而不是等待更多 seed。target86 的逆推分支本身仍可通往 target91→behavior418→effect524；然而在这份存档中，七名候选先经工作、休息或娱乐离场，最后两名在第一次午夜刷新后欲望只有 8–16，随即因工作 target802 返回宿舍并退出 H，因此不存在有限等待次数。完整闭环见 [target-scope-save99-wait-only-route-closed.md](target-scope-save99-wait-only-route-closed.md)。反事实的第1875次等待不能作为玩家证据；不得继续从这条路线 seed 扫描或声称 PR-ready。

若未来从另一份正常存档或可信的重现存档找到路线，正式证据仍至少需要同一连续受监督 baseline 会话的三个全分辨率帧：触发前标题为凯尔希、B 名字可辨的通用文本、结算后标题变为 B；candidate 侧用同 seed 和同物理输入运行，结算后标题仍为凯尔希。两帧之间不得有任何能合法改变目标的玩家动作；触发角色或帧序不同则整对作废。原始 save99 哈希未改变，限定搜索未编辑候选或存档。

## Publication blocker

提交 PR 前由玩家确认：非当前交互目标 NPC 的纸娃娃地文恢复原目标后，按现有 Web 路由注释进入 NPC 小对话框，而不是继续因泄漏进入主对话框。
