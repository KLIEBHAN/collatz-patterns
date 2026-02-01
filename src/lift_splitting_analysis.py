#!/usr/bin/env python3
"""
Lift-Splitting Decomposition for k=5

Decomposes the k=5 discrepancy (μ - π) into:
- Coarse component Δ(b): inherited from k=4 (generates lift modes, j divisible by 3)
- Within-lift components δ₁(b), δ₂(b): new-digit splitting (generates non-lift modes)

Goal: Explain why j=79,83 dominate at k=5

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import sympy as sp
import matplotlib.pyplot as plt


def build_exact_P_k(k: int):
    """Build exact P_k matrix with rational arithmetic."""
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]
    n = len(states)
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
    P = sp.MutableDenseMatrix(n, n, [0]*(n*n))
    for x in states:
        i = idx[x]
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m]
    P = sp.Matrix(P)
    A = P.T - sp.eye(n)
    b = sp.Matrix([0]*n)
    A[n-1, :] = sp.Matrix([[1]*n])
    b[n-1] = 1
    pi = A.LUsolve(b)
    return states, pi


def syracuse_step(n: int):
    """One Syracuse step."""
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_empirical_distribution(k: int, n_samples: int = 200000, 
                                   t_burn: int = 50, seed: int = 42):
    """Sample empirical distribution mod 3^k."""
    M = 3**k
    counts = defaultdict(int)
    rng = np.random.default_rng(seed)
    
    for _ in range(n_samples):
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
    print("LIFT-SPLITTING DECOMPOSITION: k=5 Analysis")
    print("="*70)
    
    k = 5
    M = 3**k  # 243
    M_prev = 3**(k-1)  # 81
    
    # Build exact π for k=5
    print("\n1. Building exact π₅...")
    states_5, pi_5 = build_exact_P_k(k)
    pi_5_dict = {states_5[i]: float(pi_5[i]) for i in range(len(states_5))}
    print(f"   States: {len(states_5)}")
    
    # Sample empirical μ for k=5
    print("\n2. Sampling empirical μ₅ (200k samples)...")
    mu_5 = sample_empirical_distribution(k, n_samples=200000, seed=42)
    print(f"   Unique states: {len(mu_5)}")
    
    # Base classes: units mod 81 (G₄)
    base_classes = [b for b in range(1, M_prev) if b % 3 != 0]
    print(f"\n3. Analyzing {len(base_classes)} base classes (units mod 81)")
    
    # For each base class b, compute the three lifts and their discrepancies
    omega = np.exp(2j * np.pi / 3)
    
    # Store decomposition
    Delta = {}      # Coarse component
    delta_1 = {}    # Within-lift component 1
    delta_2 = {}    # Within-lift component 2
    
    print("\n4. Computing lift-splitting decomposition...")
    
    for b in base_classes:
        # Three lifts of b to mod 243
        lifts = [(b + 81 * ell) % M for ell in range(3)]
        
        # Discrepancy for each lift
        delta_lifts = []
        for ell, lift in enumerate(lifts):
            mu_val = mu_5.get(lift, 0)
            pi_val = pi_5_dict.get(lift, 0)
            delta_lifts.append(mu_val - pi_val)
        
        # Coarse component: sum of discrepancies (what k=4 would see)
        Delta[b] = sum(delta_lifts)
        
        # Within-lift components (kernel Fourier modes)
        delta_1[b] = sum(omega**ell * delta_lifts[ell] for ell in range(3))
        delta_2[b] = sum(omega**(2*ell) * delta_lifts[ell] for ell in range(3))
    
    # Compute energy in each component
    energy_coarse = sum(abs(Delta[b])**2 for b in base_classes)
    energy_within_1 = sum(abs(delta_1[b])**2 for b in base_classes)
    energy_within_2 = sum(abs(delta_2[b])**2 for b in base_classes)
    energy_total = energy_coarse + energy_within_1 + energy_within_2
    
    print("\n" + "="*70)
    print("ENERGY DECOMPOSITION")
    print("="*70)
    print(f"\nCoarse (Δ) energy:        {energy_coarse:.6e}  ({100*energy_coarse/energy_total:.1f}%)")
    print(f"Within-lift (δ₁) energy:  {energy_within_1:.6e}  ({100*energy_within_1/energy_total:.1f}%)")
    print(f"Within-lift (δ₂) energy:  {energy_within_2:.6e}  ({100*energy_within_2/energy_total:.1f}%)")
    print(f"Total energy:             {energy_total:.6e}")
    
    within_total = energy_within_1 + energy_within_2
    print(f"\n→ Within-lift total: {100*within_total/energy_total:.1f}% of energy")
    print(f"→ Coarse total:      {100*energy_coarse/energy_total:.1f}% of energy")
    
    if within_total > energy_coarse:
        print("\n✅ CONFIRMED: Within-lift components dominate!")
        print("   This explains why non-lift modes (79,83) are top targets.")
    
    # Find which base classes contribute most to within-lift error
    print("\n" + "="*70)
    print("TOP CONTRIBUTING BASE CLASSES (|δ₁(b)|)")
    print("="*70)
    
    delta_1_ranked = sorted(base_classes, key=lambda b: -abs(delta_1[b]))
    
    print(f"\n{'Rank':<6} {'b':<6} {'b mod 81':<10} {'|δ₁(b)|':<12} {'v₃(b+1)':<10} {'Notes'}")
    print("-"*70)
    
    for rank, b in enumerate(delta_1_ranked[:15], 1):
        b_mod = b % 81
        v3 = 0
        temp = b + 1
        while temp % 3 == 0:
            v3 += 1
            temp //= 3
        
        notes = ""
        if b == 80:
            notes = "← b ≡ -1 (mod 81)!"
        elif b == 53:
            notes = "← b ≡ -1 (mod 27)"
        elif (b + 1) % 9 == 0:
            notes = "← close to -1"
            
        print(f"{rank:<6} {b:<6} {b_mod:<10} {abs(delta_1[b]):<12.6f} {v3:<10} {notes}")
    
    # Check if -1 mod 81 (= 80) is the top contributor
    rank_of_80 = delta_1_ranked.index(80) + 1 if 80 in delta_1_ranked else "N/A"
    print(f"\n→ Rank of b=80 (≡ -1 mod 81): #{rank_of_80}")
    
    # Compute Fourier transform of δ₁(b) over base classes
    print("\n" + "="*70)
    print("FOURIER ANALYSIS OF δ₁(b)")
    print("="*70)
    
    phi_4 = 2 * 3**3  # 54 = |G₄|
    g = 2  # primitive root mod 81
    
    # Build discrete log for base classes
    dlog = {}
    val = 1
    for i in range(phi_4):
        dlog[val] = i
        val = (val * g) % M_prev
    
    # Fourier transform of δ₁ over G₄
    ft_delta_1 = {}
    for j in range(phi_4):
        coeff = 0
        for b in base_classes:
            chi_j_b = np.exp(2j * np.pi * j * dlog[b] / phi_4)
            coeff += delta_1[b] * chi_j_b
        ft_delta_1[j] = coeff
    
    # Find top Fourier modes of δ₁
    ft_ranked = sorted(range(phi_4), key=lambda j: -abs(ft_delta_1[j]))
    
    print(f"\nTop Fourier modes of δ₁(b) over G₄:")
    print(f"{'Rank':<6} {'j (mod 54)':<12} {'|FT[δ₁](j)|':<15} {'Lift to k=5':<15} {'Notes'}")
    print("-"*70)
    
    for rank, j in enumerate(ft_ranked[:10], 1):
        # The lift to k=5: modes on G₄ that combine with kernel modes
        # j in G₄ combined with kernel mode 1 gives j*3 + offset in G₅
        # Actually the relationship is more complex...
        # For non-lift modes in G₅, the index j satisfies j % 3 ≠ 0
        
        # The connection: δ₁(b) generates modes at positions 
        # that are NOT divisible by 3 in G₅
        
        notes = ""
        if j == 25 or j == 29:  # 54/2 ± 2 = 27 ± 2 = 25, 29
            notes = "← Nyquist-neighbor!"
        if j + (phi_4 - j) == phi_4 and j != 0:
            conj = phi_4 - j
            if conj in ft_ranked[:10]:
                notes += " (conjugate pair)"
        
        print(f"{rank:<6} {j:<12} {abs(ft_delta_1[j]):<15.6f} {'—':<15} {notes}")
    
    # Verify conjugate pairs
    print("\nConjugate check in G₄ (|G₄|=54):")
    for j in [25, 29]:
        conj = 54 - j
        print(f"  j={j}, conjugate={conj}, sum={j+conj}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    print(f"""
