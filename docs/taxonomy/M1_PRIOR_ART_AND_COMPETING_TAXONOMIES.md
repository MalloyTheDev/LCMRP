# M1 Prior Art and Competing Memory Taxonomies

**Status:** literature synthesis — not an adopted taxonomy · Prepared 2026-07-21

## Claim and evidence boundary

This document maps source-defined distinctions and exposes choices that a product-independent machine-memory taxonomy will have to make. It is not a finding, a registered foundational study, a formal model, a benchmark result, or evidence for any mechanism. No Charter mechanism evidence state applies. Nothing here establishes novelty, completeness, biological fidelity, usefulness, safety, or independent validation. Terms headed **LCMRP inference** are provisional interpretations proposed only to make later comparisons falsifiable.

This map is a literature synthesis, not a completed evidence-synthesis finding. A later structural or taxonomy evaluation may use it as an input.

## 1. Research question

Which existing classifications of human and machine memory are genuinely operationally distinguishable, which classify different dimensions under the same names, and which dimensions are missing when lifelong machine memory must also support provenance, authority, uncertainty, security, and deletion?

No answer is adopted here. The immediate objective is to prevent one familiar hierarchy—biological, architectural, storage-oriented, or product-oriented—from silently determining the M1 formal model.

## 2. Search scope and reproducibility

### 2.1 Search performed

Live searches and source checks were performed on 2026-07-21. Query families combined the following terms:

- `episodic semantic procedural prospective working memory`, `human memory control processes`, `reconsolidation`, `event segmentation`, and `forgetting`;
- `language agent memory taxonomy`, `cognitive architecture`, `parametric non-parametric memory`, `external differentiable memory`, `memory stream`, `skill library`, and `virtual context management`;
- `provenance entity activity agent`, `valid time transaction time`, `belief revision`, `truth maintenance`, `confidence calibration`, and `archival lifecycle`;
- `attribute based access control`, `permission prohibition duty`, `memory poisoning`, `prompt injection`, `training data extraction`, `machine unlearning`, and `media sanitization`.

Searches covered publisher or proceedings pages from ACM, NeurIPS, PMLR, AAAI, USENIX, PubMed-indexed primary articles, author manuscripts, and arXiv/OpenReview primary manuscripts, plus W3C Recommendations, NIST publications, IETF specifications, CCSDS recommended practice, and the official text of EU law. Searches also followed references from primary framework papers to original system papers.

### 2.2 Inclusion and exclusion rules

Included sources had to be at least one of:

1. an original experiment or source definition for a human-memory distinction;
2. an original machine-memory architecture, system, attack, or formal framework;
3. an authoritative standard, specification, official technical guidance, or official legal text.

Surveys, vendor pages, news, blogs, and unsourced explainers were not used as evidence for technical claims. A paper's own name for a component is reproduced as that paper's terminology, not endorsed as a correct classification. Preprints are marked as proposals and do not supply validation. Citation counts, benchmark numbers not needed for the taxonomy question, and claims of being “first” or “novel” were deliberately excluded.

### 2.3 Interpretation labels

- **Reproduced source claim** — a paraphrase that the linked primary source or specification itself supports.
- **LCMRP inference** — a provisional cross-domain interpretation made in this document.
- **Unresolved** — a conflict that cannot be settled from the reviewed sources without a definition choice or empirical comparison.

This was a bounded, English-language prior-art search, not a systematic review. It did not exhaust every cognitive architecture, database model, agent framework, legal regime, or 2025–2026 preprint.

## 3. Human-memory organizations and transfer limits

Human-memory research supplies several useful distinctions, but it does not supply one mutually exclusive hierarchy ready to copy into software.

