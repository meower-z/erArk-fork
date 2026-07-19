# Fable Supervision Record

## Boundary Review Before Production Edits

### Prompt

```text
/investigate-game-bug

请作为 erArk 这项候选修复的独立决策监督者，审查实现前边界与证据计划。不要修改代码，也不要承担仓库盘点；下面是已核验事实与完整 OpenSpec 内容的摘要。请主动寻找错误归因、过浅修复、漏掉的相邻行为、隐藏玩法语义、不可证伪的测试或应该拆分的范围，不要默认 997-only 正确。

用户明确要求：先把绝顶显示问题做成一个新的 997-only PR；显示系统小重构以后再谈；开发必须位于从 fork/upstream 基线创建的新 linked worktree；准备前后 Tk 图片证据；在上传、push 或创建 PR 之前停下让用户审查。

已核验生产事实：
1. 当前本地协调 main 是 9d2eb2bd3，脏且含其他工作，不能作为候选开发目录。远端包括 upstream=Godofcong-1/erArk 与 pr-fork=meower-z/erArk-fork。
2. `game_config.load_behavior_effect_data` 遇到效果 997 时，把 behavior_id 加入全局必须结算集合；998 是必须显示集合。
3. `character_get_second_behavior` 在行为入队时，根据上述集合填充角色的 must_settle / must_show 列表。
4. 远程条件为角色当前位置及 move_src 均不等于玩家位置。远程 `second_behavior_effect` 只调用 must_show_talk_check 和 must_settle_check 后返回。must_settle_check 执行配置效果、把行为归零并清空必须结算列表，但不调用口上。
5. 普通部位绝顶 1000-1043 已带 997。`plural_orgasm_2` 至 `plural_orgasm_11` 的十行有效果 409/301-306，但均没有 997。因而它们在远程产生时不进入两个列表，远程 pass 返回后仍留在 second_behavior；角色后来进入玩家附近，普通 pass 会显示并结算这条旧行为。
6. `extra_orgasm`、`b_orgasm_to_milk`、`u_orgasm_to_pee` 也没有 997，但其 Second_effect 效果函数直接调用绘制接口。仅加 997 会结算数值却仍可能显示远程文本，因此 OpenSpec 明确排除它们。
7. 用户提供的可见线索包括：等待五分钟等无关动作后，非同房间 NPC 出现绝顶/双重绝顶提示；诗怀雅同一轮先显示双重绝顶，随后到玩家位置触发发现群交。用户称最近存档可复现。静态链条能预测“远程行为滞留，靠近时延迟显示”，但尚未完成本候选独立 worktree 的自动化红测和真实 Tk A/B。
8. upstream/master 当前的 Behavior_Effect.csv 与协调 main 在这些行相同。

OpenSpec 合同：
- 新能力 `remote-plural-orgasm-settlement`。
- 远处角色得到 plural_orgasm_2..11 时：配置效果在远程二段 pass 结算，pending 行为清零，不显示该远程口上；后来靠近时不补显示且不重复结算。
- 同位置角色得到这些行为时：现有口上仍显示，效果只结算一次。
- 997 只加到上述十行；extra_orgasm、喷乳、漏尿不在这个 marker-only change 内。
- 不重构口上、队列、结算、Tk/Web，不修改普通部位绝顶、寸止或群交参与者规则。

设计选择与备选：
- 候选：十个 plural_orgasm_N 配置行追加现有 997，并重建必要生成物。
- 拒绝的备选 A：在 Python 远程路径按 plural_orgasm 前缀特判，因为重复声明式 997 职责。
- 拒绝的备选 B：同时改 extra_orgasm/喷乳/漏尿的直接绘制，因为会扩大为显示系统重构。

计划验证：
- 红测试经过配置语义、character_get_second_behavior 与真实 remote second_behavior_effect；基线应留下行为，候选应执行效果、归零、无 talk；覆盖 2..11 全集合。
- 逆向测试同位置仍显示并结算一次，并确认三个排除行为配置未变化。
- 从同一 upstream/master 制作 baseline/candidate runtime，禁用承担相同职责的本地批处理 mod；同存档、seed、PYTHONHASHSEED、窗口尺寸和书面操作路线，用真实 Tk visual workflow 捕捉并逐像素检查前后图。
- 之后才由 fable-5 撰写中文 PR 文案，并经 review-erark-pr-artifacts；在所有 outward actions 前交用户审查。

请返回：
1. VERDICT：ACCEPT / REVISE / BLOCKED；
2. 对 bug 规则、逻辑 owner 和 997-only 边界的判断；
3. 精确阻断问题（若无写 None）；
4. 自动化红绿与 Tk A/B 是否足以证明因果，若不足给出下一条最小证据路线；
5. OpenSpec 文档需做的精确修改；
6. 是否需要现在询问用户。弱证据本身不是停工理由，请给下一步。
```

