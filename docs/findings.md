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

---

## 2026-02-01: Exact P_k Model — Key Findings

### Background

Following GPT's recommendation, we built an **exact rational P_k model** for the idealized Syracuse dynamics mod 3^k with i.i.d. geometric a(n).

**Model:** X_{t+1} ≡ (3X_t + 1) · 2^{-A} (mod 3^k), where P(A=m) = 2^{-m}

### Implementation

Code: `src/exact_Pk.py`

The infinite geometric sum collapses to a finite sum because 2^r ≡ 1 (mod 3^k) where r = φ(3^k) = 2·3^{k-1}.

Transition matrix: P(x,y) = Σ_{m=1}^{r} w_m · 1{y = (3x+1)·2^{-m} mod 3^k}
with weights w_m = 2^{r-m} / (2^r - 1)

### Verified Results ✅

| k | States | P^k = Π (Rank-1) | Eigenvalues | Drift |
|---|--------|------------------|-------------|-------|
| 2 | 6 | ✅ | {1:1, 0:5} | -0.2877 |
| 3 | 18 | ✅ | {1:1, 0:17} | -0.2877 |
| 4 | 54 | ✅ | {1:1, 0:53} | -0.2877 |

**Key structural property:** P^k (not P!) is exactly rank-1, meaning all rows equal π^T.

This follows from the **coupling argument**: For two chains X_t, X'_t with same noise sequence, the difference X_t - X'_t gains a factor of 3 per step (mod 3^k), so after k steps the difference is divisible by 3^k → chains have coalesced.

### Major Discovery: π is NOT Uniform! 🔥

| k | π Range | Factor |
|---|---------|--------|
| 2 | [0.032, 0.349] | 11× |
| 3 | [0.006, 0.178] | 29× |
| 4 | [0.002, 0.090] | 50× |

The stationary distribution has **huge variance** — some residues are visited 50× more often than others!

This was computed via LU-solve of (P^T - I)π = 0 with Σπ = 1.

### Implications

1. **Drift is constant:** All states have g(x) = log(3/4) ≈ -0.2877 ✅
2. **Poisson equation:** Has finite-sum solution ψ = Σ_{t=0}^{k-1} P^t b
3. **Spectral gap:** |λ₂| = 0 exactly (all non-trivial eigenvalues are 0)

### Next Steps

1. Understand π structure: Which residues have high/low mass? Why?
2. Bridge to reality: Compare ideal P_k with empirical P̂_k from Syracuse
3. Quantify gap: ||P̂_k - P_k|| in appropriate norm

**Documentation:** `docs/experiments/gpt-exact-Pk-model.md`

---

## 2026-02-01: Why π is Not Uniform — GPT Deep Analysis (31m)

### The Core Insight

Our P_k model is a **3-adic random affine contraction system**:
```
f_a(x) = (3x + 1) / 2^a
```

In 3-adic metric |3|_3 = 1/3 < 1, so this contracts. The stationary measure π_k is the **Hutchinson measure** projected to mod 3^k — NOT the Haar measure (uniform).

### Why -1 Has Maximum Mass

The most frequent step a=1 (probability 1/2) has fixed point **x = -1**:
- f_1(x) = (3x+1)/2 → fixed point at x = -1
- This makes -1 a true attractor in 3-adic metric

**Result:** Maximum π(x) always at -1 mod 3^k:
- k=2: π(8) ≈ 0.349 (8 ≡ -1 mod 9)
- k=3: π(26) ≈ 0.178 (26 ≡ -1 mod 27)
- k=4: π(80) ≈ 0.090 (80 ≡ -1 mod 81)

**Classification:** j = v_3(x+1) — larger j means closer to -1, higher mass.

### Bridge to Real Syracuse

Deterministically, T^k(n) mod 3^k depends only on the a-block (a_0, ..., a_{k-1}).

**The proof task:** Show that a-blocks in real dynamics are close to i.i.d.-geometric (Tao approach: 3-adic character analysis).

### Next Steps

1. **Stability Lemma:** If ||Q_k - P_k|| < ε, drift stays negative
2. **Fourier Comparison:** Identify frequencies with largest ideal-vs-real gap
3. **Top-5 Proof Targets:** Characters driving the deviation

