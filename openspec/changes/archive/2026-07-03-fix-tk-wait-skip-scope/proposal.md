## Why

`local_performance` 为了避免 `WaitDraw` 消费触发按钮时残留的点击/回车输入，替换了 `Script.Core.flow_handle.askfor_wait()`。当前替换版把 `cache.wframe_mouse.w_frame_skip_wait_mouse` 当作全局跳过条件：只要该标志为真，普通 `WaitDraw` 就会直接返回。

原版 `askfor_wait()` 不检查这个标志。`w_frame_skip_wait_mouse` 原本只由少数调用点显式检查，例如逐行等待和面板级等待；右键、地图移动、长时间等待等路径更多是该标志的 producer，而不是普通 `askfor_wait()` 的合法全局 skip caller。身体检查结算后依赖普通 `WaitDraw` 停住一次；当跳过标志残留为 1 时，性能 mod 会让身体检查、身体管理以及其他普通 `WaitDraw` 全部跳过，表现为点一次按钮直接略过中间输出回到按钮界面。

本次变更需要保留性能 mod 的 stale input 防护，但收窄跳过标志的作用域，恢复原版普通 `askfor_wait()` 的等待语义。

## What Changes

- 调整 `local_performance` 的 `patched_askfor_wait()` 设计：普通 `askfor_wait()` 不再因为 `w_frame_skip_wait_mouse` 为真而提前返回。
- 保留非 Web、非 benchmark 模式下的输入重整逻辑：等待前清理旧命令队列、重置 `w_frame_up`、短暂等待 Tk 点击事件传播完成、再次重置并清理队列，然后等待新的玩家输入。
- 保留 Web 模式委托原函数、benchmark 模式直接跳过等待的特殊语义。
- 保留显式调用点的跳过语义：只有像 `LineFeedWaitDraw`、`LeftDrawTextListWaitPanel` 这类调用前自己检查 `w_frame_skip_wait_mouse` 的代码，才可以按原有方式跳过等待。
- 更新 `local_performance` 测试，覆盖“跳过标志残留时普通 `WaitDraw` 仍应等待”的回归场景。

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `tk-rendering-performance`: 收窄 Tk 等待输入优化的跳过标志作用域，避免普通等待点被性能 mod 跳过。

## Impact

- 修改 `mod/local_performance/scripts/local_performance.py` 的 `patched_askfor_wait()`。
- 修改 `mod/local_performance/tests/test_local_performance_mod.py` 中关于右键跳过的测试期望，并新增普通等待不受残留跳过标志影响的测试。
- 不需要修改身体检查面板代码；身体检查只是全局等待语义回归的显著受害场景。
