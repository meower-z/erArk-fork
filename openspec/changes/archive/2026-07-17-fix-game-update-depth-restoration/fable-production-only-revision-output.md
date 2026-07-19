Title: 修复 game_update_flow 嵌套调用返回后运行深度被误清零的问题

Body:

## 问题

`Script/Design/update.py` 的 `game_update_flow()` 用 `cache.game_update_flow_running` 记录更新流程的运行深度，并在深度达到 2 时拦截更深的嵌套调用。生产代码中存在嵌套路径：角色结算过程中，`recover_from_unconscious_h()` 会再次调用 `game_update_flow(5)`。旧实现在每一层的 `finally` 中都把标志固定清零，于是内层调用返回时，外层流程明明还在运行，深度却已被清成 0。此后该标志不再能正确反映外层仍在运行，后续的防重入判断失去了正确的深度依据。

## 修复

进入 `game_update_flow()` 时先保存调用者的深度 `caller_depth`，再将 `cache.game_update_flow_running` 置为 `caller_depth + 1`；`finally` 中不再固定清零，而是恢复为 `caller_depth`。这样每一层退出时只撤销自己增加的那一层深度，嵌套调用返回后外层深度保持正确。`>= 2` 的守卫阈值不变，时间推进、角色结算与聚焦的执行顺序也不变。
