#!/usr/bin/env python3
"""Collatz Conjecture Analysis

Goal: fast, reproducible runs with *streaming* stats (no giant arrays), plus
small derived aggregations we can plot/compare across runs.

Collatz:
- even: n -> n/2
- odd:  n -> 3n+1

Notes:
- We memoize stopping times.
- We avoid holding stopping time for every n in memory.
- We keep histograms + grouped means (mod 12, popcount) for quick correlation.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


def collatz_stopping_time(n: int, cache: Dict[int, int], *, cache_limit: int) -> int:
    """Steps to reach 1 (memoized) with a hard cache size boundary.

    Only values <= cache_limit are stored/looked-up. This prevents runaway
    memory growth on huge ranges while still capturing most useful memoization.

    Implementation detail: we only extend the path while n stays >= original_n.
    Once it drops below, we can stop and add cached remainder (if any).
    """
    if n == 1:
        return 0
    if n <= cache_limit and n in cache:
        return cache[n]

    original_n = n
    steps = 0
    # store only cacheable values, but with the step index when they were seen
    path: List[Tuple[int, int]] = []  # (val, steps_so_far_at_val)

    # Step until we either reach 1 or hit a cached value (<= cache_limit).
    while n != 1:
        if n <= cache_limit and n in cache:
            steps += cache[n]
            break

        if n <= cache_limit:
            path.append((n, steps))

        n = (n // 2) if (n % 2 == 0) else (3 * n + 1)
        steps += 1

    total_steps = steps

    # Cache intermediate values (bounded)
    for val, steps_at_val in path:
        cache.setdefault(val, total_steps - steps_at_val)

    if original_n <= cache_limit:
        cache[original_n] = total_steps

    return total_steps


def collatz_max_value(n: int) -> int:
    """Maximum value reached in the sequence (expensive; use only for sample)."""
    max_val = n
    while n != 1:
        n = (n // 2) if (n % 2 == 0) else (3 * n + 1)
        if n > max_val:
            max_val = n
    return max_val


@dataclass
class GroupStats:
    count: int = 0
    total: int = 0

    def add(self, value: int) -> None:
        self.count += 1
        self.total += value

    def mean(self) -> float:
        return (self.total / self.count) if self.count else 0.0


def ensure_len(a: List[int], n: int) -> None:
    if len(a) < n:
        a.extend([0] * (n - len(a)))


def analyze_range(limit: int, *, sample_peak_limit: int = 100_000, top_k: int = 50, cache_limit: int = 5_000_000) -> dict:
    print(f"Analyzing Collatz sequences for n = 1 to {limit:,}")
    print("=" * 60)

    start_time = time.time()
    cache: Dict[int, int] = {}
    cache_limit = int(cache_limit)

    # streaming stats
    total_steps = 0
    max_stopping_time = 0

    # histogram indexed by stopping time
    st_hist: List[int] = [0]

    # grouped correlations
    mod12 = [GroupStats() for _ in range(12)]
    popcount_groups = [GroupStats() for _ in range(65)]  # up to 64 bits

    record_holders: List[Tuple[int, int]] = []
    current_record = 0

    top_longest: List[Tuple[int, int]] = []  # (n, st) sorted desc

    for n in range(1, limit + 1):
        st = collatz_stopping_time(n, cache, cache_limit=cache_limit)
        total_steps += st

        if st > max_stopping_time:
            max_stopping_time = st

        ensure_len(st_hist, st + 1)
        st_hist[st] += 1

        mod12[n % 12].add(st)
        popcount_groups[n.bit_count()].add(st)

        if st > current_record:
            current_record = st
            record_holders.append((n, st))

        # Track top-K longest sequences
        if len(top_longest) < top_k or st > top_longest[-1][1]:
            top_longest.append((n, st))
            top_longest.sort(key=lambda x: -x[1])
            top_longest = top_longest[:top_k]

        if n % 1_000_000 == 0:
            elapsed = time.time() - start_time
            print(f"  Processed {n:,} numbers in {elapsed:.1f}s")

    elapsed = time.time() - start_time

    avg_stopping_time = total_steps / limit

    # peaks (expensive) – only sample
    peak_records: List[Tuple[int, int, float]] = []
    peak_check_upto = min(limit, sample_peak_limit)
    for n in range(1, peak_check_upto + 1):
        peak = collatz_max_value(n)
        ratio = peak / n
        if len(peak_records) < 10 or ratio > peak_records[-1][2]:
            peak_records.append((n, peak, ratio))
            peak_records.sort(key=lambda x: -x[2])
            peak_records = peak_records[:10]

    # convenience summaries
    most_common = sorted(((st, c) for st, c in enumerate(st_hist) if c), key=lambda x: -x[1])[:10]

    mod12_summary = [
        {"mod": i, "count": mod12[i].count, "avg_stopping_time": mod12[i].mean()}
        for i in range(12)
    ]

    popcount_summary = [
        {"popcount": i, "count": popcount_groups[i].count, "avg_stopping_time": popcount_groups[i].mean()}
        for i in range(len(popcount_groups))
        if popcount_groups[i].count
    ]

    results = {
        "limit": limit,
        "avg_stopping_time": avg_stopping_time,
        "max_stopping_time": max_stopping_time,
        "elapsed_seconds": elapsed,
        "record_holders": record_holders,
        "long_sequences": top_longest,
        "stopping_time_histogram": st_hist,
        "most_common_stopping_times": [
            {"steps": st, "count": c, "pct": 100 * c / limit} for st, c in most_common
        ],
        "mod12": mod12_summary,
        "popcount": popcount_summary,
        "peak_sample_upto": peak_check_upto,
        "peak_records": [
            {"n": n, "peak": peak, "ratio": ratio} for (n, peak, ratio) in peak_records
        ],
        "notes": {
            "sample_peak_limit": sample_peak_limit,
            "top_k": top_k,
            "cache_limit": cache_limit,
        },
    }

    print(f"\nCompleted in {elapsed:.1f} seconds")
    print(f"  Average stopping time: {avg_stopping_time:.2f}")
    print(f"  Max stopping time: {max_stopping_time}")
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10_000_000)
    ap.add_argument("--sample-peak", type=int, default=100_000)
    ap.add_argument("--top-k", type=int, default=50)
    ap.add_argument("--out", type=str, default="collatz_results.json")
    ap.add_argument("--cache-limit", type=int, default=5_000_000)
    args = ap.parse_args()

    results = analyze_range(
        args.limit,
        sample_peak_limit=args.sample_peak,
        top_k=args.top_k,
        cache_limit=args.cache_limit,
    )

    out_path = Path(args.out)
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\n✅ Results saved to {out_path}")


if __name__ == "__main__":
    main()
