/investigate-game-bug

你是 erArk“时停解除结算归属”fresh attempt3 正式 matched Tk A/B 的监督者。attempt3 baseline 已按你批准并冻结的预注册启动，目前在第一轮口交的第一张等待页上按 anomaly rule 零输入暂停。请以怀疑视角裁定可继续还是必须作废；不要因为 systemd 终于稳定、重跑成本很高或页面内容看起来正常而放宽，也不要把 attempt2 的页面模式当成正式结果。Candidate 没有启动，baseline 也尚未出现 release 结果。

## 冻结身份

- attempt3 preregistration SHA256：
  `6351253194decb1496b4999c58fcebda4e752ff573ab455148e6b794b892e84f`
- 你的最终 verdict：`ATTEMPT3 PREREG PASS`。
- upstream commit/tree：
  `abebf33b52ebf51424f71365946eb8df1f75a23c` /
  `214bea9f3257f5336c36c4278b1d64a0cf378be0`。
- baseline default.py SHA256：
  `ecdec42b79d393e3dc5deb0d88f1ca897d052d08ffc99c0389ab2c1ce7278be5`。
- observer SHA256：
  `31932118bf625d122807cafcd3de4a7a28eaa968cae631829d83b8c942326ab9`。
- common launcher SHA256：
  `6723e3e228c8ec37839a8a5694025f7dcb9277c9b7e096abd36e3ec5f89af7e6`。
- baseline service 仍为 active/running；Invocation ID
  `c5fa7fa8fa204e8c8e8ebd25d1b45da5`；DISPLAY `:9`；稳定窗口
  `2097189`、`1238x937`。Candidate 未启动。

## 到暂停点为止的输入与一致性

attempt3 baseline 依次用冻结的物理输入完成：鼠标点 `[001]`、slot5、读取、确认、`[4113]`、`[5052]`，然后 Return 恰好一次到 H 菜单。

`b3-00` 到 `b3-07` 与 attempt2 current-upstream baseline 的 `b2-00` 到 `b2-07` **每一张都字节相同，AE 像素差全为 0**。这包括标题、存档页、读取确认、加载主界面、开时停、进入无意识奸和首个 H 菜单。

round1 前无输入复拍 `b3-08` 与 `b3-07` 字节相同、AE=0，SHA256 均为：
`223720ace7aa4620760b301765a44c8e096670a4a7a9a70b7702404535977ae8`。

随后唯一输入是鼠标点击当前可见 `[6602]`，window-relative `(71,625)`。

## 页面差异

attempt3 当前 `b3-09-oral1-wait-page.png`，SHA256：
`81635e2e7b605b60874769e183555fd8d8c32829d18037a654c6c545aaac428e`。

原尺寸可读内容：

- `6602` / `口交`；
- `需要性爱实行值至少为450`；
- 当前值公式，总值 `11199`；
- 没有射精面板；
- 尚未显示博士/林数值记录或 `10分钟过去了`。

attempt2 诊断轮的 `b2-09` 在相同第一轮第一张页上，同样先显示 `6602`、`口交`、相同门槛和相同当前值 `11199`，但同一帧还继续显示博士/林数值记录与 `10分钟过去了`，一次 Return 就回到 H 菜单。

因此差异只是**等待页分段**：attempt3 在前提/当前值后先停页；attempt2 诊断轮把数值结算合并在同页。attempt3 尚未按 Return，所以还不知道它的下一页，但没有观察到状态值、动作语义、角色、轮次或射精面板偏差。

执行者发现 anomaly 后严格执行修正版 C：没有 Return、signal、滚动、切目标、`[4115]`、服务关闭或 candidate 启动。主协调者已原尺寸查看 b3-09 与 b2-09。

## 只读排查

- attempt2/attempt3 baseline 的 `Script/Settle/default.py` 字节相同。
- 两轮启动时生成的 `data/Character_Talk.json` 均为 131,229,025 bytes，SHA256 同为
  `08279af05806d8c928985616634d6e6c75267292210f7fe12cc65186b9067cbc`。
- 两轮 `data/Character_Event.json` SHA256 同为
  `8b95637f7eb0694c70a03ddbb05ed801bf064f771f65f5d05ab6d56911027f09`。
