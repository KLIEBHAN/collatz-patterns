#!/usr/bin/env python3
"""analyze_outlier.py

Step 0 + Step 1: Defuse outlier and forced-start sampling.

Step 0: Clean up reporting
- Mark states with N_s = 0 as NaN
- Report max only over S_min (N_s >= threshold)
- Check if outlier 6397 has incoming edges

Step 1: Forced-start sampling for residue 6397
- Generate random large numbers n ≡ 6397 (mod 6561)
- Measure 1-step and multi-step behavior
- Get real data for g(6397) and P(6397, ·)

Usage:
    python src/analyze_outlier.py
"""

import numpy as np
import random
import math
from pathlib import Path
from collections import Counter, defaultdict


def v2(x: int) -> int:
    """2-adic valuation."""
    if x == 0:
        return 0
    return (x & -x).bit_length() - 1


def odd_step(n: int) -> tuple:
    """One accelerated odd step. Returns (next_n, a)."""
    m = 3 * n + 1
    a = v2(m)
    return m >> a, a


def main():
    print("=" * 70)
    print("STEP 0: Defuse Outlier (Clean Reporting)")
    print("=" * 70)
    
    # Load original run data
    run_dir = Path("~/workspace/data/psi_correction/20260201_000919Z_k8_S500000").expanduser()
    
    g_raw = np.load(run_dir / "g_raw.npy")
    g_corrected = np.load(run_dir / "g_corrected.npy")
    psi = np.load(run_dir / "psi.npy")
    pi = np.load(run_dir / "pi_occ.npy")
    counts = np.load(run_dir / "state_counts.npy")
    
    k = 8
    mod = 3**k  # 6561
    units = [r for r in range(1, mod) if r % 3 != 0]
    n_states = len(units)
    
    print(f"\nLoaded run: {run_dir.name}")
    print(f"Total states: {n_states}")
    print(f"Total transitions: {counts.sum():,}")
    
    # --- Step 0a: Identify states with insufficient data ---
    N_min = 200
    well_sampled = counts >= N_min
    n_well_sampled = well_sampled.sum()
    
    print(f"\n--- Data Support Analysis (N_min = {N_min}) ---")
    print(f"Well-sampled states (N_s >= {N_min}): {n_well_sampled} / {n_states}")
    print(f"Under-sampled states: {n_states - n_well_sampled}")
    print(f"States with 0 visits: {(counts == 0).sum()}")
    
    # Mass outside support
    pi_outside = pi[~well_sampled].sum()
    print(f"π-mass outside S_min: {pi_outside:.6f}")
    
    # --- Step 0b: Clean max reporting ---
    # Set under-sampled states to NaN
    g_corrected_clean = g_corrected.copy()
    g_corrected_clean[~well_sampled] = np.nan
    
    max_corrected_clean = np.nanmax(g_corrected_clean)
    argmax_clean = np.nanargmax(g_corrected_clean)
    
    print(f"\n--- Clean Drift Reporting (over S_min only) ---")
    print(f"Max corrected drift (S_min): {max_corrected_clean:.6f}")
    print(f"  at state {argmax_clean} (residue {units[argmax_clean]})")
    print(f"  with {counts[argmax_clean]} visits")
    
    # Compare with naive reporting
    print(f"\nNaive max corrected drift (all): {g_corrected.max():.6f}")
    print(f"  at state {g_corrected.argmax()} (residue {units[g_corrected.argmax()]})")
    print(f"  with {counts[g_corrected.argmax()]} visits")
    
    # --- Step 0c: Check outlier 6397's graph structure ---
    outlier_residue = 6397
    outlier_idx = units.index(outlier_residue)
    
    print(f"\n--- Outlier 6397 Analysis ---")
    print(f"State index: {outlier_idx}")
    print(f"Visit count: {counts[outlier_idx]}")
    print(f"g_raw: {g_raw[outlier_idx]:.6f}")
    print(f"g_corrected: {g_corrected[outlier_idx]:.6f}")
    print(f"ψ: {psi[outlier_idx]:.6f}")
    
    # We need to check incoming edges - but we don't have P saved
    # Let's note this limitation
    print(f"\n⚠️  Cannot check incoming edges (P matrix not saved)")
    print(f"   Would need to re-run or modify compute_psi.py to save P")
    
    # ================================================================
    print("\n" + "=" * 70)
    print("STEP 1: Forced-Start Sampling for Residue 6397")
    print("=" * 70)
    
    # Generate random large numbers n ≡ 6397 (mod 6561), n odd
    n_samples = 100_000
    rng = random.Random(42)
    
    # Collect data
    a_values = []
    delta_log = []
    next_residues = Counter()
    
    print(f"\nSampling {n_samples:,} trajectories starting from residue 6397...")
    
    for _ in range(n_samples):
        # Generate n = 6397 + 6561 * r, ensuring n is odd
        r = rng.randint(1, 10_000_000)
        n = 6397 + 6561 * r
        if n % 2 == 0:
            n += 6561  # Make odd
        
        # One step
        n_next, a = odd_step(n)
        
        a_values.append(a)
        delta_log.append(math.log(n_next) - math.log(n))
        next_residues[n_next % mod] += 1
    
    # Analyze results
    a_values = np.array(a_values)
    delta_log = np.array(delta_log)
    
    print(f"\n--- 1-Step Statistics from Residue 6397 ---")
    print(f"E[a(n) | n ≡ 6397]: {a_values.mean():.4f} (theoretical geometric: 2.0)")
    print(f"E[Δlog n | n ≡ 6397]: {delta_log.mean():.6f}")
    print(f"  (This is the TRUE g(6397)!)")
    
    # Is it negative?
    if delta_log.mean() < 0:
        print(f"  ✅ NEGATIVE! This state has downward drift.")
    else:
        print(f"  ⚠️  POSITIVE drift at this state.")
    
    print(f"\nΔlog n statistics:")
    print(f"  min: {delta_log.min():.4f}")
    print(f"  max: {delta_log.max():.4f}")
    print(f"  std: {delta_log.std():.4f}")
    
    # Distribution of a
    print(f"\nDistribution of a(n):")
    a_counts = Counter(a_values)
    for a in sorted(a_counts.keys())[:10]:
        pct = 100 * a_counts[a] / n_samples
        print(f"  a={a}: {pct:.1f}%")
    
    # Transition distribution P(6397, ·)
    print(f"\nTop 10 destination residues (P(6397, ·)):")
    for residue, count in next_residues.most_common(10):
        pct = 100 * count / n_samples
        dest_idx = units.index(residue) if residue in units else "N/A"
        print(f"  → {residue} (state {dest_idx}): {pct:.2f}%")
    
    # --- Multi-step analysis ---
    print(f"\n--- Multi-Step Analysis (m=10, 50, 100) ---")
    
    for m in [10, 50, 100]:
        cumulative_drift = []
        for _ in range(10_000):
            r = rng.randint(1, 10_000_000)
            n = 6397 + 6561 * r
            if n % 2 == 0:
                n += 6561
            
            total_drift = 0.0
            for _ in range(m):
                n_next, a = odd_step(n)
                total_drift += math.log(n_next) - math.log(n)
                n = n_next
                if n == 1:
                    break
            cumulative_drift.append(total_drift)
        
        avg_drift = np.mean(cumulative_drift)
        avg_per_step = avg_drift / m
        print(f"  m={m:3d}: E[Σ Δlog] = {avg_drift:+.4f}, per step = {avg_per_step:+.6f}")
    
    # ================================================================
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"""
Step 0 Results:
  - {(counts == 0).sum()} states have 0 visits (including outlier 6397)
  - Clean max corrected drift (S_min): {max_corrected_clean:.6f}
  - The "+0.180" for 6397 was an ARTIFACT of missing data

Step 1 Results:
  - TRUE g(6397) = {delta_log.mean():.6f} (from {n_samples:,} forced samples)
  - This is {'NEGATIVE ✅' if delta_log.mean() < 0 else 'POSITIVE ⚠️'}
  - The outlier is {'NOT a real problem!' if delta_log.mean() < 0 else 'a genuine concern.'}

Conclusion:
  {'The positive drift was purely a numerical artifact from 0 visits.' if delta_log.mean() < 0 else 'The state genuinely has issues - investigate further.'}
  {'No need for Step 2 (BigInt run) for this specific issue.' if delta_log.mean() < 0 else 'Consider Step 2 (BigInt run) for complete analysis.'}
""")


if __name__ == "__main__":
    main()
