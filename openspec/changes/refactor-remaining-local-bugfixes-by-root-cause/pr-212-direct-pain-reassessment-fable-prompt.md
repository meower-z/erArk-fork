/investigate-game-bug

请作为 erArk PR #212 的 Fable 5 设计监督者，独立审查下面的事实、修复边界和双证据计划。不要把 maintainer 评论当成结论；代码和生产探针是事实来源。

## 用户确认的目标

必须同时修复：

1. `苦痛快感化` 开启时，负向苦痛变化被错误改道成负心理快感；
2. `ADD_SMALL_PAIN` / `ADD_MIDDLE_PAIN` / `ADD_LARGE_PAIN` / `EXTRA_ORGASM` 的正向苦痛直接写入绕过转换，导致开关开启时苦痛仍增加。

候选应从旧 PR 的广覆盖责任出发，修复任何真实的重复计算，并准备两组独立 Tk A/B 证据。

## 已验证事实

- 当前通用路径对所有 active state-17 最终值递归调用 state 23，未判断正负。
- 四个 direct writers 直接写 `status_data[17]`。active flag 下生产函数探针分别得到 pain `+20/+100/+1000/+120`、psychological `0`。
- 乳头夹/阴蒂夹的 ongoing second behavior 在 `Behavior_Effect.csv` 中生产可达地触发 `ADD_SMALL_PAIN`；extra orgasm 生产可达地触发 `EXTRA_ORGASM`。
- 旧 commit `21261e951` 的 `route_pain_delta` 只调用一次 `chara_feel_state_adjust`，不调用 common settlement。动态探针：pain `70`、psych adjust `2.0`、continuous `0.7` → state 23 value `98`，心理调整调用次数 1。因此“该 helper 必然重复计算两次心理快感能力加成”与代码不符。
- 另一个独立事实：现有 upstream 通用递归在 state 17 外层和 state 23 内层各应用一次连续指令衰减。raw `100`、psych adjust `2.0`、continuous `0.7` → `98`，心理调整仍只调用一次。旧 helper 保留了这个既有两阶段连续衰减。

## 候选边界

A. 仅在 common 加正值 guard：不能修 direct bypass。

B. 原样恢复旧 value-routing helper：覆盖 direct bypass，心理系数一次，但手动复制部分 state-23 计算，可能绕开 sleep/unconscious admission 或未来规则。

C. 首选：新增一个 conversion-attempt helper，输入已计算的 signed pain delta 和 change records。inactive/非正值返回 False；active 正值只调用一次既有 `base_chara_state_common_settle(... state_id=23, ability_level=ability[36], tenths_add=False ...)` 并返回 True。common state-17 分支及四个 direct writers 都调用它；False 时 caller 保留原 state-17 写入。helper 本身不计算任何心理能力系数。

D. 让 direct writers 再走 state-17 common：会重复它们已经做过的痛苦刻印/源公式调整，并新增普通 state-17 side effects。

E. 在五处重复 sign/flag/state-23 call：规则继续散落，未来仍会漏。

## 待判断问题

1. maintainer 关于“心理快感能力加成两遍”的指控是否被事实反驳？请明确区分心理能力系数与连续重复指令衰减。
2. C 是否是最小且完整的 owner boundary？如果不是，请给出更小但仍覆盖四个 direct writers 的具体边界。
3. 本 PR 是否应同时改变现有 common recursive path 的两阶段 continuous multiplier，还是应保持现有 tuning，只保证心理能力系数 exactly once？
4. 两组 Tk A/B（负向 `[4103]`、正向 clamp second effect）是否足以向 maintainer 证明同一 signed-routing rule 的两个失败方向？
5. 请审查记录 `/home/ubuntu/games/erArk/openspec/changes/refactor-remaining-local-bugfixes-by-root-cause/pr-212-direct-pain-reassessment.md` 的设计是否可接受。

请输出：`PASS` 或 `REVISE`，逐项回答 1–5；若 REVISE，给出必须修改的设计点。只有确实存在无法从代码/运行证据决定的玩家语义时，才写明需要玩家输入。
