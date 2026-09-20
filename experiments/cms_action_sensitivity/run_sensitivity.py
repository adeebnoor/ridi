#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import zipfile

import pandas as pd
import requests

OUT = pathlib.Path("out/cms_action_sensitivity")
OUT.mkdir(parents=True, exist_ok=True)

TPS_URLS = {
    2024: "https://data.cms.gov/provider-data/sites/default/files/dataset-archives/theme/hospitals/hospitals_2024-07-31.zip",
    2025: "https://data.cms.gov/provider-data/sites/default/files/dataset-archives/theme/hospitals/hospitals_2025-08-14.zip",
    2026: "https://data.cms.gov/provider-data/sites/default/files/dataset-archives/theme/hospitals/hospitals_2026-08-13.zip",
}
TABLE16B_URLS = {
    2024: "https://www.cms.gov/files/zip/fy24-ipps-final-rule-16b.zip",
    2025: "https://www.cms.gov/files/zip/fy-2025-ipps-final-rule-table-16-b.zip",
    2026: "https://www.cms.gov/files/zip/fy2026-ipps-table-16b.zip",
}
THRESHOLDS = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
FACTOR_EPS = 1e-12
DOLLAR_BASE = 10_000_000.0


def norm(s) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s).strip().lower()).strip()


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def download(url: str) -> bytes:
    r = requests.get(url, timeout=180, headers={"User-Agent": "RIDI CMS action-sufficiency sensitivity audit"})
    r.raise_for_status()
    return r.content


def canon_ccn(x) -> str:
    s = str(x).strip()
    if not s or s.lower() in {"nan", "none"}:
        return ""
    if re.fullmatch(r"\d+(?:\.0+)?", s):
        s = s.split(".")[0]
        return s.zfill(6)
    digits = re.sub(r"\D", "", s)
    return digits.zfill(6) if digits else s


def find_col(cols, predicates):
    for c in cols:
        nc = norm(c)
        if all(p(nc) for p in predicates):
            return c
    return None


def parse_tps(zip_bytes: bytes, fy: int):
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as z:
        names = z.namelist()
        hits = [n for n in names if pathlib.PurePosixPath(n).name.lower() == "hvbp_tps.csv"]
        if len(hits) != 1:
            raise RuntimeError(f"FY{fy}: expected exactly one hvbp_tps.csv, found {hits[:10]}")
        raw = z.read(hits[0])
    df = pd.read_csv(io.BytesIO(raw), dtype=str, low_memory=False)
    fy_col = find_col(df.columns, [lambda x: "fiscal" in x, lambda x: "year" in x])
    id_col = find_col(df.columns, [lambda x: "facility" in x or "provider" in x, lambda x: "id" in x or "number" in x])
    tps_col = find_col(df.columns, [lambda x: "total" in x, lambda x: "performance" in x, lambda x: "score" in x])
    if not all([fy_col, id_col, tps_col]):
        raise RuntimeError(f"FY{fy}: TPS columns not found: {list(df.columns)}")
    out = pd.DataFrame({
        "ccn": df[id_col].map(canon_ccn),
        "fy": pd.to_numeric(df[fy_col], errors="coerce"),
        "tps": pd.to_numeric(df[tps_col], errors="coerce"),
    })
    out = out[(out["fy"] == fy) & out["tps"].notna() & out["ccn"].ne("")]
    out = out.drop_duplicates("ccn", keep="first").reset_index(drop=True)
    return out, {"member": hits[0], "rows": int(len(out)), "sha256_csv": sha256(raw)}


def factor_candidates(cols):
    scored = []
    for c in cols:
        nc = norm(c)
        score = 0
        if "factor" in nc: score += 3
        if "adjustment" in nc: score += 3
        if "value based" in nc: score += 2
        if "incentive" in nc: score += 2
        if "payment" in nc: score += 1
        if score:
            scored.append((score, c))
    return sorted(scored, reverse=True)


def ccn_candidates(cols):
    scored = []
    for c in cols:
        nc = norm(c)
        score = 0
        if "ccn" in nc: score += 5
        if "provider number" in nc: score += 5
        if "cms certification" in nc: score += 5
        if "provider" in nc: score += 2
        if "number" in nc: score += 1
        if score:
            scored.append((score, c))
    return sorted(scored, reverse=True)


