# Maintainer `SPECIAL_FLAG` before/after Tk evidence contract

## Purpose and boundary

Replay the approved deterministic Tk route against current upstream baseline and the maintainer-required `SPECIAL_FLAG` candidate. This is local evidence only: do not push, publish, edit, comment on, close, or otherwise mutate PR #218.

## Exact sides

- Baseline: `upstream/master@58587deac62149d80c82b5a3c98ad29f51cfe2b4`
- Candidate: `codex/fix-discovery-settlement-special-flag@c75b3b1737f5ab958b520e568d8aead59cd1d413`
- Candidate parent: `58587deac62149d80c82b5a3c98ad29f51cfe2b4`
- Renderer: real Tk only (`web_draw = 0`)
- Allocator geometry: default `2100x1100x24`; use the same allocator-owned controller/display for sequential baseline and candidate phases

The candidate runtime must contain only the committed production revision. The local source-loading test under the candidate worktree's untracked `tests/` directory is not runtime or PR material.

## Deterministic setup

- Prepared save source: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/prepared-save/{0,1}`
- Required pristine SHA-256:
  - `0`: `465cb4b88fb50690ddecfa62e4584ed72f372cee40bd260dd3ff6b3f65bdd8f5`
  - `1`: `f04b5179ba42c3938967968c4127c0c109621e509a84fd318e7e7bf500e1b40d`
- Python RNG seed: `20260712`
- NumPy RNG seed: `20260712`
- Environment: `PYTHONHASHSEED=0`
- Evidence-only 1200x900 window overlay and launcher method: reproduce the three overlay files and their hashes recorded in the archived controller at `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/controller.sh`; apply byte-identical overlays to both disposable runtimes only.
- Physical input route: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-final-rerun-20260715/expected-physical-route.tsv` (exactly 38 inputs, one action per inspect/capture cycle)

## Visible assertion and stopping point

The shared route must reach player H with Dobermann, discovered by Closure, select option 1 (`用花言巧语支开对方`), and stop after the selected response has fully drawn. Do not advance another witness or a later discovery event.

- Baseline expected observation: Closure's selected reaction is absent and Dobermann's H text continues.
- Candidate expected observation: Closure's explanation/departure reaction, stamina `-15`, and `5分钟过去了` appear once before Dobermann's H text continues.

These are hypotheses to check from the captured frames, not a substitute for inspecting them. Capture the actual game window, inspect full-resolution frames before each next input, and if a partial redraw appears, issue no input until a settled no-input capture is inspected.

## Required retained evidence

- Disposable runtime root: `/tmp/erark-discovery-settlement-special-flag-tk-20260715/`
- Disposable capture root: `/tmp/erark-pr-images/discovery-settlement/special-flag-20260715/`
- Append-only archive: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-218/local/discovery-settlement-special-flag-c75b3b173-20260715/`

Before running, require the archive destination to be absent. Retain the controller, launcher, contract, runtime/source hashes, overlay hashes, pre/post save hashes, allocator/display/window/PID/PGID provenance, chronological action log, all raw frames, final clean frames, image dimensions, and pixel-comparison metrics. Re-open archived final images and validate archive checksums before cleanup. Then remove only the two task-owned disposable roots, let the allocator release the owner, and confirm the owner is absent from allocator status.
