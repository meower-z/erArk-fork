/investigate-game-bug

你是 erArk“时停解除结算归属”attempt3 正式 matched Tk A/B 的怀疑型监督者。请只根据下面新出现的正式运行事实裁定，不要为了保住已耗时的 baseline 而降低冻结门槛，也不要因为这是视口操作就默认任何补输入无害。Candidate 尚未启动，baseline 尚未点击 `[4115]` 或看到 release 结果。

## 已冻结规则

你以 draft SHA256 `6351253194decb1496b4999c58fcebda4e752ff573ab455148e6b794b892e84f` 给出 `ATTEMPT3 PREREG PASS`，其中冻结：

- sample1 后四步视口路线：第一次点滚动条 thumb 上方以露出角色列表；点可见 `[惊蛰]`；再点 thumb 上方取得可读惊蛰选中/状态帧；点 thumb 下方回到可见 `[4115]`。
- 每步都必须先从当前帧确认目标可读；布局或目标不符即停，不得临场换坐标或路线。
- discovery-only 七次 wheel-up 和一次无效 Page Up 明确不重放。
- pause 期间零游戏输入；若需要路线外输入，该侧作废。
- baseline 完整三样本、release 帧、正常关闭、save/allocator/log/hash 全部通过后，candidate 才可启动。

你更早的 `FOUR-STEP ROUTE PASS` 是根据探索帧 `a2-35` 到 `a2-38` 作出的。当时给你的摘要没有把一个关键前置关系说透：`a2-35` 的第一次 track-above 点击并不是从 H 菜单最底部直接发生；此前已经有七次有效 wheel-up，画面从 H 菜单逐步滚到“三张立绘和选择箭头可见”，另有一次无效 Page Up。随后 track-above 点击才到达可读角色列表。正式 prereg 后来明确删掉这些 discovery-only wheel inputs，却仍把一次 track-above 写成足以露出列表。

## attempt3 当前事实

- baseline service 仍正常存活：InvocationID `c5fa7fa8fa204e8c8e8ebd25d1b45da5`，MainPID `850970`；没有超时或异常退出。
- 已按冻结路线完成读档、开时停、进入无意识 H、四轮口交；第 4 轮首次出现射精面板并点 `[射出]`。所有实际页面均有零输入稳定复拍。
- sample1 恰好一次并通过：
  `EVIDENCE_FORMAL_STATE={"lin_4080": {"counts": {"0": 1, "21": 2}, "experience": {"10": 7, "111": 0, "156": 9, "20": 97, "78": 9}, "is_h": true, "shoot_position_body": 2}, "npc_states": {"4080": {"counts": {"0": 1, "21": 2}, "is_h": true, "shoot_position_body": 2}}, "player_is_h": true, "sample_index": 1, "target_id": 4080, "time_stop_mode": true}`
- sample1 后，从可见 `[4115]` 的底部 H 菜单帧，执行者只做了冻结 step1：在当前帧确认 `(1228,500)` 位于 bottom thumb 上方的 track，移动一次并点击一次。
- `b3-40-viewport-step1-above-track.png` SHA256 `affbd3bd98e4904a62b009736fed3de91b11f4dd6a0a1db5fc462f8a70594899`。原尺寸 `1238x937` 可读内容是林的状态/身体文字与角色立绘；没有当前地点角色名字列表，也没有可读的选中 `[林]`。
- 零输入复拍 `b3-41-viewport-step1-passive-recapture.png` 与 b3-40 字节相同，AE=0。
- action log SHA256 `b03c7d1393b9370d012eb7876747ef332c4d0ba4fbafca765eb59a88363d2ab7`，逐字记录 required list absent 后立即停止。
- 此后没有任何 alternate track click、wheel、目标点击、sample2、`[4115]`、service stop 或 candidate launch。

对比旧探索：

- 探索从 H 菜单先执行七次 wheel-up，最终 `a2-33` 显示三张立绘和选择箭头，但仍无名字列表。
- 一次 Page Up 无效，帧不变。
- 之后第一次 track-above 才产生 `a2-35`：角色列表可读、林选中。
- 所以 attempt3 b3-40 与 a2-35 的差异不是随机等待页分段，而是 prereg 删除了 a2-35 的有效滚动前置输入。

## 请裁定

1. 给出明确 verdict：attempt3 baseline 是 `INVALID`、可以 `CONTINUE`，还是需要其他处置。不要把“视口不改游戏数值”和“冻结路线允许补输入”混为一谈。
2. 若判 INVALID，请明确当前 live service 的最小合规收尾：是否应先按 InvocationID 导出 pre-stop journal、保全 b3-00..41/action log/sample1，再正常 WM 关闭或 coordinator stop，导出 post-stop journal、验 save/allocator/hash；这些材料应只作 diagnostics 还是可复用任何正式结论。
3. 若允许 CONTINUE，请逐字定义现在允许的下一次物理输入、为什么不违反“路线外输入即该侧作废”，以及 candidate 必须如何完全匹配；不要给执行者可变次数的临场滚动自由。
4. 若需要 fresh attempt4，请冻结一个不会重现此歧义的 exact viewport route。请从证据中选择或提出更严格方案，例如：
   - 重放探索已知的七次 wheel-up，再按四步 track/name/track/track；
   - 从 H 菜单连续两次固定 track-above 后再点惊蛰（这条目前只实证到第一次，不应未经你判断就视为已证明）；
   - 先做与正式结果隔离的新单侧纯视口探索，再预注册 exact route；
   - 或你认为证据支持的另一条固定路线。
   请说明是否需要先验证 route，而不是让正式 attempt4 再承担探索。
