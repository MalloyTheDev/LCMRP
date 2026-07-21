# M1 Foundational-Study Freeze Adversarial Review — 2026-07-21

## Review classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Program verification infrastructure; not a research finding or evidence record
- **Review scope:** Two proposed real, mechanism-free M1 preregistrations and the bounded registry effect needed to discover them
- **Current verdict:** **FINAL PASS — EXACT PREREGISTRATION FREEZE ONLY**
- **Study analyses executed by this review:** None
- **Research findings, closeouts, or experiment records created:** None
- **Mechanism evidence labels awarded or changed:** None
- **M1 completion established:** No

This review evaluates protocol identity, exact-byte provenance, preregistration
state, method-profile obligations, output nonexistence, and registry containment.
It does not evaluate the candidate taxonomy, prove or interpret the formal
model, inspect planned outputs, run a formal tool, adjudicate a case, or convert
`FROZEN` or `ACTIVE` into scientific evidence.

## Independence and write boundary

The verification lane treated both authoring lanes, all candidate subjects,
schemas, registries, navigation, and future canonical records as read-only. It
wrote only this review and `tests/test_m1_study_freeze.py`. It did not repair an
author artifact, create either study manifest, update an index, or execute an
analysis.

## Exact targets

| Lane | Expected study identity | Expected primary profile | Exact registered subject |
| --- | --- | --- | --- |
| Taxonomy | `LCMRP-FSTUDY-0001-M1-TAXONOMY` / `LCMRP-FSTUDYREC-0001-M1-TAXONOMY` v1 | `LCMRP-MPROF-0001-M1-STRUCTURAL-TAXONOMY` / `STRUCTURAL_OR_TAXONOMY_EVALUATION` | `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY` v1, SHA-256 `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70` |
| Formal model | `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL` / `LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL` v1 | `LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS` / `FORMAL_ANALYSIS` | `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL` v1, SHA-256 `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3` |

The canonical record paths under review are:

- `records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v1.json`
- `records/foundational/studies/LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v1.json`

## Initial integration result

The first dedicated run occurred before either author lane or the integrating
reviewer had placed canonical records in the shared tree. The suite rejected
the state **14/14 tests**: both required manifest paths were absent and
`registry/foundational-studies.yaml` still contained zero entries. This is the
correct fail-closed result. It is not a defect in the existing accepted subject
registrations and does not imply that either planned hypothesis is false.

Command:

```text
PYTHONPATH=.venv/lib/python3.12/site-packages python -m unittest tests.test_m1_study_freeze -v
```

## Positive freeze gates

The final dedicated suite requires all of the following simultaneously:

- exactly two canonical JSON manifests, at the reviewed paths, and exactly two
  matching `ACTIVE` foundational-study index entries;
- Draft 2020-12 conformance and exact study, record, profile, and registered
  subject identities;
- exact subject definition locators and raw-byte SHA-256 digests already
  admitted to the foundational-subject registry;
- `FROZEN` record and preregistration state, an initial amendment, false prior
  result access, a freeze time, authority, and immutable freeze attestation;
- freeze-attestation metadata that resolves back to the exact record, version,
  study, time, authority, and no-prior-result-access statement;
- repository-local, traversal-free resolution and raw-byte digest verification
  for every frozen subject, profile, source, environment, configuration,
  protocol, tool, category, formal-system, and freeze artifact;
- the exact, lane-specific planned analysis-ID sets, with no missing,
  duplicated, added, or cross-lane analysis identity;
- one distinct analysis-scoped planned output identity and locator per analysis,
  even when multiple analyses will later derive from one separately retained
  raw computation bundle;
- `PENDING` null digests for every planned output and proof that no planned
  output path yet exists;
- separate taxonomy positive, negative, and held-out source identities and
  provenance, with profile lists bound exactly to the positive and negative
  source roles and a coverage rule that governs held-out cases;
- non-human source declarations using only the contract's controlled roles;
- complete structural/taxonomy obligations: versioned category definitions,
  competency questions, integrity constraints, adjudication, and coverage;
- complete formal obligations: versioned formal system, assumptions,
  propositions, satisfiability or consistency checks, intended entailments,
  non-entailments or countermodels, immutable tool provenance, verification
  method, semantic-validity check, and counterexample search;
