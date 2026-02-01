#!/usr/bin/env python3
"""
Refueling Test für Key Lemma (K)
Testet ob kumulative Refuels unter θt + C*log(n) bleiben
"""

import matplotlib.pyplot as plt
import random

def get_fuel(n):
    """
    Berechnet den 'Treibstoff' h(n) = v_2(n+1).
    Das ist die Anzahl der Einsen am Ende der Binärdarstellung.
    """
    if n % 2 == 0:
        return 0  # Sollte bei Collatz-Orbit (nur ungerade) nicht passieren
    m = n + 1
    val = 0
    while m > 0 and m % 2 == 0:
        val += 1
        m //= 2
    return val

def simulate_refuel(start_n, max_steps=10000):
    n = start_n
    t_values = []
    cumulative_refuel = []
    current_refuel_sum = 0
    step = 0
    
    # Initiale Phase überspringen wir für die Statistik (das ist der C*log(n) Term)
    # Wir wollen wissen, ob NACH dem Start "frischer" Sprit generiert wird.
    
    while n > 1 and step < max_steps:
        # 1. Bestimme aktuellen Treibstoff und Schritt-Typ
        # Collatz Schritt auf ungeradem n: (3n+1) / 2^a
        temp = 3 * n + 1
        a = 0
        while temp % 2 == 0:
            a += 1
            temp //= 2
        next_n = temp
        
        # LOGIK VON PERSON 2:
        # Ein "Refuel Event" passiert nur, wenn wir neu auf einer ungeraden Zahl landen.
        # Wenn wir von n kommen, haben wir a Divisionen gemacht.
        # Wenn a >= 2 war, war es ein "Reset" (Schrumpfung).
        # Dann schauen wir, wie viel Sprit die NEUE Zahl next_n hat.
        
        step += 1
        if a >= 2:
            # Wir sind gelandet. Wie voll ist der Tank von next_n?
            fuel = get_fuel(next_n)
            # Wir zählen nur fuel > 1 als "echten" Gewinn, da h(n)>=1 für alle ungeraden gilt.
            # Person 2 nennt das (K_i - 1).
            effective_refuel = max(0, fuel - 1)
            current_refuel_sum += effective_refuel
        
        t_values.append(step)
        cumulative_refuel.append(current_refuel_sum)
        
        n = next_n
    
    return t_values, cumulative_refuel

# --- KONFIGURATION ---
steps = 3000

# 1. Der Klassiker
t_27, refuel_27 = simulate_refuel(27, steps)

# 2. Der Verschwörer (Startet mit 1000 Einsen)
conspirator = 2**1000 - 1
t_consp, refuel_consp = simulate_refuel(conspirator, steps)

# 3. Der zufällige Riese (1000 Bits)
random.seed(42)  # Reproduzierbar
random_giant = random.getrandbits(1000) | 1  # Sicherstellen, dass ungerade
t_rand, refuel_rand = simulate_refuel(random_giant, steps)

# --- PLOTTING ---
plt.figure(figsize=(12, 7))

# Plotten der Kurven
plt.plot(t_27, refuel_27, label='n=27 (Klassiker)', linewidth=2)
plt.plot(t_consp, refuel_consp, label='n=2^1000 - 1 (Verschwörer)', linestyle='--')
plt.plot(t_rand, refuel_rand, label='Random 1000-bit (Bulk)', alpha=0.7)

# Die KRITISCHE GRENZE (Theta)
# Wenn die Kurve steiler ist als diese Linie, ist Lemma (K) verletzt.
# Ein konservativer Wert für Theta ist log(4/3) / log(2) approx 0.415.
# Das wäre die Grenze, ab der der Drift positiv wird.
theta_limit = 0.415
limit_line = [theta_limit * x for x in range(steps)]
plt.plot(range(steps), limit_line, color='red', linewidth=3, label='KRITISCHE GRENZE (Theta ~ 0.415)')

plt.title('Der "Refueling"-Test: Wie oft tanken die Zahlen nach?', fontsize=14)
plt.xlabel('Anzahl der Schritte t', fontsize=12)
plt.ylabel('Kumulierter nachgetankter Treibstoff (Summe h(n)-1)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.6)

# Speichern statt anzeigen
plt.savefig('/home/clawdbot/workspace/collatz/data/refuel_test.png', dpi=150, bbox_inches='tight')
print("Plot gespeichert: data/refuel_test.png")

# Statistiken ausgeben
print("\n=== STATISTIKEN ===")
if t_27:
    print(f"n=27: {len(t_27)} steps, final refuel sum = {refuel_27[-1]}, ratio = {refuel_27[-1]/len(t_27):.4f}")
if t_consp:
    print(f"Conspirator: {len(t_consp)} steps, final refuel sum = {refuel_consp[-1]}, ratio = {refuel_consp[-1]/len(t_consp):.4f}")
if t_rand:
    print(f"Random: {len(t_rand)} steps, final refuel sum = {refuel_rand[-1]}, ratio = {refuel_rand[-1]/len(t_rand):.4f}")
print(f"\nKritische Grenze: θ = 0.415")
print(f"Wenn ratio > θ, ist (K) verletzt!")
