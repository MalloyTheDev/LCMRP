# What you need to do (solo coding path)

Research goal: better lifelong AI memory (human-inspired durability, not just longer context).  
This step: **exploratory structural self-check of your Memory Taxonomy candidate** under the honest solo+AI method.

## Already done for you (on branch `agent/m1-taxonomy-solo-ai-method-v3`)

1. Method freeze package **v3** (solo human + AI tooling) — PR #33 if not merged yet  
2. **Live solo intake** (drafted as you / MalloyTheDev):  
   - `studies/foundational/m1-taxonomy-v1/execution/execution-intake-solo.json`  
   - Receipt: `execution-intake-solo.receipt.json` (digest `929b91025df641388b4a79c71cfa6e50ed5827b741c9d18f727f13b03355c7de`)  
3. **Provisional term-contract ledger** (165 cells = 33 terms × 5 checks):  
   - `studies/foundational/m1-taxonomy-v1/execution/work/term-contract-ledger.provisional.json`  
   - All cells: `PROVISIONAL_AI_DRAFT_AWAITING_HUMAN_ACCEPT`  
   - AI drafted codes; **you** must accept or change them  

## Your required actions (in order)

### A. Confirm identity and declarations (required)

Open `execution-intake-solo.json` and verify these are true; edit if not:

- [ ] `contributor_id` is the ID you want on the scientific record  
- [ ] Dual-role statements (you authored/froze) are accurate  
- [ ] AI tooling disclosure matches how you work  
- [ ] You accept **exploratory** limits (not multi-rater independent validation)

If you edit the intake JSON, tell me and I will **recompute the receipt digest**.

### B. Accept or revise provisional codes (required before lock)

Open:

`studies/foundational/m1-taxonomy-v1/execution/work/term-contract-ledger.provisional.json`

(165 cells = 33 terms × 5 checks). Do **not** invent a locked file under `outputs/` yet.

For each cell (or in batches), either:

- leave code as-is and set `"status": "HUMAN_ACCEPTED"`, or  
- change `code` / `rationale` and set `"status": "HUMAN_REVISED"`

**Codes:** `SATISFIED` | `CHALLENGED` | `AMBIGUOUS` | `NOT_APPLICABLE` | `INVALID_CASE`

**Meaning of the five checks** (per frozen category rules):

1. Unique versioned ID  
2. Bounded definition without named product/vendor/impl  
3. Necessary-condition status Proposed/Unknown (not silent universal truth)  
4. Sufficient-condition status Proposed/scoped/Unknown (not external validity)  
5. Challengeable via distinction / counterexample / edge / unresolved obligation  

### C. Tell me when a batch is done

Reply e.g.:

- `accept all provisional term-contract cells`  
- or `accepted ENT-*; revise ROL-001 check 2 to CHALLENGED because ...`

Then I will:

1. Apply your decisions  
2. Lock the ledger (raw-byte digest)  
3. Draft the exploratory finding record  
4. Move to the next analysis  

### D. Optional: merge PR #33 first

If v3 is not on `main` yet, merge https://github.com/MalloyTheDev/LCMRP/pull/33 so the method freeze is canonical.

## What you should not do

- Do not treat AI provisional codes as final without review  
- Do not claim multi-rater reliability or independent validation  
- Do not skip intake edits if the drafted declarations are wrong  

## Files map

| File | Role |
| --- | --- |
| `execution/execution-intake-solo.json` | Your intake (edit if needed) |
| `execution/execution-intake-solo.receipt.json` | Digest receipt |
| `execution/HUMAN_ACTIONS.md` | This checklist |
| `execution/work/term-contract-ledger.provisional.json` | Analysis 1 provisional ledger (unlock until you accept) |
| `templates/foundational-execution-intake-solo.md` | Human-readable form |