**Documentation:** `docs/experiments/gpt-pi-structure-analysis-2026-02-01.md`

---

## 2026-02-01: Theoretical Validation & Stability Lemma

### Expert Review: All Results Consistent ✅

Three independent confirmations:

1. **Maximum at -1 mod 3^k** — Expected! The a=1 map f₁(x)=(3x+1)/2 has fixed point x=-1, which is a 3-adic attractor.

2. **Spearman ~0.4-0.6** — Plausible! The measure is multifractal (not explained by single feature).

3. **TV < 3% consistent with Fourier** — The bound |μ̂(χ)-π̂(χ)| ≤ 2·TV(μ,π) matches our data exactly.

### Fourier Targets Decoded 🔥

**Conjugate pairs:** j=7,11 (k=3) are conjugates (11=18-7). Same for j=21,33 (k=4).

**Lift structure:**
```
21 = 3 × 7
33 = 3 × 11
```
The k=4 "worst frequencies" are lifted from k=3 — not newly generated!

**Prediction for k=5:** j=63 (3×21) and j=99 (3×33) should dominate.

### Stability Lemma (Paper-Ready)

If ideal kernel P satisfies:
```
g_P(x) + (Pψ)(x) - ψ(x) ≤ -δ   ∀x
```

Then for Q with row-TV error ε and drift error η:
```
g_Q(x) + (Qψ)(x) - ψ(x) ≤ -δ + η + 2ε·||ψ||_∞
```

With δ ≈ 0.287 (|log(3/4)|) and our small errors → **negative drift preserved under Q**.

### Norm Recommendation

- **Stability/Drift:** Row-TV / L^∞→L^∞ operator norm
- **Bridge proofs:** Fourier (ℓ² over characters, or target specific χ)
- **Best practice:** Fourier targets → TV bound → Drift lemma

### Next Steps: Kernel Error Measurement

1. **Measure kernel error** (not just marginal):
   ```
   ε := sup_x TV(Q(x,·), P(x,·))
   ```

2. **Conditional Fourier targets:**
   ```
   Q̂_x(χ) := E[χ(X_{t+1}) | X_t = x]
   ```

If conditional targets small for j=7/11 family → we have the bridge for the stability lemma.

**Full documentation:** `docs/experiments/theoretical-validation-2026-02-01.md`

---

---

## 2026-02-01: k=6 β-Spectrum Analysis — Verifying GPT's Framework

### Background

GPT explained that j=85/401 at k=6 are not mysterious — they encode:
- **kernel twist** r = j mod 3 (r=1 or r=2 for new-digit modes)
- **base frequency** m = (j-r)/3 on the base group G₅

So j=85 = 3×28 + 1 means (m=28, r=1).

### Implementation

We implemented GPT's suggested β-spectrum analysis (`src/beta_spectrum_k6.py`):
- Compute β₁(b), β₂(b) for each base class b ∈ G₅
- Compute Fourier transforms FT[β_r](m) over G₅
- Compare with direct Fourier Δ̂(j)

### Results

**Energy Split at k=6:**
- Coarse (inherited from k=5): **26.1%**
- Within-lift (β₁ + β₂): **73.9%**

Consistent with k=5 (76% within-lift). Pattern holds!

**Top Contributors to β₁(b):**

| Rank | b | |β₁(b)| | Notes |
|------|---|--------|-------|
| 1 | **1** | 0.00681 | a=2 fixed point! |
| 2 | 17 | 0.00523 | |
| 3 | 5 | 0.00475 | |
| 36 | 242 | ... | ≡ -1 (mod 243) |

**CONFIRMED:** b=1 is the #1 contributor, exactly as GPT predicted!

This is the fixed point of the a=2 branch: x = (3x+1)/4 ⟺ x = 1

### Critical Discovery: β-Spectrum ≠ Direct Fourier Ranking

GPT claimed: Δ̂(3m+r) ∝ FT[β_r](m)

Our verification (`src/verify_fourier_relationship.py`) shows:
- The ratio |Δ̂(j)| / |FT[β_r](m)| varies from **0.1 to 5.0**
- NOT a constant factor!

**Implication:**
- m=28 is only rank #77 in the β₁-spectrum
- But j=85 is rank #1 in full Fourier
- A non-trivial "amplification factor" (~3x for m=28) exists

