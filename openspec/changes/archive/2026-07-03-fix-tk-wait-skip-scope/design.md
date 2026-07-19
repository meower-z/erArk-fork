## Context

身体检查流程的中间停顿来自 `Physical_Check_And_Manage_Panel.settle_target_physical_status()` 末尾的 `draw.WaitDraw()`。`WaitDraw.draw()` 输出文本后调用 `flow_handle.askfor_wait()`。结算函数返回后，身体检查面板外层循环会重新绘制检查项目按钮，所以只要这个等待被跳过，玩家就会看到点一次按钮后直接回到按钮界面。

`local_performance` 当前替换了 `Script.Core.flow_handle.askfor_wait()`，目标是避免按钮点击或回车事件在结算输出抵达尾部 `WaitDraw` 时仍留在队列里，导致等待点被旧事件消耗。这个目标本身成立，但实现中新增了对 `w_frame_skip_wait_mouse` 的全局提前返回。该标志会被右键、地图移动、长时间等待等路径置为 1，并且主要在回到主场景面板时清零；身体检查面板内部不会清零。

原版全局 `askfor_wait()` 的语义是：进入等待时重置 `w_frame_up`，然后等待下一次玩家点击或空输入。原版并不会因为 `w_frame_skip_wait_mouse` 残留而跳过普通等待。跳过标志只在调用点显式判断时才生效，例如 `LineFeedWaitDraw.draw()` 和 `LeftDrawTextListWaitPanel.draw()`。

## Goals / Non-Goals

**Goals:**
- 普通 `WaitDraw` 和所有直接调用 `flow_handle.askfor_wait()` 的等待点恢复原版等待语义。
- 保留 `local_performance` 的 stale click / stale enter 防护，不回滚为原版瞬时 armed wait。
- 保留 Web 模式与 benchmark 模式的现有分支。
- 保留显式调用点的右键/跳过等待语义。
- 用测试锁定身体检查同类症状的根因：`w_frame_skip_wait_mouse == 1` 时普通等待仍会 armed wait。

**Non-Goals:**
- 不改身体检查与管理面板的控制流。
- 不重新设计鼠标状态结构或 Tk 事件绑定。
- 不改变地图移动、等待 1 小时/6 小时等主动设置 `w_frame_skip_wait_mouse` 的行为。
- 不处理 Web 绘制模式的等待实现。

## Decisions

### 1. 不把 `w_frame_skip_wait_mouse` 作为全局 `askfor_wait()` 的跳过条件

从 `patched_askfor_wait()` 移除：

```python
if getattr(wframe_mouse, "w_frame_skip_wait_mouse", False):
    time.sleep(0.001)
    return
```

这样普通 `WaitDraw` 不会被残留跳过标志影响。显式跳过仍由调用点负责：如果调用点本来就是“按右键继续输出文本”的路径，它可以在调用 `askfor_wait()` 之前检查标志并选择 `time.sleep(0.001)`。

全局 `patched_askfor_wait()` 也不应在这个过程中清零 `w_frame_skip_wait_mouse`。该标志的生命周期仍归现有 producer/reset 点管理，例如右键、地图移动、长时间等待设置它，主场景绘制路径清零它。本变更只是不再让全局普通等待读取它并早退。

### 2. 保留 stale input 防护

`patched_askfor_wait()` 仍应执行：

1. 清理等待建立前已经排队的旧命令。
2. 将 `w_frame_up` 置 0。
3. 短暂等待 Tk 点击事件传播完成。
4. 再次将 `w_frame_up` 置 0，并清理这段窗口期内出现的旧命令。
5. 调用原模块中的 `askfor_str(donot_return_null_str=False)` 等待新的输入。
6. 等待结束后清理本次等待使用后残留的空输入。

这保留性能 mod 的核心目的：按钮点击触发动作时产生的旧鼠标/输入事件不会自动吃掉随后的结算等待。

等待结束后的清队列只用于丢弃旧 UI / 旧点击带来的迟到残留输入，尤其是双击或 Tk 事件延迟造成的空输入、旧按钮命令。它不应被实现为清理下一屏已经绘制并开始等待后的真实新输入；下一屏合法输入仍应由下一次 `askfor_all()` 或 `askfor_str()` 正常读取。

