/investigate-game-bug

请以怀疑视角裁决 T2 attempt6 的 probe 错误是否允许一个只删除无关字段的 attempt7。不要把静态复核当成动态通过；也不要因为前两次工具失败就降低原诊断 A 的合同。

请读取：

- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt5-aborted.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/fable-current-upstream-attempt5-hook-review-ruling.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt6-invalid.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt6/INVALID.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt6/diagnostic_tk_launcher.py`

已验证事实：

1. attempt6 使用你要求的窄 wrapper、最外层等待边界、内存日志、RNG 前后相等检查和 attempt4 画面哈希硬门禁。
2. 正常载入 save99 后，第一次 `[6001]` 的 outer_wait_begin 快照读取 `character_data.sp_flag.group_sex_mode`，baseline `SPECIAL_FLAG` 没有此成员，立即抛 `AttributeError`；高潮结算尚未运行。
3. 错误页哈希 `b251956b...` 不等于硬门禁 `00f5...`，因此整轮正确作废；后五次等待未执行。
4. `group_sex_mode` 实际是全局 `cache.group_sex_mode`。这个额外角色快照字段不属于你要求的高潮输入、`orgasm_edge_count`、`orgasm_level` 或 target601 `premise_data`，删除它不改变三个 wrapper 的转发或所需记录。
5. 其余被读成员已在当前上游类定义中静态确认存在，但 attempt6 没有动态跑过 settlement，不能声称 wrapper 已通过。
6. 错误处理器只改了隔离 runtime 的 save；原始 save99 哈希未变。污染副本保留、不复用；allocator/runtime 已清理。

唯一候选：从 evidence launcher 删除该一行额外 `sp_flag.group_sex_mode` 快照，其他 attempt6 合同逐字不变，用 pristine runtime 重跑完整同38物理输入、六次6001；任何异常/RNG变化/结果帧哈希不等立即作废。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头。PASS 时明确是否只删这一行即可；REVISE 时只给必须增加或删除的一项检查；BLOCKED 时说明为什么同一窄 wrapper 设计不能再重试。不要写 PR 文案，不要建议开放式试玩。
