# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture using Markov chain methods and Fourier analysis, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

## Current Status (2026-02-01)

### 🔥 MAJOR DISCOVERY: Absorption Contamination Removed

**The Problem:** Naive sampling showed P(a=2|b=1) = 0.74 (vs ideal 0.25) — seemed like a fundamental obstruction.

**GPT's Insight:** This is **absorption contamination**, not a 3-adic obstruction!
- ~65% of b=1 visits come from the literal absorbing state n=1
- Mixture model perfectly predicts the observed distribution

**Solution:** Killed/regenerative sampling — stop counting when n ≤ B

### 📊 B-Sweep Analysis (Latest)

The boundary threshold B dramatically affects results:

| B | TV Distance | Top-2 Modes | Type | Notes |
|---|-------------|-------------|------|-------|
| 10 | 9.85% | 401, 85 | NEW | Heavy contamination |
| 100 | 3.26% | 301, 185 | NEW | |
| 1000 | 2.19% | 273, 213 | **LIFT** | LIFTs return! |
| 10000 | 1.93% | 387, 99 | **LIFT** | |
| 100000 | 1.91% | 341, 145 | NEW | TV stabilizes |

**Key Findings:**
- TV converges to **~1.9%** (the "true" 3-adic obstruction?)
- Spectrum is NOT stable — top modes change with B
- LIFT modes return at intermediate B (1000-10000)
- P(a=2|b=1) normalizes: 0.74 → **0.23** (near ideal 0.25)
- b=1 drops from rank #1 to **#125** in β-spectrum!

### ✅ Verified Results

| Finding | Status |
|---------|--------|
| Absorption contamination identified | ✅ Confirmed |
| Killed sampling removes artifacts | ✅ TV drops 5× |
| Twist formula (exponent coords) | ✅ Exact (error ~10⁻¹⁷) |
| Energy split: 25% coarse, 75% within-lift | ✅ Verified |
| Lift-index bias dominates (not a-value bias) | ✅ New finding |

### ⚠️ Open Issues

1. **Spectrum instability:** Top modes depend on B choice
2. **Twist implementation bug:** Additive vs multiplicative kernel coordinates
3. **Interpretation pending:** What does ~1.9% TV mean for proof?

## Project Structure

```
collatz/
├── README.md
├── src/
│   ├── killed_regenerative_sampling.py  # 🔥 Decontaminated sampling
│   ├── b_sweep_analysis.py              # 🔥 Boundary threshold analysis
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
        ├── gpt-killed-analysis-2026-02-01.md   # GPT interpretation
        ├── gpt-b1-analysis-response-2026-02-01.md
        └── [more GPT analyses]
```

## Key Theoretical Framework

### The j = 3m + r Decomposition

For character index j at level k:
- **r = j mod 3**: kernel twist (r=0: LIFT, r=1,2: NEW-DIGIT)
- **m = (j-r)/3**: base frequency on G_{k-1}

### The β-Spectrum

Within-lift bias functions capture how mass splits among the 3 lifts of each base class:
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

## Proof Roadmap

### Completed ✅
1. Exact P_k model with rational arithmetic
2. π structure (Hutchinson measure)
3. Fourier analysis k=3 through k=7
4. Absorption contamination identified and removed
5. Twist formula verified in exponent coordinates
6. Energy decomposition: ~25% coarse, ~75% within-lift

### In Progress 🔄
1. Understanding B-sweep instability
2. Fixing twist implementation (additive vs multiplicative coords)
3. Interpreting converged TV (~1.9%)

### Open Questions ❓
1. At what B do we see "true" bulk behavior?
2. What causes LIFT/NEW oscillation with B?
3. Is 1.9% TV theoretically predictable?
4. How to translate to proof-theoretic bounds?

## Quick Start

```bash
cd collatz
python -m venv .venv
source .venv/bin/activate
pip install numpy scipy sympy matplotlib

# Run B-sweep analysis
python src/b_sweep_analysis.py

# Verify no-lift claim
python src/verify_no_lift_claim.py

# β top contributors under killed sampling
python src/beta_top_contributors_killed.py

# Twist formula unit test
python src/twist_unit_test.py
```

## Documentation

| Document | Description |
|----------|-------------|
| [findings.md](docs/findings.md) | Complete chronological discoveries |
| [theory.md](docs/theory.md) | Mathematical framework |
| [GPT Killed Analysis](docs/experiments/gpt-killed-analysis-2026-02-01.md) | Interpretation of decontaminated results |
| [GPT b=1 Analysis](docs/experiments/gpt-b1-analysis-response-2026-02-01.md) | Absorption contamination explanation |

## Links

- [GitHub Repository](https://github.com/KLIEBHAN/collatz-patterns)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [Tao's "Almost All" Paper](https://arxiv.org/abs/1909.03562)

---
*Project started: 2026-01-31*  
*Latest update: 2026-02-01 — B-sweep analysis, killed sampling verified, twist formula exact*
