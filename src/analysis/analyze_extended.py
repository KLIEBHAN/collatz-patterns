#!/usr/bin/env python3
"""
Extended Collatz Analysis
=========================
Exploring patterns in binary representation, prime factors, and residue classes.
"""

import time
from collections import defaultdict
import json
import math

def collatz_stopping_time(n, cache={}):
    """Calculate steps to reach 1 (with memoization)."""
    if n == 1:
        return 0
    if n in cache:
        return cache[n]
    
    original_n = n
    steps = 0
    path = []
    
    while n != 1 and n >= original_n:
        path.append(n)
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    
    if n in cache:
        total_steps = steps + cache[n]
    else:
        total_steps = steps
    
    for i, val in enumerate(path):
        if val not in cache:
            cache[val] = total_steps - i
    
    cache[original_n] = total_steps
    return total_steps


def binary_properties(n):
    """Analyze binary representation properties."""
    binary = bin(n)[2:]
    return {
        'length': len(binary),
        'ones': binary.count('1'),
        'zeros': binary.count('0'),
        'density': binary.count('1') / len(binary),  # Ratio of 1s
        'trailing_zeros': len(binary) - len(binary.rstrip('0')),
        'leading_ones': len(binary) - len(binary.lstrip('1')),
    }


def prime_factors(n):
    """Get prime factorization."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def analyze_binary_correlation(limit=100000):
    """Analyze correlation between binary properties and stopping time."""
    print(f"Analyzing binary correlation for n = 1 to {limit:,}")
    print("=" * 60)
    
    cache = {}
    
    # Group by ones-count
    by_ones_count = defaultdict(list)
    # Group by density ranges
    by_density = defaultdict(list)
    
    for n in range(1, limit + 1):
        st = collatz_stopping_time(n, cache)
        bp = binary_properties(n)
        
        by_ones_count[bp['ones']].append((n, st))
        
        # Density buckets: 0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0
        density_bucket = int(bp['density'] * 5)
        by_density[density_bucket].append((n, st))
    
    print("\n📊 Stopping Time by Number of 1-bits:")
    print("-" * 40)
    for ones in sorted(by_ones_count.keys())[:15]:
        items = by_ones_count[ones]
        avg_st = sum(st for _, st in items) / len(items)
        max_st = max(st for _, st in items)
        print(f"  {ones:2d} ones: avg={avg_st:6.1f}, max={max_st:4d}, count={len(items):6d}")
    
    print("\n📊 Stopping Time by Bit Density:")
    print("-" * 40)
    density_labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
    for bucket in range(5):
        items = by_density[bucket]
        if items:
            avg_st = sum(st for _, st in items) / len(items)
            max_st = max(st for _, st in items)
            print(f"  {density_labels[bucket]:8s}: avg={avg_st:6.1f}, max={max_st:4d}, count={len(items):6d}")
    
    return by_ones_count, by_density


def analyze_residue_classes(limit=100000):
    """Analyze behavior by residue class."""
    print(f"\nAnalyzing residue classes for n = 1 to {limit:,}")
    print("=" * 60)
    
    cache = {}
    
    # Analyze mod 6 (combines mod 2 and mod 3)
    by_mod6 = defaultdict(list)
    by_mod12 = defaultdict(list)
    
    for n in range(1, limit + 1):
        st = collatz_stopping_time(n, cache)
        by_mod6[n % 6].append((n, st))
        by_mod12[n % 12].append((n, st))
    
    print("\n📊 Stopping Time by n mod 6:")
    print("-" * 40)
    for r in range(6):
        items = by_mod6[r]
        avg_st = sum(st for _, st in items) / len(items)
        max_st = max(st for _, st in items)
        print(f"  n ≡ {r} (mod 6): avg={avg_st:6.1f}, max={max_st:4d}")
    
    print("\n📊 Stopping Time by n mod 12:")
    print("-" * 40)
    for r in range(12):
        items = by_mod12[r]
        avg_st = sum(st for _, st in items) / len(items)
        max_st = max(st for _, st in items)
        print(f"  n ≡ {r:2d} (mod 12): avg={avg_st:6.1f}, max={max_st:4d}")
    
    return by_mod6, by_mod12


def analyze_prime_factors_correlation(limit=50000):
    """Analyze correlation with prime factorization."""
    print(f"\nAnalyzing prime factor correlation for n = 1 to {limit:,}")
    print("=" * 60)
    
    cache = {}
    
    # Group by number of prime factors (with multiplicity)
    by_omega = defaultdict(list)  # Number of distinct prime factors
    by_Omega = defaultdict(list)  # Total prime factors with multiplicity
    
    # Special: numbers with only small factors
    smooth_numbers = []  # 5-smooth (factors only 2, 3, 5)
    
    for n in range(2, limit + 1):
        st = collatz_stopping_time(n, cache)
        pf = prime_factors(n)
        
        omega = len(set(pf))  # Distinct factors
        Omega = len(pf)       # With multiplicity
        
        by_omega[omega].append((n, st))
        by_Omega[Omega].append((n, st))
        
        # Check if 5-smooth
        if all(p <= 5 for p in pf):
            smooth_numbers.append((n, st, pf))
    
    print("\n📊 Stopping Time by distinct prime factors (ω):")
    print("-" * 40)
    for omega in sorted(by_omega.keys())[:8]:
        items = by_omega[omega]
        avg_st = sum(st for _, st in items) / len(items)
        max_st = max(st for _, st in items)
        print(f"  ω(n)={omega}: avg={avg_st:6.1f}, max={max_st:4d}, count={len(items):6d}")
    
    print("\n📊 Stopping Time by total prime factors (Ω):")
    print("-" * 40)
    for Omega in sorted(by_Omega.keys())[:10]:
        items = by_Omega[Omega]
        avg_st = sum(st for _, st in items) / len(items)
        max_st = max(st for _, st in items)
        print(f"  Ω(n)={Omega:2d}: avg={avg_st:6.1f}, max={max_st:4d}, count={len(items):6d}")
    
    print("\n📊 5-Smooth numbers (factors ≤ 5 only):")
    print("-" * 40)
    smooth_numbers.sort(key=lambda x: -x[1])
    print(f"  Total count: {len(smooth_numbers)}")
    print(f"  Top 10 by stopping time:")
    for n, st, pf in smooth_numbers[:10]:
        print(f"    n={n:6d} = {' × '.join(map(str, pf)):20s} → {st} steps")
    
    return by_omega, by_Omega


def find_interesting_sequences(limit=100000):
    """Find sequences with unusual properties."""
    print(f"\nFinding interesting sequences for n = 1 to {limit:,}")
    print("=" * 60)
    
    cache = {}
    
    # Find numbers where sequence length > log2(n) * some factor
    unusual_length = []
    
    for n in range(2, limit + 1):
        st = collatz_stopping_time(n, cache)
        expected = math.log2(n) * 10  # Rough heuristic
        if st > expected * 2:
            unusual_length.append((n, st, st / math.log2(n)))
    
    unusual_length.sort(key=lambda x: -x[2])
    
    print("\n🎯 Numbers with unusually long sequences (relative to log₂(n)):")
    print("-" * 50)
    for n, st, ratio in unusual_length[:15]:
        bp = binary_properties(n)
        print(f"  n={n:6d} (bits={bp['length']:2d}, ones={bp['ones']:2d}): {st} steps, ratio={ratio:.1f}")
    
    return unusual_length


if __name__ == "__main__":
    print("=" * 60)
    print("EXTENDED COLLATZ ANALYSIS")
    print("=" * 60)
    
    start = time.time()
    
    # Run all analyses
    analyze_binary_correlation(100000)
    analyze_residue_classes(100000)
    analyze_prime_factors_correlation(50000)
    find_interesting_sequences(100000)
    
    elapsed = time.time() - start
    print(f"\n✅ Analysis complete in {elapsed:.1f} seconds")
