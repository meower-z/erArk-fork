# Fable prompt: attempt 4 run 2 asynchronous page gate

Invocation contract: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Exact prompt follows.

```text
/investigate-game-bug

你是 erArk“时停解除结算归属”任务的独立监督者。你裁定 `ROUTE A PASS`，硬条件是 fresh disposable run2 从头到 sample2 后直接点击底部活跃 `[4115]`。run2 在读档确认后的页 gate 被严格判 invalid，但纯观察后来证明唯一点击只是异步处理较慢。请以怀疑视角决定是否继续诊断、如何重写下一轮时序规则，以及上游刚发生的无关漂移如何处理。不要为节省一次重跑而追认无效证据，也不要把正常异步处理误判成额外玩家输入。

## run2 冻结与前置通过

- fresh `git archive` runtime，commit `abebf33b52ebf51424f71365946eb8df1f75a23c`, tree `214bea9f...`；4174 regular files；prelaunch content-inventory SHA `96277079...`；没有复制 run1 runtime。
- prereg SHA `aae950e843269b0000e4ebe396600b0b860359466b18532e14399a8ccf5a3759`，独立只读 review `PASS`。
- observer `e33cfec8...`，independent review `PASS`；launcher `0fb10a80...`。
- post-build 八项 full hashes 全部匹配同源独立运行；title 和前三个输入页也精确匹配 run1：
  - title `5f779814...`
  - save page `74d2c7bd...`
  - slot5 option `be8c276c...`
  - load confirmation `d2ff91fe...`
- 到失效前只发送了冻结路线中的四个点击：`(112,791)`, `(31,242)`, `(50,818)`, `(89,792)`；没有重试或新增 gameplay input。

## 精确失效事实

prereg 写的是：每个 listed page 要 current capture + zero-input stable recapture；对应 pair 必须 byte-identical/AE0；语义 anchor、expected SHA、page order mismatch 立即 invalid，不得加、重试或移动 input。

在冻结坐标 `(89,792)` 只点一次 `[000]确认读取存档` 后：

- `r2-08-loaded-main.png` 与 `r2-09-loaded-main-passive.png` 字节相同、AE0，但 SHA 是 `9b3ab06ca8f3789cbbb5631e6085605ac800fa7a1c37b0a39551c4efbc04c7a7`，不是 expected main `5569ab54...`。
- 原图仍显示旧确认页；输入历史在 `[000]确认读取存档` 下方新出现 `0`。这证明唯一 transport 已进入 Tk input，但游戏线程尚未消费。
- 执行者依 prereg 当场宣布 INVALID/STOP，没有重试、额外 input、signal 或继续路线。

主协调者只授权诊断性零输入观察，明确“不救回有效”：

- delayed `r2-10` 变成 expected main scene，SHA `5569ab549bdd967c7d1c0aaf8068b77c50ade8e55a2eeab0fb8b9116d5f55c70`，可读 `[4113]`；`r2-09→10` AE 158363。
- 第二张零输入 `r2-11` 与 r2-10 字节相同、AE0、同 SHA。
- 因而唯一 `(89,792)` click 最终正常消费；没有第二 transport。run2 仍永久 INVALID/STOP，当前窗口停在 exact expected main scene，unit/window 仍活着。
- action.log SHA `d3f67858e1dbeef70707c80531531c4ca4467103c44cb6e71050debea8bc0ec7`；outcome SHA `e74f294eb066819cda21d3ab5507c0b75cd992f1e66a5705e1137d50a5c3de5f`。

这与 run1 target click 的已知异步现象同类：immediate frame 仍旧，稍后才 redraw。run2 prereg 对 target click 特别允许异步等待，却没有对普通按钮统一采用“先等预期语义 anchor，再取稳定 pair”的规则。

## 当前上游又前进

run2 启动后只读核对发现 `upstream/master` 已从 `abebf33b...` 前进到 `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`，两个提交仅修改吃饭与阴道高潮纸娃娃 talk/data、相关说明、package/update log；没有修改 `Script/Settle/default.py`、`Script/Design/talk.py`、`time_stop_off.csv`、observer 或这条林口交→惊蛰→解除时停路线的代码。新 talk 会改变生成 `Character_Talk.json` 的整体哈希，但没有证据显示本路线输出变化。run2 的 pinned snapshot/provenance 没有被悄悄改写。

## 请作最后决定

1. 给出 `RUN2 INVALID / CONTINUE DIAGNOSTIC`、`RUN2 INVALID / CLOSE`、`RUN2 SALVAGE` 或 `REVISE`。我们认为按 literal prereg run2 已 invalid，不主张 salvage；由你最终决定。
2. 当前 invalid run2 已在 exact expected main scene，且没有额外 gameplay input。是否允许继续剩余冻结物理路线，只作为 endpoint 诊断，尝试到 sample2 后点一次 active `[4115]`？这样可先判断 Route A 端点，而后仍另建 fresh valid run；还是必须现在关闭，下一轮从头同时验证时序和端点？
3. 下一次 fresh run 的统一页面时序规则应如何写？建议机械规则：每个 gameplay transport 后，按固定 1 秒间隔零输入 capture，最多 5 秒；中间旧页/输入回显不算失败；只有出现 expected semantic anchor 后才取第二张零输入 stable frame并要求 byte-identical/AE0；5 秒内未出现 expected anchor、出现错误新页、或状态异常才 invalid。是否接受？是否需更短/更长或用日志/窗口事件作条件？
4. 如果允许 current run2 继续诊断且 endpoint 成功，下一轮 fresh valid run 是否仍必须从头；还是 endpoint 已被正常物理路线诊断证明，下一轮可直接成为 formal baseline？请明确，不要默认。
5. 上游漂移：是否允许 route rehearsal 继续明确钉在 `abebf33b`，但 fresh valid/formal baseline+candidate 统一从最新 `3a1c9e` 重建并重新核对所有页面/state anchors；还是必须先在 `3a1c9e` 再做一个 disposable endpoint rehearsal？两提交不触碰相关代码但会改变整体 talk build。
6. observer `e33cfec8...` 是否继续冻结，不因 talk-only upstream 漂移重写？
7. 是否需要玩家现在介入？这里不改玩法语义、不外发。
```