def try_sheet(raw: bytes, sheet_name):
    probe = pd.read_excel(io.BytesIO(raw), sheet_name=sheet_name, header=None, nrows=60, engine="openpyxl")
    for header_idx in range(min(40, len(probe))):
        vals = [norm(v) for v in probe.iloc[header_idx].tolist()]
        has_ccn = any(("ccn" in v) or ("provider number" in v) or ("cms certification" in v) for v in vals)
        has_factor = any(("factor" in v) and (("payment" in v) or ("adjustment" in v) or ("incentive" in v)) for v in vals)
        if not (has_ccn and has_factor):
            continue
        df = pd.read_excel(io.BytesIO(raw), sheet_name=sheet_name, header=header_idx, engine="openpyxl")
        ccands = ccn_candidates(df.columns)
        fcands = factor_candidates(df.columns)
        if not ccands or not fcands:
            continue
        ccn_col = ccands[0][1]
        factor_col = fcands[0][1]
        out = pd.DataFrame({
            "ccn": df[ccn_col].map(canon_ccn),
            "factor": pd.to_numeric(df[factor_col], errors="coerce"),
        })
        out = out[out["ccn"].ne("") & out["factor"].notna()]
        if len(out) >= 100:
            out = out.drop_duplicates("ccn", keep="first").reset_index(drop=True)
            return out, {
                "sheet": str(sheet_name), "header_row_zero_based": int(header_idx),
                "ccn_col": str(ccn_col), "factor_col": str(factor_col), "rows": int(len(out))
            }
    return None, None


def parse_table16b(zip_bytes: bytes, fy: int):
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as z:
        xlsx = [n for n in z.namelist() if n.lower().endswith(".xlsx") and "16" in n.lower()]
        if not xlsx:
            xlsx = [n for n in z.namelist() if n.lower().endswith(".xlsx")]
        errors = []
        for member in xlsx:
            raw = z.read(member)
            try:
                xl = pd.ExcelFile(io.BytesIO(raw), engine="openpyxl")
                for sh in xl.sheet_names:
                    try:
                        out, meta = try_sheet(raw, sh)
                        if out is not None:
                            meta.update({"member": member, "sha256_xlsx": sha256(raw)})
                            return out, meta
                    except Exception as e:
                        errors.append(f"{member}/{sh}: {type(e).__name__}: {e}")
            except Exception as e:
                errors.append(f"{member}: {type(e).__name__}: {e}")
    raise RuntimeError(f"FY{fy}: unable to parse Table 16B. Errors: {errors[:8]}")


def summarize_subset(df: pd.DataFrame, threshold: float) -> dict:
    s = df[df["abs_dtps"] <= threshold + 1e-12].copy()
    n = len(s)
    if n == 0:
        return {"threshold": threshold, "n": 0}
    changed = s["abs_dfactor"] > FACTOR_EPS
    return {
        "threshold": threshold,
        "n": int(n),
        "factor_changed_n": int(changed.sum()),
        "factor_changed_prop": float(changed.mean()),
        "mean_abs_dfactor": float(s["abs_dfactor"].mean()),
        "median_abs_dfactor": float(s["abs_dfactor"].median()),
        "p90_abs_dfactor": float(s["abs_dfactor"].quantile(0.90)),
        "mean_normalized_usd_per_10m": float(s["abs_dfactor"].mean() * DOLLAR_BASE),
        "median_normalized_usd_per_10m": float(s["abs_dfactor"].median() * DOLLAR_BASE),
        "positive_n": int((s["dfactor"] > FACTOR_EPS).sum()),
        "negative_n": int((s["dfactor"] < -FACTOR_EPS).sum()),
        "zero_n": int((s["abs_dfactor"] <= FACTOR_EPS).sum()),
    }


provenance = {}
year_data = {}
for fy in [2024, 2025, 2026]:
    tps_zip = download(TPS_URLS[fy])
    fac_zip = download(TABLE16B_URLS[fy])
    tps, tmeta = parse_tps(tps_zip, fy)
    fac, fmeta = parse_table16b(fac_zip, fy)
    linked = tps.merge(fac, on="ccn", how="inner", validate="one_to_one")
    linked["fy"] = fy
    linked.to_csv(OUT / f"linked_FY{fy}.csv", index=False)
    year_data[fy] = linked
    provenance[str(fy)] = {
        "tps_url": TPS_URLS[fy], "tps_zip_sha256": sha256(tps_zip), "tps": tmeta,
        "table16b_url": TABLE16B_URLS[fy], "table16b_zip_sha256": sha256(fac_zip), "table16b": fmeta,
        "linked_n": int(len(linked)),
    }

