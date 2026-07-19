# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — the glossary of local-fork domain terms and mechanisms.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in.
- **`docs/wiki/INDEX.md`** — the project wiki: snapshot pages on cross-module contracts and invariants. Scan the index, open only the pages touching your area.
- This repo also carries extensive upstream system docs under `.github/prompts/数据处理工作流/` and per-subsystem `.md` files inside `Script/System/*` — for questions about how a game system works, those remain the primary reference; `CONTEXT.md` and ADRs cover the *local fork's* vocabulary and decisions on top of them.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo:

```
/
├── CONTEXT.md
├── docs/adr/
│   └── 0001-....md
└── Script/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0003 — but worth reopening because…_

## Keep the wiki folded

The wiki describes HEAD; a change that lands makes some pages stale. When your change alters behavior a wiki page describes, either rewrite that page in the same change (`/project-wiki` fold discipline) or state explicitly which page is now stale. Never leave a page silently contradicting the code.
