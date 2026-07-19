/investigate-game-bug

请以怀疑视角裁决 T7 在你选定的静态状态机步骤中遇到的最后矛盾。不要把静态“应当进入”当成运行事实，也不要建议继续扫 seed。

请读取：

- `openspec/changes/fix-talk-common-state-leaks/fable-target-seed0-counterevidence-review-ruling.md`
- `openspec/changes/fix-talk-common-state-leaks/target-scope-save99-v-reachability.md`
- `/tmp/erark-t7-seed-search-20260715/seed-00-choice4-bound.log`
- 当前上游 `character_behavior.py`、`handle_npc_ai_in_h.py`、`handle_npc_ai.py`、状态机 target91/92、`settle_behavior` 的 effect dispatch 与 `Character_Event.json`。

已验证事实：

1. save99 中 Theresa56/Lin4080 都在同场、is_h、旧 behavior418、flag0、未束缚/未疲劳/未昏迷；玩家 group_sex_mode=true、type1、A/B模板为空。
2. 静态链显示 type1 hook 对不在模板者设置 masturebate flag3、异常bit1并把旧行为覆写 SHARE_BLANKLY；随后 NPC 进入 find_character_target。H门允许 group+flag3，target91 前提按现有读取均真，state machine92 应把新行为设为418，随后同次 judge_character_status 开始时结算。
3. 上游 `Character_Event.json` 没有任何 behavior_id=`masturebate` 事件，因此 type0前置事件不会跳过418指令效果。418进入正常 settle 后 effect524 必经。
4. 但完整 seed0 日志对 Theresa/Lin 都记录 effect_parts=[]、0次 handle_masturebate_add_adjust、无绝顶。现有 probe 包装 `handle_npc_ai_in_h.evaluate_npc_body_part_prefs`；真实524 dispatch 是 `constant.settle_behavior_effect_data[524]` 的 decorator wrapper 再调用该模块属性。未发现明确早绑定旁路，但现有日志没有直接记录实际新 behavior id 或 dispatch effect_id。
5. 发现面板真实选择[4]，口上普通且 target始终3，不是解释。

唯一候选诊断：只重跑 seed0 一次，保持完整 startup/load/CID213设置/一次6001/两个[4]，不做seed范围。观察压缩为两类现有值：

- 在 state machine 返回后记录 Theresa/Lin 实际选中的 target id、behavior id、masturebate flag和 premise_data[91]；
- 在通用 `settle_behavior.handle_instruct_data` effect dispatch 处记录这两人的实际 effect_id 序列，直接确认是否出现524。

不包装 effect524实现、不改变返回值/异常、不额外求前提、不逐条记录 RNG函数；记录前后验证Python/NumPy RNG state且内存缓冲。成功会区分“未进入418”与“进入418但旧probe漏记”；失败/行为扰动则冻结 save99 路线。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头。PASS 时给最小硬门禁；REVISE 时只改一项观察边界；BLOCKED 时说明为什么这一次诊断仍不能消解矛盾。不要写 PR 文案，不要提出其他路线。
