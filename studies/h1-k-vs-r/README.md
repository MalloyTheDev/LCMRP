# Study: H1 — Do Organizations K and R genuinely diverge?

A study folder under `studies/h1-k-vs-r/` with this card as its `README.md`. Per
[`METHOD.md`](../../METHOD.md) §2 and §3.6, this card is **both** the
preregistration (§1–§4, committed *before* the analysis so the git timestamp
locks the plan) **and** the report (§5–§8, added afterward). Amendments are
dated and appended in §4; the original plan is never overwritten.

- **Status:** Complete
- **Date planned:** 2026-07-24 · **Date completed:** 2026-07-24
- **Hypothesis:** H1 — "Organizations K and R genuinely diverge" ([`docs/HYPOTHESES.md`](../../docs/HYPOTHESES.md))
- **Evidence label (target / achieved):** E1 → **E2** · `[AI-assisted]` **yes**
- **AI-assisted disclosure:** The four case encodings, the divergence tabulation,
  and this card were materially drafted and coded by an AI assistant
  (Claude, model `claude-opus-4-8`) under the direction and review of the single
  human maintainer. Per METHOD.md §1, AI is not an author and an AI pass never
  lifts E2 → E3.

---

## 1. Question

Is there at least one constructed organization-competition case for which the two
candidate primary organizations of the memory taxonomy — **K** (stable
kind-first partition) and **R** (contextual role-first relation) — are *forced by
their own frozen coding commitments* to different structural outcomes on
identity, classification cardinality, required context, WORKING treatment, or
composite handling, such that the divergence is a consequence of the
organizations' commitments and not of case wording?

This is the taxonomy's own rejection test (MEMORY_TAXONOMY_v0.1 §"Why the
organizations genuinely compete" and §"Rejection conditions": *"If later
evaluation finds no case for which the organizations require different identity,
cardinality, or classification outcomes, M1-O2 must be rejected and the
organizations collapsed or reformulated."*). The study does **not** ask which
organization is better; a K-or-R superiority verdict is out of scope and
forbidden by the plan (see §3).

## 2. Inputs (pinned)

All bytes analyzed are pinned by SHA-256 (GNU coreutils `sha256sum` 9.4).

| Artifact | Path | SHA-256 |
|---|---|---|
| Held-out organization cases | `docs/taxonomy/cases/held-out-cases.json` | `1aef47de0110cab90cc44a06886fb3bd1d581f5169e8fc32100719d4ff596335` |
| Category evaluation rules (coding rubric) | `docs/taxonomy/category-evaluation-rules.json` | `6868d5c3dc3c1c98081af1e86145394129c5bc77ddfe8014ecab684561e1aa31` |
| Candidate taxonomy (subject) | `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md` | `77ff4468d2164c9cdf61dba42287e5a9fbfe41e3ab8e920542d8811e06e95f7b` |

**Subject binding check (integrity constraint IC-01).** Both the cases file
(`subject_binding.raw_byte_sha256`) and the rules file
(`subject_binding.raw_byte_sha256`) pin the taxonomy subject digest
`77ff4468…95f7b`. The computed digest of `MEMORY_TAXONOMY_v0.1.md` equals that
value, so the coding rules and cases bind the exact subject version analyzed
here. Subject: `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY` v1.

**Cases in scope.** Only the four `organization_case: true` held-out cases:
`CASE-HOLD-001-COMPLETED-REMINDER`, `CASE-HOLD-002-SIGNED-COMPOSITE`,
`CASE-HOLD-003-SOURCE-SENSITIVE-GENERAL-CLAIM`,
`CASE-HOLD-004-DURABLE-POLICY-IN-ACTIVE-TASK`. The twelve non-organization cases
(005–016) are out of scope for H1.

**Tool / model versions.** `sha256sum` (GNU coreutils) 9.4; `git` 2.43.0; AI
assistant `claude-opus-4-8`. No code, ML model, embedding, or network service is
used in the adjudication (integrity constraint IC-02).

**Held-out discipline (METHOD.md §3.5).** These cases carry no expected
classification and were frozen with the method. This study is their first
confirmatory pass; no case, rule, dimension, or decision threshold in §3–§4 was
changed in response to anything seen while coding.

## 3. Method

### 3.1 Organizations under test (frozen commitments)

From `category-evaluation-rules.json` → `organizations` (verbatim commitments):

