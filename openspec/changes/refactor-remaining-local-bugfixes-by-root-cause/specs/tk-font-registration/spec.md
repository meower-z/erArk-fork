## MODIFIED Requirements

### Requirement: Register bundled fonts privately before Tk resolves configured families
The Tk desktop bootstrap SHALL make the explicitly configured bundled Sarasa family available to the current Windows process without installing it system-wide, and SHALL verify the platform-resolved family rather than treating creation of a Tk named font as proof of file loading.

#### Scenario: Development Tk bootstrap uses the bundled Sarasa asset
- **WHEN** Tk mode starts from a source checkout on Windows
- **THEN** the bootstrap SHALL resolve `static/fonts/等距更纱黑体.ttf` relative to the source tree rather than the current working directory
- **AND** it SHALL register that canonical path with `AddFontResourceExW` and `FR_PRIVATE` before creating the Tk root or any Tk font

#### Scenario: Packaged Tk bootstrap uses the external static tree
- **WHEN** the one-file Windows executable starts beside the release `static` directory
- **THEN** the bootstrap SHALL resolve the Sarasa asset relative to `sys.executable`
- **AND** Full and Lite package verification SHALL prove that the same asset is present and resolvable

#### Scenario: Tk verifies the actual configured family
- **WHEN** the Tk root exists after private registration
- **THEN** a font requesting the configured Sarasa family SHALL resolve through `Font.actual("family")` to an accepted bundled family name
- **AND** a created Tk named-font object, requested family, or lack of an exception SHALL NOT by itself count as successful font loading

#### Scenario: Registration cannot provide the family
- **WHEN** the Sarasa asset is missing, corrupt, or rejected by the platform
- **THEN** Tk startup SHALL continue with an explicit fallback diagnostic and without recording a successful registration
- **AND** it SHALL NOT claim that the bundled family loaded

#### Scenario: Registration follows Tk renderer lifetime
- **WHEN** Web mode starts
- **THEN** it SHALL perform no Windows private-font registration
- **AND** when Tk mode starts, duplicate paths or repeated registration calls SHALL NOT add the same font more than once in the process
- **AND** a successful private registration SHALL remain live until the Tk UI lifetime ends

#### Scenario: Additional bundled font files are considered
- **WHEN** another `.ttf`, `.otf`, or `.ttc` file exists beside the configured Sarasa asset
- **THEN** it SHALL NOT be registered merely because of its extension
- **AND** adding it to the Tk bootstrap SHALL require a proven renderer consumer and its own resolved-family evidence
