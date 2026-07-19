---
name: capture-tk-evidence
description: Capture deterministic before/after screenshots from the real erArk Tk renderer, end to end. Allocates a display, launches baseline and candidate, navigates the game mouse-only by reading each frame, and hands the frames to review and publishing. Use when a bugfix or PR needs visual A/B evidence from the Tk game, when a capture attempt got stuck in the game's menus, or when investigate-game-bug reaches its evidence step.
---

# Capture Tk Evidence

Produce a comparable pair of screenshots from the real erArk Tk game: a baseline frame that shows the bug and a candidate frame that shows it gone. You have vision and a shell but no game knowledge; this skill supplies both the capture protocol and the in-game route. The governing discipline is **frame-driven and mouse-only**: interact by clicking (and scrolling to) the buttons you can see on the current screenshot. Never type, and never act on a memorized or assumed game state. You can only click a button that is on the frame, so the classic failure of sending a value to the wrong screen is impossible by construction.

This file covers the common case: display setup, launch, frame capture, the vision-click loop, and the in-game route. Read [references/tk-evidence-known-good.md](references/tk-evidence-known-good.md) once before your first run; it holds the full launcher template, capture contract, hashing, archiving, and cleanup.

## Set Up the Display and Launch

Both phases (baseline and candidate) run inside one allocator-owned controller. Never launch the game outside the allocator: untracked launchers escape its cleanup and reservation checks.

1. Start the controller through the shared slot allocator (the script lives in the sibling skill; do not copy it):
   ```bash
   python .codex/skills/investigate-game-bug/scripts/tk_capture_slots.py run \
     --owner <thread:candidate> --runtime <runtime-dir> -- <absolute-controller-path>
   ```
