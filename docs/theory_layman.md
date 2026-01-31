# Das Collatz-Problem: Eine Erklärung für Nicht-Mathematiker 🧮

*Eines der einfachsten ungelösten Probleme der Mathematik — und unser Versuch, es zu knacken.*

---

## Was ist das Collatz-Problem?

Nimm irgendeine positive Zahl und wende diese zwei einfachen Regeln an:

- **Gerade Zahl?** → Halbieren
- **Ungerade Zahl?** → Mal 3, plus 1

Wiederhole das, bis du bei 1 landest.

### Beispiel: Starte mit 7

```
7 ist ungerade  → 3×7+1 = 22
22 ist gerade   → 22÷2 = 11
11 ist ungerade → 3×11+1 = 34
34 ist gerade   → 34÷2 = 17
17 ist ungerade → 3×17+1 = 52
52 ist gerade   → 52÷2 = 26
26 ist gerade   → 26÷2 = 13
13 ist ungerade → 3×13+1 = 40
40 ist gerade   → 40÷2 = 20
20 ist gerade   → 20÷2 = 10
10 ist gerade   → 10÷2 = 5
5 ist ungerade  → 3×5+1 = 16
16 ist gerade   → 16÷2 = 8
8 ist gerade    → 8÷2 = 4
4 ist gerade    → 4÷2 = 2
2 ist gerade    → 2÷2 = 1 ✓
```

**16 Schritte** von 7 nach 1.

### Die große Frage

**Vermutung:** Egal welche Startzahl du nimmst — du landest IMMER bei 1.

Das wurde seit 1937 für alle Zahlen bis etwa 10²⁰ (eine 1 mit 20 Nullen!) überprüft. Niemand hat je eine Ausnahme gefunden. Aber **bewiesen** ist es nicht.

Der berühmte Mathematiker Paul Erdős sagte: *"Die Mathematik ist noch nicht reif für solche Probleme."*

---

## Warum ist das so schwer?

### Das Tauziehen zwischen Wachsen und Schrumpfen

Bei ungeraden Zahlen wird die Zahl größer (×3+1).  
Bei geraden Zahlen wird sie kleiner (÷2).

**Die Hoffnung:** Im Durchschnitt schrumpft die Zahl, weil das Halbieren "stärker" ist als das ×3.

**Das Problem:** Die Schritte sind nicht zufällig! Welche Zahlen du durchläufst, hängt davon ab, wo du gestartet bist. Diese Abhängigkeiten machen einen Beweis extrem schwierig.

### Verrückte Ausreißer

Die Zahl **27** braucht **111 Schritte** und erreicht zwischendurch einen Wert von über 9.000 — obwohl sie selbst nur zweistellig ist!

Die Zahl **77.671** erreicht einen Peak von **1,57 Milliarden** (das 20.000-fache des Startwerts), bevor sie zu 1 kollabiert.

---

## Unser Ansatz: Die Zahlen in Gruppen einteilen

Statt jede Zahl einzeln zu betrachten, sortieren wir sie in "Schubladen" — basierend auf dem Rest bei Division.

### Beispiel: Reste bei Division durch 3

Jede Zahl hat einen Rest von 0, 1 oder 2 wenn man sie durch 3 teilt:
- 7 ÷ 3 = 2 Rest **1** → Schublade "1"
- 22 ÷ 3 = 7 Rest **1** → Schublade "1"
- 11 ÷ 3 = 3 Rest **2** → Schublade "2"

Wir benutzen feinere Schubladen (Rest bei Division durch 3⁸ = 6.561), um die Dynamik besser zu verstehen.

### Was wir herausgefunden haben

Wir haben 2 Millionen Zahlen analysiert und gemessen, wie sich Zahlen in verschiedenen "Schubladen" verhalten:

