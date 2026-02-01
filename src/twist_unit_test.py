#!/usr/bin/env python3
"""
Twist Formula Unit Test (GPT's Diagnostic)

GPT's exact identity in exponent coordinates:
Let r = |G_k| = 3n. In cyclic coordinate t ∈ {0,...,3n-1} where x = 2^t:

Split t = u + nℓ, then:
    β_r(u) := δ(u) + ω^(-r) δ(u+n) + ω^(-2r) δ(u+2n)

Exact identity:
    δ̂(3m+r) = Σ_{u=0}^{n-1} β_r(u) exp(-2πi(3m+r)u/(3n))

If this fails → indexing/normalization bug.
If this holds but residue-lift β fails → additive vs multiplicative misalignment.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_killed_distribution(k: int, n_samples: int, B: int = 100, seed: int = 42):
    """Sample with killed process."""
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


def main():
    print("="*70)
    print("TWIST FORMULA UNIT TEST (EXPONENT COORDINATES)")
    print("="*70)
    
    k = 5
    M = 3**k  # 243
    phi_k = 2 * 3**(k-1)  # 162 = |G_k|
    n = phi_k // 3  # 54 = |G_{k-1}|
    
    print(f"\nParameters:")
    print(f"  k = {k}")
    print(f"  M = 3^k = {M}")
    print(f"  |G_k| = φ(3^k) = {phi_k}")
    print(f"  n = |G_{k-1}| = {n}")
    
    # Build discrete log table: x = 2^t mod M
    g = 2
    exp_to_x = {}  # t -> x
    x_to_exp = {}  # x -> t
    val = 1
    for t in range(phi_k):
        exp_to_x[t] = val
        x_to_exp[val] = t
        val = (val * g) % M
    
    print(f"\n1. Built discrete log table (generator g=2)")
    
    # Sample μ and build π
    print(f"\n2. Sampling μ (killed) and building π...")
    states, pi_dict = build_exact_pi(k)
    mu_dict = sample_killed_distribution(k, n_samples=400000, B=100, seed=42)
    
    # Build δ in exponent coordinates: δ(t) = μ(2^t) - π(2^t)
    delta_exp = np.zeros(phi_k)
    for t in range(phi_k):
        x = exp_to_x[t]
        delta_exp[t] = mu_dict.get(x, 0) - pi_dict.get(x, 0)
    
    print(f"   ||δ||₂ = {np.linalg.norm(delta_exp):.6f}")
    
    # Compute β_r(u) in exponent coordinates
    # β_r(u) = δ(u) + ω^(-r) δ(u+n) + ω^(-2r) δ(u+2n)
    print(f"\n3. Computing β_r(u) in exponent coordinates...")
    
    omega = np.exp(2j * np.pi / 3)
    beta = {1: np.zeros(n, dtype=complex), 2: np.zeros(n, dtype=complex)}
    
    for u in range(n):
        for r in [1, 2]:
            beta[r][u] = (delta_exp[u] + 
                         omega**(-r) * delta_exp[u + n] + 
                         omega**(-2*r) * delta_exp[u + 2*n])
    
    print(f"   ||β₁||₂ = {np.linalg.norm(beta[1]):.6f}")
    print(f"   ||β₂||₂ = {np.linalg.norm(beta[2]):.6f}")
    
    # Compute δ̂(j) directly via DFT
    print(f"\n4. Computing δ̂(j) directly...")
    delta_hat_direct = np.fft.fft(delta_exp)
    
    # Compute δ̂(3m+r) via the formula
    # δ̂(3m+r) = Σ_{u=0}^{n-1} β_r(u) exp(-2πi(3m+r)u/(3n))
    print(f"\n5. Computing δ̂(3m+r) via β formula...")
    delta_hat_formula = {}
    
    for j in range(phi_k):
        r = j % 3
        if r == 0:
            continue  # Lift modes, different formula
        m = j // 3
        
        # Sum over u
        coeff = 0
        for u in range(n):
            phase = np.exp(-2j * np.pi * j * u / phi_k)
            coeff += beta[r][u] * phase
        
        delta_hat_formula[j] = coeff
    
    # Compare!
    print(f"\n" + "="*70)
    print("COMPARISON: Direct FFT vs Formula")
    print("="*70)
    
    print(f"\n{'j':<8} {'r':<4} {'|Direct|':<14} {'|Formula|':<14} {'Ratio':<10} {'Phase Δ':<10}")
    print("-"*60)
    
    # Test a few specific modes
    test_js = [1, 2, 4, 5, 79, 80, 83, 82, 85, 86]
    
    errors = []
    for j in test_js:
        r = j % 3
        if r == 0:
            continue
        
        direct = delta_hat_direct[j]
        formula = delta_hat_formula[j]
        
        mag_direct = abs(direct)
        mag_formula = abs(formula)
        ratio = mag_direct / mag_formula if mag_formula > 1e-12 else float('inf')
        
        # Phase difference
        if mag_direct > 1e-12 and mag_formula > 1e-12:
            phase_diff = np.angle(direct / formula) * 180 / np.pi
        else:
            phase_diff = 0
        
        errors.append(abs(direct - formula))
        
        print(f"{j:<8} {r:<4} {mag_direct:<14.8f} {mag_formula:<14.8f} {ratio:<10.4f} {phase_diff:+.1f}°")
    
    # Overall error analysis
    print(f"\n" + "="*70)
    print("OVERALL ERROR ANALYSIS (NEW-DIGIT modes only)")
    print("="*70)
    
    all_errors = []
    all_ratios = []
    
    for j in range(phi_k):
        r = j % 3
        if r == 0:
            continue
        
        direct = delta_hat_direct[j]
        formula = delta_hat_formula[j]
        
        err = abs(direct - formula)
        all_errors.append(err)
        
        if abs(formula) > 1e-12:
            all_ratios.append(abs(direct) / abs(formula))
    
    print(f"\nComplex error |δ̂_direct - δ̂_formula|:")
    print(f"  Mean: {np.mean(all_errors):.2e}")
    print(f"  Max:  {np.max(all_errors):.2e}")
    print(f"  RMS:  {np.sqrt(np.mean(np.array(all_errors)**2)):.2e}")
    
    print(f"\nMagnitude ratios |δ̂_direct| / |δ̂_formula|:")
    print(f"  Mean: {np.mean(all_ratios):.4f}")
    print(f"  Std:  {np.std(all_ratios):.4f}")
    print(f"  Min:  {np.min(all_ratios):.4f}")
    print(f"  Max:  {np.max(all_ratios):.4f}")
    
    # Verdict
    print(f"\n" + "="*70)
    if np.mean(all_errors) < 1e-10:
        print("✅ UNIT TEST PASSED!")
        print("   The exponent-coordinate formula is EXACT.")
        print("   → Bug must be in residue-lift implementation (additive vs multiplicative)")
    elif np.std(all_ratios) / np.mean(all_ratios) < 0.01:
        print("⚠️ Formula correct up to normalization factor")
        print(f"   Constant ratio: {np.mean(all_ratios):.4f}")
    else:
        print("❌ UNIT TEST FAILED")
        print("   Check indexing/normalization in exponent coordinates")
    print("="*70)


if __name__ == "__main__":
    main()
