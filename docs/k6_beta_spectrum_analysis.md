# k=6 β-Spectrum Analysis Results

**Date:** 2026-02-01  
**Author:** clawdbot

## Summary

Analysis of the k=6 Fourier decomposition into coarse (lift) and within-lift (β) components.

## Key Results

### 1. Energy Split
- **Coarse (inherited from k=5):** 26.1%
- **Within-lift (new digit):** 73.9%
- → **Within-lift dominates**, consistent with k=5 findings

### 2. Top Fourier Modes (Direct Analysis)
From `k6_fourier_results.json`:

| Rank | j | Type | |Δ̂(j)| |
|------|---|------|--------|
| 1 | 401 | NEW-DIGIT | 0.0391 |
| 2 | 85 | NEW-DIGIT | 0.0391 |
| 3 | 237 | LIFT (3×79) | 0.0382 |
| 4 | 249 | LIFT (3×83) | 0.0382 |
| 5 | 337 | NEW-DIGIT | 0.0362 |

### 3. GPT's Decode
- j=85 = 3×28 + 1 → base frequency m=28, kernel twist r=1
- j=401 = 3×133 + 2 → base frequency m=133, kernel twist r=2
- 28 + 133 = 161 = φ(3⁵) - 1 (conjugate relationship)

### 4. β-Spectrum vs Full Fourier

**Critical Finding:** The relationship Δ̂(j) ≠ const · FT[β_r](m)

The ratio |Δ̂(j)| / |FT[β_r](m)| varies significantly:
- Mean: 1.30
- Std: 0.96
- Range: 0.10 to 5.04

This explains why:
- j=85/401 are top in full Fourier (|Δ̂| = 0.039)
- But m=28/133 are NOT top in β-spectrum (|FT[β]| = 0.012/0.010)
- The ratio factor (~3-4x) amplifies them in the full Fourier

### 5. Top Contributors to β₁(b)

| Rank | b | |β₁(b)| | Notes |
|------|---|--------|-------|
| 1 | **1** | 0.00681 | **a=2 fixed point!** |
| 2 | 17 | 0.00523 | |
| 3 | 5 | 0.00475 | |
| 4 | 13 | 0.00408 | close to 1 (mod 27) |
| ... | 242 | ... | Rank #36 (≡ -1 mod 243) |

**Confirmed:** b=1 (the fixed point of the a=2 branch x=(3x+1)/4) is the #1 contributor!

### 6. Correlation with v₃(b-1)

| v₃(b-1) | Count | Mean |β₁| | Max |β₁| |
|---------|-------|----------|---------|
| b=1 | 1 | 0.00681 | 0.00681 |
| 0 | 81 | 0.00087 | 0.00523 |
| 1 | 54 | 0.00053 | 0.00408 |
| 2 | 18 | 0.00049 | 0.00200 |
| 3 | 6 | 0.00050 | 0.00072 |

b=1 is a massive outlier, confirming dynamical significance.

## Interpretation

1. **GPT's high-level picture is correct:**
   - Within-lift (new-digit) modes dominate
   - j=85/401 correspond to (m=28, r=1) and (m=133, r=2)
   - The 237/249 modes are lifts of k=5's 79/83

2. **The β-spectrum doesn't directly predict rankings:**
   - The transformation from β_r(b) to Δ̂(j) involves non-trivial factors
   - Can't simply look at |FT[β_r](m)| to predict |Δ̂(3m+r)|

3. **b=1 being top contributor is dynamically meaningful:**
   - It's the fixed point of the a=2 branch
   - Natural "resonance site" for systematic deviations

## Next Steps

1. **Understand the ratio factor:** Why does the transformation amplify m=28/133?
2. **Theoretical attack:** Can we explain why b=1 dominates β₁?
3. **k=7 prediction:** Lifts of 85/401 should appear at 3×85=255, 3×401=1203

## Files

- `data/beta_spectrum_k6.json` - Full numerical results
- `src/beta_spectrum_k6.py` - Analysis script
- `src/verify_fourier_relationship.py` - Ratio verification
