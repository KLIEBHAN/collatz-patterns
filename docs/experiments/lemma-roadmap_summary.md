# Executive summary: GPT lemma-roadmap (M2–M4 → proof targets)

This is a short, human-usable summary of `docs/experiments/lemma-roadmap_gpt.md` (GPT 5.2 Pro extract). The goal is to keep us oriented toward **provable, finite objects**.

## The 5 lemma candidates (compressed)

### L1) Finite-state Markov reduction + spectral gap on mod \(3^k\)
**Claim-shape:** The process \(X_t = n_t \bmod 3^k\) (units modulo \(3^k\)) behaves like an ergodic Markov chain with stationary \(\pi_k\) and a spectral gap (or explicit TV-mixing rate).

**Why it matters:** Once you have a spectral gap, you get exponential decay of correlations for bounded observables and can use Poisson-equation / Foster–Lyapunov machinery.

**What supports it (M2):** Empirical transition matrices \(\hat P_k\) stable across N-bands, second eigenvalue \(|\lambda_2|<1-\gamma\), TV distance decays ~exp(-ct).

**Next experiments:** M2 with k=4..8, t up to 50, estimate \(\hat P_k\), \(\hat\pi_k\), \(|\hat\lambda_2|\).

---

### L2) Conditional geometric law for \(a(n)=v_2(3n+1)\) under the evolved measure
**Claim-shape:** Under the evolved distribution (after burn-in), \(a\) is close to geometric, possibly conditional on residue state \(r\bmod 3^k\), with short-range dependence.

**Why it matters:** This turns the log increment \(\Delta\log\approx \log 3 - a\log 2\) into a (nearly) negatively drifting additive functional.

**What supports it (M3):** Histograms at t>0 match geometric fits; conditional distributions vary mildly by state; autocorrelation decays quickly.

**Next experiments:** M3 at t ∈ {0,1,5,10,20,50}, plus conditional P(a|r) for k=6..8.

---

### L3) Poisson correction \(V(n)=\log n + \psi(n\bmod 3^k)\) yields uniform negative drift
**Claim-shape:** There exists \(\psi\) on residues so that the corrected potential has negative expected drift per step (or per block), uniformly over residue states, possibly excluding a controlled exceptional set.

**Why it matters:** This is the most “proof-shaped” bridge: a finite-dimensional object (\(\psi\) over finitely many states) implying descent.

**What supports it (M4 + M2):** Measured state-dependent drift \(\mu(r)\) is explainable/correctable by \(\psi\); after correction the worst-state drift becomes negative with margin.

**Next experiments:** M4 estimate \(\mu(r)=E[\Delta\log|r]\); then numerically solve a Poisson equation / least squares for \(\psi\) and validate on held-out samples.

---

### L4) Exponential rarity of “bad blocks” (large deviations)
**Claim-shape:** Blocks where halving is insufficient (too many small a’s) occur with exponentially small probability under the evolved measure; their contribution can be bounded.

**Why it matters:** Gives control over near-critical excursions that create record-holders.

**What supports it (M3):** Run-length distribution for a∈{1,2} (or threshold) has exponential tails; weak dependence supports large deviation bounds.

**Next experiments:** M3 run-length stats + conditional versions by residue state.

---

### L5) Conditional termination from block-descent + finite verification
**Claim-shape:** If you can prove a block-descent inequality outside a finite “bad set”, then checking the finite set (by brute force) closes the loop.

**Why it matters:** Converts infinite proof into (finite-state lemma) + (finite computation).

**What supports it:** Strongly negative block drift except in few motifs/states; empirically small “bad set”.

## Recommended starting parameters (practical)
- Start with **k=6..8**, **t_max=50**, and samples **S=200k** (smoke test) → **S=2M** (stable eigenvalue estimates).
- Keep train/test split: e.g. sample n from [1,50M] for tuning, validate on [50M,100M].

## What we should do next (order)
1) M2 estimate \(\hat P_k\), \(\hat\pi_k\), mixing rate / \(|\lambda_2|\).
2) M3 check a-distribution + correlation length + bad-block tails.
3) M4 compute drift by state; attempt \(\psi\)-correction (numerical) as a concrete object.

Links:
- Full GPT extract: `docs/experiments/lemma-roadmap_gpt.md`
