# PR #218 final Tk rerun contract

## Purpose

Replay the previously approved real-Tk route on PR #218's exact live base and head, then compare the newly observed behavior with the two static images already embedded in the PR. The result is observational only: whether the new run agrees or disagrees, this session must report and record it without editing, commenting on, closing, or otherwise changing the upstream PR.

## Exact revisions

- Live PR: `Godofcong-1/erArk#218`
- PR state observed before launch: open, ready for review (`draft=false`)
- Baseline: `master@94d586840484adf21fcf746dba0444551dd6a5a1`
- Candidate: `meower-z:codex/fix-discovery-settlement-ad-hoc@4e226f4f587b82a87368a3d7976650593323a7b4`
- Renderer: real Tk (`web_draw = 0`)
- Allocator geometry: default `2100x1100x24`; game window expected at 1200x900 from the approved evidence overlay

## Deterministic inputs

- Prepared save source: `/tmp/erark-discovery-settlement-redo-baseline-20260713/save/7/{0,1}`
- Expected pristine save hashes:
  - slot data `0`: `465cb4b88fb50690ddecfa62e4584ed72f372cee40bd260dd3ff6b3f65bdd8f5`
  - slot data `1`: `f04b5179ba42c3938967968c4127c0c109621e509a84fd318e7e7bf500e1b40d`
- Evidence-only identical overlay sources:
  - `game.py`: `8f7a54afe14cce9cd469c5810813913e573898da5d49d7c65104c5a49d3ef80e`
  - `config.ini`: `c6b42618edb759830daacb8cfb4b934975ad9a645306c28fb39c7edb3cd745e4`
  - `Script/Core/main_frame.py`: `003f40baa18db357e3df462e883c852666664aae81a022373cb0ae7b224a4be0`
- Python RNG seed: `20260712`
- NumPy RNG seed: `20260712`
- `PYTHONHASHSEED=0`
- Written route: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/action-log.tsv`

## Visible assertion and stopping point

The same route must reach player H with Dobermann, discovered by Closure, then select option 1 (`用花言巧语支开对方`) with the successful judgment. Stop immediately after the selected response outcome is fully drawn; do not advance another witness or use later discovery behavior as evidence.

- Baseline expected observation: Closure's selected reaction is absent and Dobermann's H text continues.
- Candidate expected observation: Closure's explanation/departure reaction, stamina `-15`, and five-minute passage appear once before Dobermann's H text continues.

These are expectations for comparison, not assumptions. The visual agent must inspect each actual frame and report any divergence.

## Existing PR images to compare

- Before: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/baseline-missing-closure-response-clean.png`
  - SHA-256 `584baebf25b79af9ee7769fe4a0d7152a1875d321c5dd8c69d423655aa121bd5`
- After: `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/final/candidate-closure-response-once-clean.png`
  - SHA-256 `1ea9a3603978b393fe976e8a4b3fce31c846fe1a6b24c8a9d507078dd469299e`

Compare both player-visible meaning and pixels after reproducing the same 1200x900 crop. Pixel identity is useful supporting evidence but is not required for semantic agreement if an unrelated upstream visual difference is fully explained.

## Runtime and retained evidence

- Disposable runtime root: `/tmp/erark-pr218-final-tk-rerun-20260715/`
- Disposable capture root: `/tmp/erark-pr-images/discovery-settlement/pr218-final-rerun-20260715/`
- Append-only archive destination after verification: `~/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/`

The run must retain a chronological action log, manifest, controller/launcher, exact source and overlay hashes, save pre/post hashes, allocator/display/window/PID/PGID provenance, raw frames, clean comparison crops, image dimensions, and comparison metrics. After the archive is verified and reopened, remove only the two disposable roots above and confirm the allocator owner and related process groups are gone.
