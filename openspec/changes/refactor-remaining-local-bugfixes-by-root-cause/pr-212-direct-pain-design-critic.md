REVISE

边界 C 本身正确：它是覆盖 common 路径和四个 direct writers 的最小完整边界；心理能力系数只在 canonical state-23 结算中计算一次，也不会形成递归环。

必须补两项：

1. `handle_extra_orgasm` 应根据 helper 的返回值切换描述：

   - 已转换：显示“心理快感和恐怖”
   - 未转换：保留“苦痛和恐怖”

   恐怖结算与额外高潮次数清零保持不变，并加入相应断言。

2. 测试矩阵必须明确覆盖：

   - common 正向转换同时正确转发 `change_data` 和 `change_data_to_target_change`，两者只记录 state 23；
   - direct 正向转换在睡眠、无意识导致 state-23 提前返回时，helper 仍返回“转换路径已接管”，caller 不得回落写入 state 17，且 state 23 和变更记录均不增加。

除此之外，没有发现 owner、重复 adjustment、continuous tuning 或公开语义方面的 blocker。
