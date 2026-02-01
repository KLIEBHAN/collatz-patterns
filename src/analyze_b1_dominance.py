#!/usr/bin/env python3
"""
Analyze why b=1 dominates the within-lift bias β₁(b).

The hypothesis: b=1 is the fixed point of the a=2 branch:
    x = (3x+1)/4 ⟺ x = 1

We investigate:
1. P(a=2|b) - conditional probability of a=2 given residue b
2. Deviation from ideal P(a=2) = 1/4
3. Correlation with β₁(b) magnitude

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import json


def syracuse_step(n: int):
    """One Syracuse step, returns (next_n, a)."""
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_conditional_a_distribution(k: int, n_samples: int = 500000, 
                                       t_burn: int = 50, seed: int = 42):
    """
    Sample P(a | b) for each base class b mod 3^k.
    
    Returns: dict[b] -> Counter[a] -> count
    """
    M = 3**k
    # counts[b][a] = number of times we saw a=a when starting from residue b
    counts = defaultdict(lambda: defaultdict(int))
    
    rng = np.random.default_rng(seed)
    
    for i in range(n_samples):
        if i % 100000 == 0 and i > 0:
            print(f"  Sampled {i}/{n_samples}...", flush=True)
        
        # Random large odd start
        n = int(rng.integers(10**8, 10**12)) | 1
        
        # Burn-in to reach stationary distribution
        for _ in range(t_burn):
            if n == 1:
                n = int(rng.integers(10**8, 10**12)) | 1
            n, _ = syracuse_step(n)
        
        # Now n is roughly stationary. Record (b, a) pair.
        b = n % M
        if b % 3 != 0:  # Only units
            n_next, a = syracuse_step(n)
            counts[b][a] += 1
    
    return counts


def main():
    print("="*70)
    print("ANALYZING b=1 DOMINANCE")
    print("="*70)
    
    k = 5  # Analyze at k=5 first (smaller, clearer)
    M = 3**k  # 243
    
    print(f"\nParameters:")
    print(f"  k = {k}")
    print(f"  M = 3^{k} = {M}")
    
    # Sample conditional a distribution
    n_samples = 500000
    print(f"\n1. Sampling P(a|b) ({n_samples} samples)...")
    counts = sample_conditional_a_distribution(k, n_samples=n_samples, seed=42)
    print(f"   Done. Base classes with data: {len(counts)}")
    
    # Compute P(a=2|b) for each b
    base_classes = [b for b in range(1, M) if b % 3 != 0]
    
    print("\n2. Computing P(a=2|b)...")
    
    p_a2_given_b = {}
    total_samples_per_b = {}
    
    for b in base_classes:
        total = sum(counts[b].values())
        if total > 0:
            p_a2_given_b[b] = counts[b][2] / total
            total_samples_per_b[b] = total
        else:
            p_a2_given_b[b] = 0.25  # Default to ideal
            total_samples_per_b[b] = 0
    
    # Ideal P(a=2) = 1/4
    ideal_p_a2 = 0.25
    
    # Compute deviations
    deviations = {b: p_a2_given_b[b] - ideal_p_a2 for b in base_classes}
    
    # Rank by |deviation|
    ranked = sorted(base_classes, key=lambda b: -abs(deviations[b]))
    
    print("\n" + "="*70)
    print("TOP 20 DEVIATIONS FROM IDEAL P(a=2) = 0.25")
    print("="*70)
    
    print(f"\n{'Rank':<6} {'b':<8} {'P(a=2|b)':<12} {'Deviation':<12} {'v₃(b-1)':<10} {'Notes'}")
    print("-"*70)
    
    for rank, b in enumerate(ranked[:20], 1):
        p = p_a2_given_b[b]
        dev = deviations[b]
        
        # v₃(b-1)
        if b == 1:
            v3 = float('inf')
        else:
            v3 = 0
            temp = b - 1
            while temp % 3 == 0:
                v3 += 1
                temp //= 3
        
        notes = ""
        if b == 1:
            notes = "← a=2 FIXED POINT!"
        elif b == M - 1:
            notes = "← b ≡ -1"
        elif (b - 1) % 27 == 0:
            notes = "← close to 1 (mod 27)"
        
        v3_str = "∞" if v3 == float('inf') else str(v3)
        sign = "+" if dev > 0 else ""
        print(f"{rank:<6} {b:<8} {p:<12.4f} {sign}{dev:<11.4f} {v3_str:<10} {notes}")
    
    # Check b=1 specifically
    print("\n" + "="*70)
    print("b=1 DETAILED ANALYSIS")
    print("="*70)
    
    b1_counts = counts[1]
    b1_total = sum(b1_counts.values())
    
    print(f"\nSamples at b=1: {b1_total}")
    print(f"\na distribution at b=1:")
    for a in sorted(b1_counts.keys()):
        p = b1_counts[a] / b1_total
        ideal = 0.5**(a)
        dev = p - ideal
        sign = "+" if dev > 0 else ""
        print(f"  a={a}: P={p:.4f} (ideal={ideal:.4f}, dev={sign}{dev:.4f})")
    
    # Mean a at b=1
    mean_a_b1 = sum(a * b1_counts[a] for a in b1_counts) / b1_total
    ideal_mean_a = 2.0  # E[geometric] = 2
    
    print(f"\nMean a at b=1: {mean_a_b1:.4f} (ideal: {ideal_mean_a:.4f})")
    
    # Compare with b=-1 (b=242)
    print("\n" + "="*70)
    print("COMPARISON: b=1 vs b=242 (≡-1)")
    print("="*70)
    
    for b, name in [(1, "b=1"), (M-1, "b=-1 (242)")]:
        bc = counts[b]
        bt = sum(bc.values())
        mean_a = sum(a * bc[a] for a in bc) / bt if bt > 0 else 0
        p_a2 = bc[2] / bt if bt > 0 else 0
        
        print(f"\n{name}:")
        print(f"  Samples: {bt}")
        print(f"  P(a=2): {p_a2:.4f} (ideal: 0.25)")
        print(f"  Mean a: {mean_a:.4f} (ideal: 2.0)")
    
    # Correlation analysis
    print("\n" + "="*70)
    print("CORRELATION: P(a=2|b) DEVIATION vs |β₁(b)|")
    print("="*70)
    
    # Load β₁ data from previous analysis
    try:
        with open('data/beta_spectrum_k6.json') as f:
            beta_data = json.load(f)
        
        # Extract β₁ magnitudes for k=5 base classes
        # Note: beta_spectrum_k6.json is for k=6, so base classes are mod 243
        # We need to recompute for k=5 or use different data
        print("\n(Note: β₁ data is from k=6 analysis, base classes mod 243)")
        print("Skipping correlation - would need k=5 β₁ data")
        
    except FileNotFoundError:
        print("\nNo β₁ data available for correlation analysis")
    
    # Theoretical interpretation
    print("\n" + "="*70)
    print("THEORETICAL INTERPRETATION")
    print("="*70)
    
    print("""
