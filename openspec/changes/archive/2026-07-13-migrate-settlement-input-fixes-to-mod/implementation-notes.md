## Backup and branch boundary

- Source branch before backup: `codex/local-bugfix-audit-fixes` at `20e7e01ac`.
- Temporary backup branch: `codex/temp-settlement-input-boundaries-backup-20260711`.
- Snapshot commit: `4ee74f87f backup: preserve settlement input boundary worktree`.
- The backup excludes the two protected PO files and the unrelated `prepare-upstream-mod-pr` skill.
- The active branch was switched back after the snapshot; tracked upstream source and browser files are currently unchanged from HEAD.

## Prototype-to-mod migration map

| Prototype file | Disposition on active branch | Mod owner / rationale |
| --- | --- | --- |
| `Script/Core/io_web.py` | Reverted | `local_settlement_input_fix` wraps `append_current_draw_element` only for explicit `wait`; the empty `line_wait` exemption was omitted because upstream Tk does not wait on empty split lines. |
| `Script/Design/talk.py` | Reverted | Settlement mod wraps `handle_talk_draw` by queue delta; movement-context mod separately replaces `code_text_to_draw_text` for NPC `{move}`. |
| `Script/System/Instruct_System/handle_instruct.py` | Reverted | Settlement mod wraps one-hour and six-hour waits with `finally` ownership. |
| `Script/System/Web_Draw_System/dialog_box.py` | Reverted | Queue-drain helper lives inside the settlement mod instead of registering a new upstream symbol. |
| `Script/System/Web_Draw_System/web_draw_adapter.py` | Reverted | Settlement mod replaces the small `WebDrawAdapter.adapt_wait_draw` method at load time. |
| `Script/UI/Moudle/draw.py` | Reverted | Settlement mod wraps `WaitDraw.draw` and `LineFeedWaitDraw.draw`. |
| `Script/UI/Moudle/panel.py` | Reverted | Settlement mod wraps `LeftDrawTextListWaitPanel.draw`. |
| `Script/UI/Panel/draw_event_text_panel.py` | Reverted | Settlement mod wraps `DrawEventTextPanel.draw` and waits only when dialog state actually changed. |
| `Script/UI/Panel/navigation_panel.py` | Reverted | Settlement mod wraps `Base_function_class.move_to_scene`. |
| `Script/UI/Panel/see_map_panel.py` | Reverted | Settlement mod wraps all five real map movement callbacks. |
| `static/game.js` | Reverted and intentionally not migrated | The mod removes the exact completed `wait` element before republishing, so old browser code never sees `await_input:false`. The mod loader has no browser-asset patch mechanism. |
| `mod/tests/bdd/web_game_driver.py` | Reverted and intentionally not migrated | The user prohibited scripted BDD interaction. Loader/unit checks remain automated; behavioral BDD evidence comes from direct Tk GUI use by a subagent. |
| `tests/test_wait_skip_ownership.py` | Preserved only on backup branch | Replaced by component-owned tests under `mod/local_settlement_input_fix/tests/`. |

## Component boundaries

### `local_settlement_input_fix`

Owns Web explicit wait publication, direct main/minor dialog pacing, and skip ownership. It depends on `local_performance`, installs after that mod, and wraps upstream callables rather than copying map/event/talk functions.

### `local_npc_move_talk_context_fix`

Owns only the independently discovered NPC `{move}` formatting error. It expands the common movement template with the original NPC id and delegates the expanded literal back to upstream formatting. Player movement and all other paper-doll placeholders remain upstream-owned.

## Automated verification

Completed:

- `python -m py_compile` for both component scripts and both component test files: passed.
- `python -m pytest mod/local_settlement_input_fix/tests mod/local_npc_move_talk_context_fix/tests -q --tb=short`: `10 passed`.
- Real enabled-mod loader smoke (`test_mods_loaded_without_errors` only; not used as BDD evidence): `1 passed`.
- A second non-BDD loader probe initialized the real config and mod manager, confirmed both mods loaded, confirmed the NPC formatter module marker, confirmed Web/io wrappers, and confirmed both long-wait registry entries point to their scoped wrappers.
- Maintained component pytest set excluding the two plain-script suites: `164 passed`.
- `python mod/local_performance/tests/test_local_performance_mod.py --mod-root mod/local_performance`: passed.
- `python mod/local_fontfix/tests/test_local_fontfix_mod.py --mod-root mod/local_fontfix`: passed.

One aggregate pytest attempt included `local_fontfix` and `local_performance` as pytest suites. It produced `163 passed, 22 errors` because those legacy files require their plain-script `--mod-root` entrypoint and expose no pytest fixture. Both were rerun through their documented entrypoints and passed; the errors were invocation errors, not behavioral failures.

The protected PO SHA256 values were checked before and after the real loader probe and remained exactly `bfc77d23...d81cde43` and `e59bdeb4...75879b`.

## GUI evidence

A subagent ran the real Tk application under Xvfb and interacted only through visible coordinate clicks. No WebGameDriver, game API, or scripted BDD driver was used. The exact path was: title `神经重载` -> save 5 -> load confirmation -> movement -> upper map -> medical department entrance to life/entertainment entrance -> life/entertainment entrance to trade entrance -> chat -> wait without input -> fresh click.

Observed evidence:

- `/tmp/erark-tk-10-title.png`: nonblank Tk title screen; the runtime log confirmed both local mods loaded.
- `/tmp/erark-tk-17-after-long-move.png`: the first long movement returned to the destination interface without the reported block of repeated Doctor-at-the-same-place messages.
- `/tmp/erark-tk-20-move-0p4s.png` and `/tmp/erark-tk-22-move-6s.png`: the reverse long movement likewise produced no repeated Doctor movement block and recovered after transient redraw.
- `/tmp/erark-tk-27-chat-wait.png` and `/tmp/erark-tk-28-chat-still-waiting-no-click.png`: the post-movement chat settlement remained on the same explicit wait page after eight seconds without input.
- `/tmp/erark-tk-29-chat-after-fresh-click.png`: one new click advanced from that wait page to the main interface. This also demonstrates that movement skip did not leak into the next explicit wait.

The exercised route did not emit any visible NPC movement line. Therefore the GUI run confirms the reported repeated-Doctor block is absent on representative long movements, while the narrower guarantee that a visible NPC movement line carries that NPC's name remains covered by component tests rather than direct GUI evidence.

Linux/Xvfb could not apply Tk's `root.state('zoomed')`. The subagent used a temporary try/except plus fixed-geometry fallback only in an isolated evidence worktree; its complete patch is `/tmp/erark-tk-linux-shim.diff`. The evidence worktree, Xvfb, and game processes were removed after capture. The shared repository has no corresponding `Script/` or `static/` change.

## Rollback and future migration

- Disable `local_settlement_input_fix` to restore upstream wait/skip behavior.
- Disable `local_npc_move_talk_context_fix` to restore upstream paper-doll movement formatting.
- Neither rollback requires touching upstream game files.
- For a future upstream contribution, start from these narrow patch points rather than the backup branch's broad diff. The static browser change is not required by the mod design.
