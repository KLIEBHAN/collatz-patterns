#!/usr/bin/env python3
"""
Noise Floor Test

GPT's suggestion: Check if 1.9% TV is signal or sampling noise.

Test:
1. Run 5 independent seeds at B=100000
2. Measure mean(TV) and std(TV)
3. Run with 4× samples — if TV drops like 1/√N, it's noise

Expected noise floor: √(|G|/N)/2 ≈ √(486/N)/2

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import time


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_killed_distribution(k: int, n_samples: int, B: int, seed: int):
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


def compute_tv(mu, pi, states):
    """Compute TV distance."""
    return sum(abs(mu.get(x, 0) - pi.get(x, 0)) for x in states) / 2


def main():
    print("="*70)
    print("NOISE FLOOR TEST")
    print("="*70)
    
    k = 6
    B = 100000
    G_size = 486  # |G_6| = φ(3^6)
    
    print(f"\nParameters: k={k}, B={B}, |G|={G_size}")
    
    # Build π once
    print("\nBuilding exact π₆...")
    states, pi = build_exact_pi(k)
    
    # Test 1: Multiple seeds at base sample size
    print("\n" + "="*70)
    print("TEST 1: 5 independent seeds (N=200,000)")
    print("="*70)
    
    n_samples_base = 200000
    seeds = [42, 123, 456, 789, 1011]
    tvs_base = []
    
    expected_noise = 0.5 * np.sqrt(G_size / n_samples_base)
    print(f"\nExpected noise floor: {expected_noise:.4f} ({expected_noise*100:.2f}%)")
    
    for seed in seeds:
        t0 = time.time()
        mu = sample_killed_distribution(k, n_samples_base, B=B, seed=seed)
        tv = compute_tv(mu, pi, states)
        tvs_base.append(tv)
        print(f"  Seed {seed}: TV = {tv:.4f} ({tv*100:.2f}%) [{time.time()-t0:.1f}s]")
    
    mean_tv = np.mean(tvs_base)
    std_tv = np.std(tvs_base)
    
    print(f"\n  Mean TV: {mean_tv:.4f} ({mean_tv*100:.2f}%)")
    print(f"  Std TV:  {std_tv:.4f} ({std_tv*100:.2f}%)")
    print(f"  CV:      {std_tv/mean_tv:.2f}")
    
    # Test 2: Scale sample size ×4
    print("\n" + "="*70)
    print("TEST 2: Scaling test (N × 4)")
    print("="*70)
    
    n_samples_4x = n_samples_base * 4
    expected_noise_4x = 0.5 * np.sqrt(G_size / n_samples_4x)
    
    print(f"\nN = {n_samples_4x:,}")
    print(f"Expected noise floor: {expected_noise_4x:.4f} ({expected_noise_4x*100:.2f}%)")
    print(f"If pure noise: TV should drop by factor √4 = 2")
    
    t0 = time.time()
    mu_4x = sample_killed_distribution(k, n_samples_4x, B=B, seed=42)
    tv_4x = compute_tv(mu_4x, pi, states)
    print(f"\n  TV (4× samples): {tv_4x:.4f} ({tv_4x*100:.2f}%) [{time.time()-t0:.1f}s]")
    
    # Compare
    tv_base_seed42 = tvs_base[0]  # Same seed for fair comparison
    ratio = tv_base_seed42 / tv_4x
    
    print(f"\n  TV ratio (N → 4N): {ratio:.2f}×")
    
    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)
    
    if ratio > 1.8:
        print(f"\n✅ TV dropped by {ratio:.1f}× (close to √4=2)")
        print("   → Most of the measured TV is SAMPLING NOISE!")
        print(f"   → True obstruction is likely BELOW {tv_4x*100:.1f}%")
        verdict = "NOISE"
    elif ratio > 1.3:
        print(f"\n⚠️ TV dropped by {ratio:.1f}× (between 1 and 2)")
        print("   → Mix of signal and noise")
        print(f"   → True obstruction is somewhere in [{tv_4x*100:.1f}%, {mean_tv*100:.1f}%]")
        verdict = "MIXED"
    else:
        print(f"\n🎯 TV only dropped by {ratio:.1f}× (much less than √4=2)")
        print("   → The ~{:.1f}% TV is mostly REAL SIGNAL!".format(mean_tv*100))
        print("   → This is the true 3-adic obstruction")
        verdict = "SIGNAL"
    
    # Additional: estimate true signal
    # If TV² = signal² + noise², and noise scales as 1/√N
    # Then TV(N)² - TV(4N)² ≈ 3/4 × noise(N)² if pure noise
    # Or TV(N)² ≈ TV(4N)² if pure signal
    
    signal_estimate = np.sqrt(max(0, tv_4x**2 - expected_noise_4x**2))
    print(f"\n  Estimated true signal: ~{signal_estimate:.4f} ({signal_estimate*100:.2f}%)")
    print(f"  Estimated noise at N=200k: ~{expected_noise:.4f} ({expected_noise*100:.2f}%)")
    
    print("\n" + "="*70)
    print(f"VERDICT: {verdict}")
    print("="*70)
    
    # Save results
    import json
    results = {
        'k': k,
        'B': B,
        'G_size': G_size,
        'n_samples_base': n_samples_base,
        'tvs_base': tvs_base,
        'mean_tv': mean_tv,
        'std_tv': std_tv,
        'n_samples_4x': n_samples_4x,
        'tv_4x': tv_4x,
        'ratio': ratio,
        'expected_noise_base': expected_noise,
        'expected_noise_4x': expected_noise_4x,
        'signal_estimate': signal_estimate,
        'verdict': verdict
    }
    
    with open('data/noise_floor_test.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/noise_floor_test.json")


if __name__ == "__main__":
    main()
