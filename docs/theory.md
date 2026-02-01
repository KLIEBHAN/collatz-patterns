# Collatz Conjecture: Theoretical Framework

**A conditional reduction of Collatz to a single No-Conspiracy Lemma.**

This document presents a rigorous Foster-Lyapunov framework that transforms the Collatz conjecture from "does every trajectory reach 1?" to "can arithmetic conspire against descent?"

---

## 1. The Problem

**Collatz Conjecture (1937):** For any positive integer n, repeated application of the Collatz function eventually reaches 1.

**Status:** Unproven. Verified to ~10²⁰. Erdős: "Mathematics is not yet ready for such problems."

---

## 2. The Syracuse Map

We study the **accelerated odd map** (Syracuse function):

$$T(n) = \frac{3n+1}{2^{a(n)}}$$

where $a(n) = ν_2(3n+1)$ is the 2-adic valuation.

**Log-increment:**
$$\Delta \log n = \log T(n) - \log n = \log 3 - a(n) \cdot \log 2$$

**Ideal expectation:** If a(n) ~ Geometric(1/2) with E[a] = 2:
$$\mathbb{E}[\Delta \log n] = \log(3/4) \approx -0.288 < 0$$

---

## 3. The Three-Phase Model

Our empirical finding: Collatz dynamics have distinct phases depending on n.

| Phase | Range | Kernel Defect | Behavior |
|-------|-------|---------------|----------|
| **Crystalline** | n ≤ 10 | ~73% | Deterministic, structured |
| **Transition** | n ~ 100 | ~11% | "Ice melts" |
| **Liquid** | n ≥ 1000 | ~0% (noise) | **Bulk = Ideal** |

**Key insight:** The "Collatz structure" only exists at small n. Bulk behavior is indistinguishable from the ideal stochastic model.

---

## 4. Foster-Lyapunov Framework

The mathematical machinery that converts our empirical findings into a proof strategy.

### 4.1 The Lyapunov Function

$$V(n) = \log n + \psi(X(n))$$

where:
- $X(n) = n \mod 3^k$ (residue state)
- $\psi: (\mathbb{Z}/3^k\mathbb{Z})^× \to \mathbb{R}$ is bounded (Poisson correction)

**Why this form:**
- log n captures the multiplicative nature of T(n)
- ψ(X) neutralizes residue-dependent drift fluctuations

### 4.2 Key Definitions

| Term | Symbol | Definition |
|------|--------|------------|
| **Small Set** | C | {n ≤ B₀} — finite, handled by verification |
| **Kernel Defect** | ε | sup_x TV(Q(x,·), P_k(x,·)) |
| **Exponent Defect** | η | sup_x \|E[a \| X=x] - 2\| |
| **Drift Bound** | δ | Guaranteed descent rate outside C |

### 4.3 The Drift Condition (D1)

For all odd n > B₀:
$$\mathbb{E}[V(T(n)) - V(n) \mid \mathcal{F}] \leq -\delta$$

**Physical meaning:** "Gravity always pulls downward in the bulk."

### 4.4 Sufficient Condition (SUFF)

The drift condition holds if:
$$\log(3/4) + \eta \log 2 + \frac{1}{3B_0} + 2\varepsilon\|\psi\|_\infty \leq -\delta$$

**Our empirical evidence:** In the liquid phase (n > 1000), ε → 0 and η → 0.

### 4.5 Bounded Increments (BI)

$$V(T(n)) - V(n) \leq \log 2 + 2\|\psi\|_\infty$$

Since T(n)/n ≤ 2 always. This bounds "upward jumps."

---

## 5. The Bridge Lemma

The logical connection between bulk (statistics) and boundary (verification).

**Lemma (Supermartingale Hitting):**

If (D1) holds with δ > 0 outside C = {n ≤ B₀}, and (BI) holds, then:

1. $P(\tau_C < \infty) = 1$ (eventually enters C)
2. $\mathbb{E}[\tau_C] \leq \frac{V(n_0) - \inf_{n \in C} V(n)}{\delta}$

where τ_C = inf{t : n_t ≤ B₀}.

**Proof sketch:** Define M_t = V(n_{t∧τ_C}) + δ(t∧τ_C). By (D1), this is a supermartingale. Taking t→∞ yields E[τ_C] < ∞.

**Physical meaning:** "You can't escape gravity forever. Eventually you fall into C."

---

## 6. Finite Verification

Once in C = {n ≤ B₀}, we verify computationally:

**Statement:** For every odd n ≤ B₀, there exists t such that T^t(n) = 1.

This is trivial to check (already done to 10²⁰+) but formally closes the proof.

---

## 7. The Terminal Funnel

The "crystalline" phase isn't random — it's a deterministic chute to 1:

```
190 → 82 → 61 → 23 → 35 → 53 → 5 → ... → 1
```

**Key insight:** The 73% "defect" at small n is actually helpful — it's extra deterministic pull toward 1, not an obstruction.

---

## 8. Complete Proof Structure

