# Root-Cause Audit Findings

Date: 2026-07-06

## Disposition status (updated same day)

- F1 pain dead-guard: **fixed** in `628f62295`.
- F2 group-hypnosis wipe + F3 unnormal-flag resettle: **fixed** in `7e660de42` (evaluate_hypnosis_completion wrapped at the shared origin).
- F4 group-start admission premise: **fixed** in `3f39d361d` (premise registry replacement, loop bug covered).
- F5 edge-release rejudge: **fixed** in `ad10572ad` (POST-state gate).
- Hypnosis air-type silent abort (minor): **fixed** alongside the documentation commit (warning drawn only when the room, not the degree, is the blocker).
- R1 per-count settlement: **reconciled** — delta spec now carries a MODIFIED "Batch NPC orgasm events" requirement with per-count semantics; script docstring/README reworded.
- R2 extension/pain flag contract and the remaining known-limitation items: **documented** in the respective mod READMEs (orgasm batch, edge release, movement, target context, masturbation intent, pain).
- R2 follow-up (2026-07-07): **resolved by user decision** — `pain_as_pleasure` is a permanent,
  hypnosis-gated grant: the flag persists dormant outside hypnosis states and reactivates on the
  next one; only explicit 解除催眠 (or upstream `HYPNOSIS_FLAG_TO_0`) removes it. Implemented by
  flipping the pain mod's residual branch to `restore_flag=True` (conversion still suppressed
  outside hypnosis); pinned by `test_inactive_pain_as_pleasure_keeps_pain_as_pain`.
- Critic's "monolith wave/≥3-bonus dropped" concern: **checked and refuted** — the behavior moved into the batch's `climax_count >= 3` path, pinned by `test_real_h_orgasm_batch_release_preserves_multi_count_edges` and `..._preserves_three_count_bonus`.
- Masturbation-intent README/manifest contradiction: **corrected** — the manifest's narrow judge_character_h_obscenity_unconscious wrapper is now documented as the intended resync form.
- F6 cross-platform save loading (found live by BDD on 2026-07-06, not part of the
  original audit): **fixed** in `735ce3621` via the new mod `local_cross_platform_save_fix`.

Method: each split bugfix mod was audited against the current upstream `Script/` code
by an independent reader, and every change-proposing finding was then adversarially
verified by two independent reviewers (a correctness lens and a regression-risk lens);
only findings that survived both refutation attempts are marked SURVIVES below. A
completeness critic then looked for gaps the per-mod passes missed (cross-mod
interactions, un-migrated monolith behavior, loader coverage). This audit is source
inspection plus local test runs; it does not itself execute full game flows.

Verdict scale: **root-cause** (the divergence fixes the causal defect), **shallow-justified**
(symptom patch that is the right call for a function-replacement mod, with the trade-off
stated), **shallow-needs-deepening** (a deeper fix is reachable within mod scope),
**defective** (the fix itself is buggy).

## Verdict summary

| Mod | Verdict | Disposition |
| --- | --- | --- |
| `local_group_target_context_fix` | root-cause | keep; document inert type-3 patch + out-of-scope sibling leak |
| `local_h_movement_interrupt_fix` | root-cause | keep; document `move_stop` belt-and-braces + divergences |
| `local_group_masturbation_intent_fix` | root-cause | keep; primary refuted; document manifest/README mismatch |
| `local_group_participant_admission_fix` | **shallow-needs-deepening** | **deepen**: cover the group-sex START admission path |
| `local_hypnosis_state_fix` | **shallow-needs-deepening** | **deepen**: 1212 group-hypnosis wipe + unnormal-flag resettle |
| `local_pain_as_pleasure_fix` | root-cause | **deepen**: add dead-character guard on conversion path |
| `local_h_orgasm_batch_fix` | root-cause | reconcile spec/description for intended per-count settlement |
| `local_group_edge_release_fix` | root-cause | **deepen**: POST-state rejudge trigger; document off-scene sibling |

The pair flagged as deepest-risk in the handoff (orgasm batch + edge release) both
verify as root-cause fixes; their remaining issues are a spec/description mismatch and
two narrow sibling gaps, not a broken settlement core.

## Findings to fix (confirmed, low-regression, root-cause deepenings)

### F1 — `local_pain_as_pleasure_fix`: positive-pain conversion skips the dead-character guard (minor, SURVIVES)

Upstream `base_chara_state_common_settle` returns immediately for dead characters
(`Script/Settle/common_default.py`), before any settlement. The mod's positive-pain
conversion branch (`patched_base_chara_state_common_settle`,
`mod/local_pain_as_pleasure_fix/scripts/local_pain_as_pleasure_fix.py:170-183`) converts
pain to psychological pleasure with no dead check, so a character who dies mid-H with
`unconscious_h ∈ {4,5,6,7}` and `pain_as_pleasure` set gets pleasure written where
upstream would no-op. The sibling `patched_handle_extra_orgasm` already has this guard
(`:254`), so the fix is a consistency repair inside the same file.

