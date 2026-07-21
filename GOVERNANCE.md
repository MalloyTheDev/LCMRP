# LCMRP Governance

## Scope

This document governs research decisions, evidence claims, repository changes, and program-boundary enforcement for the Lifelong Cognitive Memory Research Program.

LCMRP is an independent, product-independent research program. Governance exists to keep research questions falsifiable, evidence traceable, failures visible, and product pressure from determining research conclusions.

## Governing authority

Documents have the following order of authority:

1. The current approved Program Charter
2. This governance policy and the research-layer and evidence-state policies
3. Approved specifications, schemas, protocols, and decision records
4. Individual experiment plans and implementation documentation
5. Source-code comments and informal discussion

A lower-authority artifact cannot silently override a higher-authority one. A conflict with the Program Charter blocks acceptance until the contribution changes or a charter amendment is approved.

Published charter versions are historical records. A semantic change to the charter requires a new version; it must not rewrite the meaning of an existing version in place.

## Roles

Roles describe responsibilities and may be held by the same person unless a gate explicitly requires independence.

### Program stewards

Program stewards maintain the charter, program scope, governance rules, and long-term research agenda. They decide charter amendments and resolve boundary disputes.

### Maintainers

Maintainers review repository changes, protect reproducibility and compatibility, enforce required records, and merge accepted contributions. Merge authority does not authorize unsupported evidence claims.

### Research leads

Research leads own a declared research question or workstream. They are responsible for hypotheses, protocols, baselines, rejection criteria, provenance, results, and failure reporting.

### Contributors

Contributors may propose definitions, benchmarks, implementations, experiments, replications, security analyses, documentation, or corrections. Contributions are evaluated by their evidence and compliance, not by contributor status.

### Evidence reviewers

Evidence reviewers assess whether a maturity gate is satisfied for the exact claim and mechanism version. They must record uncertainty, failed obligations, and conflicts of interest. Review is not independent validation unless the independence requirements are separately met and documented.

### Security reviewers

Security reviewers assess threat models, trust boundaries, abuse cases, privacy risks, mitigations, and residual risk. A security reviewer may block a state transition or release when material risk is unaddressed or inaccurately represented.

## Operational authority and appointments

### Initial authority

Until a superseding appointment is recorded, the account that owns the public repository is the program steward and sole maintainer. This makes ordinary repository work possible while LCMRP is a solo-maintained project. It does not make that person independent from research they originated.

The program steward may appoint or remove maintainers through a public governance decision that identifies the person, scope of authority, effective date, and rationale. An appointment becomes effective only after the appointee accepts it. A maintainer may resign through a public record.

The current steward may transfer stewardship through a public decision accepted by the successor. Urgent access revocation during a security incident may occur before publication, but a non-sensitive record must be added when disclosure is safe.

Removal is prospective. It does not erase prior decisions, reviews, conflicts, or evidence records.

### Reviewer designation

Evidence and security reviewers are designated for a specific decision by an eligible maintainer. They do not need repository merge access. The decision record must identify the reviewer, relevant competence, relationship to the originating work, conflicts considered, and whether the review is an originator review, non-originating review, or independent external evaluation.

A reviewer is eligible when they:

- Can assess the claim, protocol, evidence, and limitations relevant to the decision
- Have access to the artifacts required for that assessment
- Disclose authorship, implementation work, employment or reporting relationships, funding, product interests, and other material conflicts
- Are not subject to a recusal rule required by the requested evidence state

### Appointment and removal safeguards

No maintainer, reviewer, or steward appointment changes an artifact's evidence state. Appointment authority cannot be used to manufacture reviewer independence. A reviewer appointed after contributing materially to the originating mechanism or experiment remains an originating reviewer for that work.

## Approval, quorum, and recusal

Quorum means the required eligible, non-recused decision-makers have participated. One person may satisfy more than one role only when the decision does not require separation or independence.

