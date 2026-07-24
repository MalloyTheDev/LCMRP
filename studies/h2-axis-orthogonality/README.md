# Study: H2 — Classification axes A1–A10 are non-redundant

A study is a folder under `studies/<slug>/` with this card as its `README.md`.
The card is both the **preregistration** (§1–§4, written to stand alone before
looking at results) and the **report** (§5–§8, added after). Amend, don't
overwrite: plan changes after the pre-analysis boundary go in dated notes in §4.
See [`METHOD.md`](../../METHOD.md).

- **Status:** Complete
- **Date planned:** 2026-07-24 · **Date completed:** 2026-07-24
- **Hypothesis:** H2 — "The classification axes are non-redundant" ([`docs/HYPOTHESES.md`](../../docs/HYPOTHESES.md))
- **Evidence label (target / achieved):** E1 → **E2** · `[AI-assisted]` **yes**

> **`[AI-assisted]`** — The axis coding, the witness search, and this card were
> materially drafted by an AI assistant (Claude, Opus 4.8) under single-analyst
> direction. Per [`METHOD.md`](../../METHOD.md) §1, AI is never an author and an
> AI pass never lifts E2 → E3. This study is capped at E2.

---

## 1. Question

For the candidate taxonomy's ten orthogonal classification axes **A1–A10**
(defined in [`docs/taxonomy/MEMORY_TAXONOMY_v0.1.md`](../../docs/taxonomy/MEMORY_TAXONOMY_v0.1.md),
"Orthogonal classification axes"), does **each axis carry information not derivable
from the other nine** — i.e., does each axis have at least one *witness* in the
frozen constructed case set: a case (or minimal case pair) in which that axis
takes a distinguishing value while the axes it is most at risk of collapsing into
are held fixed?

This is the taxonomy's own stated rejection condition, in the affirmative: the
taxonomy must be superseded in part if "one axis logically determines another
despite the claimed orthogonality"
([`MEMORY_TAXONOMY_v0.1.md`](../../docs/taxonomy/MEMORY_TAXONOMY_v0.1.md),
"Rejection conditions"). H2 asks whether that condition is *avoided* for all ten.

## 2. Inputs (pinned)

Exact bytes analyzed, by SHA-256 (computed 2026-07-24 with `sha256sum`, GNU
coreutils):

| File | Role | SHA-256 |
|---|---|---|
| `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md` | Subject: defines axes A1–A10 | `77ff4468d2164c9cdf61dba42287e5a9fbfe41e3ab8e920542d8811e06e95f7b` |
| `docs/taxonomy/cases/positive-cases.json` | Case set (20 positive) | `be51f9d77b6652760e49fa8908e03f6d289612867549295ffd10897ab7b7e607` |
| `docs/taxonomy/cases/negative-cases.json` | Case set (12 negative) | `df2d0120ab777dcfb6b49530d7d7548bf270f4803a9a0e9991eeafef6e3ec71d` |
| `docs/taxonomy/cases/held-out-cases.json` | Case set (16 held-out) | `1aef47de0110cab90cc44a06886fb3bd1d581f5169e8fc32100719d4ff596335` |
| `docs/HYPOTHESES.md` | H2 statement | `d83cc24b7dbcee75c2c511f796e97eda03d84f71fceb62d88d3af93cab37d05a` |
| `studies/STUDY-CARD-TEMPLATE.md` | Card template | `a9f262c3af7952fa8c3ce33d7b894eddd7c861097b153dbbfeb7a65d66dd0ca2` |
| `METHOD.md` | Method rules | `4afafa8adaf3b07253bee3668a003e3b0214fcaeef22b11a1d576a9251dd51c5` |

**Subject-binding check (confirmatory prerequisite):** the taxonomy file's own
digest `77ff…5f7b` equals the `subject_binding.raw_byte_sha256` recorded inside
all three case files. The cases therefore pin exactly this taxonomy version; the
axis definitions coded below are the frozen ones. Recorded, not assumed.

