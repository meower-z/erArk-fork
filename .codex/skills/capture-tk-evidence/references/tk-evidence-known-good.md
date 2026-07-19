# Known-Good Tk Evidence Profile

Use this profile as the starting point for deterministic before/after evidence from the real erArk Tk renderer. It records the reusable method proven during PR #217 and separates required settings from values that happened to be allocated during that run.

## Acquire The Display

Run both baseline and candidate phases inside one allocator-owned controller:

```bash
python .codex/skills/investigate-game-bug/scripts/tk_capture_slots.py run \
  --owner <thread:candidate> \
  --runtime <candidate-worktree> \
  -- <controller>
```

Keep the allocator's default Xvfb geometry `2100x1100x24` unless the evidence needs a different verified layout. This size produced a readable `2100x1079` maximized erArk window with the settlement result and its unchanged surrounding values in one frame.

Before launching, write the capture contract: the exact visible assertion, baseline source ref and runtime, candidate source ref and runtime, enabled mods or overlays and their hashes, prepared save or fixture and its hashes, trigger state, route, seed controls, expected unchanged context, evidence directory, and stopping condition. Do not begin an A/B run whose two sides are not fully identified.

Do not hard-code a display number. Read `$DISPLAY` and `$ERARK_TK_CAPTURE_SLOT` inside the controller. PR #217 happened to receive slot `0` and `DISPLAY=:25`; those are provenance values, not configuration requirements. Start `openbox` on the allocated display before launching the game.

Run baseline and candidate sequentially in that same controller so they share the display geometry and window-manager behavior. Never start this launcher outside the allocator: launcher-based processes are not guaranteed to be recognized by the allocator's legacy-process reservation check. Keep each phase alive behind a `ready`/`done` handshake while the visual worker inspects and operates the window.

Let the controller and its game and `openbox` children inherit the allocator-created process group; do not use `setsid`, `disown`, or another detachment mechanism. Install a controller exit trap that terminates and reaps its current game and `openbox` children. The allocator remains the final process-group cleanup boundary.

## Launch The Real Tk Game Deterministically

Use `web_draw = 0`. Set `PYTHONHASHSEED` before Python starts, and seed both Python and NumPy before importing any game module:

```python
import random
import runpy
import sys
import tkinter
from pathlib import Path

import numpy

original_wm_state = tkinter.Wm.wm_state


def linux_compatible_wm_state(window, newstate=None):
    if newstate == "zoomed":
        window.attributes("-zoomed", True)
        return None
    return original_wm_state(window, newstate)


random.seed(<seed>)
numpy.random.seed(<seed>)
tkinter.Wm.wm_state = linux_compatible_wm_state
tkinter.Wm.state = linux_compatible_wm_state
sys.path.insert(0, str(Path.cwd()))
runpy.run_path("game.py", run_name="__main__")
```

Launch it as `PYTHONHASHSEED=<seed> python <launcher>`. The `zoomed` compatibility shim avoids Linux Tk rejecting the Windows-style maximized state. PR #217 used seed `20260714` for all three seed controls.

Copy byte-identical prepared save files into both runtimes before launch and record their SHA-256 hashes. After the route, hash both runtime copies again. If the route should not save, require the original hashes to remain unchanged. If normal gameplay intentionally autosaves, preserve and compare both post-route saves, and restore the same pristine inputs before replaying either phase. Keep generated PO or other launch side effects out of the candidate diff.

## Find And Record The Window

Poll for the visible game window while also checking that the game process is alive:

```bash
window_id=$(xdotool search --onlyvisible --name '^erArk ' 2>/dev/null | head -n 1 || true)
xdotool windowactivate --sync "$window_id"
```

Allow up to 180 seconds for first launch on a cold runtime. Fail if the process exits or no window appears. Record, for each phase:

- runtime path and source commit or source-file hashes;
- display, allocator slot, Xvfb geometry, window id, window title, and captured dimensions;
- supervisor, controller, game, and Xvfb PID/PGID values, gathered explicitly from allocator state and `ps` rather than assumed to exist in one status record;
- save, launcher, action-log, and retained-frame hashes.

The PR #217 run produced window id `4194341` and title `erArk 2026.7.13-1 -α测` in both phases. Treat these only as a comparability check for that archived run, never as reusable constants.

## Operate And Capture One State At A Time

After inspecting the current full-resolution screenshot, issue exactly one physical input. The following are alternatives for separate inspect/capture cycles, not a two-command batch:

```bash
xdotool type --clearmodifiers --delay <milliseconds> '<text>'
xdotool key --clearmodifiers Return
```

Capture the actual game window rather than the root desktop:

```bash
import -display "$DISPLAY" -window "$window_id" <frame.png>
```

Open every frame with `view_image` before deciding the next action. Wait for Tk to finish redrawing; if a capture is partial, send no input, capture again, and proceed only after inspecting the settled frame. A partial redraw occurred during PR #217 and this pause prevented the A/B routes from diverging.

Once exploration finds a short route, replay the written route from pristine saves. Give baseline and candidate the same physical inputs in the same order. Typing a value is one physical input and pressing `Return` is the next; inspect and capture between them. The proven PR #217 example used ten inputs to load slot 0 and run command `3008` (`看电影`); that route is an example, not a general requirement.

## Prove The Pair Is Comparable

Inspect the final full-resolution images, then use metadata and pixel comparisons as supporting checks:

```bash
identify <baseline.png> <candidate.png>
sha256sum <baseline.png> <candidate.png>
compare -metric AE <baseline.png> <candidate.png> null:
```

Prefer a byte-identical pre-action frame. Explain every visible final difference and confirm unchanged context remains visible. PR #217 had byte-identical `2100x1079` pre-action frames and only 143 changed pixels in the result frames: `习得 +3M` became `习得 +3K`, while the surrounding target values and action output stayed identical.

## Close And Archive The Run

Append every input to a chronological action log with UTC time, phase, frame label, action type, and value. Preserve the controller, launcher, prepared save, manifest, provenance, action log, and final evidence under `~/games/archive/erArk-upstream-pr-evidence/PR-<number>/local/<candidate>/`.

Treat that archive as append-only. Before copying, require the destination not to exist. If the same candidate needs another retained run, create a uniquely named run subdirectory or stop for collision resolution; never delete or overwrite earlier evidence implicitly.

Re-open the archived media and compare its hashes with the capture source. End the controller, let the allocator release its process groups and display, and confirm `tk_capture_slots.py status` no longer lists this owner. Delete only task-owned disposable `/tmp` paths; do not disturb another allocator owner or unrelated process.