- **Organization K — stable kind-first partition.** (1) Every admitted memory
  series receives exactly one primary functional kind from
  {EPISODIC, SEMANTIC, PROCEDURAL, PROSPECTIVE}. (2) The primary kind remains
  stable for the series. (3) Cross-primary-kind use requires a new series or
  separately admitted derivative. (4) WORKING is an availability tier, not a
  primary kind. (5) Mixed inputs are split, or assigned one declared primary
  kind with secondary annotations.
- **Organization R — contextual role-first relation.** (1) Functional categories
  relate an object version to query/task, actor, purpose, and time. (2) One
  object may play zero, one, or multiple roles. (3) Context-only role change does
  not create a new object version. (4) A reproducible role assignment requires
  the complete declared context tuple. (5) Representational kind and lifecycle
  state remain separate axes.

### 3.2 Dimensions coded per case per organization

The five structural dimensions named in the task and grounded in the taxonomy's
competition table and axes A1–A10:

1. **Identity multiplication** — does the organization force more than one memory
   identity/series/version for the case's content? (axis A4/A9; ENT-003/004)
2. **Classification cardinality** — how many primary functional categories the
   organization attaches to the object(s). (axis A2)
3. **Required context** — must the coding record a context tuple
   (object, query/task, actor, purpose, time) to reproduce the classification? (axis A2/A3)
4. **WORKING treatment** — is WORKING an availability **tier** or a functional
   **role** on par with the others? (ROL-005; DIST-20)
