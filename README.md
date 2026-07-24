# Lifelong Cognitive Memory Research Program (LCMRP)

Research notes on lifelong, human-inspired memory for AI systems — a candidate
vocabulary, a formal model, a prior-art survey, and a set of constructed test
cases for pressure-testing the ideas.

This repository holds working research drafts. Nothing here is a validated
finding or an adopted standard; the documents are falsifiable candidates meant
to be refined, argued with, and revised.

## Contents

- **[Candidate Memory Taxonomy v0.1](docs/taxonomy/MEMORY_TAXONOMY_v0.1.md)** —
  a product-independent vocabulary for machine memory: candidate terms with
  necessary/sufficient conditions, classification axes, observable
  distinctions, and two deliberately competing organizations (kind-first vs.
  role-first) designed to be testable against each other.
- **[Candidate Formal Memory Object Model v0.1](docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md)** —
  FMO-0.1, an abstract typed transition system for memory-object identity,
  lifecycle, time, provenance, authority, conflict, and deletion, with
  invariants, countermodels, and open proof obligations.
- **[Prior Art and Competing Memory Taxonomies](docs/taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md)** —
  a literature synthesis across cognitive-science and machine-memory work
  (CoALA, MemGPT, HippoRAG, Generative Agents, memory taxonomies, and more)
  mapping which distinctions are genuinely operational.
- **[Taxonomy-to-FMO Crosswalk Draft](docs/taxonomy/M1_TAXONOMY_TO_FMO_CROSSWALK_DRAFT_v0.1.md)** —
  a draft mapping between the taxonomy terms and the formal model.
- **[Constructed cases](docs/taxonomy/cases/)** and
  **[category evaluation rules](docs/taxonomy/category-evaluation-rules.json)** —
  positive, negative, and held-out cases plus the coding rules used to test
  whether the taxonomy's distinctions hold up.

- **[Testable hypotheses](docs/HYPOTHESES.md)** — five falsifiable
  propositions (H1–H5) drawn from the taxonomy and formal model, a recommended
  first experiment, and benchmark options.

## How this project works

This is a solo, AI-assisted research effort, and its process is deliberately
lightweight.

- **[Research method](METHOD.md)** — evidence labels, hypothesis discipline,
  reproducibility, and honesty rules, sized for one person.
- **[Contributing](CONTRIBUTING.md)** — how to raise issues, propose changes, or
  (most usefully) replicate and refute a study.
- **[Decision log](docs/decisions/)** — lightweight ADRs recording why choices
  were made.
- **[Changelog](CHANGELOG.md)** — how the repository evolves.

## Scope

This project studies memory mechanisms as research artifacts. Terms borrowed
from biological memory are motivation or analogy, not claims of equivalence,
unless direct evidence supports a stronger relationship.

## License

Licensed under the [MIT License](LICENSE).
