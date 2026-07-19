**PASS**

## DOCS

`current-upstream-wait-lifecycle.md` PASS，我核对了原始证据而非只读文档：

- 归档 `SHA256SUMS` 全部校验通过；`pre-route-save-hashes.txt` 与 `post-route-save-hashes.txt` 两个 slot99 文件哈希逐一相同。
- `wait-lifecycle-trace.jsonl` 含 `outer_wait_entry`（`outer_wait: 1, behavior_id: wait, duration: 5`），且 grep 全文件无任何 `outer_wait_exit` 记录 —— 与文档一致。
- 我用 `view_image` 打开了 `frame-37-after-confirm-9-timeout.png`：清晰可读 `H中被发现`、`可露希尔发现了你正在和凯尔希等多人群交，要怎么做?`、`[1]用花言巧语支开对方`、`[4]邀请对方加入群交`、`[5]尴尬地结束H`。文档写的选项文本 `[4]邀请对方加入群交` 与画面完全一致（本次提问里写的"邀请加入群交"是转述省字，以文档和画面为准）。
- 九次 wait 的顺序、call site（`talk.py:552` / `manage_power_system_panel.py:243` / `character_behavior.py:270` / NPC 阶段）与 `wait-sequence.md` 及帧序号一一对应。
- Attempt 8 纠正的表述（退出一个 `WaitDraw` 即进入同一 outer update 的后续 wait，两帧不足以判定序列）与 Attempt 9 的实测结果自洽。
- INVALID 定性正确：发现面板是普通玩法分支，只是超出预声明合同；文档明确写了"discovery panel 不是失败证据"，没有把它当 bug。

无需修正。

## NEXT STEP

**允许**该单次有界路线续探，不冻结路线。理由：正式 A/B 要求 baseline/candidate 用相同物理输入到达匹配触发并回到可比较的静止帧；目前路线在第一次 `outer_wait_exit` 之前被一个普通选择面板截断，这是纯粹的路线未知量，不是证据缺陷。RNG 已冻结、save99 前后哈希不变、runtime 一次性——这一步完全可逆、无外发动作，不需要玩家决定。不写 PLAYER INPUT REQUIRED。

## BOUND CONTRACT

下一次尝试（Attempt 10）的完整合同：

1. **设置逐项不变**：unchanged upstream `72e2805`、pristine save99、seed 0、`PYTHONHASHSEED=0`、同一 evidence-only wrapper（安装前后 RNG fingerprint 必须再次相等）、tk-visual-runner + allocator slot、同样的逐帧 `view_image` 决策纪律。
2. **重放段**：从载入到第九次 wait，每一页必须与 Attempt 9 对应帧内容身份一致（同一角色、同一结算类型、同一动作文本）后才发那一次空 Return。任何一页身份不符 → 立即停止、不再输入、整次 INVALID（判定为确定性破裂），帧留作诊断。
3. **面板前置条件**：第九次 Return 后出现的面板必须与 frame-37 三要素完全一致——标题 `H中被发现`、正文点名可露希尔与凯尔希多人群交、恰好三个选项 `[1]用花言巧语支开对方` / `[4]邀请对方加入群交` / `[5]尴尬地结束H`。角色不同、选项集不同、措辞不同 → 不输入，INVALID。
4. **固定输入**：满足前置条件后，输入恰好一次 `4` + Return。此后不再允许任何选择输入。
5. **可接受结果（现在预先固定）**：可露希尔加入成功或拒绝/失败**均可接受**——seed 已冻结，出现哪个分支是确定的；路线图只要求记下它。条件是后续每一页都是普通 wait/信息页（逐帧确认后各发一次空 Return）。若在第一次 `outer_wait_exit` 之前出现**任何**再次的选择面板（无论何种），停止、不输入、本次对"完成路线"为 INVALID，但已映射的页仍是有效诊断数据。
6. **完成判定**：trace 中出现 `outer_wait_exit`（对应 `outer_wait: 1`）**且**当前帧经 `view_image` 确认是等待玩家指令的正常主面板。两者缺一不算完成。
7. **停止与无二次 6001 的证明**：完成判定成立后零输入——捕获最终帧、记录 post-route save 哈希、经 allocator 停止进程。证明链三重：chronological action log 中 `6001` 键序恰好出现一次；trace 中 `outer_wait_entry` 计数为 1；帧序列里指令输入页只出现一次。三者任何一处不符即撤回"无二次 6001"声明。
8. **归档**：与 Attempt 9 同格式（帧、trace、action log、manifest、SHA256SUMS、pre/post save 哈希），日期目录置于同一 archive 根下；归档校验后清理 task-owned `/tmp` runtime。

## EVIDENCE GATE

即使续探成功，其全部产出（trace、帧序、action log、outer_wait_exit 记录）**仍只是 route map**——它证明"从载入到第一次外层等待结束存在一条固定输入的确定性路线"，不证明 bug 存在或修复有效。

启动正式 baseline/candidate A/B 的充分条件：路线图覆盖从载入到第一次 `outer_wait_exit` 的每个输入，且合同能预先写出每一步的预期页面身份。A/B 本身即是路线确定性的最终检验——baseline 或 candidate 任何一侧偏离映射路线即整对作废，不需要在 A/B 之前再跑一次额外的确认重放。

A/B 的可接受证据只有一种形态：current upstream 上真实 Tk 的全分辨率前后对比图，baseline 侧可读地显示同一结算批次内寸止结果重复、candidate 侧显示单次，由 `view_image` 逐张检查确认可读、可比。trace、日志、哈希、旧版截图一律只是佐证，不能替代。本 bug 的可见症状是寸止结算重复，不适用"同一 NPC 连续两次 `H中被发现` 单图"硬门槛，走普通的前后图要求即可。
