#!/usr/bin/env python3
"""oddmap_stats.py

Sampling-based experiments for the accelerated odd Collatz map (Syracuse map):

  T(n) = (3n+1) / 2^{a(n)},  a(n)=v2(3n+1), n odd.

Implements Milestones M2–M4 from docs/experiments/M2-M4-spec.md:
- M2: residue mixing/bias mod 3^k
- M3: distribution + autocorrelation of a(n) under evolved measure
- M4: drift (Delta log) and state-dependent drift by residue

Outputs are written to data/oddmap_stats/<run-id>/ (gitignored).

Design goal: keep dependencies minimal (stdlib only). Plotting is optional.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import json
import math
import os
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def v2(x: int) -> int:
    """2-adic valuation of a positive integer (largest k s.t. 2^k | x)."""
    # x>0
    return (x & -x).bit_length() - 1


def odd_step(n: int) -> Tuple[int, int]:
    """One accelerated odd step.

    Returns (next_n, a) where a=v2(3n+1).
    """
    m = 3 * n + 1
    a = v2(m)
    return m >> a, a


def mod_pow3_units(k: int) -> Tuple[int, List[int], Dict[int, int]]:
    """Return modulus 3^k, list of units (not divisible by 3), and index map."""
    mod = 3**k
    units = [r for r in range(1, mod) if r % 3 != 0]
    idx = {r: i for i, r in enumerate(units)}
    return mod, units, idx


def tv_distance(p: List[float], q: List[float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def normalize_counts(counts: List[int]) -> List[float]:
    s = sum(counts)
    if s == 0:
        return [0.0 for _ in counts]
    return [c / s for c in counts]


@dataclass
class RunConfig:
    N: int
    S: int
    seed: int
    k_max: int
    t_list: List[int]
    drift_k: int
    conditional_k: int


def sample_odd_uniform(N: int, rng: random.Random) -> int:
    # sample odd in [1,N]
    x = rng.randrange(1, N + 1)
    return x if x % 2 == 1 else (x - 1 if x > 1 else 1)


def write_csv(path: Path, header: List[str], rows: Iterable[Iterable[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(list(r))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=50_000_000)
    ap.add_argument("--S", type=int, default=200_000, help="number of sampled starting values")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--k-max", type=int, default=8)
    ap.add_argument(
        "--t-list",
        type=str,
        default="0,1,2,3,5,8,13,21,34,50",
        help="comma-separated t values (odd-steps) to record",
    )
    ap.add_argument("--drift-k", type=int, default=8, help="k used for state-dependent drift")
    ap.add_argument("--conditional-k", type=int, default=8, help="k used for P(a|residue) sampling")
    ap.add_argument("--outdir", type=str, default="../data/oddmap_stats")
    args = ap.parse_args()

    t_list = [int(x.strip()) for x in args.t_list.split(",") if x.strip()]
    t_max = max(t_list)

    cfg = RunConfig(
        N=args.N,
        S=args.S,
        seed=args.seed,
        k_max=args.k_max,
        t_list=t_list,
        drift_k=args.drift_k,
        conditional_k=args.conditional_k,
    )

    run_id = time.strftime("%Y%m%d_%H%M%SZ", time.gmtime()) + f"_N{cfg.N}_S{cfg.S}_k{cfg.k_max}_t{t_max}_seed{cfg.seed}"
    outroot = Path(args.outdir).expanduser().resolve() / run_id
    outroot.mkdir(parents=True, exist_ok=True)

    (outroot / "config.json").write_text(json.dumps(dataclasses.asdict(cfg), indent=2), encoding="utf-8")

    rng = random.Random(cfg.seed)

    # Precompute mod 3^k units indices for k=1..k_max
    mod3 = {}
    units_idx = {}
    for k in range(1, cfg.k_max + 1):
        mod, _units, idx = mod_pow3_units(k)
        mod3[k] = mod
        units_idx[k] = idx

    # M2: residue histograms counts[k][t][unit_index]
    counts: Dict[int, Dict[int, List[int]]] = {}
    for k in range(1, cfg.k_max + 1):
        size = 2 * (3 ** (k - 1))
        counts[k] = {t: [0] * size for t in cfg.t_list}

    # M3: a distributions by time index i (0..t_max-1)
    a_hist_by_i: List[Counter[int]] = [Counter() for _ in range(t_max)]
    # M3: autocorrelation needs sequence stats; we do lagged correlations via sums.
    # We'll record for lags 1..L on the fly.
    L = 20
    # sums for correlation across all trajectories: sum a_i, sum a_{i+lag}, sum a_i*a_{i+lag}, counts
    corr = {
        lag: {"n": 0, "sx": 0.0, "sy": 0.0, "sxx": 0.0, "syy": 0.0, "sxy": 0.0}
        for lag in range(1, L + 1)
    }

    # Conditional a given residue state (k=conditional_k) at step i (we do at i=0..t_max-1)
    cond_k = cfg.conditional_k
    cond_mod = mod3[cond_k]
    cond_idx = units_idx[cond_k]
    # store limited a values up to a_max_bucket; bigger go into overflow
    a_max_bucket = 32
    cond_a_counts: Dict[int, List[int]] = {  # state_index -> buckets
        s: [0] * (a_max_bucket + 2) for s in range(len(cond_idx))
    }

    # M4: drift by residue state for drift_k
    drift_k = cfg.drift_k
    drift_mod = mod3[drift_k]
    drift_idx = units_idx[drift_k]
    drift_stats = {s: {"n": 0, "sum": 0.0, "sum2": 0.0} for s in range(len(drift_idx))}
    drift_global = {"n": 0, "sum": 0.0, "sum2": 0.0}

    # simulate
    t_set = set(cfg.t_list)
    start = time.time()
    for j in range(cfg.S):
        n = sample_odd_uniform(cfg.N, rng)

        # walk for t_max steps
        a_seq: List[int] = []
        n_seq: List[int] = [n]
        for i in range(t_max):
            nxt, a = odd_step(n_seq[-1])
            a_seq.append(a)
            n_seq.append(nxt)

        # M2: record residues of n_t for t in t_list (note: state lives in units mod 3^k for t>=1)
        for t in cfg.t_list:
            nt = n_seq[t]
            for k in range(1, cfg.k_max + 1):
                r = nt % mod3[k]
                if r % 3 == 0:
                    # should be rare for t>=1; ignore for histogram on units
                    continue
                counts[k][t][units_idx[k][r]] += 1

        # M3: a distributions by i
        for i, a in enumerate(a_seq):
            a_hist_by_i[i][a] += 1

        # M3: correlations
        for lag in range(1, L + 1):
            for i in range(t_max - lag):
                x = a_seq[i]
                y = a_seq[i + lag]
                st = corr[lag]
                st["n"] += 1
                st["sx"] += x
                st["sy"] += y
                st["sxx"] += x * x
                st["syy"] += y * y
                st["sxy"] += x * y

        # conditional a|state at i=0 (can extend to multiple i later)
        state_r = n_seq[0] % cond_mod
        if state_r % 3 != 0:
            s = cond_idx[state_r]
            a0 = a_seq[0]
            if a0 <= a_max_bucket:
                cond_a_counts[s][a0] += 1
            else:
                cond_a_counts[s][a_max_bucket + 1] += 1  # overflow

        # M4: drift per step i=0..t_max-1 aggregated by residue at time i
        for i in range(t_max):
            ni = n_seq[i]
            nj1 = n_seq[i + 1]
            # drift in log
            d = math.log(nj1) - math.log(ni)
            drift_global["n"] += 1
            drift_global["sum"] += d
            drift_global["sum2"] += d * d

            r = ni % drift_mod
            if r % 3 == 0:
                continue
            s = drift_idx[r]
            ds = drift_stats[s]
            ds["n"] += 1
            ds["sum"] += d
            ds["sum2"] += d * d

        if (j + 1) % max(1, cfg.S // 10) == 0:
            elapsed = time.time() - start
            (outroot / "progress.log").write_text(f"{j+1}/{cfg.S} samples in {elapsed:.1f}s\n", encoding="utf-8")

    runtime_s = time.time() - start

    # Write M2 distributions + TV to reference (t_ref=t_max)
    t_ref = t_max
    m2_rows = []
    tv_rows = []
    for k in range(1, cfg.k_max + 1):
        pref = normalize_counts(counts[k][t_ref]) if t_ref in counts[k] else None
        for t in cfg.t_list:
            pt = normalize_counts(counts[k][t])
            for idx, prob in enumerate(pt):
                m2_rows.append((k, t, idx, prob))
            if pref is not None:
                tv_rows.append((k, t, tv_distance(pt, pref)))

    write_csv(outroot / "m2_residue_probs.csv", ["k", "t", "state_index", "prob"], m2_rows)
    write_csv(outroot / "m2_tv_to_tmax.csv", ["k", "t", "tv_to_tmax"], tv_rows)

    # Write M3 a hist
    m3_rows = []
    for i, h in enumerate(a_hist_by_i):
        tot = sum(h.values())
        for a, c in sorted(h.items()):
            m3_rows.append((i, a, c, c / tot if tot else 0.0))
    write_csv(outroot / "m3_a_hist_by_step.csv", ["i", "a", "count", "prob"], m3_rows)

    # Write M3 correlations
    corr_rows = []
    for lag, st in corr.items():
        n = st["n"]
        if n == 0:
            continue
        mx = st["sx"] / n
        my = st["sy"] / n
        vx = st["sxx"] / n - mx * mx
        vy = st["syy"] / n - my * my
        cov = st["sxy"] / n - mx * my
        rho = cov / math.sqrt(vx * vy) if vx > 0 and vy > 0 else 0.0
        corr_rows.append((lag, n, rho))
    write_csv(outroot / "m3_a_autocorr.csv", ["lag", "n_pairs", "rho"], corr_rows)

    # Write conditional a|state (only for i=0 currently)
    cond_rows = []
    for s, buckets in cond_a_counts.items():
        tot = sum(buckets)
        if tot == 0:
            continue
        for a, c in enumerate(buckets):
            if a == 0:
                continue
            label = a if a <= a_max_bucket else f">{a_max_bucket}"
            cond_rows.append((cond_k, s, label, c, c / tot))
    write_csv(outroot / "m3_a0_cond_on_state.csv", ["k", "state_index", "a", "count", "prob"], cond_rows)

    # Write drift by state
    drift_rows = []
    for s, st in drift_stats.items():
        n = st["n"]
        if n == 0:
            continue
        mean = st["sum"] / n
        var = st["sum2"] / n - mean * mean
        drift_rows.append((drift_k, s, n, mean, var))
    write_csv(outroot / "m4_drift_by_state.csv", ["k", "state_index", "n", "mean_dlog", "var_dlog"], drift_rows)

    g_n = drift_global["n"]
    g_mean = drift_global["sum"] / g_n
    g_var = drift_global["sum2"] / g_n - g_mean * g_mean

    summary = {
        "run_id": run_id,
        "runtime_s": runtime_s,
        "t_max": t_max,
        "global_drift_mean": g_mean,
        "global_drift_var": g_var,
        "notes": {
            "cond_a_only_i0": True,
            "drift_aggregated_over_i": f"0..{t_max-1}",
        },
    }
    (outroot / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
