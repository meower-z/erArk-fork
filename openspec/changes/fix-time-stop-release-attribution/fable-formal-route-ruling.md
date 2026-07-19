/investigate-game-bug

你是 erArk“时停解除结算归属”任务的正式 Tk 路线监督者。当前只请审查：这次正常 UI 探索是否足以批准一条 exact matched baseline/candidate A/B 路线。不要因为候选代码已得到 CODE PASS、探索耗时较长或结果方向符合预期而降低门槛；也不要把探索成功当成正式 A/B 已成功。若证据仍有缺口，请指出最小补证，不要泛化要求。

## 已生效的既有裁定

- 原一 NPC 路线已作废：`judge_before_pl_behavior()` 会在 effect 527 前清掉当前对象的 `shoot_position_body`。
- 多目标路线只有在正常 UI 切到 B 后仍保留 A 的正 deferred counts 与 `shoot_position_body` 时，才可进入正式 A/B。
- attempt #1 是结果出现前的外部 SIGTERM，已获 `RESTART EXPLORATION PASS`。
- attempt #2 读档默认对象实际为林 4080；首次正 count 出现后，你裁定 `CONTINUE WITH LIN PASS`，并冻结林为 A、惊蛰 306 为 B。正式重放不得补点可露希尔。

## 冻结环境

- 探索 baseline：`06fc59c1e71d092224375fc4a096b956aea2ad63`。
- 探索 `Script/Settle/default.py` SHA256：`ecdec42b79d393e3dc5deb0d88f1ca897d052d08ffc99c0389ab2c1ce7278be5`。
- Observer SHA256：`870dca54b465fa2bfc62eb044a7d7f69a70e0d4e7986a969d902b9fddabdf500`。
- seed `5270714`；`PYTHONHASHSEED=0`。
- 来源 `save/8` 与运行后的 slot5、slot95 均保持：file 0 `a91afea82d91981bd14e40f9b3dc7ffa6392627951187d227b7b10443e1af981`；file 1 `45e77cfecf83ebecc980eece54b14eb981946b2f2a2af094f48e7e5844b8fdac`。
- launcher log SHA256：`c6f3b6e23b8aa592f28c84cd8d23168063d4e1ab2613f02896281a41b88d2585`。
- action log SHA256：`ebe0726a3c0122dea13975afb709e359f1b3dc9801ed5aa0263c29f6dfea1de6`。
- 更新后 manifest SHA256：`ffa0ea0858ad0dd6300fbf9a8f4a4b8ebb2f7cb11065499d92cf09ce01ac4530`。
- launcher 只有一次预期 zoomed fallback；没有 traceback、Exception 或额外 TclError。运行结束后相关 Tk/Xvfb/observer 进程均消失，allocator 三槽全空。

## 正常 UI 探索结果

从 save/8 的默认林目标开始：

1. 正常读档。
2. 执行 `[4113]` 开时停。
3. 执行 `[5052]` 进入无意识奸并 Return。
4. 连续执行四次 `[6602]` 口交：前三次没有射精选择；第四次出现正常 `[忍住]` / `[射出]` 面板，选择 `[射出]`；可读画面写明“在林的口腔射精，射出了20ml精液（醒来第一发+）”。
5. 回到 H 菜单后，切换前 observer 原文为：
   `EVIDENCE_TRIGGER_STATE={"npc_states": {"4080": {"counts": {"0": 1, "21": 2}, "is_h": true, "shoot_position_body": 2}}, "player_is_h": true, "target_id": 4080, "time_stop_mode": true}`
6. 只通过正常场景角色列表点击 `[惊蛰]`。原尺寸画面可读地显示惊蛰被选中及惊蛰状态行。
7. 纯滚动回到指令区；`[4115] 在H中取消时停` 仍清晰可见且可点。
8. 切换后 observer 原文为：
   `EVIDENCE_TRIGGER_STATE={"npc_states": {"4080": {"counts": {"0": 1, "21": 2}, "is_h": true, "shoot_position_body": 2}}, "player_is_h": true, "target_id": 306, "time_stop_mode": true}`
9. 两次 observer 中林 4080 的完整对象逐字节相同，只有 `target_id` 从 4080 变为 306。Observer 只列出有正 count 或非默认射精位置的 NPC，所以惊蛰不出现在 `npc_states` 中不是“切换时执行了行为前清理”的证明；静态调用顺序仍是下一条 `[4115]` 行为开始时只清当前 B，不清 A。
10. 探索没有点击 `[4115]`，没有观察 baseline 结算，也没有保存游戏。

关键原尺寸帧均为 `1238x937`：

- `a2-22-oral4-shoot-selected.png`：正常射精选择与林口内射精文字，SHA256 `101c5676b3170f79f8f60a32b33df497711479b155dee8738fbf858d296f2674`。
- `a2-35-scrollbar-page-up.png`：`[林]` 被选中，SHA256 `06b06047ed22d8b82c5d6bad921920970af980e383b3c948629e2bfa0e64237b`。
- `a2-37-jingzhe-proof-scroll.png`：`[惊蛰]` 被选中及惊蛰状态行，SHA256 `2883d5c41d07a3ac301152fc28c486ccca98c9297d9dabf76f2d27d3907b55a1`。
- `a2-38-scrollbar-page-down.png`：切换后 `[4115]` 可见，SHA256 `88eeaf1cf93143e549c77b378df29aa67b0831a5eee8df144b1fcdc5b524ee92`。
- `a2-39-post-signal-preserved.png`：observer 后无输入重拍，与上一帧字节相同。

