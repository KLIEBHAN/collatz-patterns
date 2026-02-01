# Lemma (K) Empirical Analysis: The Buffer Effect

**Date:** 2026-02-01 23:00 UTC
**Status:** ✅ RESOLVED — (K) holds empirically but is theoretically weak

---

## Summary

We tested Lemma (K) empirically and found it **holds for all tested cases** with C ≈ 2.42. However, deeper analysis reveals this is due to a "buffer effect" — orbits terminate before exhausting their budget, NOT because the underlying dynamics satisfy (K).

---

## Lemma (K) Statement

```
Σᵢ₌₀ᵗ⁻¹ 𝟙{a(Tⁱ(n))=1} ≤ θt + C·log₂(n)
```

With θ = 0.415, C ≈ 2.42.

---

## Empirical Results

### Test Summary

| Parameter | Value |
|-----------|-------|
| θ (critical density) | 0.415 |
| Minimum C for all tests | ≈ 2.42 |
| Candidates tested | ~2500 |
| Worst case | n = 63728127 |

### Key Test Cases

| n | Steps | #a=1 | Ratio | Holds? |
|---|-------|------|-------|--------|
| 27 | 41 | 24 | 0.585 | ✅ (with C≥2) |
| 8400511 | 256 | 152 | 0.594 | ✅ (with C≥2.5) |
| 63728127 | 357 | 208 | 0.583 | ✅ (with C≥2.42) |

---

## The Paradox: Why Does (K) Hold?

### Observation 1: Actual Slope > θ

Looking at the empirical data:
- **Allowed slope (θ):** 0.415
- **Actual slope:** ~0.50 (consistently across all orbits)

The orbits are "sinning" — they accumulate a=1 steps faster than θ allows!

### Observation 2: But No Violation Found

Despite the wrong slope, no orbit actually violates (K). Why?

---

## The Resolution: The Buffer Effect

### The Math

(K) is violated when:
```
count_a1 > θ·t + C·log₂(n)
```

If the actual slope is p ≈ 0.50, then:
```
count_a1 ≈ p·t = 0.50·t
```

The "excess consumption" per step is:
```
p - θ = 0.50 - 0.415 = 0.085
```

### Break-Even Point

The buffer C·log₂(n) is exhausted when:
```
(p - θ)·t* = C·log₂(n)

t* = C·log₂(n) / (p - θ)
t* ≈ 2.42 · log₂(n) / 0.085
t* ≈ 28.5 · log₂(n)
```

### The Key Insight

**Orbits terminate BEFORE reaching the break-even point!**

| n | log₂(n) | Break-even t* | Actual steps | Margin |
|---|---------|---------------|--------------|--------|
| 27 | 4.75 | ~135 | 41 | 94 steps |
| 8400511 | 23.0 | ~655 | 256 | 399 steps |
| 63728127 | 25.9 | ~738 | 357 | 381 steps |

Typical Collatz orbits have length O(log n) to O(log² n), which is much less than 28·log₂(n).

---

## Implications

### Why (K) is NOT a Good Proof Target

1. **(K) depends on termination:** It holds BECAUSE orbits terminate, not because of intrinsic dynamics
2. **Circular reasoning:** Using (K) to prove termination is circular — (K) already assumes orbits are short enough
3. **Would fail for infinite orbits:** A hypothetical non-terminating orbit would eventually break (K)

### The Correct Interpretation

> "(K) is practically useful but theoretically wobbly. For a rigorous proof, RTD (exponential waiting time) is safer because it corrects the SLOPE itself, not relying on a buffer."

### What We Actually Learned

1. ✅ **Empirically validated:** (K) holds for all tested terminating orbits
2. ⚠️ **Theoretically weak:** (K) is an artifact of finite orbit length
3. 🎯 **Better target:** RTD Lemma (Return-Time vs Depth) fixes the slope problem

---

## Comparison: (K) vs RTD

| Aspect | Lemma (K) | RTD Lemma |
|--------|-----------|-----------|
| What it controls | Cumulative a=1 count | Time between deep returns |
| Mechanism | Budget/buffer | Exponential spacing |
| Depends on termination? | Yes (implicitly) | No |
| Slope correct? | No (0.50 > 0.415) | Would correct it |
| Proof viability | Circular | Direct |

---

## Conclusion

**Lemma (K) is a useful empirical observation but not a viable proof target.**

The buffer C·log₂(n) hides the fact that orbits "sin" (have wrong slope) but "die before judgment" (terminate before violating the bound).

For a rigorous proof, we need RTD: prove that deep 2-adic returns are exponentially spaced, which would fix the slope directly rather than relying on orbit termination.

---

## Files

- `src/refuel_test.py` — Visual refueling test
- `src/test_lemma_k.py` — Systematic (K) verification
- `data/refuel_test.png` — Visualization
