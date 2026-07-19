# Fable ruling: attempt 4 transient wait-page race

Invocation: `claude -p --model claude-fable-5 --effort medium --tools "" --no-session-persistence`.

Prompt: [fable-formal-attempt4-transient-wait-race-prompt.md](fable-formal-attempt4-transient-wait-race-prompt.md).

Exact response follows.

```text
## 裁定

**总判:这是正常的 Tk 鼠标竞态,不是证据污染,协议错在把非关键瞬时页设成了硬门。** 依据:未发送任何额外输入(action log 在案),静态调用链完整解释了分叉机制(`askfor_wait()` 清零 `w_frame_up` 后被同一次 click 的 release 满足),且 run2 到达的 H 菜单与 run1 补 Return 后的 H 菜单 SHA 完全一致(`223720ac...`)——两条分支收敛到同一字节状态,这是"同一语义状态、瞬时页被消费"的强证据,而非状态污染的特征(污染会产生不同终态)。

逐题回答:

### 1. CONTINUE FROM H MENU

**明确禁止补发那个 Return。** 等待已被 release 消费,此刻补 Return 会落入 H 菜单上下文,成为一次未预注册的真实输入——那才是污染。把稳定 H 菜单(`223720ac...`)直接认定为 `[5052]` 成功完成的 semantic checkpoint,从此继续四轮口交、sample1、切目标、sample2、active `[4115]` endpoint。全程维持 `DIAGNOSTIC ONLY` 标记,任何产物不得进入 PASS/PR 证据。

### 2. 正式 prereg 的竞态处理

**选方案一(可选瞬时页 + 双预注册分支),并采纳方案三的后半句(允许 baseline/candidate 分支不同)。** 具体规则:

- 单击 `[5052]` 后,按既有节奏截图;若"进入无意识奸模式"页稳定出现(byte-identical pair),按一次 Return;若直接出现 H 菜单,不补任何输入。
- 两分支必须收敛到同一语义锚(可读 `[6602]` 与 `[4115]` 的 H 菜单)并各自取得 within-arm 的 stable pair;记录实际走了哪条分支。
- **允许 baseline 与 candidate 走不同分支。** 理由:分叉点由 OS 级事件时序决定,不可控;要求分支一致会让合法配对随机作废。而该分支差异不改变语义状态——静态链已证明 H common settle 在 draw 返回后无条件执行,wait 页上的输入只是"任意键消费",不是有意义的 gameplay input;且 candidate diff 只在 `Script/Settle/default.py`,输入系统两侧同码。冻结要求改为:**语义状态一致 + 有意义输入序列一致**。
- 否决键盘 transport 方案:偏离已探索的正常玩家路线,且 key-release 有同类竞态,零收益。

### 3. "错误新页"的精确定义

一个稳定页是"错误页",当且仅当它**不在预注册语义链上**:显示错误文本、意外场景、或链上未枚举的菜单。**沿链跳到更后的已枚举稳定 checkpoint 不是错误页**——记录跳过、继续执行。必须逐页出现的:稳定交互决策点(下一个有意义输入在此选择的菜单)——这些是门。瞬时 wait 页("按任意键"类过渡页)只是可选证据:拍到了就存档,被竞态消费了就记录分支,不设门。

### 4. 门的可执行规则

**是,以"状态改变动作的最终稳定语义 checkpoint"为门**,但加一条不可放宽的例外:**承载被测结算文本的 wait 页是硬证据要求**。sample1/sample2/endpoint 处若关键结算输出显示在可被竞态消费的 wait 页上,而截图节奏(1 秒)未能捕获可读帧,则**该 sample 作废,整轮 run 重启**——测量页不适用"最终锚点即可"的放宽。竞态只消费紧跟触发点击的第一个 wait,1 秒节奏通常来得及(r2-14 即在 1 秒内捕获),但捕获失败时的处置必须预注册为"重启",不是"用后续状态推断读数"。

### 5. 不改游戏代码

**不改。** 该竞态对真实玩家的影响至多是通知页一闪而过,状态结算完全一致,不妨碍游戏、不损坏存档;当前候选也不触碰输入系统。在 investigation record 里记一条低优先级观察(`askfor_wait` 与 command selection 共用 mouse state,单击可消费紧邻 wait 页),供将来独立评估,不并入本任务、不擅立新 bug。

### 6. observer 与正式包

observer `e33cfec8...` **继续冻结**。正式包(provenance `7f0e6b3a...`)**可直接用作 formal baseline/candidate,无需 disposable rehearsal**,附两个前置条件:(a) 先把第 2、3、4 条的分支规则写入 prereg 文档再启动;(b) 本次 diagnostic 须先走到 `[4115]` endpoint——若途中暴露新阻断,回来复议;若干净到达,formal run 从 title 直接开始,baseline 完成后才准 candidate,旧 run2 永不追认。

### 7. 玩家介入

**不需要。** 协议修订与 diagnostic 续跑均为内部、可逆、不改玩法语义、不外发,不满足停下等玩家的条件。继续执行。
```
