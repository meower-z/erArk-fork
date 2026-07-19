/investigate-game-bug

请以怀疑视角裁决 T2 attempt7 的画面门禁是否过早执行，以及是否允许一个只修正“何时判结果帧”的 attempt8。不要放宽 exact hash，不要把黑屏中间帧当结果，也不要因连续工具失败自动允许重试。

请读取：

- `openspec/changes/judge-orgasm-edge-once-per-settlement/fable-current-upstream-attempt5-hook-review-ruling.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/fable-current-upstream-attempt6-review-ruling.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt7-invalid.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt7/INVALID.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt7/diagnostic-trace.jsonl`
- attempt4 正常结果帧与 attempt7 frame-28/pixel diff。

已验证事实：

1. attempt7 严格只删了 Fable 授权的一行错误快照字段；fresh runtime，路径到第一次6001前无异常。
2. controller 在第一次6001+Return 后捕获 frame-28，SHA `961b8b...`，不等于硬门 `00f5d1...`，因此按原合同停止，第二次等待未输入。
3. 主线程与 visual agent 都查看了画面：frame-28 仍是几乎全黑的未完成重绘中间状态，不是正常主指令面板。
4. trace 只有 probe setup、三个 wrapper installed、finder removed；没有 `outer_wait` 完成记录，也没有任何wait诊断/RNG记录。无游戏异常。故截帧时第一次等待尚未从最外层 wrapper 返回。
5. setup RNG前后相同；source/runtime save均未变；已清理。

唯一候选修正：attempt8 的代码和38物理输入合同不变。每次 Return 后先反复只读捕获画面、不发送任何输入；只有同时满足 (a) trace 已出现对应 `outer_wait` 完成记录，(b) 画面完整显示主指令面板而非黑屏/中间帧，才把该帧命名为 post-wait result 并执行原 exact SHA `00f5d13c...` 门禁。在此之前的中间帧只记诊断，不判结果也不输入下一步。若等待在有限上限内不返回则作废；若返回后的完整结果帧仍不等 exact SHA则作废。其他wrapper/RNG/六次路线/candidate禁令全部不变。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头。PASS 时给一个有限等待上限和完成判据；REVISE 时只改一项稳定判据；BLOCKED 时说明为什么无法区分中间重绘与结果。不要写PR文案，不要建议其他路线。
