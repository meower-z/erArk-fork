1. `CODE: PASS`
production-only diff 语义正确：保存 `caller_depth` 并在 `finally` 恢复，使嵌套调用退出时恢复到调用者深度而非清零。逐层验证：深度 0→1（外层）、1→2（内层）、深度 2 时守卫 `>= 2` 提前返回且不改状态；异常路径经 `finally` 逐层正确回退。与旧代码相比消除了“内层退出把外层标志清零、导致守卫失效”的缺陷。单文件、单提交、无越界内容，适合 side-branch review。

2. `UPSTREAM SCOPE: PASS`
不提交 tests/ 完全符合用户明确要求；测试已作为本地未跟踪证据保留且哈希一致，验证链未断。**不要**往生产代码加入替代自检（assert、日志探针等）——上游无此惯例，属凭空扩 scope。

3. `PR DRAFT REQUIREMENT`
“随本 PR 提交了自动化测试”及四条测试断言**必须全部删除**——它们对 PR 内容做了不实陈述。本地测试**不得**出现在 PR-facing 文案中：技能规则明确要求省略 local-only tests；PR 中的验证性陈述只能依托随 PR 可见的证据。据此提醒：真实 Tk A/B 取证尚缺，这是本候选提交 PR 前的既存 blocker（本次裁决不改变该状态）。

4. `REMOTE UPDATE`
技术判断：是。`--force-with-lease` 用本地 bc1bfb44e 替换远端 80a711603 是让同名 fork branch 全部历史不含 tests/ 的正确且唯一干净手段（普通 push 会保留旧提交在历史中）；lease 可防远端被并发更新时误覆盖。此判断不构成授权，push 需用户单独批准。

5. **无需修改生产代码。** 必做项仅为文案与流程：删除 PR draft 中的测试陈述（经 fable-5 写手重写），并在获得授权前不更新远端；Tk 取证缺口在 PR 提交前仍需补齐。
