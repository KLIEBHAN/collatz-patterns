# GPT Analysis: B-Sweep Instability Interpretation

**Date:** 2026-02-01  
**Topic:** Why does the Fourier spectrum change with boundary B?

---

## The Question

Our B-sweep showed:
- TV converges: 9.85% → 1.91%
- But top modes keep changing (LIFT at B=1000-10000, NEW at B=100 and B=100000)

Is this a problem?

---

## GPT's Answer: No — This is Expected!

### 1. B-Instability is Normal

> "Expecting the spectrum to stabilize in B is like expecting a river's turbulence spectrum to stay the same when you move the finish line upstream."

Different B = different sampling measure μ^(B). The **norm** (TV) can converge while the **spectrum** (which modes are top) moves around.

### 2. LIFT/NEW Oscillation Explained

**LIFT modes** (j ≡ 0 mod 3) measure **coarse mismatch** — discrepancy already visible on G₅:
```
Δ̂₆(3m) = (ρ#μ₆^(B) - ρ#π₆)^(m)
```

**NEW modes** (j ≡ 1,2 mod 3) measure **within-lift splitting** — how mass splits among 3 lifts.

The oscillation pattern:
| B | Dominant | Reason |
|---|----------|--------|
| Small (10) | NEW | Structured small-n creates fine biases |
| Intermediate (1000-10000) | LIFT | Removed worst near-1 structure, but moderate n still has coarse bias |
| Large (100000) | NEW | Large n → coarse close to ideal, within-lift is bottleneck |

### 3. WARNING: 1.9% May Be Sampling Noise!

For |G₆| = 486 and N = 400,000 samples:
```
Typical TV noise ≈ (1/2) √(|G|/N) = (1/2) √(486/400000) ≈ 0.017 = 1.7%
```

**This is very close to our observed 1.9%!**

**Required test:**
1. Run 5 independent seeds at B=100000
2. Measure mean(TV) and std(TV)
3. Run with 4× samples — if TV drops like 1/√N, it's noise

### 4. For Proof Strategy

The B-sweep is **heuristic**, not a proof object. The proof-shaped quantities are:

**Kernel defects** (conditional mixing):
```
ε₁ := sup_x TV(Q(x,·), P(x,·))
```

These are stable because they're conditional and don't depend on boundary sampling choice.

### 5. Better Alternative: Stratify by log(n)

Instead of boundary B, collect transitions in bins of log(n):
- n ∈ [10⁶, 10⁷), [10⁷, 10⁸), ...
- Compute μ_k,bin and Fourier spectrum per bin

This answers: "Which n-scales generate coarse vs within-lift mismatch?"

---

## Practical Checklist

For each B in sweep, compute:

1. **Projected TV:** TV(ρ#μ₆^(B), π₅) — measures coarse mismatch
2. **Within-lift energy fraction:** β-energy / total energy
3. **Noise floor test:** 5 seeds at B=10⁵, scale sample ×4

If (1) is large at B=1000-10000 but small at B=100000 → LIFT/NEW flip explained.
If TV scales like 1/√N → "bulk obstruction" may be below 1%!

---

## Key Quote

> "The B-dependence is telling you you're not looking at a single monolithic obstruction; you're looking at a scale-dependent mix of two obstructions (coarse vs within-lift), plus a very real statistical noise floor once you get down to ~2% TV. That's exactly the sort of structure you can turn into a multi-scale proof plan."
