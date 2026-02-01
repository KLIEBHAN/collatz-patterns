#!/usr/bin/env python3
"""
k=7 Fourier Analysis

Testing predictions:
- Lifts of k=6 top modes: 3×85=255, 3×401=1203, 3×237=711, 3×249=747
- New-digit modes from β-spectrum on G₆

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import json


def build_exact_pi_k(k: int):
    """Build exact stationary distribution π_k."""
    print(f"  Building π_{k}...", flush=True)
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
    
    print(f"  Building {n}x{n} transition matrix...", flush=True)
    P = np.zeros((n, n))
    for i, x in enumerate(states):
        if i % 200 == 0:
            print(f"    Row {i}/{n}...", flush=True)
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m-1]
    
    print(f"  Solving for stationary distribution...", flush=True)
    A = P.T - np.eye(n)
    A[-1, :] = 1
    b = np.zeros(n)
    b[-1] = 1
    pi = np.linalg.solve(A, b)
    pi = pi / pi.sum()
    
    return states, {states[i]: pi[i] for i in range(n)}


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_empirical_distribution(k: int, n_samples: int, seed: int = 42, t_burn: int = 50):
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
    print("k=7 FOURIER ANALYSIS")
    print("="*70)
    
    k = 7
    M = 3**k           # 2187
    phi = 2 * 3**(k-1) # 1458
    nyquist = phi // 2 # 729
    
    print(f"\nParameters:")
    print(f"  k = {k}")
    print(f"  M = 3^{k} = {M}")
    print(f"  φ(3^{k}) = {phi}")
    print(f"  Nyquist = {nyquist}")
    
    # Predictions
    print(f"\n🎯 PREDICTIONS:")
    print(f"  Lifts of k=6 NEW-DIGIT tops (85,401):")
    print(f"    3×85 = 255")
    print(f"    3×401 = 1203")
    print(f"  Lifts of k=6 LIFT tops (237,249):")
    print(f"    3×237 = 711")
    print(f"    3×249 = 747")
    print(f"  Conjugates at k=7: j + (1458-j) = 1458")
    print(f"    255 + 1203 = {255 + 1203} (should be 1458)")
    print(f"    711 + 747 = {711 + 747} (should be 1458)")
    
    # Build model
    print(f"\n1. Building exact π_{k}...")
    states, pi_dict = build_exact_pi_k(k)
    n = len(states)
    print(f"   Done. {n} states.")
    
    # Build characters
    print(f"\n2. Building {phi} characters...")
    g = 2
    dlog = {}
    val = 1
    for i in range(phi):
        dlog[val] = i
        val = (val * g) % M
    print(f"   Done.")
    
    # Sample empirical
    n_samples = 500000
    print(f"\n3. Sampling empirical distribution ({n_samples} samples)...")
    emp_dist = sample_empirical_distribution(k, n_samples=n_samples, seed=42)
    print(f"   Done. Unique states: {len(emp_dist)}")
    
    # Compute Fourier deviations
    print(f"\n4. Computing Fourier deviations...")
    
    deviations = []
    for j in range(phi):
        if j % 200 == 0:
            print(f"    j = {j}/{phi}...", flush=True)
        
        # Δ̂(j) = Σ_x (μ(x) - π(x)) χ_j(x)
        delta_hat = 0
        for x in states:
            chi_j_x = np.exp(2j * np.pi * j * dlog[x] / phi)
            delta_hat += (emp_dist.get(x, 0) - pi_dict[x]) * chi_j_x
        
        deviations.append({
            'j': j,
            'magnitude': abs(delta_hat),
            'divisible_by_3': (j % 3 == 0),
            'r': j % 3,
            'm': (j - (j % 3)) // 3 if j % 3 != 0 else None
        })
    
    deviations.sort(key=lambda x: -x['magnitude'])
    
    # TV distance
    tv = sum(abs(pi_dict.get(x, 0) - emp_dist.get(x, 0)) for x in states) / 2
    
    # Results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    print(f"\nTotal Variation distance: {tv:.4f} ({100*tv:.2f}%)")
    
    print(f"\n🎯 TOP 15 PROOF TARGETS:")
    print(f"{'Rank':<6} {'j':<8} {'|Δ̂|':<12} {'r=j%3':<8} {'m':<8} {'Type':<12} {'Notes'}")
    print("-"*80)
    
    predicted_lifts = {255, 1203, 711, 747}
    
    for rank, d in enumerate(deviations[:15], 1):
        j = d['j']
        r = d['r']
        m = d['m']
        mode_type = "LIFT" if d['divisible_by_3'] else "NEW-DIGIT"
        
        notes = ""
        if j == 255:
            notes = "← 3×85 (predicted lift!)"
        elif j == 1203:
            notes = "← 3×401 (predicted lift!)"
        elif j == 711:
            notes = "← 3×237 (predicted lift!)"
        elif j == 747:
            notes = "← 3×249 (predicted lift!)"
        elif j in predicted_lifts:
            notes = "(predicted)"
        
        # Check conjugate
        conj = phi - j
        if conj != j and any(dd['j'] == conj for dd in deviations[:15]):
            if not notes:
                notes = f"(conj of {conj})"
        
        m_str = str(m) if m is not None else "—"
        print(f"{rank:<6} {j:<8} {d['magnitude']:<12.6f} {r:<8} {m_str:<8} {mode_type:<12} {notes}")
    
    # Check predictions
    print("\n" + "="*70)
    print("PREDICTION CHECK")
    print("="*70)
    
    j_to_rank = {d['j']: i+1 for i, d in enumerate(deviations)}
    
    print(f"\nPredicted LIFT modes (from k=6 tops):")
    for j, src in [(255, "3×85"), (1203, "3×401"), (711, "3×237"), (747, "3×249")]:
        rank = j_to_rank.get(j, "N/A")
        mag = next((d['magnitude'] for d in deviations if d['j'] == j), 0)
        status = "✅" if rank <= 10 else "⚠️" if rank <= 20 else "❌"
        print(f"  j={j} ({src}): Rank #{rank}, |Δ̂|={mag:.6f} {status}")
    
    # Mode distribution
    print("\n" + "="*70)
    print("MODE DISTRIBUTION")
    print("="*70)
    
    for cutoff in [10, 20, 30]:
        lift_count = sum(1 for d in deviations[:cutoff] if d['divisible_by_3'])
        new_count = cutoff - lift_count
        print(f"  Top-{cutoff}: LIFT={lift_count} ({100*lift_count/cutoff:.0f}%), NEW-DIGIT={new_count} ({100*new_count/cutoff:.0f}%)")
    
    # Conjugate pairs
    print("\n" + "="*70)
    print("CONJUGATE PAIRS IN TOP-15")
    print("="*70)
    
    top15_js = [d['j'] for d in deviations[:15]]
    for j in top15_js:
        conj = phi - j
        if conj in top15_js and j < conj:
            print(f"  {j} + {conj} = {j+conj} = φ(3^7) ✓")
    
    # Save results
    results = {
        'k': k,
        'phi': phi,
        'tv_distance': float(tv),
        'n_samples': n_samples,
        'top30': [{
            'j': d['j'],
            'magnitude': float(d['magnitude']),
            'r': d['r'],
            'm': d['m'],
            'divisible_by_3': d['divisible_by_3']
        } for d in deviations[:30]],
        'predictions': {
            'lift_255_rank': j_to_rank.get(255),
            'lift_1203_rank': j_to_rank.get(1203),
            'lift_711_rank': j_to_rank.get(711),
            'lift_747_rank': j_to_rank.get(747)
        }
    }
    
    with open('data/k7_fourier_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/k7_fourier_results.json")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
