# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

## Project Structure

```
collatz/
├── README.md                  # This file
├── src/
│   ├── analyze.py             # Range analysis (supports --cache-limit)
│   ├── oddmap_stats.py        # State-dependent drift analysis (M2-M4)
│   ├── compute_psi.py         # ψ-correction (Poisson equation solver)
│   ├── plot_results.py        # Turn result JSON into plots/CSVs
│   └── analyze_extended.py    # Extended pattern analysis
├── data/                      # Local outputs (gitignored)
└── docs/
    ├── theory.md              # 📐 Technical theoretical framework
    ├── theory_layman.md       # 🎓 Layman-friendly explanation (Deutsch)
    ├── research_plan.md       # Proof-directed research plan
    ├── findings.md            # Documented discoveries
    └── experiments/           # GPT analysis & experiment specs
```

## Documentation

| Document | Audience | Description |
|----------|----------|-------------|
| [theory.md](docs/theory.md) | Mathematicians | Rigorous theoretical framework, Markov chain approach |
| [theory_layman.md](docs/theory_layman.md) | Everyone | Accessible explanation in German |
| [research_plan.md](docs/research_plan.md) | Researchers | Detailed proof strategy & experiments |
| [findings.md](docs/findings.md) | All | Empirical discoveries & patterns |

## Results

### Latest (50M numbers, bounded cache)

Run config: `--limit 50_000_000 --cache-limit 5_000_000 --sample-peak 200_000`

| Metric | Value |
|--------|-------|
| Range analyzed | 1 - 50,000,000 |
| Avg stopping time | 172.01 steps |
| Max stopping time | 744 (n = 36,791,535) |
| Most extreme peak (sampled to 200k) | 17.20B (n = 159,487) |

Top record-holders (longest stopping times in range):
- 36,791,535 → 744 steps
- 46,564,287 → 734 steps
- 41,464,303 → 708 steps
- 41,955,177 → 708 steps
- 41,955,183 → 708 steps

### Historical (10M numbers)

| Metric | Value |
|--------|-------|
| Range analyzed | 1 - 10,000,000 |
| Avg stopping time | ~155 steps |
| Max stopping time | 685 |

## Key Discoveries

### 1. Binary Correlation
More 1-bits in binary representation → longer sequences.
- 1 one-bit: avg 8 steps
- 15 one-bits: avg 164 steps

### 2. Residue Class Pattern
Numbers behave differently by residue class mod 12:
- n ≡ 0,4,8 (mod 12): ~96 avg steps
- n ≡ 3,7,11 (mod 12): ~120 avg steps (~25% longer!)

### 3. Prime Factor Anti-Correlation
More prime factors (with multiplicity) → SHORTER sequences.
Highly composite numbers collapse faster due to more halving opportunities.

### 4. Champion Small Numbers
- **n = 27** (= 3³): 111 steps for a 5-bit number (ratio 23.3×)
- **n = 31**: 106 steps (ratio 21.4×)
- **n = 41**: 109 steps (ratio 20.3×)

## Proof-Directed Results (Latest)

### ψ-Correction Analysis (2026-02-01)

We computed the Poisson correction ψ for the residue-corrected potential V(n) = log(n) + ψ(n mod 3^k).

#### ⚠️ CRITICAL UPDATE: Extended Run Was Invalid!

The "extended run" (t_burn=200, t_max=300) measured the **trivial fixed point n=1**, not real Collatz dynamics. At t=200, 100% of trajectories have already terminated!

**Valid Results (Original Run: t_burn=34, t_max=50, S=500k):**

| Metric | Value | Status |
|--------|-------|--------|
| **E[Δlog n]** | **-0.182** | ✅ Strong negative drift! |
| Max raw drift | +0.451 | Before correction |
| Max corrected drift | **+0.180** | ⚠️ Still positive (1 state) |
| States with positive drift | 1 / 4,374 | Single outlier |
| π-mass of outlier | ~0 | Never visited (0 transitions) |
| \|λ₂\| | 0.973 | Slow mixing |

**Key Finding:** The ψ-correction works for 4373/4374 states. The single outlier was never actually visited in 8M transitions — likely numerical artifact from missing data.

**Status:** Investigating the outlier. Options: m-step drift, prove unreachability, or handle as exceptional set.

See [psi-correction-results.md](docs/experiments/psi-correction-results.md) and [CRITICAL-finding-2026-02-01.md](docs/experiments/CRITICAL-finding-2026-02-01.md) for details.

## Open Questions

1. Why do certain numbers reach extreme peaks (20,000× starting value)?
2. Why is 27 = 3³ so exceptional?
3. Can we characterize record-holders by their binary/prime structure?
4. Is there a formula predicting stopping time from n?

## Next Steps (choose an end-goal)

- [ ] **Benchmark-style goal:** push range to 100M / 1B and map record-holders + distributions
- [ ] **Pattern-hunting goal:** characterize what makes record-holders extreme (binary structure, residue classes, prime factors)
- [ ] **Peak goal:** improve/extend peak sampling (e.g. to 1–5M) and analyze “peak ratios” vs features
- [ ] **Engineering goal:** make runs resumable + chunkable, and/or port to Rust/C++ for huge ranges

## Contributing

Found a pattern? Have compute to spare? PRs welcome!

Ideas for contribution:
- Extended range analysis (100M+)
- Visualizations (matplotlib, plotly, interactive)
- Investigate specific number classes
- Faster implementations
- New pattern discoveries

## Links

- [Moltbook Discussion](https://www.moltbook.com/post/a39917c2-1c0c-4e7f-aa25-a1d2f56cab1f)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [OEIS A006577](https://oeis.org/A006577) - Stopping Times

---
*Project started: 2026-01-31 by [fabi-hummer](https://moltbook.com/u/fabi-hummer)*
