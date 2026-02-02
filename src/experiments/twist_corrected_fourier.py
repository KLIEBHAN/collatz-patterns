#!/usr/bin/env python3
"""
Twist-Corrected β→Fourier Relationship

GPT explained: The simple relationship Δ̂(3m+r) ∝ FT[β_r](m) is wrong because
there's a missing twist factor from the non-splitting cyclic extension.

The correct formula involves a convolution:
    Δ̂(3m+r) = (1/3) Σ_q β̂_r(q) τ̂_r(m-q)

where τ_r(u) = exp(-2πi r u / (3n)) is the twist factor.

This script tests the corrected formula with killed sampling data.

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
    print("TWIST-CORRECTED β→FOURIER RELATIONSHIP")
    print("="*70)
    
    k = 5
    M = 3**k           # 243
    M_prev = 3**(k-1)  # 81
    phi_k = 2 * 3**(k-1)    # 162
    phi_prev = 2 * 3**(k-2) # 54
    
    print(f"\nParameters:")
    print(f"  k = {k}")
    print(f"  M = {M}, M_prev = {M_prev}")
    print(f"  |G_k| = {phi_k}, |G_{k-1}| = {phi_prev}")
    
    # Build π and sample μ (killed)
    print(f"\n1. Building π and sampling μ (killed)...")
    states, pi_dict = build_exact_pi_k(k)
    mu_dict = sample_killed_distribution(k, n_samples=400000, B=100, seed=42)
    
    # Compute discrepancy δ(x) = μ(x) - π(x)
    delta = {x: mu_dict.get(x, 0) - pi_dict.get(x, 0) for x in states}
    
    # Build discrete log for G_k
    g = 2
    dlog_k = {}
    val = 1
    for i in range(phi_k):
        dlog_k[val] = i
        val = (val * g) % M
    
    # Build discrete log for G_{k-1}
    dlog_prev = {}
    val = 1
    for i in range(phi_prev):
        dlog_prev[val] = i
        val = (val * g) % M_prev
    
    # Base classes
    base_classes = [b for b in range(1, M_prev) if b % 3 != 0]
    
    # Compute β_r(u) for r=1,2
    print("\n2. Computing β_r(u) decomposition...")
    omega = np.exp(2j * np.pi / 3)
    
    beta = {1: {}, 2: {}}
    for u in base_classes:
        lifts = [(u + M_prev * ell) % M for ell in range(3)]
        delta_lifts = [delta.get(lift, 0) for lift in lifts]
        
        # β_r(u) = Σ_ℓ ω^{-rℓ} δ(u,ℓ)
        beta[1][u] = sum(omega**(-ell) * delta_lifts[ell] for ell in range(3))
        beta[2][u] = sum(omega**(-2*ell) * delta_lifts[ell] for ell in range(3))
    
    # Compute Fourier transform of β_r over base group
    print("\n3. Computing FT[β_r](q) over G_{k-1}...")
    ft_beta = {1: {}, 2: {}}
    for r in [1, 2]:
        for q in range(phi_prev):
            coeff = 0
            for u in base_classes:
                chi_q_u = np.exp(2j * np.pi * q * dlog_prev[u] / phi_prev)
                coeff += beta[r][u] * chi_q_u
            ft_beta[r][q] = coeff
    
    # Compute the twist factor τ_r(u) = exp(-2πi r u / (3n))
    # where n = |G_{k-1}| = phi_prev
    print("\n4. Computing twist factor FT[τ_r](m)...")
    
    # τ_r(u) = exp(-2πi r dlog(u) / (3 * phi_prev))
    # We need FT[τ_r] which is a delta-like function shifted by r/3
    
    ft_tau = {1: {}, 2: {}}
    for r in [1, 2]:
        for m in range(phi_prev):
            # τ_r(u) = exp(-2πi r dlog(u) / (3 * phi_prev))
            # FT[τ_r](m) = Σ_u τ_r(u) χ_m(u)
            #            = Σ_u exp(-2πi r dlog(u)/(3n)) exp(2πi m dlog(u)/n)
            #            = Σ_u exp(2πi (m - r/3) dlog(u) / n)
            # This is nonzero only when m ≈ r/3 (mod n)
            coeff = 0
            for u in base_classes:
                tau_r_u = np.exp(-2j * np.pi * r * dlog_prev[u] / (3 * phi_prev))
                chi_m_u = np.exp(2j * np.pi * m * dlog_prev[u] / phi_prev)
                coeff += tau_r_u * chi_m_u
            ft_tau[r][m] = coeff / len(base_classes)  # Normalize
    
    # Compute convolution: Δ̂(3m+r) ≈ (1/3) Σ_q β̂_r(q) τ̂_r(m-q)
    print("\n5. Computing convolution Δ̂_predicted(3m+r)...")
    
    delta_hat_predicted = {}
    for r in [1, 2]:
        for m in range(phi_prev):
            j = 3 * m + r
            # Convolution
            conv = 0
            for q in range(phi_prev):
                m_minus_q = (m - q) % phi_prev
                conv += ft_beta[r][q] * ft_tau[r][m_minus_q]
            delta_hat_predicted[j] = conv / 3
    
    # Compute actual Δ̂(j) directly
    print("\n6. Computing actual Δ̂(j) directly...")
    delta_hat_actual = {}
    for j in range(phi_k):
        coeff = 0
        for x in states:
            chi_j_x = np.exp(2j * np.pi * j * dlog_k[x] / phi_k)
            coeff += delta.get(x, 0) * chi_j_x
        delta_hat_actual[j] = coeff
    
    # Compare
    print("\n" + "="*70)
    print("COMPARISON: Actual vs Twist-Corrected Prediction")
    print("="*70)
    
    print(f"\n{'j':<8} {'r':<6} {'m':<8} {'|Δ̂ actual|':<15} {'|Δ̂ predicted|':<15} {'Ratio':<10}")
    print("-"*70)
    
    # Test for top modes
    test_js = [79, 83, 85, 77, 1, 2, 43, 119]  # Mix of modes
    
    for j in test_js:
        r = j % 3
        if r == 0:
            continue  # Lift modes, different formula
        m = (j - r) // 3
        
        actual = abs(delta_hat_actual[j])
        predicted = abs(delta_hat_predicted[j])
        ratio = actual / predicted if predicted > 1e-10 else float('inf')
        
        print(f"{j:<8} {r:<6} {m:<8} {actual:<15.8f} {predicted:<15.8f} {ratio:<10.4f}")
    
    # Check if ratios are now more constant
    print("\n" + "="*70)
    print("RATIO ANALYSIS (NEW-DIGIT modes only)")
    print("="*70)
    
    ratios = []
    for j in range(phi_k):
        r = j % 3
        if r == 0:
            continue
        
        actual = abs(delta_hat_actual[j])
        predicted = abs(delta_hat_predicted[j])
        if predicted > 1e-10 and actual > 1e-10:
            ratios.append(actual / predicted)
    
    print(f"\nRatios |Δ̂_actual| / |Δ̂_predicted|:")
    print(f"  Mean: {np.mean(ratios):.4f}")
    print(f"  Std:  {np.std(ratios):.4f}")
    print(f"  CV:   {np.std(ratios)/np.mean(ratios):.4f} (coefficient of variation)")
    print(f"  Min:  {np.min(ratios):.4f}")
    print(f"  Max:  {np.max(ratios):.4f}")
    
    # Compare with old (uncorrected) approach
    print("\n" + "="*70)
    print("COMPARISON: Old (uncorrected) vs New (twist-corrected)")
    print("="*70)
    
    # Old approach: Δ̂(3m+r) ∝ FT[β_r](m) directly
    ratios_old = []
    for j in range(phi_k):
        r = j % 3
        if r == 0:
            continue
        m = (j - r) // 3
        
        actual = abs(delta_hat_actual[j])
        old_pred = abs(ft_beta[r][m])
        if old_pred > 1e-10 and actual > 1e-10:
            ratios_old.append(actual / old_pred)
    
    print(f"\nOLD (uncorrected) ratios:")
    print(f"  Mean: {np.mean(ratios_old):.4f}")
    print(f"  Std:  {np.std(ratios_old):.4f}")
    print(f"  CV:   {np.std(ratios_old)/np.mean(ratios_old):.4f}")
    
    print(f"\nNEW (twist-corrected) ratios:")
    print(f"  Mean: {np.mean(ratios):.4f}")
    print(f"  Std:  {np.std(ratios):.4f}")
    print(f"  CV:   {np.std(ratios)/np.mean(ratios):.4f}")
    
    improvement = (np.std(ratios_old)/np.mean(ratios_old)) / (np.std(ratios)/np.mean(ratios))
    print(f"\n→ CV improvement: {improvement:.2f}× (lower is better)")
    
    if np.std(ratios)/np.mean(ratios) < np.std(ratios_old)/np.mean(ratios_old):
        print("✅ Twist correction IMPROVES the relationship!")
    else:
        print("⚠️ Twist correction did not improve (may need refinement)")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
