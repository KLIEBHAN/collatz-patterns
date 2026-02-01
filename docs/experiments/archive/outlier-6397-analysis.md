# Outlier State Analysis: Residue 6397

**Date:** 2026-02-01 06:35 UTC

## The Outlier

From the valid run (t_burn=34, t_max=50, S=500k):

| Property | Value |
|----------|-------|
| State Index | 4264 |
| Residue (mod 6561) | **6397** |
| Visit Count | **0** (in 8M transitions!) |
| g_raw | 0.000 (no data) |
| g_corrected | +0.180 |
| ψ | -0.180 |

The "positive corrected drift" is **entirely from ψ** — there are no actual data points for this state.

## Why 0 Visits?

Residue 6397 is a **"transient early" residue**:

| Time Window | Visits to 6397 | Percentage |
|-------------|----------------|------------|
| t < 34 (early) | 542 | **98.5%** |
| t = 34-50 (late) | 6 | **1.1%** |

Numbers pass through 6397 early in their trajectory, but almost never at late times (t=34-50).

### Expected vs Actual

With 500k trajectories and ~6 expected visits per 1M trajectories at t=34-50:
- Expected visits: ~3
- Actual visits: 0
- Probability of 0 visits (Poisson): **~5%**

→ The 0 visits is **bad luck**, not impossibility.

## Properties of Residue 6397

```
6397 in different representations:
  Binary: 0b1100011111101 (13 bits, 9 ones)
  mod 3: 1
  mod 9: 7
  mod 27: 25
```

Numbers with this residue exist and DO reach 1:
- n=19519: reaches 1 in 54 steps
- n=32641: reaches 1 in 20 steps
- n=45763: reaches 1 in 62 steps

## Why ψ = -0.180?

The Poisson equation solution assigns ψ values based on the transition structure. For state 6397:
- It has no outgoing transitions in our data
- The solver assigns a ψ value based on interpolation/regularization
- This creates an artifact where g_corrected = g_raw + (Pψ - ψ) ≠ ḡ

With g_raw = 0 and ψ = -0.180:
```
g_corrected = 0 + (Pψ)(6397) - (-0.180)
            = (Pψ)(6397) + 0.180
```

Since we don't know (Pψ)(6397) from data, the solver guesses, resulting in g_corrected ≈ +0.18.

## Resolution Options

### Option 1: Ignore (pragmatic)
- The state is never visited in practice
- π-mass = 0
- For proof purposes, can exclude as "exceptional set"

### Option 2: Targeted sampling
- Sample trajectories that pass through 6397
- Get actual data for g_raw and transitions
- Recompute ψ with real data

### Option 3: Early-time window
- Use t_burn=0, t_max=34 instead
- 6397 is well-visited at early times
- Trade-off: non-stationary effects

### Option 4: m-Step drift
- Compute cumulative drift over m steps
- If neighboring states have negative drift, m-step from 6397 may also be negative
- Requires transition data we don't have

## Recommendation

**Use Option 1 (ignore) + Option 3 (early-time validation):**

1. For the proof structure, treat 6397 as an exceptional set with π-mass ≈ 0
2. Run a separate analysis with t_burn=0 to verify 6397 behaves normally at early times
3. If early-time drift for 6397 is also negative, the late-time artifact is irrelevant

---

*The outlier is a data gap, not a structural problem.*
