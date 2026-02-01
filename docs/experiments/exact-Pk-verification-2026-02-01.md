# Exact P_k Model Verification

**Date:** 2026-02-01  
**Status:** ✅ Verified

## Summary

We implemented and verified the exact rational P_k model for the idealized Syracuse dynamics mod 3^k.

## Model Definition

**State space:** S_k = (ℤ/3^k ℤ)^× = {x ∈ {1,...,3^k-1} : 3 ∤ x}

**Size:** |S_k| = φ(3^k) = 2·3^{k-1}

**Dynamics:** X_{t+1} ≡ (3X_t + 1) · 2^{-A} (mod 3^k)

where A ~ Geometric(1/2), i.e., P(A=m) = 2^{-m} for m ≥ 1.

## Key Insight: Finite Collapse

The infinite sum collapses to finite because 2 has finite multiplicative order mod 3^k:

**r = ord_{3^k}(2) = φ(3^k) = 2·3^{k-1}**

So 2^r ≡ 1 (mod 3^k) and we can group terms:

**w_m = P(A ≡ m mod r) = 2^{r-m} / (2^r - 1)** for m = 1,...,r

The transition matrix becomes:

**P(x,y) = Σ_{m=1}^{r} w_m · 𝟙{y = (3x+1)·2^{-m} mod 3^k}**

## Implementation

**File:** `src/exact_Pk.py`

Uses SymPy for exact rational arithmetic. Key functions:
- `build_exact_P_k(k)` — constructs P, π, states
- `verify_Pk_is_rank1(P, pi, k)` — checks P^k = Π
- `poisson_solve_finite_sum(P, pi, g, k)` — solves Poisson equation

## Results

### Verification Table

| k | M = 3^k | |S_k| | r | P^k = Π | Eigenvalues | π uniform? |
|---|---------|------|-----|---------|-------------|------------|
| 2 | 9 | 6 | 6 | ✅ | {1:1, 0:5} | ❌ |
| 3 | 27 | 18 | 18 | ✅ | {1:1, 0:17} | ❌ |
| 4 | 81 | 54 | 54 | ✅ | {1:1, 0:53} | ❌ |

### P^k Rank-1 Property

**Theorem (Coupling):** In this model, P^k is exactly the rank-1 projection onto the stationary distribution.

**Proof sketch:** Couple two chains X_t, X'_t with identical noise A_t. Then:
- X_{t+1} - X'_{t+1} ≡ 3(X_t - X'_t) · U_{t+1} (mod 3^k)
- After k steps: X_k - X'_k ≡ 3^k · (...) ≡ 0 (mod 3^k)

So chains coalesce in exactly k steps regardless of starting points. □

### Stationary Distribution π

**π is NOT uniform!** This was computed via LU-solve of (P^T - I)π = 0.

| k | π_min | π_max | Ratio |
|---|-------|-------|-------|
| 2 | 0.032 | 0.349 | 10.9× |
| 3 | 0.006 | 0.178 | 29.2× |
| 4 | 0.002 | 0.090 | 50.3× |

The variance grows with k — some residues are visited much more frequently!

### Drift

**E[A] = 2** (geometric expectation, preserved under collapse)

**Drift = log(3) - E[A]·log(2) = log(3/4) ≈ -0.2877**

This is constant across all states (in the idealized model).

### Poisson Equation

The equation (I - P)ψ = g - ḡ has an exact finite-sum solution:

**ψ = Σ_{t=0}^{k-1} P^t (g - ḡ)**

This works because P^k b = Π b = 0 for any mean-zero b.

## Comparison with Empirical Results

Our empirical P̂_k (from Syracuse sampling) showed:
- |λ₂| ≈ 0.973 (slow mixing)
- Variable drift across states
- ψ-correction needed

The ideal model has |λ₂| = 0 (instant mixing after k steps), constant drift, and trivial ψ.

**The gap between ideal and real is the key to a proof.**

## Next Steps

1. **Analyze π structure:** Which residues are high/low probability? Why?
2. **Bridge to reality:** Define ||P̂ - P|| and bound it
3. **Extend to k=5,6:** Verify structure holds at larger scales
4. **Compare empirical π̂ with theoretical π**

## Code Output

```
============================================================
k = 4, M = 3^4 = 81
============================================================
States: 54 (= φ(3^4) = 2·3^3)
Order r = ord_M(2) = 54
π is stationary: True
π is uniform: False
  π range: [0.001789, 0.089735]
P^4 = Π (rank-1): True

Drift analysis:
  E[A] (collapsed) = 2.000000
  Theoretical drift = log(3) - E[A]*log(2) = -0.287682
  log(3/4) = -0.287682
```

## References

- GPT analysis: `gpt-exact-Pk-model.md`
- Critical review: `critical-review-forced-start.md`
- Theory: `../theory.md`
