#!/usr/bin/env python3
"""A dependency-free demonstration of the decision-identity paradox."""

from __future__ import annotations

import argparse


def run_experiment(n: int = 10_000, k: int = 50) -> dict[str, float | int]:
    if n < 2:
        raise ValueError("n must be at least 2")
    if k < 1 or 2 * k > n:
        raise ValueError("k must satisfy 1 <= k <= n/2")

    baseline = list(range(n))
    updated = baseline[k : 2 * k] + baseline[:k] + baseline[2 * k :]
    top_baseline = set(baseline[:k])
    top_updated = set(updated[:k])
    overlap = len(top_baseline & top_updated)
    union = len(top_baseline | top_updated)

    rho = 1.0 - (12.0 * k**3) / (n * (n**2 - 1))
    ridi = 1.0 - overlap / union
    return {
        "n": n,
        "k": k,
        "spearman": rho,
        "overlap": overlap,
        "ridi": ridi,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show that near-perfect global rank agreement can hide complete top-k replacement."
    )
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--k", type=int, default=50)
    args = parser.parse_args()
    result = run_experiment(args.n, args.k)

    print(f"Candidates (n):               {result['n']:>6,}")
    print(f"Decision capacity (k):        {result['k']:>6,}")
    print(f"Global Spearman agreement:  {result['spearman']:.9f}")
    print(f"Top-k overlap:                {result['overlap']:>6,} / {result['k']:,}")
    print(f"RIDI:                          {result['ridi']:.3f}")
    print()
    print("Verdict: near-perfect global agreement, completely different decisions.")


if __name__ == "__main__":
    main()

