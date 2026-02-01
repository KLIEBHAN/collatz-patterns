# GPT Analysis: Foster-Lyapunov Framework for Collatz

**Date:** 2026-02-01  
**Thinking Time:** ~10 minutes  
**Topic:** Concrete, paper-ready Foster-Lyapunov framework for accelerated Syracuse dynamics

---

## Summary

GPT provided a complete framework matching our "crystalline / transition / liquid" empirical picture. Key components:

1. **Lyapunov function:** V(n) = log n + ψ(X(n)) where X(n) = n mod 3^k
2. **Drift condition:** E[V(T(n)) - V(n) | F] ≤ -δ for n > B₀
3. **Small set:** C = {n ≤ B₀} (finite, hence petite)
4. **Bridge lemma:** Supermartingale argument → τ_C < ∞ a.s.
5. **Finite verification:** Check all n ≤ B₀ reach 1

---

## The Framework

### 0. Nuance: Deterministic Map vs Foster-Lyapunov

Foster-Lyapunov is for stochastic processes. Syracuse T(n) is deterministic.

**Two ways to introduce randomness:**
1. Random initial condition (log-uniform)
2. Regenerative/killed sampling (our setup)

We use (2): restart from large-n distribution when n_t ≤ B.

### 1. State Space and Bulk/Boundary Split

Fix:
- Modulus depth k ≥ 1, M = 3^k
- Bulk threshold B₀ (empirically ~10³)
- Terminal funnel threshold B_f (empirically ~10)

**Small set:** C := {n ∈ 2Z+1 : 1 ≤ n ≤ B₀}

**Residue state:** X(n) := n mod 3^k ∈ (Z/MZ)×

### 2. The Lyapunov Function

**Recommended:** V(n) = log n + ψ(X(n))

Where ψ: (Z/MZ)× → R is bounded.

**Why:**
- log n matches multiplicative nature of T(n)
- ψ(X) neutralizes residue-dependent drift (Poisson correction)

**Options for ψ:**
- **Option A (simplest):** ψ ≡ 0. Viable if bulk conditional law of a(n) is close to geometric.
- **Option B (robust):** ψ solves Poisson equation on ideal kernel P_k.

### 3. Drift Identity and Bounded Increments

For odd n:

```
V(T(n)) - V(n) = log(T(n)/n) + ψ(X(T(n))) - ψ(X(n))
               = log 3 + log(1 + 1/(3n)) - a(n) log 2 + [ψ terms]
```

**Bounded increase (BI):**
```
V(T(n)) - V(n) ≤ log 2 + 2‖ψ‖_∞
```

Since T(n)/n ≤ 2 always. This is crucial for supermartingale arguments.

### 4. The Kernels

**Ideal kernel P_k:**
- A ~ Geom(1/2) on {1,2,...}, P(A=a) = 2^{-a}
- Y = (3X + 1) · 2^{-A} (mod M)
- Bulk log drift: ḡ = log 3 - 2 log 2 = log(3/4) < 0

**Empirical kernel Q_{k,B₀}:**
- Conditional distribution of X(T(n)) given X(n) = x in bulk ensemble n > B₀

### 5. The Drift Condition

**Drift condition (D1):**
```
E[V(n_{t+1}) - V(n_t) | F_t] ≤ -δ  on {n_t > B₀}
```

Equivalently (D1'):
```
E[V(T(n)) - V(n) | X(n) = x, n > B₀] ≤ -δ  ∀x ∈ S_k
```

### 6. Sufficient Condition (SUFF)

Define defect parameters:
- **Kernel defect:** ε := sup_x TV(Q(x,·), P_k(x,·))
- **Exponent defect:** η := sup_x |E[A | X=x, n>B₀] - 2|

Then (D1') holds if:
```
log(3/4) + η log 2 + 1/(3B₀) + 2ε‖ψ‖_∞ ≤ -δ
```

**Paper takeaway:** Prove uniform bounds on η, ε in bulk, pick B₀ large enough → get explicit δ > 0.

### 7. Bridge Lemma

**Lemma (Supermartingale hitting):**

Assume (D1) with δ > 0 outside C = {n ≤ B₀}, and (BI).

Let τ_C := inf{t ≥ 0 : n_t ≤ B₀}.

Then:
1. P(τ_C < ∞) = 1
2. E[τ_C] ≤ (V(n₀) - inf_{n∈C} V(n)) / δ

**Proof sketch:**
Define M_t := V(n_{t∧τ_C}) + δ(t∧τ_C). By (D1), (M_t) is a supermartingale.
Taking expectations and t→∞ yields E[τ_C] < ∞, hence τ_C < ∞ a.s.

### 8. Finite Verification

**Statement:** Compute for every odd n ≤ B₀ the orbit under T until it hits 1 (or memoized value).

This proves: ∀n ≤ B₀, ∃t: T^t(n) = 1.

### 9. Mapping Empirical Results to Framework

| Phase | Empirical | Framework Role |
|-------|-----------|----------------|
| Crystalline (≤10) | 73% row defects | Inside C, handled by finite verification |
| Transition (~100) | 11% max defects | Inside C (choose B₀ > 100) |
| Liquid (≥1000) | Bulk = Ideal | Justifies small ε, η in (SUFF) |

**Key insight:** Don't demand drift in crystalline phase — put it inside C!

The terminal funnel (61→23→35→53→5) is a *feature* for finite verification, not something to approximate.

### 10. What Remains for Rigorous Proof

> Prove a uniform bulk kernel approximation Q ≈ P_k with explicit constants outside a finite set C, then combine (SUFF) + bridge lemma + finite verification.

Everything else becomes routine once that approximation is proved.

---

## Paper-Ready Proposition

**Proposition (Foster-Lyapunov descent to a finite set).**

Fix k ≥ 1 and B₀ ≥ 1. Let V(n) = log n + ψ(n mod 3^k) with ψ bounded. Assume there exists δ > 0 such that for all odd n > B₀,

```
E[V(T(n)) - V(n) | F] ≤ -δ,
```

and that V(T(n)) - V(n) ≤ K uniformly for some finite K.

Let τ_{B₀} = inf{t : n_t ≤ B₀}.

Then τ_{B₀} < ∞ almost surely and E[τ_{B₀}] ≤ (V(n₀) - inf_{n≤B₀} V(n)) / δ.

If additionally every odd n ≤ B₀ is verified to reach 1 under iteration of T, then n₀ reaches 1 almost surely.

---

## GPT's Closing Question

> If you tell me which exact ensemble you want the "E[·]" to refer to in your writeup (log-uniform start? regenerative stationary measure above B₀?), I can rewrite the drift hypothesis (D1) in the cleanest form for that choice and specify exactly what "uniform bulk kernel approximation" lemma you'd need to make the whole pipeline rigorous.
