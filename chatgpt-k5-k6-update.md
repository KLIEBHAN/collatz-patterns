# Update: k=5 and k=6 Fourier Analysis Results

Following your earlier analysis, we ran the experiments you suggested. Here are the complete results.

## k=5 Results (Recap)

**Top targets:** j=79, 83 (NOT the predicted lifts j=63, 99)
- 79 % 3 = 1, 83 % 3 = 2 → new-digit modes
- 79 + 83 = 162 = φ(3⁵) → conjugates ✓
- TV distance: 5.2%

**Lift-Splitting Decomposition (your suggestion):**
We implemented the coarse vs within-lift energy decomposition:
- Coarse Δ(b) energy: **24.1%**
- Within-lift δ₁(b) + δ₂(b) energy: **75.9%**

→ **Confirmed:** Within-lift dominates 3:1, explaining why non-lift modes win.

**Surprise:** Top contributor to δ₁ was b=1, not b=80 (≡-1 mod 81) as hypothesized. b=80 ranked #8.

## k=6 Results (NEW)

**Parameters:** M=729, φ(3⁶)=486, Nyquist=243, 400k samples

**Top 10 Proof Targets:**

| Rank | j | |Δ| | j%3 | Type | Notes |
|------|---|-----|-----|------|-------|
| 1 | 401 | 0.0391 | 2 | NEW | conjugate of 85 |
| 2 | 85 | 0.0391 | 1 | NEW | conjugate of 401 |
| 3 | 237 | 0.0382 | 0 | LIFT | = 3×79 ✓ |
| 4 | 249 | 0.0382 | 0 | LIFT | = 3×83 ✓ |
| 5 | 337 | 0.0362 | 1 | NEW | |
| 6 | 149 | 0.0362 | 2 | NEW | |
| 7 | 359 | 0.0347 | 2 | NEW | |
| 8 | 127 | 0.0347 | 1 | NEW | |
| 9 | 379 | 0.0343 | 1 | NEW | |
| 10 | 107 | 0.0343 | 2 | NEW | |

**TV distance:** 8.32%

**Your predictions:**
- Lifts j=237, 249: Rank #3-4 ✅ (close!)
- Nyquist-neighbors j=241, 245: Rank #267-268 ❌ (not dominant at all)

**Mode distribution in Top-20:**
- LIFT modes: 4 (20%)
- NEW-DIGIT modes: 16 (80%)

## Summary: The Pattern Across k

| k | φ(3^k) | Top-2 | Type | Lifts of prev? |
|---|--------|-------|------|----------------|
| 3 | 18 | 7, 11 | NEW | — |
| 4 | 54 | 21, 33 | LIFT | = 3×7, 3×11 ✅ |
| 5 | 162 | 79, 83 | NEW | ≠ 3×21, 3×33 |
| 6 | 486 | 85, 401 | NEW | ≠ 3×79, 3×83 (but these are #3-4) |

**Key observation at k=6:** First time we see **coexistence** - both new modes (85,401) AND lifted modes (237,249) in the top-5, with very similar magnitudes (0.039 vs 0.038).

## Open Questions

1. **What determines j=85, 401 at k=6?** These are not Nyquist-neighbors (243±2), not lifts of k=5 tops. What's special about them?

2. **Why did Nyquist-neighbor prediction fail?** At k=5 you predicted 79,83 as Nyquist-neighbors (81±2) and that was correct. At k=6, 241,245 (243±2) completely failed. Why?

3. **Is the coexistence at k=6 significant?** The gap between #2 (0.0391) and #3 (0.0382) is only 2.4%. Is this "competition" or noise?

4. **What's the relationship between 85 and the dynamics?** 
   - 85 % 3 = 1 (new-digit mode)
   - 85 / 3 ≈ 28.33 (not a clean lift)
   - Any group-theoretic significance?

Looking forward to your interpretation of these surprising k=6 results!
