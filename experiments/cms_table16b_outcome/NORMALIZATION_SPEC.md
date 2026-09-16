# Normalization specification

The analysis consumes two UTF-8 CSV files. Normalization is a provenance-preserving extraction step, not an analytical choice.

## `tps.csv`
Required columns:
- `snapshot_date` — ISO date
- `fiscal_year` — integer
- `ccn` — six-digit CMS Certification Number string
- `tps` — published Total Performance Score text parseable as Decimal

Required locked snapshots:
- 2024-10-30 / FY2024
- 2025-02-19 / FY2025
- 2025-11-26 / FY2025
- 2026-02-25 / FY2026

No rank-based filtering occurs during normalization.

## `factors.csv`
Required columns:
- `fiscal_year` — 2024, 2025 or 2026
- `ccn` — six-digit CCN string
- `actual_vbp_factor` — the **actual** Hospital VBP payment adjustment factor from Table 16B, preserved as published text and parseable as Decimal

The Table 16B column must be identified by the official table header/legend, not by column position. If more than one plausible factor field exists, normalization stops and the ambiguity is documented before values are analysed.

## CCN normalization
- trim whitespace;
- if numeric-looking, remove a terminal spreadsheet `.0` representation only when it is a pure integer representation;
- preserve/pad to six digits;
- reject non-digit identifiers after normalization;
- never merge distinct CCNs by fuzzy matching, name matching or geography.

## Audit trail
The extraction step must write a provenance record containing raw file SHA-256, inner filename, selected source headers, row count, duplicate-CCN count, nonnumeric-value count and unmatched-CCN count after linkage.