### 3. 测试从“右键标志会跳过全局等待”改为“右键标志不会跳过普通等待”

现有 `test_wait_respects_active_right_click_skip()` 体现的是当前错误行为，应改写为普通等待场景：

- Arrange: `w_frame_skip_wait_mouse = 1`，队列里没有有效新输入。
- Act: 调用 `patched_askfor_wait()`。
- Assert: 它仍会进入 `flow_handle.askfor_str(donot_return_null_str=False)`，并在测试模拟的新输入后返回。

同时保留 stale click 测试，确保修复不会回退到消费旧点击事件。还需要覆盖真实回归形态：`w_frame_skip_wait_mouse = 1` 与旧空输入同时存在时，旧空输入被清理，普通等待仍 armed wait，而不是 `sleep(0.001)` 后直接返回。

还需要覆盖旧鼠标状态：进入 `patched_askfor_wait()` 前如果 `w_frame_up == 1`，补丁必须在 arming 前后清零该状态，并进入 fresh `askfor_str(donot_return_null_str=False)`，不能让旧鼠标状态吃掉当前等待。

Web 与 benchmark 分支也应有轻量测试：Web 模式委托 `call_original(FLOW_HANDLE, "askfor_wait")`，benchmark 模式直接返回且不调用 `flow_handle.askfor_str()`。

### 4. 不在身体检查面板局部清零跳过标志

局部清零只能修复身体检查一个入口，还会遗漏告白、怀孕、宿舍、外勤、身体管理、设置说明等所有普通 `WaitDraw`。根因在全局等待函数的语义被扩大，修复应落在 `local_performance` 的 replacement 上。

## Risks / Trade-offs

- [Risk] 用户按右键后普通 `WaitDraw` 会恢复原版等待，不再由性能 mod 直接跳过。Mitigation: 这是原版语义；真正需要连续跳过的调用点已经在调用前显式检查 `w_frame_skip_wait_mouse`。
- [Risk] stale input 防护中的时间窗口过短或过长仍可能影响手感。Mitigation: 本变更不调整 `WAIT_INPUT_ARMING_DELAY_SECONDS`，只收窄跳过标志作用域。
- [Risk] `_drain_pending_orders()` 在等待后清理队列可能掩盖其他输入路径问题。Mitigation: 保持既有行为不扩大范围；本次测试只锁定跳过标志回归。

## Verification Plan

- 运行 `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`。
- 运行 `python -m py_compile mod/local_performance/scripts/local_performance.py mod/local_performance/tests/test_local_performance_mod.py`。
- 手动验证普通 Tk 模式：在身体检查/身体管理面板内右键制造 residual skip flag，或用 debug 方式直接设置 `cache.wframe_mouse.w_frame_skip_wait_mouse = 1`，且不要经过会清零的主场景绘制路径；随后选择检查项目，中间结算输出应等待一次点击，再回到检查项目按钮界面。
- 手动验证另一个普通 `WaitDraw` 场景，例如身体管理结算或体检设置说明；同样在 residual skip flag 存在时，一次点击只应通过一个等待点。
- 手动验证 producer 状态：用 `WAIT_1_HOUR` / `WAIT_6_HOUR`、地图移动、导航，或 debug 直接模拟这些 producer 设置的 residual skip flag，再进入一个普通 `WaitDraw` 场景；如果实际路径会经过主场景清零，则以 debug 设置方式模拟 producer 后状态。
- 手动验证显式 skip 调用点仍按原有路径生效：`LineFeedWaitDraw.draw()` 与 `LeftDrawTextListWaitPanel.draw()` 在调用前检查 `w_frame_skip_wait_mouse` 时仍可跳过等待。
- 如验证长时间等待相关行为，应把 `WAIT_1_HOUR` / `WAIT_6_HOUR` 只视为 skip flag producer，再观察后续显式 skip 调用点，而不是把它们当作直接 skip caller。