- **Tool/model versions:** analysis and drafting by Claude (Opus 4.8, model id
  `claude-opus-4-8`), single session, 2026-07-24. Hashing: `sha256sum`
  (coreutils). No other tooling; no code was executed against the cases (paper
  exercise, as H2 anticipates).

## 3. Method

### 3.1 Scope of the case set used

All three frozen case files are read. The positive set supplies the primary
witnesses because its cases are *minimal controlled pairs* — each POS case varies
one declared observable distinction while holding a shared context fixed, which
is exactly the structure an axis-independence witness needs. Held-out cases are
used as corroborating/secondary witnesses. **Held-out honesty:** these bytes are
consulted only to *report* whether they corroborate; no method rule, witness
criterion, or verdict in §3–§4 is revised in response to them
([`METHOD.md`](../../METHOD.md) §5).

### 3.2 Axis coding

For each axis A1–A10, I record the distinct values the axis takes across the
corpus and identify the case(s)/facts exhibiting them. Axis definitions and
candidate value lists are taken verbatim from the taxonomy's "Orthogonal
classification axes" table. An "item" is a single fact/object described in a case
(cases often describe a controlled pair of items).

### 3.3 Witness criterion (the confirmatory test)

Axis **Ak** has an **independent-variation witness** iff the corpus contains two
items I, J with:

1. **(distinguishing values)** Ak(I) ≠ Ak(J) — the axis takes two different
   declared values; **and**
2. **(not a relabeling)** at least the axis (or axes) Ak is *most at risk of
   collapsing into* is held equal across I and J — so the change in Ak is not a
   mere renaming of a neighbour axis's change. The at-risk partner axes are
   pre-named per axis in §3.5 below.

**Witness strength** is graded and reported, not hidden:

- **STRONG** — a single minimal pair (ideally within one constructed case, or two
  cases matched on several axes) flips Ak while the neighbour axis/axes and most
  others are held fixed.
- **MODERATE** — Ak varies against a fixed at-risk neighbour, but the two items
  also differ on axes beyond that neighbour (partial isolation).
- **PARTIAL** — Ak demonstrably varies and is not a function of the named
  neighbour, but no case controls the isolation cleanly; the co-varying axes are
  named as a **gap**.
- **NONE (null)** — no witness: Ak is constant across the whole corpus, or every
  change in Ak co-occurs with a perfect 1:1 change in one single other axis
  across *all* cases. This is the refute signal for that axis.

Ambiguity handling: where an item's axis value is arguable, the more conservative
coding (the one *less* favourable to finding a witness) is used, and the
alternative is noted. A witness that survives only under a generous coding is
downgraded one strength grade.

### 3.4 Confirmatory vs exploratory

- **Confirmatory** (tests H2): §3.3 applied to all ten axes; the confirm/refute
  rule in §4.
- **Exploratory** (hypothesis-generating, labelled inline in §5): observations
  about *which pairs of axes* are hardest to separate, and proposals for
  purpose-built ablation cases. These may motivate future cases but are not
  reported as support for H2.

### 3.5 Pre-named at-risk neighbour axes (fixed before coding)

The taxonomy's own "why not reducible" column and its rejection conditions flag
these collapse risks; I pin them now so the "not a relabeling" test in §3.3(2) is
not chosen after seeing results:

- **A1** (representational kind) at risk of collapsing into **A2** (functional
  role) and/or **A9** (derivation form).
- **A2** (functional role) at risk of collapsing into **A1**.
- **A3** (temporal orientation) at risk of collapsing into **A2** (prospective
  role vs prospective time).
- **A4** (lifecycle state) at risk of collapsing into **A8** (availability) —
  both list *archived*, *deletion pending*.
- **A5** (epistemic posture) at risk of collapsing into **A4** (admission).
- **A6** (provenance condition) at risk of collapsing into **A9** (derivation
  form) — both describe lineage.
- **A7** (authority relation) at risk of collapsing into actor identity (a
  non-axis property).