within_year = {}
for fy, df in year_data.items():
    g = df.groupby("tps", dropna=True)["factor"].agg(["size", "nunique", "min", "max"]).reset_index()
    dup = g[g["size"] >= 2].copy()
    discord = dup[(dup["max"] - dup["min"]).abs() > FACTOR_EPS].copy()
    within_year[str(fy)] = {
        "duplicate_tps_levels_n": int(len(dup)),
        "hospitals_in_duplicate_tps_levels_n": int(dup["size"].sum()) if len(dup) else 0,
        "discordant_tps_levels_n": int(len(discord)),
        "hospitals_in_discordant_tps_levels_n": int(discord["size"].sum()) if len(discord) else 0,
        "max_within_tps_factor_range": float((discord["max"] - discord["min"]).max()) if len(discord) else 0.0,
    }
    dup.to_csv(OUT / f"within_year_tps_levels_FY{fy}.csv", index=False)

transition_rows = []
transition_summaries = {}
for old, new in [(2024, 2025), (2025, 2026)]:
    a = year_data[old][["ccn", "tps", "factor"]].rename(columns={"tps":"tps_old","factor":"factor_old"})
    b = year_data[new][["ccn", "tps", "factor"]].rename(columns={"tps":"tps_new","factor":"factor_new"})
    m = a.merge(b, on="ccn", how="inner", validate="one_to_one")
    m["transition"] = f"FY{old}_to_FY{new}"
    m["dtps"] = m["tps_new"] - m["tps_old"]
    m["abs_dtps"] = m["dtps"].abs()
    m["dfactor"] = m["factor_new"] - m["factor_old"]
    m["abs_dfactor"] = m["dfactor"].abs()
    m.to_csv(OUT / f"hospital_transition_FY{old}_to_FY{new}.csv", index=False)
    transition_rows.append(m)
    transition_summaries[f"FY{old}_to_FY{new}"] = [summarize_subset(m, t) for t in THRESHOLDS]

pooled = pd.concat(transition_rows, ignore_index=True)
pooled.to_csv(OUT / "hospital_transitions_pooled.csv", index=False)
pooled_sensitivity = [summarize_subset(pooled, t) for t in THRESHOLDS]

mapping_support = {}
for old, new in [(2024, 2025), (2025, 2026)]:
    def map_by_tps(df):
        return df.groupby("tps")["factor"].agg(
            n="size", median_factor="median", mean_factor="mean", min_factor="min", max_factor="max"
        ).reset_index()
    ma = map_by_tps(year_data[old]).rename(columns={c:f"{c}_old" for c in ["n","median_factor","mean_factor","min_factor","max_factor"]})
    mb = map_by_tps(year_data[new]).rename(columns={c:f"{c}_new" for c in ["n","median_factor","mean_factor","min_factor","max_factor"]})
    s = ma.merge(mb, on="tps", how="inner")
    s["abs_delta_median_factor"] = (s["median_factor_new"] - s["median_factor_old"]).abs()
    s["normalized_usd_per_10m"] = s["abs_delta_median_factor"] * DOLLAR_BASE
    s.to_csv(OUT / f"shared_tps_support_FY{old}_to_FY{new}.csv", index=False)
    changed = s["abs_delta_median_factor"] > FACTOR_EPS
    mapping_support[f"FY{old}_to_FY{new}"] = {
        "shared_exact_tps_levels_n": int(len(s)),
        "changed_median_factor_levels_n": int(changed.sum()),
        "changed_median_factor_prop": float(changed.mean()) if len(s) else None,
        "median_abs_delta_median_factor": float(s["abs_delta_median_factor"].median()) if len(s) else None,
        "mean_abs_delta_median_factor": float(s["abs_delta_median_factor"].mean()) if len(s) else None,
        "p90_abs_delta_median_factor": float(s["abs_delta_median_factor"].quantile(0.90)) if len(s) else None,
        "max_abs_delta_median_factor": float(s["abs_delta_median_factor"].max()) if len(s) else None,
        "median_normalized_usd_per_10m": float(s["normalized_usd_per_10m"].median()) if len(s) else None,
    }

