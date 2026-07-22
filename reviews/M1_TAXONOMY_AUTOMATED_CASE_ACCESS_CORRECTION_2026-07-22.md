# M1 Taxonomy Automated Case-Access Correction — 2026-07-22

## Classification and disposition

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Program-infrastructure incident correction supporting Layer 1
- **Affected study:** `LCMRP-FSTUDY-0001-M1-TAXONOMY`
- **Affected study record:** `LCMRP-FSTUDYREC-0001-M1-TAXONOMY@1`
- **Disposition:** **AUTOMATED PRE-INTAKE CASE ACCESS CONFIRMED; EXECUTION REMAINS BLOCKED**
- **Research result created:** No
- **Research finding or closeout created:** No
- **Mechanism evidence effect:** None; not applicable to this foundational study
- **M1 completion effect:** None; M1 remains in progress
- **Product or integration authority created:** None

This record corrects the repository's current access-state interpretation after a
static audit found that general validation processes opened the three frozen
taxonomy case files before any governed execution intake existed. The accesses
were validation operations: JSON parsing, raw-byte digest calculation, and
freeze-test content inspection. They were not adjudication, coding, analysis,
or case-packet generation, and they created no planned output or scientific
result. They nevertheless accessed case bytes and therefore must not be
described as if no process had accessed those bytes.

The version-1 study remains frozen, blocked, and unexecuted. An intake created
later cannot retroactively authorize these events.

## 1. Scope and terminology

This correction distinguishes four things:

1. **Operational access:** a process opened case bytes for parsing, hashing, or
   text inspection.
2. **Research execution:** adjudicators coded cases under the frozen protocol.
3. **Research output:** a declared analysis ledger, catalog, or other planned
   result artifact.
4. **Research interpretation:** a finding, terminal disposition, closeout, or
   evidence claim derived from outputs.

For the audited automated routes, only the first is established. This
distinction limits the scientific consequence; it does not erase the
access-control failure.

The audit did not open, parse, hash, render, or summarize any production case
body. It inspected source code, non-case metadata, path existence, Git history,
and GitHub Actions metadata. The containment implementation and its adversarial
tests use only synthetic temporary case fixtures.

## 2. Preserved historical review scope

The [taxonomy execution-readiness review](M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md)
accurately records the actions performed by that review lane: it deliberately
did not run the repository validator or test suite and did not open case bodies.
The [study-execution decision](M1_STUDY_EXECUTION_DECISION_2026-07-21.md)
similarly describes the isolated taxonomy-readiness and verification lanes in
their reviewed scope. Those historical statements are not rewritten here.

This correction concerns other automated processes and later repository-wide
validation. It supersedes only any present-day inference that the case files
retain a process-wide, post-freeze no-access history. It does not reinterpret
the readiness review as having performed case adjudication or accessed a
scientific result.

## 3. Confirmed observations

### 3.1 Static code trace at the accepted merge

