#!/usr/bin/env python3
"""
Transition Matrix Heatmap (Experiment C)

Visualize the conditional transition probabilities Q(x,·) vs ideal P(x,·).
If heatmap shows structure → conditional defects found.
If uniform → even stronger randomness argument.

Author: clawdbot
Date: 2026-02-01
"""

import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import json


def syracuse_step(n: int):
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def sample_transitions(k: int, n_samples: int, B: int, seed: int = 42):
    """Sample transitions (x → y) under killed process."""
    M = 3**k
    # Count transitions: transitions[x][y] = count
    transitions = defaultdict(lambda: defaultdict(int))
    
    rng = np.random.default_rng(seed)
    n_collected = 0
    n = int(rng.integers(10**10, 10**14)) | 1
    
    while n_collected < n_samples:
        if n <= B:
            n = int(rng.integers(10**10, 10**14)) | 1
            continue
        
        x = n % M
        if x % 3 != 0:
            next_n, a = syracuse_step(n)
            y = next_n % M
            if y % 3 != 0 and next_n > B:
                transitions[x][y] += 1
                n_collected += 1
            n = next_n
        else:
            n, _ = syracuse_step(n)
    
    return dict(transitions)


def build_ideal_P(k: int):
    """Build ideal transition matrix P."""
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
    
    return states, idx, P


def transitions_to_matrix(transitions, states, idx):
    """Convert transition counts to probability matrix."""
    n_states = len(states)
    Q = np.zeros((n_states, n_states))
    
    for x, targets in transitions.items():
        if x not in idx:
            continue
        i = idx[x]
        total = sum(targets.values())
        if total > 0:
            for y, count in targets.items():
                if y in idx:
                    j = idx[y]
                    Q[i, j] = count / total
    
    return Q


def main():
    print("="*70)
    print("TRANSITION MATRIX HEATMAP (Experiment C)")
    print("="*70)
    
    # Use k=5 for cleaner visualization (162 states vs 486)
    k = 5
    B = 10  # Low B where we found structure
    n_samples = 500000
    
    print(f"\nParameters: k={k}, B={B}, n_samples={n_samples}")
    
    # Build ideal P
    print("\n1. Building ideal transition matrix P...")
    states, idx, P = build_ideal_P(k)
    n_states = len(states)
    print(f"   |G_{k}| = {n_states}")
    
    # Sample transitions
    print(f"\n2. Sampling transitions (B={B})...")
    transitions = sample_transitions(k, n_samples, B=B, seed=42)
    print(f"   Sampled {len(transitions)} unique starting states")
    
    # Convert to matrix
    print("\n3. Converting to probability matrix Q...")
    Q = transitions_to_matrix(transitions, states, idx)
    
    # Compute difference
    diff = np.abs(Q - P)
    
    # Statistics
    print("\n4. Computing statistics...")
    
    # Row-wise TV distances
    row_tv = np.sum(diff, axis=1) / 2
    
    print(f"\n   Max row TV:  {np.max(row_tv):.4f}")
    print(f"   Mean row TV: {np.mean(row_tv):.4f}")
    print(f"   Std row TV:  {np.std(row_tv):.4f}")
    
    # Find worst rows
    worst_idx = np.argsort(row_tv)[-10:][::-1]
    print(f"\n   Top 10 worst conditional defects:")
    print(f"   {'Rank':<6} {'State x':<10} {'TV(Q(x,·), P(x,·))':<20}")
    print(f"   {'-'*36}")
    for rank, i in enumerate(worst_idx):
        print(f"   {rank+1:<6} {states[i]:<10} {row_tv[i]:<20.4f}")
    
    # Create visualizations
    print("\n5. Creating heatmaps...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Ideal P
    ax1 = axes[0, 0]
    im1 = ax1.imshow(P, cmap='Blues', aspect='auto')
    ax1.set_title(f'Ideal P (k={k})')
    ax1.set_xlabel('Target state index')
    ax1.set_ylabel('Source state index')
    plt.colorbar(im1, ax=ax1, label='P(x,y)')
    
    # Plot 2: Empirical Q
    ax2 = axes[0, 1]
    im2 = ax2.imshow(Q, cmap='Blues', aspect='auto')
    ax2.set_title(f'Empirical Q (B={B})')
    ax2.set_xlabel('Target state index')
    ax2.set_ylabel('Source state index')
    plt.colorbar(im2, ax=ax2, label='Q(x,y)')
    
    # Plot 3: Difference |Q - P|
    ax3 = axes[1, 0]
    im3 = ax3.imshow(diff, cmap='Reds', aspect='auto')
    ax3.set_title(f'|Q - P| (conditional defects)')
    ax3.set_xlabel('Target state index')
    ax3.set_ylabel('Source state index')
    plt.colorbar(im3, ax=ax3, label='|Q(x,y) - P(x,y)|')
    
    # Plot 4: Row TV distances
    ax4 = axes[1, 1]
    ax4.bar(range(n_states), row_tv, width=1.0, color='red', alpha=0.7)
    ax4.axhline(y=np.mean(row_tv), color='blue', linestyle='--', label=f'Mean: {np.mean(row_tv):.3f}')
    ax4.set_title('TV(Q(x,·), P(x,·)) by source state')
    ax4.set_xlabel('Source state index')
    ax4.set_ylabel('Row TV distance')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('data/transition_heatmap_k5_B10.png', dpi=150)
    print(f"   Saved: data/transition_heatmap_k5_B10.png")
    
    # Also do B=100 for comparison
    print(f"\n6. Comparing with B=100...")
    transitions_100 = sample_transitions(k, n_samples, B=100, seed=42)
    Q_100 = transitions_to_matrix(transitions_100, states, idx)
    diff_100 = np.abs(Q_100 - P)
    row_tv_100 = np.sum(diff_100, axis=1) / 2
    
    print(f"\n   B=10:  Mean row TV = {np.mean(row_tv):.4f}, Max = {np.max(row_tv):.4f}")
    print(f"   B=100: Mean row TV = {np.mean(row_tv_100):.4f}, Max = {np.max(row_tv_100):.4f}")
    
    # Summary
    print(f"\n{'='*70}")
    print("ANALYSIS")
    print(f"{'='*70}")
    
    if np.max(row_tv) > 0.1:
        print(f"\n⚠️ Found significant conditional defects!")
        print(f"   Some states have TV > 10% from ideal.")
        print(f"   The marginal may look good but transitions are structured.")
    elif np.max(row_tv) > 0.05:
        print(f"\n📊 Moderate conditional defects found.")
        print(f"   Some structure in transitions, but not severe.")
    else:
        print(f"\n✅ Transitions look close to ideal!")
        print(f"   Conditional behavior matches marginal finding.")
    
    print(f"\n{'='*70}")
    print("DONE")
    print(f"{'='*70}")
    
    # Save data
    results = {
        'k': k,
        'B': B,
        'n_samples': n_samples,
        'n_states': n_states,
        'mean_row_tv': float(np.mean(row_tv)),
        'max_row_tv': float(np.max(row_tv)),
        'std_row_tv': float(np.std(row_tv)),
        'worst_states': [{'state': int(states[i]), 'tv': float(row_tv[i])} 
                        for i in worst_idx],
        'B_100_mean_tv': float(np.mean(row_tv_100)),
        'B_100_max_tv': float(np.max(row_tv_100))
    }
    
    with open('data/transition_heatmap_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to data/transition_heatmap_results.json")


if __name__ == "__main__":
    main()