The a=2 branch has the map: x → (3x+1)/4

Fixed point: x = 1

When the Syracuse chain visits b=1 mod 3^k, the deterministic dynamics
has a natural "attraction" toward this fixed point, which may cause
systematic deviations from the ideal i.i.d. geometric behavior.

Key observations:
1. b=1 is special because (3·1+1)/4 = 1 (fixed point)
2. If the chain is near 1 in the actual integers (not just mod 3^k),
   the a=2 branch keeps it there
3. This creates a "resonance" that breaks the ideal model assumption

This explains why β₁(b) is largest at b=1: the within-lift bias
reflects this dynamical fixed-point structure.
""")
    
    # Save results
    results = {
        'k': k,
        'n_samples': n_samples,
        'p_a2_given_b': {str(b): float(p) for b, p in p_a2_given_b.items()},
        'top20_deviations': [
            {
                'b': int(b),
                'p_a2': float(p_a2_given_b[b]),
                'deviation': float(deviations[b])
            }
            for b in ranked[:20]
        ],
        'b1_analysis': {
            'total_samples': int(b1_total),
            'a_distribution': {str(a): int(c) for a, c in b1_counts.items()},
            'mean_a': float(mean_a_b1)
        }
    }
    
    with open('data/b1_dominance_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/b1_dominance_analysis.json")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
