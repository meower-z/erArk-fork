`REVISE`

## 一、文档裁决:撤回基本准确,但一处表述仍会误导新人

`target-scope-save99-v-reachability.md` 的 Status 段、"Rejected static two-candidate model" 标题和结尾的 falsification 段都正确;人数修正(九名 B 候选)与保留算式的处理也合理。日志核对无误:我重新算了 `/tmp/erark-t7-seed-search-20260715/seed-00-choice4-bound.log` 的 SHA-256,与文档一致;58 行日志逐项支持已验证事实 1–7(两个发现面板 `common_behavior_id=null`、target 前后均为 3、effect_parts 为空、11:57 完成)。

需精确修改两处:

1. **第 11–15 行的小节** 标题 "Why one wait can settle masturbation twice" 和结论句 "Therefore the first normal wait can run the real V-affecting effect 524 twice for one NPC" 仍是**现在时陈述句**。顶部 Status 免责不足以中和一个断言式小节标题——按小节阅读的新人会把它当成仍然成立的机制分析。改为:标题 → "Rejected scheduling premise: why the model expected two settlements";第 15 行 → "该模型据此认为首次等待会调用两次 effect 524;seed-0 运行已证明该调度前提不成立"(过去时+指向反证)。
2. **第 13 行的机制描述本身在代码层面就是错的**,不只是被运行时推翻。我核对了上游代码:effect 结算发生在 `judge_character_status()` 内 (`character_behavior.py:232`),而该函数对 NPC 只在行为为 `SHARE_BLANKLY`(新选行为后)或 `MOVE` 时调用 (`character_behavior.py:169-177`) ——即**结算在行为开始时,不在结束时**。存档里 11:45 开始的旧 `masturebate` 行为的效果早在存档前的开始时刻结算过,永远不会"到点再结算一次"。且群交 type-1 钩子 (`handle_npc_ai_in_h.py:580-586`) 在结算点之前直接把 `behavior_id` 覆写为 `SHARE_BLANKLY`。"first settlement still uses the 11:45 start" 这句应标注为该模型的错误假设,而非中性机制转述。

## 二、反证足以停止 seed 扫描:是

逻辑成立且我不降低门槛地认可:随机 seed 只能改变**已发生调用**的结果分布,不能创造调用。seed-0 运行显示零次 `handle_masturebate_add_adjust` 进入,故 0..63 扫描全部在扫一个不存在的分支。暂停正确;3.2 保持 `TK EVIDENCE BLOCKER`、不声称 PR-ready 也正确。

## 三、唯一下一步:选 A

选 **A**,并将其收窄为一个可判定命题——我已替你验证它是可回答的,不是开放式追踪:

> 沿 seed-0 trace 静态确认:(1) `judge_character_h_obscenity_unconscious` → `npc_ai_in_group_sex` (`handle_npc_ai_in_h.py:118` 调用点、`580-586`/`625-631` 覆写点) 在结算前丢弃旧 `masturebate` 行为;(2) 结算只在 `SHARE_BLANKLY→find_character_target→judge_character_status` 的新行为开始时发生;(3) 沿自慰 state machine(`masturebate` flag 3 / `STATUS_ARDER` 路径)判定:save99 中是否存在一个确定的正常等待时点,使某 B 候选**新选中**行为 418 并在同一玩家等待内触发一次 effect 524。

- **成功证明**:存在具体的等待序列(第 N 次 `[6001]` 时某 NPC 重入 418),effect 524 在该时点必然被调用一次——此时才恢复受控 seed 运行(定点验证该一次调用,不是盲扫),Tk 证据路线重新可行。
- **失败证明**:若 state machine 在群交 type-1 下永远不再进入 418(或进入时 V 不可选),则 save99 路线在任何等待次数下都不可达 V 绝顶 Talk_Common——那时才转入 B(冻结 save99 路线、候选保持代码级 bug、Tk/PR 维持 blocked),且 B 的结论有静态证明背书而非仅一次运行的归纳。

不选 B:单次 5 分钟等待的 trace 只证明"这一个时点没调用",不证明"任何正常时点都不调用"——现在冻结是过早归纳。不选 C:A 收窄后本身就是区分状态生命周期(丢弃-重选-开始时结算)的最窄步骤,不存在更窄的替代。