Fix: delegate dead characters to the captured original at the top of the `state_id == 17`
handling.

### F2 — `local_hypnosis_state_fix`: group hypnosis (effect 1212) still wipes active hypnosis state (major, SURVIVES)

The 1211 wrapper compensates for `evaluate_hypnosis_completion`
(`Script/UI/Panel/hypnosis_panel.py`) zeroing `sp_flag.unconscious_h` when the player's
default hypnosis type is 0 and target degree ≥ 50. But group hypnosis, effect 1212 /
`handle_hypnosis_all` (`Script/Settle/default.py`), calls the same
`evaluate_hypnosis_completion` per scene character and is not wrapped, so an
already-hypnotized NPC (flag 4-7) has their state wiped when the player casts group
hypnosis with default type 0.

Fix (root cause, covers both 1211 and 1212): make `evaluate_hypnosis_completion`'s type-0
branch preserve an existing 4-7 flag instead of zeroing it.

### F3 — `local_hypnosis_state_fix`: restore branch does not resettle unnormal-flag bits 5/6 (minor, SURVIVES)

Every upstream write to `sp_flag.unconscious_h` in hypnosis flows is paired with
`settle_chara_unnormal_flag(id, 5)` and `(id, 6)`; the mod's own
`_apply_current_hypnosis_state` does too (`:66-68`). The restore branch (`:193-199`) writes
`unconscious_h` without resettling, so the cached unnormal bitmask (consulted by
`handle_normal_5/6` premises) stays stale and a hypnosis-state talk gate can read the wrong
value for one settle. Fix: mirror the `settle_chara_unnormal_flag` calls on the restore path.

### F4 — `local_group_participant_admission_fix`: group-sex START path admits tired NPCs (major, SURVIVES)

The mod guards three admission entries (discovery join, invite list, direct invite) but not
the primary START path: `handle_ask_group_sex`
(`Script/System/Instruct_System/handle_instruct.py:1340-1393`) admits every in-scene NPC by
execution value alone. Its only tired gate is the instruct premise `SCENE_ALL_NOT_TIRED`
(`handle_scene_all_not_tired`, `Script/Design/handle_premise/handle_premise_place.py:696-719`),
which has a `return 1` **inside** the candidate loop — so it checks only the first non-player
NPC — and tests only `sp_flag.tired`, not the mod's fuller criteria (`tired_level >= 2` or
`hit_point <= 1`). Fix: replace `handle_scene_all_not_tired` to iterate all non-player scene
characters with the mod's `_is_character_tired_for_group_sex` criteria.

### F5 — `local_group_edge_release_fix`: rejudge fires for tired followers with no new behavior (minor, SURVIVES)

The wrapper computes `should_rejudge_status` from PRE-state and then unconditionally
re-runs `judge_character_status` after the original
(`mod/local_group_edge_release_fix/scripts/local_group_edge_release_fix.py:441-454`). The
rejudge is only needed when the original actually assigned a fresh `GROUP_SEX_NPC_HP_0_END`
behavior; for a tired follower whose follow branch assigns no new behavior, it triggers an
extra mid-flight settlement. Fix: gate the rejudge on POST-state
`behavior.behavior_id == constant.Behavior.GROUP_SEX_NPC_HP_0_END`.

### F6 — upstream: cross-platform save loading wipes scene registrations (major, live-reproduced)

Scene/map keys and dormitory-style fields are `os.sep`-joined before being pickled into
saves. Loading a save whose origin platform used a different separator (the user's
Windows playthrough on this Linux VPS) makes `save_handle.update_map` treat every
foreign-separator scene key as stale: it deletes them all and substitutes the boot-time
empty scenes, silently wiping every character's `scene_data[...].character_list`
registration. Most flows read `character.position` directly, so the game appears to
work; anything querying the scene roster degrades (empty lists) or crashes —
`group_sex_end` fails with `list.remove(x): x not in list` in
`map_handle.get_chara_now_scene_all_chara_id_list(0, remove_own_character=True)`.
Reproduced live through the web driver on slot 99 before the fix; the raw pickle was
verified consistent (player registered), isolating the defect to the load path.

Fix (root cause, `735ce3621`): new mod `local_cross_platform_save_fix` replaces
`save_handle.load_save` and normalizes all separator-joined data at the deserialization
boundary (full field inventory from scanning a real Windows save: scene/map keys,
`scene_path`/`map_path`, `dormitory`/`pre_dormitory`, `dormitory_admin_target_room`,
`air_hypnosis_position`, `facility_damage_data` keys, `maintenance_place` values).
Covered by LB-BDD-012 (failing-first synthetic + real slot-99 regression + web
full-flow verification).

