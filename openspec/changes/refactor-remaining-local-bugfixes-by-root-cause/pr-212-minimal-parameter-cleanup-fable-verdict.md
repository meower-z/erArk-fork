## PASS

### Reviewer 说法是否属实

**部分属实：存在真实的重复计算，但被重复的因子说错了。** 我独立核对了候选代码与旧 PR commit `c72d25a54` 的差异及三个修正因子的实际调用路径：

- **State 17 苦痛基础修正**（`chara_base_state_adjust`）：State 17 在 CSV 中 type=1，走 common 的 `else` 分支，新旧版本都只调用 **1 次**。
- **State 23 心理快感能力修正**（`chara_feel_state_adjust(character_id, 23, ability[36])`）：全仓只有 helper 内这一处，新旧版本都只调用 **1 次**。Reviewer 所说的"心理快感能力加成计算两遍"**不符合代码事实**。
- **连续指令修正**（`continuous_adjust`）：这才是真正重复的因子。common 在 `common_default.py:253` 已执行 `final_adjust *= continuous_adjust`（连续 5 次时为 0.4），旧 PR 把已含 0.4 的 `final_value` 连同同一个 `continuous_adjust` 传入 helper，helper 又乘一次 —— **旧版乘了 2 次**。提供的动态数字自洽：旧版 `100×1×0.4×2×0.4=32`，候选 `100×1×0.4×2=80`。

即 reviewer 发现了真实的 bug（走 pain-as-pleasure 路由时数值被多打了一次连续指令折扣），但把重复因子误称为心理快感能力加成。PR 材料如需引用 reviewer 意见，应表述为"连续指令修正重复计算"。

### 四行删除是否完整且最小

**是。** 我确认 `git diff c72d25a54` 的 numstat 为 `0 additions / 4 deletions`，只改 `Script/Settle/common_default.py`：删除的恰好是重复乘法一行、因此死掉的参数、其文档行、及唯一的传参处。仓内 `route_pain_delta` 共 5 个调用点：common 一处（改为 2 参），Second_effect 四处 direct writers（`Second_effect.py:1247/1840/2626/3201`）本就是 2 参调用，旧版第三参默认 1 —— 删除对它们的数值**无任何影响**。`favorability` 结算里的另一处 `continuous_adjust`（`common_default.py:594` 起）与苦痛路由无关，不在范围内。两文件 `py_compile` 通过，`git diff --check` 干净。

设计边界保持不变：`route_pain_delta` 与四个调用点原样保留，无 helper 重写、无调用点重构，符合用户授权范围。修复后语义与 upstream 一致 —— 连续指令折扣恰好作用一次，心理快感能力修正在路由处恰好作用一次。
