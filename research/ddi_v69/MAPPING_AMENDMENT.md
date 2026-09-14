# Pre-outcome mapping amendment
14 September 2026. No allocation outcome had been inspected when this rule was fixed.

The intake test of a punctuation-stripping normalizer failed: it mapped two distinct DDInter IDs (DDInter1894 and DDInter2138) to the same text key `typhoid vaccine live`, collapsed 139 addition pairs, and produced 224 spurious overlaps with the baseline graph. That normalizer is rejected; its audit is retained.

The primary mapping is now Unicode NFKC, casefold, collapse repeated whitespace, strip leading/trailing whitespace, and PRESERVE punctuation. This reproduces 160235 original pairs + 134948 disjoint additions = 295183 pairs. The resulting edge-bearing graph has 2283 names; the archive's 2290 drug-table entries need not all have edges. No two distinct source IDs in the additions map to the same key under this rule. This is a source-label identity analysis, not proof of chemical or therapeutic equivalence.

NHANES semicolon-delimited combination ingredients are split before this exact-name match. No first-token shortcut, punctuation stripping, synonym expansion, salt stripping, or formulation collapse is permitted. Ambiguous/unmatched names are excluded and counted. All other protocol choices, rankers, capacities and tolerances remain unchanged. This is an exploratory author-side lock, not a prospective clinical registration.
