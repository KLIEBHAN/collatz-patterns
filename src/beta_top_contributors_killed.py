#!/usr/bin/env python3
"""
β Top Contributors Under Killed Sampling (Step 2)

GPT's suggestion: List top b ∈ G₅ by |β₁(b)|, |β₂(b)| at k=6 killed.
Check if these b's have anomalous P(a|b) or lift-choice distributions.

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


def sample_killed_with_details(k: int, n_samples: int, B: int = 100, seed: int = 42):
    """Sample with killed process, tracking a-values and lift indices."""
    M = 3**k
    M_prev = 3**(k-1)
    
    # Counts per residue
    counts = defaultdict(int)
    # P(a|b) tracking
    a_given_b = defaultdict(lambda: defaultdict(int))
    # Lift index tracking: which lift ℓ ∈ {0,1,2} for each base b
    lift_given_b = defaultdict(lambda: defaultdict(int))
    
    rng = np.random.default_rng(seed)
    n_collected = 0
    n = int(rng.integers(10**10, 10**14)) | 1
    
    while n_collected < n_samples:
        if n <= B:
            n = int(rng.integers(10**10, 10**14)) | 1
            continue
        
        b_k = n % M
        if b_k % 3 != 0:
            counts[b_k] += 1
            n_collected += 1
            
            # Track base class and lift index
            b_prev = b_k % M_prev
            lift_idx = (b_k - b_prev) // M_prev  # ℓ ∈ {0,1,2}
            lift_given_b[b_prev][lift_idx] += 1
            
            # Track a-value for this transition
            next_n, a = syracuse_step(n)
            a_given_b[b_k][a] += 1
            
            n = next_n
        else:
            n, _ = syracuse_step(n)
    
    total = sum(counts.values())
    mu = {b: c / total for b, c in counts.items()}
    
    return mu, dict(a_given_b), dict(lift_given_b)


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


def compute_beta(mu_k, pi_k, k):
    """Compute β₁(b) and β₂(b) for each base class b ∈ G_{k-1}."""
    M = 3**k
    M_prev = 3**(k-1)
    
    omega = np.exp(2j * np.pi / 3)
    base_classes = [b for b in range(1, M_prev) if b % 3 != 0]
    
    beta_1 = {}
    beta_2 = {}
    
    for b in base_classes:
        # Three lifts of b
        lifts = [b + M_prev * ell for ell in range(3)]
        
        # δ(lift) = μ(lift) - π(lift)
        deltas = [mu_k.get(lift, 0) - pi_k.get(lift, 0) for lift in lifts]
        
        # β_r(b) = Σ_ℓ ω^{-rℓ} δ(b, ℓ)
        beta_1[b] = sum(omega**(-ell) * deltas[ell] for ell in range(3))
        beta_2[b] = sum(omega**(-2*ell) * deltas[ell] for ell in range(3))
    
    return beta_1, beta_2


def main():
    print("="*70)
    print("β TOP CONTRIBUTORS UNDER KILLED SAMPLING")
    print("="*70)
    
    k = 6
    n_samples = 500000
    B = 100
    
    print(f"\nParameters: k={k}, n_samples={n_samples}, B={B}")
    
    # Sample with details
    print("\n1. Sampling with a-value and lift tracking...")
    mu_6, a_given_b, lift_given_b = sample_killed_with_details(k, n_samples, B=B, seed=42)
    
    # Build π
    print("2. Building exact π₆...")
    states_6, pi_6 = build_exact_pi(k)
    
    # Compute β
    print("3. Computing β₁(b), β₂(b)...")
    beta_1, beta_2 = compute_beta(mu_6, pi_6, k)
    
    # Sort by magnitude
    beta_1_sorted = sorted(beta_1.items(), key=lambda x: abs(x[1]), reverse=True)
    beta_2_sorted = sorted(beta_2.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print("\n" + "="*70)
    print("TOP 10 β₁(b) CONTRIBUTORS")
    print("="*70)
    print(f"{'Rank':<6} {'b':<8} {'|β₁(b)|':<12} {'b%3':<6} {'b%8':<6}")
    print("-"*40)
    
    top_b1 = []
    for i, (b, val) in enumerate(beta_1_sorted[:10]):
        print(f"{i+1:<6} {b:<8} {abs(val):<12.6f} {b%3:<6} {b%8:<6}")
        top_b1.append(b)
    
    print("\n" + "="*70)
    print("TOP 10 β₂(b) CONTRIBUTORS")
    print("="*70)
    print(f"{'Rank':<6} {'b':<8} {'|β₂(b)|':<12} {'b%3':<6} {'b%8':<6}")
    print("-"*40)
    
    top_b2 = []
    for i, (b, val) in enumerate(beta_2_sorted[:10]):
        print(f"{i+1:<6} {b:<8} {abs(val):<12.6f} {b%3:<6} {b%8:<6}")
        top_b2.append(b)
    
    # Analyze P(a|b) for top contributors
    print("\n" + "="*70)
    print("P(a|b) FOR TOP β₁ CONTRIBUTORS (vs ideal geometric)")
    print("="*70)
    
    M = 3**k
    ideal_pa = {1: 0.5, 2: 0.25, 3: 0.125, 4: 0.0625}
    
    results = []
    for b in top_b1[:5]:
        # Get all k=6 residues that project to this b
        lifts = [b + 243 * ell for ell in range(3)]
        
        total_a = defaultdict(int)
        for lift in lifts:
            if lift in a_given_b:
                for a, cnt in a_given_b[lift].items():
                    total_a[a] += cnt
        
        total = sum(total_a.values())
        if total > 0:
            print(f"\nb = {b} (total visits: {total})")
            print(f"  {'a':<4} {'P(a|b)':<10} {'Ideal':<10} {'Deviation':<10}")
            print(f"  {'-'*34}")
            
            for a in [1, 2, 3, 4]:
                p_obs = total_a[a] / total if total > 0 else 0
                p_ideal = ideal_pa.get(a, 2**(-a))
                dev = p_obs - p_ideal
                print(f"  {a:<4} {p_obs:<10.4f} {p_ideal:<10.4f} {dev:+.4f}")
                
            results.append({
                'b': b,
                'total_visits': total,
                'P_a': {a: total_a[a]/total for a in range(1, 6) if total_a[a] > 0}
            })
    
    # Analyze lift choice distribution
    print("\n" + "="*70)
    print("LIFT CHOICE DISTRIBUTION FOR TOP β₁ CONTRIBUTORS")
    print("="*70)
    print("(Ideal: each lift ℓ ∈ {0,1,2} should be ~33.3%)")
    
    for b in top_b1[:5]:
        if b in lift_given_b:
            total = sum(lift_given_b[b].values())
            print(f"\nb = {b}")
            for ell in [0, 1, 2]:
                cnt = lift_given_b[b].get(ell, 0)
                pct = 100 * cnt / total if total > 0 else 0
                dev = pct - 33.33
                print(f"  ℓ={ell}: {pct:5.1f}% ({dev:+5.1f}%)")
    
    # Compare b=1 (old top) vs new tops
    print("\n" + "="*70)
    print("COMPARISON: b=1 (old champion) vs NEW top contributors")
    print("="*70)
    
    b1_rank_beta1 = next(i for i, (b, _) in enumerate(beta_1_sorted) if b == 1) + 1
    b1_rank_beta2 = next(i for i, (b, _) in enumerate(beta_2_sorted) if b == 1) + 1
    
    print(f"\nb=1 rank in |β₁|: #{b1_rank_beta1}")
    print(f"b=1 rank in |β₂|: #{b1_rank_beta2}")
    print(f"\nNew top-3 in β₁: {[b for b, _ in beta_1_sorted[:3]]}")
    print(f"New top-3 in β₂: {[b for b, _ in beta_2_sorted[:3]]}")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)
    
    # Save results
    save_data = {
        'k': k,
        'n_samples': n_samples,
        'B': B,
        'beta_1_top10': [{'b': b, 'magnitude': abs(v)} for b, v in beta_1_sorted[:10]],
        'beta_2_top10': [{'b': b, 'magnitude': abs(v)} for b, v in beta_2_sorted[:10]],
        'b1_rank_beta1': b1_rank_beta1,
        'b1_rank_beta2': b1_rank_beta2
    }
    
    with open('data/beta_top_contributors_killed.json', 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\nResults saved to data/beta_top_contributors_killed.json")


if __name__ == "__main__":
    main()
