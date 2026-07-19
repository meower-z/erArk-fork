# Current-upstream diagnostic attempt 7: premature frame gate

Attempt 7 has no diagnostic-A result. It stopped after physical input 28/38, the first `[6001]` and Return, without entering the second wait.

The captured PNG had SHA-256 `961b8b559bf5f94b8223a4f65620ba1b3435243e423f66384728d489a4238107`, not the then-required PNG byte hash `00f5d13c45e2fd43a8a9612dbaa9c70e0de06abf1800cf0ca3acf495708bc2e5`. Later independent review proved the decoded 2100×1079 pixel raster is exactly identical to the accepted attempt4 result frame: AE=0, RMSE=0, and both decode to RGB raster SHA-256 `a16009f709c1885cd214e66f60bf99faeb0c997f3843dc0e23f29ef875987536`. The earlier "black incomplete repaint" interpretation was wrong; the dark frame is the fully settled game UI. The byte mismatch came only from PNG encoding.

The trace still contained only setup and wrapper-installation records and no completed `outer_wait`, so no per-wait diagnostic or RNG record exists. Because the full result frame had already settled, that absence exposes a boundary-predicate defect in the instrument rather than premature capture. Attempt 7 remains invalid under its original byte-hash contract, but its invalidation does not show player-visible behavior drift.

The setup RNG checkpoint passed, no exception appeared in game/allocator/window-manager logs, and source plus runtime save copies remained unchanged. The run was still correctly invalidated because the pre-agreed contract required the exact result-frame hash before any second wait; an intermediate frame cannot satisfy it.

The retained `INVALID.md` has SHA-256 `c442f281155a915d57352fd21a02e2f0855bfc84e6c6486ccb7a0fcb85fe6499` under `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt7/`. Allocator, runtime, control files, and disposable worktree registration were cleaned.
