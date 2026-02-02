#!/usr/bin/env python3
"""
Verify the relationship between full Fourier Δ̂(j) and the β-spectrum FT[β_r](m).

The theory says: for j = 3m + r (with r ∈ {1,2}):
    Δ̂(j) should be related to FT[β_r](m)

Let's verify this explicitly.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import json


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


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_empirical_distribution(k: int, n_samples: int = 400000, 
                                   t_burn: int = 50, seed: int = 42):
    M = 3**k
    counts = defaultdict(int)
    rng = np.random.default_rng(seed)
    
    for i in range(n_samples):
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
    print("VERIFYING FOURIER <-> β-SPECTRUM RELATIONSHIP")
    print("="*70)
    
    k = 6
    M = 3**k           # 729
    M_prev = 3**(k-1)  # 243
    phi_k = 2 * 3**(k-1)    # 486
    phi_prev = 2 * 3**(k-2) # 162
    
    # Build distributions
    print("\n1. Building distributions...")
    states_6, pi_6 = build_exact_pi_k(k)
    mu_6 = sample_empirical_distribution(k, n_samples=400000, seed=42)
    
    # Discrepancy
    delta = {x: mu_6.get(x, 0) - pi_6.get(x, 0) for x in states_6}
    
    # Build discrete logs for both groups
    print("\n2. Building character tables...")
    
    # G_6: discrete log mod 729
    g = 2
    dlog_6 = {}
    val = 1
    for i in range(phi_k):
        dlog_6[val] = i
        val = (val * g) % M
    
    # G_5: discrete log mod 243
    dlog_5 = {}
    val = 1
    for i in range(phi_prev):
        dlog_5[val] = i
        val = (val * g) % M_prev
    
    # Base classes
    base_classes = [b for b in range(1, M_prev) if b % 3 != 0]
    
    # Compute β functions
    print("\n3. Computing β functions...")
    omega = np.exp(2j * np.pi / 3)
    
    beta = {1: {}, 2: {}}  # β₁(b) and β₂(b)
    
    for b in base_classes:
        lifts = [(b + M_prev * ell) % M for ell in range(3)]
        delta_lifts = [delta[lift] for lift in lifts]
        
        beta[1][b] = sum(omega**ell * delta_lifts[ell] for ell in range(3))
        beta[2][b] = sum(omega**(2*ell) * delta_lifts[ell] for ell in range(3))
    
    # Now compare: Δ̂(j) vs FT[β_r](m) for j = 3m + r
    print("\n4. Computing both representations and comparing...")
    
    # Test several j values, including j=85 and j=401
    test_js = [85, 401, 79, 83, 149, 337, 1, 2, 238, 250]
    
    print(f"\n{'j':<8} {'r=j%3':<8} {'m=(j-r)/3':<10} {'|Δ̂(j)|':<15} {'|FT[β_r](m)|':<15} {'Ratio':<10}")
    print("-"*70)
    
    for j in test_js:
        # Full Fourier: Δ̂(j) = Σ_x δ(x) χ_j(x)
        chi_j = {x: np.exp(2j * np.pi * j * dlog_6[x] / phi_k) for x in states_6}
        delta_hat_j = sum(delta[x] * chi_j[x] for x in states_6)
        
        # β-spectrum
        r = j % 3
        if r == 0:
            # Coarse mode - different relationship
            continue
            
        m = (j - r) // 3
        
        # FT[β_r](m) = Σ_b β_r(b) χ_m(b)
        ft_beta_r_m = sum(beta[r][b] * np.exp(2j * np.pi * m * dlog_5[b] / phi_prev) 
                         for b in base_classes)
        
        ratio = abs(delta_hat_j) / abs(ft_beta_r_m) if abs(ft_beta_r_m) > 1e-10 else float('inf')
        
        print(f"{j:<8} {r:<8} {m:<10} {abs(delta_hat_j):<15.8f} {abs(ft_beta_r_m):<15.8f} {ratio:<10.4f}")
    
    # Also check what happens when we use the "wrong" mapping
    print("\n" + "="*70)
    print("CHECKING TOP MODES FROM k6_fourier_results")
    print("="*70)
    
    # Load the k6 results
    with open('data/k6_fourier_results.json') as f:
        k6_results = json.load(f)
    
    top5 = k6_results['top20'][:5]
    
    print(f"\n{'Rank':<6} {'j':<8} {'r':<6} {'m':<8} {'|Δ̂(j)|':<15} {'|FT[β_r](m)|':<15} {'Ratio':<10}")
    print("-"*80)
    
    for i, item in enumerate(top5, 1):
        j = item['j']
        r = j % 3
        
        if r == 0:
            print(f"{i:<6} {j:<8} {r:<6} {'(coarse)':<8} {item['total_diff']:<15.6f} {'N/A':<15} {'N/A':<10}")
            continue
        
        m = (j - r) // 3
        
        # Recompute to verify
        chi_j = {x: np.exp(2j * np.pi * j * dlog_6[x] / phi_k) for x in states_6}
        delta_hat_j = sum(delta[x] * chi_j[x] for x in states_6)
        
        ft_beta_r_m = sum(beta[r][b] * np.exp(2j * np.pi * m * dlog_5[b] / phi_prev) 
                         for b in base_classes)
        
        ratio = abs(delta_hat_j) / abs(ft_beta_r_m) if abs(ft_beta_r_m) > 1e-10 else float('inf')
        
        print(f"{i:<6} {j:<8} {r:<6} {m:<8} {abs(delta_hat_j):<15.8f} {abs(ft_beta_r_m):<15.8f} {ratio:<10.4f}")
    
    # Check the normalization
    print("\n" + "="*70)
    print("NORMALIZATION CHECK")
    print("="*70)
    
    print(f"\nSum of |δ(x)|: {sum(abs(delta[x]) for x in states_6):.6f}")
    print(f"Sum of |β₁(b)|: {sum(abs(beta[1][b]) for b in base_classes):.6f}")
    print(f"Sum of |β₂(b)|: {sum(abs(beta[2][b]) for b in base_classes):.6f}")
    
    # Parseval check
    print("\n" + "="*70)
    print("UNDERSTANDING THE RELATIONSHIP")
    print("="*70)
    
    # The key insight: χ_j on G_6 restricted to a lift b + M_prev·ℓ
    # χ_j(b + M_prev·ℓ) = χ_j(b) · χ_j(M_prev)^ℓ
    
    # Since g=2 is primitive root:
    # χ_j(M_prev) = e^{2πi j·dlog(M_prev)/φ_k}
    
    # Check what dlog(M_prev) is
    print(f"\nM_prev = 243 = 3^5")
    print(f"dlog_6(243) is not defined (243 ≡ 0 mod 3)")
    
    # Actually 243 is not coprime to 729, so it's not in the group!
    # The lifts are b, b+243, b+486 (mod 729)
    # b+243 and b+486 might not be in G_6...
    
    # Wait, let me check: for b coprime to 3, is b+243 coprime to 3?
    # b+243 ≡ b (mod 3), so if b ≢ 0 (mod 3), then b+243 ≢ 0 (mod 3) ✓
    
    # So the lifts are all in G_6. But 243 itself is not.
    # The character on the kernel of the projection is:
    # χ_j restricted to {b, b+243, b+486} depends on j mod something...
    
    # Let me think more carefully about the lift structure
    print("\nThe lift structure:")
    print(f"  For b ∈ G_5 (coprime to 3, mod 243):")
    print(f"  Lifts to G_6: b, b+243, b+486 (mod 729)")
    
    # The kernel of the projection G_6 → G_5 consists of elements
    # x such that x ≡ 1 (mod 243)
    # These are: 1, 1+243=244, 1+486=487≡487-729=-242≡487 (mod 729)
    # Wait, 487 mod 729 = 487
    # Let's check if 244 is in G_6: 244 = 4·61, not divisible by 3 ✓
    # 487 = 487, not divisible by 3 ✓
    
    print(f"\n  Kernel of G_6 → G_5: {{1, 244, 487}}")
    for x in [1, 244, 487]:
        print(f"    {x} mod 243 = {x % 243}")
    
    # The character χ_j on the kernel is determined by j mod (|G_6|/|G_5|) = j mod 3
    # More precisely, χ_j(244) = e^{2πi j·dlog(244)/486}
    
    print(f"\n  dlog_6(244) = {dlog_6[244]}")
    print(f"  dlog_6(487) = {dlog_6[487]}")
    
    # The kernel is generated by one of these
    # χ_j(244) = e^{2πi j·{dlog_6[244]}/486}
    # For j=1: χ_1(244) = e^{2πi·{dlog_6[244]}/486}
    
    d244 = dlog_6[244]
    for j in [0, 1, 2, 3, 85, 401]:
        chi_j_244 = np.exp(2j * np.pi * j * d244 / phi_k)
        print(f"  χ_{j}(244) = e^{{2πi·{j}·{d244}/486}} = {chi_j_244:.4f}")
    
    print("\n" + "="*70)
    print("KEY INSIGHT")
    print("="*70)
    
    print("""