- an exact binding between the formal-system profile artifact and a declared
  `FORMAL_INPUT` source, plus a semantic check that cannot be replaced with
  syntax, parsing, or schema validation alone;
- empty research-finding, closeout, mechanism, experiment, and evidence
  registries and empty canonical result-record directories;
- no mechanism maturity effect, affirmative evidence or completion claim,
  product-integration binding, or CorpusStudio dependency; and
- distinct study, profile, source, analysis, and artifact identities across the
  two lanes.

The taxonomy freeze records role eligibility and isolation requirements but
does not invent personnel. Its separately governed post-freeze/pre-coding
`execution/execution-intake.json` must not exist in this increment; a later
intake must bind the exact frozen manifest digest and stable contributor IDs
before any coding.

## Adversarial mutations

| Attack | Mutation | Required rejection |
| --- | --- | --- |
| Subject swap | Exchange the taxonomy and formal subject blocks | Exact admitted-subject binding fails |
| Profile swap | Exchange the two primary profiles | Exact profile ID, kind, and obligations fail |
| Digest substitution | Replace an admitted subject digest with a valid-length false digest | Exact subject and raw-byte digest checks fail |
| Unsafe locator | Replace a protocol path with `../outside.md` | Traversal and immutable-resolution checks fail |
| Freeze-artifact swap | Bind the taxonomy manifest to the formal freeze attestation | Attestation record/study/time/authority binding fails |
| Missing analysis | Remove every planned taxonomy analysis | Schema and atomic-analysis gates fail |
| Duplicate analysis | Duplicate a formal analysis and its output reference | Exact analysis-ID and distinct analysis-output gates fail |
| Source-role collapse | Relabel the negative taxonomy source as positive | Required separate negative coverage fails |
| Fake held-out set | Give the held-out source the positive source's provenance artifact | Independent held-out provenance gate fails |
| Human/unknown source | Mark a source as human or use `RESULTS` as its role | Contract and non-human source gates fail |
| Obligation deletion | Remove taxonomy integrity constraints, formal entailments, or tool provenance | Profile schema and explicit obligation gates fail |
| Syntax laundering | Replace all formal semantic methods with “Syntax checking only” | Semantic-validity and counterexample gates fail |
| Executed-output smuggling | Point a planned output at an existing manifest and mark its digest `VERIFIED` | Pending/null and nonexistence gates fail |
| Claim laundering | Assert protocol completion, scientific evidence, or M1 completion | Claim-boundary gate fails |
| Maturity leakage | Mark mechanism maturity applicable or label-awarding | No-mechanism-effect gate fails |
| Registry contamination | Add an entry to a result/evidence registry or alter the study-index digest | Containment and exact-byte index gates fail |

## Final validation result

Canonical integration produced exactly two `ACTIVE`, `FROZEN` records:

| Study | Manifest raw-byte SHA-256 | Freeze-attestation raw-byte SHA-256 | Planned analyses / sources |
| --- | --- | --- | --- |
| `LCMRP-FSTUDY-0001-M1-TAXONOMY` | `01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139` | `fbfa5b94cc940af1ccf5e38ddf763ef93982463ca0bd8f5fb0325d4bf6e843a9` | 5 / 5 |
| `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL` | `b99da2d9cfa34d659416fe30cc1d3fa731425d1fcfb8b6c9422cd9b5add2707e` | `f004f0c9415b72d9904c7c8f20c76aff8a365f07a2cf9f902f81678265c39f19` | 7 / 5 |

The first canonical verifier run rejected one expectation mismatch: the formal
manifest correctly retained `SOURCE-FSC-01`, an immutable `PRIOR_WORK` binding
to the accepted Foundational Study Contract, while the verifier's provisional
expected set omitted it. The source was not removed or rewritten. Independent
inspection confirmed that it is a legitimate non-human method-contract input,
and the gate was corrected to pin all five exact formal source IDs.

