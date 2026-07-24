# Contributing

This is a small, solo-maintained research repository. Decisions are made by the
maintainer (a [BDFL / do-ocracy](https://opensource.guide/leadership-and-governance/)
model); proposals pass by lazy consensus when no one objects. There is no
committee, quorum, or sign-off gate — see [`METHOD.md`](METHOD.md) for why the
process is intentionally minimal.

## How to raise something

- **Found a problem with an artifact?** Open an issue naming the artifact and
  version, what's wrong, and (if you have one) a proposed change. A concrete
  counterexample to a candidate definition or a countermodel to the formal model
  is especially welcome — this project *wants* to be falsified.
- **Have a question?** Open an issue.
- **Want to propose a change?** Open a pull request. Small, focused changes are
  easier to accept.

## Ground rules for changes

- **Artifacts are versioned drafts.** Substantive revisions bump the minor
  version (`0.1 → 0.2`) and are recorded in [`CHANGELOG.md`](CHANGELOG.md). See
  the versioning rule in [`METHOD.md`](METHOD.md).
- **Real decisions get an ADR.** If a change reflects a decision (adopting,
  rejecting, or superseding an approach), add a short record in
  [`docs/decisions/`](docs/decisions/).
- **Claims carry evidence labels and disclose AI assistance**, per
  [`METHOD.md`](METHOD.md). Don't label solo, AI-assisted work as "validated" or
  "independently corroborated."
- **Keep negative and null results.** They're part of the record, not failures
  to hide.

## Replication

The fastest way to help is to replicate or refute a study: follow its "how to
falsify this" note, run it independently, and report what you find. Independent
corroboration is the one thing the solo maintainer cannot produce alone.
