## 0. Current Status

- [x] 0.1 Record the root reconstruction, candidate implementation, defensive NPC snapshot, both mod paths, global formatter scope, test limitations, and residual verification in `implementation-notes.md`
- [x] 0.2 Candidate code and test cases are written; they have not been run or accepted as end-to-end proof
- [ ] 0.3 Isolate this narrow diff from unrelated waiting-protocol edits before final review or integration evidence

## 1. Audit the Observed Release

- [x] 1.1 Statically trace effect 527, the H-orgasm batch override, the generic second-stage loop, and the Tk/Web render-collection entry points with object-identity evidence; real rendering remains open
- [x] 1.2 Reconstruct the screenshot from six deferred part counts and distinguish effect values from elapsed-time hypotheses
- [x] 1.3 Statically enumerate zero-count, multi-NPC, remote-NPC, polluted-player-ID, and unrelated queued-second-behavior paths; runtime evidence remains open

## 2. Correct Ownership and Formatting

- [x] 2.1 Pass each release into its NPC `TargetChange` and keep later second-stage effects on the same object
- [x] 2.2 Set `time_stop_release` only for non-zero counts while preserving counter and unconscious-item cleanup for every NPC
- [x] 2.3 Correct compact formatter sign handling and K/M group indexing without changing effect formulas

## 3. Verify End to End

- [x] 3.1 Add table-driven formatter regressions for 999, 1000, 999999, 1000000 and signed counterparts including -500
- [x] 3.2 Add one- and two-NPC release regressions that assert root/target attribution, counter clearing, marker consumption, and unrelated second effects exactly once
- [ ] 3.3 After the audit is complete, run focused unit tests, enabled-mod integration, Tk settlement rendering, Web collection, and relevant time-stop/H regressions; then inspect the actual diff
- [ ] 3.4 Add actual-applied-delta and cap cases and inspect stored values against reported values
- [ ] 3.5 Trace mod disabled and enabled with the real loader for zero, one, multiple, and remote NPCs plus unrelated queued effects; prove marker identity and defensive player exclusion
- [ ] 3.6 Split the Web collection assertion from `settlement_input` so this change can be verified independently of the frozen waiting protocol
