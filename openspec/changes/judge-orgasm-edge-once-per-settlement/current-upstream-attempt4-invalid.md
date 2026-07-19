# Current-upstream Tk attempt 4: invalid route

## Verdict

The 2026-07-15 replay on `upstream/master@72e28051ebaaabb069d06059b4633fda90b0b621` stopped during baseline and is not PR evidence. The candidate side was not started because the frozen baseline route did not reach the required visible trigger.

## Exact route and result

- Runtime controls: save 99, `random`/`numpy` seed `0`, `PYTHONHASHSEED=0`, real Tk, allocator-owned display, full-resolution frame after each physical input.
- The replay used 38 physical inputs: 26 to load slot 99 and 12 to type and submit exactly six `[6001]等待五分钟` actions.
- No discovery panel appeared, so the prescribed `[4]` inputs for 可露希尔 or 陈 were not reachable. No seventh wait was attempted.
- All six post-wait frames and one later no-input frame were byte-identical, with SHA-256 `00f5d13c45e2fd43a8a9612dbaa9c70e0de06abf1800cf0ca3acf495708bc2e5`. They show only `凯尔希阴道小绝顶`, not the required 清流/特蕾西娅 result cluster.
- The game log contains no `Traceback`, `Exception`, `TclError`, or error line. The two save files retained their pre-route hashes. The allocator returned to 3/3 free.

## What this does and does not prove

The current-upstream replay does not reproduce the old visible route. It cannot distinguish a discovery-condition failure from later edge-settlement behavior because the target orgasm/result path was never visibly reached. It does not weaken the focused code-level regression, but it invalidates reuse of the old Tk pair as current-upstream proof and blocks a current `local-review-ready` claim.

The bounded next diagnostic question is whether live orgasm counters or discovery prerequisites differ after each wait, or whether a different normal player route can reach a stable multi-part result cluster. A new pristine A/B should begin only after that trigger route is understood.

The retained local diagnostic files are under `/tmp/erark-pr-evidence/orgasm-edge-current/formal-current-20260715-attempt4/`. The chronological action log has SHA-256 `03ef64d68494ae4a20f1bfea42a8a9acad5bc081ef016284300229a66a288200`; `INVALID.md` has SHA-256 `ab5e1637f58f5d40a4c0c63c7f681e289bbf211eadc14462151f7b11ea0c4484`.
