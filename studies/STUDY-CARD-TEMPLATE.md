# Study: <title>

A study is a folder under `studies/<slug>/` with this card as its `README.md`.
The card is both the **preregistration** (fill §1–§4 and commit *before* looking
at results — the commit timestamp locks it) and the **report** (fill §5–§8
after). Amend, don't overwrite: if the plan changes after the pre-analysis
commit, add a dated note in §4 rather than editing the original. See `METHOD.md`
at the repository root.

- **Status:** Planned | Analysis committed | Complete
- **Date planned:** YYYY-MM-DD · **Date completed:** YYYY-MM-DD
- **Hypothesis:** <e.g. H1 from docs/HYPOTHESES.md>
- **Evidence label (target / achieved):** E1 → E2 · `[AI-assisted]` yes/no

## 1. Question

The single falsifiable question this study answers.

## 2. Inputs (pinned)

Exact artifacts and their SHA-256 hashes; tool/model versions used. E.g.
`docs/taxonomy/cases/*.json`, `category-evaluation-rules.json`, and the taxonomy
subject hash they pin.

## 3. Method

What you will do, step by step, precisely enough to reproduce. What counts as a
hit/miss per item. How ambiguity and disagreement are handled. Which part is
**confirmatory** (tests the pre-stated hypothesis) vs **exploratory**
(hypothesis-generating — label it as such wherever it appears).

## 4. What would confirm / refute

The specific result that confirms the hypothesis and the specific result that
refutes it (state the rejection condition). *Amendments (dated) go here.*

<!-- Commit the card up to here BEFORE running the analysis. -->

## 5. Results

Every outcome, including nulls, negatives, and unclassifiable items. Tables where
useful. No result is dropped for weakening the hypothesis.

## 6. Assessment

What the results mean for the hypothesis, and the evidence label you are
claiming. If E2: include the verbatim caveat — "Supported under a preregistered
protocol; single-analyst, not independently replicated." Never claim
"validated/confirmed" from solo work.

## 7. Limitations

What this does not show; threats to validity (e.g. single-adjudicator bias).

## 8. How to replicate or falsify this

Inputs + hashes + procedure, and the specific result that would overturn the
conclusion — so an independent replicator (the path to E3) can act.
