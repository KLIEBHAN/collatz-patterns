# GPT 5.2 Pro Analysis: Outlier Handling & Sampling Strategies

*Date: 2026-02-01 06:37 UTC*
*Thinking time: ~12 minutes*

## Context

After discovering that:
1. The "Extended Run" (t=200-300) measured the trivial fixed point (100% at n=1)
2. Outlier state 6397 had 0 visits in 8M transitions
3. Residue 6397 appears 98.5% at t<34, only 1.1% at t=34-50

We asked GPT for guidance on:
1. How to handle the outlier (no real data)
2. Is m-step drift still useful?
3. Alternative sampling strategies

---

## GPT's Key Insight

> "Der Fixpunkt hat euch einmal getrollt; das passiert jedem, der mit absorbierenden Prozessen spielt. Der gute Teil: ihr habt jetzt ein sehr klares Engineering-Kriterium gelernt — 'lange Zeiten' sind nur dann informativ, wenn die Trajectories dort noch nicht absorbiert sind."

---

## Question 1: How to Handle the Outlier?

### Problem
When a state s* has 0 visits in the sampling window:
- ĝ(s*) (state drift) is **not estimable**
- P̂(s*, ·) (transition row) is **not estimable**
- ψ(s*) becomes a "free parameter" filled by numerical regularization
- "Max corrected drift = +0.180" is an **artifact**, not real data

### Solution: Report Correctly

1. **Define a data-support set:**
   ```
   S_min := {s : N_s ≥ N_min}
   ```
   with e.g., N_min = 200 or 1000

2. **Report:**
   - `max_{s ∈ S_min} d_corr(s)` (plus confidence upper bound)
   - π̂(S_min^c) — total mass outside support
   - States with N_s = 0: mark as **NaN**, not "positive"

### Diagnostic: Check Graph Structure

Build the directed graph of observed transitions in window t=34..50:
- Edge s → s' if C(s, s') > 0

Check:
- Is 6397 in the giant SCC (strongly connected component)?
- Are there ANY incoming edges to 6397?

If incoming = 0, then 6397 is "outside" the empirical dynamics support.

---

## Question 2: Is m-Step Drift Still Useful?

### Answer: Yes, but depends on the goal

### Case A: Statements under the window measure (evolved measure at t≥34)
- m-step drift is **very useful**
- The outlier is **irrelevant** if unreachable from the support

**What to do:**
1. Compute m-step drift only on the observed SCC/support
2. Estimate/bound probability of reaching outlier in m steps
3. If 0 hits in M "chances" → p ≲ 3/M as rough 95% upper bound

### Case B: Worst-case statement "for all residues"
- m-step drift is useful
- But you **need data for the outlier** (via forced sampling)

---

## Question 3: Alternative Sampling Strategies

### Why Extended Run Failed
With starting values n ≤ 5·10^7, long horizons (t ~ 200+) are not "mixing measurement" but "absorption at 1".

To measure "late times" properly, you must either:
1. Start far from 1, OR
2. Actively remove absorption from the experiment

### Strategy S1 ⭐ (Recommended): Very Large Starting Values

**The cleanest solution: measure real dynamics, not the fixed point.**

**Implementation:**
- Choose start n₀ as random odd L-bit number, e.g., L=256 or L=384
- Probability of reaching 1 within 300 odd-steps is practically zero
- Then t=200..300 or t=300..400 windows work without absorption

**Suggested Parameters:**
| Parameter | Value |
|-----------|-------|
| k | 8 (as before) |
| t_max | 400 |
| t_burn | 200 |
| Window | t ∈ [200, 399] (200 steps) |
| S | 200,000 trajectories |
| Transitions | ~40M in window |

**Why this fixes the outlier:**
"Late" behavior is no longer dominated by "near 1" but by genuine large-n dynamics. You'll see if 6397 is truly "unreachable" or just disappears in small-n setup.

### Strategy S2: Regenerative Sampling (Restart at small n)

If you don't want BigInts or want to measure "only large-n":

1. Set threshold B (e.g., B = 10^6 or 10^9)
2. Simulate trajectories, but when n_t ≤ B, end episode and restart with fresh large start
3. Collect transitions only while n_t > B

**Proof-compatible** because typical proof structure is:
- Show drift/descent for n large
- Brute-force verify small set n ≤ B

### Strategy S3: Quasi-Stationary Sampling (Fleming-Viot)

For explicitly approximating "conditioned on not absorbed":

1. Maintain population of M particles (trajectories)
2. Per step: all update n ↦ T(n)
3. If particle hits 1 (or < B), replace with copy of random surviving particle

Approximates quasi-stationary distribution of "killed chain". Technically powerful but methodologically demanding.

---

## Concrete Next Steps (GPT's Plan)

### Step 0: "Defuse" the Outlier

For the run t=34..50:
1. Set drift/values for states with N_s = 0 to **NaN**
2. Report maxima only over S_min (e.g., N_s ≥ 200)
3. Report π̂(S_min^c)
4. Check if there are incoming edges to 6397

**Result:** "We have no information for this state" — clean and honest.

### Step 1: Forced-Start Sampling for Outlier (Cheap, Highly Informative)

To know if 6397 is structurally "bad":

1. Generate random large numbers n = 6397 + 6561·r (with r random, n odd)
2. Measure 1-step and m-step behavior from this start:
   - Distribution of a(n)
   - Δlog n
   - Target residue T(n) mod 6561

**Result:** Real data for row P(6397, ·) and g(6397) without waiting for "natural" visits.

### Step 2: New Extended Run with Large Starting Values (S1)

The real fix for "we need longer burn-ins / real mixing":

1. Implement BigInt starting values (256-384 bits)
2. Run with t_burn=200, t_max=400
3. Solve for ψ again

**Expected result:**
- Outlier problems dramatically reduced
- |λ₂| / TV-mixing meaningfully interpretable (not fighting absorption)

---

## Summary Answers

| Question | Answer |
|----------|--------|
| **Outlier handling** | Mark as NaN (no data). Report only over S_min. Check incoming edges. |
| **m-Step drift useful?** | Yes, for observed support. For outlier: only with forced sampling. |
| **Alternative sampling** | S1 (large starts) recommended. S2 (regenerative) also good. S3 (QSD) advanced. |

---

## Key Lesson Learned

> "Mit Startwerten n ≤ 5·10^7 sind lange Horizons (t ~ 200+) keine 'Mixing-Messung', sondern fast immer 'Absorption bei 1'."

**Engineering criterion:** Long times are only informative when trajectories haven't absorbed yet.

---

*Analysis complete. Next: Implement Step 0 (defuse outlier), then Step 1 (forced sampling), then Step 2 (large-n run).*
