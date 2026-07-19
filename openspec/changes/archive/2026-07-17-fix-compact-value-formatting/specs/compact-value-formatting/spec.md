## ADDED Requirements

### Requirement: Format compact values by absolute magnitude
The shared value formatter SHALL select compact suffixes from a value's absolute numeric magnitude and SHALL apply the sign independently.

#### Scenario: Values below one thousand
- **WHEN** an integer value has absolute magnitude below 1000
- **THEN** the formatter returns the signed integer without a compact suffix
- **AND** `-500` is not reduced to a bare suffix such as `-M`

#### Scenario: Thousand range
- **WHEN** a value has absolute magnitude from 1000 through 999999
- **THEN** the formatter uses the `K` suffix
- **AND** `1000`, `-1000`, `999999`, and `-999999` preserve their signs and correct group

#### Scenario: Million range
- **WHEN** a value has absolute magnitude from 1000000 through 999999999
- **THEN** the formatter uses the `M` suffix
- **AND** positive and negative values of equal magnitude use the same compact digits with only the sign differing

#### Scenario: Billion range
- **WHEN** a value has absolute magnitude from 1000000000 through 999999999999
- **THEN** the formatter uses the existing `G` suffix
- **AND** positive and negative values of equal magnitude use the same compact digits with only the sign differing

#### Scenario: Existing larger compact suffixes
- **WHEN** a value reaches a larger magnitude represented by the formatter's existing suffix list
- **THEN** the formatter selects that suffix by the same absolute-magnitude rule
- **AND** this change does not introduce a new suffix, rounding policy, or stored-value conversion

#### Scenario: Fractional input
- **WHEN** the formatter receives a non-integer numeric value
- **THEN** it truncates the value to an integer before selecting the suffix
- **AND** `999.9` is displayed as `+999`

### Requirement: Preserve value meaning at every shared caller
The formatter correction SHALL change display text only and SHALL NOT change the stored or settled value supplied by any production caller.

#### Scenario: Compact core and local callers use the formatter
- **WHEN** acting-character state display, acting-character experience display, or local batch output formats the same signed value
- **THEN** each caller uses the same corrected sign and compact group
- **AND** no caller requires time-stop-specific state to produce the result

#### Scenario: Target settlement keeps exact values
- **WHEN** an interaction target's state, experience, HP, MP, favorability, trust, or hypnosis change is displayed
- **THEN** the existing exact-number formatter remains in use
- **AND** this change does not compact or otherwise alter that target-side text

#### Scenario: Settlement value is formatted
- **WHEN** a settlement caller passes a value to the formatter
- **THEN** the underlying state and change record remain unchanged
- **AND** only the rendered text reflects the corrected compact unit