| Erkenntnis | Was es bedeutet |
|------------|-----------------|
| **Globaler Trend ist negativ** | Im Durchschnitt schrumpfen die Zahlen (gut!) |
| **Manche Schubladen sind "schlecht"** | ~15% der Schubladen haben einen positiven Trend (Zahlen wachsen dort) |
| **Die schlechten Schubladen sind nicht ZU schlecht** | Maximaler positiver Trend ist +0.45, nicht unbegrenzt |

### Die Idee für einen Beweis

1. **Zeige, dass Zahlen schnell zwischen Schubladen wechseln** (sie bleiben nicht in schlechten Schubladen stecken)

2. **Finde eine "Korrektur"** — eine Art Bonus/Malus für jede Schublade, sodass nach Korrektur ALLE Schubladen einen negativen Trend haben

3. **Beweise, dass "Pechsträhnen" selten sind** — Phasen wo viele ungünstige Schritte hintereinander kommen

---

## Unsere Entdeckungen (bisher)

### 🔢 Binärmuster
Zahlen mit vielen Einsen in ihrer Binärdarstellung brauchen länger:
- 1 Eins → ~8 Schritte
- 15 Einsen → ~164 Schritte

### 🎯 Magische Zahl 27
27 = 3³ ist ein "Champion" — extrem lange Sequenz für so eine kleine Zahl. Warum gerade 27? Das verstehen wir noch nicht vollständig.

### ⚡ Hochzusammengesetzte Zahlen sind schnell
Zahlen mit vielen Primfaktoren (wie 12 = 2×2×3) kollabieren schnell — sie haben mehr Gelegenheiten zum Halbieren.

---

## Wie würde ein Beweis aussehen?

```
┌─────────────────────────────────────────┐
│  1. Schubladen-Dynamik verstehen        │
│     ↓                                   │
│  2. Korrektur finden die alles negativ  │
│     macht                               │
│     ↓                                   │
│  3. Zeigen dass Pechsträhnen selten     │
│     ↓                                   │
│  4. Mathematisch beweisen, dass das     │
│     reicht                              │
│     ↓                                   │
│  ✓ Collatz-Vermutung bewiesen!          │
└─────────────────────────────────────────┘
```

Wir sind bei Schritt 1-2 und haben vielversprechende empirische Daten. Der Weg zum vollständigen Beweis ist noch weit, aber wir verstehen das Problem jetzt viel besser.

---

## Warum ist das wichtig?

### Für die Mathematik
Ein Beweis würde neue Techniken entwickeln, die auf andere Probleme anwendbar wären.

### Für Chaos-Theorie
Collatz zeigt, wie einfache Regeln zu komplexem Verhalten führen — ähnlich wie Wetter oder Wirtschaft.

### Für Kryptographie
Ähnliche "schwer vorhersagbare" Funktionen werden für Verschlüsselung genutzt.

### Oder einfach: Es ist ein schönes Rätsel
Seit fast 90 Jahren rätseln Mathematiker daran. Manchmal ist das Grund genug.

---

## Zum Mitmachen

Unser Code ist öffentlich: **[github.com/KLIEBHAN/collatz-patterns](https://github.com/KLIEBHAN/collatz-patterns)**

Du kannst:
- Die Analyse selbst laufen lassen
- Mit größeren Zahlenmengen experimentieren
- Neue Muster suchen
- Visualisierungen erstellen

---

## Zusammenfassung

| Frage | Antwort |
|-------|---------|
| Was ist Collatz? | Ein einfaches Zahlenspiel: gerade → halbieren, ungerade → ×3+1 |
| Was ist die Vermutung? | Jede Startzahl landet irgendwann bei 1 |
| Ist es bewiesen? | Nein, seit 1937 nicht |
| Unser Ansatz? | Zahlen in "Schubladen" einteilen und statistische Muster finden |
| Fortschritt? | Vielversprechende Daten, aber noch kein Beweis |

---

*"Die Mathematik ist nicht reif für solche Probleme"* — aber vielleicht wird sie es bald sein. 🦞

---

*Letzte Aktualisierung: 2026-01-31*
