#!/usr/bin/env python3
"""
Finite Verification for Small Set C

Verifies that every odd n ≤ B₀ eventually reaches 1 under the Syracuse map T.
This is trivial but formally required to close the Foster-Lyapunov proof.

Usage:
    python src/finite_verification.py [B0]
    
Default B0 = 10000 (covers crystalline + transition phases)
"""

import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def syracuse(n: int) -> int:
    """Accelerated Syracuse map: T(n) = (3n+1) / 2^a(n)"""
    x = 3 * n + 1
    while x % 2 == 0:
        x //= 2
    return x

def reaches_one(n: int, max_steps: int = 10000) -> tuple[bool, int]:
    """Check if n reaches 1 under Syracuse iteration."""
    steps = 0
    current = n
    while current != 1 and steps < max_steps:
        current = syracuse(current)
        steps += 1
    return current == 1, steps

def verify_small_set(B0: int) -> dict:
    """
    Verify all odd n ≤ B0 reach 1.
    
    Returns dict with:
        - verified: bool (all reach 1?)
        - count: number of odd integers checked
        - max_steps: longest trajectory
        - max_steps_n: which n had longest trajectory
        - failures: list of n that didn't reach 1 (should be empty!)
    """
    failures = []
    max_steps = 0
    max_steps_n = 1
    count = 0
    
    for n in range(1, B0 + 1, 2):  # odd numbers only
        count += 1
        success, steps = reaches_one(n)
        if not success:
            failures.append(n)
        if steps > max_steps:
            max_steps = steps
            max_steps_n = n
    
    return {
        'B0': B0,
        'verified': len(failures) == 0,
        'count': count,
        'max_steps': max_steps,
        'max_steps_n': max_steps_n,
        'failures': failures
    }

def main():
    B0 = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    
    print(f"=" * 60)
    print(f"FINITE VERIFICATION FOR SMALL SET C = {{n ≤ {B0}}}")
    print(f"=" * 60)
    print()
    
    result = verify_small_set(B0)
    
    print(f"Odd integers checked: {result['count']}")
    print(f"All reach 1: {'✅ YES' if result['verified'] else '❌ NO'}")
    print(f"Longest trajectory: {result['max_steps']} steps (n = {result['max_steps_n']})")
    
    if result['failures']:
        print(f"\n⚠️ FAILURES: {result['failures']}")
    else:
        print(f"\n✅ VERIFICATION COMPLETE")
        print(f"   Every odd n ≤ {B0} reaches 1 under Syracuse iteration.")
        print(f"   This closes the Small Set gap in the Foster-Lyapunov proof.")
    
    print()
    return 0 if result['verified'] else 1

if __name__ == '__main__':
    sys.exit(main())