At merge commit
[`cc39cc1aaef2f5456b637940c5df0dad674f3d14`](https://github.com/MalloyTheDev/LCMRP/commit/cc39cc1aaef2f5456b637940c5df0dad674f3d14),
the validator had three independent case-body access paths during one normal
invocation:

- [`validate_serialized_documents`](https://github.com/MalloyTheDev/LCMRP/blob/cc39cc1aaef2f5456b637940c5df0dad674f3d14/tools/validate_repository.py#L407-L417)
  loaded every repository JSON file, including each taxonomy case file;
- [`validate_local_artifact_references`](https://github.com/MalloyTheDev/LCMRP/blob/cc39cc1aaef2f5456b637940c5df0dad674f3d14/tools/validate_repository.py#L893-L903)
  loaded every JSON file again; and
- the same function
  [recomputed every recorded or verified local SHA-256](https://github.com/MalloyTheDev/LCMRP/blob/cc39cc1aaef2f5456b637940c5df0dad674f3d14/tools/validate_repository.py#L908-L930),
  including the three case bindings declared `VERIFIED` by the frozen manifest.

The accepted freeze suite also
[read every immutable source to recompute its digest](https://github.com/MalloyTheDev/LCMRP/blob/cc39cc1aaef2f5456b637940c5df0dad674f3d14/tests/test_m1_study_freeze.py#L286-L302)
and later
[read the same sources as text for content checks](https://github.com/MalloyTheDev/LCMRP/blob/cc39cc1aaef2f5456b637940c5df0dad674f3d14/tests/test_m1_study_freeze.py#L446-L478).
The source list included all taxonomy provenance artifacts. These routes were
not guarded by an intake-aware reader or a process-level case-access tripwire.

The code trace establishes operational access whenever those commands reached
the applicable functions. It does not establish that a human or model examined
the resulting in-memory values.

### 3.2 Confirmed automation runs

The following GitHub Actions records bind the affected commands to exact
revisions:

| Run | Exact head | Observed workflow state | Access interpretation |
| --- | --- | --- | --- |
| [29876120708](https://github.com/MalloyTheDev/LCMRP/actions/runs/29876120708) | `5928dcbb0cd2a9d0d730248bd28255e55592d29f` | Repository validator ran and failed; the full suite was skipped. | The validator's body scans and digest route ran before its aggregate failure was reported. |
| [29881627540](https://github.com/MalloyTheDev/LCMRP/actions/runs/29881627540) | `b9ae454cdd7b8d9fc9dd88c7a6049eef35eb3489` | Repository validator and complete suite both passed. | Both validator and freeze-suite access routes ran. |
| [29882273616](https://github.com/MalloyTheDev/LCMRP/actions/runs/29882273616) | `cc39cc1aaef2f5456b637940c5df0dad674f3d14` | Post-merge repository validator and complete suite both passed. | Both validator and freeze-suite access routes ran on the accepted merge. |

The failed run started at `2026-07-21T23:07:54Z`. The successful pull-request
run started at `2026-07-22T00:55:08Z`, and the successful post-merge run started
at `2026-07-22T01:08:27Z`. GitHub records the post-merge job as complete at
`2026-07-22T01:08:49Z`; the run metadata was updated at `2026-07-22T01:08:50Z`.

Local repository-validator and full-suite invocations also occurred during the
repair work before the defect was identified. Their exact invocation count and
per-open chronology were not retained in an immutable repository log, so this
record does not invent either. Repetition within mutation-heavy freeze tests
also means that a source-level minimum per helper call must not be presented as
the total number of opens.

### 3.3 What was and was not emitted

Observed command output did not print case bodies, case-level classifications,
codes, rationales, agreement measurements, or taxonomy conclusions. No planned
taxonomy output, research-finding record, or foundational closeout was created,
and the applicable registries remained empty. These are bounded observations
about the inspected logs and repository state, not proof that no unrecorded
process, cache, or external observer existed.

## 4. Impact assessment

### Observation

- The case files' strict process-wide pre-intake access chronology is
  compromised.
- The accesses occurred through general validation infrastructure, not through
  the frozen two-primary/one-tie adjudication procedure.
- No research output or interpretation was produced by those access routes.
- Version 1 was already blocked for independent metadata, intake, actor, and
  supersession reasons.

### Inference

The confirmed access does not reveal a taxonomy result, but it removes the
basis for a future declaration that the existing version-1 case bytes were
never accessed after freeze and before intake. A later version-2 package and
human-contributor intake must disclose this history. The steward must decide,
under explicit review, whether those cases may be retained with the disclosure
or must be replaced by newly frozen material. Eligibility and no-prior-access
for any prospective human contributor cannot be inferred from automation logs.

### Not established

This correction does not establish or challenge case quality, case sensitivity,
taxonomy correctness, category coverage, adjudicator agreement, Cohen's kappa,
support, rejection, ambiguity, null outcome, external validity, novelty,
security effectiveness, privacy effectiveness, deletion effectiveness,
implementation suitability, or product readiness.

## 5. Containment action

The repair is intentionally limited to program infrastructure:

1. bootstrap an authoritative protected-artifact catalog from the fixed
   foundational-study registry and every indexed canonical study manifest
   before any broad content scan;
2. classify taxonomy case sources from authoritative method-profile, source
   kind, and source-role metadata rather than a fragile directory name;
3. preserve the protected union across all indexed taxonomy versions, including
   superseded records, and reject ambiguous active lineages, broken digest
   links, aliases, unsafe locators, undeclared protected-root entries, and
   cross-version planned-output reuse;
4. make generic validator readers skip authoritative protected bodies, reject
   non-authoritative or aliased requests to resolve them, recognize exact
   retained `DRAFT` manifest mirrors only as inert metadata, and defer case
   digest verification;
5. refactor production freeze checks to validate case locator, digest metadata,
   structural presence, and immutability state without opening case bytes;
6. run the validator and complete suite through an independent Python audit-hook
   tripwire that denies study-artifact body opens during catalog bootstrap,
   terminates with dedicated status `97` before a protected child open, unions
   inherited, catalog-discovered, and explicit protections, and rejects
   interpreter or descendant routes that would suppress the hook; and
7. retain synthetic mutation tests for path, alias, lineage, bootstrap, output,
   and access-control failures.

This containment does not create a post-intake reader, an execution capability,
an intake schema, a contributor identity, a version-2 study, or authorization
to verify case digests. Those belong to separately reviewed increments.

## 6. Security, privacy, deletion, and governance considerations

- Case bytes remain opaque to ordinary validation even though the files are
  declared synthetic and non-human-subject inputs. Synthetic status does not
  justify bypassing the frozen access sequence.
- The process tripwire protects the additive configured/catalog union and
  compares lexical paths, resolved aliases, and filesystem identities before
  standard Python opens. Catalog construction separately rejects symlink and
  hard-link ambiguity and undeclared entries in protected namespaces.
- No case body is copied into this correction, logs, fixtures, or test output.
- No deletion is performed. The frozen version-1 artifacts and the operational
  history are preserved rather than rewritten.
- Changes to validation/access semantics require explicit steward review. This
  containment must not be auto-merged merely because tests pass.
- Raw operational logs are not promoted to scientific evidence by this review.

## 7. Limitations and open obligations

- GitHub Actions metadata proves which workflow steps ran, while the access
  interpretation relies on the exact source code at each head. No immutable
  per-file open ledger existed for the historical runs.
- Local invocation counts and timestamps are incomplete.
- The audit did not inspect process caches, runner disks, backups, or external
  telemetry, and makes no deletion-success claim about them.
- The tripwire covers the approved Python validation commands and their standard
  Python file/process APIs; it is not an operating-system sandbox. Direct native
  syscalls through FFI, pre-opened descriptors, hostile interpreter or
  dependency code that executes before `sitecustomize`, deliberate mutation
  through Python-object introspection, debuggers, or privileged external
  processes are outside its enforcement boundary. Shell and non-Python
  descendants are rejected; introducing non-Python validation would require a
  separately reviewed OS-level containment mechanism.
- Containment does not repair the version-1 metadata blockers or define the
  human attribution, eligibility, intake, and external receipt contracts.
- A later superseding study must explicitly address the compromised access
  chronology before any case-byte verification or adjudication is considered.

## Final disposition

**Record the automated accesses, keep taxonomy execution stopped, and accept no
case-access or execution authority from this correction.** The next code review
may accept only the containment and disclosure controls described above. A
separate later increment must define the intake/declaration/receipt contracts;
another governed increment must freeze and review any version-2 study package.
