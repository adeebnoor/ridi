#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import pathlib
import re
import urllib.request
import zipfile
from datetime import date, datetime, timezone

import numpy as np
import pandas as pd

from ridi_audit.selector import identity_utility_frontier, select_identity_control

API = "https://data.cms.gov/provider-data/api/1/archive/aggregate/theme/hospitals/relative"
FYS = [2017, 2018, 2019, 2020, 2021]
KS = [100, 500, 1000]
ETAS = [0.0, 0.0001, 0.001]

METHODOLOGY = {
    "FY2017_to_FY2018": "domain structure/weights and measure set changed",
    "FY2018_to_FY2019": "measure set changed",
    "FY2019_to_FY2020": "four 25% domains persisted, but THA/TKA complication performance period changed",
    "FY2020_to_FY2021": "scoring inputs/measure set changed",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_bytes(url: str, timeout: int = 300) -> tuple[int, bytes, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "RIDI CMS historical extension reproducibility audit"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return getattr(r, "status", 200), r.read(), dict(r.headers)


def parse_date(s: str) -> date:
    return datetime.strptime(s[:10], "%Y-%m-%d").date()


def normalize_col(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s).strip().lower()).strip()


def choose_col(columns, accepted):
    norm = {normalize_col(c): c for c in columns}
    for a in accepted:
        if a in norm:
            return norm[a]
    return None


def canonical_id(x) -> str:
    s = str(x).strip()
    if re.fullmatch(r"\d+(?:\.0+)?", s):
        s = s.split(".")[0]
        return s.zfill(6)
    return s


def spearman_from_scores(df: pd.DataFrame) -> float:
    # Average-rank Spearman correlation on the common universe.
    a = df["tps_old"].rank(method="average", ascending=False)
    b = df["tps_new"].rank(method="average", ascending=False)
    return float(a.corr(b, method="pearson"))


def selected_ids(df: pd.DataFrame, score_col: str, k: int) -> list[str]:
    x = df[["facility_id", score_col]].copy()
    x = x.sort_values([score_col, "facility_id"], ascending=[False, True], kind="mergesort")
    return x["facility_id"].head(k).tolist()


def tie_min_changed(df: pd.DataFrame, k: int) -> int:
    def status(score_col: str):
        x = df[["facility_id", score_col]].copy()
        vals = x[score_col].to_numpy(float)
        order = np.lexsort((x["facility_id"].astype(str).to_numpy(), -vals))
        cutoff = vals[order[k - 1]]
        H = set(x.loc[x[score_col] > cutoff, "facility_id"].astype(str))
        B = set(x.loc[x[score_col] == cutoff, "facility_id"].astype(str))
        q = k - len(H)
        if q < 0 or q > len(B):
            raise RuntimeError("invalid cutoff tie accounting")
        return H, B, q

    H0, B0, q0 = status("tps_old")
    H1, B1, q1 = status("tps_new")
    hh = len(H0 & H1)
    hb = len(H0 & B1)
    bh = len(B0 & H1)
    bb = len(B0 & B1)

    use_hb = min(hb, q1)
    use_bh = min(bh, q0)
    rem0 = q0 - use_bh
    rem1 = q1 - use_hb
    use_bb = min(bb, rem0, rem1)
    max_overlap = hh + use_hb + use_bh + use_bb
    return int(k - max_overlap)


def discover_snapshot(rows: list[dict], fy: int) -> dict | None:
    start = date(fy - 1, 10, 1)
    end = date(fy, 9, 30)
    eligible = []
    for r in rows:
        if r.get("type") != "theme" or not r.get("date") or not r.get("url"):
            continue
        try:
            d = parse_date(r["date"])
        except Exception:
            continue
        if start <= d <= end:
            eligible.append((d, r))
    if not eligible:
        return None
    eligible.sort(key=lambda z: z[0])
    return eligible[-1][1]


def extract_tps(zip_bytes: bytes, fy: int) -> tuple[pd.DataFrame, dict]:
    z = zipfile.ZipFile(io.BytesIO(zip_bytes), "r")
    exact = [n for n in z.namelist() if pathlib.PurePosixPath(n).name.lower() == "hvbp_tps.csv"]
    if len(exact) != 1:
        raise RuntimeError(f"expected exactly one hvbp_tps.csv, found {len(exact)}: {exact[:10]}")
    member = exact[0]
    raw = z.read(member)
    df = pd.read_csv(io.BytesIO(raw), dtype=str, low_memory=False)
    fy_col = choose_col(df.columns, ["fiscal year"])
    id_col = choose_col(df.columns, ["facility id", "provider id"])
    tps_col = choose_col(df.columns, ["total performance score"])
    if not fy_col or not id_col or not tps_col:
        raise RuntimeError(f"required columns missing: fy={fy_col}, id={id_col}, tps={tps_col}; columns={list(df.columns)}")
    parsed_fy = pd.to_numeric(df[fy_col], errors="coerce")
    tps = pd.to_numeric(df[tps_col], errors="coerce")
    out = pd.DataFrame({
        "facility_id": df[id_col].map(canonical_id),
        "fiscal_year": parsed_fy,
        "tps": tps,
    })
    out = out[(out["fiscal_year"] == fy) & np.isfinite(out["tps"]) & out["facility_id"].ne("")]
    dup = out["facility_id"].duplicated(keep=False)
    if dup.any():
        dups = out.loc[dup, "facility_id"].tolist()[:20]
        raise RuntimeError(f"duplicate Facility IDs after parsing for FY{fy}: {dups}")
    out = out.sort_values("facility_id").reset_index(drop=True)
    meta = {
        "tps_archive_member": member,
        "tps_bytes": len(raw),
        "tps_sha256": sha256_bytes(raw),
        "rows_in_csv": int(len(df)),
        "rows_target_fy_finite_tps": int(len(out)),
        "columns": {"fiscal_year": fy_col, "facility_id": id_col, "total_performance_score": tps_col},
    }
    return out, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    status, api_bytes, _ = get_bytes(API)
    if status != 200:
        raise RuntimeError(f"archive API HTTP {status}")
    api_sha = sha256_bytes(api_bytes)
    api = json.loads(api_bytes)
    rows = api["data"]

    source = {
        "protocol_id": "RIDI-CMS-HVBP-HISTORICAL-EXTENSION-v1",
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "archive_api": API,
        "archive_api_sha256": api_sha,
        "fiscal_years": {},
    }
    data_by_fy: dict[int, pd.DataFrame] = {}
    failures = {}

    for fy in FYS:
        meta = discover_snapshot(rows, fy)
        if meta is None:
            failures[str(fy)] = "no official theme-level hospital archive snapshot in locked fiscal-year window"
            continue
        rel = meta["url"]
        url = rel if rel.startswith("http") else "https://data.cms.gov" + rel
        rec = {
            "archive_date": meta.get("date"),
            "cms_archive_id": meta.get("id"),
            "cms_name": meta.get("name"),
            "official_url": url,
            "cms_reported_bytes": meta.get("size"),
        }
        try:
            http, zbytes, _ = get_bytes(url)
            rec["http_status"] = http
            rec["raw_zip_bytes"] = len(zbytes)
            rec["raw_zip_sha256"] = sha256_bytes(zbytes)
            if http != 200:
                raise RuntimeError(f"HTTP {http}")
            df, xmeta = extract_tps(zbytes, fy)
            rec.update(xmeta)
            if len(df) == 0:
                raise RuntimeError("selected official snapshot contains no finite TPS rows for target fiscal year")
            data_by_fy[fy] = df
        except Exception as e:
            failures[str(fy)] = f"{type(e).__name__}: {e}"
            rec["failure"] = failures[str(fy)]
        source["fiscal_years"][str(fy)] = rec

    results = []
    for fy0, fy1 in zip(FYS[:-1], FYS[1:]):
        key = f"FY{fy0}_to_FY{fy1}"
        if fy0 not in data_by_fy or fy1 not in data_by_fy:
            results.append({
                "transition": key,
                "status": "unavailable",
                "methodology_annotation": METHODOLOGY[key],
                "reason": f"missing parsed FY data: {fy0 not in data_by_fy=}, {fy1 not in data_by_fy=}",
            })
            continue

        a = data_by_fy[fy0].rename(columns={"tps": "tps_old"})[["facility_id", "tps_old"]]
        b = data_by_fy[fy1].rename(columns={"tps": "tps_new"})[["facility_id", "tps_new"]]
        m = a.merge(b, on="facility_id", how="inner", validate="one_to_one")
        m = m.sort_values("facility_id").reset_index(drop=True)
        n = len(m)
        rho = spearman_from_scores(m)

        for k in KS:
            if n < k:
                results.append({
                    "transition": key, "status": "capacity_unavailable", "k": k,
                    "common_universe": n, "methodology_annotation": METHODOLOGY[key],
                    "reason": "common universe smaller than k",
                })
                continue

            old_set = set(selected_ids(m, "tps_old", k))
            new_set = set(selected_ids(m, "tps_new", k))
            shared = len(old_set & new_set)
            delta = k - shared
            ridi = 0.0 if delta == 0 else float(2.0 * delta / (k + delta))
            tie_min = tie_min_changed(m, k)

            ids = m["facility_id"].astype(str).tolist()
            s0 = m["tps_old"].astype(float).tolist()
            s1 = m["tps_new"].astype(float).tolist()
            frontier = identity_utility_frontier(ids, s0, s1, k)

            for eta in ETAS:
                sel = select_identity_control(frontier, eta)
                results.append({
                    "transition": key,
                    "status": "ok",
                    "methodology_annotation": METHODOLOGY[key],
                    "fiscal_year_old": fy0,
                    "fiscal_year_new": fy1,
                    "common_universe": n,
                    "spearman": rho,
                    "k": k,
                    "shared": shared,
                    "changed_slots": delta,
                    "ridi": ridi,
                    "tie_min_changed_slots": tie_min,
                    "eta": eta,
                    "j_eta": int(sel["j_eta"]),
                    "utility_regret": float(sel["utility_regret"]),
                    "controlled_ridi": float(sel["ridi_controlled"]),
                    "avoidable_turnover_fraction": sel["avoidable_turnover_fraction"],
                })

    dfres = pd.DataFrame(results)
    dfres.to_csv(outdir / "historical_results.csv", index=False)
    (outdir / "source_provenance.json").write_text(json.dumps(source, indent=2), encoding="utf-8")

    summary = {
        "protocol_id": "RIDI-CMS-HVBP-HISTORICAL-EXTENSION-v1",
        "execution_status": "completed",
        "failures": failures,
        "primary_k": 500,
        "primary_eta": 0.001,
        "results": results,
    }
    (outdir / "historical_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# CMS HVBP historical extension — locked execution report",
        "",
        "Protocol: RIDI-CMS-HVBP-HISTORICAL-EXTENSION-v1",
        "",
        "## Source recovery",
        "",
    ]
    for fy in FYS:
        r = source["fiscal_years"].get(str(fy), {})
        if str(fy) in failures:
            lines.append(f"- FY{fy}: **unavailable** — {failures[str(fy)]}")
        else:
            lines.append(
                f"- FY{fy}: archive {r.get('archive_date')}; finite TPS n={r.get('rows_target_fy_finite_tps')}; "
                f"ZIP sha256={r.get('raw_zip_sha256')}; TPS sha256={r.get('tps_sha256')}"
            )

    lines += ["", "## Primary historical results (k=500, eta=0.001)", ""]
    primary = dfres[(dfres.get("status") == "ok") & (dfres.get("k") == 500) & (dfres.get("eta") == 0.001)] if not dfres.empty else pd.DataFrame()
    if len(primary):
        lines.append("| Transition | N | Spearman | Changed | Tie-min | j(0.1%) | Avoidable | Regret | Methodology note |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---|")
        for _, r in primary.iterrows():
            av = r["avoidable_turnover_fraction"]
            avs = "NA" if pd.isna(av) else f"{100*float(av):.2f}%"
            lines.append(
                f"| {r['transition'].replace('_to_', '→')} | {int(r['common_universe'])} | {float(r['spearman']):.3f} | "
                f"{int(r['changed_slots'])} | {int(r['tie_min_changed_slots'])} | {int(r['j_eta'])} | {avs} | "
                f"{100*float(r['utility_regret']):.4f}% | {r['methodology_annotation']} |"
            )
    else:
        lines.append("No transition satisfied the locked source-recovery rules.")

    lines += [
        "",
        "## Interpretation boundary",
        "",
        "These are exact finite-transition descriptives. Historical programme changes are annotated and are not pooled with FY2024→FY2026 as one stable scoring regime or one annual turnover rate.",
    ]
    (outdir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
