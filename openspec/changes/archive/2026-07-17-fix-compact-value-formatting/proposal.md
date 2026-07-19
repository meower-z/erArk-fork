## Why

The shared compact-number formatter derives suffix groups from the signed text length and an off-by-one index. Negative values and thousand/million boundaries can therefore display the wrong unit or collapse to text such as `-M`, which makes otherwise valid settlement values look corrupted.

## What Changes

- Compute the compact group from absolute magnitude while preserving the original sign.
- Map every existing compact suffix, including `K`, `M`, and `G`, to the correct magnitude boundary.
- Verify every production caller and preserve the target-side exact-number path, so the display-only correction does not change values or widen into a UI policy change.
- Keep time-stop release attribution outside this change.

## Capabilities

### New Capabilities

- `compact-value-formatting`: Defines correct signed compact-unit presentation for the shared value formatter and its production callers.

### Modified Capabilities

None.

## Impact

This change affects the shared value-text formatter used by the acting character's state and experience display, plus compatible local batch output. Target-character settlement fields deliberately keep their existing exact-number formatter. Stored values, effect formulas, and settlement ownership remain unchanged.
