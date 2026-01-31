#!/usr/bin/env python3
"""
Collatz Conjecture Analysis
===========================
Analyzing sequences for patterns in stopping times and trajectory behavior.

The Collatz function:
- If n is even: n → n/2
- If n is odd:  n → 3n + 1

Conjecture: Every positive integer eventually reaches 1.
"""

import time
from collections import defaultdict
import json

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
    
    # n is now either 1 or smaller than original (cached)
    if n in cache:
        total_steps = steps + cache[n]
    else:
        total_steps = steps
    
    # Cache intermediate values
    for i, val in enumerate(path):
        if val not in cache:
            cache[val] = total_steps - i
    
    cache[original_n] = total_steps
    return total_steps


def collatz_max_value(n):
    """Find the maximum value reached in the sequence."""
    max_val = n
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        max_val = max(max_val, n)
    return max_val


def analyze_range(limit):
    """Analyze Collatz sequences for numbers 1 to limit."""
    print(f"Analyzing Collatz sequences for n = 1 to {limit:,}")
    print("=" * 60)
    
    start_time = time.time()
    cache = {}
    
    stopping_times = []
    record_holders = []  # Numbers that set new records for stopping time
    current_record = 0
    
    # Distribution of stopping times
    time_distribution = defaultdict(int)
    
    # Numbers with stopping time in certain ranges
    long_sequences = []  # top 20 longest
    
    for n in range(1, limit + 1):
        st = collatz_stopping_time(n, cache)
        stopping_times.append(st)
        time_distribution[st] += 1
        
        if st > current_record:
            current_record = st
            record_holders.append((n, st))
        
        # Track longest sequences
        if len(long_sequences) < 20 or st > long_sequences[-1][1]:
            long_sequences.append((n, st))
            long_sequences.sort(key=lambda x: -x[1])
            long_sequences = long_sequences[:20]
        
        if n % 1_000_000 == 0:
            elapsed = time.time() - start_time
            print(f"  Processed {n:,} numbers in {elapsed:.1f}s")
    
    elapsed = time.time() - start_time
    
    # Statistics
    avg_stopping_time = sum(stopping_times) / len(stopping_times)
    max_stopping_time = max(stopping_times)
    
    print(f"\nCompleted in {elapsed:.1f} seconds")
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    
    print(f"\n📊 Basic Statistics:")
    print(f"  Range analyzed: 1 to {limit:,}")
    print(f"  Average stopping time: {avg_stopping_time:.2f}")
    print(f"  Maximum stopping time: {max_stopping_time}")
    
    print(f"\n🏆 Record Holders (numbers that set new stopping time records):")
    for n, st in record_holders[-15:]:
        print(f"  n = {n:>12,} → {st} steps")
    
    print(f"\n🔝 Top 20 Longest Sequences:")
    for n, st in long_sequences:
        print(f"  n = {n:>12,} → {st} steps")
    
    # Look for patterns in record holders
    print(f"\n🔍 Pattern Analysis:")
    
    # Check if record holders follow any pattern
    record_nums = [n for n, _ in record_holders]
    
    # Check for numbers of form 2^k - 1
    print("\n  Numbers of form 2^k - 1 (Mersenne-like):")
    for k in range(1, 30):
        m = 2**k - 1
        if m <= limit:
            st = collatz_stopping_time(m, cache)
            print(f"    2^{k} - 1 = {m:>12,} → {st} steps")
    
    # Check for numbers of form 3^k
    print("\n  Numbers of form 3^k:")
    k = 1
    while 3**k <= limit:
        n = 3**k
        st = collatz_stopping_time(n, cache)
        print(f"    3^{k} = {n:>12,} → {st} steps")
        k += 1
    
    # Stopping time distribution summary
    print(f"\n📈 Stopping Time Distribution:")
    print(f"  Most common stopping times:")
    sorted_dist = sorted(time_distribution.items(), key=lambda x: -x[1])[:10]
    for st, count in sorted_dist:
        pct = 100 * count / limit
        print(f"    {st} steps: {count:,} numbers ({pct:.2f}%)")
    
    # Find clusters
    print(f"\n🎯 Interesting Observations:")
    
    # Numbers that reach very high values
    print("\n  Numbers with highest trajectory peaks (checking sample):")
    peak_records = []
    for n in range(1, min(limit, 100000) + 1):
        peak = collatz_max_value(n)
        ratio = peak / n
        if len(peak_records) < 10 or ratio > peak_records[-1][2]:
            peak_records.append((n, peak, ratio))
            peak_records.sort(key=lambda x: -x[2])
            peak_records = peak_records[:10]
    
    for n, peak, ratio in peak_records:
        print(f"    n = {n:>8,} → peak = {peak:>15,} (ratio: {ratio:.1f}x)")
    
    return {
        'limit': limit,
        'avg_stopping_time': avg_stopping_time,
        'max_stopping_time': max_stopping_time,
        'record_holders': record_holders,
        'long_sequences': long_sequences,
        'elapsed_seconds': elapsed
    }


if __name__ == "__main__":
    # Start with 10 million for meaningful patterns
    results = analyze_range(10_000_000)
    
    # Save results
    with open('collatz_results.json', 'w') as f:
        json.dump({
            'limit': results['limit'],
            'avg_stopping_time': results['avg_stopping_time'],
            'max_stopping_time': results['max_stopping_time'],
            'record_holders': results['record_holders'][-30:],
            'long_sequences': results['long_sequences'],
            'elapsed_seconds': results['elapsed_seconds']
        }, f, indent=2)
    
    print(f"\n✅ Results saved to collatz_results.json")
