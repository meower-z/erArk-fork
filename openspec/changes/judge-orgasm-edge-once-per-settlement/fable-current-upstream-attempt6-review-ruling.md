`PASS` — 只删 launcher 第 109 行 `"group_sex_mode": character_data.sp_flag.group_sex_mode,` 这一行即可，attempt6 合同其余部分逐字不变。

我对 baseline `72e28051e` 独立复核了裁决依据，不依赖你的静态结论：

1. **故障字段定位属实**：`group_sex_mode` 在该基线只存在于 `Cache`（`game_type.py:1808`，`class Cache` 起于 1634 行），`SPECIAL_FLAG` 类体中不存在该成员。`AttributeError` 的归因正确，且该字段确实不属于原裁决要求的三项测量（高潮输入字典、`orgasm_edge_count`/`orgasm_level`、target-601 已有 `premise_data`）中的任何一项。删除它不触碰三个 wrapper 的转发、边界语义或必需记录。
2. **其余快照成员逐一核实存在于基线类定义**：`SPECIAL_FLAG.is_h`、`SPECIAL_FLAG.see_pl_h`、`BODY_H_STATE.orgasm_edge`（467 行）、`orgasm_edge_count`（453 行）、`orgasm_level`（449 行）。另核实了 probe 的位置参数映射与基线签名一致：`orgasm_settle(character_id, change_data, normal, extra, un_count)`（`second_behavior.py:371`）、`search_target(character_id, target_list, null_target, premise_data, ...)`（`handle_npc_ai.py:436`）。
3. **诊断 A 合同不降级**：attempt7 的产出仍必须自证——六帧全部字节等于 `00f5d13c...`、每段 `guarded` RNG 前后相等、无异常，缺任一项整轮作废。静态复核只降低了再浪费一轮的概率，不构成任何"已通过"声明；attempt6 的失效不改变对 attempt7 的验收标准。
4. **失效模式安全**：即便还有静态复核漏掉的动态缺陷（例如存档实例缺类定义属性），其表现是异常→错误页→帧哈希不等→硬门禁作废，代价是一轮运行，不是污染证据。因此不需要为其余快照字段追加删除或预检——保留 attempt6 其余字段逐字不变反而使 attempt7 与已裁决合同的可比性最大。

不允许的引申：本 PASS 仅授权删除该一行并重跑；不授权修改 wrapper 语义、快照其他字段、38 次物理输入或硬门禁哈希。
