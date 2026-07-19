## Context

`Script.Design.attr_text.get_value_text()` is a shared display formatter. Its suffix list starts with `K`, but the current group index and signed string-length logic make four-digit values select `M` and can reduce a negative three-digit value to `-M`. Candidate code already exists on local `main`; this change isolates and verifies only that formatter responsibility.

## Goals / Non-Goals

**Goals:**

- Format sign independently from absolute magnitude.
- Define integer truncation at the formatter entry and preserve compact integer behavior while correcting every existing suffix group; production callers already supply integers.
- Verify all production callers, the separate target-side exact-number path, and one understandable real-Tk output.

**Non-Goals:**

- Change stored values, effect formulas, production caller conversions, or settlement ownership.
- Include time-stop release attribution or batch-mod settlement changes.
- Add new units beyond those already supported by the formatter.

## Decisions

### Derive the group from absolute numeric magnitude

Choose the existing compact-suffix group with integer magnitude thresholds, then apply the original sign to the compact text. This avoids making the minus sign part of the digit count.

Alternative considered: strip `-` from the current string logic. Rejected because it leaves the independent off-by-one suffix index in place and keeps representation details as the source of magnitude.

### Keep the formatter global and distinguish its callers from exact-number output

The defect is in the shared formatter, not in time-stop output. The candidate must remain usable by the acting character's state and experience output and by local batch output. The interaction target uses `number_to_symbol_string()` instead; that exact-number behavior is valid and remains outside this change.

The local batch caller is private compatibility verification, not a new upstream capability or a reason to include mod code in the submitted diff.

Alternative considered: patch only the time-stop caller. Rejected because the same deterministic boundary error remains for every other caller.

### Keep the submitted change presentation-only

Submitted tests assert exact text at signed boundary values and fractional truncation. A local-only production-path probe exercised the real settlement text assembly and proved that acting-character values use compact text while a target value remains exact. That larger probe is deliberately excluded from the PR diff and PR text under the reviewer-sized test rule. The PR-facing evidence uses one real Tk case rather than claiming every caller needs its own screenshot.

## Risks / Trade-offs

- **[Hidden caller expects the wrong suffix]** → enumerate every production call site and inspect representative output before review.
- **[Mixed time-stop diff obscures the boundary]** → build the candidate from the formatter-only hunk and exclude attribution or waiting-protocol edits.
- **[The helper's new fractional contract is mistaken for existing behavior]** → state that entry truncation is newly defined and verify that production callers already pass integers.
- **[A formatter fix silently standardizes target output]** → keep every `number_to_symbol_string()` target field unchanged and assert one target value remains exact.
- **[Large values retain the same off-by-one defect]** → apply the same magnitude rule through the formatter's existing suffix list and include the `G` boundary in the contract.
