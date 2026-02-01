# Collatz Findings & Observations

## 2026-01-31: Initial Analysis (10M)

### Key Metrics
- Range: 1 to 10,000,000
- Runtime: 27 seconds (Python with memoization)
- Avg Stopping Time: 155.27 steps
- Max Stopping Time: 685 steps

### Top Record Holders
| n | Steps | Notes |
|---|-------|-------|
| 8,400,511 | 685 | Current champion in range |
| 8,865,705 | 667 | |
| 6,649,279 | 664 | |
| 9,973,919 | 662 | |
| 6,674,175 | 620 | |

### Extreme Peak Discovery
**n = 77,671** reaches a peak of **1,570,824,736** (1.57 billion)

This is 20,224× the starting value! A small 5-digit number explodes to over 1.5 billion before collapsing back to 1.

Other high-ratio numbers:
- 60,975 → peak 593M (9,730×)
- 69,535 → peak 593M (8,532×)
- 65,307 → peak 522M (7,990×)

**Observation:** Several numbers converge to the same peak (593,279,152). This suggests common "attractor" values in the trajectories.

### Pattern: 2^k - 1 (Mersenne-like)
```
k=5:  31 → 106 steps
k=11: 2,047 → 156 steps
k=17: 131,071 → 224 steps
k=23: 8,388,607 → 473 steps
```

**Observation:** Not monotonic! k=7 (127) only takes 46 steps, while k=5 (31) takes 106. The relationship between k and stopping time is complex.

### Pattern: 3^k
Powers of 3 don't show a clear pattern in stopping times:
- 3^3 = 27 → 111 steps (high!)
- 3^4 = 81 → 22 steps (low!)
- 3^10 = 59,049 → 135 steps

**Observation:** 27 has an unusually long sequence for its size. Related to its binary representation (11011)?

### Stopping Time Distribution
Most common stopping times:
- 119 steps: 1.09%
- 124 steps: 1.06%
- 150 steps: 1.05%

The distribution is surprisingly flat - no single value dominates significantly.

---

## 2026-01-31: Extended Analysis (100K)

### Binary Correlation: CONFIRMED ✅
More 1-bits in binary representation → longer sequences:

| 1-bits | Avg Steps | Max |
|--------|-----------|-----|
| 1 | 8.0 | 16 |
| 5 | 93.4 | 280 |
| 10 | 115.8 | 350 |
| 15 | 164.1 | 288 |

**Key Insight:** Bit density (ratio of 1s to total bits) strongly correlates with stopping time.

### Residue Class Pattern: FOUND ✅
Numbers behave differently by residue class mod 12:

| Class | Avg Steps |
|-------|-----------|
| n ≡ 0,4,8 (mod 12) | ~96 |
| n ≡ 3,7,11 (mod 12) | ~120 |

**Difference:** ~25% longer for odd residues that are ≡ 3 (mod 4)!

**Hypothesis:** Numbers ≡ 3 (mod 4) always go UP on the first step (3n+1), while others may go down. This initial "boost" cascades into longer sequences.

### Prime Factor Anti-Correlation: DISCOVERED ✅
More prime factors (with multiplicity) → SHORTER sequences:

| Ω(n) | Avg Steps |
|------|-----------|
| 1 (primes) | 104.1 |
| 5 | 96.6 |
| 10 | 65.6 |

**Hypothesis:** Highly composite numbers have more factors of 2, leading to more immediate halvings and faster collapse.

### Champion Small Numbers
Relative to their bit-length, these are exceptionally long:
- **n=27:** 111 steps, ratio 23.3× (5 bits) — THE CHAMPION
- **n=31:** 106 steps, ratio 21.4× (5 bits)
- **n=41:** 109 steps, ratio 20.3× (6 bits)

27 = 3³ is particularly interesting - pure power of 3, binary = 11011.

---

## Research Directions

### Completed
- ✅ Binary analysis — confirmed correlation with bit density
- ✅ Residue classes — found pattern in mod 12 classes  
- ✅ Prime factor correlation — anti-correlation discovered

### Open
- ⬜ Attractor values — why do multiple numbers reach same peak (593,279,152)?
- ⬜ Graph structure — model Collatz as directed graph
- ⬜ Powers of 3 — why is 27 = 3³ so extreme?
- ⬜ Binary patterns — specific bit patterns that predict long sequences?
- ⬜ Closed-form approximation — can we estimate stopping time from n?

---

## 2026-02-01: Markov Analysis & ψ-Correction Critical Review

### Background

Shifted approach from "push N" statistics to **drift/mixing/finite-state reduction** using the accelerated odd map (Syracuse): T(n) = (3n+1)/2^{a(n)} where a(n) = v₂(3n+1).

Analysis up to 50M with state reduction mod 3^8 = 6561.

### The Outlier Problem

During ψ-correction analysis, state **6397** showed anomalous behavior:
- Positive corrected drift: **+0.180** (all others negative)
- Zero visits in time window t=34..50
- 98.5% of visits occurred at t < 34

### Resolution: Poisson Artifact ✅

**Root cause:** The "+0.180" was a **data artifact**, not structural:
- 0-visit states have undefined rows in transition matrix P̂
- Poisson solver produces arbitrary values for empty rows
- State with maximum drift being a zero-visit state = textbook artifact

### Forced-Start Validation

Applied **Forced-Start methodology** to directly sample state 6397:
- Sample n ≡ 6397 (mod 6561) with random large quotients
- Observed a(n) distribution: ~49.8% a=1, ~25.3% a=2 (geometric ✅)
- Measured g(6397) = **strongly negative** (consistent with other states)

### Critical Review Findings (ChatGPT 5.2 Pro, 22m analysis)

**Methodology: ✅ Correct**
- Forced-Start is valid because 6561 = 3^8 is odd → bijection mod 2^m preserved
- Geometric a(n) distribution confirms no 2-adic bias

**Status: Strong Evidence, Not Proof**
- ψ-correction empirically validated
- All states now show negative corrected drift
- BUT: P̂, ĝ, ψ are estimated, not exact
- Missing: Why can deterministic Syracuse be approximated by finite Markov reduction?

### Roadmap to Rigorous Proof

1. **Level 1 (Achievable):** Build exact P_k with P(a=m) = 2^(-m), prove drift lemma
2. **Level 2 (Difficult):** Control model-to-reality gap (Fourier methods)
3. **Level 3 (Achievable if L2 done):** Drift + concentration → descent proof

### Recommended Next Steps

1. Extend Forced-Start to all 1784 low-count states (N_s < 200)
2. Use large BigInt starts (256-bit) for long-horizon sampling
3. Build exact rational P_k model as proof object

**Full documentation:** `docs/experiments/critical-review-forced-start.md`

---

## Conjectures (Unproven)

1. **Bit Density Conjecture:** For numbers of equal bit-length, stopping time correlates positively with Hamming weight (number of 1-bits).

2. **Residue Cascade Conjecture:** Numbers ≡ 3 (mod 4) have longer average sequences because 3n+1 is always even, guaranteeing an immediate drop after the initial rise.

3. **Prime Shortcut Conjecture:** Numbers with many small prime factors reach 1 faster because they encounter more "halving shortcuts" through powers of 2.