5. **Composite handling** — how indivisible mixed content is treated (forced
   split vs single retained object). (A1 "composite"; edge case "indivisible
   signed document")

Codings use only the frozen case facts and frozen commitments (no invented
facts; integrity constraint IC-01, coding_semantics). Where a case does not
exercise a dimension it is marked **N/A** (per `coding_semantics.NOT_APPLICABLE`);
N/A is not a divergence. Where more than one coding survives the frozen text for a
single organization it is recorded as **AMBIGUOUS** (per
`coding_semantics.AMBIGUOUS`) rather than forced (IC-04).

### 3.3 Per-dimension divergence judgment

For each case × dimension, mark **DIFFER** iff K and R are *required by their own
commitments* to different structural commitments on that dimension, and the
difference is not an artifact of wording (i.e., it traces to a specific frozen
commitment of K and a specific frozen commitment of R that cannot both be
honored by one encoding). Otherwise mark **same / no divergence**.

### 3.4 Encoding coverage

A case is "encodable" by an organization iff that organization's commitments
yield at least one determinate structural encoding of the case facts (it need not
be unique; an AMBIGUOUS pair still counts as encodable). A case that is
`INVALID_CASE` for an organization (internally contradictory or missing a
required fact) is not encodable and is reported as a null.

### 3.5 Confirmatory vs exploratory

- **Confirmatory** (tests H1): §3.1–§3.4 applied to all four organization cases,
  and the §4 decision rule. This is the only part that may report support.
- **Exploratory** (hypothesis-generating only, may not report support): any
  observation about *why* a divergence arises, any remark on relative cost or
  convenience of K vs R, and any pattern noticed across cases. Labeled `[EXPLORATORY]`
  inline in §5–§6.

### 3.6 Forbidden outputs

No "winner" may be declared: the study may not conclude that K or R is more
correct, more useful, more mature, or preferable. No maturity, adoption, or
external-validity claim may be made; the taxonomy is **not** adopted or validated
by this study (interpretation_boundary in both input files). The only admissible
confirmatory conclusion is SUPPORT or REJECT of *divergence* per §4.

## 4. What would confirm / refute

**Preregistered decision rule (from H1 and the taxonomy rejection condition).**

- **SUPPORT (divergence holds):** *both* organizations encode *all four* cases
  **and** at least **two** cases each **differ across at least two** of the five
  dimensions. Interpretation: K and R are distinct hypotheses worth carrying.
- **REJECT (collapse-or-reformulate):** fewer than two cases differ, **or** the
  differing cases differ on fewer than two dimensions, **or** either organization
  cannot encode ≥3 of the four cases. Interpretation: trigger the taxonomy's own
  M1-O2 rejection condition — collapse or reformulate the two organizations.

The rule is symmetric and does not reference which organization "wins." All
outcomes, including any case neither organization can encode (a null) and any
AMBIGUOUS coding, are reported in §5 regardless of their effect on the
hypothesis (METHOD.md §4.7).

<!-- ================= PRE-ANALYSIS PLAN ENDS HERE / RESULTS BEGIN BELOW ================= -->
<!-- Commit the card up to this line BEFORE running the analysis (METHOD.md §2.1). -->

## 5. Results

All four `organization_case: true` cases were encoded under K and under R using
only the frozen facts. No case was `INVALID_CASE` for either organization: **both
organizations encode all four cases; there are no encoding nulls.** Two within-K
disjunctions were recorded as AMBIGUOUS (noted below); both branches still
diverge from R.

### 5.1 Per-case encodings

#### CASE-HOLD-001-COMPLETED-REMINDER
Facts: one unchanged object says "submit a permit at 09:00" with an
unresolved-trigger state before 09:00; after recorded completion a later task
asks the same actor to reconstruct what occurred; no content changes between
tasks.

- **K:** At admission the object bears one primary kind. An unresolved trigger +
  intended future action is a **PROSPECTIVE** series (ROL-004). The later
  reconstruction-of-what-occurred is **episodic use** (ROL-001), which crosses
  the primary kind. K commitments (2)+(3) forbid the prospective series becoming
  episodic; the episodic use **requires a new series or a separately admitted
  derivative**. → *identity multiplication.* [AMBIGUOUS within K: "new series"
  vs "separately admitted derivative" — both multiply identity.]
- **R:** One object plays a **prospective** role in task 1 and an **episodic**
  role in task 2. Content-unchanged, so commitment (3): **no new version.** The
  context tuple for each task must be recorded (commitment 4).

#### CASE-HOLD-002-SIGNED-COMPOSITE
Facts: one indivisible signed document contains an ordered repair **procedure**
and a **narrative** of the incident in which it was learned; splitting the bytes
breaks the signature, though derived objects could retain lineage.

- **K:** Content spans PROCEDURAL (ROL-003) and EPISODIC (ROL-001). Commitment
  (5): **split into distinct series** (derived objects retaining lineage — which
  breaks the original signature / incurs a provenance cost) **or** assign **one
  primary kind with secondary annotations** (keeps the signature but forces a
  primary-kind adjudication and demotes the other aspect). [AMBIGUOUS within K:
  split vs single-primary+annotation.] Either branch imposes a
  forced-split/forced-primary cost R does not.
- **R:** Commitment (2)+"retain one composite object and classify each use
  context": **one composite object retained**, signature intact, procedural role
  in one context and episodic role in another, each with its context tuple.

#### CASE-HOLD-003-SOURCE-SENSITIVE-GENERAL-CLAIM
Facts: one object states a ferry departs at 17:00 and links to the particular
trip where the schedule was learned; task 1 asks the general schedule, a later
task asks who was present when it was learned.

- **K:** The general schedule claim is **SEMANTIC** (ROL-002) and the primary
  semantic series stays semantic. The "who was present when learned" query is
  **episodic** and crosses the primary kind, so the source episode is handled as
  **separate provenance or a separate series** (commitment 3) → *identity
  multiplication.*
- **R:** One object plays a **semantic** role for task 1 and an **episodic** role
  for task 2 (commitments 2+3), no version change, each with its context tuple.

#### CASE-HOLD-004-DURABLE-POLICY-IN-ACTIVE-TASK
Facts: a durable policy object constrains a short active review task with an
explicit task-handoff condition; the policy remains durably admitted after the
task and its content never changes.

- **K:** The durable policy is **PROCEDURAL** primary kind (ROL-003); its
  active-task use is the **WORKING availability tier** (commitment 4), not a
  second primary kind. No cross-primary-kind crossing occurs, so **no new
  identity** is required. Cardinality: one primary kind (+ tier annotation).
- **R:** Procedural and working are **simultaneous contextual roles**
  (commitments 1+2); WORKING (ROL-005) is a role on par with the others. One
  object, ≥2 roles, context tuple required. **No new identity.**

### 5.2 Divergence table (confirmatory)

DIFFER = K and R are forced to different commitments on that dimension; · = same
/ no divergence; N/A = dimension not exercised by the case.

| Case | Identity multiplication | Classification cardinality | Required context | WORKING treatment | Composite handling | # dims differing |
|---|---|---|---|---|---|---|
| 001 Completed reminder | **DIFFER** (K new series/derivative; R one object) | **DIFFER** (K 1 primary kind/series; R many roles/one object) | **DIFFER** (K none; R tuple required) | N/A | N/A | **3** |
| 002 Signed composite | **DIFFER** (K split→sig cost, or 1-primary+annotation; R one object) | **DIFFER** (K 1 primary kind; R multi-role) | **DIFFER** (K none; R tuple) | N/A | **DIFFER** (K forced split/primary; R retains composite) | **4** |
| 003 Source-sensitive claim | **DIFFER** (K separate episodic provenance/series; R one object) | **DIFFER** (K 1 primary kind; R multi-role) | **DIFFER** (K none; R tuple) | N/A | · (both treat the source link as provenance; not indivisible) | **3** |
| 004 Durable policy in task | · (both keep one object) | **DIFFER** (K 1 primary kind + tier; R ≥2 co-equal roles) | **DIFFER** (K none; R tuple) | **DIFFER** (K = tier; R = role) | N/A | **3** |

**Encoding coverage:** K encodes 4/4; R encodes 4/4. No nulls, no
`INVALID_CASE`.

**Cases differing on ≥2 dimensions:** all four (001:3, 002:4, 003:3, 004:3).

### 5.3 Source of each divergence (which commitments collide)

Every DIFFER traces to a specific frozen commitment pair, not to wording:

- **Identity (001, 002, 003):** K commitment (3) "cross-primary-kind use requires
  a new series or separately admitted derivative" vs R commitment (3)
  "context-only role change does not create a new object version." A single
  object cannot both be split/derived (K) and left unmultiplied (R).
- **Cardinality (all four):** K commitment (1) "exactly one primary functional
  kind" vs R commitment (2) "may play … multiple roles."
- **Required context (all four):** K's kind is series-stable/intrinsic (no tuple)
  vs R commitment (4) "a reproducible role assignment requires the complete
  declared context tuple."
- **WORKING (004):** K commitment (4) "WORKING is an availability tier rather
  than a primary kind" vs R treating WORKING (ROL-005) as a role comparable to
  the others.
- **Composite (002):** K commitment (5) "mixed inputs are split or assigned one
  declared primary kind with secondary annotations" vs R "retain one composite
  object and classify each use context."

### 5.4 Exploratory observations (not confirmatory; may not report support)

- `[EXPLORATORY]` The identity-multiplication divergence recurs specifically when
  a later task demands a cross-kind functional use of byte-unchanged content
  (001, 003). This suggests a future targeted test isolating "role change alone"
  as the trigger variable.
- `[EXPLORATORY]` CASE-002 is the only case that exercises the composite
  dimension and the only one carrying an explicit signature/provenance cost under
  K; it produced the widest divergence (4 dims). This is a hypothesis for H2-style
  axis-independence work, not evidence here.
- `[EXPLORATORY]` No relative-cost or preference claim is drawn from the above;
  such a claim is forbidden by §3.6.

## 6. Assessment

**Decision rule (§4) applied:** both organizations encode all four cases (4/4
each, ≥3 satisfied) **and** at least two cases (in fact all four) differ across at
least two dimensions. Both SUPPORT conditions are met and no REJECT condition is
triggered.

**Confirmatory conclusion: H1 is SUPPORTED — Organizations K and R genuinely
diverge.** There exist constructed organization-competition cases (all four,
minimally two) for which K and R are forced by their own frozen commitments to
different structural outcomes, and each divergence traces to a named commitment
collision rather than to case wording (§5.3). The taxonomy's M1-O2 rejection
condition is **not** triggered; carrying both organizations forward as distinct
hypotheses is justified on this structural basis.

**This does not pick a winner.** The study makes no claim that K or R is more
correct, useful, mature, or preferable; that verdict is out of preregistration
and forbidden (§3.6). The taxonomy is **not** adopted or validated by this result;
the finding is bounded structural divergence only
(`interpretation_boundary` of both input files).

**Evidence label: E2 (Supported, solo, preregistered) · `[AI-assisted]`.** Per
METHOD.md §1 and §4.8, the verbatim caveat applies:

> **Supported under a preregistered protocol; single-analyst, not independently
> replicated.**

Not "validated" or "confirmed." E3 is not claimed and cannot be self-assigned;
it would require an independent, non-AI-only second adjudicator (see §8).

## 7. Limitations

- **Single adjudicator, AI-assisted.** All four encodings and the divergence
  judgments were produced by one human-directed AI pass. The AI review does not
  count as independent corroboration (METHOD.md §1); it cannot lift E2 → E3.
- **Not genuinely blinded.** The `blind_packet_rule` in the cases file
  contemplates withholding `stress_targets`/`organization_case` from primary
  adjudicators, but this run was not blinded: the analyst saw the full case file,
  including selection rationales. An author who can see (or reconstruct) the
  `stress_targets` cannot truly blind themselves; a time-separated second pass by
  the same person only partly mitigates this (H1 "Solo?" note). Confirmation bias
  toward finding divergence is the primary threat to validity.
- **Held-out set is repository-visible and candidate-derived** (`holdout_limit`):
  the cases were constructed from the subject's own open obligations and are not
  independently sampled, representative, or natural. Divergence on these cases
  does not generalize to arbitrary memory content.
- **Divergence ≠ correctness.** SUPPORT means K and R make *different* structural
  commitments, not that either commitment is right, complete, safe, useful, or
  biologically valid (IC-12; interpretation_boundary). No maturity or adoption
  claim is made.
- **Judgment calls (disclosed).** (a) CASE-003 composite dimension was coded
  no-divergence because the object is a semantic claim with a provenance link,
  not an indivisible signed composite like 002; a coder who reads K's
  "separate provenance/series" as a composite split could mark it DIFFER, which
  would only *strengthen* the SUPPORT outcome, so the conservative choice was
  taken. (b) CASE-004 identity was coded no-divergence because neither
  organization crosses a primary kind (K keeps WORKING as a tier, R adds a role),
  so both keep one object; the divergence there is carried by cardinality and
  WORKING treatment. (c) Two within-K AMBIGUOUS disjunctions (001 new-series vs
  derivative; 002 split vs single-primary+annotation) were retained rather than
  forced (IC-04); both branches of each still diverge from R, so the SUPPORT
  outcome is robust to how they resolve.

## 8. How to replicate or falsify this

**Inputs (re-verify the exact bytes):**

```
sha256sum docs/taxonomy/cases/held-out-cases.json \
          docs/taxonomy/category-evaluation-rules.json \
          docs/taxonomy/MEMORY_TAXONOMY_v0.1.md
```

Expect:
`1aef47de0110cab90cc44a06886fb3bd1d581f5169e8fc32100719d4ff596335` (cases),
`6868d5c3dc3c1c98081af1e86145394129c5bc77ddfe8014ecab684561e1aa31` (rules),
`77ff4468d2164c9cdf61dba42287e5a9fbfe41e3ab8e920542d8811e06e95f7b` (subject).
The subject digest must equal both files' `subject_binding.raw_byte_sha256`
(IC-01); if any digest differs, stop — the pins are stale.

**Procedure to reproduce:** for each `organization_case: true` case
(CASE-HOLD-001…004), encode it under the frozen K and R commitments in
`category-evaluation-rules.json` → `organizations` across the five dimensions in
§3.2, using only the case's own `facts`. Mark DIFFER per §3.3, build the §5.2
table, then apply the §4 decision rule.

**What would overturn the SUPPORT conclusion (falsification):** re-adjudication
(ideally blinded per the cases file's `blind_packet_rule`, and by a second,
non-AI-only person — the path to E3) that shows **any** of:

1. Fewer than two cases differ on ≥2 dimensions — e.g. if a reviewer finds that
   K is *not* forced to multiply identity in 001/003 (reads the later query as
   satisfiable by the same prospective/semantic series without a new
   series/derivative), and that the remaining divergences are wording artifacts,
   collapsing the count below the §4 threshold.
2. Either organization cannot encode ≥3 of the four cases (an `INVALID_CASE`
   finding on two or more).
3. Any DIFFER is shown to rest on wording rather than a genuine commitment
   collision (§5.3), reducing the qualifying cases below two.

Any one of these triggers the taxonomy's M1-O2 rejection condition (collapse or
reformulate K and R). Note that a genuine E3 upgrade — not merely re-running this
study — requires at least one recruited second coder whose work is not AI-only
(METHOD.md §1, §4.9); this solo, AI-assisted card cannot reach E3 by itself.

---

*This card is [AI-assisted]. §1–§4 are the preregistered plan (to be committed
before §5–§8). §5–§8 are the report. Evidence label E2; the solo caveat in §6 is
verbatim and non-removable without independent corroboration.*
