# Research Method

How this project produces trustworthy work as a solo, AI-assisted effort. The
rules are deliberately lightweight: each one exists to make a claim more
credible or an output more reproducible for *one person*. Anything that only
coordinates people who don't exist here is left out on purpose.

The guiding sources are linked inline; this file adapts their *principles*, not
their institutional machinery.

## 1. Evidence labels

Every substantive claim carries one label. Default new material to the lowest
applicable label; moving up requires stated, checkable grounds (grade down by
default, up only on evidence — the [GRADE](https://www.gradeworkinggroup.org/)
logic). The labels also track *verification status* in the tiered spirit of the
[TOP Guidelines](https://www.cos.io/initiatives/top-guidelines) (disclosed →
shared → independently verified). The top rung is the only one the author cannot
grant themselves.

| Label | Meaning | What you may claim |
|---|---|---|
| **E0 — Exploratory** | A pattern or idea noticed *while looking at* material; no pre-stated hypothesis. | "Suggests / may indicate / worth testing." Generates hypotheses only. |
| **E1 — Candidate** | A defined, falsifiable proposal with conditions and rejection criteria, not yet tested against the frozen cases. *The taxonomy and FMO sit here.* | "Proposed / candidate." States commitments. No claim of support. |
| **E2 — Supported (solo, preregistered)** | A confirmatory result from a plan committed *before* analysis, run against the frozen cases, with all outcomes (including nulls) reported; checked only by the author. | "Supported under a preregistered protocol; single-analyst, not independently replicated" — that caveat, verbatim. Never "validated/confirmed." |
| **E3 — Independently corroborated** | E2 plus at least one replication or adjudication by a person who is not the author and whose work is not AI-only. | May drop the solo caveat. **The author may never self-assign E3.** |

**`[AI-assisted]`** is an orthogonal tag, not a level. Apply it to any artifact
an AI materially drafted, mapped, or coded. AI is never an author, and an AI
review never lifts E2 → E3 ([ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/),
[Nature](https://www.nature.com/nature-portfolio/editorial-policies/ai)).

## 2. Hypothesis discipline (preregistration-lite)

1. **Pre-plan before analysis.** Before evaluating anything against the frozen
   or held-out cases, commit a short plan — adapted from the
   [AsPredicted](https://osf.io/m3spx/) 9-question format: the question, what
   counts as a hit/miss per term, which cases, how ambiguity is handled, what
   would falsify the hypothesis, and what is exploratory. The git commit
   timestamp *is* the preregistration. In practice this plan is §1–§4 of a study
   card (§3.6); the card becomes the report when you add results — it is one
   document written at two times, not two artifacts.
2. **Amend, don't overwrite.** If the plan changes after it's committed, add a
   dated "Amendment" note saying what changed and why. A superseded plan stays
   visible (same spirit as the `@version` term IDs).
3. **Label confirmatory vs exploratory** inline, always. Anything not in the
   pre-committed plan is "exploratory / hypothesis-generating" and may motivate
   a future test but may not be reported as support
   ([Kimmelman et al. 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4028181/)).

## 3. Reproducibility

Adapted from the [ML Reproducibility Checklist](https://arxiv.org/abs/2003.12206)
and the [Model Card](https://arxiv.org/abs/1810.03993) /
[Datasheet](https://arxiv.org/abs/1803.09010) pattern — keep the cheap,
high-value items:

4. **Pin inputs.** Each study names the exact bytes it analyzes (e.g. a file's
   SHA-256), the tool/model versions used, and one documented command or
   step-list that regenerates every reported output.
5. **Keep the case sets frozen; keep the held-out set held out.** Do not consult
   held-out cases until the confirmatory pass, and never edit a case or
   definition *in response to* a coding difficulty seen after freeze — record
   the difficulty as a finding instead.
6. **One-page study card.** Each study is a folder under `studies/<slug>/` with
   one study-card `README.md` (template:
   [`studies/STUDY-CARD-TEMPLATE.md`](studies/STUDY-CARD-TEMPLATE.md)) recording:
   question, inputs + hashes, method, confirmatory-vs-exploratory split, results
   (including nulls), evidence label, `[AI-assisted]` disclosure, limitations,
   and "how to falsify this."

## 4. Honesty rules

7. **Retain every outcome.** Null, negative, superseded, rejected, and
   unclassifiable results are kept, not dropped. A study that fails to support
   its hypothesis is a completed study
   ([Rosenthal 1979](https://pages.ucsd.edu/~cmckenzie/Rosenthal1979PsychBulletin.pdf)).
8. **Solo work is capped at E2.** No artifact authored and checked only by the
   maintainer (with or without AI) may claim "validated," "confirmed," or
   "independently corroborated."
9. **Invite replication.** Each study ends with a short "how to replicate or
   falsify this" note, so the missing external reviewer is invited rather than
   faked.

## 5. Versioning

Artifacts use [Semantic Versioning](https://semver.org/) semantics and stay
honest about maturity:

- We are in **0.y**: anything may change at any time; there are no stability
  guarantees. Staying at 0.y is the correct signal for a falsifiable draft.
- Bump the **minor** (`0.1 → 0.2`) on any substantive revision; record it in
  [`CHANGELOG.md`](CHANGELOG.md) and, if it reflects a real decision, an ADR in
  [`docs/decisions/`](docs/decisions/).
- Reserve **1.0.0** for an artifact you are prepared to call stable.
- A public snapshot is a git **tag**; to make a release independently citable,
  enable the [GitHub–Zenodo integration](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content),
  which mints a DOI per release and reads [`CITATION.cff`](CITATION.cff).

## What this project deliberately does *not* do

No multi-role committees, quorums, or "independent adjudicator" *requirements*;
no freeze/intake/guard machinery; no immutable registries or mandatory sign-off
gates. A solo project cannot staff those, so such rules either block all work or
get satisfied by pretending an AI is "independent" — which is worse than an
honest single-analyst label. Provenance is the git commit hash; a citable
snapshot is a git tag (plus a DOI at first release). The honest solo cap (§4)
and the invitation to replicate (§9) replace the committee that isn't here.

Where an existing research artifact still says a study should use "independent
adjudication" (e.g. the taxonomy's recommended falsification step), read that as
the optional path to **E3**, not a gate on doing the work: a solo analyst runs
the study to **E2** now, and independent adjudication is what a second person
later adds to reach E3.