```
                    ┌─────────────────────────────┐
                    │  Start: any n₀ > B₀         │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  BULK (n > B₀)              │
                    │  • Drift condition (D1)     │
                    │  • Kernel ≈ Ideal (SUFF)    │
                    │  • Gravity pulls down       │
                    └─────────────┬───────────────┘
                                  │
                                  │ Bridge Lemma: τ_C < ∞ a.s.
                                  ▼
                    ┌─────────────────────────────┐
                    │  SMALL SET C (n ≤ B₀)       │
                    │  • Finite verification      │
                    │  • Terminal funnel          │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  n = 1  ✓                   │
                    └─────────────────────────────┘
```

---

## 9. The Deterministic Wall: What's Really Missing

### The Core Problem

Collatz is **deterministic**. Our framework uses Markov chain theory. This creates a fundamental gap:

| What We Have | What We Need |
|--------------|--------------|
| "ε small under our sampling" | "ε small for EVERY n > B₀" |
| Average-case behavior | Worst-case guarantee |
| Random-like in experiments | No adversarial counterexample |

**This gap IS the Collatz conjecture.**

### The Missing "No Conspiracy" Lemma

A rigorous proof would require something like:

> **Uniform Block-Drift Lemma:** There exist m, k, δ > 0, B₀ such that for EVERY odd n > B₀:
> 
> V(T^m(n)) - V(n) ≤ -δ

This is NOT implied by our empirical findings. It requires proving that no starting integer can produce an infinite chain of "bad blocks" (low a-values).

### Why This Is Hard

For any finite pattern (a₀, ..., a_{m-1}), there typically exist infinitely many integers realizing that pattern. So "no conspiracy" must mean one of:
1. Bad blocks cannot chain forever along any orbit
2. Long bad chains force eventual compensating large valuations

This is a **global, adversarial control problem** — fundamentally different from our statistical measurements.

### The Formal No-Conspiracy Lemma

**Definition (Uniform Block-Drift):**

There exist integers m ≥ 1, k ≥ 1, constants δ > 0, B₀, and a bounded function ψ: S_k → ℝ such that for **every** odd n > B₀:

$$\sum_{i=0}^{m-1} \left( \log \frac{T(T^i(n))}{T^i(n)} + \psi(X_{i+1}) - \psi(X_i) \right) \leq -\delta$$

Equivalently: V(T^m(n)) - V(n) ≤ -δ for all n > B₀.

**Why This Is The Key:**
- If true → Foster-Lyapunov gives deterministic descent
- If false → there exists a "conspiracy" starting integer
- Our empirics suggest true, but proving it is the hard part

### Honest Framework Classification

| Target | Achievability |
|--------|---------------|
| "Almost all n" (Tao-style) | ✅ Plausibly achievable |
| "All n > B₀" | Reduces to No-Conspiracy Lemma |

Our framework is best described as:
> **A conditional proof:** "If No-Conspiracy Lemma holds, then Collatz is true."

---

---

## 10. The Two-Theorem Structure

This is how to properly frame our contribution:

### Theorem A: The Scaffold (Our Contribution) ✅

**Statement:** If the deterministic Syracuse map satisfies the Uniform Block-Drift condition (No-Conspiracy Lemma), then:
1. V(n) = log n + ψ(n mod 3^k) is a valid Lyapunov function
2. Every trajectory eventually enters {n ≤ B₀}
3. Combined with finite verification, every trajectory reaches 1

**Status:** Proven (conditional on the lemma)

### Theorem B: The Foundation (Open Problem) ❓

**Statement:** Prove the Uniform Block-Drift / No-Conspiracy condition.

**Status:** Open. Our empirical evidence suggests it holds, but:
- "Holds on average" ≠ "Holds for every n"
- The gap is exactly the Collatz conjecture
- No known technique bridges this gap

### Why This Framing Matters

This makes the work **scientifically citable**. We're not claiming to prove Collatz. We're claiming:

> "We've transformed Collatz into a precise No-Conspiracy statement, and we have strong empirical evidence that this statement holds."

---

## 11. Relation to Tao (2019)

Tao proved "almost all Collatz orbits attain almost bounded values" using logarithmic density arguments.

**Our contribution:**
- Precise characterization of *where* non-ideal behavior lives (n ≤ 1000)
- Quantification of the phase transition (B ~ 100)
- Explicit proof framework (Foster-Lyapunov)

---

## 11. References

- Lagarias, J.C. "The 3x+1 Problem and its Generalizations" (1985)
- Tao, T. "Almost all orbits of the Collatz map attain almost bounded values" (2019)
- Meyn & Tweedie. "Markov Chains and Stochastic Stability" (2009)

---

## Appendix: Detailed GPT Analyses

- [Foster-Lyapunov Framework](experiments/gpt-foster-lyapunov-framework-2026-02-01.md) — Complete paper-ready setup
- [Terminal Funnel Analysis](experiments/gpt-conditional-defects-2026-02-01.md) — Why x=61 has 73% defect
- [Noise Floor Analysis](experiments/gpt-noise-floor-analysis-2026-02-01.md) — Why bulk TV is sampling noise

---

*Updated: 2026-02-01*
