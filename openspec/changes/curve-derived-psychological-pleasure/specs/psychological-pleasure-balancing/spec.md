## ADDED Requirements

### Requirement: Derived psychological pleasure uses measured diminishing returns
For positive triggering-state deltas, the system SHALL calculate the base psychological pleasure produced by `extra_feel_settle` with a monotonic diminishing-return curve rather than an unbounded fixed proportion across the full input range. The curve parameters MUST be selected from recorded low, medium, and high settlement measurements, not from a single outlier.

#### Scenario: Increasing ordinary input remains rewarding
- **WHEN** two positive triggering-state deltas are within the documented ordinary range and the second is larger than the first
- **THEN** the curved base psychological pleasure for the second delta is not lower than the first

#### Scenario: Extreme input is compressed
- **WHEN** positive triggering-state deltas exceed the documented curve breakpoint
- **THEN** the marginal increase in base psychological pleasure decreases relative to the source-state increase

### Requirement: Balance acceptance is quantitative
The project SHALL define and record a numerical acceptance band before enabling the curve in production. The evidence MUST compare the derived base amount and final posted psychological pleasure with the other pleasure channels from representative settlements for states 10, 14, 16, and 17.

#### Scenario: Curve candidate is evaluated
- **WHEN** a curve family and parameters are proposed
- **THEN** the review evidence includes current and candidate results for low, medium, and high inputs across all four triggering states

#### Scenario: Acceptance target is unresolved
- **WHEN** the breakpoint, compression target, or acceptable relationship to other pleasure channels has not been approved
- **THEN** production balance code remains unchanged

### Requirement: Existing settlement responsibilities remain intact
The balance curve SHALL change only the base derived amount owned by `extra_feel_settle`. Existing ability gates, state-to-ability mapping, state-23 modifiers, psychological experience award, storage cap, and change-record ownership MUST remain unchanged unless a separately specified defect requires otherwise.

#### Scenario: Curved amount is settled
- **WHEN** a qualifying state 10, 14, 16, or 17 delta produces derived psychological pleasure
- **THEN** the curved base amount continues through the existing psychological-pleasure settlement and accounting path

#### Scenario: Signed pain routing is reviewed
- **WHEN** pain is retained as state 17 or converted to state 23 by `pain_as_pleasure`
- **THEN** that routing decision is unchanged by the derived psychological-pleasure curve

### Requirement: Ambiguous non-positive behavior is not changed implicitly
Until separately decided, the system SHALL preserve the current `extra_feel_settle` behavior for zero and negative triggering-state deltas. A future change to that behavior MUST state its gameplay rule and provide independent verification.

#### Scenario: Balance curve is implemented without a non-positive decision
- **WHEN** the new curve is applied to positive triggering-state deltas
- **THEN** zero and negative triggering-state behavior remains equivalent to the pre-change implementation
