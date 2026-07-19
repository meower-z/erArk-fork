## Context

`extra_feel_settle` derives additional psychological pleasure when a settlement adds state 10, 14, 16, or 17 and the corresponding ability reaches level 5. Its current base formula is `max(10, final_value / 20)`, after which the ordinary state-23 settlement applies psychological sensitivity, the matching ability, and other pleasure modifiers. Large source deltas can therefore produce psychological pleasure that is visibly separated from every other pleasure channel in the same action.

This is a balance concern at the derived-value owner, not a routing defect. Signed pain routing determines whether a pain delta remains state 17 or becomes state 23; it must not absorb this later tuning work.

## Goals / Non-Goals

**Goals:**

- Establish reproducible low, medium, and high baseline ranges for all four `extra_feel_settle` sources.
- Select a monotonic curve that preserves useful low-end feedback but reduces the marginal gain from extreme source deltas.
- Keep the curve local to the derived psychological-pleasure base value so existing ability gates, state-23 modifiers, experience, caps, and change records retain their current ownership.
- Define a quantitative acceptance band before changing production code.

**Non-Goals:**

- Changing signed pain routing or the meaning of `pain_as_pleasure`.
- Rebalancing every pleasure source in the game.
- Changing ability thresholds, psychological experience, save data, or CSV identifiers.
- Choosing curve constants from a single screenshot or one unusually large settlement.

## Decisions

### Tune the derived-value owner

The curve belongs at the current `final_value` transformation inside `extra_feel_settle`. Applying a cap after the state-23 settlement would mix this source with psychological sensitivity and unrelated buffs; changing the shared state-23 formula would affect every psychological-pleasure source.

### Measure before choosing a curve

Record source delta, current derived base value, final psychological pleasure, relevant ability levels, and the other pleasure channels in the same settlement. Use representative low, medium, and high inputs for states 10, 14, 16, and 17. Curve candidates may include square-root, logarithmic, rational, or piecewise diminishing-return forms, but no family or constants are accepted until the comparison table exposes the useful low-end range and the extreme tail.

### Preserve existing downstream ownership

The selected curve will return only the base derived amount. Existing state-23 settlement remains responsible for psychological modifiers, storage, caps, change records, and psychological experience. This keeps the balance adjustment independently reviewable and prevents another duplicate settlement path.

### Gate implementation on an explicit target

Before production edits, record the chosen breakpoint, low-end continuity expectation, high-end compression target, and acceptable relationship to the largest non-psychological pleasure channel in the representative cases. Those numbers require a separate user balance decision; this planning record does not silently choose them.

## Risks / Trade-offs

- **[Over-compression]** A steep curve could make high-level abilities feel unrewarding -> compare the whole input range and require monotonic output.
- **[Low-end discontinuity]** The current minimum of 10 may dominate small inputs -> evaluate the minimum separately instead of preserving or removing it by assumption.
- **[Negative-input ambiguity]** The current `max(10, final_value / 20)` can produce positive derived pleasure for zero or negative source deltas -> preserve current behavior until that semantic question is explicitly decided.
- **[Misdiagnosed source]** Large final values may also come from downstream psychological modifiers -> record both the pre-modifier derived amount and final posted amount.

## Open Questions

1. Which curve family and breakpoint best preserve ordinary rewards while compressing extreme settlements?
2. What numerical ratio to the other pleasure channels counts as an acceptable upper range?
3. Should zero or negative source deltas continue to receive the current minimum derived value, or should that be a separate correctness change?
