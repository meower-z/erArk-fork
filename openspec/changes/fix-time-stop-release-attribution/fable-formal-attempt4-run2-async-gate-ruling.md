# Fable ruling: attempt 4 run 2 asynchronous page gate

Invocation: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Prompt: [fable-formal-attempt4-run2-async-gate-prompt.md](fable-formal-attempt4-run2-async-gate-prompt.md).

Exact response follows.

```text
## 裁定

**1. `RUN2 INVALID / CONTINUE DIAGNOSTIC`。**
按 prereg 字面规则 run2 已 invalid，维持原判，不 salvage——追认会让下次 gate 形同虚设。但事后零输入观察证明失效原因是时序规则缺陷（普通按钮无异步等待条款），不是证据污染：唯一 transport 最终被正常消费，r2-10/11 与 expected main SHA `5569ab54...` 完全一致。这属于"规则误伤"，不是"运行可疑"。

**2. 允许继续，仅作 endpoint 诊断。**
当前窗口停在 byte-exact expected main scene、无任何多余 gameplay input，是已知干净状态。继续冻结物理路线到 sample2 并点一次 active `[4115]`，代价近零、能提前证伪 Route A 端点。硬性条款：全部产物标记 `DIAGNOSTIC ONLY`，不得出现在任何 PASS 论证或 PR 证据中；若中途任何页面偏离冻结路线，立即停止，不重试。

**3. 接受机械时序规则，两处修改。**
- 最大窗口从 5 秒放宽到 **10 秒**。零输入等待不会污染证据，放宽只花时间；5 秒这个任意上限刚刚制造了一次误判，Xvfb 下 Tk 重绘慢是已观测事实（r2-09→10 即超出即时窗口）。
- "到达"判定用 **semantic anchor**（如可读的 `[4113]`/`[4115]` 文本），不用整页 SHA；anchor 出现后再取零输入 stable pair，要求 byte-identical/AE0，并核对 expected SHA。中间旧页、输入回显不算失败。
- 不引入日志/窗口事件作为 gate 条件——保持 observer 纯截图判定，日志可留作补充诊断，不参与判 invalid。
- Invalid 条件只剩三个：10 秒内 anchor 未出现、出现错误的新页、进程/窗口异常。

**4. 下一次 fresh valid run 必须从头，且它才是 formal baseline。**
endpoint 诊断成功只降低风险，不能把 run2 或诊断续跑升格为 baseline——诊断段运行在一个已被判 invalid 的 unit 上，链条不完整。明确规定：下一 run 从 title 开始，用第 3 条新时序规则，一次覆盖时序与端点。

**5. 上游漂移：诊断续跑钉在 `abebf33b`；formal baseline+candidate 统一重建于 `3a1c9e6`。**
不需要在 `3a1c9e6` 先做额外的 disposable rehearsal——两个提交不触碰 `Script/Settle/default.py`、`talk.py`、`time_stop_off.csv` 或路线代码，风险由 formal run 自身的 prelaunch anchor 重核对覆盖。注意所有 expected page SHA 必须在 `3a1c9e6` 上重新推导（talk build 变了，不得复用旧哈希表）；若重核对发现路线页面出现非预期差异，停下重新评估，那时再考虑 rehearsal。

**6. observer `e33cfec8...` 继续冻结。**
talk-only 漂移不触及 observer 逻辑。若 expected 哈希表当前内嵌在 observer 里，把它拆成 per-run manifest 数据文件，observer 代码本身不重写。

**7. 不需要玩家介入。**
全部是时序/工作流决定，不改玩法语义、不外发。继续执行。
```