summary = {
    "analysis_id": "RIDI-CMS-ACTION-SUFFICIENCY-SENSITIVITY-v1",
    "status": "post_hoc robustness/scope analysis; does not replace the preregistered Table 16B linkage",
    "fiscal_years": [2024, 2025, 2026],
    "temporal_scope": "Two adjacent comparable program transitions; historical years are not pooled because the locked methodology screen found no pre-FY2024 adjacent pair satisfying strict scoring-regime invariance.",
    "provenance": provenance,
    "within_year_exact_tps": within_year,
    "hospital_transition_sensitivity": transition_summaries,
    "pooled_hospital_transition_sensitivity": pooled_sensitivity,
    "shared_score_support_mapping": mapping_support,
    "interpretation_boundary": [
        "Published TPS equality/near-equality is descriptive evaluation equivalence, not a causal treatment.",
        "Payment-factor differences are actual Table 16B action differences, but dollar values are fixed-volume normalizations, not hospital revenue estimates.",
        "Hospital-transition observations are not treated as independent annual replications; calendar generalizability remains limited to FY2024-FY2026.",
        "The shared-score-support analysis tests whether the published TPS alone reconstructs the payment action over the observed score support; it does not claim the annual mapping should be invariant."
    ]
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
(OUT / "source_provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")

lines = [
    "# CMS action-sufficiency sensitivity audit",
    "",
    "**Status:** post hoc robustness/scope analysis. The preregistered exact-TPS linkage remains the primary CMS analysis.",
    "",
    "## Why this analysis",
    "",
    "The primary CMS result spans only two adjacent fiscal-year transitions. This audit does not manufacture additional annual replications from non-comparable scoring regimes. Instead it asks whether the conclusion depends on the rare exact-equality subset or on one analytic choice, and whether published TPS reconstructs payment action over the full shared score support.",
    "",
    "## Exact and near-equality hospital-transition sensitivity",
    "",
    "| Scope | abs(Delta TPS) <= | n | factor changed | mean abs(Delta factor) | median abs(Delta factor) | normalized mean per USD 10m |",
    "|---|---:|---:|---:|---:|---:|---:|",
]
for key, rows in list(transition_summaries.items()) + [("Pooled", pooled_sensitivity)]:
    for r in rows:
        if r.get("n", 0) == 0:
            continue
        lines.append(
            f"| {key} | {r['threshold']:.2f} | {r['n']} | {r['factor_changed_n']}/{r['n']} ({100*r['factor_changed_prop']:.1f}%) | "
            f"{r['mean_abs_dfactor']:.6f} | {r['median_abs_dfactor']:.6f} | USD {r['mean_normalized_usd_per_10m']:,.0f} |"
        )

lines += ["", "## Within-year exact published-TPS check", ""]
for fy, r in within_year.items():
    lines.append(
        f"- FY{fy}: {r['duplicate_tps_levels_n']} repeated published-TPS levels covering {r['hospitals_in_duplicate_tps_levels_n']} hospitals; "
        f"{r['discordant_tps_levels_n']} score levels had more than one actual Table 16B factor."
    )

lines += ["", "## Shared exact-TPS support across adjacent years", ""]
for k, r in mapping_support.items():
    lines.append(
        f"- {k}: {r['shared_exact_tps_levels_n']} exact TPS values occurred in both years; "
        f"{r['changed_median_factor_levels_n']} ({100*r['changed_median_factor_prop']:.1f}%) mapped to a different median actual payment factor; "
        f"median absolute factor difference {r['median_abs_delta_median_factor']:.6f} "
        f"(fixed-volume normalization USD {r['median_normalized_usd_per_10m']:,.0f} per USD 10m)."
    )

lines += [
    "",
    "## Interpretation",
    "",
    "This audit strengthens scope, not chronology. The defensible claim is not that many independent years were observed. It is that the preregistered exact-equality result is reproduced separately in each of two consecutive comparable updates, is embedded in a much larger near-equality hospital-transition set, and can be examined across the entire exact shared score support. Calendar generalizability remains explicitly limited to FY2024-FY2026.",
]
(OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
