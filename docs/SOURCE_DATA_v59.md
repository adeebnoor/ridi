# Nature v59 source-data map

Current manuscript: **Identical audits, different AI decisions**  
Submission workbook: `RIDI_Nature_Source_Data_v59.xlsx`

This page records the display-item structure used in the v59 submission package and prevents figure-number drift between the manuscript and Source Data workbook.

| Display item | Scientific role | Source Data sheet |
|---|---|---|
| Fig. 1 | Audit-equivalence / finite-allocation non-identification | `Fig1` |
| Fig. 2 | COMPAS constructive audit-equivalence classes | `Fig2` |
| Fig. 3 | Preregistered RAG behavioral consequence and controls | `Fig3` |
| Fig. 4 | EPSS production update and outcome-checked identity control | `Fig4` |
| Fig. 5 | Exact identity–utility frontier: minimum necessary membership change under utility budget | `Fig5` |
| Extended Data Fig. 1 | EPSS operational-partition refinement | `ED1` |
| Extended Data Fig. 2 | RAG ambiguity, capacity and order sensitivities | `ED2` |
| Extended Data Fig. 3 | Sufficient margin certificate | `ED3` |
| Extended Data Fig. 4 | Controlled cross-modal and vision-retrieval boundary analyses | `ED4` |
| Extended Data Fig. 5 | ReVerb45K, non-graph text-retrieval and DistMult transport/attribution analyses | `ED5` |
| Extended Data Fig. 6 | Four EPSS production-transition stress tests | `ED6` |
| Extended Data Fig. 7 | CMS HVBP annual-score transport | `ED7` |
| Extended Data Fig. 8 | Registered RxNorm and Open Targets failures/boundaries | `ED8` |

## v58 → v59 structural change

The former Extended Data Fig. 9 (exact identity–utility frontier) is promoted to **Main Fig. 5** in v59. The remaining Extended Data figures are renumbered in the order of first citation in the main text:

- old ED6 → new ED1
- old ED8 → new ED2
- old ED7 → new ED3
- old ED1 → new ED4
- old ED2 → new ED5
- old ED5 → new ED6
- old ED4 → new ED7
- old ED3 → new ED8

No scientific endpoint is changed by this renumbering. The change is editorial/structural and the v59 workbook preserves panel-level provenance to the frozen numerical artifacts.

## Reproducibility status

RAG preregistration: https://osf.io/txwdv/  
Community CODECHECK request: https://github.com/codecheckers/register/issues/208

CODECHECK remains open; no certificate is claimed until formally issued.