The next dedicated run passed **14/14**. The complete suite then exposed three
stale subject-admission assertions that still prohibited every real study after
subject admission. The root integration reviewer narrowed those historical
gates to continue prohibiting findings, closeouts, mechanisms, experiments,
and evidence while allowing only the separately reviewed frozen-study pair.
The following complete run reached **143/144**, with the sole remaining failure
being a navigation link to the root-owned decision artifact before that file
existed. This is a publication-integration dependency, not a study-contract or
digest failure. After the root decision artifact was added, the verification
lane independently re-ran the same integrated tree and obtained the final
results below.

| Check | Current result |
| --- | --- |
| Dedicated study-freeze suite | **14/14 passed** |
| Exact manifest/index SHA-256 recomputation | Passed for both records |
| Immutable input and freeze-attestation resolution | Passed |
| Planned-output pending/null/nonexistence checks | Passed for all 12 analyses |
| Empty result/evidence registries and record areas | Passed |
| Test-module compilation | Passed |
| Dependency consistency (`python -m pip check`) | Passed |
| Complete unit suite | **144/144 passed** |
| Repository validator | Passed |

No author-reported result was substituted for these in-process runs. The
final pass covers exact identity, immutable inputs, preregistration, method
obligations, planned-output absence, and registry containment only. It does not
cover execution, a result, a finding, a closeout, scientific validation,
mechanism maturity, product integration, or M1 completion.

## Security, privacy, and governance observations

- Local SHA-256 resolution detects byte substitution relative to the reviewed
  digest. It does not authenticate authorship, prove semantic correctness, or
  prevent a coordinated replacement of both content and every reference before
  review.
- A repository-local freeze attestation is auditable but is not a trusted
  external timestamp or independent registrar.
- The v0.1 profile prohibits human subjects and participant data. The tests
  reject a source that changes that flag, but they cannot prove that a public
  non-human artifact contains no accidentally embedded personal information.
- Separating held-out provenance reduces direct fixture reuse. It does not by
  itself prove that an author never inspected held-out content before freeze.
- Keeping planned outputs absent prevents this increment from publishing
  results through the protocol path. It does not prevent out-of-repository
  analysis unless governance and review are also followed.

## Limitations and open obligations

1. This is internal, agent-assisted, repository-local review, not independent
   scientific validation.
2. Schema and digest validity establish contract shape and byte identity, not
   taxonomy usefulness, biological validity, formal consistency,
   satisfiability, soundness, realizability, or security.
3. The mutation set is representative, not exhaustive; coordinated multi-file
   substitutions still require human review and protected repository history.
4. No analysis has been executed. Therefore there is no basis for a finding,
   closeout, replication claim, evidence status, or M1 completion claim.
5. Planned tool provenance describes a reproducibility input; it is not proof
   that the tool is correct or will be invoked as planned.
6. A later result must bind one exact frozen manifest, subject, profile,
   analysis, and raw-byte manifest digest. This review does not pre-approve any
   later finding.
7. Taxonomy adjudicator identities are intentionally not fabricated at freeze.
   Execution remains blocked until a later immutable intake records two
   eligible primary adjudicators and one eligible tie adjudicator, their
   declarations, isolation, and no-prior-result-access state.

## Recommended next step

After an exact-head freeze passes all gates and steward review, execute each
study in a separately governed increment without modifying the frozen
manifests. Publish one immutable finding or terminal disposition per planned
analysis, including `NOT_RUN`, `HALTED`, `INVALID`, null, negative, and
contradictory outcomes. Only then evaluate an exact immutable closeout whose
analysis set is equal to the frozen plan. Keep both studies mechanism-free and
product-independent throughout.

## Decision

**FINAL PASS — EXACT PREREGISTRATION FREEZE ONLY.** The integrated tree contains
exactly the two reviewed `ACTIVE`, `FROZEN` Layer 1 studies, binds their admitted
subjects and all immutable inputs by raw-byte digest, preserves distinct
profile and analysis identities, leaves every planned output absent and
`PENDING`, and creates no finding, closeout, mechanism, experiment, evidence,
or maturity effect. The taxonomy execution intake is also absent as required;
personnel must be bound later without modifying the frozen manifest. This pass
must not be restated as execution authorization without the declared intake and
pre-execution gates, as a favorable result, as validation of either subject, or
as M1 completion.
