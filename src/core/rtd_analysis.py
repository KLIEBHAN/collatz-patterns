#!/usr/bin/env python3
"""
RTD (Return Time vs Depth) Analysis
Testet ob die Wartezeit auf Tiefe R exponentiell mit R wächst.
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict

def get_2adic_depth(n):
    """
    Berechnet die Tiefe R = v_2(n+1).
    Das ist die Anzahl der Einsen am Ende von n (binär).
    z.B. n=...0111 -> R=3.
    """
    if n % 2 == 0:
        return 0
    m = n + 1
    val = 0
    while m > 0 and m % 2 == 0:
        val += 1
        m //= 2
    return val

def analyze_rtd(start_bits=3000, max_steps=500000):
    """
    Führt eine RTD (Return Time vs Depth) Analyse durch.
    Wir nehmen eine zufällige Zahl mit 'start_bits' Länge,
    damit der Orbit nicht zu schnell stirbt (wir brauchen viele Daten).
    """
    # Riesige Zufallszahl als Start
    random.seed(42)  # Reproduzierbar
    n = random.getrandbits(start_bits) | 1
    
    # Speicher für: Wann haben wir Tiefe R das letzte Mal gesehen?
    # Dictionary: R -> letzter_zeitpunkt
    last_seen = {}
    
    # Speicher für: Alle Wartezeiten für Tiefe R
    # Dictionary: R -> [diff1, diff2, ...]
    wait_times = defaultdict(list)
    
    print(f"Starte Simulation mit {start_bits}-Bit Zahl für {max_steps} Schritte...")
    
    for t in range(max_steps):
        if n <= 1:
            print(f"Orbit terminiert bei Schritt {t}")
            break
        
        # 1. Bestimme Tiefe R der aktuellen Zahl
        depth = get_2adic_depth(n)
        
        # 2. Registriere Wartezeiten für ALLE Tiefen r <= depth
        # Denn wenn eine Zahl Tiefe 5 hat, hat sie auch Tiefe 4, 3 und 2.
        # Wir betrachten nur r >= 2 (da r=1 trivial ist für alle ungeraden).
        if depth >= 2:
            # Wir cappen R bei 25, sonst wird die Statistik zu dünn
            max_r_track = min(depth, 25)
            for r in range(2, max_r_track + 1):
                if r in last_seen:
                    diff = t - last_seen[r]
                    wait_times[r].append(diff)
                # Update: Wir haben r jetzt gesehen
                last_seen[r] = t
        
        # 3. Collatz Schritt
        temp = 3 * n + 1
        while temp % 2 == 0:
            temp //= 2
        n = temp
    
    return wait_times

# --- DURCHFÜHRUNG ---
print("RTD-Analyse: Return Time vs Depth")
print("=" * 60)

# Wir simulieren 200.000 Schritte. Das sollte reichen, um R bis ca. 12-15 gut zu sehen.
data = analyze_rtd(start_bits=4000, max_steps=200000)

# --- AUSWERTUNG ---
print("\n" + "=" * 60)
print("ERGEBNISSE:")
print("=" * 60)

# Wir berechnen den Durchschnitt der Wartezeiten pro Tiefe R
depths = sorted(data.keys())
avg_waits = [np.mean(data[r]) for r in depths]
counts = [len(data[r]) for r in depths]

# Zum Vergleich: Die theoretische Kurve 2^(R-1)
theoretical_curve = [2**(r-1) for r in depths]

print(f"\n{'R':<5} {'Samples':<10} {'Avg Wait':<12} {'Theory 2^(R-1)':<15} {'Ratio':<10}")
print("-" * 55)
for r, avg, theory, count in zip(depths, avg_waits, theoretical_curve, counts):
    ratio = avg / theory if theory > 0 else 0
    print(f"{r:<5} {count:<10} {avg:<12.2f} {theory:<15} {ratio:<10.3f}")

# --- PLOTTING ---
plt.figure(figsize=(10, 6))

# WICHTIG: Logarithmische Y-Achse!
# Wenn die Hypothese stimmt, muss die Kurve hier eine GERADE sein.
plt.semilogy(depths, avg_waits, 'bo-', label='Gemessene Wartezeit (Simulation)', linewidth=2, markersize=8)
plt.semilogy(depths, theoretical_curve, 'r--', label='Theorie: 2^(R-1)', linewidth=2)

plt.title('RTD-Analyse: Wie lange muss man auf "Treibstoff" warten?', fontsize=14)
plt.xlabel('Tiefe R (= ν₂(n+1))', fontsize=12)
plt.ylabel('Durchschnittliche Wartezeit (Schritte) [Log Skala]', fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend(fontsize=12)

# Annotation
mid_idx = len(depths) // 2
if mid_idx < len(avg_waits):
    plt.text(depths[mid_idx], avg_waits[mid_idx]*2, 
             "Gerade Linie = Exponentielle Kosten!", 
             fontsize=11, color='green', fontweight='bold')

plt.tight_layout()
plt.savefig('/home/clawdbot/workspace/collatz/data/rtd_analysis.png', dpi=150, bbox_inches='tight')
print("\nPlot gespeichert: data/rtd_analysis.png")

# --- FAZIT ---
print("\n" + "=" * 60)
print("FAZIT:")
print("=" * 60)

# Prüfe ob die Ratio konstant ist (würde exponentielle Skalierung bestätigen)
ratios = [avg / (2**(r-1)) for r, avg in zip(depths, avg_waits)]
ratio_mean = np.mean(ratios)
ratio_std = np.std(ratios)

print(f"\nMittlere Ratio (gemessen / 2^(R-1)): {ratio_mean:.3f} ± {ratio_std:.3f}")

if ratio_std / ratio_mean < 0.3:
    print("✅ Ratio ist relativ konstant → RTD scheint zu halten!")
    print(f"   Wartezeit skaliert wie {ratio_mean:.2f} × 2^(R-1)")
else:
    print("⚠️  Ratio variiert stark → RTD Status unklar")