### Verdict

```text
**1. VERDICT: ACCEPT**（附三处 OpenSpec 补充，见第 5 条；无需先问用户。）

**2. 规则、owner、997-only 边界的判断**

- 违反的规则表述正确：「远程产生的二段行为必须在远程 pass 内结算并清空，不得滞留到靠近时补显示」。该规则的声明式 owner 就是 Behavior_Effect.csv 的 997 标记 + `must_settle_check`，1000-1043 已是先例；plural_orgasm_2..11 是同类遗漏，不是新机制。归因链（无 997 → 不入 must_settle → 远程 pass 返回后滞留 → 靠近时旧行为显示）与已核验事实 2-5 自洽，且能预测诗怀雅线索。
- 拒绝备选 A 正确：Python 侧前缀特判会造出第二个 owner。拒绝备选 B 正确：那是显示系统问题，用户已明确推迟。
- 997-only 边界成立，但有一个必须写明的后果：**extra_orgasm、喷乳、漏尿的同型滞留 bug 在本 change 后仍然存在**。如果用户存档的复现路线里混有这三者，玩家会看到「修了一半」。这不是扩scope的理由，是必须在 proposal 的 non-goals 里写成 known-remaining defect 并预告后续 change 的理由。

**3. 精确阻断问题**

None。

**4. 证据是否足以证明因果**

基本足够，但当前计划有两个可证伪性缺口，补上才算闭合：

- **红测必须断言数值确实结算，而不仅是「行为归零、无 talk」。** 否则测试无法区分「正确远程结算」和「行为被吞掉、效果丢失」。候选侧对 409/301-306 至少抽查一项数值增量（基线 vs 候选同输入对比）。
- **Tk A/B 的基线侧必须先拍到延迟显示的复现帧**（用户存档 + 等待类无关动作 → 非同房 NPC 绝顶提示出现），候选侧同路线同帧位无该文本。只有候选侧「干净」而基线侧没拍到脏帧，等于没有 A。

补上这两点后，自动化红绿 + Tk A/B 足以让人类 reviewer 信服因果，不需要更多证据路线。

**5. OpenSpec 需做的精确修改**

1. **non-goals 增补**：明确写出 extra_orgasm / b_orgasm_to_milk / u_orgasm_to_pee 的远程滞留是已知未修缺陷，本 change 后仍可复现，修复需先解决其 Second_effect 直接绘制（后续显示系统 change 的动机）。
2. **测试合同增补**：红测的候选侧断言至少一项配置效果的数值增量已应用（不只是行为清零 + 无 talk）。
3. **逆向检查增补一项**：诗怀雅线索里的「靠近后触发发现群交」在候选下仍能按现有规则发生——验证群交发现不依赖那条滞留的 second_behavior。如果验证发现它*确实*依赖滞留行为，这就是隐藏玩法语义,升级为 blocker 回来重议。

**6. 是否需要现在询问用户**

不需要。997-only 边界、Tk 证据、push 前停下都已是用户明示要求；上述三条是文档与测试计划内部修订，属可自决范围。下一步：按第 5 条改 OpenSpec → 建 upstream/master 基线 worktree → 先写红测跑出基线红。唯一需要回到用户的触发条件是第 5.3 条验证失败（群交发现依赖滞留行为）。
```

## Evidence-route consultation after slot 7 did not reproduce

The real Tk baseline used pristine slot 7, no mods, a fixed seed, and nine normal five-minute waits from 21:17 through 22:02. No remote plural-orgasm output appeared. Fable-5 was therefore asked only to choose the next evidence route and stopping conditions; it did not execute analysis or implementation.

Its direction was:

1. First inspect slot 7 read-only for a plausible trigger window; if none exists, scan the other existing saves with the same predicate rather than opening each one in Tk.
2. Replay only the best matching save. If no existing save matches, use normal player actions to establish a controlled reproduction, with a hard budget of 30 player actions or three hours of visual work.
3. A valid baseline must visibly show the remote plural-orgasm output with a character name and game-time/context anchoring. A valid candidate image must use the same save, seed, physical action sequence, action index, and game time so the missing line is demonstrated by matched context rather than by an isolated ordinary screen.
4. A nearby plural-orgasm positive control is additionally required to show that normal talk was not disabled.
5. The candidate may enter user review only when the baseline positive frame, matched candidate absence frame, and nearby positive control all exist with a consistent manifest. Automated green alone does not replace the real Tk evidence.

The read-only scan then found that slot 7 had no character in a relevant H state at its save point, while existing slot 99 had ten NPCs, including Swire, actively masturbating in the human-power room. Slot 99 became the next pristine visual route without changing the 997-only implementation boundary.
