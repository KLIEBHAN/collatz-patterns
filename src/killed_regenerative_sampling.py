#!/usr/bin/env python3
"""
Killed/Regenerative Sampling for Collatz Analysis

Implements GPT's recommendation to remove absorption contamination:
- Stop counting when n ≤ B (kill at boundary)
- This separates true 3-adic mixing from boundary artifacts

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


def sample_killed_distribution(k: int, n_samples: int, B: int = 100,
                                t_max: int = 1000, seed: int = 42):
    """
    Sample empirical distribution mod 3^k with killed/regenerative process.
    
    Key difference from naive sampling:
    - We do NOT count visits when n ≤ B (the "boundary zone")
    - We regenerate (restart) when hitting n ≤ B
    - This removes absorption contamination from b=1
    
    Args:
        k: Level (mod 3^k)
        n_samples: Number of valid samples to collect
        B: Boundary threshold (kill when n ≤ B)
        t_max: Max steps before forced regeneration
        seed: Random seed
    
    Returns:
        counts: dict[b] -> count
        a_counts: dict[b][a] -> count for P(a|b) analysis
        stats: dict with regeneration statistics
    """
    M = 3**k
    counts = defaultdict(int)
    a_counts = defaultdict(lambda: defaultdict(int))
    
    rng = np.random.default_rng(seed)
    
    n_collected = 0
    n_regenerations = 0
    n_boundary_hits = 0
    n_timeout_regens = 0
    
    # Start with a large random odd number
    n = int(rng.integers(10**10, 10**14)) | 1
    
    while n_collected < n_samples:
        # Check if we need to regenerate
        if n <= B:
            # Hit boundary - regenerate
            n_boundary_hits += 1
            n_regenerations += 1
            n = int(rng.integers(10**10, 10**14)) | 1
            continue
        
        # Record this visit (only if n > B)
        b = n % M
        if b % 3 != 0:  # Only units
            counts[b] += 1
            n_collected += 1
            
            if n_collected % 100000 == 0:
                print(f"  Collected {n_collected}/{n_samples}...", flush=True)
        
        # Take a step and record (b, a) pair for P(a|b) analysis
        n_next, a = syracuse_step(n)
        
        if b % 3 != 0:
            a_counts[b][a] += 1
        
        n = n_next
        
        # Timeout regeneration (shouldn't happen often for large starts)
        # but prevents infinite loops
        if rng.random() < 1/t_max:
            n_timeout_regens += 1
            n_regenerations += 1
            n = int(rng.integers(10**10, 10**14)) | 1
    
    stats = {
        'n_samples': n_collected,
        'n_regenerations': n_regenerations,
        'n_boundary_hits': n_boundary_hits,
        'n_timeout_regens': n_timeout_regens,
        'boundary_B': B
    }
    
    return dict(counts), dict(a_counts), stats


def build_exact_pi_k(k: int):
    """Build exact stationary distribution π_k."""
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]
    n = len(states)
    r = 2 * 3**(k-1)
    D = 2**r - 1
    
    w = np.array([2**(r-m) / D for m in range(1, r+1)])
    
    inv2 = pow(2, -1, M)
    inv2pow = [1]
    cur = inv2
    for m in range(1, r+1):
        inv2pow.append(cur)
        cur = (cur * inv2) % M
    
    idx = {x:i for i, x in enumerate(states)}
    
    P = np.zeros((n, n))
    for i, x in enumerate(states):
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m-1]
    
    A = P.T - np.eye(n)
    A[-1, :] = 1
    b = np.zeros(n)
    b[-1] = 1
    pi = np.linalg.solve(A, b)
    pi = pi / pi.sum()
    
    return states, {states[i]: pi[i] for i in range(n)}


def main():
    print("="*70)
    print("KILLED/REGENERATIVE SAMPLING — Removing Absorption Contamination")
    print("="*70)
    
    k = 5
    M = 3**k  # 243
    B = 100   # Kill boundary
    
    print(f"\nParameters:")
    print(f"  k = {k}")
    print(f"  M = 3^{k} = {M}")
    print(f"  Boundary B = {B} (kill when n ≤ B)")
    
    # Build ideal π
    print(f"\n1. Building ideal π_{k}...")
    states, pi_dict = build_exact_pi_k(k)
    print(f"   Done. {len(states)} states.")
    
    # Sample with killed process
    n_samples = 500000
    print(f"\n2. Sampling with killed/regenerative process ({n_samples} samples)...")
    counts, a_counts, stats = sample_killed_distribution(k, n_samples, B=B, seed=42)
    
    print(f"\n   Sampling stats:")
    print(f"   - Total samples: {stats['n_samples']}")
    print(f"   - Regenerations: {stats['n_regenerations']}")
    print(f"   - Boundary hits: {stats['n_boundary_hits']}")
    print(f"   - Timeout regens: {stats['n_timeout_regens']}")
    
    # Convert to distribution
    total = sum(counts.values())
    mu_killed = {b: c / total for b, c in counts.items()}
    
    # Compute TV distance
    tv = sum(abs(pi_dict.get(x, 0) - mu_killed.get(x, 0)) for x in states) / 2
    
    print(f"\n3. Results:")
    print(f"   TV(μ_killed, π) = {tv:.4f} ({100*tv:.2f}%)")
    
    # Compare with naive sampling (for reference)
    print(f"\n4. Compare P(a=2|b) for key residues:")
    print(f"\n{'b':<8} {'P(a=2|b) killed':<18} {'Ideal':<10} {'Deviation':<12} {'Notes'}")
    print("-"*70)
    
    for b in [1, 17, 25, 49, 242]:
        if b in a_counts:
            total_b = sum(a_counts[b].values())
            p_a2 = a_counts[b].get(2, 0) / total_b if total_b > 0 else 0
            dev = p_a2 - 0.25
            
            notes = ""
            if b == 1:
                notes = "← Was 0.74 before!"
            elif b == 242:
                notes = "← b ≡ -1"
            elif b in [17, 25, 49]:
                notes = f"← ≡ {b % 8} (mod 8)"
            
            sign = "+" if dev > 0 else ""
            print(f"{b:<8} {p_a2:<18.4f} {0.25:<10.4f} {sign}{dev:<11.4f} {notes}")
    
    # β-spectrum analysis with killed data
    print("\n" + "="*70)
    print("β-SPECTRUM ANALYSIS (with killed sampling)")
    print("="*70)
    
    M_prev = 3**(k-1)  # 81
    base_classes = [b for b in range(1, M_prev) if b % 3 != 0]
    
    omega = np.exp(2j * np.pi / 3)
    
    beta_1 = {}
    for b in base_classes:
        lifts = [(b + M_prev * ell) % M for ell in range(3)]
        delta_lifts = [mu_killed.get(lift, 0) - pi_dict.get(lift, 0) for lift in lifts]
        beta_1[b] = sum(omega**ell * delta_lifts[ell] for ell in range(3))
    
    # Top contributors
    beta_1_ranked = sorted(base_classes, key=lambda b: -abs(beta_1[b]))
    
    print(f"\nTop 10 contributors to β₁(b) (KILLED sampling):")
    print(f"{'Rank':<6} {'b':<8} {'|β₁(b)|':<15} {'Notes'}")
    print("-"*50)
    
    for rank, b in enumerate(beta_1_ranked[:10], 1):
        notes = ""
        if b == 1:
            notes = "← Was #1 before!"
        elif b == 80:
            notes = "← b ≡ -1 (mod 81)"
        
        print(f"{rank:<6} {b:<8} {abs(beta_1[b]):<15.8f} {notes}")
    
    # Check b=1 rank
    rank_of_1 = beta_1_ranked.index(1) + 1 if 1 in beta_1_ranked else "N/A"
    print(f"\n→ Rank of b=1: #{rank_of_1} (was #1 in contaminated sampling)")
    
    # Energy split
    energy_beta_1 = sum(abs(beta_1[b])**2 for b in base_classes)
    print(f"\nWithin-lift energy (β₁): {energy_beta_1:.6e}")
    
    # Save results
    results = {
        'k': k,
        'boundary_B': B,
        'n_samples': n_samples,
        'tv_distance': float(tv),
        'stats': stats,
        'p_a2_killed': {
            str(b): float(a_counts[b].get(2, 0) / sum(a_counts[b].values()))
            for b in [1, 17, 25, 49, 242] if b in a_counts and sum(a_counts[b].values()) > 0
        },
        'beta_1_top10': [
            {'b': int(b), 'magnitude': float(abs(beta_1[b]))}
            for b in beta_1_ranked[:10]
        ],
        'b1_rank': rank_of_1
    }
    
    with open('data/killed_regenerative_k5.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/killed_regenerative_k5.json")
    
    print("\n" + "="*70)
    print("COMPARISON: Before vs After Decontamination")
    print("="*70)
    
    print(f"""
    Metric                    | Contaminated | Killed/Regen
    --------------------------|--------------|-------------
    P(a=2|b=1)               | 0.7391       | {results['p_a2_killed'].get('1', 'N/A'):.4f}
    b=1 rank in β₁           | #1           | #{rank_of_1}
    TV(μ, π)                 | ~5.2%        | {100*tv:.2f}%
    """)
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
