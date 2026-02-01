# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture using Markov chain methods and Fourier analysis, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

## Current Status (2026-02-01)

### 🔥 MAJOR DISCOVERY: Fixed Point Structure

**The obstruction to proving Collatz is not random — it's the fixed point structure!**

We discovered that b=1 (mod 3^k) has massively elevated P(a=2):

| b | P(a=2\|b) | Ideal | Deviation |
|---|-----------|-------|-----------|
| **1** | **0.7391** | 0.25 | **+0.489** (3× ideal!) |
| 25 | 0.6218 | 0.25 | +0.372 |
| 17 | 0.5892 | 0.25 | +0.339 |
| 242 (≡-1) | 0.2425 | 0.25 | ~0 |

**Why?** The a=2 branch x → (3x+1)/4 has fixed point x=1. Visits to b≡1 often come from actual n=1, which stays at 1 via a=2.

### Fourier Analysis Summary (k=3 through k=7)

| k | φ(3^k) | TV Dist | Top-2 Modes | Type | Pattern |
|---|--------|---------|-------------|------|---------|
| 3 | 18 | 2.0% | 7, 11 | NEW | — |
| 4 | 54 | 3.0% | 21, 33 | LIFT | 3×7, 3×11 |
| 5 | 162 | 5.2% | 79, 83 | NEW | Nyquist-neighbors |
| 6 | 486 | 8.3% | 85, 401 | NEW | (m=28, r=1/2) |
| 7 | 1458 | 11.3% | 929, 529 | NEW | (m=309/176, r=2/1) |

**Key Pattern:**
- NEW-DIGIT modes dominate each level (~80% of top-10)
- Previous top modes become stable lifts (mid-tier ranks)
- Lifts predicted correctly: k=6→k=7 lifts 255/1203, 711/747 all in top-12 ✅

### Energy Decomposition

At each level, discrepancy δ = μ - π decomposes into:
- **Coarse (inherited):** ~25-30%
- **Within-lift (new digit):** ~70-75%

The within-lift component β_r(b) captures how mass splits among lifts. Top contributor: **b=1** (the a=2 fixed point).

## Project Structure

```
collatz/
├── README.md
├── src/
│   ├── exact_Pk.py              # Exact P_k model (rational arithmetic)
│   ├── k6_fourier_fast.py       # k=6 Fourier analysis
│   ├── k7_fourier_analysis.py   # k=7 Fourier analysis
│   ├── beta_spectrum_k6.py      # β-spectrum decomposition
│   ├── analyze_b1_dominance.py  # 🔥 P(a|b) analysis
│   ├── lift_splitting_analysis.py # k=5 lift decomposition
│   └── verify_fourier_relationship.py
├── data/
│   ├── k6_fourier_results.json
│   ├── k7_fourier_results.json
│   ├── beta_spectrum_k6.json
│   └── b1_dominance_analysis.json
└── docs/
    ├── findings.md              # All discoveries (detailed)
    ├── theory.md                # Mathematical framework
    └── experiments/
        ├── gpt-k6-deep-analysis-2026-02-01.md  # GPT's quotient+kernel theory
        ├── k7-analysis-2026-02-01.md
        └── [more experiment docs]
```

## Key Theoretical Framework

### The j = 3m + r Decomposition (GPT's Insight)

For character index j at level k:
- **r = j mod 3**: kernel twist (r=0: lift, r=1,2: new-digit)
- **m = (j-r)/3**: base frequency on G_{k-1}

Example: j=85 at k=6 decodes as:
- 85 = 3×28 + 1 → (m=28, r=1)
- Base frequency m=28 has order 81 in G_5 (deep 3-adic character)

### The β-Spectrum

Within-lift bias functions:
```
β_1(b) = Σ_ℓ ω^ℓ (μ(b,ℓ) - π(b,ℓ))
β_2(b) = Σ_ℓ ω^{2ℓ} (μ(b,ℓ) - π(b,ℓ))
```

The Fourier spectrum of β_r captures which base frequencies dominate.

### The Fixed Point Mechanism — RESOLVED ✅

**UPDATE (2026-02-01):** GPT analysis revealed this is **absorption contamination**, not a 3-adic obstruction!

The huge P(a=2|b=1) = 0.74 is explained by a **mixture model**:
- ~65% of visits to b≡1 come from actual n=1 (absorbing state)
- Predicted: P(a=2|b=1) = 0.25 + 0.75×0.65 = 0.74 ✓

**The b=25, 17, 49 pattern:** All ≡ 1 (mod 8) — this is a **2-adic** effect!

**Implication:** The true 3-adic mixing obstruction may be smaller than measured. Need "killed/regenerative" sampling to separate absorption from mixing.

## Proof Roadmap

### Completed ✅
1. Exact P_k model with rational arithmetic
2. π structure (Hutchinson measure, -1 is attractor)
3. Fourier comparison k=3 through k=7
4. β-spectrum decomposition (coarse vs within-lift)
5. b=1 dominance explained via P(a=2|b) measurement
6. Lift prediction verified (k=6 → k=7)

### Open Questions
1. Why does the ratio |Δ̂(j)|/|FT[β_r](m)| vary (0.1 to 5.0)?
2. Can we theoretically bound P(a=2|b=1) deviation?
3. How to translate fixed-point structure into proof-theoretic bounds?

### The Bridge to Proof
> Show that deviations from ideal i.i.d. geometric behavior are bounded,  
> and that the fixed-point structure at b=1 doesn't prevent global descent.

## Quick Start

```bash
cd collatz
python -m venv .venv
source .venv/bin/activate
pip install numpy scipy sympy matplotlib

# Run k=7 Fourier analysis
python src/k7_fourier_analysis.py

# Analyze b=1 dominance
python src/analyze_b1_dominance.py

# β-spectrum decomposition
python src/beta_spectrum_k6.py
```

## Documentation

| Document | Description |
|----------|-------------|
| [findings.md](docs/findings.md) | Complete chronological discoveries |
| [theory.md](docs/theory.md) | Mathematical framework |
| [GPT k=6 Analysis](docs/experiments/gpt-k6-deep-analysis-2026-02-01.md) | Quotient+kernel decomposition |
| [k=7 Results](docs/experiments/k7-analysis-2026-02-01.md) | Lift predictions verified |

## Links

- [GitHub Repository](https://github.com/KLIEBHAN/collatz-patterns)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [Tao's "Almost All" Paper](https://arxiv.org/abs/1909.03562)

---
*Project started: 2026-01-31*  
*Latest update: 2026-02-01 — b=1 fixed point discovery, k=7 analysis, β-spectrum*