- **A8** (availability/persistence) at risk of collapsing into **A4**.
- **A9** (derivation form) at risk of collapsing into **A6**.
- **A10** (sensitivity/handling) at risk of collapsing into **A7** (authority)
  and/or the representational/functional family (A1/A2).

## 4. What would confirm / refute

- **Confirms H2:** *every* axis A1–A10 has at least one independent-variation
  witness (STRONG, MODERATE, or PARTIAL) under §3.3 — no axis is fully determined
  by the other nine across the corpus.
- **Refutes H2:** *some* axis has **NONE** — it is constant across the whole
  corpus, or its every change is a perfect 1:1 relabeling of one single other
  axis across all cases (→ derivable → that axis should be **dropped or merged**,
  the taxonomy's stated rejection condition "one axis logically determines
  another").
- **Partial outcome reported, not rounded:** an axis whose only witness is PARTIAL
  is counted toward "confirm" (it is not fully determined) **but** is flagged as a
  gap requiring a purpose-built control. The verdict states the count of STRONG /
  MODERATE / PARTIAL separately so a reader is not told a clean result was
  obtained where it was not.

**Preregistration boundary (honesty note):** this card is written in a single
session; §1–§4 were fixed as the plan before the §5 axis table was coded, and are
not revised in light of it. Unlike a git-timestamped two-commit preregistration
([`METHOD.md`](../../METHOD.md) §2), a single session cannot *prove* the plan
preceded the analysis. This is a real limitation of solo, single-sitting work and
is carried into §7; it does not license relaxing the §3.3 criterion.

<!-- ============================================================= -->
<!-- PLAN ENDS (preregistration, §1–§4) · RESULTS BEGIN (§5–§8)    -->
<!-- ============================================================= -->

## 5. Results

### 5.1 Axis-value coding (evidence base)

Distinct declared values found per axis, with the case items exhibiting them
(POS = positive, HOLD = held-out; item labels are the objects named in the case
facts):

| Axis | Distinct values seen in corpus | Example items |
|---|---|---|
| A1 Representational kind | claim, procedure-like constraint, policy, event trace, provenance assertion, composite | POS-016 (claim), POS-018/O181 (procedure), HOLD-004 (policy), POS-019 visit link (event trace), POS-015/T15 (provenance assertion), HOLD-002 (composite) |
| A2 Functional role | episodic, semantic, procedural, prospective, working, multiple | POS-019 (episodic↔semantic), POS-018 (procedural/prospective), POS-020 (working), HOLD-002 (multiple) |
| A3 Temporal orientation | retrospective, presently active, prospective, atemporal; validity time varying | POS-018/O181 (atemporal) vs O182 (prospective); POS-016 (validity intervals); HOLD-006 (temporal reversal) |
| A4 Lifecycle state | candidate, rejected, admitted/active, superseded, archived, deletion pending, deleted | POS-001 (candidate→rejected), POS-002 (admitted), POS-005 (superseded), POS-012 (archived vs deleted) |
| A5 Epistemic posture | asserted, unresolved, challenged, conflicted; confidence & uncertainty separate | POS-002 (unresolved), POS-013 (confidence⊥correctness), POS-014 (uncertainty vs low confidence), POS-015 (challenged) |
| A6 Provenance condition | source-linked, derived, consolidated, disputed | POS-015 (connected vs disputed/forged), POS-006 (consolidated/derived), HOLD-005 (different sources) |
| A7 Authority relation | permitted, denied, obligated, contested, expired, unknown | POS-017 (permitted-to-archive, not-to-delete, expired), HOLD-007 (contested), HOLD-010 (denied) |
| A8 Availability & persistence | active, suppressed, low-priority, archived, deletion pending, verified within scope; persistent vs task-local | POS-009 (priority 0.8→0.5), POS-010/011/012 (suppressed/archived/deleted), POS-020 (durable vs task-local) |
| A9 Derivation form | direct encoding, successor update, consolidation, abstraction, reconsolidation, imported copy | POS-005 (successor update), POS-006 (consolidation vs abstraction), POS-007 (update vs reconsolidation), HOLD-012 (imported copy) |
| A10 Sensitivity & handling | public/unstated, restricted, sensitive, disputed | HOLD-008 (sensitive), HOLD-005 (differing consent/handling), POS-015/HOLD-014 (disputed) |

Every axis takes ≥ 2 distinct declared values across the corpus, so no axis is
refuted by constancy.

### 5.2 Witness per axis

| Axis | Witness (pair) | At-risk neighbour held fixed | Strength | Notes |
|---|---|---|---|---|
| **A1** Representational kind | POS-018/O181 (procedure) vs HOLD-004 (policy) | **A2 = procedural** and **A9 = direct encoding**, A4 = admitted, all held equal | **MODERATE** | A1 differs (procedure vs policy) at equal (A2, A9) ⇒ A1 ≠ f(A2, A9). Corroborated: HOLD-002 (composite) and POS-019 (claim) both reach A2 = multiple ⇒ A1 ≠ f(A2). No single case flips *only* A1 → see gap G1. |
| **A2** Functional role | POS-019: one unchanged object, task T191 (semantic) vs T192 (episodic) | **A1 = claim**, content, A4, A6, A9 all fixed — only the query varies | **STRONG** | Cleanest isolation in the set: the only thing that changes is the (non-axis) query, and the role flips. Directly answers competency Q1. |
| **A3** Temporal orientation | POS-016: C161 (valid 08:00–09:00) vs C162 (valid 10:00–11:00) | **A2 = semantic**, A1 = claim held fixed | **MODERATE** | Validity-time (A3) varies with functional role fixed ⇒ A3 ≠ f(A2). POS-018 (atemporal vs prospective) is a second witness but there A2 co-varies. |
| **A4** Lifecycle state | POS-005: V1 becomes **superseded yet remains referencable/available** | **A8 = available/active** held fixed | **STRONG** | A4 = superseded while A8 = available ⇒ A4 ≠ f(A8). Resolves the A4/A8 collapse risk together with the A8 witness below. |
| **A5** Epistemic posture | POS-013: C131 conf 0.95 & false vs C132 conf 0.25 & true | **A4 = admitted**, A1 = claim held fixed | **STRONG** | Epistemic posture/confidence varies while lifecycle fixed and independent of stipulated correctness. POS-002 (admitted but unresolved) is a second STRONG witness for A5 ≠ f(A4). |
| **A6** Provenance condition | POS-015: connected attributed trace vs a challenged/forged edge | content & object fixed; and POS-006 varies **A9** while **A6 = derived** stays fixed | **STRONG** | Two-way separation from A9: POS-006/007 flip A9 (consolidation/abstraction/reconsolidation) at fixed A6 = derived; POS-015 flips A6 (source-linked→disputed) at fixed derivation. Resolves the A6/A9 collapse risk. |
| **A7** Authority relation | POS-017: same actor A17 — permitted to archive class X (day 1–30), **not** permitted to delete / other purpose / after day 30 | **actor identity fixed** (the pre-named at-risk non-axis) | **STRONG** | Authority varies by operation/purpose/time with actor constant ⇒ A7 ≠ f(actor). Answers competency Q9. |
| **A8** Availability & persistence | POS-009: priority 0.8→0.5 while claim & admission unchanged; and POS-020: durable vs task-local at equal working role | **A4 = active** held fixed (POS-009); **A2 = working** fixed (POS-020) | **STRONG** | A8 varies at fixed A4 ⇒ A8 ≠ f(A4). With POS-005 (A4 varies at fixed A8) this is a clean two-way separation of A4 and A8. |
| **A9** Derivation form | POS-007: changed successor **without** prior retrieval (update) vs comparable successor **with** logged retrieval + new context (reconsolidation) | **A6 = derived** held fixed; content-change held comparable | **STRONG** | Sole controlled difference is the causal-retrieval record. POS-006 (consolidation vs abstraction) and POS-005 (successor update) are further witnesses at fixed A6. |
| **A10** Sensitivity & handling | HOLD-008 (sensitive clinic-attendance content, deletion-scoped) vs POS-012 (deletion-scoped, sensitivity unstated); and HOLD-005 (byte-identical claims, differing consent/handling) | representational/functional/epistemic family (A1/A2/A3/A5) held fixed in HOLD-005 (byte-identical) | **PARTIAL** | A10 differs while the memory-function family is fixed ⇒ A10 ≠ f(A1,A2,A3,A5). **But** in HOLD-005 A10 co-varies with A6/A7/A8 (the whole governance bundle changes together); no case isolates sensitivity from authority/provenance → see gap G2. |

### 5.3 Outcome tally

- Axes with an independent-variation witness: **10 / 10**.
- By strength (totals to 10): **STRONG = 7** (A2, A4, A5, A6, A7, A8, A9),
  **MODERATE = 2** (A1, A3), **PARTIAL = 1** (A10).
- Axes with **NONE / null**: **0**. No axis is constant across the corpus, and no
  axis's variation is a perfect 1:1 relabeling of a single other axis.

### 5.4 Gaps (nulls-of-isolation, reported honestly)

These are not refutations (no axis is fully determined), but real weaknesses in
how cleanly the *existing* case set isolates two axes:

- **G1 — A1 (representational kind) has no single-case control.** The witness is
  assembled from two cases (POS-018 vs HOLD-004) rather than one minimal pair that
  flips only representational kind while holding everything else. The corpus was
  built around the 20 observable distinctions (DIST-01…20), none of which is "hold
  role/lifecycle/provenance fixed, vary representational kind." So A1's
  non-redundancy rests on a *constructed* cross-case comparison, weaker than the
  within-case controls the other axes enjoy.
- **G2 — A10 (sensitivity/handling) never varies alone.** In every case where
  sensitivity changes, at least one of A6/A7/A8 changes with it (governance
  facts travel as a bundle: source + consent + authority + retention + handling).
  So while A10 is clearly not a function of the *memory-function* axes, the corpus
  cannot rule out that A10 is, within the governance family, partly redundant with
  A7 (authority) or A6 (provenance). This is the residual collapse risk H2 most
  needs a purpose-built case to close.

### 5.5 Exploratory observations (hypothesis-generating; NOT support for H2)

- The two axis pairs the taxonomy pre-flagged as highest collapse risk —
  **A4/A8** (lifecycle vs availability) and **A6/A9** (provenance vs derivation) —
  are the ones the case set *does* cleanly separate, in both directions (POS-005 +
  POS-009 for A4/A8; POS-006/007 + POS-015 for A6/A9). The residual risk instead
  sits with **A1** and **A10**, which the case authors did not build controlled
  pairs for. Exploratory hypothesis: a follow-up "axis-ablation" case file with
  one minimal pair per axis (flip only Ak) would upgrade A1 and A10 to STRONG or
  expose a genuine A10↔A7 redundancy. This motivates new cases; it is not itself
  evidence for or against H2.

## 6. Assessment

Under the preregistered §3.3 criterion and §4 rule, **H2 is supported**: all ten
axes A1–A10 have at least one independent-variation witness in the frozen case
set, and **no axis is fully determined by the other nine** across the corpus —
the taxonomy's "one axis logically determines another" rejection condition is
**not** triggered. Seven axes have STRONG (single-pair, well-isolated) witnesses;
A1 and A3 are MODERATE; A10 is PARTIAL with a documented isolation gap.

**Evidence label: E2 (Supported).** Verbatim caveat, as required by
[`METHOD.md`](../../METHOD.md) §1/§4:

> **Supported under a preregistered protocol; single-analyst, not independently
> replicated.**

This is **not** a claim that the taxonomy is validated, adopted, correct, or
complete. It establishes only that, on this frozen constructed set and under this
one coding, each axis carries information the others do not fully carry — a
structural property, not external validity. The taxonomy remains an **E1
candidate**; H2 clearing E2 does not promote it.

## 7. Limitations

- **Single-analyst, AI-assisted coding.** The axis-value table (§5.1) and every
  witness pairing were produced by one analyst with AI assistance. Axis coding of
  natural-language cases is interpretation-laden; a second coder could assign
  different values and collapse a witness. This is the dominant threat and the
  reason the study is capped at E2 (no self-assigned E3).
- **Preregistration is single-session.** As noted in §4, the plan/analysis split
  is logical, not git-timestamped across two commits; the plan's temporal priority
  cannot be independently verified from this artifact alone.
- **The case set was not built for axis-ablation.** It was constructed around 20
  observable distinctions and 12 integrity constraints, not around "flip exactly
  one axis." Hence the within-case controls happen to isolate some axes cleanly
  (A2, A4–A9) and leave others (A1, A10) only cross-case or bundled — gaps G1/G2.
  A negative reading of those gaps cannot be excluded by this set alone.
- **Weaker than full logical ablation.** H2's ideal test (H2 in
  [`docs/HYPOTHESES.md`](../../docs/HYPOTHESES.md)) is "predict each axis from the
  other nine; redundant iff perfectly predictable." With ~48 hand-coded items and
  no two sharing an identical other-nine tuple, a literal
  "not-a-function-of-all-nine" proof is unavailable; §3.3 substitutes the weaker
  "not a relabeling of the at-risk neighbour(s)." Confirmation is therefore of the
  weaker claim.
