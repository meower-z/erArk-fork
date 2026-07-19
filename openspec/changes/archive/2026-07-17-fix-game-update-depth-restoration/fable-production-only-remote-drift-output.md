**裁定(Fable 发布监督者)——五问逐项:**

**1. 本地 production-only 候选保持不变 — 是。**
`bc1bfb44e` 满足全部约束(基于当前 upstream `3a1c9e620`、单提交、树中无 `tests/`)。远端漂移不影响本地候选的正确性,不要为迁就远端而改动它。

**2. 授权后使用该精确 lease 命令 — 是。**
命令形式正确:`--force-with-lease=refs/heads/<branch>:23188ce1a` 把预期远端值钉死在已核实的漂移提交上,若远端再次变动则推送失败而非覆盖未知状态;显式 refspec 指定了确切的本地 SHA 与目标 ref。这是最小风险的改写方式。注意此举会有意丢弃 `80a711603`(含测试的旧候选)与 GitHub merge commit——二者均无需保留,本地已持有 production 修复的唯一权威副本。

**3. 普通 merge/rebase/push 为何不行 — 因祖先污染。**
非强制 push 要求新 tip 是 `23188ce1a` 的后代,而 `23188ce1a` 以 `80a711603`(含 `tests/test_game_update_depth_restoration.py`)为父提交。任何保留该祖先的历史,测试文件都永久存在于提交历史中;即使追加一个删除测试的提交,"候选完整历史不含测试"仍不成立。满足该要求只有一条路:以不含测试的提交替换整个分支历史,即强制改写。

**4. 获新授权前必须停止 — 是。**
强制改写远端是外向、破坏性动作,需要单独授权;旧的 side-branch 推送授权不覆盖对已漂移状态的改写(Codex 本轮的解读正确)。且按程序规则,我(Fable)不能授予 push 授权——只能确认上述命令是授权后的正确执行方式。另外应向用户报告:该 merge commit 由 GitHub 在 2026-07-14 19:30 UTC 创建、非 Codex 操作,来源可能是 fork 上的 "Update branch" 按钮或自动同步,值得用户知晓但不构成阻塞。

**5. 不改变此前结论。**
漂移只影响远端候选分支的状态,不触及本地 diff、PR 文案、或证据完整性。维持:代码 PASS、文案 PASS、上游 PR artifact 因缺少真实 Tk A/B 而 BLOCKED。远端 lease 改写作为发布前的独立前置任务记录,与 Tk A/B 阻塞项并列、互不依赖。

**下一步(不需玩家输入即可继续):** Tk A/B 证据仍是唯一实质阻塞项,按 `Operate Tk Through A Local Visual Agent` 推进;远端改写等待用户单独授权后执行第 2 问命令。
