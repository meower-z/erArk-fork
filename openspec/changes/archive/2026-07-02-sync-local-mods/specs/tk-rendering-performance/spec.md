## ADDED Requirements

### Requirement: Coalesce Tk scroll-to-end calls during queue rendering
The performance fix SHALL preserve upstream queue rendering while reducing repeated scroll-to-end work.

#### Scenario: Queue rendering requests multiple end-scrolls
- **WHEN** upstream queue rendering calls `see_end()` multiple times during one queue drain
- **THEN** the patched renderer performs one final `see_end()` after the drain
- **AND** it calls `update_idletasks()` when available

### Requirement: Wait for fresh input after settlement output
The performance fix SHALL avoid consuming stale click or enter events when arming a normal-mode wait prompt.

#### Scenario: Stale input exists before WaitDraw
- **WHEN** pending order queue entries or old mouse-up state exist before `askfor_wait()` arms
- **THEN** pending orders are drained
- **AND** `w_frame_up` is reset before and after the short arming delay
- **AND** the wait reads fresh input instead of the stale event

#### Scenario: Alternate modes are active
- **WHEN** web mode, benchmark mode, or right-click skip behavior is active
- **THEN** the patched wait preserves the existing special-case behavior
