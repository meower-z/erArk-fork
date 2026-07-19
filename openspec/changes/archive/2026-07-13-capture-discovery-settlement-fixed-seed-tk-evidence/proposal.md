## Why

The discovery-settlement candidate has passed implementation review but still has no valid player-visible Tk evidence. The previous scripted title-screen attempts were invalid, so the candidate needs a fresh, deterministic A/B capture performed through visual interaction before PR prose can be written.

## What Changes

- Prepare matching upstream and candidate Tk runtimes from the same save and configuration.
- Use one explicit fixed seed, `20260712`, in both runtimes only to make the discovery trigger repeatable.
- Follow the approved direct-hidden player route through the local visual-agent workflow: inspect each captured Tk frame, choose one action from its current pixels, perform that action locally, and inspect the next frame.
- Capture and inspect matching trigger and outcome frames that show the missing baseline reaction and the candidate's exactly-once persuaded-and-left reaction.
- Keep all saves, runtime preparation, and images local; do not publish evidence, push, or create or edit a PR.

## Capabilities

### New Capabilities

- `discovery-settlement-tk-evidence`: Defines the deterministic, fair, visually operated Tk A/B evidence contract for the discovery-settlement candidate.

### Modified Capabilities

None.

## Impact

This change affects only local OpenSpec records, temporary A/B runtimes, reproduction saves, and local screenshot artifacts. It does not change production code, public APIs, committed game data, or PR state.
