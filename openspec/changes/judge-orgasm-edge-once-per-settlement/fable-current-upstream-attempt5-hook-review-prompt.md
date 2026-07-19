/investigate-game-bug

请以怀疑视角决定 T2 当前上游只读诊断是否可以用一个更窄 hook 继续。不要因为现有代码测试通过而放宽证据要求，也不要把“RNG 状态相同”自动等同于“观察无行为影响”。

请读取：

- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt4-invalid.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt5-aborted.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/fable-current-upstream-attempt4-review-ruling.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt5/ABORTED.md`
- 需要时读取当前上游相关 `init_character_behavior`、`orgasm_settle`、`search_target` 代码。

已验证事实：

1. 你上一轮最终选择 A：同 save99、seed0、PYTHONHASHSEED0、六次 `[6001]`，逐次观察清流/特蕾西娅/凯尔希的高潮输入、寸止计数、高潮等级和 target601 发现前提；不跑 candidate，不猜第七次。
2. attempt5 的 global `sys.setprofile` 安装前后 Python/NumPy RNG fingerprint 相同，但该机制在过滤前接收所有 Python call/return，启动很慢且观察面过宽。
3. attempt5 的 Tk 窗口约 105 秒出现，只走到存档页8/9；未加载 save99、未执行等待，因此没有诊断结果。运行已清理，存档未变。
4. 唯一备选是正常 import 完成后的 evidence-only loader，仅包装：
   - `init_character_behavior()`：只标记一次等待边界；
   - `orgasm_settle()`：只复制已有实参字典及清流/特蕾西娅/凯尔希的前后 `orgasm_edge_count`、`orgasm_level`；
   - `search_target()`：只复制函数已经计算出的 target601 `premise_data`，不额外调用任何前提。
5. 每段日志前后都比较 Python/NumPy RNG state，不同立即抛错；包装器不提前 import 游戏模块、不改变返回值/异常、不进入生产 diff。真实 Tk 仍由 visual agent 逐帧走完全相同六次路线。

请裁决这个窄 hook 是否足够不扰动、能回答你选定的诊断 A。只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头：

- PASS：给出运行前必须固定的最小合同；
- REVISE：指出必须删掉/替换的具体 wrapper 或还需增加的一项不扰动自校验；
- BLOCKED：说明为何任何函数包装都无法提供可信诊断，并给一个更窄且有限的替代观测方法。

不要写 PR 文案，不要建议开放式试玩，不要提出多个并行方向。