## Findings to reconcile via spec/documentation

### R1 — `local_h_orgasm_batch_fix`: per-count effect settlement vs "settled once" (major, SURVIVES)

The split mod settles each orgasm behavior's effects once **per rolled count**
(`effect_behavior_counts`, `h_orgasm_batch.py:487-491`), whereas upstream's 0/1 switch settles
each id once and the **active** spec still requires the old semantics
(`openspec/specs/h-orgasm-settlement/spec.md:23-26`). Per-count is consistent with the
edge-release motivation (recovering the N-1 pent-up orgasms upstream drops) and is
deliberately tested, so it reads as an intended deepening rather than a bug. Disposition:
reconcile — add a MODIFIED requirement in the delta spec documenting per-count settlement
and reword `mod_info.json`/README so they stop claiming original attribute settlement is
preserved. (This is a spec decision; not reverting silently.)

### R2 — Cross-mod: `group_sex_extension` boost vs `local_pain_as_pleasure_fix` lazy clear (critic)

`group_sex_extension`'s 全员催眠增强 sets `hypnosis.pain_as_pleasure = True` on complete-hypnosis
group members with no requirement that they be in a hypnosis-unconscious H session. The pain
mod's `patched_base_chara_state_common_settle` has a residual-flag branch
(`_raw_pain_as_pleasure` with `restore_flag=False`, `:184-185`) that permanently clears the
flag when the character is not in `unconscious_h ∈ {4,5,6,7}` at the next pain settle. This is
a genuine cross-mod contract question (intended lifetime of `pain_as_pleasure` set outside a
hypnosis-unconscious session). Disposition: document as a known interaction and flag for the
user; do not silently change gameplay balance between a bugfix mod and a preference mod.
2026-07-07 update: user decided on the permanent-grant contract (flag persists dormant outside
hypnosis, effect stays hypnosis-gated, removal only via explicit dispel); the residual-clear
branch now restores the flag instead of deleting it. See the disposition list above.

## Findings to document as known limitations (deferred / risky to auto-fix)

- **`local_h_orgasm_batch_fix` edge-failure double-count** (minor, SURVIVES): the mod
  faithfully reproduces upstream's re-settlement math where `orgasm_judge` re-calls
  `orgasm_settle` with the same dict; a proposed idempotency fix was flagged by review as
  potentially regressive in one edit site. Document under 已知上游遗留.
  2026-07-06 live check: slot-99 full settlement carries no `orgasm_edge == 3` participant,
  so no live reproduction obtained; stays documented.
- **`local_h_orgasm_batch_fix` mark stale-filter sibling** (minor, SURVIVES): the same
  pre-built-filter defect the mod fixes for orgasms remains for marks; the proposed rebuild
  was flagged as regressive in the player-target edit site. Document; revisit with a
  narrower fix. 2026-07-06 live check: slot-99 `group_sex_end` + rest settled the ~160-entry
  player backlog with a clean error.log — no live reproduction obtained; stays documented.
- **`local_group_edge_release_fix` off-scene self-END_H** (minor, SURVIVES): an edging NPC
  separated from the player scene self-ends H and loses pending edge counters; the mod's 528
  wrapper declines because its guard only accepts `GROUP_SEX_NPC_HP_0_END`. Document as
  intentionally cleanup-only, consistent with the stale-template treatment.
- **`local_h_movement_interrupt_fix` `move_stop` belt-and-braces** (minor, SURVIVES):
  `_stop_player_move_on_h_interrupt` sets `sp_flag.move_stop = True` with no live consumer in
  the `npc_active_h` call context; the patched move loop self-clears it on the next move.
  Document (or drop the line) rather than treat as a live bug.
- **`local_group_target_context_fix` inert type-3 patch** (info): the replaced
  `npc_ai_in_group_sex_type_3` targets upstream code that is currently dead; the replacement
  is inert but harmless. Document.
- **Loader rollback coverage** (critic): `mod_manager` rollback snapshots only
  manifest-declared targets, not exec-time runtime patches (panel/registry hooks), so a
  partial load failure can leave a mod half-applied. Already acknowledged as intentionally
  narrow in the 2026-07-05 follow-up; broadening it is out of scope for this pass.
- **Un-migrated monolith behavior** (critic): the split edge-release dropped the monolith's
  wave-based release and the ≥3-release bonus orgasm. Confirm whether the drop was intended;
  if so document, if not restore. Deferred pending that decision.

## Test-coverage gaps observed

The isolated per-mod unit tests mock the `Script` modules, so they cannot catch cross-mod
interactions or upstream-drift. The new `mod/tests/bdd/` harness closes part of this: web-mode
end-to-end for boot/load/flow, and an in-process near-real harness that drives the actually
installed patches against unmocked `Script` modules and real config data (LB-BDD-007 now runs
there for real). Each deepening below lands with a regression test that fails before the fix.
