# Current-upstream Diagnostic A attempt 8: invalid after first result confirmation

Attempt 8 used untouched current upstream `72e28051ebaaabb069d06059b4633fda90b0b621`, real Tk, pristine save 99, seed `0`, `PYTHONHASHSEED=0`, and the Fable-approved 44-input contract. No candidate code ran.

The first result-image gate passed. `frame-28-w1-result.png` is 2100×1079 and its decoded RGB raster SHA-256 is `a16009f709c1885cd214e66f60bf99faeb0c997f3843dc0e23f29ef875987536`, exactly matching the contracted first-wait result.

The next gate failed. The agent sent exactly one empty Return and waited for the bounded 40-second interval. The trace gained no completed `outer_wait`, and the inspected `frame-29-w1-after-empty-return-timeout.png` still showed the settlement text page rather than an input-ready main panel with an empty input field. The run therefore stopped before a second `[6001]`; no rescue input was sent.

This run does not answer Diagnostic A and supplies no evidence about whether the old multi-part edge trigger remains reachable. It proves only that the one-empty-Return route contract is insufficient for this exact result page. The retained evidence is under `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt8/`, including `RESULT.md`, `action-log.md`, `manifest.md`, `diagnostic-trace.jsonl`, the two inspected frames, RGB hashes, and pre/post save hashes. Source and isolated runtime saves retained the same two hashes before and after the route. The allocator was released and the disposable runtime, controller, and detached worktree were removed.

No further Tk replay may infer a new confirmation count from this failure. A new route contract must first explain the visible settlement-page waiting lifecycle and define a bounded, visually checked exit condition.
