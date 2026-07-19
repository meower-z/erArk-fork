## 1. Wait Semantics

- [x] 1.1 Remove the `w_frame_skip_wait_mouse` early-return branch from `mod/local_performance/scripts/local_performance.py::patched_askfor_wait()`.
- [x] 1.2 Do not clear or otherwise mutate `w_frame_skip_wait_mouse` inside global `patched_askfor_wait()`; existing producer/reset paths own that flag lifecycle.
- [x] 1.3 Keep the Web mode fallback to the original `askfor_wait()`.
- [x] 1.4 Keep benchmark mode as a direct return.
- [x] 1.5 Keep stale queued input draining before arming the wait.
- [x] 1.6 Keep `w_frame_up` reset before and after the arming delay.
- [x] 1.7 Keep the fresh-input wait path through `flow_handle.askfor_str(donot_return_null_str=False)`.
- [x] 1.8 Keep the post-wait `_drain_pending_orders()` cleanup so late empty input from double-clicks or delayed Tk events cannot satisfy the next normal wait.

## 2. Regression Tests

- [x] 2.1 Update the existing right-click skip test so `w_frame_skip_wait_mouse = 1` does not bypass ordinary `patched_askfor_wait()`.
- [x] 2.2 Keep or extend the stale-click test to prove queued old empty input is drained before the wait arms.
- [x] 2.3 Add an assertion that `patched_askfor_wait()` calls `flow_handle.askfor_str(donot_return_null_str=False)` even when `w_frame_skip_wait_mouse` is already 1; do not require positional-argument spelling.
- [x] 2.4 Add a combined regression case where `w_frame_skip_wait_mouse = 1` and stale empty input is already queued; verify the stale input is drained and the function still arms a fresh wait instead of returning after `sleep(0.001)`.
- [x] 2.5 Add a stale non-empty command case where an old button command is already queued; verify `_drain_pending_orders()` clears it and the function still arms a fresh wait through `flow_handle.askfor_str(donot_return_null_str=False)`.
- [x] 2.6 Add a stale mouse-state case where `w_frame_up = 1` before entering `patched_askfor_wait()`; verify the state is reset and the function still arms a fresh wait through `flow_handle.askfor_str(donot_return_null_str=False)`.
- [x] 2.7 Add coverage proving `patched_askfor_wait()` does not clear `w_frame_skip_wait_mouse`.
- [x] 2.8 Add a real right-click residual case where both `w_frame_skip_wait_mouse = 1` and `w_frame_up = 1` exist before entering `patched_askfor_wait()`; verify `w_frame_up` is reset and the function still arms a fresh wait through `flow_handle.askfor_str(donot_return_null_str=False)`.
- [x] 2.9 Add Web mode coverage proving the patched wait delegates to `call_original(FLOW_HANDLE, "askfor_wait")`.
- [x] 2.10 Add benchmark mode coverage proving the patched wait returns without calling `flow_handle.askfor_str()`.
- [x] 2.11 Add post-wait cleanup cases where `askfor_str()` leaves late queued input behind; verify final `_drain_pending_orders()` removes both empty input and a non-empty old button command before the next wait can observe them.
- [x] 2.12 Add a panel-loop regression case where a normal `WaitDraw` returns and the next panel immediately calls `askfor_all()`; verify a stale non-empty old button command is not consumed by that next `askfor_all()` and cannot re-trigger the same body-check action.
- [x] 2.13 Add a consecutive-waits regression case where `w_frame_skip_wait_mouse = 1` remains set across two ordinary `patched_askfor_wait()` calls; verify both calls enter fresh `flow_handle.askfor_str(donot_return_null_str=False)` instead of the first click causing the second wait to auto-skip.
- [x] 2.14 Rename or rewrite the existing `test_wait_respects_active_right_click_skip()` because it currently asserts the old broken behavior; the new test name and expectation must reflect the new rule: residual skip flag does not bypass normal wait and still enters `flow_handle.askfor_str(donot_return_null_str=False)`.
- [x] 2.15 Keep the deferred scroll test unchanged.
- [x] 2.16 Register every new or rewritten test helper in `mod/local_performance/tests/test_local_performance_mod.py::main()`, because this file is executed as a plain script rather than by pytest discovery.

## 3. Verification

- [x] 3.1 Run `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`.
- [x] 3.2 Run `python -m py_compile mod/local_performance/scripts/local_performance.py mod/local_performance/tests/test_local_performance_mod.py`.
- [x] 3.3 Run `openspec validate fix-tk-wait-skip-scope --strict`.
- [ ] 3.4 In Tk mode, while already inside the body-check/body-management panel, create a residual skip flag by right-clicking or by debug-setting `cache.wframe_mouse.w_frame_skip_wait_mouse = 1`; avoid any main-scene redraw path that clears the flag, then verify a body-check action stops on the intermediate settlement output until the player clicks once.
- [ ] 3.5 In Tk mode, verify explicit skip-wait callers are not regressed: `LineFeedWaitDraw.draw()` and `LeftDrawTextListWaitPanel.draw()` should still skip only because they check `w_frame_skip_wait_mouse` before calling `askfor_wait()`.
- [ ] 3.6 If checking producer behavior from `WAIT_1_HOUR` / `WAIT_6_HOUR`, map movement, or navigation, treat these as skip flag producers; if the real route passes through main-scene redraw and clears the flag, use debug state setup to mimic the producer's post-state before entering a normal `WaitDraw` path.
- [ ] 3.7 In Tk mode, verify another ordinary `WaitDraw` path such as body-management settlement or physical-exam setting details also advances by one wait per click when a residual skip flag exists.