### Key Insights

1. **GPT's qualitative picture is correct:**
   - Within-lift dominates
   - b=1 is the hotspot (a=2 fixed point)
   - j=85/401 encode (m=28, r=1) and (m=133, r=2)

2. **The quantitative relationship is more complex:**
   - FT[β_r](m) doesn't directly give Δ̂(3m+r) rankings
   - There's a frequency-dependent amplification factor

3. **Physical interpretation:**
   - b=1 being top contributor = systematic deviation near a=2 fixed point
   - The Syracuse dynamics has structure around this dynamical fixed point

### Open Questions

1. What determines the amplification factor?
2. Can we predict which m values get amplified?
3. ~~k=7: Will 255=3×85, 1203=3×401 be top lifts?~~ → **CONFIRMED!**

**Full documentation:** `docs/experiments/gpt-k6-deep-analysis-2026-02-01.md`

---

## 2026-02-01: k=7 Analysis — Lift Predictions Confirmed! ✅

### Predictions vs Results

| Prediction | j | Rank | Status |
|------------|---|------|--------|
| 3×85 | 255 | 9 | ✅ |
| 3×401 | 1203 | 10 | ✅ |
| 3×237 | 711 | 11 | ✅ |
| 3×249 | 747 | 12 | ✅ |

**All 4 predicted lifts in Top-12!**

### New Dominant Modes

Top-2 at k=7: j=929/529 (NEW-DIGIT)
- 929 = 3×309 + 2 → (m=309, r=2) on G_6
- 529 = 3×176 + 1 → (m=176, r=1) on G_6

### Pattern Summary

| k | Top-2 | Type | Previous Lifts |
|---|-------|------|----------------|
| 5 | 79/83 | NEW | — |
| 6 | 85/401 | NEW | 237/249 (3-4) |
| 7 | 929/529 | NEW | 255/1203 (9-10), 711/747 (11-12) |

**Consistent pattern:**
- NEW-DIGIT modes dominate (~80% of top-10)
- Lifts are stable but not dominant
- Each level generates fresh within-lift bias

### Interesting: j=85 Persists at k=7

j=85 appears at rank 13-14 (as itself, not lifted). Since gcd(85,3)=1, it embeds directly into G_7.

**Full documentation:** `docs/experiments/k7-analysis-2026-02-01.md`

---

## 2026-02-01: MAJOR DISCOVERY — Why b=1 Dominates 🔥

### The Smoking Gun

We measured P(a=2|b) — the probability of the a=2 branch given residue class b.

**Result:** P(a=2|b=1) = **0.7391** (ideal: 0.25)

That's **2.96× the ideal probability!**

### Top Deviations from Ideal P(a=2)=0.25

| Rank | b | P(a=2\|b) | Deviation |
|------|---|-----------|-----------|
| 1 | **1** | **0.7391** | **+0.489** |
| 2 | 25 | 0.6218 | +0.372 |
| 3 | 17 | 0.5892 | +0.339 |
| ... | ... | ... | ... |
| — | 242 (≡-1) | 0.2425 | -0.003 |

Note: b=-1 is essentially at the ideal — it's NOT special for a=2.

### The Mechanism

1. **Fixed point:** x = (3x+1)/4 ⟺ **x = 1**
2. When the chain visits b ≡ 1 (mod 3^k), many of these visits come from **actual n = 1**
3. And n=1 stays at 1 via the a=2 branch: (3·1+1)/4 = 1
4. This creates massive over-representation of a=2 at b=1

### Full a-Distribution at b=1

| a | P(a\|b=1) | Ideal | Deviation |
|---|-----------|-------|-----------|
| 1 | 0.1749 | 0.5000 | **-0.325** |
| 2 | **0.7391** | 0.2500 | **+0.489** |
| 3 | 0.0458 | 0.1250 | -0.079 |
| 4 | 0.0176 | 0.0625 | -0.045 |

a=1 is suppressed, a=2 is boosted — because the fixed point dynamics dominates!

### Implication

This completely explains why β₁(b) is largest at b=1:
- The ideal model assumes P(a|b) = geometric
- Reality: P(a=2|b=1) is 3× higher due to fixed point
- This deviation propagates into the within-lift bias function

**The obstruction to proving Collatz is not random — it's the fixed point structure of the a=2 branch!**