1800 秒 root cell 在上述 post-switch observer 和保留帧都写入之后到达预先记录的上限。正常 WM 关闭请求使 Tk 窗口消失；随后只精确 TERM 该次孤儿 PGID/PID。这是证据完成后的预知时限，不是结果出现前的未知中断。

## 当前 upstream 漂移

当前 `upstream/master` 为 `abebf33b52ebf51424f71365946eb8df1f75a23c`。从探索 ref 到当前 upstream，Git 只显示 `Script/Design/talk.py` 改动（#214）。正式 baseline/candidate 都拟基于当前 upstream 重新构建，并从同一原始 save、seed、launcher 开始；不会把旧探索 runtime 当正式 baseline。

## 正式 A/B 的预注册结算差异（供你判断是否还需补路线证据）

已按实际源码单独推导：在林 `counts={0:1,21:2}`、`shoot_position_body=2` 时，effect 527 唯一可区分的直接记录是经验 78 无意识绝顶 `+1` 与经验 111 饮精绝顶 `+1`。Baseline 把两者显示在玩家 root 组；candidate 把两者归到林组。林真实经验增量与各经验 ID 记录总量两侧必须守恒。后续 generic pass 两侧共同；林的最终经验 78 行在 candidate 中会因迁入该直接 `+1` 而比 baseline 林组大 1，不能误要求该行完全相同。这些只是待验证预期，不是现有正式 A/B 结果。

## 需要你裁定

1. 给 `FORMAL ROUTE PASS`、`REVISE` 或 `FAIL`。现有证据是否足以批准正式 matched Tk A/B，而不是批准候选结果？
2. 若 PASS，请明确冻结：A=林 4080，B=惊蛰 306；四次口交，第四次选择射出；release 前预期状态为林 `counts={0:1,21:2}`、`shoot_position_body=2`、当前目标 306、时停与玩家 H 均为 true；baseline/candidate 任一项不一致即整对无效，不得调整轮次。
3. 探索为了找角色列表用了七次滚轮、一次已证明无效的 Page Up，随后才发现可直接点滚动条。正式路线应完整重放这些探索性视口输入，还是预注册较短视口路线“点滚动条上方 → 点惊蛰 → 点滚动条下方”，并保证 baseline/candidate 使用相同有意义输入？请明确选择，不要默认两者等价。
4. 探索发生在旧 ref，正式两侧会基于当前 upstream。已知唯一版本差异是 `talk.py`。在当前 upstream 上从头完成同档、同 seed、同动作的 matched A/B 是否足够，还是必须先额外做一次当前 upstream 单侧路线探索？
5. 正式 A/B 是否还需补充任何 pre-release 状态证明？特别是：是否接受“可读惊蛰选择帧 + post-switch `target_id=306` + 林状态不变 + `[4115]` 可见”作为点击 `[4115]` 前的完整 gate？
6. 探索按你此前要求没有点击 `[4115]`、没有取得 baseline 结算页。是否确认这是正确隔离，正式结算页应只来自预注册后的 matched A/B？
7. 是否需要玩家现在介入？这里没有提出玩法语义变更或外发动作。

## Fable verdict（逐字保存）

**FORMAL ROUTE PASS。** 逐项裁定如下：

**1. 是否足以批准正式 matched A/B——是。** 此前设定的准入条件是"正常 UI 切到 B 后仍保留 A 的正 deferred counts 与 `shoot_position_body`"。两次 observer 中林 4080 对象逐字节相同、仅 `target_id` 变化，配合可读的惊蛰选中帧与 `[4115]` 可见帧，恰好证明了这一条，且证据链（seed、save 哈希、observer/launcher/action log 哈希、无 traceback、槽位清空）完整。此 PASS 批准的是**路线**，不是候选结果——正式 A/B 的结算差异仍待验证。

**2. 冻结确认。** A=林 4080，B=惊蛰 306；`[4113]` → `[5052]` → 四次 `[6602]`，第四次选 `[射出]`；点击 `[4115]` 前状态必须为：林 `counts={0:1,21:2}`、`shoot_position_body=2`、`target_id=306`、`time_stop_mode=true`、`player_is_h=true`。baseline/candidate 任一侧任一项不符即整对无效。补充一条边界：若某侧第四次 `[6602]` 未出现射精面板（如 talk.py 的 RNG 消耗漂移所致），这是**路线失效**，须停下重新报备，不得现场加减轮次后继续。

**3. 预注册短视口路线。** 采用"点滚动条上方 → 点惊蛰 → 点滚动条下方"，两侧输入序列完全一致。探索期的七次滚轮和无效 Page Up 是发现噪声，重放它们不增加证据、只增加失败面。滚动是纯视图操作，前提是每次点击仍从当前帧确认目标可见——若短路线某帧与预期不符，停下重拍评估，不得盲点。

**4. 无需额外单侧探索。** 唯一漂移是 `talk.py`（#214），不触碰结算与状态路径；两侧同基于当前 upstream，天然 matched。正式运行自身的 gate 帧（第 2 条冻结项）就是对新 ref 上路线有效性的检验——gate 不过即整对作废并回来报备，这比强制一次上游探索更省且同样安全。

**5. pre-release gate 接受。** "可读惊蛰选中帧 + post-switch observer `target_id=306` + 林对象与切换前逐字节相同 + `[4115]` 可见帧"即为点击 `[4115]` 前的完整 gate，两侧各自满足且互相可比。不追加要求。

**6. 隔离正确。** 探索不点 `[4115]`、不取结算页是对的；正式结算页只能来自预注册后的 matched A/B，探索 runtime 不得充当任一侧。

**7. 不需要玩家介入。** 无玩法语义变更、无外发动作；预注册的结算差异预期（78/111 归组迁移、总量守恒、林 78 行差 1）留待正式结果对照后再裁定。
