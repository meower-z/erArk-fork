## Why

`extra_feel_settle` currently derives psychological pleasure from submission, sadism, exposure, and masochism using a mostly linear value before applying psychological-pleasure multipliers. In real settlement output this derived value can grow far beyond every other pleasure channel, creating a visible balance discontinuity rather than a gradual reward curve.

## What Changes

- Measure representative low, medium, and high triggering-state deltas and compare the resulting psychological pleasure with the other pleasure channels in the same settlement.
- Replace the current unbounded linear derived-value step with a monotonic curve that preserves meaningful low-end gains while compressing extreme values.
- Keep the existing state-to-ability gates, psychological-pleasure settlement path, psychological experience award, cap accounting, and change-record ownership unless measurement reveals a separate defect.
- Keep this balance work separate from signed pain routing: the routing fix decides the destination of a pain delta, while this change only tunes the additional psychological pleasure produced by `extra_feel_settle`.

## Capabilities

### New Capabilities

- `psychological-pleasure-balancing`: Defines a measured, curved balance contract for psychological pleasure derived from submission, sadism, exposure, and masochism.

### Modified Capabilities

- None.

## Impact

- Primary balance owner: `Script/Settle/common_default.py::extra_feel_settle`.
- Requires focused numerical tests and representative real-settlement comparisons before selecting curve parameters.
- Does not change the current signed pain-routing PR and introduces no save-format, CSV-ID, or public-interface change.
