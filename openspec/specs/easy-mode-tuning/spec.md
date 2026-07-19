# easy-mode-tuning Specification

## Purpose
TBD - created by archiving change sync-local-mods. Update Purpose after archive.
## Requirements
### Requirement: Accelerate hypnosis progress for easy mode
Easy mode SHALL retain the upstream hypnosis ceiling and modifiers while increasing the random progress multiplier.

#### Scenario: Hypnosis progress is calculated for an NPC
- **WHEN** hypnosis progress is calculated for a non-player target below the current player ability ceiling
- **THEN** the random multiplier uses `5..10`
- **AND** player talent, aromatherapy, and target ability modifiers still apply

### Requirement: Increase sanity max growth for easy mode
Easy mode SHALL convert daily sanity cost into max sanity growth at a one-to-one rounded rate.

#### Scenario: Daily sanity cost qualifies for growth
- **WHEN** the player has at least `50` daily sanity cost and max sanity is below `9999`
- **THEN** max sanity increases by `round(today_cost)`
- **AND** max sanity is capped at `9999`
- **AND** daily sanity cost is reset to zero

### Requirement: Lower hotel room prices for easy mode
Easy mode SHALL lower the love hotel room prices while preserving booking side effects.

#### Scenario: Player books a hotel room
- **WHEN** the player books standard, theme, or top suite rooms
- **THEN** the required pink voucher prices are `1`, `2`, and `3`
- **AND** checkout time, room level, and theme-room rewards follow the upstream booking flow

