# Local Rebase Record

## Decision

The open PR was still reported as mergeable, so rebase was not required to resolve a conflict. The branch was nevertheless 18 commits behind `upstream/master`, and its failing CI result came from that older base. None of the intervening upstream commits changed `Script/Design/hypnosis_state.py` or `Script/Settle/default.py`, so a local rebase was the lowest-risk preparation for a later PR update.

## Revisions

- Old local/remote PR head: `e1a9378b140f99cd62f9c678c3a1113981e4e342`
- Old merge base: `0dcac14dcab33fb2865f8eb9a05150336b413ed1`
- Refreshed `upstream/master`: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`
- New local rebased head: `4a2b280a4c26ffa69090ff41ea244a10954c52d4`
- New head parent: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`
- Ahead/behind after rebase: one local commit ahead, zero behind

`git range-diff` reports the old and rebased committed patch as equal. The rebase completed without conflicts.

## Dirty-State Preservation

The uncommitted one-line semantic correction and untracked local focused tests were stored in stash object `61d9307444cf3c4d9cab495cd71926f096088932`, restored after rebase, and verified against their pre-rebase hashes. The temporary stash entry was then removed.

- Restored `Script/Design/hypnosis_state.py`: `03cdd85c2910b4222dd84e3fa62e3ae18515ca9163bfbde15f4430e0aee07057`
- Restored focused test source: `2eeecc648e06973eee0130e3eccee4f80b358b76a2d71b4a7333d3dd6848b192`

## Post-Rebase Verification

- Full production diff from current `upstream/master`: two files, 25 insertions and 9 deletions.
- Uncommitted correction relative to the rebased commit: one insertion in `Script/Design/hypnosis_state.py`.
- Focused suite: `13 passed`.
- `python -m py_compile Script/Design/hypnosis_state.py`: passed.
- `git diff --check`: passed.
- Current candidate `Script/Settle/default.py`: `b98657231300367771e206656ff3ba3ddda4d36dd42748918fe3b01fb611c690`.

The two candidate production-file hashes still match the archived Tk evidence manifest, so the rebase did not change the executable code proven by that evidence.

## Remaining Boundary

No push or GitHub PR edit was performed. The remote PR still points to the old head. The rebased commit message also retains the rejected sleep-preservation wording and must be corrected when the user separately authorizes committing/amending the one-line fix and updating the remote branch.