| Decision | Minimum approval | Solo-maintainer rule |
| --- | --- | --- |
| Ordinary documentation, tooling, tests, and non-semantic maintenance | One maintainer | The sole maintainer may approve and merge their own change after recording validation performed. |
| Charter, governance, layer-boundary, evidence-semantics, schema, or registry-history change | Program-steward approval and maintainer review | The sole steward-maintainer may approve the change through a public pull request with rationale, compatibility impact, and validation. This is governance approval, not independent research validation. |
| Award from `HYPOTHESIS` through `SECURITY-REVIEWED` | One maintainer decision supported by the required evidence record and a recorded evidence review | If no non-originating reviewer is available, the sole maintainer may record an explicitly disclosed originator self-review. That review can satisfy only gates that do not require independence. |
| Award of `INDEPENDENTLY_VALIDATED` | An affirmative, claim-scoped determination by one eligible external evaluator, followed by administrative acceptance by a maintainer | An originating researcher or solo maintainer cannot self-award this state. They may only merge or record an eligible external evaluator's decision without expanding its scope. |
| Award of `INTEGRATION CANDIDATE` | One maintainer confirms every prerequisite, including an existing valid independent-validation decision for the claimed scope | The sole maintainer may record the administrative decision but cannot supply the independent-validation prerequisite themselves. |
| Award of `PRODUCTION-READY` | Product-specific operational and governance authority outside foundational and reference-implementation research | LCMRP evidence alone cannot award this state. The repository may record, but not substitute for, the external product decision. |
| Evidence demotion, qualification, or withdrawal | One maintainer with a superseding evidence decision | A sole maintainer may act immediately to prevent an overstated or unsafe claim from remaining current. |

For awards below `INDEPENDENTLY_VALIDATED`, an originator self-review must be labeled as such and cannot be cited as independent corroboration. If a required quorum is unavailable, the proposal remains pending and the mechanism retains its prior state.

A reviewer must recuse from a decision when:

- The requested state requires independence and the reviewer originated, designed, implemented, operated, or analyzed the mechanism or originating experiment in a material way
- The reviewer's compensation, employment evaluation, product interest, or direct reporting relationship depends materially on the outcome
- The reviewer cannot access enough evidence to assess the claimed scope
- An undisclosed relationship or conflict would reasonably undermine the stated review type

Recusal removes the person from quorum for that decision. A conflicted steward may handle mechanical repository administration only after the required non-conflicted decision has been made; they cannot replace or broaden that decision.

### Independence threshold

An `INDEPENDENTLY_VALIDATED` decision requires an evaluator outside the originating experiment who did not materially design the mechanism, implement the evaluated version, run or analyze the originating experiment, or prepare the evidence award. The evaluator must use a stable attributed identity and disclose relevant organizational, financial, product, supervisory, and personal relationships.

The evaluator may reproduce the result or perform a substantive independent review, consistent with the evidence-state definition, but must state which mode was used. The record must identify artifacts examined, protocol deviations, claims supported or contradicted, unresolved obligations, and the evaluator's affirmative or negative decision.

Membership in the same broad community or organization is not automatically disqualifying. A direct reporting relationship, result-contingent compensation, shared ownership of the mechanism, material contribution to the originating work, or another relationship that permits control over the evaluation is disqualifying for the independent label.

Selection or appointment by the originating researcher does not establish independence. The accepting maintainer must document the evaluator's eligibility against this threshold. When the accepting maintainer is also the originator, the external evaluator's recorded decision is controlling and may not be broadened during merge.

## Decision classes

### Program decisions

Program decisions include charter changes, workstream creation or retirement, governance changes, and changes to research or product boundaries. They require a pull request containing the motivation, alternatives, compatibility impact, risks, and migration or transition plan where applicable.

### Research-definition decisions

Taxonomies, formal definitions, benchmark contracts, and evaluation metrics must state their scope, assumptions, unresolved alternatives, and criteria for revision. Definitions must not be chosen solely because they make a preferred mechanism perform better.

### Experiment decisions

An experiment must identify its research question, layer, falsifiable hypothesis, baselines, datasets or scenarios, metrics, protocol, analysis plan, rejection criteria, security and privacy considerations, and reproducibility requirements before confirmatory results are interpreted.

