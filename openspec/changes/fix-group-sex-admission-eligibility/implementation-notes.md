## Task 1.1 — Core admission-caller inventory (2026-07-17, clean upstream 97c35826e)

Recorded from core source, NOT from the local mod. The local `local_group_participant_admission_fix`
mod is the private-fork wrapper being converged; it is not treated as authority here.

### Ineligibility definition (provisional, from design.md)

A character is ineligible for a **new** group-sex invitation/confirmation when ANY of:
- `hit_point <= 1` (力竭/濒倒)
- `sp_flag.tired == 1` (疲劳 flag; `handle_self_tired`)
- `get_tired_level(tired_point) >= 2` (困倦等级≥2, i.e. `tired_point/160 > 0.84`)

### Callers and their CURRENT core eligibility gate

| # | Caller (core) | Location | Current gate | Fatigue-aware? |
|---|---|---|---|---|
| 1 | Discovery entry (panel) | `sex_be_discovered_panel.Sex_Be_Discovered_Panel.draw` | none — always shows "[4]邀请对方加入群交" | ❌ |
| 2 | Discovery → join | `sex_be_discovered_panel...._invite_find_char_to_join` | `handle_premise.handle_instruct_judge_group_sex(id)` (willingness only) | ❌ |
| 3 | Invite list | `group_sex_panel.Edit_Group_Sex_Temple_Panel.show_invite_npc_panel` | `instuct_judege.calculation_instuct_judege(0,id,"群交")[0]` (willingness only) | ❌ |
| 4 | Direct invite | `group_sex_panel.Edit_Group_Sex_Temple_Panel.invite_npc` | `handle_premise.handle_normal_24567(id)` (states 2/4/5/6/7 — NOT fatigue) | ❌ |
| 5 | Group START (player) | InstructConfig 5055 `邀请群交` → premise `SCENE_ALL_NOT_TIRED` (`handle_scene_all_not_tired`) | per-char `handle_self_tired` (tired flag only) | ⚠️ partial (flag only; not hp≤1 / tlvl≥2) |

