# M2–M4 Experimental Specification (v1)

This document is a **pre-registered spec** for the next proof-directed milestones. The goal is to measure *bias/mixing* and *state-dependent drift* of the accelerated odd Collatz map and produce artifacts that can plausibly support a proof-shaped argument (finite-state drift, Foster–Lyapunov criteria, etc.).

## Definitions (accelerated odd map)
For odd \(n\):
\[
T(n) = \frac{3n+1}{2^{a(n)}},\quad a(n)=v_2(3n+1)\in\mathbb N.
\]
Odd-only orbit: \(n_{i+1}=T(n_i)\).
Log increment:
\[
\Delta_i = \log n_{i+1}-\log n_i = \log(3n_i+1) - \log n_i - a(n_i)\log 2.
\]
(For large \(n\), \(\log(3n+1)-\log n\approx\log 3\).)

## Shared experimental setup
We will primarily use **sampling**, not full enumeration, to iterate quickly.

### Sampling
- Draw \(n\) uniformly from odd integers in \([1,N]\).
- Optionally exclude multiples of 3 in analyses that require invertibility mod \(3^k\) (document clearly).

### Parameter grid (default)
- \(N\in\{10^7, 5\cdot10^7\}\) (train), later \(N=10^8\) (test)
- \(k\in\{1,2,\dots,8\}\)
- \(t\in\{0,1,2,3,5,8,13,21,34,50\}\) (Fibonacci-like) + optional dense 0..50 for one run
- samples per config: start with \(S=200{,}000\), scale to \(S=2{,}000{,}000\) if noise is high

### Outputs (gitignored)
All outputs go to:
- `data/oddmap_stats/<run-id>/`

Run id format:
- `YYYYMMDD_HHMMZ_N{N}_S{S}_k{Kmax}_t{Tmax}`

Each run should write:
- `config.json`
- `m2_residue_distributions.parquet` (or csv)
- `m3_a_distributions.parquet`
- `m4_drift_by_state.parquet`
- `plots/*.png`

### Minimal code
Implement in:
- `src/oddmap_stats.py`

## M2 — Mixing / bias modulo \(3^k\)
### Hypotheses
H2.1: For moderate \(k\le 8\) and moderate times \(t\le 50\), the distribution of \(T^t(n)\bmod 3^k\) (restricted to units mod \(3^k\)) approaches a stable distribution \(\pi_k\) largely independent of \(N\) once \(N\) is large.

H2.2: Some residue classes are systematically over/under-represented (bias), and this bias is measurable and stable across \(N\) and across time windows.

### Metrics
For each \((k,t)\):
- empirical distribution \(p_{k,t}(r) = \Pr[T^t(n)\equiv r\ (\bmod\ 3^k)]\) over \(r\in (\mathbb Z/3^k\mathbb Z)^\times\)
- convergence to a reference distribution \(\hat\pi_k\) (estimated at largest \(t\), e.g. \(t=50\)):
  - total variation: \(\mathrm{TV}(p,\pi)=\tfrac12\sum_r |p(r)-\pi(r)|\)
  - optionally KL divergence (with smoothing)
- effective sample size diagnostics

### Design
For each sampled \(n\): compute \(n_t=T^t(n)\) for each \(t\) in grid, record \(n_t\bmod 3^k\).

### Interpretation
- Fast decay of TV vs \(t\) supports treating residue as approximately mixed after modest steps.
- Persistent bias indicates state dependence; this becomes input for M4/M5 (\(\psi_k\) correction).

### Failure modes / pitfalls
- Conditioning on odd (and/or excluding multiples of 3) changes measures; must document.
- Using \(T\) changes parity by construction; comparisons must be apples-to-apples.
- Small \(S\) will look noisy for large \(k\) (many states). Increase \(S\) or reduce \(k\).

## M3 — Distribution and autocorrelation of \(a(n)=v_2(3n+1)\) under evolved measure
### Hypotheses
H3.1: Under the evolved distribution (after \(t\) steps), \(a\) is close to geometric-like but with measurable state dependence.

H3.2: Autocorrelation of \(a_i\) along odd orbits decays quickly (short memory), allowing low-order Markov approximations.

### Metrics
For each \(t\):
- histogram \(\hat P_t(a=m)\), \(m\in\{1,2,\dots,m_{max}\}\)
- fitted geometric parameter \(\hat q_t\) (e.g., MLE) + goodness-of-fit distance (KS / chi-square)
- conditional histograms \(\hat P_t(a=m\mid r)\) for \(r\bmod 3^k\)
- autocorrelation \(\rho(\ell)=\mathrm{corr}(a_i,a_{i+\ell})\) for \(\ell\le 20\)
- run-length stats for “small a” blocks (e.g. \(a\in\{1,2\}\))

### Design
For each sampled \(n\): simulate odd-only orbit for \(t_{max}\) steps; record \(a_i\) along the way.

### Interpretation
- If \(a\) becomes approximately geometric with short memory, then drift arguments become more plausible (still not a proof).
- Strong state dependence implies we need residue-corrected potentials (M5).

### Failure modes
- If we only look at \(t=0\), we miss the bias induced by evolution; must include \(t>0\).

## M4 — Drift measurement (raw and state-dependent)
### Hypotheses
H4.1: The mean log drift \(\mathbb E[\Delta]\) is negative under the evolved measure, but not uniformly across residue states.

H4.2: A small subset of residue states are “worst” (least negative / near-critical drift) and correlate with record-holders.

### Metrics
- global \(\hat\mu_t = \mathbb E[\Delta\mid\text{time }t]\)
- state-dependent drift \(\hat\mu_{t}(r)=\mathbb E[\Delta\mid n_t\bmod 3^k=r]\)
- identify worst states: \(\arg\max_r \hat\mu_t(r)\) and quantiles

### Design
Compute \(\Delta_i\) from \(n_i\to n_{i+1}\) during simulation.
Aggregate by state \(r=n_i\bmod 3^k\) for a chosen \(k\).

### Interpretation
- If \(\max_r \hat\mu(r)\) is still negative (with confidence bounds), that suggests a route to a uniform drift certificate.
- If not, the set of bad states is the concrete object to attack (prove transient/rare, or fix with \(\psi_k\)).

### Failure modes
- Finite-sample noise for large \(k\) states; need \(S\) large or smaller \(k\).

## Documentation checklist
Each run must include:
- exact commit hash of code
- config.json with parameters
- summary markdown in `docs/experiments/runs/<run-id>.md`

## Train/Test discipline
- Use \([1,50M]\) samples as “train” for exploratory tuning.
- Freeze parameters/metrics, then validate on \([50M,100M]\) samples.
