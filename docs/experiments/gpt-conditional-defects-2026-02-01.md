# GPT Analysis: Conditional Defects at x=61

**Date:** 2026-02-01  
**Topic:** Why does state x=61 have 73% TV? What pattern is in the worst states?

---

## Key Insight: The Terminal Funnel

At small B, the killed/regenerative process spends time in a **terminal funnel** — a finite directed graph of small integers just above B that deterministically feed into n ≤ B.

When estimating row kernels Q(x,·), some rows look nothing like ideal because you're averaging over "the few specific small n's the dynamics visits when about to die."

---

## Why x=61 Has 73% TV

### The Deterministic Chute

```
61 → 23 → 35 → 53 → 5 (≤10, killed)
```

Step by step:
- 61: 3·61+1 = 184 = 8·23 → a=3, T(61)=23
- 23: 3·23+1 = 70 = 2·35 → a=1, T(23)=35
- 35: 3·35+1 = 106 = 2·53 → a=1, T(35)=53
- 53: 3·53+1 = 160 = 32·5 → a=5, T(53)=5 ≤ 10 (killed)

### Why This Creates 73% TV

Ideal P(61,·) distributes mass geometrically:
- a=1 → y≡92: weight ~0.5
- a=2 → y≡46: weight ~0.25
- a=3 → y≡23: weight ~0.125
- a=4 → y≡133: weight ~0.0625
- ...

But empirical Q(61,·) at B=10 is concentrated at y=23 (because many "x=61" events are literally n=61, which deterministically goes to 23 via a=3).

If Q(61,23) ≈ 0.85 while P(61,23) ≈ 0.125, TV ≳ 0.72 just from this one entry!

---

## Sanity Check: Is 73% Real or Noise?

Row-TV in a 162-state distribution is **unstable when the row has few samples**. Under the ideal model, if a row has only N_x transitions, expected TV is roughly ~const/√N_x (with const ≈ 0.84 for a geometric-shaped row).

To see TV ≈ 0.73 from pure sampling noise, you'd need N_x to be tiny (single digits).

**Interpretation:**
- If N_{61} is large (hundreds+): 73% is **real structure** (terminal funnel bias)
- If N_{61} is small: 73% could be mostly estimator noise

Either way, 61 being "special" is about **where the process spends time**, not about primality.

---

## The Pattern in Worst States

They all line up with the terminal funnel:

| x | smallest n₀ > 10 | a(n₀) | T(n₀) | successor |
|---|------------------|-------|-------|-----------|
| 190 | 433 | 2 | 325 | 82 |
| 82 | 325 | 4 | 61 | 61 |
| 61 | 61 | 3 | 23 | 23 |
| 23 | 23 | 1 | 35 | 35 |
| 35 | 35 | 1 | 53 | 53 |
| 77 | 77 | 3 | 29 | 29 |
| 29 | 29 | 3 | 11 | 11 |
| 25 | 25 | 2 | 19 | 19 |
| 49 | 49 | 2 | 37 | 37 |
| 134 | 377 | 2 | 283 | 40 |

> "This is way too coherent to be a 'prime pattern.' It's a small-integer skeleton of the dynamics."

---

## Proof Implications

### This Does NOT Threaten a Drift Proof

> "A Foster-Lyapunov proof never needs Q(x,·) ≈ P(x,·) for all x in the region where you're about to terminate anyway."

You pick a petite set C = {n ≤ B₀}, verify it by computation, and prove uniform negative drift outside. The bizarre terminal funnel rows are inside the finite region you handle separately.

**In fact, a terminal funnel is helpful:** it's extra deterministic pull toward C!

### State Reduction Insight

"State = n mod 3^k" is NOT Markov for the killed process at small B. The conditional law of a depends strongly on the scale of n, not just its 3-adic residue.

For proof-directed modeling, use:
- Bulk sampling (forced-start at large n) so scale mixture disappears
- Or enlarged state with 2-adic/history information

---

## B=10 → B=100 Improvement Explained

At B=10: residues like 61, 23, 35 have small representatives above 10, so they appear as actual small integers on the way to death → deterministic rows.

At B=100: those small integers are inside the killed set. When you see x=61 at B=100, actual n must be ≥ 547 (smallest odd > 100 with that residue) → pushes toward geometric-a regime.

> "The improvement is not mysterious: you moved the boundary past the worst terminal funnel nodes."

---

## Predictions to Verify

1. **Q(61, 23) should be inflated** (much larger than ideal 0.125)
2. **Q(61, 92) and Q(61, 46) should be suppressed** (ideal ~0.5 and ~0.25)
3. **The whole worst list forms a "too-deterministic chain":**
   - Q(190, 82) inflated
   - Q(82, 61) inflated
   - Q(61, 23) inflated
   - Q(23, 35) inflated
   - Q(35, 53) inflated

---

## Meta-Lesson

> "Experiment C is doing its job—it's showing you where your reduction breaks. At B=10 the breakage is exactly where you'd expect: in the terminal funnel. That's not a Collatz 'monster'; it's the Collatz map walking you to the exit."

---

## GPT's Recommended Next Steps

### 1. Attach Counts and Error Bars
For each of the "worst 10" rows, report N_x (row sample size). Then compute a null p-value by simulating N_x samples from P(x,·) and asking how often TV exceeds the observed. This separates "real defect" from "low-count hallucination."

### 2. Print the Top Successors for x=61
List the top 5 y with Q(61,y) and compare to P(61,y). If the terminal funnel story is right, you'll see:
- Big spike at y=23
- Suppression at y=92 and y=46

### 3. Repeat Experiment C at Truly Bulk Boundary
Run at B=10⁵ OR with forced-start large n≡x. This tells you whether the *bulk* one-step kernel is close statewise — which is what you actually want for a stability proof.

---

## Status

**Verified:** The 73% spike at x=61 disappears at higher B (see Three-Phase Model in findings.md). This confirms the terminal funnel explanation — it's a boundary effect, not a deep mathematical obstruction.