The relationship Δ̂(j) = FT[β_r](m) for j = 3m + r should hold, but 
there might be a normalization factor or phase factor involved.

The ratio between |Δ̂(j)| and |FT[β_r](m)| should be constant for all j
with the same r value. Let's check this:
""")
    
    # Compute ratios for all j with r=1
    ratios_r1 = []
    for m in range(phi_prev):
        j = 3*m + 1
        chi_j = {x: np.exp(2j * np.pi * j * dlog_6[x] / phi_k) for x in states_6}
        delta_hat_j = sum(delta[x] * chi_j[x] for x in states_6)
        
        ft_beta_1_m = sum(beta[1][b] * np.exp(2j * np.pi * m * dlog_5[b] / phi_prev) 
                         for b in base_classes)
        
        if abs(ft_beta_1_m) > 1e-10:
            ratios_r1.append(abs(delta_hat_j) / abs(ft_beta_1_m))
    
    print(f"Ratios |Δ̂(j)|/|FT[β₁](m)| for r=1:")
    print(f"  Mean: {np.mean(ratios_r1):.6f}")
    print(f"  Std:  {np.std(ratios_r1):.6f}")
    print(f"  Min:  {np.min(ratios_r1):.6f}")
    print(f"  Max:  {np.max(ratios_r1):.6f}")
    
    if np.std(ratios_r1) < 0.01 * np.mean(ratios_r1):
        print("\n✅ Ratios are nearly constant! The relationship holds with a constant factor.")
    else:
        print("\n❌ Ratios vary significantly. The simple relationship doesn't hold.")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    main()
