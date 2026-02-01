# Update: Killed Sampling Results & Twist Correction Attempt

Following your recommendation, we implemented killed/regenerative sampling. The results are surprising!

## 1. Killed Sampling Implementation

We kill (regenerate) when n ≤ B (B=100), removing absorption contamination.

### k=5 Results

| Metric | Contaminated | Killed |
|--------|--------------|--------|
| TV distance | 5.2% | **1.32%** |
| P(a=2\|b=1) | 0.7391 | **0.2319** |
| b=1 rank in β₁ | #1 | **#2** |

✅ **Confirmed:** P(a=2|b=1) normalized to ~0.23 (near ideal 0.25)!

### k=6 Results — THE SURPRISE

| Metric | Contaminated | Killed |
|--------|--------------|--------|
| TV distance | 8.32% | **2.88%** (2.9× reduction) |
| Top-2 modes | j=401, 85 | **j=149, 337** |
| Top-3-4 | j=237, 249 (LIFT) | j=355, 131 (NEW) |
| Lifts in Top-20 | 4 (20%) | **0 (0%)** |
| NEW-DIGIT in Top-20 | 80% | **100%** |

**The top modes changed completely!**

Full k=6 Killed Top-10:
| Rank | j | |Δ| | j%3 | Type |
|------|---|-----|-----|------|
| 1 | 149 | 0.00984 | 2 | NEW |
| 2 | 337 | 0.00984 | 1 | NEW |
| 3 | 355 | 0.00982 | 1 | NEW |
| 4 | 131 | 0.00982 | 2 | NEW |
| 5 | 467 | 0.00980 | 2 | NEW |
| 6 | 19 | 0.00980 | 1 | NEW |
| 7 | 463 | 0.00891 | 1 | NEW |
| 8 | 23 | 0.00891 | 2 | NEW |
| 9 | 89 | 0.00890 | 2 | NEW |
| 10 | 397 | 0.00890 | 1 | NEW |

**No LIFT modes (j%3==0) in Top-20!**

## 2. New Top Mode Decomposition

The new leaders decode as:
- j=149 = 3×49 + 2 → (m=49, r=2) on G₅
- j=337 = 3×112 + 1 → (m=112, r=1) on G₅

Note: 149 + 337 = 486 = φ(3⁶) — conjugate pair.

Compare to contaminated top modes:
- j=85 = 3×28 + 1 → (m=28, r=1)
- j=401 = 3×133 + 2 → (m=133, r=2)

These are **completely different base frequencies**!

## 3. Twist-Corrected β→Fourier — FAILED

I implemented your suggested correction:
```
Δ̂(3m+r) = (1/3) Σ_q β̂_r(q) τ̂_r(m-q)
```
where τ_r(u) = exp(-2πi r u / (3n))

**Result:**
| Metric | Old (uncorrected) | New (twist-corrected) |
|--------|-------------------|----------------------|
| CV (Coeff. of Variation) | 1.04 | **1.48** |
| Mean ratio | 1.55 | 5.64 |

The correction made things **worse**! The ratio |Δ̂_actual| / |Δ̂_predicted| became more variable, not more constant.

Possible issues:
1. Indexing convention mismatch (discrete log vs residue)
2. Normalization factor
3. Something wrong with τ̂_r computation

## Questions

1. **What's special about m=49 and m=112?**
   - These are the new "true" obstruction frequencies after decontamination
   - m=28 (old top) is now gone — was it purely an absorption artifact?

2. **Why do ALL lifts disappear from Top-20?**
   - In contaminated: 4 LIFT modes in Top-20 (j=237, 249, 381, 105)
   - In killed: 0 LIFT modes
   - Does this mean the "lift-stability" pattern was an artifact?

3. **What went wrong with the twist correction?**
   - The formula you gave:
     ```
     β̂_r^twist(m) = (1/n) Σ_u β_r(u) exp(-2πi m u/n) exp(-2πi r u/(3n))
     ```
   - Should Δ̂(3m+r) ≈ (1/3) β̂_r^twist(m)?
   - Or is there convolution with τ̂_r as well?

4. **Is the true 3-adic obstruction now "solved"?**
   - TV dropped to 2.88% (from 8.32%)
   - But it's still non-zero
   - What's causing the remaining 2.88%?

5. **Next steps?**
   - k=7 with killed sampling?
   - Debug twist formula?
   - Try to bound the remaining TV theoretically?

Looking forward to your analysis!
