# output 线现状判定：`fix-time-stop-release-settlement-output`

## 结论

output change 是一个**捆绑了三件事**的更大变更；三部分已分别被覆盖或即将被覆盖，**仅剩 1 项独立残留**（marker 收窄，非用户报告症状）。建议本 attribution PR 合并后，将 output change 归档，或把残留单列为一个极小的独立 change。

## 三部分拆解

| output change 内含 | 对应任务 | 现状 |
| --- | --- | --- |
| 1. 归属：把每个干员的时停释放记进其 `TargetChange` | 2.1 | **= 本 attribution PR**（`fix-time-stop-release-attribution`，已推 origin）|
| 2. 数值缩写：K/M 单位与负号 | 2.3 / 3.1 | **已由上游 PR #217 覆盖**（`fix-compact-value-formatting` 已归档；`attr_text.py` 现已用 `abs()` + `(digit_count-1)//3`，确认在 upstream/master）|
| 3. marker 收窄：仅对非零计数干员置 `time_stop_release`，同时对全部干员保留无意识衣物/精液/失窃物恢复 | 2.2 | **残留**，两处都没覆盖 |

## 关于「博士博士」显示

用户报告的「博士博士」抬头 = 归属 bug 的直接后果：旧代码把干员绝顶经验记进玩家根对象，结算面板遂在玩家块（抬头 `name+nick_name`＝博士博士）下显示。本 attribution PR 修复归属后，经验改由干员的 `TargetChange` 显示在干员抬头下，「博士博士」误显示随之消失。已用真实结算显示代码前后对照验证（见 `.codex-evidence/time-stop-release-attribution/`）。

## 唯一残留（2.2）是否真问题

- 当前代码对 `cache.npc_id_got` 里**每个**干员都置 `time_stop_release = True`，即使其延迟绝顶计数全为零。
- attribution PR **有意不含**此项（proposal 明确「保留原有的零计数标记 / 空调用 / 无意识恢复路径」）。
- 影响面：`time_stop_release` 会让 `handle_self_time_stop_orgasm_relase` 为真，进而影响后续经验的无意识转换判定；对零计数干员置此标记在理论上可能让**其后**发生的普通结算被误判为时停解放。这是一个防御性收窄，**不是**用户当初报告的症状，目前也无复现证据表明它单独造成可见错误。

## 建议

1. 本 attribution PR 合并后，output change 的 1、2 均已落地/被上游覆盖。
2. 残留 2.2 若确认为真 bug，建议单开一个极小 change（只改 `time_stop_release` 的置位条件），不要塞进本 attribution PR（避免扩大范围）。
3. output change 目录可标注为「被 #217 + attribution PR 拆分覆盖，残留仅 2.2」并建议归档。此处**未擅自改动**其 tracked openspec 文件，交由你决定。
