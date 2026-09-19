# AJSE EDITORIAL PRE-MORTEM

Target: Arabian Journal for Science and Engineering (AJSE), Computer Science and Engineering / Systems Engineering.

Official journal pages reviewed 19 September 2026:
- Aims and scope: https://link.springer.com/journal/13369/aims-and-scope
- Submission guidelines: https://link.springer.com/journal/13369/submission-guidelines

## Five likely desk-rejection arguments and the required answer

### 1. "Determinism/reproducibility is already known; where is the engineering contribution?"
Required answer: the paper is not a generic repeatability warning. It isolates execution-path composition while holding the target prompt, model revision, decoding rule and scorer fixed; it distinguishes bit/text, normalized-text and final-decision reproducibility; and it measures within-path repeatability separately from between-path divergence.

### 2. "This is just a benchmark anecdote."
Required answer: two independently developed open model families, four task families, 600 frozen targets per model, four execution paths, duplicate executions, fixed companion construction and 100,000-resample inference. Every model × benchmark cell is reported.

### 3. "Batch effects could be confounded by changed prompts."
Required answer: the runner verifies the target's exact non-padding token IDs under every batch condition. Only surrounding batch composition/padding geometry changes.

### 4. "The study is outcome-selected."
Required answer: public protocol, model/data revisions, frozen item hashes, companion-plan hashes, endpoints and analysis code all predate endpoint generation. Null or adverse results are retained.

### 5. "This duplicates another manuscript."
Required answer: Nature firewall. No RIDI, allocation-identity theorem, frontier, EPSS, CMS, Nature RAG panel, Nature Qwen results, Nature figures/tables/query rows or numerical results are used. The paper is disclosed to Nature later as a related but empirically separate manuscript.

## Manuscript discipline for AJSE

- Research Article, not Technical Note.
- Abstract 150–250 words.
- Engineering framing from title through discussion.
- Primary figures must show execution-path effect sizes and uncertainty, not decorative benchmark leaderboards.
- Methods must be sufficient for exact independent replay.
- AI/LLM use disclosure follows Springer instructions.
- Four conflict-free international reviewer suggestions will be prepared from different institutions/countries.
- Do not submit until raw artifacts, environment manifest and analysis outputs are frozen.
