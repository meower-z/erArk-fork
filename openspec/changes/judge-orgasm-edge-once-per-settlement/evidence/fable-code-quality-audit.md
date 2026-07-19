`REVISE`

正确性、状态生命周期与测试均通过审计；仅有注释用词一档需要修。

## 正确性与生命周期（通过）

- 判定前置且完整：`candidate_orgasm_edge_count`（旧计数 + 本次 normal + un_count）与成功分支实际提交量（`climax_count = normal + un_count`，`second_behavior.py:452,465`）逐部位一致，判定输入与承诺写入等价。
- 失败路径：旧计数并入 `un_count` 释放，而 `now_data` 只由 `pre + normal/extra` 推进（`second_behavior.py:444-447`），等级不会因释放旧计数被重放；`orgasm_judge` 不再二次调用 `orgasm_settle`。测试 `test_shared_failure_releases_whole_batch_without_level_replay` 的 `degree_levels == [1,1,1,0,0,1]` 精确锁死了这一点。
- 与外部调用方无冲突：显式解放路径 `Script/Settle/default.py:6684` 以 `orgasm_edge == 2` 进入，`orgasm_edge_flag` 为假，不会触发 clear/rebind，传引用的 `orgasm_edge_count` 不被本函数误改（copy-before-clear 也兜住了别名情况）。`clear()` 与其他处置零写法（`default.py:2278`）对下游等价——所有读方都用 `.get`/求和。
- 时停、非寸止、部位 3/未知部位的旁路语义与旧代码逐一对齐（参数化测试覆盖）。

## 测试质量（通过）

7 个测试各守一条不变量，无互相掩盖的断言；`test_real_orgasm_judge_calls_real_settlement_once` 用真实 `orgasm_judge` → 真实 `orgasm_settle` 链验证 `calls == 1`，正是本 PR 的核心回归。AST 抽取 + 桩环境的做法对单文件小 scope 合理。无明显冗余。

## 需修事项（均为注释用词，低严重度）

1. **`second_behavior.py:412`** — 根因：「本次普通解放输入」「实时账本」是本 PR 发明的术语，代码里该字典的既有名字是「不计数高潮（结算字典）」，字段是「寸止计数」，读者需自行猜映射；「提前」也没有参照物。最小修改：
   - 原文：`# 共同寸止失败时，将旧账加入本次普通解放输入并提前清空实时账本`
   - 建议：`# 共同寸止失败时，将已累积的寸止计数并入本次不计数高潮一起解放，清空寸止计数并进入解放状态`

   （顺带把该行未注明的 `orgasm_edge = 2` 状态迁移写进注释，这是该块最重的一个副作用。）

2. **`second_behavior.py:392`** — 根因：「确定一次共同寸止结果」在非寸止路径并不发生，措辞略过了条件。最小修改：
   - 原文：`# 在修改部位状态前收集本次高潮，并确定一次共同寸止结果`
   - 建议：`# 在修改任何部位状态前收集本次高潮计数；若处于寸止状态，则只做一次共同寸止判定`

3. **`second_behavior.py:457`（可选，diff 相邻行）** — 根因：时停分支写入的是 `time_stop_orgasm_count`，注释却沿用「寸止计数」，与本 PR 反复强调的「寸止/时停分流」直接矛盾；该注释紧贴本 PR 改动的 `if time_stop_flag:` 行。
   - 原文：`# 绝顶计入寸止计数`
   - 建议：`# 绝顶计入时停计数`

## 建议的最小注释补丁

```
second_behavior.py:392
- # 在修改部位状态前收集本次高潮，并确定一次共同寸止结果
+ # 在修改任何部位状态前收集本次高潮计数；若处于寸止状态，则只做一次共同寸止判定

second_behavior.py:412
- # 共同寸止失败时，将旧账加入本次普通解放输入并提前清空实时账本
+ # 共同寸止失败时，将已累积的寸止计数并入本次不计数高潮一起解放，清空寸止计数并进入解放状态

second_behavior.py:457（可选）
- # 绝顶计入寸止计数
+ # 绝顶计入时停计数
```

其余（`judge_orgasm_edge_success` 的 `dict = None` 兼容默认、docstring 第 599 行「实时寸止计数」措辞、变量命名）均清楚准确，无需改动。
