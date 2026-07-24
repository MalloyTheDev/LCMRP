# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); artifact versions
follow [Semantic Versioning](https://semver.org/) (see [`METHOD.md`](METHOD.md)).

This changelog is for humans. Research artifacts carry their own `_vX.Y` version
in their filename and header; this file records how the repository as a whole
evolves.

## [Unreleased]

### Added
- `METHOD.md` — the project's research method: evidence labels (E0–E3 + the
  `[AI-assisted]` tag), preregistration-lite, reproducibility, honesty rules,
  and artifact versioning.
- `docs/HYPOTHESES.md` — five falsifiable hypotheses (H1–H5), a recommended
  first experiment, benchmark options, and the FMO reference-implementation
  sketch.
- `CONTRIBUTING.md` — lightweight contribution and decision model.
- `docs/decisions/` — lightweight Architecture Decision Records, with a
  template and the first two records.
- `studies/STUDY-CARD-TEMPLATE.md` — the preregistration-and-report template for
  running a study (e.g. the H1 first experiment).
- This changelog.

### Changed
- Re-pinned the taxonomy subject hash in `docs/taxonomy/cases/*.json` and
  `category-evaluation-rules.json` to the current bytes, and reframed the
  taxonomy's "independent adjudication" step as the optional path to E3 rather
  than a prerequisite, per `METHOD.md`.

### Removed
- The prior AI-generated governance apparatus (multi-role governance, review
  records, registries, schema/validator tooling, freeze/intake machinery) was
  removed earlier so the repository holds its research content directly. See
  `docs/decisions/0002-adopt-lightweight-research-rules.md`.
