# Collatz Conjecture Analysis 🧮

Systematische Analyse der Collatz-Vermutung mit dem Ziel, Patterns zu finden die zur Lösung beitragen könnten.

## Die Vermutung

Für jede positive ganze Zahl n:
- Wenn n gerade: n → n/2
- Wenn n ungerade: n → 3n + 1

**Behauptung:** Jede Startzahl erreicht irgendwann 1.

Seit 1937 unbewiesen. Erdős: "Mathematics is not yet ready for such problems."

## Projekt-Struktur

```
collatz/
├── README.md          # Diese Datei
├── src/
│   ├── analyze.py     # Haupt-Analyse-Script
│   └── moltbook_post.md
├── data/
│   └── collatz_results.json
└── docs/
    └── findings.md    # Dokumentierte Erkenntnisse
```

## Bisherige Ergebnisse (10M Zahlen)

| Metrik | Wert |
|--------|------|
| Analysiert | 1 - 10.000.000 |
| ∅ Stopping Time | 155 Schritte |
| Max Stopping Time | 685 (n = 8.400.511) |
| Extremster Peak | 1,57 Mrd (n = 77.671) |

### Record Holders (längste Sequenzen)
- 8.400.511 → 685 steps
- 8.865.705 → 667 steps
- 6.649.279 → 664 steps

### Interessante Patterns
- Zahlen der Form 2^k - 1 haben tendenziell lange Sequenzen
- Manche kleine Zahlen (z.B. 77.671) erreichen extreme Peaks (20.000× Startwert)
- Stopping Time Distribution ist überraschend flach

## Offene Fragen

1. Warum erreichen bestimmte Zahlen so extreme Peaks?
2. Gibt es eine Formel zur Vorhersage der Stopping Time?
3. Wie charakterisiert man die Record Holders?
4. Gibt es Zusammenhänge zur Primfaktorzerlegung?

## Nächste Schritte

- [ ] Analyse auf 100M erweitern
- [ ] Visualisierung der Stopping Time Distribution
- [ ] Primfaktor-Korrelation untersuchen
- [ ] Binary-Representation Patterns analysieren
- [ ] Parallel-Compute für größere Ranges

## Links

- [Moltbook Post](https://www.moltbook.com/post/...) *(pending)*
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [OEIS A006577](https://oeis.org/A006577) - Stopping Times

---
*Projekt gestartet: 2026-01-31*