- **Held-out set used only for corroboration.** Held-out cases informed no method
  or verdict change, but they were read; a purist might prefer they be untouched
  until a later confirmatory pass. Their use here is limited to secondary
  witnesses and is disclosed.
- **No claim beyond structure.** Nothing here speaks to whether the axes are
  useful, exhaustive, biologically grounded, or implementable.

## 8. How to replicate or falsify this

**Replicate (paper exercise, ~half a day):**

1. Fetch the seven files in §2 and verify each SHA-256 with `sha256sum`
   (coreutils). Confirm the taxonomy digest equals
   `subject_binding.raw_byte_sha256` in each case file.
2. Read the "Orthogonal classification axes" table in the taxonomy and the case
   `facts`. Re-code §5.1 independently.
3. Apply the §3.3 witness criterion to each axis using the §3.5 at-risk pairings.
   Grade each witness STRONG / MODERATE / PARTIAL / NONE.
4. You reproduce the conclusion if you find ≥ 1 witness for all ten axes and no
   axis is constant or a 1:1 relabeling.

**Falsify / overturn (the specific results that would break each verdict):**

- **Overturn a witness:** show that the two items in any §5.2 pair actually share
  the *same* value on the axis claimed to differ (the coding was wrong), or that
  the at-risk neighbour was *not* in fact held fixed. If this collapses any axis
  to NONE, H2 is refuted and that axis should be dropped or merged.
- **Refute via ablation (strongest path, needs a new case file):** build
  `docs/taxonomy/cases/axis-ablation-cases.json` with, for each axis, one minimal
  pair identical on the other nine axes and differing only on that axis. If any
  axis **cannot** be so constructed — i.e., flipping it forces a co-flip of
  another axis in every attempt — that axis is derivable and H2 is refuted for it.
  This directly closes gaps **G1 (A1)** and **G2 (A10)**: an A10 pair holding
  A6/A7/A8 fixed while varying only sensitivity would upgrade A10 to STRONG; if no
  such pair exists, A10↔{A6,A7} redundancy is demonstrated.
- **Independent adjudication (path to E3):** a second coder, not the author and
  not AI-only, re-runs steps 2–4 blind to this card's witness table. Agreement on
  all ten verdicts corroborates; a disagreement that turns any axis to NONE
  refutes. Per [`METHOD.md`](../../METHOD.md) §1, only this step can lift the
  result above E2.
