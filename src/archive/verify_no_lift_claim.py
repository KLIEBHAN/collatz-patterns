#!/usr/bin/env python3
"""
Verify the "No Lift" Claim

GPT's suggestion: Compute TV(ρ#μ₆, π₅) directly.
If it's tiny, the disappearance of lifts from top-20 is explained.

Also compute energy split at k=6 killed: coarse vs within-lift.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict


def syracuse_step(n: int):
    """One Syracuse step, returns (next_n, a)."""
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
    b = np.zeros(n_states)
    b[-1] = 1
    pi = np.linalg.solve(A, b)
    pi = pi / pi.sum()
    
    return states, {states[i]: pi[i] for i in range(n_states)}


def project_to_lower_k(mu_dict, k_from, k_to):
    """Project measure from G_k to G_{k-1} via ρ: x ↦ x mod 3^{k-1}."""
    M_to = 3**k_to
    projected = defaultdict(float)
    
    for x, prob in mu_dict.items():
        x_proj = x % M_to
        if x_proj % 3 != 0:  # Still in G_{k-1}
            projected[x_proj] += prob
    
    # Renormalize
    total = sum(projected.values())
    return {x: p / total for x, p in projected.items()}


def tv_distance(mu, pi, states):
    """Compute total variation distance."""
    tv = 0
    for x in states:
        tv += abs(mu.get(x, 0) - pi.get(x, 0))
    return tv / 2


def compute_energy_split(mu_k, pi_k, k):
    """Compute coarse vs within-lift energy split."""
    M = 3**k
    M_prev = 3**(k-1)
    
    states_k = [x for x in range(1, M) if x % 3 != 0]
    states_prev = [x for x in range(1, M_prev) if x % 3 != 0]
    
    # Delta at level k
    delta_k = {x: mu_k.get(x, 0) - pi_k.get(x, 0) for x in states_k}
    
    # Project to level k-1
    mu_proj = defaultdict(float)
    pi_proj = defaultdict(float)
    
    for x in states_k:
        x_proj = x % M_prev
        mu_proj[x_proj] += mu_k.get(x, 0)
        pi_proj[x_proj] += pi_k.get(x, 0)
    
    # Coarse delta
    delta_coarse = {b: mu_proj[b] - pi_proj[b] for b in states_prev}
    
    # Total energy = Σ |δ(x)|²
    total_energy = sum(d**2 for d in delta_k.values())
    
    # Coarse energy: lift delta_coarse back to k (uniform within fiber)
    # Each coarse delta contributes to 3 lifts
    coarse_energy = 0
    for b in states_prev:
        # The coarse component at each lift is delta_coarse[b] / 3
        coarse_energy += 3 * (delta_coarse[b] / 3)**2
    
    # Within-lift energy = total - coarse
    within_lift_energy = total_energy - coarse_energy
    
    return {
        'total': total_energy,
        'coarse': coarse_energy,
        'within_lift': within_lift_energy,
        'coarse_pct': 100 * coarse_energy / total_energy if total_energy > 0 else 0,
        'within_lift_pct': 100 * within_lift_energy / total_energy if total_energy > 0 else 0
    }


def main():
    print("="*70)
    print("VERIFY 'NO LIFT' CLAIM")
    print("="*70)
    
    # Parameters
    k = 6
    k_prev = 5
    n_samples = 500000
    B = 100
    
    print(f"\nParameters: k={k}, k_prev={k_prev}, n_samples={n_samples}, B={B}")
    
    # Step 1: Sample μ₆ (killed)
    print(f"\n1. Sampling μ₆ (killed, B={B})...")
    mu_6 = sample_killed_distribution(k, n_samples, B=B, seed=42)
    print(f"   Sampled {len(mu_6)} distinct residues")
    
    # Step 2: Build π₅ and π₆
    print("\n2. Building exact π₅ and π₆...")
    states_5, pi_5 = build_exact_pi(k_prev)
    states_6, pi_6 = build_exact_pi(k)
    print(f"   |G₅| = {len(states_5)}, |G₆| = {len(states_6)}")
    
    # Step 3: Project μ₆ to G₅
    print("\n3. Projecting μ₆ to G₅ (ρ#μ₆)...")
    mu_6_proj = project_to_lower_k(mu_6, k, k_prev)
    print(f"   Projected to {len(mu_6_proj)} residues")
    
    # Step 4: Compute TV distances
    print("\n4. Computing TV distances...")
    tv_mu6_pi6 = tv_distance(mu_6, pi_6, states_6)
    tv_proj_pi5 = tv_distance(mu_6_proj, pi_5, states_5)
    
    print(f"\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    print(f"\n   TV(μ₆, π₆)     = {tv_mu6_pi6:.4f} ({tv_mu6_pi6*100:.2f}%)")
    print(f"   TV(ρ#μ₆, π₅)   = {tv_proj_pi5:.4f} ({tv_proj_pi5*100:.2f}%)")
    print(f"   Ratio          = {tv_proj_pi5/tv_mu6_pi6:.2f}×")
    
    if tv_proj_pi5 < tv_mu6_pi6 * 0.3:
        print(f"\n   ✅ CONFIRMED: Projected TV is much smaller!")
        print(f"      This explains why LIFT modes disappeared from top-20.")
    else:
        print(f"\n   ⚠️ Projected TV is not much smaller than full TV.")
    
    # Step 5: Energy split
    print(f"\n5. Computing energy split at k={k}...")
    energy = compute_energy_split(mu_6, pi_6, k)
    
    print(f"\n   Total energy:      {energy['total']:.6e}")
    print(f"   Coarse energy:     {energy['coarse']:.6e} ({energy['coarse_pct']:.1f}%)")
    print(f"   Within-lift energy: {energy['within_lift']:.6e} ({energy['within_lift_pct']:.1f}%)")
    
    if energy['within_lift_pct'] > 90:
        print(f"\n   ✅ Within-lift dominates! ({energy['within_lift_pct']:.1f}%)")
        print(f"      All remaining mismatch is digit-splitting (NEW-DIGIT modes).")
    
    # Step 6: Also sample μ₅ killed and compare
    print(f"\n6. Sampling μ₅ (killed) for comparison...")
    mu_5 = sample_killed_distribution(k_prev, n_samples, B=B, seed=42)
    tv_mu5_pi5 = tv_distance(mu_5, pi_5, states_5)
    
    print(f"\n   TV(μ₅, π₅)     = {tv_mu5_pi5:.4f} ({tv_mu5_pi5*100:.2f}%)")
    print(f"   TV(ρ#μ₆, π₅)   = {tv_proj_pi5:.4f} ({tv_proj_pi5*100:.2f}%)")
    
    if abs(tv_proj_pi5 - tv_mu5_pi5) < 0.005:
        print(f"\n   ≈ Similar! The projected k=6 measure matches k=5 killed measure.")
    elif tv_proj_pi5 < tv_mu5_pi5:
        print(f"\n   ρ#μ₆ is closer to π₅ than μ₅ is!")
        print(f"   → Going to higher k helps wash out coarse mismatch.")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)
    
    # Save results
    import json
    results = {
        'k': k,
        'k_prev': k_prev,
        'n_samples': n_samples,
        'B': B,
        'tv_mu6_pi6': tv_mu6_pi6,
        'tv_proj_pi5': tv_proj_pi5,
        'tv_mu5_pi5': tv_mu5_pi5,
        'energy_split': energy
    }
    
    with open('data/no_lift_verification.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/no_lift_verification.json")


if __name__ == "__main__":
    main()
