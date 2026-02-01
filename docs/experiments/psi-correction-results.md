# ψ-Correction Results (2026-02-01)

Implementation and results of the Poisson correction for the Collatz residue-corrected potential.

## Background

Following GPT 5.2 Pro analysis (`gpt-analysis-B-next.md`), we implemented the ψ-correction:

$$V(n) = \log n + \psi(n \bmod 3^k)$$

The goal: Make the drift uniformly negative across all residue states.

## Implementation

**Script:** `src/compute_psi.py`

**Method:**
1. Generate S trajectories of length t_max
2. Use only late-time transitions (t ≥ t_burn) to avoid non-stationary bias
3. Build empirical transition matrix P̂(x,y)
4. Compute state-dependent drift ĝ(x)
5. Solve Poisson equation: (I - P̂ + 1π̂ᵀ)ψ = ĝ - ḡ
6. Compute corrected drift: d_corr(x) = g(x) + (Pψ)(x) - ψ(x)

## Results

### Run Parameters
| Parameter | Value |
|-----------|-------|
| N (max starting value) | 50,000,000 |
| S (samples) | 500,000 |
| k (mod 3^k) | 8 |
| t_burn | 34 |
| t_max | 50 |
| Total transitions | 8,000,000 |

### Key Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Global drift** | -0.182 | ✅ Negative (as expected) |
| **Max raw drift** | +0.451 | Before correction, some states go "uphill" |
| **Max corrected drift** | +0.180 | ⚠️ Still positive after correction |
| **\|λ₂\|** | 0.973 | Slow mixing (close to 1) |
| **ψ range** | 14.86 | Correction magnitude |

### State Analysis

| Metric | Value |
|--------|-------|
| Total states | 4,374 |
| States with positive corrected drift | **1** |
| π-mass of positive states | **≈ 0** |

**Key finding:** Only 1 out of 4,374 states has positive corrected drift after applying ψ, and this state has negligible stationary probability (practically never visited).

## Interpretation

### What worked:
- The Poisson correction successfully made 99.98% of states (by probability mass) have negative drift
- Global drift remains strongly negative (-0.182)
- The correction magnitude (ψ range ~15) is reasonable

### Open questions:
1. **The single outlier:** Is it statistical noise or structural?
2. **Slow mixing (|λ₂| = 0.973):** Does this affect proof viability?
3. **Sufficient for proof?** Can we proceed with "almost all states" negative?

### Possible next steps:
- Increase samples to reduce noise
- Investigate the outlier state specifically
- Try different k values (k=6, k=7) for comparison
- Consult GPT for interpretation (pending)

## Files

| File | Description |
|------|-------------|
| `src/compute_psi.py` | Main computation script |
| `data/psi_correction/*/summary.json` | Run summaries |
| `data/psi_correction/*/psi.npy` | ψ values per state |
| `data/psi_correction/*/drift_comparison.csv` | Raw vs corrected drift |

## Raw Output (500k run)

```
Computing ψ for k=8, 4374 states
N=50,000,000, S=500,000, t_burn=34, t_max=50
Total transitions: 8,000,000
Global drift: -0.181579
Max raw drift: 0.451180
Min raw drift: -5.099775
|λ₂| = 0.973333
Max corrected drift: 0.179962
Min corrected drift: -0.000808
ψ range: 14.8594

⚠️  Some states still have positive corrected drift
   Worst: 0.179962
   1 states with positive drift (π-mass: 0.0000)
```

---

*Analysis date: 2026-02-01*
*Awaiting GPT interpretation of results*
