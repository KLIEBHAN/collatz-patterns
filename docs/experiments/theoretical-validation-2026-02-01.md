# Theoretical Validation & Stability Lemma — 2026-02-01

Expert theoretical analysis of our Collatz findings.

---

## 1. Validation: Results Consistent with Theory ✅

Three independent confirmations:

### (i) Maximum at -1 mod 3^k — Attractor of Dominant Map

The most frequent event is a=1 (P(a=1) = 1/2). The corresponding affine map:
```
f₁(x) = (3x + 1) / 2  (mod 3^k)
```
has fixed point **x ≡ -1 (mod 3^k)**:
- 2x = 3x + 1 ⟹ x = -1

In 3-adic metric, ×3 is a contraction → -1 is a true attractor for the most frequent branch.

**Conclusion:** Maximum π at -1 is exactly the expected picture.

### (ii) Spearman Correlation ~0.4-0.6 — Plausible, Not Perfect

The correlation with j = v₃(x+1) is moderate because:
- Other frequent branches (a=2, a=3, ...) have their own fixed points
- These redistribute mass via preimages
- The exact π_k is a projection of a 3-adic stationary measure
- Typically **multifractal** — not explained by a single feature

**Conclusion:** ~0.5 correlation is exactly what we'd expect.

### (iii) TV Deviation < 3% — Consistent with Fourier Differences

For any character χ:
```
|μ̂(χ) - π̂(χ)| = |E_μ[χ] - E_π[χ]| ≤ 2·TV(μ, π)
```

Our largest |Δ| ≈ 0.025 implies TV ≈ 2-3% — completely consistent.

**Important caveat:** This bounds the marginal distribution (μ vs π), not automatically the transition kernels (Q vs P). The stability lemma requires kernel-proximity.

---

## 2. Fourier Targets: Why j=7,11 and j=21,33?

### (a) Conjugate Pairs

In cyclic groups, Fourier modes come as pairs j and r-j (complex conjugates).

- **k=3:** φ(27) = 18, and 11 = 18 - 7 ✅
- **k=4:** φ(81) = 54, and 33 = 54 - 21 ✅

These pairs appearing together is a consistency check: the deviation sits in a **real direction** (cosine component).

### (b) k=4 Targets are Lifted k=3 Targets 🔥

**Critical observation:**
```
21 = 3 × 7
33 = 3 × 11
```

In (ℤ/3⁴ℤ)× (order 54), characters with index divisible by 3 are exactly those that **factor through** the reduction mod 3³.

**Translation:** The worst k=4 deviation comes from the k=3 level — it's lifted, not newly generated.

### (c) Proof Implications

This is extremely valuable:
- Don't need to control "all new 3-adic digits"
- Only a few **persistent harmonic modes** matter

When analyzing deterministic dynamics mod 3^k, statements take the form:
```
E[χ(X_t)] is small for all non-trivial χ
```
(Cancellation in exponential sums / characters)

**Our targets are exactly the χ where cancellation is weakest.** This is perfect for proof-directed work.

### (d) Prediction for k=5

**Hypothesis:** The lifted targets will dominate:
```
j = 3 × 21 = 63
j = 3 × 33 = 99
```
(and their conjugates in the order-162 group)

**If confirmed:** Strong evidence for a stably-scaling obstruction (not just sampling noise).

---

## 3. Stability Lemma: Kernel-Proximity ⟹ Negative Corrected Drift

### Notation

- **S:** Finite state space (here: (ℤ/3^k ℤ)×)
- **P:** Ideal Markov kernel (our exact P_k)
- **Q:** "True/empirical" transition dynamics (Markov approximation of deterministic Syracuse)
- **g_P, g_Q:** State-dependent raw drift per step for log n
  ```
  g_R(x) := E_R[Δlog n | X_t = x]  for R ∈ {P, Q}
  ```
- **ψ:** Correction potential
- **V(n) := log n + ψ(n mod 3^k)**

### Lemma Statement

**Assume:** There exist constants δ > 0 and potential ψ such that for ideal kernel P:
```
g_P(x) + (Pψ)(x) - ψ(x) ≤ -δ   ∀x ∈ S     (★)
```

**Define:**
```
ε := sup_{x∈S} TV(Q(x,·), P(x,·))     [row-TV error]
η := ||g_Q - g_P||_∞                   [drift error]
```

**Then:** For all x ∈ S:
```
g_Q(x) + (Qψ)(x) - ψ(x) ≤ -δ + η + 2ε·||ψ||_∞     (†)
```

