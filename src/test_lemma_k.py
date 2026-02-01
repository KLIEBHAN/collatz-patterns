#!/usr/bin/env python3
"""
Direkter Test von Lemma (K):
  Σ 𝟙{a=1} ≤ θt + C·log₂(n)

Zählt a=1 Schritte direkt und prüft gegen die Grenze.
"""

import random
import math

def collatz_step(n):
    """Syracuse map: T(n) = (3n+1) / 2^a, returns (next_n, a)"""
    temp = 3 * n + 1
    a = 0
    while temp % 2 == 0:
        a += 1
        temp //= 2
    return temp, a

def test_lemma_k(start_n, max_steps=10000, theta=0.415, C=1.0):
    """
    Testet Lemma (K) für einen Startwert.
    
    Returns: dict mit Statistiken
    """
    n = start_n
    log_n = math.log2(start_n) if start_n > 0 else 0
    
    count_a1 = 0  # Anzahl a=1 Schritte
    total_steps = 0
    
    max_ratio = 0  # Maximum von (count_a1 - C*log_n) / t
    worst_step = 0
    
    violations = []  # Schritte wo (K) verletzt wird
    
    while n > 1 and total_steps < max_steps:
        next_n, a = collatz_step(n)
        total_steps += 1
        
        if a == 1:
            count_a1 += 1
        
        # Prüfe (K): count_a1 ≤ θ*t + C*log₂(n)
        bound = theta * total_steps + C * log_n
        
        if count_a1 > bound:
            violations.append({
                'step': total_steps,
                'count_a1': count_a1,
                'bound': bound,
                'excess': count_a1 - bound
            })
        
        # Track worst ratio: (count_a1 - C*log_n) / t
        if total_steps > 0:
            effective_ratio = (count_a1 - C * log_n) / total_steps
            if effective_ratio > max_ratio:
                max_ratio = effective_ratio
                worst_step = total_steps
        
        n = next_n
    
    # Finale Statistiken
    final_ratio = count_a1 / total_steps if total_steps > 0 else 0
    effective_final = (count_a1 - C * log_n) / total_steps if total_steps > 0 else 0
    
    return {
        'start_n': start_n,
        'log_n': log_n,
        'total_steps': total_steps,
        'count_a1': count_a1,
        'final_ratio': final_ratio,
        'effective_ratio': effective_final,
        'max_ratio': max_ratio,
        'worst_step': worst_step,
        'violations': len(violations),
        'first_violation': violations[0] if violations else None,
        'holds': len(violations) == 0
    }

def main():
    print("=" * 70)
    print("LEMMA (K) TEST: Σ 𝟙{a=1} ≤ θt + C·log₂(n)")
    print("=" * 70)
    
    theta = 0.415  # Kritische Grenze
    C = 1.0        # Konstante für log-Term
    
    print(f"\nParameter: θ = {theta}, C = {C}")
    print("-" * 70)
    
    # Test-Kandidaten
    test_cases = [
        ("n=27 (Klassiker)", 27),
        ("n=703 (bekannt lang)", 703),
        ("n=77671 (extremer Peak)", 77671),
        ("2^100 - 1 (100 Einsen)", 2**100 - 1),
        ("2^500 - 1 (500 Einsen)", 2**500 - 1),
        ("2^1000 - 1 (1000 Einsen)", 2**1000 - 1),
    ]
    
    # Zufällige große Zahlen
    random.seed(42)
    for i in range(5):
        bits = random.randint(100, 2000)
        n = random.getrandbits(bits) | 1  # ungerade
        test_cases.append((f"Random {bits}-bit #{i+1}", n))
    
    # Spezielle "adversarial" Kandidaten
    # Zahlen nahe -1 mod 2^k für verschiedene k
    for k in [10, 20, 50]:
        n = 2**k - 1  # = -1 mod 2^k, hat h(n) = k
        test_cases.append((f"2^{k} - 1 (h={k})", n))
    
    print(f"\n{'Name':<30} {'Steps':>8} {'#a=1':>8} {'Ratio':>8} {'Eff.Ratio':>10} {'Holds?':>8}")
    print("-" * 70)
    
    all_hold = True
    worst_case = None
    worst_eff_ratio = -float('inf')
    
    for name, n in test_cases:
        result = test_lemma_k(n, max_steps=50000, theta=theta, C=C)
        
        status = "✅" if result['holds'] else "❌"
        print(f"{name:<30} {result['total_steps']:>8} {result['count_a1']:>8} "
              f"{result['final_ratio']:>8.4f} {result['effective_ratio']:>10.4f} {status:>8}")
        
        if not result['holds']:
            all_hold = False
            if result['first_violation']:
                print(f"   ⚠️  Erste Verletzung bei Schritt {result['first_violation']['step']}: "
                      f"count={result['first_violation']['count_a1']}, bound={result['first_violation']['bound']:.2f}")
        
        if result['effective_ratio'] > worst_eff_ratio:
            worst_eff_ratio = result['effective_ratio']
            worst_case = (name, result)
    
    print("-" * 70)
    print(f"\n📊 ZUSAMMENFASSUNG:")
    print(f"   Kritische Grenze θ = {theta}")
    print(f"   Getestete Fälle: {len(test_cases)}")
    print(f"   Alle halten (K): {'✅ JA' if all_hold else '❌ NEIN'}")
    
    if worst_case:
        name, result = worst_case
        print(f"\n   Worst Case: {name}")
        print(f"   - Effektive Ratio: {result['effective_ratio']:.4f}")
        print(f"   - Raw Ratio: {result['final_ratio']:.4f}")
        print(f"   - Abstand zu θ: {theta - result['effective_ratio']:.4f}")
    
    # Zusätzlicher Test: Suche nach Zahlen mit hohem initialem h(n)
    print(f"\n" + "=" * 70)
    print("ADVERSARIAL SEARCH: Zahlen mit sehr hohem h(n)")
    print("=" * 70)
    
    # Zahlen der Form 2^k * m - 1 mit kleinem m
    print(f"\n{'Form':<40} {'h(n)':>6} {'Steps':>8} {'Eff.Ratio':>10} {'Holds?':>8}")
    print("-" * 70)
    
    for k in [20, 50, 100, 200]:
        for m in [1, 3, 5, 7]:
            n = (2**k) * m - 1
            if n > 1 and n % 2 == 1:
                # h(n) = ν₂(n+1) = ν₂(2^k * m) = k + ν₂(m)
                h_n = k
                result = test_lemma_k(n, max_steps=50000, theta=theta, C=C)
                status = "✅" if result['holds'] else "❌"
                print(f"2^{k}*{m} - 1 (h={h_n}){'':<20} {h_n:>6} {result['total_steps']:>8} "
                      f"{result['effective_ratio']:>10.4f} {status:>8}")

if __name__ == "__main__":
    main()
