#!/usr/bin/env python3
"""
Signal vs B Analysis (Experiment A)

GPT recommendation: Run noise-floor scaling at B=10, 100, 1000
to determine signal(B) curve — where does real structure live?

For each B, fit: TV² = signal² + c/N
This separates true signal from sampling noise.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import json
import time


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_killed(k: int, n_samples: int, B: int, seed: int):
    """Sample with killed/regenerative process."""
    M = 3**k
    counts = defaultdict(int)
    rng = np.random.default_rng(seed)
    n_collected = 0
    n = int(rng.integers(10**10, 10**14)) | 1
    
    while n_collected < n_samples:
        if n <= B:
            n = int(rng.integers(10**10, 10**14)) | 1
            continue
        b = n % M
        if b % 3 != 0:
            counts[b] += 1
            n_collected += 1
        n, _ = syracuse_step(n)
    
    total = sum(counts.values())
    return {b: c / total for b, c in counts.items()}


def build_pi(k: int):
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


def tv_distance(mu, pi, states):
    return sum(abs(mu.get(x, 0) - pi.get(x, 0)) for x in states) / 2


def fit_signal(N_values, tv_values):
    """Fit TV² = signal² + c/N, return signal estimate."""
    x = np.array([1/N for N in N_values])
    y = np.array([tv**2 for tv in tv_values])
    
    # Linear regression: y = a + b*x where a = signal², b = c
    A = np.vstack([np.ones_like(x), x]).T
    result = np.linalg.lstsq(A, y, rcond=None)
    a, b = result[0]
    
    signal = np.sqrt(max(0, a))
    noise_coeff = np.sqrt(max(0, b))
    
    return signal, noise_coeff, a, b


def main():
    print("="*70)
    print("SIGNAL VS B ANALYSIS (Experiment A)")
    print("="*70)
    
    k = 6
    B_values = [10, 100, 1000, 10000, 100000]
    N_values = [100000, 200000, 400000]
    seeds = [42, 123, 456]
    
    print(f"\nParameters: k={k}")
    print(f"B values: {B_values}")
    print(f"N values: {N_values}")
    print(f"Seeds per (B,N): {len(seeds)}")
    
    # Build π once
    print("\nBuilding exact π₆...")
    states, pi = build_pi(k)
    G = len(states)
    print(f"|G₆| = {G}")
    
    results = []
    
    for B in B_values:
        print(f"\n{'='*70}")
        print(f"B = {B}")
        print(f"{'='*70}")
        
        tv_by_N = {}
        
        for N in N_values:
            tvs = []
            t0 = time.time()
            for seed in seeds:
                mu = sample_killed(k, N, B=B, seed=seed)
                tv = tv_distance(mu, pi, states)
                tvs.append(tv)
            
            mean_tv = np.mean(tvs)
            std_tv = np.std(tvs)
            tv_by_N[N] = mean_tv
            
            print(f"  N={N:>7}: TV = {mean_tv:.4f} ± {std_tv:.4f} ({mean_tv*100:.2f}%) [{time.time()-t0:.1f}s]")
        
        # Fit signal
        signal, noise_coeff, a, b = fit_signal(
            list(tv_by_N.keys()), 
            list(tv_by_N.values())
        )
        
        print(f"\n  Fit: TV² = {a:.6f} + {b:.1f}/N")
        print(f"  Signal = {signal:.4f} ({signal*100:.2f}%)")
        print(f"  Noise coefficient = {noise_coeff:.2f}")
        
        results.append({
            'B': B,
            'tv_by_N': {str(N): tv for N, tv in tv_by_N.items()},
            'signal': signal,
            'signal_pct': signal * 100,
            'noise_coeff': noise_coeff,
            'fit_intercept': a,
            'fit_slope': b
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY: signal(B) curve")
    print(f"{'='*70}")
    
    print(f"\n{'B':<10} {'Signal':<12} {'Signal %':<12} {'Noise Coeff':<12}")
    print("-"*50)
    for r in results:
        print(f"{r['B']:<10} {r['signal']:<12.4f} {r['signal_pct']:<12.2f} {r['noise_coeff']:<12.2f}")
    
    # Analysis
    print(f"\n{'='*70}")
    print("ANALYSIS")
    print(f"{'='*70}")
    
    signals = [r['signal'] for r in results]
    
    if signals[0] > 0.05 and signals[-1] < 0.01:
        print("\n✅ Clear signal(B) decay:")
        print(f"   B=10:     signal = {signals[0]*100:.1f}%")
        print(f"   B=100000: signal = {signals[-1]*100:.2f}%")
        print("\n   → Real structure lives at SMALL n (low B)")
        print("   → Bulk (high B) is essentially ideal")
    elif all(s > 0.03 for s in signals):
        print("\n⚠️ Signal persists across all B:")
        print("   → May indicate genuine obstruction at all scales")
    else:
        print("\n📊 Mixed pattern — see signal(B) curve for details")
    
    print(f"\n{'='*70}")
    print("DONE")
    print(f"{'='*70}")
    
    # Save
    with open('data/signal_vs_B.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/signal_vs_B.json")


if __name__ == "__main__":
    main()
