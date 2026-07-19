# diary-history Specification

## Purpose
Define bounded diary browsing while preserving complete unexported history, export safety, and compatibility with existing saves.

## Requirements
### Requirement: Bound the default diary view
The diary panel SHALL NOT concatenate and render the entire unexported action history when it opens. It SHALL default to the current game day's most recent bounded page and SHALL require explicit navigation to access older or additional entries.

#### Scenario: Long history opens on the current day
- **WHEN** `daily_intsruce` contains entries and date separators spanning many game days
- **THEN** opening the diary constructs only the current day's bounded page for the initial draw
- **AND** entries from earlier days are not included in that first draw payload
- **AND** the panel provides an explicit way to navigate to earlier history

#### Scenario: Current day exceeds one page
- **WHEN** the current game day alone contains more entries or characters than the configured page bound
- **THEN** the first draw remains within that bound
- **AND** the player can explicitly load or navigate to the remaining entries from the same day

#### Scenario: No recognized legacy date separator exists
- **WHEN** an old save contains diary entries without a recognizable generated date separator
- **THEN** the panel still opens with a bounded suffix page
- **AND** older ungrouped entries remain accessible rather than being discarded

### Requirement: Preserve full unexported history and export behavior
Bounding the interactive view SHALL NOT silently delete or omit unexported diary records. The explicit save/export action SHALL continue to write all unexported action entries and user-inserted text before clearing the exported cache according to the existing behavior.

#### Scenario: User exports while browsing only today's page
- **WHEN** the player is viewing a bounded current-day page and selects “保存并更新日记文件”
- **THEN** the output file contains all unexported `daily_intsruce` entries, including older days not currently visible
- **AND** the output includes the user's inserted diary text
- **AND** the cache is cleared only after the complete export succeeds

#### Scenario: Export fails
- **WHEN** writing the diary file raises an error before completion
- **THEN** unexported in-memory history is not cleared
- **AND** the player can retry without losing records

### Requirement: Build diary pages without quadratic concatenation
The system SHALL construct each displayed diary page in time and memory proportional to that page's content, using collected segments or an equivalent linear composition method rather than repeated concatenation across the full history.

#### Scenario: Large persisted history is opened
- **WHEN** a save contains tens of thousands of unexported action fragments
- **THEN** the amount of text passed to the initial draw is limited to the configured page bound
- **AND** page construction does not repeatedly copy the entire accumulated history
- **AND** both Tk and Web diary entry paths remain responsive enough to return navigation controls

### Requirement: Keep existing diary saves compatible
The bounded diary implementation SHALL read existing `daily_intsruce: List[str]` save data without requiring destructive migration.

#### Scenario: Old save is loaded
- **WHEN** a save created before bounded diary browsing contains a flat `daily_intsruce` list with multiple generated date separators
- **THEN** the diary groups or indexes those entries for bounded browsing at runtime
- **AND** loading and saving the game preserves every original entry until explicit diary export
