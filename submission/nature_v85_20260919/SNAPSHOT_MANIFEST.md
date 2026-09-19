# Nature submission snapshot — v85 PRE-ETHICS

**Date:** 19 September 2026  
**Title:** *Public systems change what they prioritise without recording it*  
**Author:** Adeeb Noor  
**Status:** current pre-submission snapshot; all author-side scientific/editorial work complete except the verified KAU ethics/IRB/REC determination and transfer into Nature's official dynamic Reporting Summary PDF.

## Local delivery package

`RIDI_Nature_v85_PRE_ETHICS_FINAL_20260919.zip`

SHA-256:
`aec706842e42f3c3aff0e6deb1dfd21c621509c0825438e28f6f39ebf55a652c`

The package contains:
- main manuscript DOCX/PDF;
- Supplementary Information DOCX/PDF;
- cover letter DOCX/PDF;
- Reporting Summary factual response sheet DOCX/PDF;
- hostile-editor audit;
- submission checklist;
- status/README files;
- locked Qwen3-32B and frontier-to-downstream aggregate JSON;
- SHA-256 manifest.

## Document hashes

- `ca62c21b0395ee0687efddc34f8998929bb4a9ea872f10cff47387140a79f5a4` — Manuscript_v85_PRE_ETHICS_FINAL.docx
- `00b40d679c0a256c7542fe5a80a185db06d78e993a4460125de0f7a1abbb6962` — Manuscript_v85_PRE_ETHICS_FINAL.pdf
- `5b10f4c83c6ac49c5175c108907cff349992221eb456024c4cce56a19b363acf` — Supplementary_Information_v85_PRE_ETHICS_FINAL.docx
- `f40e5066f536ada0c65d973b6c745ea1a9587722a29a2b99c2a9ccb8e5ee682b` — Supplementary_Information_v85_PRE_ETHICS_FINAL.pdf
- `4e7d38f34f60377d847b288880d496cc453a937bea0e725f9b1fda238fe8141e` — Cover_Letter_Nature_v85_PRE_ETHICS.docx
- `da902f221776f91666b165f0620bb0a7072ea4240e67d0ac2c31326b52b5d56b` — Cover_Letter_Nature_v85_PRE_ETHICS.pdf
- `8b42afe1c5b0ce371fdf9725730ec954ef1856f02a3fda7c59cc7f203e8e2a60` — Reporting_Summary_Response_Sheet_v85_PRE_ETHICS.docx
- `27c19d80219b776f2680807817a2284f5ca01d49d6d7bee3a5b998063971bb9b` — Reporting_Summary_Response_Sheet_v85_PRE_ETHICS.pdf

## QA freeze

- Summary: 193 words.
- Main text before References including Summary: 3,849 words.
- Methods: approximately 4,471 words by the final DOCX paragraph-range count.
- Main render: 29/29 pages visually inspected.
- SI render: 29/29 pages visually inspected.
- Cover letter: 2/2 pages visually inspected.
- Reporting response sheet: 3/3 pages visually inspected.
- Main/SI accessibility after cleanup: zero findings.
- Hidden comments removed; no substantive tracked changes retained.

## Latest locked scientific extensions

### Qwen3-32B scale transfer
- protocol lock: `266b9f1e6dcbe8f4dc3feb1bd279c18af2564954`
- query-record archive: `5c2b28edf9144b4d8c0adfc3f044ca9d868ee35b`
- locked aggregate: `63152b13610b2a0df7e4947912c8e15ab7dd0db5`
- macro correctness divergence: 12.37% (95% bootstrap 10.07–14.77%)
- same-query Qwen3-8B macro: 17.27%
- paired 32B−8B: −4.90 percentage points (95% −7.77 to −2.03)
- interpretation: persistence across scale, not scale invariance.

### Frontier → downstream control
- protocol lock: `383830dbd7c67f1898e88422bab8a49e5e91e9de`
- frozen 400-query panel: `f98be71b4402d95a3337dac78f272c3aa55cbd62`
- exact query-record archive: `d2162d26754917d6b635d23d7d80163d7a00ef2d`
- locked aggregate: `a13864d63198fce111651090dcc0924dce644a01`
- changed slots: 5.7275 → 5.3850 at k=10, eta=0.001
- benchmark accuracy: 57.25% → 57.00%; paired difference −0.25 pp (95% −1.25 to +0.75)
- interpretation: descriptive finite-panel trade-off; no non-inferiority/downstream-benefit claim.

## Only hard blocker

Before journal submission, insert the **verified King Abdulaziz University ethics/IRB/REC determination** applicable to the secondary analyses:
1. authority / committee;
2. decision (approval, documented exemption, or institutional not-required determination);
3. date;
4. reference number.

Do not copy an upstream study's approval as if it approved this study.

After that insertion, re-render the affected documents, transfer the prepared responses into Nature's official dynamic Reporting Summary PDF, regenerate hashes and mark the snapshot SUBMIT READY.

## Superseded snapshots

Earlier Nature snapshots, including v45 and later working versions, are retained only for provenance. v85 PRE-ETHICS is the current snapshot.
