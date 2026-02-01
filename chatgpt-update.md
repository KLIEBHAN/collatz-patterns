# Update: k=5 Fourier Analysis Results

## Context
Following your analysis of our Collatz project, we tested your prediction that k=5 top Fourier targets would be j=63,99 (lifts of j=21,33 from k=4).

## Results: Prediction Partially Refuted

**k=5 Top Targets (verified stable across 5 random seeds, 200k samples each):**

| Rank | j | |Δ| | Notes |
|------|---|------|-------|
| 1-2 | 79, 83 | 0.033-0.036 | **NEW** (not lifts!) |
| 3-4 | 127, 35 | 0.027-0.030 | Also new |
| 7-8 | 63, 99 | 0.022 | Predicted lifts |

**Key observations:**
- 79 % 3 = 1, 83 % 3 = 2 → NOT divisible by 3 → NOT lifts from k=4
- 79 + 83 = 162 = φ(3⁵) → correct conjugate pair ✓
- j=63,99 (the predicted lifts 3×21, 3×33) are present but only rank #7-8

## Lift Pattern Summary

| Transition | Predicted | Actual | Match |
|------------|-----------|--------|-------|
| k=2 → k=3 | 6, 12 | 7, 11 | ❌ |
| k=3 → k=4 | 21, 33 | 21, 33 | ✅ |
| k=4 → k=5 | 63, 99 | 79, 83 | ❌ |

The lift structure holds for k=3→k=4 but breaks at other transitions.

## Verification
- Compared empirical against **exact** π (rational arithmetic, sympy)
- Tested 5 different random seeds: j=79,83 appear as top-2 in **all 5** (100%)
- j=127,35 appear as #3-4 in all 5 seeds
- TV distance at k=5: ~5.2%

## Open Questions

1. **What makes j=79,83 special?** Why do these specific character indices dominate at k=5 when they're not inherited from k=4?

2. **Is there a pattern?** At k=3 we got "new" targets (7,11), at k=4 they lifted to (21,33), at k=5 we again get "new" targets (79,83). Does this alternate?

3. **What's the relationship between 79,83 and the dynamics?** Is there structure relating these indices to the Syracuse map's behavior mod 243?

4. **Prediction for k=6:** Will 79,83 lift to 237,249 (×3), or will new modes emerge again?

## Data Available
- Full Fourier coefficient tables for k=2,3,4,5
- Exact π distributions (rational)
- Empirical sampling data (200k+ samples per k)

Looking forward to your theoretical interpretation!