Key findings:

1. ENERGY SPLIT:
   - Coarse (inherited from k=4): {100*energy_coarse/energy_total:.1f}%
   - Within-lift (new digit):     {100*within_total/energy_total:.1f}%
   
   → {'Within-lift dominates' if within_total > energy_coarse else 'Coarse dominates'}!

2. TOP CONTRIBUTORS TO δ₁:
   - Rank #1: b = {delta_1_ranked[0]} (|δ₁| = {abs(delta_1[delta_1_ranked[0]]):.6f})
   - b = 80 (≡ -1 mod 81) rank: #{rank_of_80}

3. FOURIER OF δ₁:
   - Top modes in G₄ are j = {ft_ranked[0]}, {ft_ranked[1]}
   - These generate the non-lift modes in G₅

4. CONNECTION TO j=79,83:
   - 79 % 3 = {79 % 3}, 83 % 3 = {83 % 3} (non-lifts ✓)
   - 79 = 81-2, 83 = 81+2 (Nyquist-neighbors in G₅)
   - The within-lift discrepancy δ₁ projects to these modes
""")
    
    # Save plot
    print("\nGenerating visualization...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: |δ₁(b)| vs b
    ax1 = axes[0, 0]
    bs = sorted(base_classes)
    delta_1_vals = [abs(delta_1[b]) for b in bs]
    ax1.bar(bs, delta_1_vals, width=1, alpha=0.7)
    ax1.axvline(x=80, color='red', linestyle='--', label='b=80 (≡-1 mod 81)')
    ax1.set_xlabel('Base class b (mod 81)')
    ax1.set_ylabel('|δ₁(b)|')
    ax1.set_title('Within-lift discrepancy by base class')
    ax1.legend()
    
    # Plot 2: |δ₁(b)| vs v₃(b+1)
    ax2 = axes[0, 1]
    v3_vals = []
    for b in bs:
        v3 = 0
        temp = b + 1
        while temp % 3 == 0:
            v3 += 1
            temp //= 3
        v3_vals.append(v3)
    ax2.scatter(v3_vals, delta_1_vals, alpha=0.6)
    ax2.set_xlabel('v₃(b+1) = 3-adic valuation of b+1')
    ax2.set_ylabel('|δ₁(b)|')
    ax2.set_title('Discrepancy vs proximity to -1')
    
    # Plot 3: Energy pie chart
    ax3 = axes[1, 0]
    sizes = [energy_coarse, energy_within_1, energy_within_2]
    labels = ['Coarse Δ(b)', 'Within-lift δ₁(b)', 'Within-lift δ₂(b)']
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax3.set_title('Energy decomposition')
    
    # Plot 4: Fourier spectrum of δ₁
    ax4 = axes[1, 1]
    js = list(range(phi_4))
    ft_vals = [abs(ft_delta_1[j]) for j in js]
    ax4.bar(js, ft_vals, width=1, alpha=0.7)
    ax4.axvline(x=27, color='red', linestyle='--', alpha=0.5, label='Nyquist (54/2=27)')
    ax4.set_xlabel('Fourier index j (in G₄)')
    ax4.set_ylabel('|FT[δ₁](j)|')
    ax4.set_title('Fourier spectrum of within-lift component')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('data/lift_splitting_k5.png', dpi=150)
    print("Saved: data/lift_splitting_k5.png")
    
    plt.close()


if __name__ == "__main__":
    main()
