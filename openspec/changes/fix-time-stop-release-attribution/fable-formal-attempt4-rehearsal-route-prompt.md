# Fable prompt: attempt 4 viewport rehearsal route ruling

Invocation contract: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Exact prompt follows.

```text
/investigate-game-bug

你是 erArk“时停解除结算归属”任务的独立监督者。请以怀疑视角裁定一次 disposable baseline-only 正常 Tk 路线演练，决定正式 matched baseline/candidate A/B 之前还缺什么。不要因为候选代码已有 CODE PASS、演练最终找到了可用画面、或任务耗时较长而降低标准；也不要把本次 baseline-only 演练当作正式结果证据。若我们的路线解释有误，以你的决定为准。请只要求能改变可信度的最小补证。

## 已生效的前序裁定

- attempt 3 baseline 因正式预注册遗漏了七次有因果作用的滚轮输入而无效，只能作为诊断材料。
- 你要求先在当前 upstream baseline 上做隔离的单侧 viewport rehearsal，找出并完整重放“从底部 H 菜单切到惊蛰、可读证明惊蛰被选中、回到可见 [4115]”的正常 UI 路线；正式 A/B 必须另建新目录和预注册。
- A=林 4080，B=惊蛰 306；release 前林必须有 `counts={0:1,21:2}`、`shoot_position_body=2`，当前目标 306，时停和玩家 H 均为 true，且不能有其他 NPC trigger。

## 演练隔离与运行身份

- current-upstream baseline commit: `abebf33b52ebf51424f71365946eb8df1f75a23c`
- runtime: `/tmp/erark-t4-formal-current-20260714-attempt3/baseline`
- seed `5270714`; `PYTHONHASHSEED=0`; geometry `2100x1100x24`
- baseline `Script/Settle/default.py` SHA256: `ecdec42b79d393e3dc5deb0d88f1ca897d052d08ffc99c0389ab2c1ce7278be5`
- observer SHA256: `31932118bf625d122807cafcd3de4a7a28eaa968cae631829d83b8c942326ab9`; it reports every NPC with positive deferred count or non-default shoot position plus Lin's selected experience values
- launcher SHA256: `c67736d2db13b7236fd7069616211a8e8fe8804c60f21dbc309f34a246bf71a4`
- service remains active with InvocationID `375e5003ad3c44779f1e283f26d18d84`; no restart occurred
- manifest SHA256: `bf088540f196bd2ec1f5c805efeccad69b99a6436c9062562e1137af7c4cbc2f`
- corrected append-only action log SHA256: `9a11572ad999e1126b9d775f588b99b946bca436ca7f4b8681c4bead11bb0b6e`
- launcher log SHA256: `e9a593febf271a503a5cfe5a0cb49ef303602f389903eae7cfa3e1f5ced5dbcd`
- save files were copied from the frozen source; no save action was issued

## 从头正常 UI 路线

本次单侧演练从 slot 5 开始，正常执行 `[4113]` 开时停、`[5052]` 进入无意识奸、Return，然后四轮 `[6602]` 口交。前三轮没有射精面板；第四轮首次出现 `[忍住]/[射出]`，只点击一次 `[射出]`。画面可读地显示“在林的口腔射精，射出了20ml精液（醒来第一发+）”，随后回到稳定底部 H 菜单。

sample 1 原文：
`EVIDENCE_FORMAL_STATE={"lin_4080": {"counts": {"0": 1, "21": 2}, "experience": {"10": 7, "111": 0, "156": 9, "20": 97, "78": 9}, "is_h": true, "shoot_position_body": 2}, "npc_states": {"4080": {"counts": {"0": 1, "21": 2}, "is_h": true, "shoot_position_body": 2}}, "player_is_h": true, "sample_index": 1, "target_id": 4080, "time_stop_mode": true}`

从稳定底部 H 菜单开始：

1. 点击 scrollbar trough window-relative `(1228,500)` 一次；稳定画面 `r1-43/44` 显示林的身体/状态区域，SHA `affbd3bd...`。
2. 保持同一坐标再点一次；稳定画面 `r1-45/46` 可读显示场景名单 `[林] [惊蛰] [凯尔希] [可露希尔]`，其中林选中，SHA `b32265d7...`。
3. 在经过被动稳定重拍后，只点击一次可读 `[惊蛰]` 的测量中心 `(515,589)`。立即截图仍是 hover/旧内容，所以没有重试；稍后的两个零输入画面 `r1-49/50` 字节相同，已经回到底部 H 菜单，SHA `eea82d5e...`。
4. sample 2 原文：
`EVIDENCE_FORMAL_STATE={"lin_4080": {"counts": {"0": 1, "21": 2}, "experience": {"10": 7, "111": 0, "156": 9, "20": 97, "78": 9}, "is_h": true, "shoot_position_body": 2}, "npc_states": {"4080": {"counts": {"0": 1, "21": 2}, "is_h": true, "shoot_position_body": 2}}, "player_is_h": true, "sample_index": 2, "target_id": 306, "time_stop_mode": true}`
5. sample 1→2 中林的完整对象和全体非默认 NPC trigger map 逐字节不变，只有 sample index 和 target ID 变化。

## 切换后的可读证明与一个纠正过的误判

sample 2 后的底部 H 菜面与 sample 前字节相同。为完整重放 viewport 路线，执行者又从底部开始：

1. 在 `(1228,500)` 点 trough 一次。`r1-52/53` 字节相同，SHA `2883d5c4...`。执行者最初只把它记为“惊蛰状态/身体 + portrait tops”。主协调者随后按 1238×937 原图复核，发现画面顶部其实已经完整可读 `当前位置的角色一览: [林] [惊蛰] [凯尔希] [可露希尔]`，`[惊蛰]` 高亮，另有惊蛰名称、状态和身体行。执行者独立按原图复核后同意，并只向 action log 追加了解释更正，没有改写历史 transport。
2. 执行者原先预期第二次同坐标点击才出现名单，于是又在 `(1228,500)` 点了一次。`r1-54/55` 字节相同，SHA `07410fe3...`。它没有显示名单，而是翻得更早，显示一页 H 指令 grid，其中 `[4115]在H中取消时停` 清楚可见。执行者依照当时的 literal anchor rule 立即停止，没有临场补操作。

因此事实是：第一下已经完成“名单可读 + 惊蛰高亮 + 惊蛰状态”证明；第二下不是随机漂移，而是继续向更早输出翻页，并让另一个 `[4115]` 可见。没有再次点目标，没有 sample 3，没有点 `[4115]`，没有取得 baseline release 结果，没有关闭窗口或停止服务。

## 我们当前的疑问（请你作最后决定）

1. 给出 `REHEARSAL ROUTE PASS`、`REVISE` 或 `FAIL`。这次演练是否已经满足你对 attempt 4 预注册路线的单侧前置要求？
2. 如果 PASS，是否批准冻结以下正式路线：sample 1 后从底部同坐标 trough 点两次 → 在可读名单只点一次惊蛰 → 等待底部画面两次无输入字节稳定 → sample 2 硬门槛 → trough 点一次，要求同屏出现四人名单、惊蛰高亮和惊蛰状态 → trough 同坐标再点一次，要求 H grid 和 `[4115]` 可见 → 正式侧才点击一次可见 `[4115]`？任一 anchor、面板轮次或 sample 状态不符即整侧无效，不能补输入。
3. `r1-55` 中的 `[4115]` 来自更早输出页，虽然可见，但本次演练没有点击验证它仍绑定当前 callback。正式 A/B 能否把“点击它后必须进入预期 release 页，否则整对作废”作为足够严格的首次验证；还是必须先在这个 disposable baseline rehearsal 中点击它一次、把由此得到的任何结算画面永久排除为正式证据，然后再新建正式目录？
4. 如果还需补演练，请明确最小步骤。当前窗口仍原样存活在 `r1-55`，没有更多输入；可以按你的决定继续一次，或直接关掉并重开全程。不要默认可以随意尝试多个坐标。
5. 正式 A/B 是否必须保留切换后的可读惊蛰证明循环？内部 sample 2 已证明 target 306 且林不变，但画面证明可以让人类审稿者看懂目标切换。若你认为它增加脆弱性而不增加可信度，请明确删除；若保留，请明确上述一次上翻是否足够。
6. 既有 formal observer 是否足够：它显示全体非默认 trigger NPC、林的经验快照、target、H 和时停；还是正式前还需加入某个特定字段？
7. 是否需要玩家现在介入？这只是证据路线，不改变玩法语义，也不做外发动作。
```
