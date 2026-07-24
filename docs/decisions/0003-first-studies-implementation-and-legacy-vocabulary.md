# 0003. First studies, reference implementation, formal model, and legacy vocabulary

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Maintainer
- **Affects:** `studies/`, `impl/`, `formal/`, `docs/taxonomy/*`

## Context

With the lightweight rules in place (ADR-0002), the project ran its first
studies and built the first executable artifacts, all solo and AI-assisted.
Two loose ends surfaced during a consistency pass: the flagship research
artifacts did not carry inline evidence labels, and the taxonomy documents and
case JSON still used vocabulary from the removed program (a "Program Charter,"
"registered subjects," "production registries," the `M1`/`M1-O2` identifiers,
`DRAFT_FREEZE_INTENT`, and blind-multi-adjudicator "packet" language).

## Decision

**1. Record the first research artifacts** (evidence labels per `METHOD.md`):

- `studies/h1-k-vs-r/` — H1 structural adjudication. Outcome: **SUPPORTED** —
  Organizations K and R genuinely diverge (all four organization cases differ
  on ≥2 dimensions). **E2**, single-analyst, `[AI-assisted]`.
- `studies/h2-axis-orthogonality/` — H2 axis non-redundancy. Outcome:
  **SUPPORTED** — 10/10 axes have an independent-variation witness, with two
  honest isolation gaps (A1, A10) flagged for a purpose-built case set. **E2**,
  single-analyst, `[AI-assisted]`.
- `impl/` — minimal FMO reference interpreter (append-only, in-memory) with a
  passing test suite covering the invariants, all ten countermodels, the H5
  deletion-scope logic, and the executable H1 discriminator. `[AI-assisted]`.
- `formal/alloy/` — an Alloy encoding of the FMO core for H3 (satisfiability +
  non-entailment checks). `[AI-assisted]`; "faithful to the prose" is a claim a
  human must verify.

**2. Assign evidence labels to the flagship artifacts.** The candidate taxonomy,
formal model, and crosswalk are **E1 (candidate)**; the prior-art survey is
**E0 (exploratory)**; all are `[AI-assisted]`. The FMO, crosswalk, and prior-art
headers now carry these labels inline. The taxonomy document's inline label is
deferred to its next version bump (see point 4).

**3. Read legacy vocabulary as historical.** Where the taxonomy documents or the
case/rule JSON refer to a "Program Charter," "registered subjects,"
"registries," `M1`/`M1-O2`, `DRAFT_FREEZE_INTENT`, or blind-multi-adjudicator
"packets," treat these as historical labels from the removed program. The
operative rules are `METHOD.md`; any "independent adjudication" requirement is
the optional path to **E3**, never a gate on running a study solo.

**4. Do not mutate just-analyzed bytes to fix wording.** The H1/H2 studies pin
the exact SHA-256 of `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md`,
`docs/taxonomy/cases/*.json`, and `category-evaluation-rules.json`. Editing those
files now would invalidate pins recorded in the same batch. The inline label and
vocabulary cleanups for those specific files are therefore deferred to the
taxonomy's next version bump (`v0.1 → v0.2`), when the pins and CHANGELOG update
together. This ADR is the authoritative interim record.

Alternatives considered: rewrite the pinned artifacts now and re-pin every study
(rejected — it invalidates freshly recorded provenance for a wording change, and
the versioning rule exists precisely to avoid silent edits to analyzed bytes).

## Consequences

The repository now contains its first evidence (two E2 findings) plus executable
and formal artifacts, all honestly labeled and capped at E2. Evidence labels are
assigned for every flagship artifact even where one inline edit is deferred. The
next taxonomy version bump carries the deferred inline cleanups. The H1/H2
findings are E2 and invite a second human for E3.
