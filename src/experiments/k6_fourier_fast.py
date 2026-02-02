#!/usr/bin/env python3
"""
k=6 Fourier Analysis - FAST VERSION (numpy floats)

Uses float64 instead of exact rationals for speed.
For numerical stability, this is more than sufficient.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple
import json
import sys


def build_P_k_float(k: int):
    """Build P_k matrix with floats (FAST)."""
    print(f"  Building P_{k} matrix (float version)...", flush=True)
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]
    n = len(states)
    print(f"  States: {n}", flush=True)
    
    r = 2 * 3**(k-1)
    D = 2**r - 1
    
    # Weights as floats
    w = np.array([2**(r-m) / D for m in range(1, r+1)])
    
    inv2 = pow(2, -1, M)
    inv2pow = [1]
    cur = inv2 % M
    for m in range(1, r+1):
        inv2pow.append(cur)
        cur = (cur * inv2) % M
    
    idx = {x:i for i, x in enumerate(states)}
    
    print(f"  Building {n}x{n} transition matrix...", flush=True)
    P = np.zeros((n, n))
    
    for i, x in enumerate(states):
        if i % 100 == 0:
            print(f"    Row {i}/{n}...", flush=True)
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m-1]
    
    # Solve for stationary distribution
    print(f"  Solving for stationary distribution π...", flush=True)
    
    # Method: solve (P^T - I)π = 0 with Σπ = 1
    # Use eigenvalue approach: π is left eigenvector for eigenvalue 1
    A = P.T - np.eye(n)
    A[-1, :] = 1  # Replace last equation with sum constraint
    b = np.zeros(n)
    b[-1] = 1
    
    pi = np.linalg.solve(A, b)
    
    # Normalize to ensure sum = 1
    pi = pi / pi.sum()
    
    return states, P, pi, idx


def syracuse_step(n: int) -> Tuple[int, int]:
    """One Syracuse step."""
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_empirical_distribution(k: int, n_samples: int, seed: int = 42, 
                                   t_burn: int = 50) -> Dict[int, float]:
    """Sample empirical distribution mod 3^k."""
    M = 3**k
    counts = defaultdict(int)
    rng = np.random.default_rng(seed)
    
    for i in range(n_samples):
        if i % 100000 == 0 and i > 0:
            print(f"    Sampled {i}/{n_samples}...", flush=True)
        
        n = int(rng.integers(10**8, 10**12)) | 1
        for _ in range(t_burn):
            if n == 1:
                n = int(rng.integers(10**8, 10**12)) | 1
            n, _ = syracuse_step(n)
        
        x = n % M
        if x % 3 != 0:
            counts[x] += 1
    
    total = sum(counts.values())
    return {x: c / total for x, c in counts.items()}


def main():
    print("="*70)
    print("k=6 FOURIER ANALYSIS - FAST VERSION")
    print("="*70)
    
    k = 6
    M = 3**k  # 729
    phi = 2 * 3**(k-1)  # 486
    nyquist = phi // 2  # 243
    
    print(f"\nParameters:")
    print(f"  k = {k}")
    print(f"  M = 3^{k} = {M}")
    print(f"  φ(3^{k}) = {phi}")
    print(f"  Nyquist = {nyquist}")
    
    print(f"\nGPT's Predictions:")
    print(f"  If inherited: j = 237 (3×79), 249 (3×83)")
    print(f"  If new-digit: j = 241 (243-2), 245 (243+2)")
    
    # Build model (FAST)
    print(f"\n1. Building exact π_{k} (float version)...")
    states, P, pi, idx = build_P_k_float(k)
    n = len(states)
    pi_dict = {states[i]: pi[i] for i in range(n)}
    print(f"   Done. {n} states.")
    
    # Build characters
    print(f"\n2. Building {phi} characters...")
    g = 2  # primitive root
    dlog = {}
    val = 1
    for i in range(phi):
        dlog[val] = i
        val = (val * g) % M
    
    characters = {}
    for j in range(phi):
        chi_j = {}
        for x in states:
            chi_j[x] = np.exp(2j * np.pi * j * dlog[x] / phi)
        characters[j] = chi_j
    print(f"   Done.")
    
    # Compute ideal Fourier coefficients
    print(f"\n3. Computing ideal Fourier coefficients...")
    ideal_coeffs = {}
    for j in range(phi):
        if j % 100 == 0:
            print(f"    j = {j}/{phi}...", flush=True)
        chi_j = characters[j]
        ideal_coeffs[j] = sum(pi_dict[x] * chi_j[x] for x in states)
    print(f"   Done.")
    
    # Sample empirical distribution
    n_samples = 400000
    print(f"\n4. Sampling empirical distribution ({n_samples} samples)...")
    emp_dist = sample_empirical_distribution(k, n_samples=n_samples, seed=42)
    print(f"   Done. Unique states: {len(emp_dist)}")
    
    # Compute empirical Fourier coefficients
    print(f"\n5. Computing empirical Fourier coefficients...")
    emp_coeffs = {}
    for j in range(phi):
        if j % 100 == 0:
            print(f"    j = {j}/{phi}...", flush=True)
        chi_j = characters[j]
        emp_coeffs[j] = sum(emp_dist.get(x, 0) * chi_j[x] for x in states)
    print(f"   Done.")
    
    # Compute deviations
    print(f"\n6. Computing deviations...")
    deviations = []
    for j in range(phi):
        ideal = ideal_coeffs[j]
        emp = emp_coeffs[j]
        deviations.append({
            'j': j,
            'total_diff': abs(ideal - emp),
            'ideal_mag': abs(ideal),
            'emp_mag': abs(emp),
            'divisible_by_3': (j % 3 == 0)
        })
    
    deviations.sort(key=lambda x: -x['total_diff'])
    
    # TV distance
    tv = sum(abs(pi_dict.get(x, 0) - emp_dist.get(x, 0)) for x in states) / 2
    
    # Results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    print(f"\nTotal Variation distance: {tv:.4f} ({100*tv:.2f}%)")
    
    print(f"\n🎯 TOP 10 PROOF TARGETS:")
    print(f"{'Rank':<6} {'j':<6} {'|Δ|':<12} {'j%3':<6} {'Type':<15} {'Notes'}")
    print("-"*70)
    
    for rank, d in enumerate(deviations[:10], 1):
        j = d['j']
        div3 = d['divisible_by_3']
        mode_type = "LIFT" if div3 else "NEW-DIGIT"
        
        notes = ""
        if j == 237:
            notes = "← 3×79 (predicted lift)"
        elif j == 249:
            notes = "← 3×83 (predicted lift)"
        elif j == 241:
            notes = "← 243-2 (predicted new)"
        elif j == 245:
            notes = "← 243+2 (predicted new)"
        
        # Check conjugate
        conj = phi - j
        if conj != j and any(dd['j'] == conj for dd in deviations[:10]):
            if not notes:
                notes = f"(conj of {conj})"
        
        print(f"{rank:<6} {j:<6} {d['total_diff']:<12.6f} {j%3:<6} {mode_type:<15} {notes}")
    
    # Check GPT's predictions
    print("\n" + "="*70)
    print("GPT PREDICTION CHECK")
    print("="*70)
    
    j_to_rank = {d['j']: i+1 for i, d in enumerate(deviations)}
    
    print(f"\nPredicted LIFT indices (if inherited from k=5):")
    for j in [237, 249]:
        rank = j_to_rank.get(j, "N/A")
        dev = next((d['total_diff'] for d in deviations if d['j'] == j), 0)
        print(f"  j={j}: Rank #{rank}, |Δ|={dev:.6f}")
    
    print(f"\nPredicted NEW-DIGIT indices (if new splitting):")
    for j in [241, 245]:
        rank = j_to_rank.get(j, "N/A")
        dev = next((d['total_diff'] for d in deviations if d['j'] == j), 0)
        print(f"  j={j}: Rank #{rank}, |Δ|={dev:.6f}")
    
    # Determine which hypothesis wins
    lift_indices = {237, 249}
    new_indices = {241, 245}
    
    top2 = {deviations[0]['j'], deviations[1]['j']}
    top5 = {d['j'] for d in deviations[:5]}
    
    print(f"\nActual top-2: {sorted(top2)}")
    print(f"Actual top-5: {sorted(top5)}")
    
    if top2 & lift_indices:
        print("\n✅ LIFT hypothesis supported! (inherited from k=5)")
    elif top2 & new_indices:
        print("\n✅ NEW-DIGIT hypothesis supported! (new splitting at k=6)")
    elif top5 & lift_indices:
        print("\n⚠️ LIFT indices in top-5 but not top-2")
    elif top5 & new_indices:
        print("\n⚠️ NEW-DIGIT indices in top-5 but not top-2")
    else:
        print("\n❓ Neither prediction in top-5 - unexpected result!")
    
    # Also check k=5 lifts of other top modes
    print(f"\nOther k=5 lifts (3×35=105, 3×127=381):")
    for j in [105, 381]:
        rank = j_to_rank.get(j, "N/A")
        dev = next((d['total_diff'] for d in deviations if d['j'] == j), 0)
        print(f"  j={j}: Rank #{rank}, |Δ|={dev:.6f}")
    
    # Conjugate pairs
    print("\n" + "="*70)
    print("CONJUGATE PAIRS IN TOP-10")
    print("="*70)
    
    top10_js = [d['j'] for d in deviations[:10]]
    for j in top10_js:
        conj = phi - j
        if conj in top10_js and j < conj:
            print(f"  {j} + {conj} = {j+conj} = φ(3^6) ✓")
    
    # Mode type distribution
    print("\n" + "="*70)
    print("MODE TYPE DISTRIBUTION")
    print("="*70)
    
    for cutoff in [10, 20]:
        lift_count = sum(1 for d in deviations[:cutoff] if d['divisible_by_3'])
        new_count = cutoff - lift_count
        print(f"  Top-{cutoff}: LIFT={lift_count}, NEW-DIGIT={new_count}")
    
    # Save results
    results = {
        'k': k,
        'phi': phi,
        'tv_distance': float(tv),
        'n_samples': n_samples,
        'top20': [{**d, 'total_diff': float(d['total_diff']), 
                   'ideal_mag': float(d['ideal_mag']), 
                   'emp_mag': float(d['emp_mag'])} for d in deviations[:20]],
        'predictions': {
            'lift_237_rank': j_to_rank.get(237),
            'lift_249_rank': j_to_rank.get(249),
            'new_241_rank': j_to_rank.get(241),
            'new_245_rank': j_to_rank.get(245),
            'lift_105_rank': j_to_rank.get(105),
            'lift_381_rank': j_to_rank.get(381)
        }
    }
    
    with open('data/k6_fourier_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/k6_fourier_results.json")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