Material post-result changes to hypotheses, metrics, exclusions, or analysis must be disclosed. Post hoc work is permitted when labeled exploratory.

### Evidence-state decisions

Evidence states apply to an exact mechanism version and claim scope. A passing build, successful demonstration, or completed experiment never promotes a mechanism automatically. Promotion, demotion, qualification, and withdrawal require traceable evidence decisions under [Evidence and Readiness States](docs/program/EVIDENCE_STATES.md).

### Implementation decisions

Reference-implementation choices must preserve replaceable boundaries where practical and document why concrete dependencies were selected. Convenience, current product compatibility, or vendor availability must not be presented as evidence that an architecture is generally correct.

## Decision process

Substantive changes use the following process:

1. Open or identify a bounded research question or governance problem.
2. Declare the applicable research layer and affected evidence claims.
3. Record alternatives, assumptions, risks, and acceptance or rejection criteria.
4. Submit an independently reviewable pull request.
5. Resolve blocking research-integrity, security, privacy, reproducibility, and program-boundary findings.
6. Record the decision and supporting artifact identifiers.
7. Preserve dissent, uncertainty, and rejected alternatives when they materially affect interpretation.

Emergency security changes may be reviewed privately and merged with restricted detail. The public record should be completed after coordinated disclosure when doing so no longer increases risk.

## Research integrity

LCMRP retains negative results, null findings, failed replications, and mechanisms rejected by evidence. Results must not be removed merely because they weaken a preferred hypothesis.

Contributors must:

- Distinguish confirmatory analysis from exploratory analysis
- Preserve raw or minimally transformed results when licensing, privacy, and storage constraints permit
- Record exclusions, failed runs, deviations, and missing data
- Report uncertainty and avoid unsupported generalization
- Trace claims to evidence records and immutable artifact versions
- Identify conflicts between new and prior evidence
- Correct material errors through an auditable superseding record
- Avoid invented references, fabricated measurements, and unverified claims of novelty

Human-inspired terminology must be operationally defined. Similarity to biological memory is motivation or analogy unless direct evidence supports a stronger relationship.

## Program independence

LCMRP must not be described or governed as part of CorpusStudio. CorpusStudio architecture, repositories, product plans, interfaces, technology choices, schedules, and delivery needs cannot determine Layer 1 conclusions or Layer 2 interfaces.

CorpusStudio-specific production code is outside this program's authorized scope.

When a substantive artifact discusses CorpusStudio, all such content must be isolated under a section titled **Future CorpusStudio Integration Implications**, immediately labeled **RESEARCH-TO-PRODUCT HYPOTHESIS**, and accompanied by the independent validation still required. That section is provisional and cannot create an architecture decision, implementation commitment, roadmap recommendation, or production-readiness claim.

## Conflicts of interest and independence

Reviewers must disclose authorship, implementation involvement, organizational relationships, funding, product ownership, or other interests that could affect judgment.

An originating researcher may review correctness but cannot self-certify independent validation. A solo maintainer is not independent merely because no other maintainer is appointed. Independent validation records must satisfy the eligibility, recusal, quorum, and independence threshold above and must state what was reproduced or reviewed, the evaluator's relationship to the originating work, artifacts available, protocol deviations, and unresolved claims.

## Versioning and amendments

Governance, schemas, protocols, benchmarks, and mechanism interfaces must use explicit versions when interpretation or reproducibility depends on their contents.

A proposed amendment must include:

- The exact text or contract being changed
- The reason for the change
- Alternatives considered
- Effects on existing experiments and evidence
- Compatibility or migration requirements
- New risks or authority changes

Editorial corrections may be merged without a version increment only when they do not change meaning. If meaning is plausibly affected, create a new version and preserve the prior one.

## Enforcement

Maintainers may reject or revert work that violates the charter, overstates evidence, hides negative results, weakens provenance, crosses user or product boundaries, or introduces unresolved material security or privacy risk.

Disputed decisions should be documented with the claim, evidence, governing rule, alternatives, and final rationale. Governance disagreements must not be resolved by silently changing experimental records or maturity labels.
