# tk-font-registration Specification

## Purpose
TBD - created by archiving change sync-local-mods. Update Purpose after archive.
## Requirements
### Requirement: Register bundled fonts privately before Tk resolves configured families
The font fix SHALL register bundled font files into the current Windows process without installing them system-wide.

#### Scenario: Bundled fonts exist under runtime roots
- **WHEN** `.ttf`, `.otf`, or `.ttc` files exist under `static/fonts` or `fonts`
- **THEN** the font fix registers each unique file with `AddFontResourceExW` and `FR_PRIVATE`
- **AND** duplicate paths are ignored

#### Scenario: Sarasa font is not installed globally
- **WHEN** the desktop Tk UI requests the configured Sarasa family
- **THEN** Tk can resolve the bundled Sarasa family after private registration
- **AND** the UI does not fall back solely because the font is missing from the global system font table

