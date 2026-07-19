/investigate-game-bug

你是 erArk“时停解除结算归属”任务的独立监督者。你上一轮裁定 run2 永久 INVALID，但允许从 exact main scene 继续到 release endpoint，仅作诊断；每个 transport 后最多等 10 秒，先认 semantic anchor，再取 stable pair；错误的新页要停。执行现在遇到一个新事实：单击 `[5052]无意识奸` 后，没有额外输入，却直接到达了预期的 H 菜单，跳过了 run1 曾显示的“进入无意识奸模式”等待页。请以怀疑视角判断这是证据污染、正常的 Tk 鼠标竞态，还是协议把非关键瞬时页错误地设成了硬门。不要因为最终页恰好可继续就放宽标准，也不要因为旧路线列出了中间页就忽略实际输入实现。

## run2 身份与前判

- run2 固定在 `abebf33b52ebf51424f71365946eb8df1f75a23c`，fresh archive runtime；它因早先读档页的异步时序误判而永久 INVALID，所有续跑产物都是 `DIAGNOSTIC ONLY`。
- 你上一轮裁定允许从 byte-exact main scene 继续冻结物理路线，目的只是在正式 A/B 前提前验证 active `[4115]` endpoint；任何 PASS 或 PR 证据都不得引用 run2。
- 当前 unit/window/PID 链未更换，窗口未关闭，进程正常；observer 尚未发 signal。

## 本轮精确 transport 与截图

1. 从 r2-10/r2-11 byte-exact main scene，仅单击一次 visible `[4113]`，坐标 `(1035,517)`。
2. 一秒后 r2-12 已显示 `[4114]` 和 `[5052]`；再一秒 r2-13 byte-identical/AE0，SHA256 `8144286f1f3523d4973663d40c9517226ab49166d7b281ae94cfeec42c64c6a8`。这一门正常通过。
3. 从该 stable page，仅单击一次 visible `[5052]无意识奸`，坐标 `(381,681)`。
4. 没有发送 Return、第二次点击、alternate coordinate、observer signal 或任何其他输入。
5. 一秒后的 r2-14 已是 H 菜单，可读 `[6602]口交` 与 `[4115]在H中取消时停`；再一秒 r2-15 byte-identical/AE0，SHA256 `223720ace7aa4620760b301765a44c8e096670a4a7a9a70b7702404535977ae8`。
6. run1 的同一点击先停在“进入无意识奸模式”页，SHA `5b1bfd54...`，另按一次 Return 后才到同一个 H 菜单 SHA `223720ac...`。
7. 执行者按你上一轮“错误新页即停”的字面规则停止，没有从 H 菜单继续。action log SHA256 `d231f247d28c75620572b1059e43ec6e0ef8c6cedff01f0e29498105c6de9825`；outcome SHA256 `0b77c12633e87cdc61b961c0aecbff22e5ff3bcdc7e12eb6c7d119976f07d7cc`。

## 静态实现解释

这不是猜测，当前 pinned runtime 的调用链如下：

- `handle_unconscious_h()` 先设置无意识/H 状态，然后构造 `WaitDraw`，绘制“进入无意识奸模式”，调用 `now_draw.draw()`，最后才做 H common settle。
- `WaitDraw` 最终调用 `flow_handle.askfor_wait()`。
- `askfor_wait()` 先执行 `cache.wframe_mouse.w_frame_up = 0`，随后以这个 mouse-up flag 等待任意输入。
- command selection 与 wait 共用 Tk mouse state。一次物理 `xdotool click 1` 包含 press 与 release；若 command 在 press/早期事件时开始处理，而 release 在 `askfor_wait()` 清零后到达，同一次点击的 release 会立即满足 wait。若 release 在清零前到达，等待页会留下来，必须另按 Return。
- 这解释了 run1 与 run2 的差别，而且 candidate 唯一改动在 `Script/Settle/default.py` 的 effect 527 参数归属，不触碰输入、WaitDraw 或 H 入口。

## 已准备但未启动的正式包

- formal baseline/candidate 都是从最新 pinned upstream `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5` 独立 archive 重建，只有 `Script/Settle/default.py` 不同；尚未启动，也没有正式 gameplay input。
- 正式 provenance SHA256 `7f0e6b3a74eb9826941a411916e8b7e03fd5fc4ac210da7a8f7c79621d4952f9`。
- 旧 run2 不能被追认；下一次 fresh run 仍从 title 开始，baseline 完成后才允许 candidate。

## 请作最终决定

1. 对当前 diagnostic 给 `CONTINUE FROM H MENU`、`CLOSE/RESTART` 或 `REVISE`。若允许继续，是否明确禁止补发 run1 那个 Return，直接把 stable H 菜单当作 `[5052]` 已成功完成的 semantic checkpoint，然后继续四轮口交、sample1、切目标、sample2、active `[4115]` endpoint？
2. 正式 prereg 应如何处理这类同一 mouse click 可能消费紧接 wait 的竞态？请在以下思路中做最终选择，或给更严格的替代：
   - 把“进入无意识奸模式”设为可选瞬时页；transport 后接受两种预注册分支：若等待页稳定出现则按一次 Return，若直接出现 H 菜单则不补输入；最终必须到同一 H 菜单和同一 observer state。
   - 改用键盘/其他 transport，强制等待页可捕获；但这将偏离已探索的正常按钮点击，并且也需证明没有 key-up 同类竞态。
   - baseline/candidate 都必须走完全相同的瞬时分支，否则整对 invalid；或允许它们分支不同，只要冻结语义状态和后续有意义输入一致。请明确。
3. 你上一轮写的“错误新页”应如何精确定义，避免把“预期状态链上的更后稳定 checkpoint”与真正错误页混在一起？哪些页必须逐页出现，哪些只需要最终状态锚点？
4. 正式 protocol 是否应以“状态改变动作的最终稳定语义 checkpoint”为门，而输出/结算 wait pages 仍逐页捕获？如果不是，请给可执行规则。
5. 这个发现是否要求修改游戏代码？当前任务候选不触碰输入系统；除非它妨碍真实玩家或破坏证据，请不要把测试装置竞态擅自扩成新产品 bug。
6. observer `e33cfec8...` 是否继续冻结？正式包是否仍可直接作为下一次 formal baseline/candidate，而无需再做一次 disposable rehearsal？
7. 是否需要玩家现在介入？这里不改玩法语义、不外发。
