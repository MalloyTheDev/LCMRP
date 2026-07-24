# 0001. Record decisions in ADRs

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Maintainer
- **Affects:** repository process

## Context

This is a solo research repository. Decisions — adopting a definition, rejecting
an approach, superseding a candidate after a study — need a durable rationale so
that later work (and any future contributor) can see *why* something was done,
not just *what* changed. A previous attempt captured this with heavyweight
"review records" and immutable registries that added ceremony without value and
were removed.

## Decision

Record significant decisions as lightweight Architecture Decision Records (ADRs)
in `docs/decisions/`, using the five-field format in `adr-template.md` (Michael
Nygard's pattern). Files are numbered `NNNN-title.md`. ADRs are append-only:
once Accepted, a decision is not edited but superseded by a later ADR.

Alternatives considered: heavyweight review-record machinery (rejected — the
ceremony it added is what we just removed); no decision log at all (rejected —
loses the rationale that makes research revisable).

## Consequences

Each real decision costs ~15 lines and no process gate. The git history plus the
ADR log together provide the immutable, dated, authored record the old
registries were trying to build. This ADR itself is the bootstrap record for the
practice.
