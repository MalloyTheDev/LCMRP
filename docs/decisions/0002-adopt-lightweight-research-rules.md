# 0002. Adopt lightweight, evidence-based research rules

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Maintainer
- **Affects:** repository process; `METHOD.md`, `CONTRIBUTING.md`, `docs/HYPOTHESES.md`

## Context

The repository previously carried an extensive AI-generated governance apparatus
— multi-role governance with quorums and recusal, a chain of adversarial-review
records, immutable registries, and study freeze/intake machinery requiring three
independent human adjudicators. For a solo project this blocked all research
output (no single person can satisfy a three-human independence gate) and buried
the actual research content. It was removed.

That left a gap: without *some* discipline, solo research isn't credible either.
The need was a method sized for one person that still separates planned from
found, grades evidence honestly, discloses AI assistance, and keeps negative
results — grounded in real practice rather than invented process.

## Decision

Adopt a minimal, evidence-based ruleset:

- **`METHOD.md`** — an E0–E3 evidence-label scheme (with an orthogonal
  `[AI-assisted]` tag), preregistration-lite before analysis, cheap
  reproducibility items, honesty rules (retain nulls; cap solo work at E2;
  invite replication), and a SemVer-0.y versioning rule. Grounded in AsPredicted,
  the TOP Guidelines, GRADE, Model Cards/Datasheets, the ML Reproducibility
  Checklist, and ICMJE/Nature AI-disclosure policy.
- **`docs/HYPOTHESES.md`** — five falsifiable hypotheses and a recommended first
  experiment, so the project has concrete evidence targets.
- **`CONTRIBUTING.md`**, **`CHANGELOG.md`**, **`docs/decisions/`** — minimal
  viable governance (BDFL/do-ocracy, Keep a Changelog, ADRs).

Explicitly deferred until a second maintainer exists: `GOVERNANCE.md` and a code
of conduct. Explicitly *not* reintroduced: roles/quorums, mandatory independent
adjudication, freeze/intake machinery, immutable registries.

Alternatives considered: rebuild a formal governance framework (rejected — it's
what failed here); adopt no rules at all (rejected — solo work still needs the
planned-vs-found separation and honest evidence caps to be credible).

## Consequences

The project can now produce research output solo while labeling it honestly.
Provenance is the git commit hash; citation is a git tag plus a DOI at first
release. The rule of admission for any future process: it must make a specific
claim more credible or an output more reproducible for one person, or it stays
out. The next concrete step is running the H1 (K vs R) paper experiment under
these rules.
