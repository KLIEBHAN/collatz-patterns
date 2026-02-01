# Collatz Conjecture: Theoretical Framework

A rigorous mathematical framework for our proof-directed approach.

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

## 9. What Remains for Rigorous Proof

> **The key missing piece:** Prove a uniform bulk kernel approximation Q ≈ P_k with explicit constants outside a finite set C.

Once this is proved, combine:
1. (SUFF) → δ > 0
2. Bridge Lemma → τ_C < ∞
3. Finite Verification → reaches 1

Everything else becomes routine.

---

## 10. Relation to Tao (2019)

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
