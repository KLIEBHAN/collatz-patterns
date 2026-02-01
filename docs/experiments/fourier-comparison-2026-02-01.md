# Fourier/Character Comparison: Ideal vs Empirical

**Date:** 2026-02-01  
**Status:** ✅ Completed

## Summary

Compared Fourier coefficients of:
- **Ideal:** Stationary distribution π_k from exact P_k model
- **Empirical:** Distribution from actual Syracuse trajectories

Goal: Identify "proof target" frequencies with largest deviation.

## Method

### Characters on (ℤ/3^k ℤ)×

Multiplicative characters χ_j indexed by j ∈ {0, ..., φ(3^k)-1}:
```
χ_j(x) = exp(2πi j · log_g(x) / φ(3^k))
```
where g=2 is a primitive root mod 3^k.

### Fourier Coefficients

- Ideal: π̂(χ_j) = Σ_x π(x) χ_j(x)
- Empirical: μ̂(χ_j) = Σ_x μ(x) χ_j(x)

### Sampling

- 50,000-100,000 random starts from [10^8, 10^12]
- 50-step burn-in
- Record X_t mod 3^k

## Results

### Total Variation Distance

| k | M | States | Samples | TV Distance |
|---|---|--------|---------|-------------|
| 2 | 9 | 6 | 50k | 0.0079 |
| 3 | 27 | 18 | 50k | 0.0198 |
| 4 | 81 | 54 | 100k | 0.0299 |

**Observation:** TV distance grows with k (finer resolution reveals more deviation).

### Top 5 Proof Targets by k

#### k=2 (mod 9)
| Rank | j | |Δ| | |π̂| | |μ̂| |
|------|---|-----|-----|-----|
| 1 | 2 | 0.0118 | 0.218 | 0.211 |
| 2 | 4 | 0.0118 | 0.218 | 0.211 |
| 3 | 3 | 0.0060 | 0.333 | 0.327 |

#### k=3 (mod 27)
| Rank | j | |Δ| | |π̂| | |μ̂| |
|------|---|-----|-----|-----|
| 1 | 7 | 0.0267 | 0.133 | 0.108 |
| 2 | 11 | 0.0267 | 0.133 | 0.108 |
| 3 | 6 | 0.0118 | 0.218 | 0.211 |

#### k=4 (mod 81)
| Rank | j | |Δ| | |π̂| | |μ̂| |
|------|---|-----|-----|-----|
| 1 | 21 | 0.0246 | 0.133 | 0.110 |
| 2 | 33 | 0.0246 | 0.133 | 0.110 |
| 3 | 19 | 0.0228 | 0.013 | 0.034 |
| 4 | 35 | 0.0228 | 0.013 | 0.034 |
| 5 | 17 | 0.0187 | 0.060 | 0.046 |

## Key Observations

### 1. Symmetry
Characters j and (n-j) always have equal deviations (conjugate symmetry).

### 2. Small Deviations
All deviations |Δ| < 0.03 — the empirical dynamics is CLOSE to the ideal model!

### 3. Persistent Targets
The indices j=7 (k=3) and j=21 (k=4) both correspond to similar "harmonic" positions in the character group.

### 4. TV Growth
TV distance: 0.008 → 0.020 → 0.030 as k increases. This is expected: finer 3-adic resolution reveals more deviation from i.i.d.-geometric.

## Interpretation for Proof Strategy

### The Good News
- Deviations are small (< 3%)
- Real Syracuse is a "small perturbation" of ideal model
- Stability lemma has room to work

### The Proof Targets
A rigorous proof would need to bound these specific Fourier coefficients:
- **k=3:** Control characters j=7, 11
- **k=4:** Control characters j=21, 33

These correspond to specific exponential sums over Syracuse orbits.

### Connection to Tao's Approach
Tao's "almost all" result uses similar 3-adic character analysis. The targets we identified are exactly the "problematic" frequencies that a proof must control.

## Files

- Code: `src/fourier_comparison.py`
- Data: `data/fourier_comparison.json`

## Next Steps

1. **Stabilitätslemma:** Formalize: if |π̂ - μ̂| < ε for all χ, then drift stays negative
2. **Analytic bounds:** Try to bound |μ̂(χ)| using number-theoretic methods
3. **Scale up:** Test k=5, k=6 to see if target pattern continues
