# Apply status

## Completed preparation

- Baseline: `0dcac14dcab33fb2865f8eb9a05150336b413ed1`
- Candidate: `92121977bc4629b836383a10759d6d2ced72ae0a`
- Fresh runtimes: `/tmp/erark-discovery-fixedseed-baseline` and `/tmp/erark-discovery-fixedseed-candidate`
- Fixed seed: `20260712`, injected at the same location in both temporary `game.py` files
- Tk configuration: Chinese, 1200 x 900, debug off, Web off, all mods disabled
- Save slot: source slot 4 copied to slot 97 in both runtimes
- Save hashes:
  - `0`: `465cb4b88fb50690ddecfa62e4584ed72f372cee40bd260dd3ff6b3f65bdd8f5`
  - `1`: `f04b5179ba42c3938967968c4127c0c109621e509a84fd318e7e7bf500e1b40d`
- Visual route: `/tmp/erark-discovery-fixedseed-visual-route.md`

## Runtime blocker

The first visual preflight was deferred because another Tk evidence task held `/tmp/erark-game-capture.lock`; no discovery process was launched during that conflict.

After the lock became free, a fresh disposable baseline copy launched successfully on the real Tk display. An external Claude Chrome/noVNC visual agent was restricted from Bash and file tools and instructed to inspect the title screen, select `[001]神经重载`, and reach visible slot 97. It returned no output before the 240-second timeout (`status 124`), so genuine visual operation was not established.

The disposable game and runtime were cleaned up and the capture lock was released. No baseline or candidate evidence run started, no target image exists, and tasks 2.1 onward remain incomplete. Scripted interaction is not an acceptable fallback.

## Superseded route

The project skill was subsequently updated with the established same-machine visual-agent workflow. It explicitly uses an isolated local X display, ImageMagick window captures, `view_image` inspection, and one visually selected `xdotool` action at a time while prohibiting VNC/noVNC and blind or prerecorded input. The Chrome/noVNC timeout above is retained as history but is no longer the active blocker or the route to retry.

## Local visual apply result

The local visual preflight passed on isolated Xvfb display `:103`: the agent inspected the real title screen, selected `[001]神经重载`, and reached the page containing slot 97 through the required capture-inspect-one-action cycle.

Both temporary runtimes received the same established Linux fixed-geometry shim and the exact PR-207 cross-platform save overlay `2dd4e9d6b`. Their `Script/Core/save_handle.py` SHA-256 is `302ac805f4fa50bdac7baab52d62c45da998434006c962c4468aa9fe6a12fa7f`, with no parity diff. The slot-97 hashes remained unchanged.

The first baseline evidence run reached discovery at `N=9` but was invalidated because the visual agent selected `[4]邀请对方加入群交` instead of `[1]用花言巧语支开对方`; its named trigger was deleted. A clean retry again reached discovery at `N=9`, proving the fixed seed is repeatable, but the fixed one-hour lock holder expired before the evidence frame was accepted. Another task then acquired the shared lock, so the diagnostic frame at `/tmp/erark-discovery-visual/baseline/38-trigger.png` is not PR evidence. No persuasion action occurred in the clean retry, no candidate run started, and the approved evidence directory remains empty.

The chronological local action record is `/tmp/erark-discovery-fixedseed-action-log.md`. Task 2.1 is complete; tasks 2.2 onward remain incomplete. The next retry must use a process-lifetime capture lock with no time-based expiry.

## Completed replacement capture

The later process-lifetime-locked run completed the matched fixed-seed A/B. The accepted current-upstream/candidate package is under `/tmp/erark-pr-images/discovery-settlement/final-redo-20260713/`, with the final before/after assets under its `final/` directory. Both sides use the same startup seed sources, save, route, discovery point, and response; the comparison stops after the discoverer reaction without advancing a later witness.

The inspected result is narrower than the earlier plan's character wording: Closure is the discoverer in the accepted route. Current upstream omits her accepted-and-left reaction after the response, while candidate `5d360f71e` displays that complete reaction once before Dobermann's H text continues. The replacement `fable-5` draft and fresh artifact review passed for local review. Publication remained outside this evidence-only change.
