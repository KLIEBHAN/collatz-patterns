#!/usr/bin/env python3
"""compute_psi.py

Computes the Poisson correction ψ for the Collatz residue-corrected potential:

    V(n) = log(n) + ψ(n mod 3^k)

This makes the drift uniformly negative across all residue states (if successful).

Based on GPT 5.2 Pro analysis recommendations (docs/experiments/gpt-analysis-B-next.md).

Usage:
    python src/compute_psi.py --S 500000 --k 8 --t-burn 34 --t-max 50
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def v2(x: int) -> int:
    """2-adic valuation: largest k s.t. 2^k | x."""
    return (x & -x).bit_length() - 1


def odd_step(n: int) -> Tuple[int, int]:
    """One accelerated odd step. Returns (next_n, a)."""
    m = 3 * n + 1
    a = v2(m)
    return m >> a, a


def mod_pow3_units(k: int) -> Tuple[int, List[int], Dict[int, int]]:
    """Return modulus 3^k, list of units (not divisible by 3), and index map."""
    mod = 3**k
    units = [r for r in range(1, mod) if r % 3 != 0]
    idx = {r: i for i, r in enumerate(units)}
    return mod, units, idx


def sample_odd_uniform(N: int, rng: random.Random) -> int:
    x = rng.randrange(1, N + 1)
    return x if x % 2 == 1 else (x - 1 if x > 1 else 1)


@dataclass
class PsiResult:
    k: int
    t_burn: int
    t_max: int
    n_samples: int
    n_transitions: int
    psi: np.ndarray  # shape (n_states,)
    g_raw: np.ndarray  # raw drift per state
    g_corrected: np.ndarray  # corrected drift per state
    pi_occ: np.ndarray  # occupancy-based stationary dist
    pi_eig: np.ndarray  # eigenvector-based stationary dist
    lambda2: complex  # second eigenvalue
    global_drift: float
    worst_raw_drift: float
    worst_corrected_drift: float
    psi_range: float
    state_counts: np.ndarray


def compute_psi(
    N: int,
    S: int,
    k: int,
    t_burn: int,
    t_max: int,
    seed: int = 42,
    verbose: bool = True,
) -> PsiResult:
    """
    Main computation:
    1. Generate trajectories
    2. Build transition matrix P from t_burn to t_max
    3. Compute drift g(x) per state
    4. Solve Poisson equation for ψ
    5. Compute corrected drift
    """
    rng = random.Random(seed)
    mod, units, idx = mod_pow3_units(k)
    n_states = len(units)  # 2 * 3^(k-1)
    
    if verbose:
        print(f"Computing ψ for k={k}, {n_states} states")
        print(f"N={N:,}, S={S:,}, t_burn={t_burn}, t_max={t_max}")
    
    # Transition counts C(x,y) and drift sums
    C = defaultdict(lambda: defaultdict(int))  # C[x][y]
    drift_sum = defaultdict(float)  # sum of Δlog for state x
    drift_sum2 = defaultdict(float)  # sum of (Δlog)^2 for state x
    drift_count = defaultdict(int)  # count for state x
    
    # For occupancy-based pi
    occupancy = np.zeros(n_states, dtype=np.int64)
    
    start = time.time()
    n_transitions = 0
    
    for j in range(S):
        n = sample_odd_uniform(N, rng)
        
        # Walk t_max steps
        n_seq = [n]
        for i in range(t_max):
            nxt, a = odd_step(n_seq[-1])
            n_seq.append(nxt)
        
        # Use only t_burn <= t < t_max for transitions
        for t in range(t_burn, t_max):
            n_t = n_seq[t]
            n_t1 = n_seq[t + 1]
            
            r_t = n_t % mod
            r_t1 = n_t1 % mod
            
            # Skip if not in units (divisible by 3)
            if r_t % 3 == 0 or r_t1 % 3 == 0:
                continue
            
            x = idx[r_t]
            y = idx[r_t1]
            
            # Transition count
            C[x][y] += 1
            n_transitions += 1
            
            # Drift
            dlog = math.log(n_t1) - math.log(n_t)
            drift_sum[x] += dlog
            drift_sum2[x] += dlog * dlog
            drift_count[x] += 1
            
            # Occupancy (count state x)
            occupancy[x] += 1
        
        if verbose and (j + 1) % max(1, S // 10) == 0:
            elapsed = time.time() - start
            print(f"  {j+1:,}/{S:,} trajectories ({elapsed:.1f}s)")
    
    if verbose:
        print(f"Total transitions: {n_transitions:,}")
    
    # Build transition matrix P
    P = np.zeros((n_states, n_states))
    row_totals = np.zeros(n_states)
    
    for x in range(n_states):
        total = sum(C[x].values())
        row_totals[x] = total
        if total > 0:
            for y, cnt in C[x].items():
                P[x, y] = cnt / total
    
    # Compute drift per state g(x)
    g_raw = np.zeros(n_states)
    g_var = np.zeros(n_states)
    state_counts = np.zeros(n_states, dtype=np.int64)
    
    for x in range(n_states):
        n_x = drift_count[x]
        state_counts[x] = n_x
        if n_x > 0:
            g_raw[x] = drift_sum[x] / n_x
            g_var[x] = drift_sum2[x] / n_x - g_raw[x]**2
    
    # Stationary distribution: occupancy-based
    pi_occ = occupancy / occupancy.sum() if occupancy.sum() > 0 else np.ones(n_states) / n_states
    
    # Stationary distribution: eigenvector-based (left eigenvector of P for eigenvalue 1)
    # π P = π, or P^T π = π
    try:
        eigenvalues, eigenvectors = np.linalg.eig(P.T)
        # Find eigenvalue closest to 1
        idx_1 = np.argmin(np.abs(eigenvalues - 1.0))
        pi_eig = np.real(eigenvectors[:, idx_1])
        pi_eig = np.abs(pi_eig)  # ensure positive
        pi_eig = pi_eig / pi_eig.sum()
        
        # Second largest eigenvalue (for mixing)
        eigenvalues_sorted = sorted(eigenvalues, key=lambda x: -abs(x))
        lambda2 = eigenvalues_sorted[1] if len(eigenvalues_sorted) > 1 else 0
    except Exception as e:
        print(f"Warning: eigenvalue computation failed: {e}")
        pi_eig = pi_occ.copy()
        lambda2 = 0
    
    # Global drift (weighted by stationary dist)
    global_drift = np.sum(pi_occ * g_raw)
    
    if verbose:
        print(f"Global drift: {global_drift:.6f}")
        print(f"Max raw drift: {g_raw.max():.6f}")
        print(f"Min raw drift: {g_raw.min():.6f}")
        print(f"|λ₂| = {abs(lambda2):.6f}")
    
    # Solve Poisson equation: (I - P + 1 π^T) ψ = g - g_bar
    # where g_bar = Σ π(x) g(x)
    g_bar = global_drift
    rhs = g_raw - g_bar
    
    # Build (I - P + 1 π^T)
    I = np.eye(n_states)
    one_pi = np.outer(np.ones(n_states), pi_occ)
    A = I - P + one_pi
    
    try:
        psi = np.linalg.solve(A, rhs)
        # Center ψ so that π · ψ = 0
        psi = psi - np.sum(pi_occ * psi)
    except np.linalg.LinAlgError as e:
        print(f"Warning: solve failed, using least squares: {e}")
        psi, residuals, rank, s = np.linalg.lstsq(A, rhs, rcond=None)
        psi = psi - np.sum(pi_occ * psi)
    
    # Compute corrected drift: d_corr(x) = E[Z_t | X_t = x]
    # where Z_t = Δlog + ψ(X_{t+1}) - ψ(X_t)
    # E[Z | X=x] = g(x) + Σ_y P(x,y) ψ(y) - ψ(x)
    #            = g(x) + (Pψ)(x) - ψ(x)
    P_psi = P @ psi
    g_corrected = g_raw + P_psi - psi
    
    if verbose:
        print(f"Max corrected drift: {g_corrected.max():.6f}")
        print(f"Min corrected drift: {g_corrected.min():.6f}")
        print(f"ψ range: {psi.max() - psi.min():.4f}")
    
    return PsiResult(
        k=k,
        t_burn=t_burn,
        t_max=t_max,
        n_samples=S,
        n_transitions=n_transitions,
        psi=psi,
        g_raw=g_raw,
        g_corrected=g_corrected,
        pi_occ=pi_occ,
        pi_eig=pi_eig,
        lambda2=lambda2,
        global_drift=global_drift,
        worst_raw_drift=g_raw.max(),
        worst_corrected_drift=g_corrected.max(),
        psi_range=psi.max() - psi.min(),
        state_counts=state_counts,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=50_000_000)
    ap.add_argument("--S", type=int, default=500_000, help="number of trajectories")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--t-burn", type=int, default=34, help="burn-in time (skip t < t_burn)")
    ap.add_argument("--t-max", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--outdir", type=str, default="../data/psi_correction")
    args = ap.parse_args()
    
    result = compute_psi(
        N=args.N,
        S=args.S,
        k=args.k,
        t_burn=args.t_burn,
        t_max=args.t_max,
        seed=args.seed,
        verbose=True,
    )
    
    # Save results
    run_id = time.strftime("%Y%m%d_%H%M%SZ", time.gmtime()) + f"_k{args.k}_S{args.S}"
    outroot = Path(args.outdir).expanduser().resolve() / run_id
    outroot.mkdir(parents=True, exist_ok=True)
    
    # Summary
    summary = {
        "run_id": run_id,
        "k": result.k,
        "t_burn": result.t_burn,
        "t_max": result.t_max,
        "n_samples": result.n_samples,
        "n_transitions": result.n_transitions,
        "global_drift": float(result.global_drift),
        "worst_raw_drift": float(result.worst_raw_drift),
        "worst_corrected_drift": float(result.worst_corrected_drift),
        "psi_range": float(result.psi_range),
        "lambda2_abs": float(abs(result.lambda2)),
        "success": bool(result.worst_corrected_drift < 0),
    }
    (outroot / "summary.json").write_text(json.dumps(summary, indent=2))
    print("\n" + "="*50)
    print(json.dumps(summary, indent=2))
    
    # Save arrays
    np.save(outroot / "psi.npy", result.psi)
    np.save(outroot / "g_raw.npy", result.g_raw)
    np.save(outroot / "g_corrected.npy", result.g_corrected)
    np.save(outroot / "pi_occ.npy", result.pi_occ)
    np.save(outroot / "state_counts.npy", result.state_counts)
    
    # CSV for easy inspection
    with open(outroot / "drift_comparison.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state_idx", "n", "g_raw", "g_corrected", "psi", "pi_occ"])
        for i in range(len(result.psi)):
            w.writerow([i, result.state_counts[i], result.g_raw[i], 
                       result.g_corrected[i], result.psi[i], result.pi_occ[i]])
    
    print(f"\nResults saved to: {outroot}")
    
    # Key verdict
    print("\n" + "="*50)
    if result.worst_corrected_drift < 0:
        print("✅ SUCCESS: All corrected drifts are NEGATIVE!")
        print(f"   Worst corrected drift: {result.worst_corrected_drift:.6f}")
        print("   This is a candidate Lyapunov function!")
    else:
        print("⚠️  Some states still have positive corrected drift")
        print(f"   Worst: {result.worst_corrected_drift:.6f}")
        n_positive = np.sum(result.g_corrected > 0)
        mass_positive = np.sum(result.pi_occ[result.g_corrected > 0])
        print(f"   {n_positive} states with positive drift (π-mass: {mass_positive:.4f})")


if __name__ == "__main__":
    main()
