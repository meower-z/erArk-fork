/investigate-game-bug

你是 erArk “时停解除结算归属”任务的最终技术范围监督者。一个 fresh-context 独立代码/规范审查给出 `REVISE`：生产 hunk 本身被认为最小且方向正确，但 OpenSpec 可能承诺了候选没有实现、也不该由本 PR 改变的后续二段/远处行为；测试也有一处函数注释缺失和几项过度表述。请从怀疑视角决定是扩实现/测试，还是收窄文档到真实 bug 边界。不要因为 Tk A/B 正在进行就默认代码已够，也不要因为规范写得漂亮就要求 scope creep。

## 当前生产候选

effect 527 遍历 NPC。原版用玩家 root `CharacterStatusChange` 调 `orgasm_settle(npc_id, root_change, un_count_orgasm_dict=...)`。候选仅在有任一正数计数时 `setdefault(npc_id, TargetChange())`，把该 NPC 的 `TargetChange` 传给真实 `orgasm_settle`；全零计数仍用原 root object 调 no-op，保留 `time_stop_release=True`、清零、清理。生产 diff 7 additions/2 deletions。

真实 registry test 直接执行 effect 527，覆盖零、单 NPC、多 NPC、远处 NPC；断言正数调用收到 `root_change.target_change[npc_id]` 的同一对象，真实 stored exp 与 target record 一致，Web collector 保留 character ID，计数/清理正确，无关假的 `unrelated_behavior` 仍留在 queue。它人工设 `shoot_position_body=2`，作为同步经验 owner 的代码级触发，不自称正常玩家路线；正常 Tk 路线另行证明 UI 可达。

## Fresh reviewer blockers

1. 现 spec 顶层写“deferred release and its follow-up effects in that NPC's target-owned settlement change object”；普通场景的 `handle_instruct_data()` 在 effect 527 后确实 `setdefault` 同一 target block 并跑 queued second behavior。但远处 NPC 在 `second_behavior_effect()` 的位置分支进入 `must_settle_check()`，那里新建并丢弃另一份 `CharacterStatusChange`，并不沿用 effect 527 的 `TargetChange`。这是上游既有的远处静默结算策略，候选未改变。Reviewer 认为 spec 的 follow-up/remote same-rules 承诺未实现。
2. 现零计数 scenario 写“no target-owned change block is created solely for that empty call”。在 effect 527 局部成立；但完整 `TIME_STOP_OFF` 后续通用循环会为所有 NPC 无条件 `setdefault` target block。因此若把 scenario 理解为完整行动，表述不真实。测试只直调 effect 527。
3. 现 scenario 写“unrelated queued second behaviors remain available for ordinary settlement”。测试注入一个不在真实配置中的 `unrelated_behavior`，只断言 effect 527 后它仍在 queue，没有执行普通二段结算。因此只能证明本 effect 不消费/覆盖无关队列，不能证明后续普通结算。
4. 远处 scenario 还写“exactly-once second-stage behavior follow the same rules”，同样可能把本 PR 扩成远处二段显示/owner 重构。
5. `AlwaysConfigured.get()` 是新增函数但没有中文参数/返回/用途 docstring，违反仓库规则，需补。
6. 两个 PO 文件是运行生成污染，必须在候选提交前从干净同 ref 恢复；它们不属于拟提交边界。
7. `shoot_position_body=2` 是代码探针人工触发。它只能证明 owner 机制；正常 UI 到达与可见归属必须由正在进行的 matched Tk A/B 提供，文档不能把代码探针单独写成正常玩法证明。

## 主协调者的初步判断（请独立裁定）

- Bug/PR 边界应是 effect 527 的**同步 deferred-release 变更归属**。它不应顺便重构上游远处二段行为或 generic pass。
- 顶层 requirement 应改成：effect 527 直接产生的 release changes 归 NPC target block；随后 generic second-stage pass 保持现有行为、不重复消费/不被此 effect 吞掉。只对同场景可见路径陈述复用 target block；对远处只陈述同步归属、清零/清理与现有静默路径不变。
- 零计数应明确限定“effect 527 不因空 no-op 自己创建 block”；generic pass 仍可能按既有逻辑创建空 target entry。
- 无关队列应只承诺“effect 527 不消费、不覆盖”，不宣称本测试验证了后来如何 settle。
- 代码/test只需补 `AlwaysConfigured.get()` 的中文 docstring；不为过宽文档扩大 production scope。PO 污染提交前恢复。

