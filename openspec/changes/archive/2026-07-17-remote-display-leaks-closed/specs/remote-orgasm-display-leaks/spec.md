## ADDED Requirements

### Requirement: Gate remote orgasm-derived displays on player scene
The system SHALL suppress the player-facing text of a character's瞬时 orgasm-derived H settlement when that character is not in the player's scene, while still applying the underlying numeric and resource settlement. This covers the display points left as a known unresolved defect by the `remote-plural-orgasm-settlement` change (#215): per-part orgasm talk, `extra_orgasm`, `b_orgasm_to_milk`, `u_orgasm_to_pee`, and the milking-machine / urine-collector per-turn outputs.

"Not in the player's scene" uses the same predicate as the existing remote gate at the top of `second_behavior_effect`: the character is remote when both `position` and `behavior.move_src` differ from the player's `position`; a character who moved away from the player this turn (its `move_src` equals the player's position) is still shown.

#### Scenario: Remote character produces per-part orgasm talk
- **WHEN** a character not in the player's scene reaches the orgasm/mark settlement calls of `check_second_effect` and has a non-`998` orgasm-class second behavior (for example `v_orgasm_strong`)
- **THEN** its orgasm talk is not drawn to the player
- **AND** the behavior's configured effects still run and the behavior is still cleared from the pending state

#### Scenario: Remote character triggers a directly-drawn orgasm derivative
- **WHEN** a character not in the player's scene settles `extra_orgasm`, `b_orgasm_to_milk`, `u_orgasm_to_pee`, milking-machine, or urine-collector effects
- **THEN** the corresponding derivative text is not drawn to the player
- **AND** the numeric and resource settlement (pain/terror status, banked milk/urine) is applied unchanged

#### Scenario: Character in the player's scene is unaffected
- **WHEN** the same orgasm-derived settlement occurs for the player or a character in the player's scene
- **THEN** all existing talk and derivative text is drawn as before

#### Scenario: Character that moved away from the player this turn
- **WHEN** a character's `position` differs from the player's but its `behavior.move_src` equals the player's position during this settlement
- **THEN** its orgasm talk is still drawn, matching the pre-existing empty-list remote gate's move_src exception

### Requirement: Preserve must-show and persistent-impact displays remotely
The system SHALL continue to display, for remote characters, the H-settlement events that carry lasting impact or are marked必须显示, so this convergence does not hide meaningful changes.

#### Scenario: Must-show behavior reaches the talk display while remote
- **WHEN** a `998` (must-show) second behavior — such as a mark behavior queued by a manual ability-panel upgrade, which calls `second_behavior_effect` with a non-empty list and bypasses `must_show_talk_check` — is settled for a remote character
- **THEN** its talk is drawn to the player regardless of scene, because the player-scene gate on `handle_second_talk` exempts behaviors in `config_behavior_must_show_cid_list`

#### Scenario: Mark level-up text remains visible remotely
- **WHEN** a remote character's mark ability permanently increases and `mark_effect` builds its level-up summary text
- **THEN** that summary is drawn to the player, because a permanent ability change is a lasting effect the player should be told about

#### Scenario: Plural-orgasm achievement remains visible remotely
- **WHEN** a remote character's multi-part orgasm reaches an achievement milestone (`achievement_flow(_("绝顶"), …)`)
- **THEN** the achievement is recorded and its "获得蚀刻章" notice is drawn as before, because an achievement unlock is one-time persistent progress rather than repeated瞬时 spam
