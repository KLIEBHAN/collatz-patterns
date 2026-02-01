#!/usr/bin/env python3
"""
B-Sweep Analysis (Step 4)

GPT's suggestion: Run killed analysis at k=6 for B ∈ {10, 100, 1000, 10^5}.
Track: TV, top-10 modes, dominant base frequency m.

If spectrum stabilizes as B increases → approaching true bulk obstruction.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import json


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_killed_distribution(k: int, n_samples: int, B: int, seed: int = 42):
    """Sample with killed/regenerative process."""
    M = 3**k
    counts = defaultdict(int)
    rng = np.random.default_rng(seed)
    n_collected = 0
    n_regen = 0
    n = int(rng.integers(10**10, 10**14)) | 1
    
    while n_collected < n_samples:
        if n <= B:
            n = int(rng.integers(10**10, 10**14)) | 1
            n_regen += 1
            continue
        b = n % M
        if b % 3 != 0:
            counts[b] += 1
            n_collected += 1
        n, _ = syracuse_step(n)
    
    total = sum(counts.values())
    return {b: c / total for b, c in counts.items()}, n_regen


def build_exact_pi(k: int):
    """Build exact stationary distribution π_k."""
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]
    n_states = len(states)
    r = 2 * 3**(k-1)
    D = 2**r - 1
    
    w = np.array([2**(r-m) / D for m in range(1, r+1)])
    
    inv2 = pow(2, -1, M)
    inv2pow = [1]
    cur = inv2
    for m in range(1, r+1):
        inv2pow.append(cur)
        cur = (cur * inv2) % M
    
    idx = {x: i for i, x in enumerate(states)}
    
    P = np.zeros((n_states, n_states))
    for i, x in enumerate(states):
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m-1]
    
    A = P.T - np.eye(n_states)
    A[-1, :] = 1
    b_vec = np.zeros(n_states)
    b_vec[-1] = 1
    pi = np.linalg.solve(A, b_vec)
    pi = pi / pi.sum()
    
    return states, {states[i]: pi[i] for i in range(n_states)}


def compute_fourier(mu, pi, k):
    """Compute Fourier coefficients and return top modes."""
    M = 3**k
    phi_k = 2 * 3**(k-1)
    states = [x for x in range(1, M) if x % 3 != 0]
    
    # Build discrete log
    g = 2
    x_to_exp = {}
    val = 1
    for t in range(phi_k):
        x_to_exp[val] = t
        val = (val * g) % M
    
    # Delta
    delta = {x: mu.get(x, 0) - pi.get(x, 0) for x in states}
    
    # TV distance
    tv = sum(abs(d) for d in delta.values()) / 2
    
    # Fourier
    delta_hat = {}
    for j in range(phi_k):
        coeff = 0
        for x in states:
            t = x_to_exp[x]
            phase = np.exp(2j * np.pi * j * t / phi_k)
            coeff += delta[x] * phase
        delta_hat[j] = coeff
    
    # Sort by magnitude
    sorted_modes = sorted(delta_hat.items(), key=lambda x: abs(x[1]), reverse=True)
    
    return tv, sorted_modes


def main():
    print("="*70)
    print("B-SWEEP ANALYSIS")
    print("="*70)
    
    k = 6
    n_samples = 200000  # Reduced for speed
    B_values = [10, 100, 1000, 10000, 100000]
    
    print(f"\nParameters: k={k}, n_samples={n_samples}")
    print(f"B values: {B_values}")
    
    # Build π once
    print("\nBuilding exact π₆...")
    states, pi = build_exact_pi(k)
    
    results = []
    
    for B in B_values:
        print(f"\n{'='*70}")
        print(f"B = {B}")
        print(f"{'='*70}")
        
        # Sample
        print(f"  Sampling (killed)...", end=" ", flush=True)
        mu, n_regen = sample_killed_distribution(k, n_samples, B=B, seed=42)
        print(f"done ({n_regen} regenerations)")
        
        # Fourier analysis
        tv, sorted_modes = compute_fourier(mu, pi, k)
        
        print(f"\n  TV distance: {tv:.4f} ({tv*100:.2f}%)")
        
        # Top-5 modes
        print(f"\n  Top-5 Fourier modes:")
        print(f"  {'Rank':<6} {'j':<8} {'|Δ̂|':<12} {'j%3':<6} {'m=(j-r)/3':<10}")
        print(f"  {'-'*42}")
        
        top_modes = []
        for i, (j, coeff) in enumerate(sorted_modes[:5]):
            r = j % 3
            m = (j - r) // 3 if r != 0 else j // 3
            mode_type = "LIFT" if r == 0 else "NEW"
            print(f"  {i+1:<6} {j:<8} {abs(coeff):<12.6f} {r:<6} {m:<10}")
            top_modes.append({'j': j, 'mag': abs(coeff), 'r': r, 'm': m})
        
        # Dominant base frequency for NEW-DIGIT modes
        new_modes = [(j, c) for j, c in sorted_modes if j % 3 != 0]
        if new_modes:
            top_new = new_modes[0]
            j_top = top_new[0]
            r_top = j_top % 3
            m_top = (j_top - r_top) // 3
            print(f"\n  Dominant NEW-DIGIT: j={j_top}, m={m_top}, r={r_top}")
        
        results.append({
            'B': B,
            'tv': tv,
            'n_regen': n_regen,
            'top5': top_modes,
            'dominant_m': m_top if new_modes else None
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY: How does B affect the results?")
    print(f"{'='*70}")
    
    print(f"\n{'B':<10} {'TV':<10} {'Top-2 j':<15} {'Dom. m':<10} {'Regens':<10}")
    print("-"*55)
    
    for r in results:
        top2 = f"{r['top5'][0]['j']}, {r['top5'][1]['j']}"
        print(f"{r['B']:<10} {r['tv']:.4f}    {top2:<15} {r['dominant_m']:<10} {r['n_regen']:<10}")
    
    # Check stability
    print(f"\n{'='*70}")
    print("STABILITY ANALYSIS")
    print(f"{'='*70}")
    
    dominant_ms = [r['dominant_m'] for r in results]
    top_js = [r['top5'][0]['j'] for r in results]
    
    if len(set(dominant_ms)) == 1:
        print(f"\n✅ Dominant base frequency m={dominant_ms[0]} is STABLE across all B!")
        print("   → This is likely a genuine bulk feature.")
    else:
        print(f"\n⚠️ Dominant m varies with B: {dominant_ms}")
        print("   → Still seeing survival/boundary effects.")
    
    if len(set(top_js)) == 1:
        print(f"\n✅ Top mode j={top_js[0]} is STABLE across all B!")
    else:
        print(f"\n⚠️ Top mode varies with B: {top_js}")
    
    # TV trend
    tvs = [r['tv'] for r in results]
    if tvs[-1] < tvs[0] * 0.8:
        print(f"\n📉 TV decreases as B increases: {tvs[0]:.4f} → {tvs[-1]:.4f}")
        print("   → Higher B removes more boundary effects.")
    elif tvs[-1] > tvs[0] * 1.2:
        print(f"\n📈 TV increases as B increases: {tvs[0]:.4f} → {tvs[-1]:.4f}")
    else:
        print(f"\n📊 TV roughly stable: {tvs[0]:.4f} → {tvs[-1]:.4f}")
    
    print(f"\n{'='*70}")
    print("DONE")
    print(f"{'='*70}")
    
    # Save
    with open('data/b_sweep_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/b_sweep_results.json")


if __name__ == "__main__":
    main()
