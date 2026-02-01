# GPT Analysis: Noise Floor Test Results

**Date:** 2026-02-01  
**Topic:** Is the ~0% bulk signal real? What does it mean for proof?

---

## Summary

GPT confirms our noise floor test is valid and the ~0% signal at B=100000 is real — but clarifies what this means and doesn't mean for Collatz.

---

## Key Validation

### The 8.15 constant is correct!

Theoretical prediction for i.i.d. multinomial:
```
E[TV] ≈ √((S-1)/(2πN))
```

For S = |G₆| = 486:
- Predicted: √((485)/(2π)) ≈ 8.79
- Observed: 8.15 ± 0.12

Close match! The slight difference is expected due to non-uniformity of π.

### What ~0% signal means

> "Your k=6 marginal residue distribution is statistically indistinguishable from the ideal π₆, with any true discrepancy likely ≲0.3% and possibly much smaller."

**BUT:** This is one observable. Collatz troublemakers can hide in:
1. **Conditional laws Q(x,·)** — kernel defects even if marginal matches
2. **Time correlations** — marginal perfect but transitions structured
3. **Large deviations** — rare bad blocks with many small a's

---

## Proof Roadmap (Updated)

### Where the hard part now lives

> "The hard part is no longer 'does it look random on G₆?' — your data says: for large n, it basically does. The hard part becomes 'turn this into a uniform/quantitative statement that survives worst-case and conditioning.'"

### Three-part proof structure

1. **Bulk equidistribution lemma (conditional)**
   ```
   sup_{x∈S} TV(Q^k(x,·), π) ≤ ε  for all sufficiently large n
   ```
   Not μ ≈ π, but kernel-level closeness.

2. **Stability lemma (Foster-Lyapunov)**
   If ideal model gives negative drift for V(n) = log n + ψ(x), and real kernel is within ε, drift stays negative:
   ```
   E[V_{t+1} - V_t | X_t = x] ≤ -δ + O(ε‖ψ‖_∞) + (finite-n terms)
   ```

3. **Large-deviation / bad-block control**
   Show bad blocks (many small a's) have exponentially small frequency.

---

## Skepticism Points

### What could make signal appear smaller?

1. **Killing bias** — killing changes the measure
   - Control: run ideal Markov chain with same killed protocol
   
2. **Dependence / effective sample size**
   - Trajectories are not i.i.d.
   - Check: compute integrated autocorrelation time

3. **TV estimator bias**
   - E[TV(μ̂,π)] is biased upward even when μ=π
   - Alternative: use ℓ² or chi-square statistic

### What about smaller B?

> "Almost certainly real structure at low B, because the TV values there were huge (~10% at B=10), far above the noise floor."

For intermediate B (100-10000): awkward zone where signal ≈ noise.

---

## Recommended Next Experiments

### Experiment A: Noise-floor scaling at smaller B (HIGHEST ROI)

Run same N ∈ {100k, 200k, 400k, 800k} test for:
- B = 10
- B = 100  
- B = 1000

Fit signal(B) from TV² = signal² + c/N

This tells us if LIFT/NEW oscillation is real structure or top-mode jitter.

### Experiment B: Size-stratified (log n) sampling

Instead of killing thresholds, stratify by magnitude bins:
```
log₁₀ n ∈ [6,7), [7,8), ..., [14,15)
```

Within each bin compute:
- μ_k,bin and TV to π_k
- Fourier spectrum and β-energy split
- P(a|b) and I(a;b) (mutual information)

If discrepancy shrinks with bin level → exactly what a proof wants.

### Experiment C: Kernel-level defect (not just marginal)

Pick ~50-100 starting residue states x ∈ G₆.
For each:
1. Forced-start large integers n ≡ x (mod 3⁶)
2. Evolve for k (or 2k) steps
3. Estimate TV(L(X_{t+k} | X_t = x), π)

This is closer to a Doeblin/minorization statement.

---

## What This "Too Good" Result Means

> "The 3-adic marginal mixing at level 3⁶ is not the bottleneck in the bulk."

Believable because:
- Syracuse map is 3-adically contracting
- a is close to geometric and weakly correlated

> "So the Collatz monster is probably not hiding in 'mod 3⁶ looks wrong' for large n. It's hiding in:
> - conditional kernels
> - rare-event tails  
> - worst-case exceptional sets
>
> That's still hard—but it's the kind of hard that has a clear shape."

---

## Next Step

Run Experiment A (noise scaling at B=10, 100, 1000) to get signal(B) curve.
Then we can define a concrete "exceptional set + stability margin" lemma candidate.
