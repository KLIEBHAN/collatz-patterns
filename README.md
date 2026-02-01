# Collatz Conjecture: Proof-Directed Analysis 🧮

**We proved that pure 3-adic methods CANNOT solve Collatz — and found where the real obstruction lives.**

This repository documents a systematic proof-directed investigation into the Collatz conjecture, including both positive results (what works) and negative results (what provably cannot work).

---

## 🔥 Key Discovery (2026-02-01)

### What We Proved

**A pure 3-adic Lyapunov function V(n) = log n + ψ(n mod 3^k) CANNOT provide uniform descent.**

There exists an explicit infinite family of counterexamples:
```
n ≡ -1 (mod 3^k)  AND  n ≡ -1 (mod 2^{m+1})
```

For these n:
1. All first m steps have a=1 (forced by 2-adic structure)
2. Growth by (3/2)^m
3. 3-adic residue stays at -1 → ψ cancels
4. V increases instead of decreasing

**The obstruction is 2-ADIC, not 3-adic!**

---

## The Real Structure

### The Fuel Metaphor

Define h(n) := ν₂(n+1) (2-adic valuation of n+1). Then:

- **a(n) = 1 ⟺ h(n) ≥ 2** (in the "bad" expanding regime)
- **h(T(n)) = h(n) - 1** when a=1 (exact countdown!)
- **h(n) - 1 is "fuel"** — each a=1 step burns one unit

Once h(n) = k ≥ 2, the next **k-1 steps are FORCED to be a=1**.

### The Three-Phase Model

| Phase | Boundary B | Behavior |
|-------|------------|----------|
| 🧊 **Crystalline** | ≤ 10 | Deterministic, 73% defects |
| 🌊 **Transition** | ~100 | Structure dissolves |
| 💧 **Liquid** | ≥ 1000 | **Bulk = Ideal** (noise only) |

The "Collatz structure" exists only at small n. In bulk, trajectories are statistically ideal.

---

## Current Status

### What We Know

| Result | Status |
|--------|--------|
| 3-adic ψ alone insufficient | ✅ **Proven** (explicit counterexamples) |
| Obstruction is 2-adic | ✅ **Identified** |
| Bulk behaves ideally | ✅ **Measured** (TV → 0 as 1/√N) |
| Fuel countdown structure | ✅ **Exact** (h decrements by 1) |

### 🎯 RTD Validated — "The Physics of Collatz"

**RTD Lemma (Return-Time vs Depth):**
> Waiting time for depth R scales as 2^(R-1)

**Empirically validated** with 100 orbits, ~360k data points:

| R | Avg Wait | Theory | Ratio |
|---|----------|--------|-------|
| 2-8 | 2, 4, 8, 16, 32, 64, 128 | 2^(R-1) | **0.92-1.00** ✅ |

**This is WHY Collatz works:**
```
To get R=10 fuel (9 a=1 steps):
→ Wait ~512 steps
→ Shrink by (3/4)^256 ≈ 10^{-32}
→ PULVERIZED before refueling!
```

Refueling is exponentially expensive. The "sin" (too many a=1) is paid for by the wait.

### Why (K) is Weak (But RTD is Strong)

| Aspect | (K) | RTD |
|--------|-----|-----|
| Mechanism | Buffer | Exponential cost |
| Circular? | Yes | **No** |
| Explains convergence? | Indirectly | **Directly** |

---

## Repository Structure

```
collatz-patterns/
├── src/
│   ├── refuel_test.py          # Visual refueling analysis
│   ├── test_lemma_k.py         # Lemma (K) verification
│   ├── noise_floor_test.py     # Bulk = ideal test
│   └── ...
├── docs/
│   ├── findings.md             # Complete experimental log
│   ├── theory.md               # Mathematical framework
│   └── experiments/            # Detailed analyses
│       ├── gpt-no-conspiracy-impossible-*.md
│       ├── gpt-key-lemma-attack-vectors-*.md
│       ├── gpt-key-lemma-deep-analysis-*.md
│       └── lemma-k-empirical-analysis-*.md
└── data/                       # Generated plots & results
```

---

## Quick Start

```bash
git clone https://github.com/KLIEBHAN/collatz-patterns.git
cd collatz-patterns
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib

# Key experiments
python src/test_lemma_k.py       # Test Lemma (K)
python src/refuel_test.py        # Visualize refueling
python src/noise_floor_test.py   # Verify bulk is noise
```

---

## The Path Forward

### Recommended Strategy

1. ~~Falsify (K)~~ ✅ Done — holds empirically
2. ⚠️ (K) is weak — depends on termination
3. 🎯 **RTD Lemma** — the correct target
4. Use **LTE** as mathematical lever

### What Would Constitute Progress

- Prove RTD for small fixed R (e.g., R=3,4)
- Formalize the LTE connection to return times
- Prove "almost all" RTD (weaker but rigorous)
- Find explicit counterexamples to RTD (if it's false)

---

## Key Insight

> "The Collatz problem is not about 3-adic mixing — it's about whether 2-adic neighborhoods of -1 can be visited too frequently by integer orbits."

The 2-adic extension of Collatz is conjugate to a Bernoulli shift (maximally chaotic). The hard part is showing that **positive integers** — a measure-zero subset — cannot realize the pathological patterns that exist in the full 2-adic space.

---

## References

- [Tao (2019): Almost All Collatz Orbits Attain Almost Bounded Values](https://arxiv.org/abs/1909.03562)
- [Lagarias: The 3x+1 Problem — An Annotated Bibliography](https://arxiv.org/abs/math/0309224)
- [Bernstein: The 3x+1 Map in Z_2](https://cr.yp.to/papers/collatz.pdf)

---

## What This Is (And Isn't)

### ✅ What it IS:
- A **negative result**: Pure 3-adic methods provably fail
- **Identification** of the true obstruction (2-adic)
- A **proof scaffold** with the missing brick precisely identified
- **Strong empirical evidence** supporting the framework

### ❌ What it is NOT:
- A proof of Collatz
- A claim that the problem is solved
- A bypass of the core number-theoretic difficulty

---

*Started: 2026-01-31 | Latest: 2026-02-01*  
*By [@KLIEBHAN](https://github.com/KLIEBHAN) with AI assistance (Claude + GPT)*

🦞 *"Sometimes proving something CANNOT work is the breakthrough."*
