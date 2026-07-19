## Context

Candidate `92121977b` changes discovery-reaction settlement ownership across four production files. Its implementation review passed, but the PR gate requires one representative real-Tk before/after case. Two earlier scripted title-screen attempts selected the wrong controls and produced no valid evidence. The approved case starts from save slot 4 in the medical department emergency room, enters direct hidden sex with Closure, and uses persuasion when Leizi discovers the scene.

The baseline and candidate must be comparable. Both therefore use identical save bytes, renderer settings, player input, and the explicit fixed seed `20260712`. The seed controls only which repeated `[6201]身体爱抚` action triggers discovery; the persuasion check is deterministic in the prepared save.

## Goals / Non-Goals

**Goals:**

- Produce pristine baseline and candidate Tk trigger/outcome frames from the same normal player route.
- Prove visually that the baseline omits Leizi's explicit persuaded-and-left reaction while the candidate displays it exactly once.
- Record hashes, fixed-seed injection, discovery count, stopping point, and visual inspection results needed to establish A/B fairness.

**Non-Goals:**

- Do not change the four-file candidate, save state, gameplay values, or discovery probability.
- Do not use prerecorded coordinates, blind command sequences, batch input, debug panels, network desktop relays, or state mutation to operate the game.
- Do not publish images, write PR prose, push, or create or edit a PR.

## Decisions

1. Use the literal fixed seed `20260712` in both temporary runtimes. This is preferable to selecting a seed during capture because it makes the trigger schedule reproducible and prevents A/B drift.
2. Prepare separate temporary runtimes from exact baseline and candidate revisions. This prevents untracked tests and unrelated main-worktree changes from contaminating either side.
3. Copy the same save into an unused matching slot and record hashes before launch. No pickle or gameplay-state edits are allowed.
4. Give a local visual agent the written player route and require it to capture the current Tk window, inspect the pixels, choose one next action, perform only that action with `xdotool`, and inspect a new capture before deciding again. This follows the project skill while excluding prerecorded coordinate lists and blind input sequences.
5. Capture a trigger and outcome frame on each side at matched stopping points. The outcome pair is accepted only if the candidate shows the default persuaded-and-left reaction once and the baseline clearly lacks it after drawing has completed.
6. Keep the X display local. VNC, noVNC, Websockify, browser relays, tunnels, and host-address exposure are prohibited.
7. Apply the established Linux fixed-geometry shim and exact PR-207 cross-platform save overlay `2dd4e9d6b` identically to both temporary runtimes. These overlays only make the Windows-oriented save and Tk startup usable on the evidence host; their file hashes and parity must be recorded.

## Risks / Trade-offs

- [The fixed seed may not trigger discovery within a reasonable number of repeated actions] -> Stop and record the runtime blocker rather than changing the seed silently; update the OpenSpec design before any alternative seed is used.
- [Tk may fail to create a usable window in the current environment] -> Preserve prepared runtimes and logs, mark capture tasks blocked, and do not substitute Web or synthetic evidence.
- [Text timing or scroll position may create a false A/B difference] -> Capture at the same completed-draw stopping point and require independent inspection of all original-resolution frames.
- [Temporary seed injection could alter more than trigger timing] -> Keep the injection identical and isolated in both runtimes, record its exact location and content, and remove no other randomness.
- [A long visual run can outlive a fixed-duration lock holder] -> Hold the capture lock for the actual process lifetime with no time-based expiry, and verify ownership immediately before accepting each named evidence frame.
