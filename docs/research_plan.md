# Proof-directed Collatz research plan (draft)

This plan treats computation as **instrumentation for proof ideas** (drift, mixing, finite-state reductions), not as “just push N higher”.

We focus on the **accelerated odd map** (Syracuse map):

\[
T(n) = \frac{3n+1}{2^{a(n)}},\quad a(n)=v_2(3n+1),\quad n\ \text{odd}.
\]

Heuristic log-increment:
\[
\Delta \log n \approx \log 3 - a(n)\log 2.
\]
If \(a\) behaved like i.i.d. geometric(mean 2), then \(\mathbb E[\Delta \log]\approx \log(3/4)<0\) (negative drift). The core difficulty: the orbit induces **bias** and **state-dependence**.

## Stage 0 — Definitions & proof-shaped targets

Track along odd-only orbits:
- orbit: \(n_{i+1}=T(n_i)\)
- exponents: \(a_i=v_2(3n_i+1)\)
- log increment: \(\Delta_i=\log n_{i+1}-\log n_i\)

Proof-shaped targets (increasingly realistic):
1. **Lyapunov function** \(V\) with one-step descent except on controlled exceptions.
2. **Block version**: \(V(T^m(n))\le V(n)-\delta\) for fixed \(m\).
3. **Finite-state drift**: project to residues / short memory states and prove uniform negative drift + mixing (Foster–Lyapunov style).

## Stage 1 — Candidate potentials / invariants

1. **Baseline**: \(V_0(n)=\log n\).
2. **Residue-corrected potential**:
   \[
   V_k(n)=\log n + \psi_k(n\bmod 3^k)
   \]
   Choose \(\psi_k\) to “absorb” residue-dependent drift (Poisson equation / Markov-chain correction).
3. **Short-memory state**: \(S(n)=(n\bmod 3^k, a_0,\dots,a_{m-1})\) for small \(m\), and \(V(n)=\log n+\psi(S(n))\).
4. **Criticality defect**: with \(A_j=\sum_{i<j} a_i\), define
   \[
   D_j = A_j - j\log_2 3.
   \]
   Large positive \(D_j\) suggests descent; near-zero \(D_j\) corresponds to record-holders.
5. **Backward-tree / inequality approach**: connect to Krasikov–Lagarias style difference inequalities (proof-relevant but heavier).

## Stage 2 — Proof-relevant empirical hypotheses

Design tests so that *if true*, they suggest specific lemmas.

1. **Mixing modulo \(3^k\)**: distribution of \(T^t(n)\bmod 3^k\) (for modest \(k\le 8\), \(t\le 50\)) converges quickly to a stable \(\pi_k\).
2. **Distribution of \(a(n)=v_2(3n+1)\)** under the *evolved* measure: close to geometric; short-range correlations only.
3. **State-dependent drift**: conditional mean \(\mathbb E[\Delta\log\mid n\bmod 3^k=r]\) is negative after adding a correction \(\psi_k\).
4. **Record-holder structure**: top stopping-time outliers have distinctive residue / \(a\)-sequence / defect-profile signatures.

## Stage 3 — Concrete experiments (5–10)

1. Estimate \(\pi_k\) for \(k=1..8\) at times \(t=0..50\); measure TV-distance / KL divergence vs \(t\).
2. Measure empirical \(P(a=m\mid\text{state})\) under evolved distribution; fit geometric; quantify deviations.
3. Measure autocorrelation of \(a_i\) along orbits; determine memory length.
4. Compute \(\mathbb E[\Delta\log n\mid r]\) for residues \(r\bmod 3^k\); identify worst-case residues.
5. Solve for \(\psi_k\) numerically (Poisson equation on a finite Markov approximation) and test whether \(\Delta V_k\) concentrates negative.
6. Compare feature distributions (popcount, mod classes, Ω(n), etc.) between baseline population and top-N record-holders.
7. For record-holders, compute defect profiles \(D_j\) vs \(j\); look for recurring near-critical block motifs.
8. Test “bad blocks”: frequency of consecutive small \(a\) events (e.g. \(a\in\{1,2\}\) runs) and whether they explain long stopping times.

## Stage 4 — What counts as real progress

- A **finite-state inequality** / Foster–Lyapunov drift condition with explicit constants (even for a restricted subset) that can be upgraded.
- A validated \(\psi_k\) correction giving uniformly negative drift across residue states (or a tight classification of the exceptional states).
- A lemma bounding the density/impact of “near-critical blocks” (runs with insufficient halving).

## Guardrails against overfitting

- Pre-register hypotheses/metrics before looking at new ranges.
- Train/test split by intervals (e.g. 0–50M train, 50–100M test).
- Prefer effect sizes + confidence bounds over cherry-picked maxima.

## References to anchor against

- Terence Tao’s work on the Syracuse / accelerated Collatz map and bias/mixing issues.
- Lagarias / Terras surveys.
- Krasikov–Lagarias difference inequalities; Applegate–Lagarias computational strengthening.
