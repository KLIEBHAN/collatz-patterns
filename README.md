# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture using Markov chain methods and Fourier analysis, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

---

## 🎯 LATEST BREAKTHROUGH (2026-02-01)

### The "3-adic Obstruction" is Sampling Noise!

We discovered that measured TV distances at high boundary B are **dominated by sampling noise**, not real signal.

**Noise Floor Test at B=100,000:**

| N samples | TV (mean) | TV × √N | Ratio |
|-----------|-----------|---------|-------|
| 100k | 2.54% | 8.03 | — |
| 200k | 1.81% | 8.09 | 1.40× |
| 400k | 1.32% | 8.35 | 1.37× |
| 800k | 0.91% | 8.14 | 1.45× |

**Key observations:**
- TV × √N is **constant** (8.15 ± 0.12, CV = 1.5%)
- Ratios ≈ √2 at each N doubling → **pure 1/√N scaling**
- Using TV² = signal² + noise²/N model:
  - **Estimated true signal: ~0.3%** (essentially zero!)

> **In the large-n bulk, the deterministic Collatz process closely matches the ideal i.i.d. model!**

---

## Current Status

### ✅ Confirmed Findings

| Discovery | Status | Implication |
|-----------|--------|-------------|
| Absorption contamination at b=1 | ✅ Identified & removed | P(a=2\|b=1): 0.74 → 0.23 |
| Killed sampling works | ✅ TV drops 3-5× | True structure revealed |
| Twist formula (exponent coords) | ✅ Exact (error ~10⁻¹⁷) | Math is correct |
| Energy split: 25% coarse, 75% within-lift | ✅ Verified | NEW-DIGIT modes dominate |
| TV at high B is noise | ✅ Scales as 1/√N | Bulk obstruction ~0% |

### 📊 B-Sweep Summary

| B | TV | Top-2 Modes | Interpretation |
|---|-----|-------------|----------------|
| 10 | 9.85% | 401, 85 | Heavy boundary contamination |
| 100 | 3.26% | 301, 185 | Partial decontamination |
| 1000 | 2.19% | 273, 213 | LIFT modes return |
| 10000 | 1.93% | 387, 99 | LIFT modes dominant |
| 100000 | 1.91% | 341, 145 | **Mostly sampling noise!** |

**Key insight:** The Fourier spectrum changes with B (expected), but the magnitude converges. At high B, what remains is statistical noise, not deterministic structure.

### ⚠️ Open Questions

1. **Where is the "hard part"?** If bulk is ~ideal, obstruction must live at small n
2. **Spectrum instability:** Why do top modes change with B? (GPT: expected behavior)
3. **Twist implementation:** Additive vs multiplicative kernel coords need fixing

---

## Project Structure

```
collatz/
├── README.md
├── src/
│   ├── noise_floor_test.py              # 🔥 Proves TV is sampling noise
│   ├── killed_regenerative_sampling.py  # Decontaminated sampling
│   ├── b_sweep_analysis.py              # Boundary threshold analysis  
│   ├── verify_no_lift_claim.py          # Energy split verification
│   ├── beta_top_contributors_killed.py  # β analysis under killed
│   ├── twist_unit_test.py               # Twist formula verification
│   ├── exact_Pk.py                      # Exact P_k model
│   ├── k6_fourier_fast.py               # k=6 Fourier analysis
│   ├── k7_fourier_analysis.py           # k=7 Fourier analysis
│   └── [more analysis scripts]
├── data/                                 # Results (gitignored)
└── docs/
    ├── findings.md                       # Complete chronological log
    ├── theory.md                         # Mathematical framework
    └── experiments/
        ├── gpt-b-sweep-interpretation-2026-02-01.md  # Why spectrum changes with B
        ├── gpt-killed-analysis-2026-02-01.md         # Killed sampling interpretation
        ├── gpt-b1-analysis-response-2026-02-01.md    # Absorption contamination
        └── [more GPT analyses]
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

**After decontamination:** The main bias is **lift-index preference**, not a-value deviation!

### Twist Formula (Verified Exact)

In exponent coordinates t ∈ {0,...,3n-1} where x = 2^t:
```
δ̂(3m+r) = Σ_{u=0}^{n-1} β_r(u) exp(-2πi(3m+r)u/(3n))
```

This identity is exact. Implementation issues are in residue↔exponent coordinate mapping.

### The Absorption Story

**Original observation:** P(a=2|b=1) = 0.74 (vs ideal 0.25)

**Resolution:** This was absorption contamination from the literal n=1 fixed point, not a 3-adic obstruction. Killed sampling removes it completely.

---

## Proof Roadmap

### Completed ✅
1. Exact P_k model with rational arithmetic
2. Fourier analysis k=3 through k=7  
3. Absorption contamination identified and removed
4. Twist formula verified (exponent coordinates)
5. Energy decomposition: ~25% coarse, ~75% within-lift
6. **Noise floor test: bulk TV is sampling noise, not signal**

### Key Insight for Proof

> The deterministic Collatz process, when sampled in the large-n bulk (B ≥ 100,000), shows **no measurable deviation** from the ideal i.i.d. geometric model at the 3-adic level k=6.

This suggests a proof strategy:
- **Bulk:** Essentially ideal — no obstruction
- **Boundary:** Small-n behavior needs separate treatment (finite verification)
- **Bridge:** Show that trajectories spend bounded time in problematic small-n regions

### Open Questions ❓
1. Is the ~0.3% residual signal real or fitting artifact?
2. At what n-scale does non-ideal behavior begin?
3. Can we quantify the "boundary region" that needs finite checking?

---

## Quick Start

```bash
cd collatz
python -m venv .venv
source .venv/bin/activate
pip install numpy scipy sympy matplotlib

# Key experiments:
python src/noise_floor_test.py           # Proves TV is noise
python src/b_sweep_analysis.py           # B threshold analysis
python src/verify_no_lift_claim.py       # Energy split
python src/beta_top_contributors_killed.py  # β analysis
python src/twist_unit_test.py            # Formula verification
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [findings.md](docs/findings.md) | Complete chronological discoveries |
| [theory.md](docs/theory.md) | Mathematical framework |
| [GPT B-Sweep](docs/experiments/gpt-b-sweep-interpretation-2026-02-01.md) | Why spectrum changes with B |
| [GPT Killed Analysis](docs/experiments/gpt-killed-analysis-2026-02-01.md) | Decontaminated results |
| [GPT b=1 Analysis](docs/experiments/gpt-b1-analysis-response-2026-02-01.md) | Absorption contamination |

## Links

- [GitHub Repository](https://github.com/KLIEBHAN/collatz-patterns)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [Tao's "Almost All" Paper](https://arxiv.org/abs/1909.03562)

---

*Project started: 2026-01-31*  
*Latest update: 2026-02-01 — Noise floor test proves bulk TV is sampling noise (~0.3% true signal)*
