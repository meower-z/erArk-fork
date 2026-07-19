/investigate-game-bug
/review-erark-pr-artifacts

Produce the final Chinese upstream PR title/body for the compact-value-formatting candidate by surgically updating the user-approved draft at `/tmp/erark-compact-value-formatting-pr-draft.md`.

Exact candidate boundary:

- Worktree: `/home/ubuntu/games/erArk-pr-compact-value-formatting`
- Base: `3a1c9e62003f2b4b857500b850463d3fb5b1d0e5`
- Head: `7fd521bb6d98fcaa0841cce79e6d82ecf9c04b82`
- Submitted diff: `Script/Design/attr_text.py` plus the 50-line `tests/test_compact_value_formatting.py`
- The large `test_real_settlement_callers_keep_compact_self_and_exact_target_values` test is not submitted. The draft sentence describing its `handle_settle_behavior` probe is therefore unsupported and must not appear.

Approved public visual evidence:

- Before: `https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/before-watch-movie.png`
- After: `https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/after-watch-movie.png`
- Both are inspected real-Tk 2100x1079 screenshots from the same prepared-save `看电影` route. They differ only in the intended compact suffix pixels: before shows `习得 +3M`; after shows `习得 +3K`. `学识经验 +1` and the surrounding settlement remain unchanged.
- Both raw URLs return HTTP 200 `image/png`, have no attachment disposition, and are pinned to the immutable full asset commit.

Make only these changes to the existing draft:

1. Delete the second verification bullet beginning `- 自动化检查（直接驱动 handle_settle_behavior` because it describes the removed large test. Add no replacement test prose.
2. Replace the existing `（图1：修复前，看电影结算画面，习得 +3M）` placeholder with a linked Markdown image whose alt text is `修复前：看电影结算画面，习得 +3M`, using the before URL for both `src` and `href`.
3. Replace the existing `（图2：修复后，看电影结算画面，习得 +3K）` placeholder with a linked Markdown image whose alt text is `修复后：看电影结算画面，习得 +3K`, using the after URL for both `src` and `href`.
4. Preserve the title, headings, every other sentence, order, and wording byte-for-byte. Do not add a test count, command, scope section, non-goal list, local path, investigation detail, or new caption prose.

Return the complete final draft only, with the title as the first Markdown heading, no explanation, and no code fence.
