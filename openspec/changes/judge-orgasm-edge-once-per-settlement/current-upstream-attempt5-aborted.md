# Current-upstream diagnostic attempt 5: aborted hook design

Attempt 5 used baseline `72e28051ebaaabb069d06059b4633fda90b0b621`, save 99, `random`/`numpy` seed `0`, and `PYTHONHASHSEED=0`. It installed an evidence-only global `sys.setprofile` callback intended to observe the exact six-wait route selected by Fable.

The installation self-check proved that the hook did not advance either RNG at installation: the Python fingerprint remained `46f264538534643a886ab78f16bc37e702ec6d58f1c40cc2c2c5607abc7b3900`, and the NumPy fingerprint remained `b4d5a02f810c5e32e59e351fff6ce702455339fffe2d5bd724c8ea97e0c6ac9a`.

The real Tk window appeared about 105 seconds after allocator start, and the visual route reached only save-list page 8/9. Save 99 was not loaded and no `[6001]` was executed, so this attempt cannot answer whether 清流 or 特蕾西娅 receive orgasm inputs. The coordinator stopped it because a global profiler receives every Python call and return before filtering, creating broad and hard-to-attribute runtime overhead. This is a blocker for that observation mechanism, not a game or route failure.

The two save hashes remained unchanged, allocator cleanup completed, and no production file changed. The retained local `ABORTED.md` has SHA-256 `60793df548189c39631ec6d6699db5ee4a2ead33a66c9987df02f7be464c620f` under `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt5/`.

The only proposed replacement is a post-import evidence loader that wraps three exact functions: `init_character_behavior()` only to delimit waits, `orgasm_settle()` only to copy its existing input dictionaries and pre/post counters, and `search_target()` only to copy the already-computed target-601 premise data. It would call no premise function, consume no RNG, import no game module before normal startup, and assert Python/NumPy RNG-state equality around every logging section. It has not been run.
