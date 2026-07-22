# Non-evidentiary examples

Files in this directory demonstrate schema shape and validator behavior. They are synthetic fixtures, not completed experiments, research findings, terminal study closeouts, measured results, registered subjects or mechanisms, replications, or evidence for any scientific claim.

An example must use conspicuous placeholder identifiers and must not be copied into a registry without replacing every placeholder, performing the declared work, and recording traceable artifacts. The foundational finding fixture preserves an intentional `NOT_RUN` disposition; it does not imply that an analysis was executed. The closeout fixture is `DRAFT` with a pending completeness assertion and therefore is not a terminal declaration.

Files under `examples/fixtures/` are digestable inputs used to test exact artifact binding. Their contents explicitly identify them as synthetic and non-evidentiary.

The foundational execution-intake and intake-receipt examples demonstrate the external digest-receipt binding shape only. The solo intake example demonstrates the solo-human + AI-tooling disclosure shape. They do not appoint real adjudicators, create a live study intake, or authorize taxonomy execution.

## M1 synthetic contract dry runs

The [`m1-dry-runs/`](m1-dry-runs/) directory contains two isolated, end-to-end fixture families:

- [`taxonomy/`](m1-dry-runs/taxonomy/) exercises the `STRUCTURAL_OR_TAXONOMY_EVALUATION` path, including one intentionally `NOT_RUN` analysis.
- [`formal-analysis/`](m1-dry-runs/formal-analysis/) exercises the `FORMAL_ANALYSIS` path over a deliberately trivial two-atom system that is not FMO-0.1.

Their local `ACTIVE`, `FROZEN`, `PUBLISHED`, and `COMPLETED` values demonstrate serialization and lifecycle checks only. The bundle-local indexes are not production registries, and their outcomes must not be cited as research findings, independent validation, candidate adoption, or mechanism evidence.
