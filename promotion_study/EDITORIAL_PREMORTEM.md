# JKSUCIS EDITORIAL PRE-MORTEM

Target: Journal of King Saud University – Computer and Information Sciences.

Official guidance reviewed 19 September 2026:
- Aims/scope: https://cs.ksu.edu.sa/en/jksuci/about/aimsandscope
- Journal/information to authors: https://cs.ksu.edu.sa/en/node/2231

The journal emphasizes cutting-edge work across Machine Learning, NLP and Software Engineering, uses double-anonymized review, and recommends keeping full papers within about 6,000 words.

## Six likely desk-rejection arguments and the required answer

### 1. "This is merely parser implementation detail."
Required answer: evaluator implementation is tested as an experimental factor while the raw generation is held byte-identical. The primary scientific endpoint is whether reasonable evaluator choices alter model comparisons/rankings, not whether regexes differ.

### 2. "The result depends on one model."
Required answer: three independently developed open models and four task families; 12 model×benchmark cells and 12 benchmark×model-pair ranking comparisons.

### 3. "The evaluators were chosen after seeing output."
Required answer: E1–E5 code, unit tests, ranking-reversal definition and strongest-conclusion hierarchy are publicly frozen before endpoint generation.

### 4. "A deliberately bad parser can create any result."
Required answer: every evaluator corresponds to a common deterministic benchmark-extraction convention; unresolved rates are exposed; no LLM-as-a-judge is used in the primary analysis. The paper must justify every parser as plausible, not adversarial.

### 5. "Ranking reversals are cherry-picked."
Required answer: all 12 predeclared benchmark×model-pair comparisons are shown. Ties are not forced into reversals. If no reversal occurs, the paper falls back to the predeclared score-instability or bounded-robustness conclusion.

### 6. "This overlaps the Nature manuscript."
Required answer: zero Nature data/results. Different models, different benchmarks, different endpoint, no RIDI/frontier/operational audits/Nature parser numbers. Related-manuscript disclosure is explicit.

## Submission discipline

- Blinded manuscript with no identifying author/affiliation text.
- Separate title page.
- Keep main text ≤ about 6,000 words.
- Maximum six keywords.
- Concise Results; Discussion explains significance without repeating tables.
- Prepare signed author agreement/conflict forms at submission.
- Do not oversell evaluator disagreement as a change in underlying model capability.
