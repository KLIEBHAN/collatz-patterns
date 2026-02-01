# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture using Markov chain methods and Fourier analysis, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

---

## Latest Finding (2026-02-01)

### Marginal Distribution Matches Ideal in Bulk

At high boundary B (≥100,000), the **marginal** residue distribution mod 3⁶ shows no measurable deviation from the ideal stationary distribution — the measured TV distance is dominated by sampling noise.

**Noise Floor Test at B=100,000:**

| N samples | TV (mean) | TV × √N |
|-----------|-----------|---------|
| 100k | 2.54% | 8.03 |
| 200k | 1.81% | 8.09 |
| 400k | 1.32% | 8.35 |
| 800k | 0.91% | 8.14 |

- TV × √N is constant (8.15 ± 0.12) — matches theoretical prediction √((S-1)/(2π)) ≈ 8.79
- Estimated true signal: **~0.3%** (essentially zero)

### ⚠️ Important Caveat

This is **good news but not a solution**. As GPT analysis clarified:

> "This is excellent news about mixing in one projection, not a global victory parade."

**What we showed:** The marginal law of n mod 3⁶ looks ideal in the bulk.

**What can still hide problems:**
- **Conditional kernels Q(x,·)** — kernel defects even if marginal matches
- **Time correlations** — marginal can be perfect while transitions are structured  
- **Large deviations** — rare "bad blocks" with many small a-values

The Collatz problem likely lives in these harder-to-measure aspects, not in the marginal distribution.

---

## Current Status

### ✅ Confirmed Findings

| Discovery | Status | Implication |
|-----------|--------|-------------|
| Absorption contamination at b=1 | ✅ Identified & removed | P(a=2\|b=1): 0.74 → 0.23 |
| Killed sampling works | ✅ TV drops 3-5× | Reveals decontaminated structure |
| Twist formula (exponent coords) | ✅ Exact (error ~10⁻¹⁷) | Math is correct |
| Energy split: 25% coarse, 75% within-lift | ✅ Verified | NEW-DIGIT modes dominate |
| Marginal TV at high B is noise | ✅ Scales as 1/√N | Marginal looks ideal |

### 📊 B-Sweep Summary

| B | TV | Top-2 Modes | Interpretation |
|---|-----|-------------|----------------|
| 10 | 9.85% | 401, 85 | Heavy boundary contamination |
| 100 | 3.26% | 301, 185 | Partial decontamination |
| 1000 | 2.19% | 273, 213 | LIFT modes return |
| 10000 | 1.93% | 387, 99 | LIFT modes dominant |
| 100000 | ~1.9% | varies | Mostly sampling noise |

**Note:** The spectrum (which modes are "top") changes with B — this is expected. What converges is the magnitude (TV).

### ❓ Open Questions

1. **Where is the real structure?** Need to test smaller B with same noise analysis
2. **Conditional behavior:** Does Q(x,·) also match ideal, or only the marginal?
3. **Scale dependence:** At what n-scale does non-ideal behavior begin?

---

## Proof Roadmap (GPT-suggested)

### The hard part is NOT marginal mixing

Since bulk marginal looks ideal, the proof challenge shifts to:

1. **Bulk equidistribution lemma (conditional)**
   ```
   sup_{x∈S} TV(Q^k(x,·), π) ≤ ε  for large n in state x
   ```

2. **Stability lemma (Foster-Lyapunov)**
   - Show drift stays negative even with small kernel perturbations

3. **Large-deviation / bad-block control**
   - Show rare bad stretches can't prevent eventual descent

### Next Experiments (by ROI)

| Priority | Experiment | Purpose |
|----------|------------|---------|
| A | Noise-scaling at B=10,100,1000 | Map signal(B) curve — where is real structure? |
| B | log(n) stratification | Which n-scales have non-ideal behavior? |
| C | Kernel-level defects (forced-start) | Test conditional mixing, not just marginal |

---

## Project Structure

```
collatz/
├── README.md
├── src/
│   ├── noise_floor_test.py              # Tests if TV is signal or noise
│   ├── killed_regenerative_sampling.py  # Decontaminated sampling
│   ├── b_sweep_analysis.py              # Boundary threshold analysis  
│   ├── verify_no_lift_claim.py          # Energy split verification
│   ├── beta_top_contributors_killed.py  # β analysis under killed
│   ├── twist_unit_test.py               # Twist formula verification
│   ├── exact_Pk.py                      # Exact P_k model
│   └── [more analysis scripts]
├── data/                                 # Results (gitignored)
└── docs/
    ├── findings.md                       # Complete chronological log
    ├── theory.md                         # Mathematical framework
    └── experiments/                      # GPT analyses and experiment docs
```

---

## Key Theoretical Framework

### The j = 3m + r Decomposition

For character index j at level k:
- **r = j mod 3**: kernel twist (r=0: LIFT, r=1,2: NEW-DIGIT)
- **m = (j-r)/3**: base frequency on G_{k-1}

### The β-Spectrum

Within-lift bias functions capture how mass splits among the 3 lifts:
```
β_r(b) = Σ_ℓ ω^{-rℓ} δ(b,ℓ)    where ω = e^{2πi/3}
```

### Twist Formula (Verified Exact)

In exponent coordinates t ∈ {0,...,3n-1} where x = 2^t:
```
δ̂(3m+r) = Σ_{u=0}^{n-1} β_r(u) exp(-2πi(3m+r)u/(3n))
```

### The Absorption Story

Original observation: P(a=2|b=1) = 0.74 (vs ideal 0.25)

Resolution: This was absorption contamination from n=1, not a 3-adic obstruction. Killed sampling (stopping at n ≤ B) removes it.

---

## Quick Start

```bash
cd collatz
python -m venv .venv
source .venv/bin/activate
pip install numpy scipy sympy matplotlib

# Key experiments:
python src/noise_floor_test.py           # Test if TV is noise
python src/b_sweep_analysis.py           # B threshold analysis
python src/verify_no_lift_claim.py       # Energy split
python src/twist_unit_test.py            # Formula verification
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [findings.md](docs/findings.md) | Complete chronological discoveries |
| [theory.md](docs/theory.md) | Mathematical framework |
| [GPT Noise Analysis](docs/experiments/gpt-noise-floor-analysis-2026-02-01.md) | Interpretation of noise floor test |
| [GPT B-Sweep](docs/experiments/gpt-b-sweep-interpretation-2026-02-01.md) | Why spectrum changes with B |

## Links

- [GitHub Repository](https://github.com/KLIEBHAN/collatz-patterns)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [Tao's "Almost All" Paper](https://arxiv.org/abs/1909.03562)

---

*Project started: 2026-01-31*  
*Latest update: 2026-02-01 — Marginal distribution matches ideal in bulk (but conditional behavior untested)*
