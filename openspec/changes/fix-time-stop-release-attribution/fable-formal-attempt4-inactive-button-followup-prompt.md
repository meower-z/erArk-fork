# Fable prompt: attempt 4 inactive old-button follow-up

Invocation contract: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Exact prompt follows.

```text
/investigate-game-bug

你是 erArk“时停解除结算归属”任务的独立监督者。你上一轮给出 `REVISE`，要求在仍存活的 disposable baseline-only rehearsal 中只点一次回翻旧 H grid 上可见的 `[4115]`。执行严格失败，现请基于新证据作最后路线决定。不要维护上一轮建议的面子；请重新比较最小、可信、可重复的 formal matched A/B 路线。候选代码方向和已投入时间都不能降低门槛。

## 上一轮的唯一补证指令

你要求：从 `r1-55` 测量可见 `[4115]` 中心，只点一次；零输入等两张字节相同稳定画面；如果不进入 release/结算流程就禁止重试或换坐标，截图记 log 后回来。

## 严格执行结果：旧页按钮无响应

- 输入前 unit 仍为 active/running，MainPID 889457、InvocationID `375e5003ad3c44779f1e283f26d18d84`，原四个 PID 都在同一 cgroup；没有重启。
- 输入前 `r1-56` 与 `r1-55` 字节相同，SHA256 `07410fe32dd01ca7b219d1c3744d05e68eb22f1356030c115b138544b875b3b1`，AE 0。
- 可见 `[4115]在H中取消时停` 的文字 bbox 约 `x=4..194, y=326..347`，使用安全中心 `(99,337)`。
- 只发出一次 `xdotool` click transport，坐标回读正确，命令 rc=0。
- `r1-57` immediate、`r1-58` passive、以及再等一秒零输入的 `r1-59` 全部与输入前逐字节相同，仍是 SHA `07410fe3...`、AE 0。旧 grid 和 `[4115]` 仍可见，没有 release 或结算页。
- 执行者立即 STOP；没有重试、换坐标、signal、Return、sample3、关闭或停服务。
- 主协调者按 1238×937 原图复核 `r1-59`，确认画面确实完全未变。
- append-only action log 新 SHA256 `14301afe48ffa483d9cc50bb50bc7c7ce2a24ad18257ee6b55df7468753ec2fc`。
- 更新后的 rehearsal manifest SHA256 `47286947a29115bcc185c6c117ff552480207478cb187a8e8d298323a7391871`。

因此，回翻到更早输出页的按钮文字只是可见，已经不是当前可响应的输入端点。上一轮认为“惊蛰证明循环免费地位于通往 [4115] 的路径上”被这个运行事实推翻：循环本身可做，但从那里还必须另加一条已验证的 viewport 返回路线，才能回到 callback 仍活跃的底部 H 菜单。

## 两个诚实选项

### 选项 A：删除 post-switch 可读证明循环，重做一次最终单侧演练

正式路线在点击 `[惊蛰]` 后等待 callback 把视口带回底部，取两张字节稳定图，然后 sample 2。sample 2 已经正面证明 `target_id=306`，全体非默认 trigger map 只有林 4080，且林的 counts、shoot position、experience、is_h 与 sample 1 完全不变；正常 UI 点击惊蛰的 transport 和点击前可读名单也都有逐帧记录。随后直接点击当前底部、当前回调绑定的 `[4115]`。

为满足你“终点必须演练”的要求，可关闭当前失败 run1，新建 disposable baseline rehearsal run2，从头重放已经验证的完整路线，走到 post-switch bottom/sample2 后不再上翻，直接只点一次活跃 `[4115]`，冻结其第一张稳定 release anchor；该结算永久只作诊断。run2 任一既有 anchor 不符即停止，不补输入。

代价：正式 PR-facing 画面不再另有“惊蛰高亮+状态”帧；但 observer 是可审计的内部正证，点击前名单可读，且正式 baseline/candidate release 页面本身能展示错误归属与正确归属。路线更短，减少 UI 脆弱性。

### 选项 B：保留 post-switch 可读证明循环，新增 viewport 返回演练

从 `r1-53` 的“名单+惊蛰高亮+状态”页，必须再找一条正常 scrollbar route 回到底部当前 H 菜单，然后点活跃 `[4115]`。可以另做单侧探索，例如测量 thumb 后一次 drag-to-bottom；但目前没有任何 down-route transport 已被验证。它会增加至少一个新的坐标/drag anchor，并需要先探索再从头完整重放，formal 两侧也必须完全一致。

代价：多一张人类直接可读的惊蛰选择图，但也多一条尚未知是否稳定的交互路线。不能再用旧 H grid 的失效按钮。

主协调者在新证据下倾向选项 A，因为 sample 2 是更强的当前状态证据，而额外滚动只服务展示、不服务 bug 触发；但你拥有最后决定权。如果你认为 reviewer-facing 可读选择证明不可替代，请选 B 并明确最小允许探索。

## Observer 更新

依照你上一轮要求，新的 `/tmp/erark-t4-formal-observer-attempt4.py` 已对称输出 `lin_4080` 和 `jingzhe_306` 的 experience IDs 10/20/78/111/156、counts、shoot position、is_h，同时保留全体非默认 `npc_states`、target、player H、time stop、sample index。它没有写状态；`py_compile` 通过；SHA256 `e33cfec89f0461ccfc6fb4533bada52ed40586eb18875031cc8f8f29b8031020`。独立只读审查逐行确认旧字段保留，并用假角色执行 helper，证明零 count 过滤、缺经验补 0、原对象不变、排序 JSON 可重复；结论 `PASS`，建议原样冻结。

## 请作决定

1. 给 `ROUTE A PASS`、`ROUTE B PASS`、`REVISE` 或 `FAIL`。
2. 若选 A：是否要求新建 run2 从头重放并实际点击底部活跃 `[4115]` 一次，成功后即可冻结 formal；还是当前已证明到 sample2 的 run1 加上正式侧“点击后 anchor 不符即作废”已足够？
3. 若选 B：明确唯一允许的下一轮 scrollbar 探索动作和成功 anchors；不要授权自由尝试多个坐标。
4. 明确正式 evidence 是否仍需要“惊蛰高亮+状态”PR-facing 图，还是 sample2 对称 observer + 点击前可读名单 + matched release 画面足够让人类审稿者理解 A/B 目标切换。
5. 新 observer 字段是否满足你上一轮要求；若独立代码审查 PASS，是否可直接用于新的 run2/formal prereg。
6. 是否需要玩家现在介入？这里仍不改变玩法语义，也不做外发动作。
```
