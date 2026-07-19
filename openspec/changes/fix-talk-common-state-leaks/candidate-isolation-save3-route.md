# Candidate-list isolation: local save 3 route

## Production reachability

Local `save/3` provides a short normal-player route for the candidate-list isolation scope. Its header SHA-256 is `0ef14ecae52bb85d58e30ca16fd8ae1c188abf18d8b8d26c701fb4d70e5926aa`; data SHA-256 is `9a9309236c1435d84a866bbbb7d480551af59cfa60d902909fe7f9149d0da246`.

The serialized state is 2020-03-12 12:21 in the Emergency Room with only the player and Jingzhe (CID 306). Jingzhe is the current target; neither character is in H. The room is lockable and has furniture level 2, the player's waist skill is 7, and the saved relationship/talent state makes both invite-H and intercourse judgment values about 1170, above their 350 and 500 thresholds.

The shortest normal gameplay choices are:

1. `[5047]邀请H`;
2. `[6301]阴道性交` to open the position panel;
3. `[09]对面抱位` to select and execute the first face-hug action;
4. `[6311]对面抱位` to execute it again.

Further `[6311]` choices repeat the same production behavior. Returns used only to confirm visible pages are transport inputs, not new gameplay decisions.

## Trigger probability

`data/talk/sex/insert_v/face_hug_sex.csv` is the standard talk pool, not the paperdoll pool. The compiled standard data has 51 same-weight `adv_id=0`, `sys_0` entries available to Jingzhe and no CID-306-specific entry. Exactly rows 1004 and 1047 contain `{breast_s}`.

Although the save enables paperdoll text at rate 3, `face_hug_sex` is absent from the compiled Talk_Common type index, so the 30% replacement branch does not apply to this behavior. Each face-hug execution therefore reaches `{breast_s}` with probability exactly `2/51`. The first two both hit with probability `4/2601`, about 0.154%. Ten executions fit within twelve gameplay choices and contain at least two hits with probability about 5.61%.

Whenever `{breast_s}` is reached, current upstream performs the production mutation at `talk.py:662-665`: it appends the shared `common_s["A"]` values directly into the global breast-short A list. A later hit therefore sees a longer candidate list and changed duplicate weights. The one-line candidate copies only the A list before appending, so repeated expansions start from the original global configuration.

## Evidence status

This proves a normal production trigger and a bounded player route; it is not yet visual A/B evidence. No fixed seed has been chosen, and no real Tk baseline/candidate run has verified two matched `{breast_s}` hits or a legible visible divergence. A seed may not be selected by open-ended retry. Before a Tk run, supervision must approve a bounded way to freeze a seed against the full startup/input RNG stream and must define matching-trigger and invalidation gates.

The same bounded inventory found no existing local save with a twelve-choice route for the separate non-current-NPC target-restoration scope. That scope remains independently evidence-blocked.