### Files

- `src/analyze_b1_dominance.py` — Analysis script
- `data/b1_dominance_analysis.json` — Full results

---

## 2026-02-01: GPT Analysis — b=1 is ABSORPTION CONTAMINATION 🎯

### The Revelation

GPT (17m 57s deep thinking) identified that our b=1 finding is **not a 3-adic obstruction** but rather **absorption contamination**:

> "Your b=1 finding is real and important, but it's best understood as: **'my sampling measure is not quasi-stationary; it contains lots of absorbed time.'**"

### The Mixture Model Proof

Let q = Pr(n=1 | b=1) — probability that a visit to b≡1 is actually from n=1.

**Prediction:**
- P(a=2|b=1) = q×1 + (1-q)×0.25 = 0.25 + 0.75q

**Observed:** P(a=2|b=1) = 0.7391

**Solve:** q = (0.7391 - 0.25) / 0.75 = **0.6521**

**Verify with a=1:**
- Predicted: P(a=1|b=1) = (1-q)×0.5 = 0.1739
- Observed: **0.1749** ← Almost perfect match!

**Conclusion:** ~65% of our b=1 samples are from the literal absorbing state n=1.

### b=25, 17, 49 Explained

These all have elevated P(a=2|b) because:
- 1, 17, 25, 49 ≡ **1 (mod 8)**
- For odd n, a(n)=2 exactly when n ≡ 1 (mod 8)
- This is a **2-adic** boundary effect, not 3-adic!

### The β↔Fourier Non-Proportionality

GPT explained: It's a **missing twist factor** caused by the cyclic extension structure r_k = 3r_{k-1}.

The correct formula involves a twist by the kernel character, which we didn't account for.

### Recommended Next Steps

1. **Killed/Regenerative Sampling:** Remove absorption — stop counting when n ≤ B
2. **Twist-Corrected β→Fourier:** Implement the exact formula with twist factor
3. **Re-run Analysis:** Then TV, β-energy, Fourier targets will show true 3-adic structure
4. **k=8 Only After Decontamination:** Otherwise we just measure absorption artifacts

### Implications for Proof

> "This is not an 'obstruction' to descent. It's the system telling you, loudly, 'I hit the goal state and stopped.'"

The b=1 effect is actually **good news** — it means the true 3-adic mixing obstruction may be smaller than we measured!

**Full GPT response:** `docs/experiments/gpt-b1-analysis-response-2026-02-01.md`

---

## Conjectures (Unproven)

1. **Bit Density Conjecture:** For numbers of equal bit-length, stopping time correlates positively with Hamming weight (number of 1-bits).

2. **Residue Cascade Conjecture:** Numbers ≡ 3 (mod 4) have longer average sequences because 3n+1 is always even, guaranteeing an immediate drop after the initial rise.

3. **Prime Shortcut Conjecture:** Numbers with many small prime factors reach 1 faster because they encounter more "halving shortcuts" through powers of 2.

4. **Lift-Stability Conjecture (PARTIALLY REFUTED):** The worst Fourier deviations at level k+1 are sometimes lifts (×3) of level k targets, but new dominant modes can emerge. Pattern: lifts dominate at even→odd (k=3→k=4), but new modes appear at odd→even (k=4→k=5 gave j=79,83 instead of predicted j=63,99).

---

## 2026-02-01: k=5 Fourier Analysis — Lift-Structure Test

### Hypothesis
Predicted k=5 top targets: j=63 (3×21), j=99 (3×33)

### Result: PARTIALLY REJECTED ❌

**Actual k=5 top targets:** j=79, j=83

| Rank | j | |Δ| | Notes |
|------|---|-----|-------|
| 1-2 | 79,83 | 0.0364 | **NEW** (not lifts) |
| 7-8 | 63,99 | 0.0218 | Predicted lifts |

### Key Finding
- j=79,83 are NOT divisible by 3 → new characters, not inherited
- j=63,99 still significant (#7-8), but not dominant
- Pattern: Lift structure holds at k=3→k=4 but breaks at k=4→k=5

### Implication
The obstruction landscape is richer than simple lifting. New dominant modes can emerge at each level.

**Full analysis:** `docs/experiments/k5-fourier-analysis-2026-02-01.md`
