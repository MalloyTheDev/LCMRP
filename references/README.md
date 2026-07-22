# References and Evidence Sources

This directory will hold LCMRP's verified source catalog and supporting literature artifacts. It begins empty intentionally: the program does not treat remembered, suggested, or merely discovered citations as verified evidence.

## Source policy

Prefer sources in this order when they are relevant to the claim:

1. Standards, specifications, and official technical reports
2. Primary peer-reviewed papers and proceedings
3. Authoritative datasets, benchmarks, and model or system documentation
4. Systematic reviews and high-quality surveys
5. Secondary explanations used only for orientation

Repository popularity, search rank, citation count, and vendor claims are not substitutes for methodological review. Record retractions, corrections, competing results, negative findings, and material conflicts of interest when known.

## Evidence labels

Use one label for each literature or background claim in proposals, protocols, reports, and threat models:

| Label | Meaning | Permitted use |
| --- | --- | --- |
| `[VERIFIED]` | The cited source was inspected and directly supports the bounded claim. | May support a research statement within the source's scope. |
| `[USER]` | The claim or requirement originated with a user or stakeholder. | Records provenance of a goal or assertion; it is not literature evidence. |
| `[MEMORY]` | The claim is recalled but has not been checked against a source. | Orientation only; verify before relying on it. |
| `[VERIFY]` | A plausible source or claim has been identified but verification is incomplete. | Open research item; must not be presented as established. |
| `[CONFLICT]` | Relevant sources, results, or definitions materially disagree. | State the conflict and do not resolve it without further evidence. |

Verification applies to a specific claim, not an entire source. A paper can support one statement while leaving another unsupported.

## Minimum citation record

Each cataloged source should record:

- Stable source ID
- Complete title and author or organization information
- Publication year and venue
- Persistent identifier or canonical URL, when available
- Exact version, revision, or access date for mutable material
- Source type and review status
- License or reuse restrictions relevant to retained artifacts
- Claims for which the source was inspected
- Scope limitations, conflicting evidence, and corrections
- Verifier and verification date

Never invent a DOI, arXiv identifier, theorem number, benchmark result, quotation, or bibliographic field. Leave an unknown field explicit and schedule a verification step.

## Claim-to-evidence ledger

Substantive literature reviews should maintain atomic claims rather than attaching a list of references to a whole paragraph.

| Claim ID | Bounded claim | Label | Source IDs and exact locations | Missing support | Risk if false | Next check |
| --- | --- | --- | --- | --- | --- | --- |
| `<claim ID>` | `<claim>` | `<evidence label>` | `<source and section, page, figure, or table>` | `<gap>` | `<impact>` | `<action>` |

Paraphrases must preserve the source's population, assumptions, conditions, and uncertainty. Direct quotations require exact location information and must comply with copyright and licensing limits.

## Verification workflow

1. Formulate an atomic claim before searching for support.
2. Search primary terms, adjacent terminology, standards, likely venues, and known limitations or negative results.
3. Inspect the primary source rather than relying on a search snippet or secondary citation.
4. Record the exact location and the source's scope, assumptions, and method.
5. Look for corrections, retractions, replications, and conflicting findings.
6. Assign the evidence label and record unresolved obligations.
7. Recheck mutable sources before a substantive report is finalized.

Novelty must not be claimed until relevant keywords, adjacent terms, venues, standards, and limitation searches are documented. Until then, use `candidate contribution` or `research hypothesis`.

## Current status

No sources are cataloged in this directory. The separate M1 prior-art map is a bounded, unregistered research input rather than a verified source catalog or evidence-synthesis finding. Adding a catalog entry is a research action that requires claim-level verification and review; bootstrap documentation, a link, or inclusion in the prior-art map alone does not establish a literature claim.
