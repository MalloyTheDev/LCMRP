# Study: H4-Oracle — reasoning ceiling on LongMemEval with supplied evidence

A scoped first step toward hypothesis **H4** (see [`../../docs/HYPOTHESES.md`](../../docs/HYPOTHESES.md)).
It runs on the CorpusStudio evaluation harness on local hardware. This card is
the **preregistration** (§1–4, committed before the run) and becomes the
**report** (§5–8) once the run completes. See [`METHOD.md`](../../METHOD.md).

- **Status:** Planned (preregistration committed; run pending on the local GPU)
- **Date planned:** 2026-07-24 · **Date completed:** —
- **Hypothesis:** H4-Oracle (a sub-question of H4, below)
- **Evidence label (target / achieved):** E1 → E2 · `[AI-assisted]`

## 1. Question

Full H4 asks whether FMO-style provenance/temporal memory *retrieval* improves
knowledge-update and temporal accuracy. Before building any retrieval layer, we
need the **reasoning ceiling**: when the gold evidence is *supplied* (the
LongMemEval `_oracle` setting), how accurately does the base model answer, by
question type?

**Falsifiable sub-hypothesis:** with oracle evidence supplied, the model
answers **non-abstention** questions at high accuracy (pre-registered threshold:
**≥ 80%** overall on non-abstention types). If it does, LongMemEval failures are
dominated by *retrieval*, not *reasoning* — which is the premise full H4 depends
on. If oracle accuracy is already low, the bottleneck is reasoning, and no
memory-retrieval structure (flat or FMO) can be the main lever — which would
**refute the premise of full H4** and redirect the work.

## 2. Inputs (pinned)

Pin exact SHA-256 at run time (the dataset is downloaded on the GPU host, not
stored here).

| Input | Identifier | Pin |
|---|---|---|
| Dataset | LongMemEval `_oracle` (evidence-only) — https://github.com/xiaowu0162/longmemeval | `sha256:<fill at run>` |
| Converter | `convert_longmemeval.py` (this folder) | `sha256:<fill at run — sha256sum the file>` |
| Model | `Qwen/Qwen2.5-7B` at a pinned HF revision `<commit>` | — |
| Harness | CorpusStudio `corpus-studio eval-run`, commit `<sha>` | — |

**Compute (disclosed):** RTX 5070 (Blackwell, sm_120, ~12 GB), CUDA 12.8,
Python 3.12. This is a local single-GPU run; it is **not** an independent
replication. The model is a local **Qwen2.5-7B** — disclosed because the
result is model- and decode-specific.

## 3. Method

1. Convert the LongMemEval `_oracle` JSON to CorpusStudio `instruction` JSONL:
   `python convert_longmemeval.py longmemeval_oracle.json -o oracle.instruction.jsonl --max-input-chars 12000`.
   Each row: question → `instruction`, evidence sessions → `input`, gold →
   `output`, `question_type` → `tags` (so per-type accuracy is free via the
   harness `tag_summary`). Rows are evidence-only, so they fit within seq-4096.
2. Serve the base model (vLLM, OpenAI-compatible endpoint) **or** run the
   adapter/base in-process (4-bit nf4). Decode is fixed and recorded:
   **temperature 0 (greedy), seed 0, max_output_tokens 256.**
3. Score with **two metrics, reported side by side** (robustness — a single
   metric is the fragile choice):
   - **Primary — LLM judge** (`--judge-model <evaluator>`), matching
     LongMemEval's own GPT-judge methodology; handles paraphrase.
   - **Secondary — deterministic** exact-match / normalized token-F1, for
     reproducibility. (This scorer is a small addition to the CorpusStudio eval
     engine — `scorers.py` + `cli.py`, contract name `exact_match` — landing in a
     separate CorpusStudio PR; day-one the run is fully executable with the judge
     alone.)
   Where the two disagree on a row, that row is flagged for inspection, not
   silently averaged.
4. Report **per `question_type`** (single-session-user/-assistant/-preference,
   multi-session, temporal-reasoning, knowledge-update) plus **abstention**
   precision separately (abstention is a distinct ability, not accuracy).

Example run (day-one, judge-only):
```bash
corpus-studio eval-run oracle.instruction.jsonl instruction \
  --model Qwen2.5-7B --backend openai-compatible --base-url http://localhost:8000/v1 \
  --judge-model <evaluator> --judge-backend openai-compatible --judge-base-url <...> \
  --temperature 0 --seed 0 --max-output-tokens 256 \
  --output-path reports/h4-oracle.json --progress
```

**Confirmatory vs exploratory:** the §1 threshold test is *confirmatory*. Any
per-category pattern-spotting done after seeing the numbers is *exploratory* and
will be labelled as such in §5.

## 4. What would confirm / refute

- **Confirms the sub-hypothesis** (→ pursue full H4 / FMO retrieval): overall
  non-abstention accuracy **≥ 80%**, judge and deterministic scorers agree
  within a stated margin, no single category collapsing.
- **Refutes it** (→ reasoning is the bottleneck, redirect away from retrieval as
  the main lever): overall non-abstention accuracy **< 80%**, or a core category
  (knowledge-update / temporal) well below the rest even *with* evidence in hand.
- **Invalid / not-run:** harness or serving errors → recorded as
  `unavailable`-with-reason (never a fabricated 0), per both projects' honesty
  rules.

<!-- Commit the card up to here BEFORE running the eval. -->

## 5. Results

_Pending the GPU run._ Fill: per-`question_type` accuracy (judge + deterministic),
abstention precision, overall non-abstention accuracy, judge/deterministic
agreement, and any `unavailable` rows with reasons. Report every category,
including weak ones.

## 6. Assessment

_Pending._ State the label (target E2) and, if E2, the verbatim caveat:
"Supported under a preregistered protocol; single-analyst, not independently
replicated." Never "validated." State the §1 verdict (confirm/refute) plainly.

## 7. Limitations

_Pending, but known in advance:_ single local model (Qwen2.5-7B) and decode; a
lexical secondary scorer is a proxy, not quality; oracle evidence is an upper
bound that a real retrieval layer will not match; single-GPU, not replicated.

## 8. How to replicate or falsify this

Fetch LongMemEval `_oracle`, verify its SHA-256, run the converter (its
self-test `python convert_longmemeval.py --selftest` should pass), serve
Qwen2.5-7B at the pinned revision, and run the `eval-run` command above with the
recorded decode. A different model or a real (non-oracle) retrieval setting that
scores materially differently would bound or overturn this result. Independent
adjudication (a second person re-running and re-scoring) is the path to **E3**.
