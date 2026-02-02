#!/usr/bin/env python3
"""
k=6 Fourier Analysis - Testing GPT's Prediction

GPT predicted for k=6 (φ(3^6) = 486, Nyquist = 243):
- If inherited from k=5: j = 237 (3×79), 249 (3×83) will dominate
- If new-digit splitting: j = 241 (243-2), 245 (243+2) will dominate

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import sympy as sp
from typing import Dict, List, Tuple
import json
import sys


def build_exact_P_k(k: int):
    """Build exact P_k matrix with rational arithmetic."""
    print(f"  Building P_{k} matrix (this takes a while for k={k})...", flush=True)
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]
    n = len(states)
    print(f"  States: {n}", flush=True)
    
    r = 2 * 3**(k-1)
    D = 2**r - 1
    w = [None] + [sp.Rational(2**(r-m), D) for m in range(1, r+1)]
    
    inv2 = pow(2, -1, M)
    inv2pow = [None]*(r+1)
    cur = inv2 % M
    for m in range(1, r+1):
        inv2pow[m] = cur
        cur = (cur * inv2) % M
    
    idx = {x:i for i, x in enumerate(states)}
    
    print(f"  Building {n}x{n} transition matrix...", flush=True)
    P = sp.MutableDenseMatrix(n, n, [0]*(n*n))
    
    for i, x in enumerate(states):
        if i % 50 == 0:
            print(f"    Row {i}/{n}...", flush=True)
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m]
    
    P = sp.Matrix(P)
    
    print(f"  Solving for stationary distribution π...", flush=True)
    A = P.T - sp.eye(n)
    b = sp.Matrix([0]*n)
    A[n-1, :] = sp.Matrix([[1]*n])
    b[n-1] = 1
    pi = A.LUsolve(b)
    
    return states, pi


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
        if i % 50000 == 0 and i > 0:
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


def build_characters(k: int, states: List[int]) -> Tuple[Dict, Dict]:
    """Build multiplicative characters on (Z/3^k Z)*."""
    M = 3**k
    phi = 2 * 3**(k-1)
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
    
    return characters, dlog


def main():
    print("="*70)
    print("k=6 FOURIER ANALYSIS - Testing GPT's Prediction")
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
    
    # Build exact model
    print(f"\n1. Building exact π_{k}...")
    states, pi = build_exact_P_k(k)
    n = len(states)
    pi_float = {states[i]: float(pi[i]) for i in range(n)}
    print(f"   Done. {n} states.")
    
    # Build characters
    print(f"\n2. Building {phi} characters...")
    characters, dlog = build_characters(k, states)
    print(f"   Done.")
    
    # Compute ideal Fourier coefficients
    print(f"\n3. Computing ideal Fourier coefficients...")
    ideal_coeffs = {}
    for j in range(phi):
        if j % 50 == 0:
            print(f"    j = {j}/{phi}...", flush=True)
        chi_j = characters[j]
        ideal_coeffs[j] = sum(pi_float[x] * chi_j[x] for x in states)
    print(f"   Done.")
    
    # Sample empirical distribution
    n_samples = 400000  # More samples for larger state space
    print(f"\n4. Sampling empirical distribution ({n_samples} samples)...")
    emp_dist = sample_empirical_distribution(k, n_samples=n_samples, seed=42)
    print(f"   Done. Unique states: {len(emp_dist)}")
    
    # Compute empirical Fourier coefficients
    print(f"\n5. Computing empirical Fourier coefficients...")
    emp_coeffs = {}
    for j in range(phi):
        if j % 50 == 0:
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
    tv = sum(abs(pi_float.get(x, 0) - emp_dist.get(x, 0)) for x in states) / 2
    
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
        elif j + d['j'] == phi and j != 0:
            notes = "(conjugate in top-10)"
        
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
    
    # Find ranks of predicted indices
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
    
    print(f"\nActual top-2: {sorted(top2)}")
    
    if top2 & lift_indices:
        print("→ LIFT hypothesis supported! (inherited from k=5)")
    elif top2 & new_indices:
        print("→ NEW-DIGIT hypothesis supported! (new splitting at k=6)")
    else:
        print("→ Neither prediction in top-2 - unexpected result!")
    
    # Conjugate analysis
    print("\n" + "="*70)
    print("CONJUGATE PAIRS IN TOP-10")
    print("="*70)
    
    top10_js = [d['j'] for d in deviations[:10]]
    for j in top10_js:
        conj = phi - j
        if conj in top10_js and j < conj:
            print(f"  {j} + {conj} = {j+conj} = φ(3^6) ✓")
    
    # Lift vs new-digit energy in top-20
    print("\n" + "="*70)
    print("MODE TYPE DISTRIBUTION (Top 20)")
    print("="*70)
    
    lift_count = sum(1 for d in deviations[:20] if d['divisible_by_3'])
    new_count = 20 - lift_count
    
    print(f"  LIFT modes (j%3=0):     {lift_count}/20")
    print(f"  NEW-DIGIT modes (j%3≠0): {new_count}/20")
    
    # Save results
    results = {
        'k': k,
        'phi': phi,
        'tv_distance': tv,
        'n_samples': n_samples,
        'top20': deviations[:20],
        'predictions': {
            'lift_237_rank': j_to_rank.get(237),
            'lift_249_rank': j_to_rank.get(249),
            'new_241_rank': j_to_rank.get(241),
            'new_245_rank': j_to_rank.get(245)
        }
    }
    
    with open('data/k6_fourier_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\nResults saved to data/k6_fourier_results.json")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
