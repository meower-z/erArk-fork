/investigate-game-bug

上一轮你已 PASS 边界 C 和完整记录。fresh-context critic 随后发现两个必须明确的 wiring contract；记录现已按下述文字修订。请判断这些修订是否解决 critic 意见并保持你已批准的边界，不重新讨论已裁决的 continuous tuning。

## Critic finding 1 与记录修订

`handle_extra_orgasm` 不能在 helper 返回 True 时提前结束整个函数。记录现在规定：用同一个 Boolean 选择 `心理快感和恐怖` / 原 `苦痛和恐怖` 文本；两种情况都继续恐怖结算并清零 `extra_orgasm_count`。测试必须断言文本、恐怖和清零。

## Critic finding 2 与记录修订

记录现在明确：

- common active-positive 必须同时转发 `change_data` 和 `change_data_to_target_change`，两者都只记录 state 23；
- active-positive direct writer 在 sleep 或 unconscious 导致 canonical state 23 early return 时，helper 仍返回 True 表示转换路径已接管，caller 不得回落写 state 17；state 17/state 23/两类 change record 均不增加。

## 保持不变的 owner contract

helper 接收 source-adjusted signed delta；inactive/nonpositive False；active positive 只委托 canonical state 23 一次并 True；helper 不计算心理能力系数；True 时普通 direct writers 跳过 state 17 写入。现有 common 两阶段 continuous tuning 不改。

输出 `PASS` 或 `REVISE`。如 REVISE，只列仍未解决的 mandatory design issue。除非确有新玩家语义问题，否则不要要求玩家输入。