2. **Use the display the allocator reports.** `run` blocks while the game lives, so start it in the background; it prints a JSON line with `"display": ":NN"` (also readable via `tk_capture_slots.py status`). The controller inherits that display as `$DISPLAY`, but your own driver shell, where you run xdotool and import, does not. Read `:NN` from that JSON and `export DISPLAY=:NN` in the driver shell before any capture. The value may well be `:0` on a headless host with no real desktop — that is correct; use exactly what the allocator reports and never substitute a guessed number.
3. Keep the allocator's default geometry, **`2100x1100x24`**. Start `openbox` on `$DISPLAY` *before* the game so the window can maximize.
4. Launch with the **read-only probe launcher** `.codex/skills/capture-tk-evidence/scripts/tk_evidence_launcher_probe.py`. It seeds the run, installs the Linux maximize shim (maps Tk's `wm_state("zoomed")` to `window.attributes("-zoomed", True)`), runs the runtime's `game.py`, **and** — every ~300 ms — writes `$ERARK_BUTTONS_JSON` (see below): a map `{button-return-value → [center_x, center_y]}` of every button currently clickable, read straight from the game's Tk widget so the coordinates are exact. It only *reads* widget positions and changes no game state, so both phases share it without corrupting the A/B.
   - Set `ERARK_BUTTONS_JSON=<evidence-dir>/buttons.json` in the launcher's environment.
   - Confirm `web_draw = 0` in the runtime's `config.ini` and set `PYTHONHASHSEED=<seed>` before Python starts.
   - **Without the maximize shim (and openbox), the window stays small (~`1238x937`) and captures are unusable; a correctly maximized window is ~`2100x1079`.** This is a common past mistake.

   Controller pattern (openbox first, then the probe launcher):
   ```bash
   ... run --owner <owner> --runtime <runtime> -- \
     bash -c 'openbox >openbox.log 2>&1 & ERARK_BUTTONS_JSON=<dir>/buttons.json PYTHONHASHSEED=<seed> <venv-python> .codex/skills/capture-tk-evidence/scripts/tk_evidence_launcher_probe.py >game.log 2>&1'
   ```
5. Run baseline then candidate sequentially in the same controller, each behind a `ready`/`done` handshake; the controller keeps each game alive until the visual worker signals `done`.

## Capture a Frame

Find the window once per phase, then capture the **window itself** (never the root desktop) on the **allocated** `$DISPLAY`:

```bash
window_id=$(xdotool search --onlyvisible --name '^erArk ' | head -n1)   # allow up to 180s cold start; fail if the process died
xdotool windowactivate --sync "$window_id"
import -display "$DISPLAY" -window "$window_id" frame.png
```

Verify the very first frame is the maximized size before doing anything else:

```bash
identify frame.png    # expect ~2100x1079; ~1238x937 means the window did NOT maximize, so fix openbox / the shim first
```

Open and read every frame before acting. The first settled frame is the **title menu**; from there you enter the Frame Loop and follow the route below (your first click loads a save).

## The Frame Loop

One cycle, no exceptions:

1. Capture the game window.
2. Open and read the full-resolution frame.
3. Identify the current screen from its title and visible buttons (see the Screen Atlas below).
4. Choose exactly one input that this screen accepts.
5. Send exactly one mouse action: a click on a button **by its ground-truth coordinate from `buttons.json`**, or one scroll notch. Never type, and never estimate a click pixel from the screenshot — the model sees a *downscaled* frame, so estimates miss (a prior run clicked into the language-settings menu that way).

   To click a button:
   a. Read the current frame only to *decide which* button you want, and its return-value: the `[NNN]` number, a category's Chinese name (e.g. `猥亵`), or an instruction CID (e.g. `5055`).
   b. Look up its exact center in `$ERARK_BUTTONS_JSON`:
      ```bash
      read x y < <(python3 -c "import json,os;d=json.load(open(os.environ['ERARK_BUTTONS_JSON']));print(*d['<key>']) if '<key>' in d else print('MISS')")
      ```
      If the key is `MISS`, that button is not currently on screen: scroll to bring it into the viewport, wait, and re-read `buttons.json`. (`buttons.json` lists only the *active* buttons — stale ones from scrolled-away panels are gone — so it doubles as your "which panel is active" check.)
   c. Click it:
      ```bash
      xdotool mousemove --window "$window_id" $x $y click 1
      ```
   For a scroll: `xdotool mousemove --window "$window_id" 1050 550 click 4` (button 5 = down); scroll one notch, re-read, reverse if the target moved away. `--window` keeps coordinates window-relative.

   Only if the probe/`buttons.json` is unavailable, fall back to estimating a pixel, but first draw a red marker at it on the frame (`convert frame.png -fill red -draw "point <x>,<y>" marked.png`), open `marked.png`, and confirm the dot sits on the target before clicking.
6. Wait for Tk to redraw; capture and read again before the next input.

**Verify progress by the active panel's identity, not by raw bytes.** Some screens animate (the title screen runs a live "neural connection" animation), so consecutive captures differ byte-to-byte even when nothing advanced. After each click, confirm the newest bottom panel is the screen you expected; if the same panel is still active, your click missed its target: re-read the button's exact pixel position and click again, do not proceed or start scrolling. (A byte-identical frame does mean no effect, but a byte-changed frame does not prove progress.) If a frame looks partially drawn, send nothing and capture again until it settles. If the game prints 「您输入的选项无效，请重试」, your input hit the wrong panel: stop, re-identify the active panel, and re-plan.

Explore first, then replay: once the route works, restart both phases from pristine saves and give baseline and candidate the identical input sequence.

## How the Game Accepts Input

Interact by **mouse clicks at exact coordinates from `buttons.json`**. Every screen is a menu of buttons; each button's return-value and exact center pixel are in `buttons.json`, so you click by coordinate lookup — never by typing (the game accepts typed values too, but typing is banned here: it caused the original wrong-screen failures and is fragile with Chinese names and leading zeros) and never by estimating a pixel from the downscaled screenshot (that made a run click into the wrong menu). Reading the frame tells you *which* button and *which panel*; `buttons.json` tells you *where* it is.

**The screen is an append-only log.** Each action appends a new panel *below* the previous content; the old menus stay on screen above it but are inert. The buttons you can actually act on are always the **newest block at the bottom**, usually under a fresh highlighted header (e.g. `神经连接柜`). Act only within that bottom-most active panel; clicking a stale menu above does nothing, which reads as being "stuck". After a redraw the view sits at the bottom — scroll up only to read text that ran off the top, then back down to act.

The on-screen label gives you the button's **`buttons.json` key** — the return-value you look up for its coordinate:

- A save row `[007] No.7 …` → key `"7"` (the bracket number, leading zeros stripped).
- A category button `[猥亵]` → key is its **Chinese name**, `"猥亵"`.
- An instruction `[<CID>]<名称>`, e.g. `[5055]邀请群交` → key is the CID, `"5055"` (a stable number in `data/csv/InstructConfig.csv`).
- The internal `instruct_id` (e.g. `ask_group_sex`) is never a key and never used to interact.
- A button whose premises fail is **absent from `buttons.json` and from the panel**. If a target key is missing, scroll to bring it into view; if it never appears, its premises are unmet. Diagnose; do not force it.
- After an action that ends in a wait-prompt (no keys in `buttons.json` — e.g. group-sex settlement text), advance the log with one click in an empty area; repeat until the next active panel's buttons appear.

## Screen Atlas and Route: Save → Main Scene → Instruction

The route below is the reusable navigation skeleton. Save slot, page, and instruction are scenario parameters: confirm each on screen, never from memory.

**1. Title menu.** Identify by the list `[000] -【初次唤醒】-` … `[004] -【断开连接】-`. To load a game, click `[001] -【神经重载】-`.

**2. Save list (神经连接柜).** Identify by the title `神经连接柜` and a page marker like `(0/9)` (page markers are 0-based, so `(0/9)` is the first page). Rows show either `No.<slot> <metadata>` (a real save) or `空槽位` (empty, not loadable). The bracketed number is the **page-local button index**, not the slot number: on the second page, slot 17 can appear as `[007] No.17 …`. Click the row whose `No.` matches your target save; use the previous/next page buttons if it is on another page. If your target row reads `空槽位`, the runtime is missing its save fixture: stop and fix the fixture.

**3. Save actions.** After picking a save you get `[000]读取 / [001]删除 / [002]返回`. Click `[000]读取`.

**4. Load confirm.** `[000]确认读取存档 / [001]取消`. Click `[000]确认读取存档`. The game switches to the main scene.

**5. Main scene.** Identify by the 场景 header, game time, current location, and character list. The **instruction panel is part of this same screen**, below the scene and character info; there is no separate instruction menu to enter. After a load the view often rests at one end, so the category row and instruction buttons may be off-frame. Scroll one notch (button 4 up / button 5 down), re-read the frame, and repeat until the category row and your target `[<CID>]<名称>` are on screen. Never submit a CID you cannot see.

**6. Category row.** A row of category buttons such as `[日常] [娱乐] [工作] [技艺] [猥亵]`. Colored = category enabled (its instructions are listed); gray = disabled. To enable a gray category, click it, then wait for the redraw. Clicking a colored category **disables** it: leave enabled ones alone.

**7. Select the instruction.** Confirm the exact `[<CID>]<名称>` button is on the current frame, then click it. If the instruction is not listed after its category is enabled, its premises are unmet (wrong save, missing interaction target, scene population, fatigue, H-state…). Diagnose against the instruction's premise list in `data/csv/InstructConfig.csv`; never click a CID button that is not visible.

Example verified route (scenario provenance, not constants): load save 7 from the first page and fire `[5055]邀请群交` (category 猥亵, internal id `ask_group_sex`) = click `[001]` → click `[007] No.7` → click `[000]读取` → click `[000]确认读取存档` → scroll until the 猥亵 row is visible → click `[猥亵]` if gray → scroll until `[5055]邀请群交` is visible → click it. Each click sent only after its screen was confirmed on a frame.

## Guardrails (from a real failed run)

The archetypal failure: an agent typed an instruction CID into the save-list screen, was rejected with 「您输入的选项无效，请重试」, and never reached the instruction at all. Mouse-only interaction plus the rules below make that class of failure impossible.

- Click by `buttons.json` coordinate; never type and never estimate a pixel from the screenshot. `buttons.json` holds the exact center of every active button. Typing caused the original wrong-screen failure; estimating from the downscaled frame made a later run click into the language-settings menu. A key absent from `buttons.json` is simply not on screen — scroll to reveal it, do not guess a location.
- One mouse action per frame cycle: one click or one scroll notch. Batching clicks and scrolls lands later actions on stale or half-redrawn screens and forks the A/B routes without warning.
- Confirm each transition visually. Four quick clicks prove nothing; only the main-scene frame proves the save loaded.
- A wait-prompt is dismissed by clicking the control the frame actually shows, never a blind center-click on a screen you have not identified.
- Judge progress by the active panel's identity, not by whether bytes changed. Animated screens (e.g. the title screen) change bytes without advancing, so a changed frame is not proof of progress; confirm the panel you expected is now the bottom-most active one. A byte-identical frame does still mean no effect.
- The probe launcher is read-only (it only reads Tk widget positions) and identical for both phases, so it does not affect the A/B. Still record runtime, mode, save hash, seed, geometry, and launcher per phase.
- Evidence is what you re-opened and read: the final baseline frame visibly shows the bug, the candidate frame visibly does not, and both were produced by the same replayed input sequence from pristine saves.
- When the route cannot be established, stop and report a blocker with the current frame, last accepted input, rejection text, and logs. A fabricated or guessed capture is worse than no capture.

## Finish and Hand Off

On finish, archive per the reference, end the controller, and confirm `tk_capture_slots.py status` no longer lists your owner. Never kill Xvfb / openbox / game.py by name.

The archived evidence feeds two downstream skills:

1. `review-erark-pr-artifacts` audits the frames and the PR draft against the actual diff before anything is called ready.
2. `publish-pr-screenshots` publishes the approved images via the fork's `assets` branch after review; publishing needs its own approval.

Deliver to the reviewer: the evidence directory, the capture contract, the per-phase provenance records, and the chronological action log.

> Integrator note: `investigate-game-bug` still carries the original copy of `references/tk-evidence-known-good.md`; it should be updated to point at this skill instead. `scripts/tk_capture_slots.py` stays in `investigate-game-bug` as the shared single copy.
