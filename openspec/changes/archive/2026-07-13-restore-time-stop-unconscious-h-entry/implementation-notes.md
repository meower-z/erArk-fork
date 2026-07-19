## Current Boundary (2026-07-11)

This change is now the premise-only upstream candidate for instruction 5052. The public production diff is expected to contain one edited CSV line. Player H-reset cleanup, generic Web dispatch rechecks, waiting/panel protocols, local mods, and unrelated UI behavior are excluded.

Current `upstream/master` at selection time is `0dcac14dc`, where instruction 5052 still contains `NO_TARGET_OR_TARGET_CAN_COOPERATE_OR_IMPRISONMENT_1`.

## Confirmed Root Cause

The composite added by `b206249a5d` contradicts the action it guards. Its cooperation branch expects an awake/cooperative target, so valid sleeping and time-stopped targets fail. Its imprisonment alternative does not itself prove that the target is neither parturient nor postpartum. Replacing the composite with independent unconscious and pregnancy facts directly expresses the intended contract.

## Prior Private Work

Private commit `0b3f1c1a9` combined this CSV fix with player H-reset cleanup, shared Web premise evaluation, dispatch-time Web checks, time-stop release ownership, global number formatting, tests, and OpenSpec artifacts. It is evidence that the broader local experiment existed, not a suitable upstream patch.

The earlier 30-case test file covered the broader combined scope. Its premise matrix and compiled-data checks may inform the clean regression, but its reset and Web assertions are outside this change and must not be carried into the public branch by default.

## Generated Data and Protected Localization

`data/data.json` is ignored by Git, so runtime state cannot be inferred from `git status`. Local verification must inspect instruction 5052 structurally after a controlled rebuild.

The two protected files are:

- `data/po/zh_CN/LC_MESSAGES/erArk_cook_question.po`
- `data/po/zh_CN/LC_MESSAGES/erArk_csv.po`

Hash both before and after the rebuild. Do not rely on `BUILD_PO=False` alone because the existing build path can still rewrite CSV localization output. Prefer the clean worktree's normal boot-time CSV loader if it rebuilds only runtime JSON, and verify substance afterward.

## Evidence Standard

Acceptance requires all of the following:

- a red-capable focused regression against current upstream;
- a green premise matrix after the one-line edit;
- a structured read of rebuilt `data/data.json`;
- byte-identical protected PO hashes;
- normal Tk before/after evidence using the same gameplay setup;
- a fresh diff review proving the public production scope is one CSV line.

The user authorized the source push, publication of the two approved screenshots, and creation of an upstream Draft PR on 2026-07-11.

## Verification Completed (2026-07-11)

- Clean worktree: `/home/ubuntu/games/erArk-upstream-time-stop-unconscious-h-pr`
- Branch: `codex/restore-time-stop-unconscious-h-entry`, based on `upstream/master` at `0dcac14dc`
- Focused regression: 7 failures on the untouched upstream premise chain, then 21 passes after the one-line CSV edit
- Covered unconscious states 0 through 7, two ordinary locations, parturient/postpartum targets with and without imprisonment, and the retained target/H/hidden/stamina gates
- Isolated runtime rebuild produced `data/data.json` SHA256 `0b2db00f884299592b185d2f17884106512030ce01a0e5a0ff2a702920593c91`
- Structured runtime inspection confirmed the exact accepted premise chain and absence of the old composite
- Protected PO hashes remained `dad573de8e27829029b7d214cf4a511670a5d5c545fc54c494fd52ca888394e5` and `023b33166e3039440083d90cedacefb6279eafb9230050ae2f6d074e581c0462`
- Normal Tk evidence used byte-identical slot 98 saves in the before and after worktrees
- Before: `/tmp/erark-5052-before-actions-wide.png` shows the complete available action list without instruction 5052
- After: `/tmp/erark-5052-after-actions-wide.png` shows `[5052]无意识奸` in the same action list
- Entry: `/tmp/erark-5052-after-entered-wide.png` shows `进入无意识奸模式`; `/tmp/erark-5052-after-h-interface-wide.png` shows the resulting unconscious-H action interface
- Final public production diff: one insertion and one deletion in `data/csv/InstructConfig.csv`; generated data, test artifacts, shims, saves, screenshots, mods, and OpenSpec files are absent
- Local PR draft: `/tmp/erark-time-stop-unconscious-h-pr.md`
- Source commit: `66e3d2b5237327efcdc87250d4e39e3a81bfb928` on `meower-z:codex/restore-time-stop-unconscious-h-entry`
- Approved screenshots: published from the append-only `assets` branch at `305f21f23cd58805add7edcd6906d3153459d5f8` with commit-pinned raw URLs
- Upstream PR: `https://github.com/Godofcong-1/erArk/pull/211`; created as a Draft and marked ready for review by the user at `2026-07-11T23:25:15Z`
