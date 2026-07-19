# Fable candidate-isolation final review timeout

The exact prompt is preserved in `fable-candidate-isolation-final-review-prompt.md`.

The required invocation was run from `/home/ubuntu/games/erArk`:

```text
claude -p --model claude-fable-5 --effort high --no-session-persistence "<verbatim prompt>"
```

It produced no stdout or stderr and exited only when the local 300-second command limit expired:

```text
Exit code: 124
command timed out after 300080 milliseconds
```

This is neither a CODE nor DOCS verdict. Under the user's explicit fallback authorization, the candidate proceeds only through a fresh-context independent review.
