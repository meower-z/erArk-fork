# hidden-sex-discovery Specification

## Purpose
Define hidden-sex discoverer eligibility at one player location and the existing movement reset boundary.

## Requirements

### Requirement: Do not reselect an already handled hidden-sex discoverer
The hidden-sex discovery path SHALL treat `sp_flag.see_pl_h` as a witness-handled marker for the player's current location. After a character discovers the player, that character SHALL NOT be selected again while the player remains at that location; the existing player-movement reset SHALL restore later discovery eligibility.

#### Scenario: Discovery is evaluated again before player movement
- **WHEN** a character has already opened the H discovery panel and therefore has `sp_flag.see_pl_h == True`
- **AND** hidden-sex discovery settlement is evaluated again before the player moves, regardless of which action triggers the later evaluation
- **THEN** that character SHALL be excluded from the hidden-sex discoverer candidate list
- **AND** the same character's discovery panel SHALL NOT reopen

#### Scenario: Another character has not discovered the player at this location
- **WHEN** another otherwise eligible character in the scene still has `sp_flag.see_pl_h == False`
- **THEN** the hidden-sex discovery path SHALL preserve that character's eligibility
- **AND** the ordering of the remaining eligible candidates SHALL remain unchanged

#### Scenario: Player movement resets witness eligibility
- **WHEN** the player moves and the existing movement flow resets a character's `sp_flag.see_pl_h` marker
- **THEN** that character MAY become a hidden-sex discoverer again under the ordinary eligibility rules