Key fact: `calculation_instuct_judege(...,"群交")` is a **willingness** judge (`InstructJudge.csv` id 45,
type S, threshold 600) computed from favorability/trust/etc. It does **not** consider fatigue. So the
per-NPC invitation paths (#2 #3 #4) admit a fatigued-but-high-willingness NPC. #5 rejects only the
`tired` flag, missing hp≤1 and tired_level≥2.

### Convergence target

One shared predicate owned by the premise/admission layer, consumed by #2 #3 #4 and the per-char branch
of #5. Discovery entry (#1) auto-leave and hide-vs-cancel visibility are UX/semantics decisions handled
under the cancellation rule (requires user confirmation before PR).

## Task 1.2/1.3 — Near-real red reproduction (2026-07-17, clean upstream, mods off)

Save/99 has NO naturally fatigued character (all `tired=False`, `tired_level=0`, `hit_point≥1970`), so
the bug is staged. `build_fixture.py` (near-real headless boot, `save_handle.input_load_save("99")`)
sets four off-scene willing NPCs and re-saves as `save/98`:

| id | name | staged fatigue | willing(群交) | join_gate | invite-list offers |
|----|------|----------------|:---:|:---:|:---:|
| 1 | 阿米娅 | hp=1 + tired flag + tired_pt=150 (tlvl2) | True | True | **True** |
| 10 | 陈 | hp=1 only | True | True | **True** |
| 43 | 九 | tired flag only | True | True | **True** |
| 56 | 特蕾西娅 | tired_pt=150 (tlvl2) only | True | True | **True** |

Each fatigue axis independently keeps the character admissible on clean upstream (RED). Confirmed cause:
the per-NPC admission gate is `calculation_instuct_judege(...,"群交")` (a willingness judge from
favorability/trust) with no fatigue term; `handle_instruct_judge_group_sex` wraps the same. `save/98`
is the Tk A/B fixture.

## Fix boundary (design record)

**Violated rule:** a character who is 力竭(hit_point≤1) / 疲劳(tired flag) / 重度困倦(tired_level≥2)
must not be offered or confirmed a NEW group-sex invitation.

**Owner:** the premise/admission layer — one shared predicate, not per-caller filters.

**Chosen boundary (Option 1):** add one premise `handle_self_can_join_group_sex(character_id)` (returns
0 when 力竭/疲劳/重度困倦, else 1) and delegate at every issuing/confirmation consumer:
- #2 discovery-join `_invite_find_char_to_join`: gate the accept branch on it (ineligible → refuse/end, already handled).
- #3 invite list `show_invite_npc_panel`: skip ineligible unless already invited (cancellation rule).
- #4 direct invite `invite_npc`: block a new invite of an ineligible char; still allow the cancel branch.
- #5 group-start `handle_scene_all_not_tired`: per-char, reject via the same predicate (folds the missing hp≤1 / tlvl≥2 into the existing tired-flag scene check) — **consistency add; confirm with critic whether in-scope.**

Baseline (clean upstream) has no fatigue check anywhere, so the diff is near-pure addition → `U≈0`;
lowest penalty = fewest added lines at the correct owner. Estimated `(a+b)+S-2U ≈ 16`.

**Rejected — Option 2 (the mod's shape):** inline the 3-condition check at each of ~5 callers. More added
lines, callers drift, direct calls bypass a filtered list; higher penalty and worse maintenance.

**Cancellation semantics — RESOLVED by user (2026-07-17):** the user chose "minimize code change in this
situation" over the proposal's provisional keep-visible-for-cancel rule. Implementation therefore applies
the eligibility filter **uniformly**: an ineligible character is hidden from the invite list whether or not
an invitation was already issued (dropped the `and not handle_self_now_go_to_join_group_sex` exception).
`invite_npc` still blocks a new confirmation of an ineligible character and keeps upstream's existing cancel
branch for already-invited characters. Current-participant / pending-invite exit for a now-ineligible
character remains out of scope (separate concern).

**Non-goals:** current-participant tired exit scheduling, group scheduler, discovery-reaction settlement
(#218), witness selection, willingness thresholds.

## Generalization (user-requested, 2026-07-17)

After review the user asked to make the predicate a general reusable one rather than a group-sex-specific
name. Investigation of `handle_self_tired` (`SELF_TIRED`) usage: 3 code sites, 0 talk/event CSV gating —
`character_info_head.py:126` (the `<累>` display, genuinely wants only the tired flag), the dead
`SCENE_SOMEONE_HP_1` premise (docstring "HP1或太疲劳" but only checks tired; no consumers), and
`SCENE_ALL_NOT_TIRED` (group-start). Because the display site needs the narrow flag, `handle_self_tired`
is NOT globally replaced. Instead the broad predicate is renamed `handle_self_can_join_group_sex` →
**`handle_self_exhausted`**, polarity flipped to match `handle_self_tired` (truthy = 力竭/疲劳/重度困倦),
and registered as premise `SELF_EXHAUSTED` (`self_exhausted`) so it is reusable from code AND talk/event
CSVs. The 4 group-sex call sites consume it. Commit 823a8d8d0. Focused test 13/13 green (adds a
premise-registration check). Runtime behavior unchanged, so the Tk A/B evidence still holds.
(Opportunity noted, out of scope: the dead `SCENE_SOMEONE_HP_1` could reuse this to fulfil its docstring.)

## Independent review (Opus, 2026-07-17) — PASS-WITH-NITS (of the pre-generalization diff; boundary unchanged)

Correctness, namespace resolution, `invite_npc` elif ordering, and the single-consumer scope of the
group-start broadening all confirmed against the real code. Focused test 12/12 green. Nits (non-blocking):

1. **Known residual (document in PR, out of scope):** a character invited while eligible who *then*
   becomes ineligible is now hidden from the invite panel (uniform filter), so `go_to_join_group_sex`
   stays True and the pending invite still routes them to the scene where group logic rejects them — the
   "admit then reject" residue persists for that pending-invite-then-fatigued sub-case. This is the
   explicitly out-of-scope current-participant/pending-invite exit concern; the in-scope rule (NEW
   offers/confirmations) is not violated. Call it out as a known limitation in the PR body.
2. Discovery-join silent refuse/end reuses the existing willingness-refusal path — acceptable; optionally
   note in the PR.
3. Optional: unify the blocked-invite message vs the silent discovery path — skip unless a reviewer asks.
