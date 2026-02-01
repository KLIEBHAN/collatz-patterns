#!/usr/bin/env python3
"""
Exact P_k model for Syracuse mod 3^k
Based on ChatGPT analysis 2026-02-01
"""
import sympy as sp
from fractions import Fraction
import numpy as np

def build_exact_P_k(k: int):
    """
    Exact kernel P_k on units mod 3^k for the idealized random Syracuse model:
        X_{t+1} = (3 X_t + 1) * 2^{-A}  (mod 3^k),
        P(A=m) = 2^{-m}, m>=1.

    Collapsing uses r = ord_{3^k}(2) = phi(3^k) = 2*3^(k-1).
    """
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]   # units mod 3^k
    n = len(states)
    
    r = 2 * 3**(k-1)  # for mod 3^k, ord(2)=phi(3^k)
    assert r == n, f"Expected r={r} == n={n}"
    
    D = 2**r - 1  # common denominator
    w = [None] + [sp.Rational(2**(r-m), D) for m in range(1, r+1)]
    
    # Precompute 2^{-m} mod M
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
    
    # Verify row sums = 1
    for i in range(n):
        row_sum = sum(P[i, j] for j in range(n))
        assert row_sum == 1, f"Row {i} sum = {row_sum}"
    
    # Stationary distribution pi: uniform for this model
    pi = sp.Matrix([sp.Rational(1, n)] * n)
    
    return states, P, pi, M, r


def compute_drift(states, P, k):
    """
    Compute raw drift g(x) = E[log(T(x)/x)] for each state.
    In the random model: g(x) = sum_m w_m * log((3x+1) * 2^{-m} / x)
                              = log(3 + 1/x) + sum_m w_m * (-m * log 2)
                              = log(3 + 1/x) - E[A] * log 2
    where E[A] = sum_m m * 2^{-m} = 2 for geometric.
    
    But with collapsed weights it's different. Let's compute numerically.
    """
    M = 3**k
    r = 2 * 3**(k-1)
    D = 2**r - 1
    
    # Weights
    w = [0] + [2**(r-m) / D for m in range(1, r+1)]
    
    # 2^{-m} mod M
    inv2 = pow(2, -1, M)
    inv2pow = [0]*(r+1)
    cur = inv2 % M
    for m in range(1, r+1):
        inv2pow[m] = cur
        cur = (cur * inv2) % M
    
    g = {}
    for x in states:
        c = (3*x + 1) % M
        drift = 0.0
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            # In the mod-reduced world, we track log of "effective" ratio
            # Actually for the idealized model, drift is constant!
            # g = E[log(3/2^A)] = log(3) - E[A]*log(2) = log(3) - 2*log(2) = log(3/4)
            drift += w[m] * (-m * np.log(2))
        drift += np.log(3)  # from the 3x+1
        g[x] = drift
    
    return g


def verify_rank1(P, pi, tol=1e-10):
    """Verify P is a rank-1 matrix (all rows equal to pi^T)."""
    n = P.rows
    P_float = np.array(P.tolist(), dtype=float)
    pi_float = np.array(pi.tolist(), dtype=float).flatten()
    
    for i in range(n):
        row = P_float[i, :]
        diff = np.max(np.abs(row - pi_float))
        if diff > tol:
            return False, f"Row {i} differs from pi by {diff}"
    return True, "P is rank-1 projection!"


def main():
    print("=" * 60)
    print("Exact P_k Model for Syracuse mod 3^k")
    print("=" * 60)
    
    for k in [2, 3, 4]:
        print(f"\n{'='*60}")
        print(f"k = {k}, M = 3^{k} = {3**k}")
        print(f"{'='*60}")
        
        states, P, pi, M, r = build_exact_P_k(k)
        n = len(states)
        
        print(f"States: {n} (= φ(3^{k}) = 2·3^{k-1})")
        print(f"Order r = ord_M(2) = {r}")
        
        # Check if P is rank-1
        is_rank1, msg = verify_rank1(P, pi)
        print(f"Rank-1 check: {msg}")
        
        # Compute eigenvalues (for small k)
        if k <= 3:
            print("\nComputing eigenvalues (exact)...")
            eigenvalues = P.eigenvals()
            print(f"Eigenvalues: {eigenvalues}")
            
            # Count non-zero eigenvalues
            nonzero = sum(1 for ev in eigenvalues if ev != 0)
            print(f"Non-zero eigenvalues: {nonzero}")
        
        # Compute drift
        g = compute_drift(states, P, k)
        g_values = list(g.values())
        g_mean = np.mean(g_values)
        g_std = np.std(g_values)
        
        print(f"\nDrift statistics:")
        print(f"  E[g] = {g_mean:.6f}")
        print(f"  std(g) = {g_std:.6f}")
        print(f"  log(3/4) = {np.log(3/4):.6f} (theoretical)")
        
        # Show first few states
        print(f"\nFirst 5 states and their drift:")
        for x in states[:5]:
            print(f"  g({x}) = {g[x]:.6f}")


if __name__ == "__main__":
    main()
