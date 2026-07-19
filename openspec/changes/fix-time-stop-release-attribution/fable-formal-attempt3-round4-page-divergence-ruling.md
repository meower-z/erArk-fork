/investigate-game-bug

你是 erArk“时停解除结算归属”attempt3 正式 matched Tk A/B 的监督者。Fresh baseline 依照你刚给的 `CONTINUE ATTEMPT3 BASELINE / ACTUAL-PAGE RULE` 已完成前三轮口交，现在第 4 轮首次出现射精面板，但又发现一个纯等待页边界差异，执行者在点击 `[射出]` 前零输入暂停。请裁定现有 ruling 是否允许继续，或这一新差异必须作废；不要因为当前帧与旧帧字节相同就自动放行，也不要为了维持上一裁定而忽略第 4 轮冻结要求。Candidate 尚未启动，baseline 尚未产生 release 结果或 observer sample。

## 既有 attempt3 结果

- 冻结 preregistration SHA256：
  `6351253194decb1496b4999c58fcebda4e752ff573ab455148e6b794b892e84f`。
- 你对第一轮分页差异的 exact ruling SHA256：
  `527913424f2b959f254b76361703bd661e8c1fad3eea56c443f79a76c3bac9db`。
- baseline service 仍 active/running，Invocation ID
  `c5fa7fa8fa204e8c8e8ebd25d1b45da5`，同一窗口、observer、runtime 和 service envelope。
- 第一轮按你的 passive-recapture gate 证明 b3-09/10 是稳定 prerequisite 页；一次 Return 后 b3-11/12 是稳定 numeric 页，并且 b3-11 与 invalid diagnostic b2-09 **字节相同**。两页语义并集完全正常；再一次 Return 回 H 菜单。
- 第二轮的两张稳定 wait 页和 H 菜单分别与 attempt2 对应帧字节相同。
- 第三轮的一张稳定 combined 页和 H 菜单分别与 attempt2 对应帧字节相同。
- 每个页面都执行了“正式捕获 + 零输入被动复拍”，每对均字节相同、AE=0。前三轮无射精面板、数值/角色/语义偏差或额外输入。

## 第四轮当前差异

1. b3-27 是当前 H 菜单的零输入连续性复拍，与 b3-26 字节相同。
2. 唯一新输入：鼠标点击当前可见 `[6602]`，window-relative `(71,625)`。
3. attempt3 直接到达 `b3-28-oral4-after-click.png`：
   - `口交(连续)`；
   - prerequisite/current-value `11209`；
   - 射精面板，正常同时可见 `[忍住]` 与 `[射出]`；
   - 这是 attempt3 第一次出现射精面板，确实在第 4 轮；
   - 尚未点击任何面板选项。
4. 零输入被动复拍 b3-29 与 b3-28 字节相同、AE=0，证明是稳定交互页而不是文本仍在输出。
5. b3-28、b3-29 与 invalid diagnostic attempt2 的 `b2-20-oral4-after-return1.png` **三者字节完全相同**，SHA256 均为：
   `7420c959e1b96a8bc9fbba6b1ab531b75f0290e04efbc8ac78105db301f9092a`。
6. attempt2 在到达该 b2-20 面板前，曾先呈现一个独立 `b2-19` prerequisite/current-value 页，按一次 Return 后才到 b2-20。attempt3 没有单独呈现 b2-19，首次 click 后直接到与 b2-20 相同的 stable panel。

因此这次差异是：attempt3 省略了 attempt2 的冗余 prerequisite-only 中间页，直接到达包含相同 prerequisite/current-value 加正常面板的 b2-20 字节帧。没有缺少语义内容；面板轮次、内容与状态都正确。它与第一轮分页差异方向相反，但同样说明 physical click 与 wait-page 分段存在跨进程噪声。

执行者发现后没有点击 `[射出]`、Return、signal、滚动、切目标、`[4115]`、关闭服务或启动 candidate。主协调者已原尺寸查看并独立做字节/AE 比对。

## 请裁定

1. 给 `CONTINUE ROUND4 / ACTUAL-PAGE RULE`、`INVALIDATE` 或最小其他处理。
2. 若继续，是否可把 b3-28/29 当作 stable 第 4 轮面板页，按冻结坐标鼠标点击可见 `[射出]`，然后对每个后续 actual page 做正式捕获 + 被动复拍，再一页一 Return 直到 H 菜单？
3. Candidate 是否必须精确匹配 attempt3 的第 4 轮边界（点击 `[6602]` 后直接到面板，不额外出现 prerequisite-only 页）；若 candidate 多出那一页，是否应按你上一 ruling 回来修订为语义页并集比较，而不是现场放宽？
4. 当前页面已精确等于 b2-20，是否足以证明“第 4 轮首次出现正常面板”gate，不需要额外 observer signal？
5. 是否需要玩家介入？没有玩法语义、生产代码或外发动作。

## Fable verdict（逐字保存）

## 裁定:CONTINUE ROUND4 / ACTUAL-PAGE RULE

**1. 处置。** 继续,不作废。本次差异与第一轮分页差异属同一类别:physical click 与 wait-page 分段的跨进程分页噪声,方向相反(省略页而非多出页)。判据不是"当前帧与旧帧字节相同",而是:attempt3 第 4 轮的语义页并集完整——`口交(连续)`、prerequisite/current-value `11209`、面板双选项 `[忍住]`/`[射出]` 同帧可见,首次面板确实出现在第 4 轮,且经零输入被动复拍证明稳定。attempt2 的 b2-19 是 prerequisite-only 中间页,其语义内容(`11209`)已包含在 b3-28 内,并集无缺失。第 4 轮冻结要求(首次面板必须出现在第 4 轮)已按内容满足,不是被绕过。

**2. 后续操作。** 可以。将 b3-28/29 记为稳定第 4 轮面板页。点击 `[射出]` 的坐标必须对照 b3-28 当前帧确认按钮确实位于冻结坐标处再执行——冻结坐标只在与当前可见帧一致时有效,不一致则停下重拍。此后每个 actual page 执行正式捕获 + 零输入被动复拍,逐页一次 Return 直到 H 菜单。释放后各页是本实验的核心证据,每页须原尺寸 `view_image` 检视并记录数值,不得只做哈希比对。

**3. Candidate 边界。** 不要求字节级匹配 attempt3 的分页边界。若 candidate 在点击 `[6602]` 后多出一个 prerequisite-only 页再到面板,按你上一 ruling 已冻结的语义页并集规则比较——这是执行既有裁定,不是现场放宽。必须精确匹配的是:首次面板出现的轮次(第 4 轮)、prerequisite/current-value、面板选项集合、触发输入序列。这些任一不同即作废该对。

**4. Gate 证明。** b3-28 与 b2-20 字节相同只是佐证,不是 gate 依据——b2-20 来自已作废的 attempt2,不能反向赋予效力。Gate 通过的依据是:主协调者已原尺寸检视 b3-28 本身的内容,确认第 4 轮首次面板及全部语义要素。以此为准,不需要额外 observer signal;但在记录中写明 gate 依据是被检视内容,而非字节相等。

**5. 玩家介入。** 不需要。无玩法语义抉择、无生产代码改动、无外发动作。按停止规则继续执行。
