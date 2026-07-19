## ADDED Requirements

### Requirement: Load structured room addresses across operating systems
The save loader SHALL convert foreign operating-system separators to the current platform separator in known structured game room-address fields before version migration and map reconciliation consume the loaded cache.

#### Scenario: Foreign-separator scene and map data is loaded
- **WHEN** a save contains scene or map dictionary keys and stored `scene_path` or `map_path` values using the other supported operating-system separator
- **THEN** the loader SHALL convert those addresses to the current platform format before map reconciliation
- **AND** the saved scene objects and their character registrations SHALL remain associated with the corresponding current map locations

#### Scenario: Foreign-separator character location fields are loaded
- **WHEN** a save contains foreign-separator values in a character's `dormitory`, `pre_dormitory`, dormitory-administrator target room, or air-hypnosis position
- **THEN** the loader SHALL convert each present field to the current platform format

#### Scenario: Foreign-separator facility locations are loaded
- **WHEN** facility-damage dictionary keys or maintenance-place values contain foreign-separator room addresses
- **THEN** the loader SHALL convert those structured locations to the current platform format

### Requirement: Keep path normalization narrowly scoped
The save loader SHALL normalize only the enumerated structural room-address fields and SHALL preserve unrelated save content.

#### Scenario: Save already uses the current platform separator
- **WHEN** a structured address already uses the current platform separator
- **THEN** its value SHALL remain unchanged
- **AND** a path-keyed dictionary requiring no conversion SHALL retain its existing object and entries

#### Scenario: Ordinary text contains slash characters
- **WHEN** dialogue, descriptions, names, or other non-address strings contain `/` or `\`
- **THEN** the loader SHALL NOT rewrite those strings merely because they contain a separator character

#### Scenario: Optional legacy field is absent
- **WHEN** a loaded save version does not contain one of the enumerated structured fields
- **THEN** normalization SHALL continue without inventing the field or preventing the save from loading