- attempt3 observer 相比 attempt2 observer 只新增冻结环境断言/打印与格式化；两者都在 game import 前执行相同的 `random.seed(5270714)` 与 `numpy.random.seed(5270714)`，Tk zoomed fallback 和三样本读取逻辑未变。
- attempt3 游戏日志已打印相同 seed、`PYTHONHASHSEED=0`，且 fallback 恰好 1；当前无 Traceback、Exception 或 TclError。

这说明没有发现 runtime、save、pre-route state、生成 talk 数据或首个动作输入的差异。剩余合理可能是等待页结构存在跨进程噪声；冻结预注册已把 attempt2 页模式定义为 anomaly detector，而不是 cross-attempt hard gate，同时要求 candidate 的 hard matching target 是本次 attempt3 baseline。

## 请裁定

1. 给 `CONTINUE ATTEMPT3 BASELINE / ACTUAL-PAGE RULE`、`INVALIDATE`，或指定最小处理。
2. 若允许继续，是否应从当前 b3-09 按冻结规则恰好 Return 一次，逐页捕获，直到 H 菜单，并把这次 attempt3 的实际页面边界冻结为 candidate 必须精确匹配的 hard gate？
3. 若下一页出现正常第一轮数值结算与 `10分钟过去了`，是否足以把本次差异定性为纯分页；若出现数值/语义偏差，是否立即作废？
4. 是否允许保留当前侧，不发送任何额外 observer signal 来解释分页？
5. 是否需要玩家介入？这里没有玩法语义选择、生产代码变化或外发动作。

## Fable verdict（逐字保存）

**裁定：`CONTINUE ATTEMPT3 BASELINE / ACTUAL-PAGE RULE`，附一个前置条件。** 不作废。

## 理由

到 b3-08 为止逐帧字节相同、seed/hash/数据文件/输入全部对齐，b3-09 的可见内容（动作、门槛、当前值 11199、无射精面板）与 b2-09 前半严格一致，差异仅是等待页在哪里断页。预注册已明确：attempt2 页模式是 anomaly detector，不是 cross-attempt hard gate；candidate 的 hard matching target 是本次 attempt3 baseline。因此断页差异触发暂停是正确执行，但它本身不构成作废理由——A/B 有效性取决于 candidate 是否匹配 attempt3 自己的页面边界，而这尚未被破坏。

**前置条件（继续前必须执行）**：先做一次**零输入被动复拍**当前帧并与 b3-09 比对。最简约的未排除解释是跨进程截图时机——b3-09 可能拍在文本仍在输出、尚未到达稳定等待点时。若复拍与 b3-09 字节相同，确认这是稳定等待页，按下述规则继续；若复拍已长出后续内容（趋向 b2-09 形态），则差异定性为截图时机噪声，以复拍帧为 b3-09 正式帧继续。

## 逐项答复

1. `CONTINUE`，前置条件如上。不作废。
2. **是。** 确认稳定后，从 b3-09 起按冻结规则恰好一次 Return、逐页捕获（每页同样做一次零输入稳定性复拍再定格），直到回到 H 菜单。把 attempt3 实际页面边界冻结为 candidate 必须精确匹配的 hard gate——这正是预注册的原意。
3. **是。** 若 attempt3 各页内容的并集与 b2-09 单页语义内容完全一致（数值记录、`10分钟过去了`、无射精面板差异），定性为纯分页，继续。若出现任何数值、角色、轮次或语义偏差——立即 `INVALIDATE`，不得用"接近"辩解。
4. **是。** 保留当前侧，不发送任何额外 observer signal。只允许被动截图。
5. **不需要玩家介入。** 无玩法语义选择、无生产代码变化、无外发动作。

## 记录要求

断页差异的成因目前未确证（截图时机 vs 等待页结构跨进程噪声），在 runtime manifest 中记为 open note。若 candidate 之后无法匹配 attempt3 的页面边界，说明分页在同机同 seed 下不稳定，届时整个 byte-exact 帧比对方法失效——那必须回来做预注册修正（改为语义内容比对），不得现场放宽。
