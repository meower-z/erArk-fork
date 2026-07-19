## MODIFIED Requirements

### Requirement: Wait for fresh input after settlement output
The performance fix SHALL avoid consuming stale click or enter events when arming a normal-mode wait prompt, without broadening skip-wait flags beyond their original explicit call sites.

#### Scenario: Stale input exists before WaitDraw
- **WHEN** pending order queue entries, including empty input or an old non-empty button command, exist before `askfor_wait()` arms
- **THEN** pending orders are drained before the wait arms
- **AND** `w_frame_up` is reset before and after the short arming delay
- **AND** the wait reads fresh input instead of the stale event
- **AND** any late queued input left after the wait, including empty input or an old non-empty button command, is drained before the next wait can observe it

#### Scenario: Normal WaitDraw sees a residual skip flag
- **WHEN** `w_frame_skip_wait_mouse` is already set before an ordinary `WaitDraw` calls `askfor_wait()`
- **THEN** `askfor_wait()` still arms a normal wait
- **AND** it does not return solely because `w_frame_skip_wait_mouse` is true
- **AND** it does not clear `w_frame_skip_wait_mouse`
- **AND** the player must provide a fresh click or accepted wait input before the flow continues

#### Scenario: Normal WaitDraw sees stale mouse-up state
- **WHEN** `w_frame_up` is already set before an ordinary `WaitDraw` calls `askfor_wait()`
- **THEN** `askfor_wait()` resets `w_frame_up` before and after the short arming delay
- **AND** the stale mouse-up state does not satisfy the new wait
- **AND** the wait reads fresh input before the flow continues

#### Scenario: Normal WaitDraw sees right-click residual state
- **WHEN** both `w_frame_skip_wait_mouse` and `w_frame_up` are already set before an ordinary `WaitDraw` calls `askfor_wait()`
- **THEN** `askfor_wait()` does not return solely because `w_frame_skip_wait_mouse` is true
- **AND** it resets `w_frame_up` before and after the short arming delay
- **AND** the residual mouse-up state does not satisfy the new wait
- **AND** the wait reads fresh input before the flow continues

#### Scenario: Consecutive normal waits see a residual skip flag
- **WHEN** `w_frame_skip_wait_mouse` remains set across two consecutive ordinary `WaitDraw` waits
- **THEN** the first `askfor_wait()` arms a normal wait and requires fresh input
- **AND** the second `askfor_wait()` also arms a normal wait and requires fresh input
- **AND** one click or accepted wait input cannot advance both waits

#### Scenario: WaitDraw returns to a command panel
- **WHEN** an ordinary `WaitDraw` wait completes and the flow immediately returns to a panel that calls `askfor_all()`
- **THEN** stale queued input from the previous UI, including an old non-empty button command, is not consumed by that next `askfor_all()`
- **AND** the old button command cannot re-trigger the same action
- **AND** fresh input entered after the next panel is displayed can still be handled normally

#### Scenario: Explicit skip-wait caller handles the skip flag
- **WHEN** a caller such as `LineFeedWaitDraw` or `LeftDrawTextListWaitPanel` checks `w_frame_skip_wait_mouse` before calling `askfor_wait()`
- **THEN** that caller SHALL preserve its existing skip behavior at that explicit call site
- **AND** the skip behavior is controlled at that explicit call site rather than inside global `askfor_wait()`

#### Scenario: Web mode is active
- **WHEN** web mode is active
- **THEN** the patched wait delegates to the original web-compatible wait behavior

#### Scenario: Benchmark mode is active
- **WHEN** benchmark mode is active
- **THEN** the patched wait returns without blocking
- **AND** it does not wait for `flow_handle.askfor_str()`
