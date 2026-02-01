# Collatz Conjecture: Bulk = Ideal 🧮

**TL;DR:** We found empirical evidence that Collatz dynamics behave *ideally* for large numbers. All the "weird structure" lives in a tiny boundary region near n=1.

---

## The Discovery

Using Markov chain analysis on 3-adic residues, we measured how Collatz trajectories deviate from an ideal stochastic model.

**Result:** At n > 1000, deviations are pure sampling noise. The "Collatz structure" only exists at small n.

### The Three-Phase Model

| Phase | n Range | Behavior |
|-------|---------|----------|
| 🧊 **Crystalline** | ≤ 10 | Deterministic, 73% deviation from ideal |
| 🌊 **Transition** | ~100 | "Ice melts", 11% deviation |
| 💧 **Liquid** | ≥ 1000 | **Bulk = Ideal**, ~0% true deviation |

The 73% "defect" at small n isn't mysterious — it's a **terminal funnel** (deterministic chute to 1):
```
61 → 23 → 35 → 53 → 5 → ... → 1
```

---

## Why This Matters

If bulk behavior is truly ideal, the Collatz conjecture reduces to:

1. ✅ **Bulk:** Already behaves ideally (our finding)
2. 🔄 **Bridge:** Show trajectories reach the bulk (Foster-Lyapunov)
3. ✅ **Boundary:** Finite verification (already done to 10²⁰+)

**📖 [Full theoretical framework →](docs/theory.md)** — Foster-Lyapunov setup, Bridge Lemma, proof roadmap

---

## Key Evidence

### Noise Floor Test (n > 100,000)

| Samples | TV Distance | TV × √N |
|---------|-------------|---------|
| 100k | 2.54% | 8.03 |
| 400k | 1.32% | 8.35 |
| 800k | 0.91% | 8.14 |

TV × √N is constant → **the deviation is sampling noise, not structure**.

### Signal vs Boundary

| Threshold B | True Signal |
|-------------|-------------|
| 10 | 9.6% ← real |
| 100 | 2.4% |
| 1000 | 0.8% |
| 10000+ | ~0% ← noise |

---

## Quick Start

```bash
git clone https://github.com/KLIEBHAN/collatz-patterns.git
cd collatz-patterns
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib

# Key experiments:
python src/noise_floor_test.py           # Verify bulk is noise
python src/b_sweep_analysis.py           # Phase transition
python src/transition_heatmap.py         # Conditional defects
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [findings.md](docs/findings.md) | Complete experimental log |
| [theory.md](docs/theory.md) | Mathematical framework |
| [Foster-Lyapunov](docs/experiments/gpt-foster-lyapunov-framework-2026-02-01.md) | Proof roadmap |

---

## Project Structure

```
collatz/
├── src/           # Analysis scripts
├── docs/          # Detailed documentation
│   ├── findings.md
│   ├── theory.md
│   └── experiments/
├── paper/         # Draft paper
└── data/          # Results (gitignored)
```

---

## ⚠️ The Deterministic Wall

This is **empirical evidence and a proof scaffold**, not a proof.

### What We Have:
- ✅ Empirical evidence that bulk behavior matches the ideal Markov model
- ✅ A Foster-Lyapunov framework that identifies exactly which lemmas would suffice
- ✅ Finite verification infrastructure

### What We Don't Have:
- ❌ A "no conspiracy" lemma proving uniform bounds for ALL n
- ❌ Transfer from "ε small in experiments" to "ε small for every starting point"

### The Core Issue:
> Collatz is **deterministic**. Our framework uses Markov chain theory. The gap between "random-like on average" and "no adversarial counterexample exists" is exactly the Collatz conjecture.

As GPT put it:
> "Your framework is a proof scaffold. It tells you exactly which lemmas would suffice. It becomes a proof only if you supply a precise no-conspiracy statement."

**📖 [Full critical assessment →](docs/experiments/gpt-critical-assessment-2026-02-01.md)**

---

## Links

- [Tao's "Almost All" Paper (2019)](https://arxiv.org/abs/1909.03562)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)

---

*Started: 2026-01-31 | Latest: 2026-02-01*  
*By [@KLIEBHAN](https://github.com/KLIEBHAN) with AI assistance*