**Corollary:** If η + 2ε·||ψ||_∞ ≤ δ/2, then:
```
g_Q(x) + (Qψ)(x) - ψ(x) ≤ -δ/2   ∀x     [uniform negative drift under Q]
```

### Proof (one-liner)

(Q-P)ψ(x) is a difference of expectations of the same bounded function under two distributions:
```
|(Q-P)ψ(x)| ≤ ||ψ||_∞ · ||Q(x,·) - P(x,·)||₁ = 2ε·||ψ||_∞
```

### Translation to Collatz

| Symbol | Meaning |
|--------|---------|
| δ | Negative margin in ideal model (\|log(3/4)\| ≈ 0.287) |
| η | How much does real a(n)-distribution (and log(3+1/n)) depend on state |
| ε | How close are real residue transitions to ideal kernel |

**Key insight:** With δ ≈ 0.287 ("large") vs. our percent-level errors, even rough kernel approximation preserves negative drift.

### Block Variant (Often More Realistic)

Since P^k = rank-1, we can use m-step proximity:
```
sup_{x∈S} TV(Q^m(x,·), P^m(x,·)) ≤ ε_m
```

Then for bounded f:
```
||(Q^m - P^m)f||_∞ ≤ 2ε_m · ||f||_∞
```

This controls m-step drift of V. Often easier because P^k(x,·) ≡ π and we can measure ε_k directly against π.

---

## 4. Which Norm? TV vs Operator vs Fourier

### For Stability Lemma: Row-TV / L^∞→L^∞ Operator Norm

Drift is an expectation of a bounded function under the transition distribution. Row-TV is the native norm:
```
ε = sup_x TV(Q(x,·), P(x,·))
```

Equivalently (up to factor 2):
```
||Q-P||_{∞→∞} := sup_{||f||_∞ ≤ 1} ||(Q-P)f||_∞ = sup_x Σ_y |Q(x,y) - P(x,y)|
```

**Why good:** Worst-case control per state — exactly what Foster-Lyapunov style needs.

### For Bridge Proofs (Deterministic ⟹ Ideal): Fourier

Our data shows why: deviation localizes in few frequencies.

Fourier/character bounds are the standard theoretical tools (exponential sums).

**But:** Pure sup-Fourier norm max_{χ≠1} |μ̂(χ) - π̂(χ)| controls TV poorly as system grows.

**Better approaches:**
- ℓ² Fourier bound over all characters → TV via Cauchy-Schwarz
- Direct bound on concrete target characters (empirically others are already small)

### Best Practice: Two-Stage

1. **Proof/Analysis level:** Control Fourier targets χ₇, χ₁₁ (and their lifts)
2. **Stability/Drift level:** Translate to row-TV (then (†) applies directly)

---

## 5. Next Steps: From Measurement to Lemma-Machine

We now have:
- π structure understood (max at -1, v₃(x+1) relevant)
- μ vs π very close in TV
- Concrete Fourier targets that are "lift-stable" across k

### Proof-Directed Engineering

**Step 1:** Measure kernel error (not just marginal)
```
ε := sup_x TV(Q(x,·), P(x,·))
```
or
```
ε_k := sup_x TV(Q^k(x,·), π)
```

**Step 2:** Measure conditional Fourier targets
```
Q̂_x(χ) := E[χ(X_{t+1}) | X_t = x]
```
or for k steps.

**Success criterion:** If these conditional targets are small (especially for j=7/11 family), we have exactly the bridge the stability lemma needs.

---

## 6. Summary: Where We Stand

| Component | Status |
|-----------|--------|
| π structure (max at -1) | ✅ Verified & explained |
| Marginal TV < 3% | ✅ Empirically confirmed |
| Fourier targets identified | ✅ j=7,11 and lifts |
| Lift-stability hypothesis | 🔄 Needs k=5 test |
| Stability lemma formulated | ✅ Ready to apply |
| Kernel error measurement | ⏳ Next step |
| Conditional Fourier targets | ⏳ Next step |

**The Bridge:**
> "At this point, measurement can become a lemma-machine."

---

## References

- Tao (2019): [Almost all Collatz orbits attain almost bounded values](https://arxiv.org/abs/1909.03562)
- Hutchinson measures in IFS theory
- Foster-Lyapunov drift conditions

---

*Analysis: 2026-02-01*
*Source: Expert theoretical review of our empirical findings*
