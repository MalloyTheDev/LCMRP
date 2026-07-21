# M1 synthetic contract dry runs

**Artifact classification:** Program infrastructure supporting Layer 1 — Foundational Research  
**Status:** `SYNTHETIC-DRY-RUN` / `NON-EVIDENTIARY`  
**Production registry effect:** None

These isolated fixture families exercise the accepted foundational-study contracts before any real M1 subject or study is registered:

- [Taxonomy dry run](taxonomy/) exercises `STRUCTURAL_OR_TAXONOMY_EVALUATION` using constructed cases, one serialization-only `COMPLETED` disposition, and one explicit `NOT_RUN` disposition.
- [Formal-analysis dry run](formal-analysis/) exercises `FORMAL_ANALYSIS` using a deliberately trivial two-atom propositional system and a complete four-valuation replay.

Each bundle contains local example identities, records, indexes, reports, and a native validator. Those local lifecycle states do not populate the production registries. Passing a bundle demonstrates only internal serialization, digest, identity, and closeout behavior; it does not establish taxonomy quality, formal-model correctness, a research finding, replication, independent validation, candidate adoption, mechanism evidence, implementation readiness, or M1 completion.

The separate [adversarial review](../../reviews/M1_DRY_RUN_ADVERSARIAL_REVIEW_2026-07-21.md) and [final decision](../../reviews/M1_DRY_RUN_DECISION_2026-07-21.md) record the mutation coverage, limitations, and acceptance boundary.
