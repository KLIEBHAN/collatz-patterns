# Collatz Conjecture: A Conditional Reduction 🧮

**We reduce the Collatz conjecture to a single "No Conspiracy" lemma.**

If you can prove that arithmetic doesn't conspire against descent, our Foster-Lyapunov framework completes the proof. We provide empirical evidence that no such conspiracy exists — but proving it remains the hard open problem.

---

## What We Found

Using Markov chain analysis on 3-adic residues, we discovered a clear phase structure:

| Phase | n Range | Behavior |
|-------|---------|----------|
| 🧊 **Crystalline** | ≤ 10 | Deterministic terminal funnel |
| 🌊 **Transition** | ~100 | Structure dissolves |
| 💧 **Liquid** | ≥ 1000 | **Bulk = Ideal** (indistinguishable from random) |

The "Collatz structure" only exists at small n. For large n, trajectories behave exactly like an idealized stochastic model.

---

## The Reduction

We've transformed Collatz from:
> "Does every trajectory reach 1?"

To:
> "Can arithmetic conspire to produce infinite bad-block chains?"

### Theorem A (Our Contribution) ✅

**If** the deterministic Syracuse map satisfies a uniform no-conspiracy condition, **then** the Lyapunov function V(n) = log n + ψ(n mod 3^k) proves descent to a finite set, which can be verified computationally.

### Theorem B (The Open Problem) ❓

**Prove** the uniform no-conspiracy condition: that no starting integer can produce an infinite chain of low-valuation steps that defeats the expected negative drift.

**📖 [Full theoretical framework →](docs/theory.md)**

---

## The No-Conspiracy Lemma (What's Missing)

Formally, we need:

> **Uniform Block-Drift Lemma:** There exist m ≥ 1, k ≥ 1, δ > 0, B₀ such that for **every** odd n > B₀:
> 
> V(T^m(n)) - V(n) ≤ -δ

Our empirical evidence strongly suggests this holds. But "holds on average" ≠ "holds for every n". The gap is exactly the Collatz conjecture.

---

## Empirical Evidence

### Noise Floor Test (n > 100,000)

| Samples | TV Distance | TV × √N |
|---------|-------------|---------|
| 100k | 2.54% | 8.03 |
| 400k | 1.32% | 8.35 |
| 800k | 0.91% | 8.14 |

TV × √N constant → deviation is sampling noise, not structure.

### Tao Comparison

| Approach | Target | Status |
|----------|--------|--------|
| Tao (2019) | "Almost all" (log density) | ✅ Proven |
| Our framework | "All n > B₀" | Reduces to No-Conspiracy Lemma |

---

## Quick Start

```bash
git clone https://github.com/KLIEBHAN/collatz-patterns.git
cd collatz-patterns
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib

python src/noise_floor_test.py           # Verify bulk is noise
python src/finite_verification.py        # Verify small set
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [theory.md](docs/theory.md) | Mathematical framework + No-Conspiracy Lemma |
| [findings.md](docs/findings.md) | Complete experimental log |
| [Critical Assessment](docs/experiments/gpt-critical-assessment-2026-02-01.md) | Why this is a reduction, not a proof |
| [Foster-Lyapunov](docs/experiments/gpt-foster-lyapunov-framework-2026-02-01.md) | Paper-ready framework |

---

## What This Is (And Isn't)

### ✅ What it IS:
- A **conditional proof**: "If No-Conspiracy, then Collatz"
- A **proof scaffold** that identifies exactly which lemma would suffice
- **Strong empirical evidence** that the lemma likely holds
- A **transformation** of the problem into a precise mathematical statement

### ❌ What it is NOT:
- A proof of Collatz for all n
- A bypass of the core number-theoretic difficulty
- A claim that statistics can solve a deterministic problem

---

## The Demon Analogy

Think of it as a game against an adversary:

- **Our simulations:** Random starting values. The demon loses on average.
- **A proof:** The demon picks the starting value maliciously. He searches for the one number that breaks our drift condition.
- **No-Conspiracy Lemma:** Proves the demon has no winning move — arithmetic forbids it.

Simulations can't defeat the demon because he hides in the gaps of probability.

---

## Links

- [Tao's "Almost All" Paper (2019)](https://arxiv.org/abs/1909.03562)
- [Lagarias Survey](https://arxiv.org/abs/math/0309224)

---

*Started: 2026-01-31 | Latest: 2026-02-01*  
*By [@KLIEBHAN](https://github.com/KLIEBHAN) with AI assistance*