| Organizing tradition | Reproduced source claim | Machine-transfer limit |
| --- | --- | --- |
| Stores and control processes | Atkinson and Shiffrin distinguish relatively permanent structural features from modifiable control processes, and organize their proposed system around sensory registers, a short-term store, and a long-term store ([Atkinson & Shiffrin, 1968](https://www.sciencedirect.com/science/chapter/bookseries/pii/S0079742108604223)). | A process boundary, storage tier, and retention duration are different variables in software. A fast persistent store is not thereby “short-term,” and a context buffer is not thereby a human short-term store. |
| Working memory | Baddeley and Hitch propose a limited-capacity workspace shared between storage and control demands, supported by experiments involving reasoning, comprehension, and learning ([Baddeley & Hitch, 1974](https://www.sciencedirect.com/science/chapter/bookseries/pii/S0079742108604521)). | A token window supplies bounded input state but does not, by that fact alone, implement the control functions or subsystem claims of the psychological model. |
| Episodic and semantic memory | Tulving's original account distinguishes personally experienced, temporally situated events from organized general knowledge while treating the systems as partially overlapping ([Tulving, 1972](https://alicekim.ca/12.EpSem72.pdf)). His later account also links episodic remembering to autonoetic consciousness ([Tulving, 1985](https://doi.org/10.1037/h0080017)). | A timestamped event record can meet a machine operational test without possessing subjective re-experience. Calling it “episodic” must therefore identify which properties are retained and which consciousness claim is not transferred. |
| Knowing how and knowing that | Amnesic participants acquired and retained a mirror-reading skill despite impaired memory for the encountered words, an experimental dissociation used to motivate skill/declarative distinctions ([Cohen & Squire, 1980](https://pubmed.ncbi.nlm.nih.gov/7414331/)). | Executable code, learned model parameters, a natural-language instruction, and observed task proficiency can all encode “how” differently. They should not receive one procedural label without representation and execution tests. |
| Prospective memory | Einstein and McDaniel operationalized prospective memory by asking participants to perform an action when a target event occurred, separately measuring retrospective memory ([Einstein & McDaniel, 1990](https://pubmed.ncbi.nlm.nih.gov/2142956/)). | A future-dated fact is not necessarily an intention; a machine analogue needs a pending commitment, a trigger condition, and completion, cancellation, or expiry semantics. |
| Event segmentation | Zacks and Tversky analyze events as temporally bounded units identified within continuous activity and discuss hierarchical event structure ([Zacks & Tversky, 2001](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/versky_Eventstructureinperceptionandconception.pdf)). | Software event boundaries may be supplied by a user, a sensor, a transaction, or a learned segmenter. The boundary's author and uncertainty must remain explicit. |
| Reconsolidation | In a rat auditory-fear-conditioning experiment, reactivated consolidated memories became vulnerable to protein-synthesis interference, supporting a retrieval-linked reconsolidation account in that paradigm ([Nader, Schafe & LeDoux, 2000](https://pubmed.ncbi.nlm.nih.gov/10963596/)). | Rewriting a database row after retrieval is not biological reconsolidation. A machine term must specify observable invalidation, derivation, or replacement effects rather than borrow the biological mechanism claim. |
| Forgetting | Ebbinghaus measured relearning savings over delay using controlled nonsense-syllable material and himself as the participant ([Ebbinghaus, 1885/1913 translation](https://archive.org/download/memorycontributi00ebbiuoft/memorycontributi00ebbiuoft.pdf)); a later direct replication examined the curve under closely related conditions ([Murre & Dros, 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4492928/)). | One human retention curve does not justify a universal machine decay rule. Machine forgetting may mean lower retrieval rank, loss of addressability, policy suppression, destructive erasure, or removal of learned influence. |

**LCMRP inference:** these traditions mix at least four kinds of classifier: representational content, functional role, time/persistence, and process. Their overlap is informative rather than an error. A machine taxonomy that forces every object into exactly one human-inspired leaf will discard operational facts.

## 4. Machine-memory proposals use incompatible organizing principles

The following primary systems and frameworks demonstrate that “memory” already names several non-equivalent machine constructs.

| Proposal | Source-defined organization | What it classifies well | Dimensions it leaves implicit or combines |
| --- | --- | --- | --- |
| Neural Turing Machine | A neural controller is coupled to an external matrix through differentiable attention-based reads and writes ([Graves, Wayne & Danihelka, 2014](https://arxiv.org/abs/1410.5401)). | Addressable external state and access mechanism. | Content type, authority, provenance, retention policy, and deletion. |
| Memory Networks | Inference components operate with readable and writable long-term memory; in the reported QA implementation it functions as a dynamic knowledge base ([Weston, Chopra & Bordes, 2014](https://arxiv.org/abs/1410.3916)). | Functional read/write interface and task use. | Why an item is admissible, its epistemic status, and whether “long-term” means duration, capacity, or architectural location. |
| Retrieval-Augmented Generation | Generation combines parametric memory in model weights with an explicit non-parametric memory accessed by retrieval ([Lewis et al., 2020](https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)). | Location/update-path distinction between weights and a retrievable corpus. | Event/semantic/procedural content, lifecycle, write authority, and item-level truth. |
| CoALA | Working memory is separated from long-term episodic, semantic, and procedural memories; internal actions are retrieval, reasoning, and learning ([Sumers et al., 2024](https://ar5iv.labs.arxiv.org/html/2309.02427v3)). CoALA explicitly treats procedural memory as both implicit model weights and explicit agent code. | Crosswalking cognitive-architecture functions to language-agent components. | Provenance, confidence, governance, safe deletion, and the difference between representation and demonstrated capability. Its own two forms of procedural memory show that one functional label can span incompatible update and audit paths. |
| Generative Agents | A natural-language memory stream is retrieved by recency, importance, and relevance; reflection derives higher-level material used with planning ([Park et al., 2023](https://dl.acm.org/doi/10.1145/3586183.3606763)). | Event-like records, derived reflections, and retrieval policy. | Source authority, calibration, conflict semantics, and destructive versus non-destructive consolidation. Believability evaluation is not a general memory-validity test. |
| Reflexion | Verbal feedback is retained in an “episodic memory buffer” and supplied to later trials without weight updates ([Shinn et al., 2023](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)). | Cross-trial use of textual feedback. | Whether the stored reflection is an episode, a derived semantic assertion, or a strategy. CoALA itself describes Reflexion's reflection as semantic knowledge, exposing a real label conflict rather than a clerical mismatch. |
| Voyager | An ever-growing library stores and retrieves executable code skills for later embodied tasks ([Wang et al., 2023](https://arxiv.org/abs/2305.16291)). | Explicit, compositional procedure artifacts. | Code authority, sandboxing, provenance, revocation, and the distinction between possessing code and reliably executing a skill. |
| MemGPT | Virtual context management moves information among memory tiers to present more context than the model window can hold ([Packer et al., 2023](https://arxiv.org/abs/2310.08560)). | Capacity/latency hierarchy and movement between tiers. | Epistemic status and content type; “main” and “external” memory are placement terms, not claims about meaning. |
| MemoryBank | A long-term interaction store is updated with a time-and-importance rule inspired by the Ebbinghaus forgetting curve ([Zhong et al., 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29946)). | A concrete admission, retrieval, and decay proposal for conversation history. | Whether the borrowed human curve transfers beyond its source conditions, plus user authority, deletion assurance, and independent confidence. |
| HippoRAG | A retrieval framework combines LLM extraction, a knowledge graph, and Personalized PageRank under an analogy to hippocampal indexing ([Gutiérrez et al., 2024](https://arxiv.org/abs/2405.14831)). | Associative, graph-based multi-hop retrieval. | Biological equivalence and broader memory lifecycle; the source describes inspiration, not a demonstration that the machine components instantiate the corresponding neural mechanisms. |
| MemOS | This 2025 preprint proposes parametric, activation, and plaintext memory as three operational forms managed through a common abstraction ([Li et al., 2025](https://arxiv.org/abs/2505.22101)). | Representation/location classes spanning weights, runtime state, and explicit text. | Peer-reviewed validation, stable boundaries for non-text structured artifacts, and governance semantics. It is relevant prior art, not an adopted or independently validated standard. |

**Reproduced source claim:** CoALA notes that modifying and deleting language-agent memory were understudied in its reviewed systems ([section 4.5](https://ar5iv.labs.arxiv.org/html/2309.02427v3)). **LCMRP inference:** authority, provenance, contradiction, and deletion therefore cannot be treated as optional annotations added after a cognitive or storage hierarchy is fixed; they can change which operations are valid for otherwise identical content.

## 5. Competing taxonomy organizations

These are competing ways M1 could organize the same systems. None is selected.

| Organization | Primary classifier | Benefit | Predictable failure case |
| --- | --- | --- | --- |
| Human-functional hierarchy | Working, episodic, semantic, procedural, prospective | Connects categories to candidate behavioral tests and a long research history. | A reflection derived from an episode can be event-linked, semantic, and action-guiding at once. Consciousness-dependent definitions do not transfer directly. |
| Storage/representation hierarchy | Parameters, activations/context, explicit text, vectors, graphs, code, archives | Makes update cost, addressability, portability, and erasure surfaces visible. | The same proposition copied into text, a graph, and parameters becomes three “memories” despite serving one role; representation says nothing about authority or truth. |
| Temporal/persistence hierarchy | Decision-cycle, session, cross-session, archival/indefinite | Supports survival and retention tests. | Duration is policy- and environment-dependent. An unexpired but unreachable item and an expired but recoverable replica defeat simple short/long labels. |
| Lifecycle/state hierarchy | Observed, admitted, encoded, derived, retrievable, superseded, invalidated, archived, erased | Makes transition preconditions and audit events explicit. OAIS supplies a technology-independent archival comparison framework ([CCSDS 650.0-M-3, 2024](https://ccsds.org/Pubs/650x0m3.pdf)); W3C PROV supplies generation, use, derivation, attribution, and invalidation relations ([PROV-DM](https://www.w3.org/TR/prov-dm/)). | A state hierarchy alone does not say what an object means or what behavior it supports. Replicas may occupy different states simultaneously. |
| Claim/provenance graph | Observation, assertion, inference, support, conflict, source, derivation | Preserves why a claim exists and permits source-sensitive contradiction handling. PROV is domain-agnostic but provenance consistency is not truth validation ([PROV-CONSTRAINTS](https://www.w3.org/TR/prov-constraints/)). | Procedures, opaque learned parameters, active goals, and non-propositional sensory traces fit poorly if every memory is forced to be a belief claim. |
| Governance/security organization | Subject, object, action, policy, permission, prohibition, duty, sensitivity, tenant | Makes read/write/consolidate/delete authority and threat boundaries testable. NIST ABAC evaluates subject, object, operation, and environment attributes against policy ([SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)); ODRL represents permissions, prohibitions, and duties over assets ([ODRL 2.2](https://www.w3.org/TR/odrl-model/)). | A policy view cannot replace content, temporal, or epistemic semantics. Permission to write is not evidence that a write is true or safe. |
| Orthogonal faceted taxonomy | Separate coordinates for role, content, time, process, persistence, authority, and provenance/epistemic status | Avoids forcing non-exclusive properties into one inheritance tree and allows missing values to remain explicit. | More labels, cross-facet integrity rules, and adjudication cost. It should be rejected if it does not improve agreement, prediction, or boundary-case coverage over simpler organizations. |

**LCMRP inference:** the faceted option currently covers the observed conflicts with fewer semantic overloads, but that is a design hypothesis, not a result. A lightweight SKOS concept scheme and a logic-bearing ontology also serve different purposes: SKOS explicitly supports informal concept schemes and warns that their links are not automatically formal domain axioms ([SKOS Reference](https://www.w3.org/TR/skos-reference/)). OWL can express formal class axioms ([OWL 2](https://www.w3.org/TR/owl2-syntax/)), while SHACL validates declared graph constraints ([SHACL](https://www.w3.org/TR/shacl/)). Choosing one representation must not silently upgrade an informal vocabulary into a proved theory.

## 6. Provisional facets to compare, not adopt

The following coordinates are a search-derived comparison scaffold. They do not define the M1 object model.

| Facet | Candidate values or questions | Observable discriminator | Source anchor and caution |
| --- | --- | --- | --- |
| Functional role | Maintain active state; recall prior experience; supply general knowledge; alter behavior; trigger a future commitment; preserve identity/preference continuity | Which downstream operation or behavior fails when this item is withheld while other facets are held fixed? | Working-memory, prospective-memory, and CoALA distinctions motivate role tests, but role is not representation. |
| Representational content | Observation/event; proposition; derived summary; procedure/policy; intention/goal; preference; index; model parameter; activation | Can the content be truth-evaluated, executed, awaited on a trigger, replayed as an event, or only used as an opaque state contribution? | Tulving, Cohen–Squire, Voyager, RAG, and MemOS motivate different values. One artifact may contain several content units. |
| Temporal scope | Current decision cycle; bounded task; session; cross-session; indefinitely retained; validity interval; transaction interval | Does it survive a call, decision cycle, process restart, session boundary, account boundary, and declared retention horizon? When was the claim true versus when was it recorded? | Temporal-database terminology separates valid time from transaction time ([Jensen et al., 1992](https://sigmodrecord.org/publications/sigmodRecord/9209/pdfs/140979.140996.pdf)). “Long-term” without a survival test is underspecified. |
| Lifecycle/process | Candidate; admitted; encoded; deduplicated; derived/consolidated; retrieved; revised; superseded; invalidated; archived; logically hidden; sanitized | Which transition occurred, under whose authority, from which inputs, and is the prior representation still addressable or recoverable? | PROV and OAIS model parts of this space, but neither is by itself a cognitive-memory lifecycle. |
| Persistence/location | Prompt/context; runtime activation or state; process-local store; external addressable store; replicated archive; model parameters; executable artifact | Can a discrete item be enumerated, copied, versioned, and removed without changing model parameters? Which failure or restart boundaries does it survive? | RAG's parametric/non-parametric distinction, MemGPT's tiers, and MemOS's proposal are competing cuts, not synonyms. |
| Authority/control | Proposer, subject, source, admission authority, reader, reviser, consolidator, deleter, override authority; policy constraints and tenant scope | Would the same operation be permitted if actor, purpose, tenant, source, or environment changed while content stayed identical? | ABAC and ODRL show why actor, operation, asset, and policy must be represented separately. They do not determine cognitive value. |
| Provenance/epistemic status | Direct observation; user report; tool report; imported assertion; model inference; hypothesis; policy; source authority; confidence; support/conflict; derivation | Can two byte-identical claims differ in admissibility because origin or derivation differs? Can confidence change without source or content changing? | PROV records production history, not truth. Neural confidence calibration concerns correspondence between confidence and empirical correctness, not source authority ([Guo et al., 2017](https://proceedings.mlr.press/v70/guo17a.html)). |

Two additional overlays appear necessary but are not proposed as memory kinds: **security/privacy classification** (sensitivity, tenant, threat exposure, retention duty) and **quality/evaluation state** (tested scope, calibration evidence, known contradictions). Treating either as content would conflate governance or evidence with what is remembered.

## 7. Observable distinctions

Each distinction below is a candidate competency question for a later frozen taxonomy evaluation.

1. **Context versus retrievable memory:** after removing the item from the immediate prompt and starting a fresh model call, can an identified operation recover it from maintained system state? If not, it was available context but has not demonstrated cross-call memory.
2. **Working state versus context window:** can structured active goals or intermediate variables persist across model calls and be selectively projected into a prompt? If yes, the agent has an active-state facility beyond the model's raw token window; this still does not prove equivalence to human working memory.
3. **Episodic versus semantic content:** does the item preserve a particular occurrence, temporal/spatial context, participants, and source, or assert a decontextualized generalization? An event can entail a proposition, and a record may legitimately contain both.
4. **Procedure description versus executable procedure:** holding environment and permissions fixed, can the artifact be invoked to produce a state transition, or is it only a proposition about how one might act? Natural-language instructions and code should not be assumed equivalent.
5. **Prospective commitment versus future fact:** is there an authorized pending action with trigger, completion, cancellation, and expiry semantics, or only a proposition about the future?
6. **Retrieval versus reconstruction:** are returned bytes or structured fields identical to an admitted artifact, deterministically transformed with recorded provenance, or newly generated? These outcomes have different error and deletion implications.
7. **Consolidation versus lossy summary:** are source objects linked to a newly derived object, are they retained, and can the derivation be reversed or audited? A shorter text alone does not establish consolidation.
8. **Revision versus supersession versus contradiction:** was an existing assertion mutated, was a new version linked to the old, or do two concurrently valid source claims conflict? The operations require different history semantics.
9. **Forgetting versus access suppression versus deletion:** did retrieval probability fall, did policy hide an addressable item, did the logical record disappear, did all replicas become infeasible to recover, or was learned influence removed? These outcomes must not share one unqualified “forgotten” state.
10. **Provenance versus authority versus confidence:** who or what produced the item, who may operate on it, and how well a score predicts correctness are three independently variable questions.
11. **Parametric versus explicit memory:** can the contribution be identified and removed as a discrete record without retraining or editing parameters? If not, record-level lifecycle operations do not automatically apply.
12. **Stored versus behaviorally effective:** does withholding the item under a controlled replay change retrieval output, decision quality, or action? Existence in a store is not evidence of functional use.
13. **Valid time versus record time:** when a user corrects a birth date today, the asserted real-world date and the correction's database time differ. A single timestamp cannot express both histories.
14. **Logical invalidation versus physical sanitization:** can authorized software still address the data, can ordinary recovery restore it, and can a declared adversary recover it with a stated effort? NIST defines media sanitization relative to making access infeasible for a given level of effort ([SP 800-88 Rev. 2](https://csrc.nist.gov/pubs/sp/800/88/r2/final)).

## 8. Operational edge cases

| Edge case | Classifier collision | Required observation before adjudication |
| --- | --- | --- |
| A user utterance contains a stable preference and an instruction embedded in quoted untrusted text. | One event contains candidate semantic preference content and a possible security payload. | Source spans, quoting/derivation, admission authority, instruction/data boundary, and whether either unit was admitted. |
| A reflection summarizes five episodes, then one source episode is retracted. | “Semantic memory” is derived from episodic inputs but may now be unsupported. | Derivation graph, aggregation rule, source version, recomputation behavior, and whether the reflection is invalidated or revised. |
| Two sources make the same claim with different authority and confidence. | Byte-identical content is not one epistemic object. | Independent provenance, source authority, calibration basis, tenant, and support/conflict relations. |
| A retrieved document appears in a prompt but the agent never stores it. | Retrieval input may be called semantic memory even though it is transient context for this agent. | Ownership, persistence boundary, later addressability, and whether the external corpus or the agent is the memory-bearing system. |
| A tool result was correct when recorded but the upstream source later invalidates it. | Past episode remains historically accurate while its current semantic use is unsafe. | Valid time, transaction time, invalidation notice, source-sensitive retrieval, and downstream derivations. |
| A code skill is stored as text but execution is disabled by policy. | Procedural representation exists without current procedural capability. | Executability, permissions, interpreter, environment preconditions, and behavioral test. |
| A future reminder's trigger passes while the system is offline. | Prospective content persists, but trigger semantics are ambiguous. | Delivery policy, missed-trigger behavior, expiry, idempotence, and completion record. |
| An item is deleted from the primary index but remains in a cache, backup, embedding index, and derived summary. | Logical deletion, physical erasure, and derivation invalidation diverge. | Replica inventory, deletion propagation, recovery test, derivation graph, retention exception, and sanitization assurance. |
| A fact is absent from an RDF graph. | Closed-world software may treat absence as false; RDF semantics do not generally license that conclusion. | Declared entailment regime and completeness boundary; RDF supplies model-theoretic truth preservation, not an application-specific closed-world rule ([RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-mt/)). |
| The model reproduces sensitive training text although no external record exists. | Parametric memorization creates privacy exposure without an enumerable memory object. | Extraction behavior, model/version provenance, training-data lineage, and an influence-removal test. Training-data extraction has been demonstrated against a large language model in a primary security study ([Carlini et al., 2021](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)). |
| A malicious record is crafted to dominate similarity retrieval only for a trigger. | Relevance and behavioral usefulness look normal on benign inputs while provenance and integrity are compromised. | Admission path, source authentication, trigger-conditioned retrieval, held-out benign behavior, and attacker capabilities. AgentPoison demonstrates this attack class against long-term memory or RAG knowledge bases ([Chen et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/eb113910e9c3f6242541c1652e30dfd6-Paper-Conference.pdf)). |
| One shared memory store accidentally returns another user's preference. | Semantically relevant retrieval is a cross-tenant authorization failure. | Subject, tenant, purpose, policy decision, provenance, and audit trail; content relevance cannot authorize disclosure. |
| A generated answer cites a stored source but adds an unsupported detail. | Retrieval provenance is incorrectly inherited by new generation. | Claim-level source alignment, transformation record, unsupported spans, and separate confidence. |
| A preference changes over time rather than being contradicted. | Latest-value replacement destroys legitimate temporal evolution. | Validity intervals, user authority, context, explicit correction versus preference drift, and historical-query semantics. |
| A “memory” is retrieved but ignored by the decision procedure. | Storage and recall occur without behavioral effect. | Controlled ablation holding model, seed, prompt construction, and other inputs fixed. |

These cases are examples, not evidence. A later study must freeze positive and negative cases, add held-out cases, define adjudicator independence, and prohibit post hoc category edits made after disagreements are seen.

## 9. Category conflicts and unresolved obligations

### 9.1 Content, function, and representation conflict

- “Episodic,” “semantic,” and “procedural” may describe content, a subsystem, an access route, or a behavioral capacity. The taxonomy must select and state which reading applies.
- Reflexion's own “episodic buffer” terminology and CoALA's semantic reading of the stored reflections show that paper labels alone cannot adjudicate a category.
- Code, model weights, demonstrations, and natural-language instructions can all affect future behavior. It remains unresolved whether they share a procedural role facet while retaining distinct representation values, or require narrower terms.
- A context window, an agent's cross-call working state, and a human working-memory theory have different necessary conditions. Their exact common denominator is unresolved.

### 9.2 Time and identity conflict

- “Short-term” and “long-term” lack product-independent thresholds. Survival boundaries and declared retention horizons are more testable than adjectives, but the minimal required tests are not yet fixed.
- Valid time, transaction time, event time, ingestion time, retrieval time, and deletion time can all differ. The formal model must define which clocks are authoritative and how uncertainty or missing times are represented.
- A preference change, factual correction, source contradiction, and identity hijack can produce identical text diffs but require different authority and history treatment.

### 9.3 Lifecycle conflict

- Admission, encoding, deduplication, consolidation, retrieval, reconsolidation, decay, archival, and deletion may be activities, policies, or resulting states. Treating process names as object kinds would make transition rules circular.
- Mutating an object in place conflicts with immutable provenance and longitudinal reproducibility; retaining every superseded version conflicts with some erasure obligations. The necessary separation between evidence history, operational memory, and protected audit metadata remains unresolved.
- NIST media sanitization concerns recoverability from media, while machine unlearning concerns influence in learned models. Certified-removal work defines removal relative to indistinguishability from a model that did not observe the data in a bounded setting ([Guo et al., 2020](https://arxiv.org/abs/1911.03030)); SISA training limits and partitions training influence to expedite later unlearning ([Bourtoule et al., 2021](https://arxiv.org/abs/1912.03817)). Neither result makes external-record deletion, model unlearning, and legal erasure synonymous.

### 9.4 Provenance and epistemic conflict

- W3C PROV can represent entities, activities, agents, derivations, responsibility, and provenance bundles, but a valid PROV graph establishes a consistent provenance history, not that its assertions are true.
- Confidence, probability, retrieval score, salience, source authority, and evidential support are non-interchangeable. Each needs a declared target and calibration or validation procedure.
- Classical belief-revision work distinguishes contraction and revision operations under explicit rationality postulates ([Alchourrón, Gärdenfors & Makinson, 1985](https://doi.org/10.2307/2274239)); truth-maintenance systems retain dependency justifications while revising active beliefs ([Doyle, 1979](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a)). Whether LCMRP should preserve mutually inconsistent claims, select an active belief set, or support both views at different layers remains unresolved.
- Open-world semantic models do not infer falsity from absence, while operational databases and policy engines often require bounded completeness. The formal model must declare the reasoning regime rather than inherit one from a serialization.

### 9.5 Biological analogy conflict

- Human categories can depend on consciousness, neuroanatomy, and experimental dissociations absent from machine systems.
- Architecture papers that say “inspired by” human memory establish a design analogy, not biological equivalence. M1 must record the mapping and its excluded biological claims for every borrowed term.
- Human forgetting measurements do not choose a safe machine-retention policy. Machine policies must additionally account for provenance, user authority, adversarial persistence, replicas, and demonstrable deletion.

## 10. Security, privacy, and governance implications

Memory classification affects the threat model because the same content in different persistence and authority facets creates different attack surfaces.

- **Admission and poisoning:** NIST's adversarial-ML taxonomy organizes attacks by lifecycle stage, goals, capabilities, and knowledge and includes poisoning, privacy, evasion, and generative-AI misuse classes ([NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025)). AgentPoison supplies direct evidence that a retrieval memory or knowledge base can be backdoored without model training. These sources support modeling attacker capability and lifecycle stage; they do not establish that any proposed LCMRP control is effective.
- **Query-only injection:** MINJA is a primary 2025 manuscript proposing injection of malicious records through normal agent interactions without direct memory-bank modification ([Dong et al., 2025](https://arxiv.org/abs/2503.03704)). Its status and scope must be retained when cited; it is not an independently reproduced universal attack rate.
- **Access control:** read, write, derive, execute, consolidate, export, and delete are distinct operations. ABAC demonstrates that authorization can depend on actor, object, operation, and environment. A single `owner` field cannot express all required decisions.
- **Provenance integrity:** a recorded source identifier is not source authentication, and a signed source is not necessarily truthful. Integrity, origin, authority, and epistemic confidence require separate tests.
- **Cross-user leakage:** relevance must be evaluated only after tenant and policy filtering. Otherwise better retrieval can worsen confidentiality.
- **Sensitive learned influence:** extracting training examples from model parameters shows why “no row exists” does not imply that sensitive information cannot be reproduced. Parametric and explicit memory need different deletion verification.
- **Erasure and retention:** Article 17 of the GDPR is one jurisdiction-specific source of erasure obligations and exceptions ([official consolidated text](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02016R0679-20160504)). It is not a universal taxonomy definition. The model must be capable of representing applicable authority, purpose, exception, scope, and proof of action without embedding one jurisdiction as the general architecture.
- **Audit versus erasure:** protecting a minimal audit record can conflict with deleting content and derived copies. M1 must distinguish content, provenance needed to locate derivatives, proof-of-deletion metadata, and recoverable payload; it must not assume the conflict is always resolvable.

## 11. Falsifiable comparison questions

These questions are candidate inputs to a future preregistered structural/taxonomy evaluation. Thresholds and datasets have not been selected.

1. **Agreement:** On frozen positive, negative, and adversarial cases, does a faceted taxonomy produce higher independent inter-rater agreement than a single human-functional hierarchy? Reject the claimed advantage if agreement does not improve outside the development cases.
2. **Operational prediction:** Do assigned categories predict supported operations—cross-session retrieval, exact replay, execution, contradiction handling, version-aware update, and verified deletion—better than representation-only or duration-only baselines? Reject categories that add no held-out predictive value.
3. **Collision rate:** How often does one label map to artifacts with materially different update, authority, or deletion behavior? A taxonomy that retains high within-label operational variance needs narrower definitions or additional facets.
4. **Facet necessity:** When each proposed facet is ablated, does held-out classification lose an independently observable distinction? Remove facets whose values are derivable from others under all declared cases.
5. **Architecture portability:** Can the same competency questions classify a parameter-only model, a RAG system, an explicit event store, a code-skill agent, and a tiered-context agent without vendor- or database-specific terms? Reject portability if adjudicators must introduce implementation-specific exceptions.
6. **Temporal adequacy:** Can the model represent a late correction, evolving preference, missed future trigger, and retracted source without overwriting valid history or treating every difference as contradiction?
7. **Provenance adequacy:** Can two identical claims with different sources remain distinct, and can one derived summary be invalidated when only one input is retracted? Reject the provenance model if either case loses lineage.
8. **Authority adequacy:** Can the model express that an actor may propose but not admit, read but not export, or invalidate but not physically erase? Reject a single-owner model if it cannot distinguish these cases.
9. **Deletion adequacy:** Can an erasure request enumerate primary records, indexes, caches, replicas, derived artifacts, and parametric influence while reporting different verification statuses rather than one success flag?
10. **Biological-analogy discipline:** For each human-derived term, can an adjudicator identify at least one retained operational property and one excluded biological property? Reject borrowed terms that cannot pass both checks.
11. **Security coverage:** Do authority and provenance facets expose poisoned-admission and cross-tenant retrieval failures that a content-only baseline misses on held-out attack cases?
12. **Longitudinal stability:** When a definition is versioned, can completed case decisions still resolve against their exact prior definition without silent reinterpretation?

No positive answer is presumed. Null results, lower agreement, redundant facets, and cases that remain unclassifiable would be valid outputs.

## 12. Limitations

- The search is broad but not exhaustive or systematic; absence from this map is not evidence that prior art does not exist.
- Older human-memory sources use theoretical commitments and experimental populations that cannot be generalized to machines without new operational definitions.
- Several machine-memory works are framework or architecture proposals, and some are preprints. Their inclusion establishes terminology and competing design choices, not replication or robustness.
- Standards were selected for relevant concepts, not because an LCMRP taxonomy must serialize as RDF/OWL, implement PROV, use ABAC/ODRL, or adopt OAIS.
- The map does not compare benchmark performance, implementation cost, latency, storage, compute, or token use.
- Legal examples are illustrative and jurisdiction-dependent, not legal advice or a complete governance analysis.
- No real memory objects, human participants, private data, model calls, datasets, adjudicators, or experiments were used.
- No prior-art search can establish that a future LCMRP combination is novel; a claim-specific search would still be required before any novelty statement.

## 13. Evidence status

This artifact remains a non-evidentiary M1 research input. It records reproduced source claims, provisional inferences, and unresolved obligations. It awards no mechanism maturity label, registers no subject or study, reports no finding, and validates no taxonomy. The production registries remain outside this artifact and must not be changed on its authority.

## 14. Recommended next foundational study

Design a versioned `STRUCTURAL_OR_TAXONOMY_EVALUATION` around a frozen candidate subject rather than treating this synthesis as the subject itself. Before freeze:

1. select at least two explicit competing organizations, including a simpler baseline;
2. publish versioned definitions and integrity constraints;
3. freeze representative positive, negative, multi-label, missing-value, and adversarial cases, with a held-out set;
4. preregister competency questions covering the observable distinctions in section 7;
5. define independent adjudication, disagreement handling, coverage, and rejection criteria;
6. require every human-derived term to state the retained analogy and excluded biological claim;
7. measure agreement, coverage, operational prediction, collision rate, and facet-ablation effects; and
8. preserve null, contradictory, and unclassifiable outcomes in atomic findings and an immutable closeout.

The study should reject the faceted design if its extra complexity does not yield reproducible distinctions or held-out operational value.

## 15. Primary and authoritative source index

### Human memory

- R. C. Atkinson and R. M. Shiffrin, [“Human Memory: A Proposed System and Its Control Processes”](https://www.sciencedirect.com/science/chapter/bookseries/pii/S0079742108604223) (1968).
- A. D. Baddeley and G. Hitch, [“Working Memory”](https://www.sciencedirect.com/science/chapter/bookseries/pii/S0079742108604521) (1974).
- E. Tulving, [“Episodic and Semantic Memory”](https://alicekim.ca/12.EpSem72.pdf) (1972), and [“Memory and Consciousness”](https://doi.org/10.1037/h0080017) (1985).
- N. J. Cohen and L. R. Squire, [“Preserved Learning and Retention of Pattern-Analyzing Skill in Amnesia”](https://pubmed.ncbi.nlm.nih.gov/7414331/) (1980).
- G. O. Einstein and M. A. McDaniel, [“Normal Aging and Prospective Memory”](https://pubmed.ncbi.nlm.nih.gov/2142956/) (1990).
- J. M. Zacks and B. Tversky, [“Event Structure in Perception and Conception”](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/versky_Eventstructureinperceptionandconception.pdf) (2001).
- K. Nader, G. E. Schafe, and J. E. LeDoux, [“Fear Memories Require Protein Synthesis in the Amygdala for Reconsolidation After Retrieval”](https://pubmed.ncbi.nlm.nih.gov/10963596/) (2000).
- H. Ebbinghaus, [*Memory: A Contribution to Experimental Psychology*](https://archive.org/download/memorycontributi00ebbiuoft/memorycontributi00ebbiuoft.pdf) (1885; English translation 1913).

### Machine and agent memory

- A. Graves, G. Wayne, and I. Danihelka, [“Neural Turing Machines”](https://arxiv.org/abs/1410.5401) (2014).
- J. Weston, S. Chopra, and A. Bordes, [“Memory Networks”](https://arxiv.org/abs/1410.3916) (2014).
- P. Lewis et al., [“Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”](https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) (2020).
- T. R. Sumers et al., [“Cognitive Architectures for Language Agents”](https://arxiv.org/abs/2309.02427) (TMLR camera-ready version, 2024).
- J. S. Park et al., [“Generative Agents: Interactive Simulacra of Human Behavior”](https://dl.acm.org/doi/10.1145/3586183.3606763) (2023).
- N. Shinn et al., [“Reflexion: Language Agents with Verbal Reinforcement Learning”](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) (2023).
- G. Wang et al., [“Voyager: An Open-Ended Embodied Agent with Large Language Models”](https://arxiv.org/abs/2305.16291) (2023).
- C. Packer et al., [“MemGPT: Towards LLMs as Operating Systems”](https://arxiv.org/abs/2310.08560) (2023).
- W. Zhong et al., [“MemoryBank: Enhancing Large Language Models with Long-Term Memory”](https://ojs.aaai.org/index.php/AAAI/article/view/29946) (2024).
- B. J. Gutiérrez et al., [“HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models”](https://arxiv.org/abs/2405.14831) (2024).
- Z. Li et al., [“MemOS: An Operating System for Memory-Augmented Generation in Large Language Models”](https://arxiv.org/abs/2505.22101) (preprint, 2025).

### Provenance, temporal data, policy, formal knowledge, and security

- W3C, [PROV-DM](https://www.w3.org/TR/prov-dm/) and [PROV-CONSTRAINTS](https://www.w3.org/TR/prov-constraints/) (Recommendations, 2013).
- C. S. Jensen et al., [“A Glossary of Temporal Database Concepts”](https://sigmodrecord.org/publications/sigmodRecord/9209/pdfs/140979.140996.pdf) (1992).
- CCSDS, [Reference Model for an Open Archival Information System, CCSDS 650.0-M-3](https://ccsds.org/Pubs/650x0m3.pdf) (Recommended Practice, 2024).
- NIST, [SP 800-162, Guide to Attribute Based Access Control](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) (updated 2019).
- W3C, [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) (Recommendation, 2018).
- W3C, [SKOS Reference](https://www.w3.org/TR/skos-reference/) (2009), [OWL 2 Structural Specification](https://www.w3.org/TR/owl2-syntax/) (2012), [RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-mt/) (2014), and [SHACL](https://www.w3.org/TR/shacl/) (2017).
- C. E. Alchourrón, P. Gärdenfors, and D. Makinson, [“On the Logic of Theory Change”](https://doi.org/10.2307/2274239) (1985).
- J. Doyle, [“A Truth Maintenance System”](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a) (1979).
- C. Guo et al., [“On Calibration of Modern Neural Networks”](https://proceedings.mlr.press/v70/guo17a.html) (2017).
- NIST, [AI 100-2e2025, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*](https://doi.org/10.6028/NIST.AI.100-2e2025) (2025).
- Z. Chen et al., [“AgentPoison: Red-Teaming LLM Agents via Poisoning Memory or Knowledge Bases”](https://proceedings.neurips.cc/paper_files/paper/2024/file/eb113910e9c3f6242541c1652e30dfd6-Paper-Conference.pdf) (2024).
- S. Dong et al., [“A Practical Memory Injection Attack against LLM Agents”](https://arxiv.org/abs/2503.03704) (primary manuscript, 2025).
- N. Carlini et al., [“Extracting Training Data from Large Language Models”](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting) (2021).
- C. Guo et al., [“Certified Data Removal from Machine Learning Models”](https://arxiv.org/abs/1911.03030) (2020), and L. Bourtoule et al., [“Machine Unlearning”](https://arxiv.org/abs/1912.03817) (2021).
- NIST, [SP 800-88 Rev. 2, *Guidelines for Media Sanitization*](https://csrc.nist.gov/pubs/sp/800/88/r2/final) (2025).