5. attempt3 的口交分页异常已由你分别裁为可继续；这次 viewport mismatch 是否影响那些历史裁定，还是仅影响 attempt3 的正式效力？
6. 是否需要玩家介入？这里没有玩法语义选择、生产代码变更或外发动作。

请以怀疑视角检查：最重要的是让未来人类读者相信 baseline/candidate 真是预先固定、完全匹配的运行，而不是为了走到结果临场补路线。
## Fable verdict（逐字保存）

## VERDICT: ATTEMPT3 BASELINE INVALID(正式效力作废,材料降级为 diagnostics)

### 1. 裁定与理由

**INVALID。** 判定依据不是执行者犯错——执行者严格按冻结规则执行了 step1、确认目标不符、立即停止、零污染,这是模范执行。作废的是**冻结路线本身的前提为假**:prereg 把 a2-35 的"一次 track-above 即露出角色列表"当成独立事实写入,但 a2-35 的可读列表在因果上依赖此前七次 wheel-up 建立的滚动状态。把因果必需的输入归类为"discovery-only 不重放",是路线设计错误,b3-40 是这个错误的直接实证反驳。

不能 CONTINUE 的原因很简单:prereg 没有中途修订机制,而"现在补一个允许的输入"正是未来读者最会怀疑的操作——无论我如何逐字限定,它在记录上都是**结果出现分歧后临场改路线**。冻结门槛的全部价值在于路线先于结果固定;为了保住已投入的 baseline 而中途放行补输入,等于放弃这个价值。视口输入不改游戏数值,但 prereg 冻结的是**输入序列**,不是数值影响面。

sample1 虽然本身通过,但 prereg 要求"完整三样本+release 帧+正常关闭+全部校验通过"才构成 formal baseline。不完整的 baseline 没有部分正式效力;sample1 降级为 diagnostics。

### 2. 最小合规收尾(按此顺序执行)

1. 按 InvocationID `c5fa7fa8fa204e8c8e8ebd25d1b45da5` 导出 pre-stop journal。
2. 保全 b3-00..41 全部帧、action log、sample1 JSON,连同已记录的 SHA256。
3. 正常 WM 关闭(优先)或 coordinator stop;导出 post-stop journal。
4. 验 save/allocator/hash;确认 `tk_capture_slots.py status` 释放。
5. 归档到 diagnostics 目录,与任何 formal evidence 目录物理分开,并在 manifest 中标注 `attempt3: route-precondition falsified at step1, formally invalid`。

**用途限定:仅作 diagnostics 与路线设计输入。** 明确允许的复用:sample1 的状态 JSON 格式与字段可用于设计 attempt4 的采样断言;b3-40 是 attempt4 路线设计的关键反例证据。明确禁止的复用:任何帧或 sample 出现在 formal A/B 对比、PR 证据或结论性陈述中。

### 3. CONTINUE 条件

不适用(已判 INVALID)。

### 4. attempt4 路线冻结要求

**先做隔离的单侧纯视口探索(你列的第三方案),探索验证通过后再 prereg,正式 attempt4 不承担任何探索。** 理由排除其他方案:

- **重放七次 wheel-up**:不可直接冻结。探索时的滚动几何依赖当时的页面内容长度,而口交分页异常已经证明内容长度在运行间**可变**。wheel 次数是内容长度的函数,不是稳定路线。
- **两次连续 track-above**:只实证了第一次,第二次是猜测。未经验证的步骤不得进入 prereg——这正是 attempt3 死因的重演。

attempt4 流程冻结如下:

1. **Rehearsal run**(一次性、明确标注 disposable、与 formal 结果隔离):用相同 save/seed/几何走到与 post-sample1 等价的底部 `[4115]` 帧,然后逐帧探索视口路线,每步先看当前帧再选一个输入,直到实证一条从"底部 `[4115]`"到"惊蛰可读选中帧"再回到"可见 `[4115]`"的完整输入序列。
2. **端到端复验**:同一 rehearsal 内或第二次 rehearsal 内,从底部帧完整重放该序列一次,确认每步的可读目标复现。未通过复验的路线不得冻结。
3. **Prereg 新增两条硬规则**:(a) 路线中每个输入必须附带其因果必需的全部前置输入——禁止再出现"该输入是 discovery-only 所以删除"的分类,除非有零输入对照证明删除后目标帧仍可达;(b) 每步冻结的不只是坐标,还有该步执行前必须可读的锚定内容(如"当前帧底部可见 `[4115]`"),锚定不符即停,与 attempt3 相同。
4. **一个建议供 coordinator 决定**(不构成阻塞):如果惊蛰选中帧不是结论性断言的必要证据,attempt4 应删掉这段绕行,路线越短越稳。若必要,按上述流程冻结。

### 5. 对历史裁定的影响

**口交分页异常的可继续裁定不受影响,仍然成立**——它们针对的是不同机制(H 轮次内的分页表现),依据的是当时的证据,viewport mismatch 没有推翻其中任何事实。但有两点连带后果:(a) 这些裁定在 attempt3 内的实际效力随 baseline 作废而落空,attempt4 遇到同类异常时它们作为先例继续适用;(b) 分页异常本身是"内容长度运行间可变"的证据,这直接支持第 4 条中"wheel 次数不可冻结"的判断——两件事在因果上相互印证,而非相互削弱。

### 6. 玩家介入

**不需要。** 无玩法语义选择、无生产代码变更、无外发动作;收尾与 attempt4 rehearsal 均为可逆的本地证据工序。按本裁定自主推进。

---

**给未来读者的一句话记录**:attempt3 作废不是执行失败,而是 prereg 把一个依赖滚动状态的帧误当成单击可达;执行者在第一个不符帧零污染停机,证明了冻结机制本身在工作。
