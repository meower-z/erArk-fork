**判定:PASS** — 严格等价逐-case方案正确、符合用户"禁止统一 helper、逐分支修复"的范围要求,且是该约束下事实上的最低罚分正确形状。无字段的 post-panel 推断方案 **FAIL**,不得采用。无需用户决定新游戏语义。

以下结论全部基于实际读取:候选 diff(`ffd1d1ee8` vs `3a1c9e620`)、基线面板逐 case 代码、两条 caller(`character_behavior.py:168`、`hidden_sex_panel.py:249`)、状态机 40/96(`StateMachine/default.py:1309`、`:2075`)、效果表(`Behavior_Effect.csv` 仅 377/393 两行含 1721)、效果 1721 实现(`Settle/default.py:2657`,寻路失败退化为 `WAIT` 而非保留原行为)、嵌套更新路径(`handle_instruct.py:376` 的 `update.game_update_flow`)、28 例测试与 OpenSpec design.md。

## 1. 逐-case方案与公开字段:正确、范围合规

逐 case 对照已确认合同(design.md:74)逐条成立:

- **DECEIVED/LEAVE**(补结算,flag 保持 False):面板结算一次,1721 在结算内转 MOVE,NPC 外层因 falsy 结算后继 MOVE(合同"当轮结算 MOVE"✓);direct caller 结算一次、MOVE 留待后续轮次 ✓。
- **IGNORE**(补结算,flag True):两条 caller 各恰好一次,无 MOVE 后继,外层跳过 ✓。
- **JOIN/INTERRUPT**(保留原结算,flag True):修复 NPC 外层重复结算 ✓;INTERRUPT 的 flag 在 group_sex_end/H_INTERRUPT 嵌套更新前写入 ✓。
- **DISCOVER**(补结算,flag True,先结算后 `chara_handle_instruct_common_settle`):即使 `game_update_flow` 把行为清成 `SHARE_BLANKLY`,外层仍跳过,与已审候选一致 ✓。
- **REFUSE**(保留原结算,flag False):外层结算后继 MOVE,与上游一致 ✓。
- 转隐奸/露出成功不设 flag → 外层普通空闲结算 ✓;状态机 96 无 return → None → falsy → JOIN 正常外层结算,不受影响 ✓。

**公开字段判定:最小必要的 operation-local 信息,不是隐藏协议。** 三个结构性事实使字段不可省:Tk/Web 的 `askfor_all` 丢弃回调返回值(回调→`draw()` 只能经实例状态传递);direct caller 没有外层结算;嵌套更新可改写行为使事后推断失真。字段生命周期 = 单次面板对象,写一次、经返回值读一次、无全局态——这正是 skill 偏好的 "returned result" 形态。design.md:83 已把 absent-attribute、全局标记等替代逐一否决,本方案与之一致。

一个真实的简化收益:逐-case方案里 MOVE 型反应保持 False,scheduler 只需 `if not settled:`,已审候选的 `or behavior == MOVE` 析取变得不必要——这是结构性简化,不是刷分。

## 2. 无字段推断:FAIL,具体语义差异

- **DISCOVER**:`chara_handle_instruct_common_settle` 以 character_id=0 收尾必然调用 `update.game_update_flow(duration)`(handle_instruct.py:376),可把发现者行为推进/清成 `SHARE_BLANKLY`。事后推断见到 `SHARE_BLANKLY` ∉ 跳过集 → 外层对空闲行为再跑一次 `judge_character_status`(含事件触发与 share_blankly 效果,非 no-op),与已审候选的"外层跳过"语义不同。
- **INTERRUPT**:`handle_group_sex_end`/H_INTERRUPT 同样可改写发现者行为;若嵌套更新恰好把行为改进跳过集,还会反向漏掉一次应有结算。双向都不稳。
- 这正是 design.md:83 已否决的 "behavior-history inference"。省 1 行(58 vs 61)买不回操作身份。

## 3. 更低 `3a-b` 的正确方案:不存在

四跳返回链(面板字段→draw 返回→状态机 40→`find_character_target`→scheduler)是结构性最短通道;四处补结算 + 四处置 flag + init 是逐-case语义的固有成本。核查过的替代:默认 True 反向清除需 5 处置 False(含两个转换成功分支)更差;向面板传 caller 身份参数是已被否决的"猜 owner"设计且行数更多;scheduler 内联表达式是 design.md:89 已定性的格式刷分。**61 即该约束下的地板,预计 `a≈22, b≈5, penalty≈61`(±2 取决于 docstring 行数)。**

## 4. 公开游戏语义:无未确认改变

与已审候选唯一的行为分歧在一个未被合同覆盖的边角:1721 寻路失败时行为退化为 `WAIT`(`general_movement_module` 失败分支),已审候选(flag True 且 ≠MOVE)跳过、下轮再结算;逐-case方案(flag False)当轮立即结算 WAIT——**这与上游 REFUSE 路径的原生行为一致,是更忠实于上游的一侧**,且 WAIT 时长 1 分钟、无玩家可见差异。已被用户接受的 Tk A/B 证据(面板内可见反应文本)在新形状下不变,仍有效。

## Actionable findings

1. 实施时保持 DISCOVER/INTERRUPT 分支内 "结算 → 置 flag → 嵌套玩家更新" 的顺序;flag 写入晚于嵌套更新即破坏等价。
2. scheduler 采用 `if not discoverer_reaction_settled:` 单条件(去掉 MOVE 析取),保持项目正常多行格式与中文注释。
3. 重跑 28 例测试:已核实测试按语义断言(AST 加载生产定义,不引用 `_settle_discoverer_reaction` 名字),预期仅少量适配;新增/保留对"1721→WAIT 退化当轮结算"边角无需断言(未确认合同外)。
4. 将本次逐-case边界、a/b 预算与 WAIT 边角说明补入 design.md(在主工作树 `main` 上串行编辑),替换 §2026-07-15 的结论后再动生产代码。

## Residual risk

- WAIT 退化边角(寻路失败)无运行时证据,仅静态推理 + 上游先例;影响面为 1 分钟空等的结算时机,可接受。
- 测试是 AST 隔离加载,非全游戏运行;既有的 Tk A/B 证据覆盖主可见路径,兄弟分支(IGNORE/LEAVE/DISCOVER)仍只有测试级验证——与已审候选的验证水位持平,不构成新的门槛。