## 请裁定

1. `CODE PASS / DOCS NARROW`、`IMPLEMENTATION EXPAND` 或其他明确结论。若要扩实现，指出哪条是本 owner bug 的必需部分，而非相邻上游架构问题。
2. 给出 spec/design/tasks 必须如何收窄的精确语义，特别是 follow-up、zero-count、unrelated queue、remote NPC 四处。
3. 当前真实 registry test 在补 docstring 后是否足以覆盖代码边界？是否必须增加“完整 generic pass”测试；若必须，限定它要证明什么，避免测试另一个系统。
4. 人工 `shoot_position_body=2` 的合格文档措辞是什么；若 matched Tk A/B 最终证明正常 UI 可达，是否足以补齐玩家证据。
5. 是否需要玩家现在介入？这应是修复范围/证据判断，不是未决玩法语义。

## 调用前新增的运行路径事实

正式 A/B 尚未读档，现场停在空存档页，因此没有产生可用结果或改变存档。fresh reviewer 随后补齐了此前遗漏的真实调用顺序：

- 玩家执行 `[4115]` / `[4114]` 时，`character_behavior()` 会先调用 `judge_before_pl_behavior()`，再进入 effect 527。
- `judge_before_pl_behavior()` 会把**当前交互对象**的 `shoot_position_body` 和 `shoot_position_cloth` 重置为 `-1`。
- 当前真实 `orgasm_settle()` 在 deferred counts 路径中，唯一直接写进所传 `change_data`、因而能区分旧 root owner 与候选 target owner 的数值，是 `shoot_position_body in [2, 15]` 时的饮精绝顶经验；该经验还递归产生无意识绝顶经验。其余高潮效果先进入该 NPC 的 second-behavior queue，随后 generic pass 在旧版和候选中都会用 target block 结算。
- 所以此前获批的“一名当前 NPC 口内射精后，直接 `[4115]`”路线会在 effect 527 前清掉这个可见差异，不能证明本修复。探索截图只证明了正常 UI 能产生口内射精和 deferred counts，不能证明它们在直接解除时停时仍构成 owner 差异。
- 一个可能的正常玩法路线是：对 NPC A 产生口内射精和 deferred counts 后，把当前交互对象切换到 NPC B，再解除时停；这样前置重置只作用于 B。此路线是否确实可达、切换动作是否保留 A 的两个状态，目前正由独立代码路径调查，尚无结论。

请把这组事实纳入前述裁定，并额外决定：

6. 此事实是否使原一 NPC Tk 路线无条件失效；当前尚未读档的正式 baseline 会话应结束，还是仍有某个不依赖 `shoot_position_body` 的合格可见断言可从同一路线取得？
7. 如果多目标路线经实际代码与探索证明可达，matched Tk A/B 是否应改用该路线；如果不可达，当前候选应怎样分类（仍是正常游戏 bug、仅合成状态修复、或证据不足而暂缓）？
8. 在可达性结论出来前，是否有任何理由扩大生产实现，让“当前目标直接解除”也保留射精位置？请明确区分本归属 bug 与可能改变既有射精状态生命周期的玩法变更。

## Fable verdict（逐字保存）

**裁定:CODE PASS / DOCS NARROW。生产实现不扩;spec/design/tasks 按真实 bug 边界收窄;原一 NPC Tk 路线作废,尚未读档的 baseline 会话应结束。**

## 1. 结论与理由

七条 blocker 中没有任何一条指向本 owner bug 的必需实现部分:

- 远处二段的 `must_settle_check()` 丢弃新建 change 对象,是上游既有的"远处静默结算"策略,与"effect 527 同步写入归错 owner"是不同的 rule、不同的 owner。把它拉进本 PR 是把归属修复变成远处结算重构。
- generic pass 无条件 `setdefault` 是既有行为,候选正确地不触碰它。
- 结论:代码边界正确,是文档承诺越界。唯二代码侧动作:补 `AlwaysConfigured.get()` 中文 docstring、提交前从干净同 ref 恢复两个 PO 文件。

