# GPT 5.2 Pro Analysis: k=5 Fourier Results

Date: 2026-02-01
Thinking Time: ~20 minutes

---

## Key Insight: Why j=79,83 Dominate

### The "Lift vs New-Digit" Dichotomy

Characters with index **divisible by 3** = "lifts" (don't see new digit)
Characters with index **not divisible by 3** = "new-digit modes" (see the kernel)

**k=4 top modes (21,33):** divisible by 3 → mismatch lived in coarser mod 27 structure
**k=5 top modes (79,83):** NOT divisible by 3 → mismatch lives in the **new digit splitting**

### Why 79,83 Specifically?

Two telling numerologies:
1. **Conjugate pair:** 79 + 83 = 162 = |G₅| ✓
2. **Nyquist-neighbors:** 79 = 81-2, 83 = 81+2 where |G₅|/2 = 81

**"Nyquist-neighbor"** = classic signature of localized/high-contrast error in discrete-log coordinate.

### Concrete Mechanism

At k=5, the main mismatch is NOT "which mod-81 classes have what mass" (that would create lift modes).

Instead: **"given a mod-81 class b, how is its mass split among the three lifts b, b+81, b+162?"**

That error lives in the kernel direction (size 3), and projects to Nyquist-neighbor modes when sharply localized.

---

## The Pattern Explained

**Whichever layer is currently the bottleneck dominates the Fourier error.**

| k | Top Targets | Divisible by 3? | Interpretation |
|---|-------------|-----------------|----------------|
| 3 | 7, 11 | No | New digit at k=3 is bottleneck |
| 4 | 21, 33 | Yes | Inherited from k=3 (new digit OK) |
| 5 | 79, 83 | No | New digit at k=5 is bottleneck again |

This explains TV increasing (0.8% → 2% → 3% → 5.2%): deeper 3-adic digits are harder to "equilibrate".

---

## Prediction for k=6

φ(3⁶) = 486, Nyquist = 243

**Two scenarios:**

1. **If k=6 mismatch is inherited from k=5:**
   - Top modes will be lifts: **j = 237 (3×79), 249 (3×83)**
   - Also 105 (3×35), 381 (3×127)

2. **If k=6 mismatch is new-digit splitting:**
   - Top modes will be Nyquist-neighbors: **j = 241 (243-2), 245 (243+2)**

**GPT's prediction:** Both families will be visible. Which is #1 tells you whether bottleneck is "inherited" or "new digit".

---

## Why -1 mod 81 is Likely the Culprit

Because π is spiky and maximized at -1 at every level:
- Small relative split error on heaviest base class → large absolute discrepancy
- Concentrates δ₁(b) around b ≡ -1 (mod 81)
- Exactly the localization that feeds Nyquist-neighbor modes

**Test:** Plot |δ₁(b)| vs b. If it spikes at b=80 (≡ -1 mod 81), you've explained the 79,83 dominance.

---

## Actionable Next Steps

### A. Lift-Splitting Decomposition (k=5)

For each base class b ∈ G₄ (units mod 81), define:
- **Coarse component:** Δ(b) = Σℓ δ(b,ℓ) [sum over three lifts]
- **Within-lift components:** 
  - δ₁(b) = Σℓ ω^ℓ δ(b,ℓ)
  - δ₂(b) = Σℓ ω^{2ℓ} δ(b,ℓ)
  
Where ω = e^{2πi/3} and δ(b,ℓ) = μ₅(b+81ℓ) - π₅(b+81ℓ)

**Check:**
1. Is energy mostly in δ₁/δ₂? (Should be, given non-lift winners)
2. Which base classes b contribute most? (Likely near -1)

### B. Time/Horizon Sensitivity

Compute Fourier differences at varying burn-in t:
- If j=79,83 amplitude **decays** with burn-in → mixing artifact
- If it **plateaus** → structural deterministic-vs-ideal mismatch

**Key:** Mixing artifacts are easiest to handle with Doeblin-style arguments.

---

## Bottom Line

> "79/83 are 'new-digit' (kernel-visible) Nyquist-neighbor modes, so they're screaming 'the dominant error at k=5 is in the splitting among the three lifts from mod 81 to mod 243', not in the coarse mod-81 distribution."

The "lift alternation" is naturally explained by which 3-adic layer is the current bottleneck.

---

*Analysis by ChatGPT 5.2 Pro, extracted 2026-02-01*
