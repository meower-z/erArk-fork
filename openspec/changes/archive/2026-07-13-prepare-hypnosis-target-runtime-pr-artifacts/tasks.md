## 1. Reconfirm The Minimum Boundary

- [x] 1.1 Have a fresh reviewer apply `investigate-game-bug` to the updated proposal, upstream paths, and current candidate, recording every finding only as a clue
- [x] 1.2 Evaluate the review clues against the confirmed design, then record the user's decision to retain only the directly extracted four-assignment helper

## 2. Correct The Candidate

- [x] 2.1 Rework the candidate helper to contain only the four sub-state assignments copied from direct `解除催眠`; keep unconscious matching and flag recalculation in each caller, remove the sleep-path `pain_as_pleasure` clear, and make no `npc_active_h` change
- [x] 2.2 Add or update focused local checks for the changed sleep path, unchanged direct path, unchanged `npc_active_h`, and existing neighboring cleanup
- [x] 2.3 Re-open the final diff and verify it contains no unrelated semantic change

## 3. Replace Runtime Evidence

- [x] 3.1 Prepare matching upstream and corrected-candidate runtimes from the same local save and route
- [x] 3.2 Have a visual subagent capture the minimum sleep-exit A/B sequence under the frame-by-frame local Tk rules
- [x] 3.3 Inspect the retained images and confirm upstream loses `苦痛→快感` while the corrected candidate retains it

## 4. Rewrite And Review PR Artifacts

- [x] 4.1 Mark the old screenshots and direct-cancellation PR narrative stale and exclude them from the corrected PR package
- [x] 4.2 Use the required `fable-5` medium-effort writer to produce corrected Chinese PR prose from the exact final diff and inspected evidence
- [x] 4.3 Run fresh `review-erark-pr-artifacts` review and resolve supported prose or evidence findings without widening the production fix
- [x] 4.4 Stop before updating the public fork branch, assets, or PR and wait for separate authorization; later publication proceeded only after the user separately authorized it
