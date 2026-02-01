#!/usr/bin/env python3
"""
Fourier/Character comparison: Ideal P_k vs Empirical Syracuse

Computes Fourier coefficients (characters) on (ℤ/3^k ℤ)× and compares:
- Ideal: from exact P_k / π_k
- Empirical: from actual Syracuse trajectories

Goal: Identify "proof target" frequencies with largest deviation.

Author: clawdbot
Date: 2026-02-01
"""
import numpy as np
from collections import defaultdict
import sympy as sp
from typing import List, Dict, Tuple
import json

def build_exact_P_k(k: int):
    """Build exact P_k matrix."""
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
    
    return states, P, pi, M, idx


def primitive_root_mod_3k(k: int) -> int:
    """Find a primitive root modulo 3^k."""
    M = 3**k
    phi = 2 * 3**(k-1)
    
    # 2 is a primitive root mod 3^k for all k >= 1
    # Verify: ord(2) should equal phi(3^k)
    if pow(2, phi, M) == 1:
        # Check it's actually primitive (no smaller order)
        for d in [2, 3, phi//2, phi//3]:
            if d > 0 and d < phi and pow(2, d, M) == 1:
                break
        else:
            return 2
    
    # Fallback: search
    for g in range(2, M):
        if pow(g, phi, M) == 1:
            is_primitive = True
            for d in range(1, phi):
                if phi % d == 0 and pow(g, d, M) == 1:
                    is_primitive = False
                    break
            if is_primitive:
                return g
    raise ValueError(f"No primitive root found mod {M}")


def build_characters(k: int, states: List[int]) -> Dict[int, Dict[int, complex]]:
    """
    Build all multiplicative characters on (ℤ/3^k ℤ)×.
    
    Characters are indexed by j ∈ {0, 1, ..., φ(3^k)-1}.
    χ_j(x) = exp(2πi j * log_g(x) / φ(3^k))
    where g is a primitive root.
    """
    M = 3**k
    phi = 2 * 3**(k-1)
    g = primitive_root_mod_3k(k)
    
    # Build discrete log table
    dlog = {}
    val = 1
    for i in range(phi):
        dlog[val] = i
        val = (val * g) % M
    
    # Build characters
    characters = {}
    for j in range(phi):
        chi_j = {}
        for x in states:
            # χ_j(x) = exp(2πi j * dlog(x) / φ)
            chi_j[x] = np.exp(2j * np.pi * j * dlog[x] / phi)
        characters[j] = chi_j
    
    return characters, dlog


def ideal_fourier_coefficients(pi: sp.Matrix, states: List[int], 
                                characters: Dict[int, Dict[int, complex]]) -> Dict[int, complex]:
    """
    Compute ideal Fourier coefficients: π̂(χ_j) = Σ_x π(x) χ_j(x)
    """
    n = len(states)
    pi_float = {states[i]: float(pi[i]) for i in range(n)}
    
    coeffs = {}
    for j, chi_j in characters.items():
        coeff = sum(pi_float[x] * chi_j[x] for x in states)
        coeffs[j] = coeff
    
    return coeffs


def syracuse_step(n: int) -> Tuple[int, int]:
    """One Syracuse step: return (T(n), a(n)) where a = v_2(3n+1)."""
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_empirical_distribution(k: int, n_samples: int = 100000, 
                                   t_burn: int = 50) -> Dict[int, float]:
    """
    Sample empirical distribution of X_t mod 3^k from Syracuse trajectories.
    
    Uses regenerative sampling: start from random large numbers,
    run t_burn steps, then collect mod 3^k.
    """
    M = 3**k
    counts = defaultdict(int)
    
    rng = np.random.default_rng(42)
    
    for _ in range(n_samples):
        # Start from random large odd number
        n = int(rng.integers(10**8, 10**12)) | 1  # ensure odd
        
        # Burn-in
        for _ in range(t_burn):
            if n == 1:
                # Restart if we hit 1
                n = int(rng.integers(10**8, 10**12)) | 1
            n, _ = syracuse_step(n)
        
        # Record mod 3^k (only units)
        x = n % M
        if x % 3 != 0:
            counts[x] += 1
    
    # Normalize
    total = sum(counts.values())
    dist = {x: c / total for x, c in counts.items()}
    
    return dist


def empirical_fourier_coefficients(emp_dist: Dict[int, float], states: List[int],
                                    characters: Dict[int, Dict[int, complex]]) -> Dict[int, complex]:
    """
    Compute empirical Fourier coefficients: μ̂(χ_j) = Σ_x μ(x) χ_j(x)
    """
    coeffs = {}
    for j, chi_j in characters.items():
        coeff = sum(emp_dist.get(x, 0) * chi_j[x] for x in states)
        coeffs[j] = coeff
    
    return coeffs


def main():
    print("="*70)
    print("Fourier/Character Comparison: Ideal P_k vs Empirical Syracuse")
    print("="*70)
    
    results = []
    
    for k in [2, 3, 4]:
        print(f"\n{'='*70}")
        print(f"k = {k}, M = 3^{k} = {3**k}")
        print(f"{'='*70}")
        
        # Build exact model
        print("Building exact P_k model...")
        states, P, pi, M, idx = build_exact_P_k(k)
        n = len(states)
        print(f"  States: {n}")
        
        # Build characters
        print("Building multiplicative characters...")
        characters, dlog = build_characters(k, states)
        print(f"  Characters: {len(characters)}")
        
        # Ideal Fourier coefficients
        print("Computing ideal Fourier coefficients...")
        ideal_coeffs = ideal_fourier_coefficients(pi, states, characters)
        
        # Sample empirical distribution
        n_samples = 50000 if k <= 3 else 100000
        print(f"Sampling empirical distribution ({n_samples} samples)...")
        emp_dist = sample_empirical_distribution(k, n_samples=n_samples, t_burn=50)
        print(f"  Unique states visited: {len(emp_dist)}")
        
        # Empirical Fourier coefficients
        print("Computing empirical Fourier coefficients...")
        emp_coeffs = empirical_fourier_coefficients(emp_dist, states, characters)
        
        # Compare
        print("\nFourier Coefficient Comparison:")
        print(f"{'j':<6} {'|π̂(χⱼ)|':<12} {'|μ̂(χⱼ)|':<12} {'|Δ|':<12} {'Phase Δ':<12}")
        print("-" * 60)
        
        deviations = []
        for j in range(min(n, 20)):  # Show first 20
            ideal = ideal_coeffs[j]
            emp = emp_coeffs[j]
            
            mag_ideal = abs(ideal)
            mag_emp = abs(emp)
            mag_diff = abs(mag_ideal - mag_emp)
            
            phase_ideal = np.angle(ideal)
            phase_emp = np.angle(emp)
            phase_diff = abs(phase_ideal - phase_emp)
            if phase_diff > np.pi:
                phase_diff = 2*np.pi - phase_diff
            
            deviations.append({
                'j': j,
                'ideal_mag': mag_ideal,
                'emp_mag': mag_emp,
                'mag_diff': mag_diff,
                'phase_diff': phase_diff,
                'total_diff': abs(ideal - emp)
            })
            
            if j < 15:
                print(f"{j:<6} {mag_ideal:<12.6f} {mag_emp:<12.6f} {mag_diff:<12.6f} {phase_diff:<12.4f}")
        
        # Find top deviations
        all_deviations = []
        for j in range(n):
            ideal = ideal_coeffs[j]
            emp = emp_coeffs[j]
            all_deviations.append({
                'j': j,
                'total_diff': abs(ideal - emp),
                'ideal_mag': abs(ideal),
                'emp_mag': abs(emp)
            })
        
        all_deviations.sort(key=lambda x: -x['total_diff'])
        
        print(f"\n🎯 TOP 5 PROOF TARGETS (largest |π̂ - μ̂|):")
        print(f"{'Rank':<6} {'j':<6} {'|Δ|':<12} {'|π̂|':<12} {'|μ̂|':<12}")
        print("-" * 50)
        for rank, d in enumerate(all_deviations[:5], 1):
            print(f"{rank:<6} {d['j']:<6} {d['total_diff']:<12.6f} {d['ideal_mag']:<12.6f} {d['emp_mag']:<12.6f}")
        
        # TV distance approximation
        tv_approx = sum(abs(float(pi[i]) - emp_dist.get(states[i], 0)) for i in range(n)) / 2
        print(f"\nTotal Variation distance (approx): {tv_approx:.6f}")
        
        results.append({
            'k': k,
            'n_states': n,
            'n_samples': n_samples,
            'tv_distance': tv_approx,
            'top5_targets': all_deviations[:5]
        })
    
    # Save results
    print("\n" + "="*70)
    print("SUMMARY: Proof Targets by k")
    print("="*70)
    
    for r in results:
        print(f"\nk={r['k']}: TV={r['tv_distance']:.4f}")
        print(f"  Top target: j={r['top5_targets'][0]['j']} with |Δ|={r['top5_targets'][0]['total_diff']:.6f}")
    
    # Save to JSON
    with open('data/fourier_comparison.json', 'w') as f:
        json.dump(results, f, indent=2, default=float)
    print("\nResults saved to data/fourier_comparison.json")


if __name__ == "__main__":
    main()
