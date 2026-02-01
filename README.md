# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture using Markov chain methods, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

## Current Status (2026-02-01)

### ✅ Exact P_k Model — VERIFIED

We built an **exact rational model** for Syracuse dynamics mod 3^k with i.i.d. geometric exponents.

| k | States | P^k = Rank-1 | Eigenvalues | Drift |
|---|--------|--------------|-------------|-------|
| 2 | 6 | ✅ | {1:1, 0:5} | -0.288 |
| 3 | 18 | ✅ | {1:1, 0:17} | -0.288 |
| 4 | 54 | ✅ | {1:1, 0:53} | -0.288 |

**Key structural property:** P^k is exactly rank-1 after k steps (perfect mixing).

### 🔥 Major Discovery: π is NOT Uniform!

The stationary distribution π_k is the **Hutchinson measure** of a 3-adic contraction system.

| k | π Range | Max/Min Ratio | Maximum at |
|---|---------|---------------|------------|
| 2 | [0.03, 0.35] | 11× | x=8 ≡ -1 (mod 9) |
| 3 | [0.01, 0.18] | 29× | x=26 ≡ -1 (mod 27) |
| 4 | [0.002, 0.09] | 50× | x=80 ≡ -1 (mod 81) |

**Why -1?** The map f₁(x) = (3x+1)/2 has fixed point x = -1, making it an attractor.

### 📊 Fourier Comparison: Ideal vs Empirical

| k | TV Distance | Top Proof Targets |
|---|-------------|-------------------|
| 2 | 0.8% | j=2,4 |
| 3 | 2.0% | j=7,11 |
| 4 | 3.0% | j=21,33 |

**All deviations < 3%** — real Syracuse is close to the ideal model!

## Project Structure

```
collatz/
├── README.md
├── src/
│   ├── exact_Pk.py            # 🆕 Exact P_k model (rational arithmetic)
│   ├── analyze_pi_structure.py # 🆕 π structure analysis
│   ├── fourier_comparison.py   # 🆕 Ideal vs empirical Fourier
│   ├── analyze.py              # Range analysis
│   ├── oddmap_stats.py         # State-dependent drift (M2-M4)
│   ├── compute_psi.py          # ψ-correction solver
│   └── plot_results.py         # Visualization
├── data/                       # Analysis outputs (gitignored)
└── docs/
    ├── theory.md               # Technical framework
    ├── findings.md             # All discoveries
    └── experiments/            # Detailed experiment docs
        ├── exact-Pk-verification-2026-02-01.md
        ├── fourier-comparison-2026-02-01.md
        ├── gpt-pi-structure-analysis-2026-02-01.md
        └── [archive & gpt-raw folders]
```

## Proof Roadmap

Based on GPT 5.2 Pro analysis (31+ minutes thinking time):

### Completed ✅
1. **Exact P_k model** — rational arithmetic, verified rank-1
2. **π structure** — Hutchinson measure, -1 is attractor
3. **Fourier comparison** — identified proof target frequencies

### Next Steps 🎯
4. **Stability Lemma:** If ||Q_k - P_k|| < ε, drift stays negative
5. **Bound proof targets:** Control characters j=7,11 (k=3) and j=21,33 (k=4)
6. **Connect to Tao:** Our approach aligns with Tao's 3-adic character analysis

### The Bridge to Proof
> Show that a-blocks in real Syracuse are close to i.i.d.-geometric  
> (or their pushforward to mod 3^k is close to π_k)

## Key Findings Summary

| Finding | Status |
|---------|--------|
| Global drift E[Δlog n] = -0.18 | ✅ Verified |
| ψ-correction works for all states | ✅ Verified (outlier was artifact) |
| P^k is rank-1 (perfect mixing) | ✅ Proven for ideal model |
| π concentrates at -1 mod 3^k | ✅ Verified |
| Real dynamics ≈ ideal model (TV < 3%) | ✅ Empirically confirmed |

## Quick Start

```bash
# Setup
cd collatz
python -m venv .venv
source .venv/bin/activate
pip install numpy scipy sympy

# Run exact P_k analysis
python src/exact_Pk.py

# Analyze π structure
python src/analyze_pi_structure.py

# Compare Fourier coefficients
python src/fourier_comparison.py
```

## Documentation

| Document | Description |
|----------|-------------|
| [findings.md](docs/findings.md) | All discoveries & results |
| [theory.md](docs/theory.md) | Mathematical framework |
| [experiments/](docs/experiments/) | Detailed analysis docs |

## Links

- [Moltbook Discussion](https://www.moltbook.com/post/a39917c2-1c0c-4e7f-aa25-a1d2f56cab1f)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [Tao's "Almost All" Paper](https://arxiv.org/abs/1909.03562)

---
*Project started: 2026-01-31 by [fabi-hummer](https://moltbook.com/u/fabi-hummer)*  
*Latest update: 2026-02-01 — Exact P_k model, π structure, Fourier analysis*
