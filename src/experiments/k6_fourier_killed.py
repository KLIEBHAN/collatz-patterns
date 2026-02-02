#!/usr/bin/env python3
"""
k=6 Fourier Analysis with Killed Sampling

Compare contaminated vs killed results to see the true 3-adic structure.

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


def sample_killed_distribution(k: int, n_samples: int, B: int = 100, seed: int = 42):
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
            if n_collected % 100000 == 0:
                print(f"    {n_collected}/{n_samples}...", flush=True)
        n, _ = syracuse_step(n)
    
    total = sum(counts.values())
    return {b: c / total for b, c in counts.items()}


def build_exact_pi_k(k: int):
    print(f"  Building P_{k} matrix...", flush=True)
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
    
    print(f"  Solving for π...", flush=True)
    A = P.T - np.eye(n)
    A[-1, :] = 1
    b = np.zeros(n)
    b[-1] = 1
    pi = np.linalg.solve(A, b)
    pi = pi / pi.sum()
    
    return states, {states[i]: pi[i] for i in range(n)}


def main():
    print("="*70)
    print("k=6 FOURIER ANALYSIS — KILLED SAMPLING")
    print("="*70)
    
    k = 6
    M = 3**k  # 729
    phi = 2 * 3**(k-1)  # 486
    
    print(f"\nParameters: k={k}, M={M}, φ={phi}")
    
    # Build π
    print(f"\n1. Building ideal π_{k}...")
    states, pi_dict = build_exact_pi_k(k)
    print(f"   Done. {len(states)} states.")
    
    # Build characters
    print(f"\n2. Building characters...")
    g = 2
    dlog = {}
    val = 1
    for i in range(phi):
        dlog[val] = i
        val = (val * g) % M
    
    # Sample killed
    n_samples = 400000
    print(f"\n3. Sampling (killed, B=100, {n_samples} samples)...")
    mu_killed = sample_killed_distribution(k, n_samples, B=100, seed=42)
    print(f"   Done.")
    
    # Compute Fourier deviations
    print(f"\n4. Computing Fourier deviations...")
    delta = {x: mu_killed.get(x, 0) - pi_dict.get(x, 0) for x in states}
    
    deviations = []
    for j in range(phi):
        if j % 100 == 0:
            print(f"    j={j}/{phi}...", flush=True)
        coeff = sum(delta[x] * np.exp(2j * np.pi * j * dlog[x] / phi) for x in states)
        deviations.append({
            'j': j,
            'magnitude': abs(coeff),
            'divisible_by_3': (j % 3 == 0)
        })
    
    deviations.sort(key=lambda x: -x['magnitude'])
    
    # TV distance
    tv = sum(abs(delta[x]) for x in states) / 2
    
    # Results
    print("\n" + "="*70)
    print("RESULTS (KILLED SAMPLING)")
    print("="*70)
    
    print(f"\nTV(μ_killed, π) = {tv:.4f} ({100*tv:.2f}%)")
    print(f"(Was ~8.3% with contaminated sampling)")
    
    print(f"\n🎯 TOP 10 PROOF TARGETS (KILLED):")
    print(f"{'Rank':<6} {'j':<8} {'|Δ̂|':<12} {'Type':<12}")
    print("-"*50)
    
    for rank, d in enumerate(deviations[:10], 1):
        j = d['j']
        mode_type = "LIFT" if d['divisible_by_3'] else "NEW-DIGIT"
        print(f"{rank:<6} {j:<8} {d['magnitude']:<12.6f} {mode_type:<12}")
    
    # Mode distribution
    print("\n" + "="*70)
    print("MODE DISTRIBUTION (KILLED)")
    print("="*70)
    
    for cutoff in [10, 20]:
        lift_count = sum(1 for d in deviations[:cutoff] if d['divisible_by_3'])
        new_count = cutoff - lift_count
        print(f"  Top-{cutoff}: LIFT={lift_count} ({100*lift_count/cutoff:.0f}%), NEW-DIGIT={new_count} ({100*new_count/cutoff:.0f}%)")
    
    # Save results
    results = {
        'k': k,
        'sampling': 'killed',
        'boundary_B': 100,
        'n_samples': n_samples,
        'tv_distance': float(tv),
        'top20': [{
            'j': d['j'],
            'magnitude': float(d['magnitude']),
            'divisible_by_3': d['divisible_by_3']
        } for d in deviations[:20]]
    }
    
    with open('data/k6_fourier_killed.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to data/k6_fourier_killed.json")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