## 2. 四处收窄的精确语义

- **顶层 requirement**:"当某 NPC 存在任一正数 deferred 计数时,effect 527 **自身直接写入**的解除结算变化 SHALL 记录进 `root_change.target_change[npc_id]`(该 NPC 的 target-owned block);effect 527 SHALL NOT 消费或替代随后的 generic second-stage pass,该 pass 保持现有行为不变。"删去"and its follow-up effects…same rules"一类措辞。
- **zero-count scenario**:限定为"effect 527 SHALL NOT 仅为空 no-op 调用自行创建 target block",并加一句显式说明:随后的 generic pass 仍可能按既有逻辑为所有 NPC 创建空 target entry,不在本 scenario 断言范围内。
- **unrelated queue**:只承诺"effect 527 不消费、不移除、不覆盖无关的 queued second behaviors";删去关于它们此后如何普通结算的任何验证性陈述。
- **remote NPC**:只陈述同步归属、计数清零与清理;把"远处静默二段路径(`must_settle_check()`)保持不变"写成显式 **non-goal**。删去"exactly-once second-stage behavior follow the same rules"。

## 3. 测试充分性

补 docstring 后,现有 registry test **足以**覆盖收窄后的代码边界。不强制新增"完整 generic pass"测试。若自愿加,它只许证明一个交互缝:effect 527 之后 generic pass 仍能对该 NPC 的 queued second behavior 完成恰好一次结算且不崩——即非回归护栏,不得演变成对二段系统本身的验证。用真实函数搭不便宜就不加。

## 4. 探针的合格措辞

文档写法:"测试直接设置 `shoot_position_body=2`,作为代码级触发,使 `orgasm_settle` 向所传 change 对象写入一个可区分 owner 的同步数值;它证明 effect 边界处的归属路由,不证明玩家可达性。玩家可见证据由独立的 Tk A/B 路线提供。"若 matched Tk A/B 最终以正常 UI 路线展示可见归属差异,则"探针证机制 + Tk 证可达"合起来即为完整证据,探针无须自身贴近玩法。

## 5. 玩家介入

不需要。这是修复范围与证据强度判断,属监督者职权;无未决玩法语义。最终语义确认仍按规则在 PR 提交前由用户给出。

## 6. 一 NPC 路线与 baseline 会话

**无条件失效,结束该 baseline 会话。**推理链完整:唯一同步可区分数值是 `shoot_position_body ∈ [2,15]` 的饮精绝顶经验;`judge_before_pl_behavior()` 在 effect 527 前把当前交互对象的该字段重置为 -1;其余高潮效果走 second-behavior queue,新旧两版都由 generic pass 用 target block 结算,无差异。因此同一路线上不存在不依赖 `shoot_position_body` 的合格可见断言。尚未读档意味着没有沉没成本——现在结束,别在死路线上烧 matched run。

## 7. 多目标路线的分支处理

- **若可达**(切换到 B 后 A 的 `shoot_position_body` 与 deferred counts 均保留至 effect 527):matched Tk A/B 应改用该路线,它是正常玩法且保留判别值。
- **若不可达**:先穷尽一步——确认是否存在其他生产路径能带着正数计数和存活的 shoot_position 到达 effect 527(非当前交互对象的 NPC、其他触发序)。若确无,则按 skill 规则("拒绝无生产路径能发出的 test-only 触发协议")分类为**证据不足、暂缓上游 PR**:保留候选与代码级记录为本地合成状态修复,不以"正常游戏 bug"名义提交。它可能仍是真实潜在 bug,但没有玩家可见差异就没有说服人类 reviewer 的材料。

## 8. 不扩大生产实现

**没有理由。**`judge_before_pl_behavior()` 重置射精位置是既有的射精状态生命周期规则,决定的是"是否有变化被写入";本 bug 是"写入的变化归谁"。让"当前目标直接解除"保留射精位置,是改变状态存活期的**玩法变更**,有自己的 owner、自己的证据要求,与归属修复合并会把玩法改动走私进 bugfix。若有人认为该重置本身是 bug,另开调查,凭其自身证据立案。
