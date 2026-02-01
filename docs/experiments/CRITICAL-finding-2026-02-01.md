# CRITICAL FINDING: Extended Run Measured Trivial Fixed Point!

**Date:** 2026-02-01 06:30 UTC

## The Problem

The "extended run" (t_burn=200, t_max=300) that appeared to show dramatically improved results was actually measuring **nothing meaningful**.

### What Happened

| Run | t_burn/t_max | State 0 (n=1) fraction | E[Δlog n] | worst_corrected |
|-----|--------------|------------------------|-----------|-----------------|
| Original | 34/50 | **28%** | **-0.182** | +0.180 |
| Extended | 200/300 | **100%** | -0.000005 | +0.000005 |

### Why This Happened

Collatz trajectories **terminate quickly**. Most numbers reach n=1 within 100-200 steps:

```
Starting n=42911207:
  t=0:   n=42911207
  t=50:  n=49
  t=100: n=1          ← Already at fixed point!
  t=200: n=1          ← Still at fixed point
  t=300: n=1          ← Still at fixed point
```

When t_burn=200, **100% of sampled transitions are 1→1→1→...** with:
- Δlog n = log(1) - log(1) = 0
- All "drift" metrics become trivially ~0

### The Illusion

We thought:
- "Max corrected drift dropped from 0.18 to 0.000005! 🎉"
- "99.997% improvement!"

Reality:
- We switched from measuring real Collatz dynamics to measuring the trivial fixed point
- The "improvement" was an artifact of having no data

## The REAL Results (Original Run)

From the **meaningful** run (t_burn=34, t_max=50, S=500k):

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **E[Δlog n]** | **-0.182** | ✅ Strong negative drift! |
| Max raw drift | +0.451 | Some states go "uphill" |
| Max corrected drift | **+0.180** | ⚠️ Still positive after ψ-correction |
| States with positive drift | 1 / 4,374 | Single outlier |
| π-mass of outlier | ~0 | Never visited |
| |λ₂| | 0.973 | Slow mixing |

## Key Insight

The ψ-correction is working (sort of):
- 4373/4374 states have negative corrected drift
- The single outlier was never actually visited (0 transitions)
- But: the outlier's existence is a numerical/theoretical concern

## Why GPT's Recommendation Was Wrong

GPT recommended "longer horizon (t_max=300, t_burn=200)" based on general Markov chain theory. But Collatz is special:

1. **Collatz terminates** — trajectories reach n=1 and stay there
2. At late times, you're not sampling the "stationary distribution" of residue dynamics
3. You're sampling the absorbing state

For Collatz, we need to stay in the **transient phase** (t < stopping time) to measure meaningful drift.

## Corrective Actions

1. ✅ **Identified the problem**
2. ⬜ **Use original run** (t=34-50) as the valid baseline
3. ⬜ **Investigate the outlier state** in original run
4. ⬜ **Consider different approach**: Instead of late-time sampling, use early-time with larger N, or condition on "not yet at 1"

## Updated Understanding

| What we thought | Reality |
|-----------------|---------|
| Extended run = better | Extended run = trivial |
| Drift ~10⁻⁵ = nearly solved | Drift ~10⁻⁵ = at fixed point |
| 4324 states positive = noise | We were measuring nothing |

**Actual status:** Back to original run results:
- E[Δlog n] = -0.182 ✅
- 1 outlier state with positive corrected drift ⚠️
- Need to handle the outlier (m-step drift, or prove it's unreachable, or...)

---

*This is why sanity checks matter!*
