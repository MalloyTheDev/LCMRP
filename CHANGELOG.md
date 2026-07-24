# Changelog

All notable changes to this repository are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); artifact versions
follow [Semantic Versioning](https://semver.org/) (see [`METHOD.md`](METHOD.md)).

This changelog is for humans. Research artifacts carry their own `_vX.Y` version
in their filename and header; this file records how the repository as a whole
evolves.

## [Unreleased]

### Added
- `studies/h4-longmemeval-oracle/` — preregistered H4-Oracle study card (the
  reasoning-ceiling step toward H4) plus `convert_longmemeval.py`, a
  LongMemEval→instruction-JSONL converter with a passing self-test, runnable on
  the CorpusStudio eval harness.
- `docs/decisions/0004-*.md` — records LCMRP's relationship to CorpusStudio
  (research arm of the product) and the decision to use its evaluation harness.

### Changed
- README now states the CorpusStudio relationship plainly (research arm;
  findings feed back; independence of evidence, not purpose).

### Added (earlier in this unreleased set)
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
- `studies/h1-k-vs-r/` — first study (H1): Organizations K and R genuinely
  diverge — **SUPPORTED (E2, `[AI-assisted]`)**.
- `studies/h2-axis-orthogonality/` — second study (H2): the ten classification
  axes are non-redundant — **SUPPORTED (E2, `[AI-assisted]`)**, with two
  isolation gaps flagged.
- `impl/` — minimal FMO reference implementation (append-only interpreter) with
  a passing test suite (invariants, all ten countermodels, deletion scope,
  K-vs-R discriminator).
- `formal/alloy/` — Alloy encoding of the FMO core for satisfiability and
  non-entailment checks (H3).
- `.github/` — lightweight issue templates (critique/counterexample, question)
  and a PR checklist.
- `docs/decisions/0003-*.md` — records the first studies, the executable/formal
  artifacts, evidence-label assignment, and the legacy-vocabulary reframe.
- This changelog.

### Changed
- Re-pinned the taxonomy subject hash in `docs/taxonomy/cases/*.json` and
  `category-evaluation-rules.json` to the current bytes, and reframed the
  taxonomy's "independent adjudication" step as the optional path to E3 rather
  than a prerequisite, per `METHOD.md`.
- Added inline evidence labels (E1/E0) and `[AI-assisted]` tags to the formal
  model, crosswalk, and prior-art headers; removed leftover references to the
  deleted Charter/registries; fixed a broken `METHOD.md` cross-reference; and
  aligned the `CITATION.cff` abstract with the README's falsifiable-draft framing.

### Removed
- The prior AI-generated governance apparatus (multi-role governance, review
  records, registries, schema/validator tooling, freeze/intake machinery) was
  removed earlier so the repository holds its research content directly. See
  `docs/decisions/0002-adopt-lightweight-research-rules.md`.
