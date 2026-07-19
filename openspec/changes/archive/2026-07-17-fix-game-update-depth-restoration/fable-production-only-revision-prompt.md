/investigate-game-bug
/review-erark-pr-artifacts

你是本次修复的 PR 文案写手。请用中文输出一份可直接替换的 PR draft，只输出 Title 和 Body，不要解释。

约束：

- 候选提交只修改 `Script/Design/update.py`，不包含任何自动化测试；本地测试不得出现在 PR-facing 文案中。
- 用户此前已允许在难以取得运行时证据时直接做这个小修，因此把它定位为“潜在的运行深度不变量修复”，不要声称已观察到第三次进入、守卫放行或实际重复结算。
- 可以陈述已经由源码确认的嵌套路径：角色结算过程中，`recover_from_unconscious_h()` 会调用 `game_update_flow(5)`。
- 可以陈述由旧代码直接证明的状态错误：内层返回时 `finally` 固定把计数清零，而外层仍在运行；这使后续防重入判断失去正确的深度依据。
- 不要写测试、测试命令、运行次数、本地路径、截图、证据缺口、调查过程或未来计划。
- 不要夸大，不要加入实现之外的承诺。

现有 draft：

Title: 修复 game_update_flow 嵌套调用返回后运行深度被误清零的问题

Body:

## 问题

`Script/Design/update.py` 的 `game_update_flow()` 用 `cache.game_update_flow_running` 记录更新流程的运行深度，并在深度达到 2 时拦截更深的嵌套调用。但生产代码中存在嵌套路径：角色结算过程中经 `recover_from_unconscious_h()` 会再次调用 `game_update_flow(5)`。旧实现在每一层的 `finally` 中都把标志固定清零，于是内层调用返回时，外层流程明明还在运行，深度却已被清成 0。此后在外层剩余的执行期间，新的进入会被当作第一层放行，`>= 2` 的防重入守卫实际失效。

## 修复

进入 `game_update_flow()` 时先保存调用者的深度 `caller_depth`，再将 `cache.game_update_flow_running` 置为 `caller_depth + 1`；`finally` 中不再固定清零，而是恢复为 `caller_depth`。这样每一层退出时只撤销自己增加的那一层深度，嵌套调用返回后外层深度保持正确。`>= 2` 的守卫阈值不变，时间推进、角色结算与聚焦的执行顺序也不变。

审计要求修正的唯一实质问题：

> “新的进入会被当作第一层放行，`>= 2` 的防重入守卫实际失效”超出了现有证据。请删除这一现场失败断言，改成由代码本身可证明的“不再能正确反映外层仍在运行，后续防重入判断失去正确依据”。

输出格式：

Title: ...

Body:

## 问题
...

## 修复
...
