# k=5 Fourier Analysis — Lift-Structure Test

Date: 2026-02-01

## Hypothesis

Based on the lift pattern k=3→k=4 (j=7,11 → j=21,33), we predicted:
- k=5 top targets should be j=63 (3×21) and j=99 (3×33)

## Results

**HYPOTHESIS PARTIALLY REJECTED**

### Full k=5 Ranking

| Rank | j | |Δ| | Notes |
|------|---|-----|-------|
| 1 | 79 | 0.0364 | **NEW** (not a lift) |
| 2 | 83 | 0.0364 | Conjugate of 79 |
| 3 | 127 | 0.0305 | |
| 4 | 35 | 0.0305 | Conjugate of 127 |
| 5 | 137 | 0.0230 | |
| 6 | 25 | 0.0230 | Conjugate of 137 |
| **7** | **63** | **0.0218** | **Predicted lift of 21** |
| **8** | **99** | **0.0218** | **Predicted lift of 33** |
| 9 | 111 | 0.0213 | |
| 10 | 51 | 0.0213 | |

### Key Observations

1. **j=63,99 are present but NOT dominant**
   - Ranked #7-8, not #1-2
   - Their deviation (0.0218) is ~60% of the top (0.0364)

2. **j=79,83 are NEW characters**
   - 79/3 = 26.33 (not integer)
   - 83/3 = 27.67 (not integer)
   - These are not lifts from k=4

3. **Conjugate structure preserved**
   - 79 + 83 = 162 = φ(3⁵) ✓
   - 127 + 35 = 162 ✓
   - 63 + 99 = 162 ✓

### Interpretation

The lift-structure is **incomplete**:

| Transition | Prediction | Actual | Match |
|------------|------------|--------|-------|
| k=2 → k=3 | 6,12 | 7,11 | ❌ |
| k=3 → k=4 | 21,33 | 21,33 | ✅ |
| k=4 → k=5 | 63,99 | 79,83 | ❌ |

**Pattern:** The lift structure holds at even→odd transitions (k=3→k=4) but breaks at odd→even (k=2→k=3, k=4→k=5).

### Theoretical Implications

1. **New obstructions emerge at each level**
   - Not all dominant characters are inherited from lower k
   - The "true" obstruction landscape is richer than simple lifting

2. **Proof strategy update**
   - Cannot focus only on lifted characters
   - Need to analyze which character indices become dominant at each k

3. **The characters j=79,83 require investigation**
   - Why do these specific indices dominate?
   - Is there structure relating 79,83 to the dynamics?

### Additional Data

**TV Distance by k:**
| k | TV | Top |Δ| |
|---|-----|--------|
| 2 | 0.8% | 0.012 |
| 3 | 2.0% | 0.027 |
| 4 | 3.0% | 0.025 |
| 5 | 5.2% | 0.036 |

TV grows roughly linearly; top deviation grows but not monotonically.

### Next Steps

1. **Investigate j=79,83:** What makes these indices special?
2. **Check k=6:** Do new dominant characters emerge again, or do 79,83 lift to 237,249?
3. **Analyze mod structure:** What do states with high π(x) look like under χ_79?

---

*Analysis run with 200,000 samples, exact rational P_k model*
