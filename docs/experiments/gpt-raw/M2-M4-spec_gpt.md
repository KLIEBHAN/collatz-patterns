# M2–M4 Experimental Specification (GPT 5.2 Pro extract)

Source: ChatGPT conversation `WEB:52812852-4763-42ea-a69e-be6c9c59a313` (extracted via `chatgpt-extract.sh`).

> Note: The extract contains unicode/math formatting artifacts; keep as-is for provenance.

---

M2 — Mixing / bias of accelerated odd map mod 
3
𝑘
3
k
Hypotheses

H2.1 (mixing): For fixed 
𝑘
k, the empirical distribution 
𝜇
𝑘
,
𝑡
μ
k,t
	​

 of 
𝑇
𝑡
(
𝑛
)
 
m
o
d
 
3
𝑘
T
t
(n)mod3
k
 (for odd 
𝑛
∼
Unif
{
1..
𝑁
}
n∼Unif{1..N}) approaches a time-stable distribution 
𝜋
𝑘
π
k
	​

 as 
𝑡
t grows (after a short burn-in).

H2.2 (bias structure): 
𝜋
𝑘
π
k
	​

 is not uniform on 
(
𝑍
/
3
𝑘
𝑍
)
×
(Z/3
k
Z)
×
; deviations are stable across 
𝑁
N and reflect intrinsic Syracuse bias (not a sampling artifact).

Metrics

Let 
𝑈
𝑘
=
(
𝑍
/
3
𝑘
𝑍
)
×
U
k
	​

=(Z/3
k
Z)
×
 (size 
∣
𝑈
𝑘
∣
=
2
⋅
3
𝑘
−
1
∣U
k
	​

∣=2⋅3
k−1
). Define empirical histogram:

𝜇
𝑘
,
𝑡
(
𝑟
)
=
Pr
⁡
[
𝑇
𝑡
(
𝑛
)
≡
𝑟
 
(
mod 
3
𝑘
)
]
,
𝑟
∈
𝑈
𝑘
.
μ
k,t
	​

(r)=Pr[T
t
(n)≡r (mod 3
k
)],r∈U
k
	​

.

Convergence / stability:

TV distance: 
𝑑
TV
(
𝜇
,
𝜈
)
=
1
2
∑
𝑟
∈
𝑈
𝑘
∣
𝜇
(
𝑟
)
−
𝜈
(
𝑟
)
∣
d
TV
	​

(μ,ν)=
2
1
	​

∑
r∈U
k
	​

	​

∣μ(r)−ν(r)∣.

KL divergence: 
𝐷
KL
(
𝜇
∥
𝜈
)
=
∑
𝑟
𝜇
(
𝑟
)
log
⁡
𝜇
(
𝑟
)
𝜈
(
𝑟
)
D
KL
	​

(μ∥ν)=∑
r
	​

μ(r)log
ν(r)
μ(r)
	​

 (use add-
𝜖
ϵ smoothing).

Chi-square: 
𝜒
2
(
𝜇
,
𝜈
)
=
∑
𝑟
(
𝜇
(
𝑟
)
−
𝜈
(
𝑟
)
)
2
𝜈
(
𝑟
)
χ
2
(μ,ν)=∑
r
	​

ν(r)
(μ(r)−ν(r))
2
	​

 (requires 
𝜈
(
𝑟
)
>
0
ν(r)>0).

Operational convergence: for a fixed “reference time” 
𝑡
⋆
t
⋆
	​

 (late), measure 
𝑑
TV
(
𝜇
𝑘
,
𝑡
,
𝜇
𝑘
,
𝑡
⋆
)
d
TV
	​

(μ
k,t
	​

,μ
k,t
⋆
	​

	​

) for 
𝑡
<
𝑡
⋆
t<t
⋆
	​

.

Design

Sample odd 
𝑛
n uniformly from 
[
1
,
𝑁
]
[1,N]. Track orbit 
𝑛
𝑖
=
𝑇
𝑖
(
𝑛
)
n
i
	​

=T
i
(n) for 
𝑖
=
0..
𝑡
max
⁡
i=0..t
max
	​

.

At each 
𝑡
t, record 
𝑟
𝑘
,
𝑡
=
𝑛
𝑡
 
m
o
d
 
3
𝑘
r
k,t
	​

=n
t
	​

mod3
k
 only if 
𝑛
𝑡
≢
0
(
m
o
d
3
)
n
t
	​


≡0(mod3) (expected after first step, but still enforce).

Compute 
𝜇
𝑘
,
𝑡
μ
k,t
	​

 for each 
𝑘
,
𝑡
k,t.

Holdout check: repeat on disjoint ranges (e.g., 
[
1
,
𝑁
/
2
]
[1,N/2] vs 
(
𝑁
/
2
,
𝑁
]
(N/2,N]) or two independent hash-samples; compare resulting 
𝜇
𝑘
,
𝑡
μ
k,t
	​

.

Parameters

Suggested 
𝑘
∈
{
1
,
…
,
8
}
k∈{1,…,8} (optionally 9–10 if counts per bin stay high).

𝑡
∈
{
0
,
…
,
60
}
t∈{0,…,60} with focus on 
𝑡
≤
40
t≤40 for mixing curves; pick 
𝑡
⋆
=
50
t
⋆
	​

=50 as “late” reference.

Sample size: target 
≥
200
⋅
∣
𝑈
𝑘
∣
≥200⋅∣U
k
	​

∣ samples per 
(
𝑘
,
𝑡
)
(k,t) bin for stable chi-square; for 
𝑘
=
8
k=8, 
∣
𝑈
𝑘
∣
=
2
⋅
3
7
=
4374
∣U
k
	​

∣=2⋅3
7
=4374, so 
∼
10
6
∼10
6
 samples is ample. Full sweep up to 50M odds is overkill; hashed subsample 
𝑆
∼
1
–
5
S∼1–5M is fine.

Interpretation

Rapid decay of 
𝑑
TV
(
𝜇
𝑘
,
𝑡
,
𝜇
𝑘
,
𝑡
⋆
)
d
TV
	​

(μ
k,t
	​

,μ
k,t
⋆
	​

	​

) with 
𝑡
t supports a “near-stationary residue bias” usable in drift modeling.

Stable non-uniform 
𝜋
𝑘
π
k
	​

 across 
𝑁
N indicates intrinsic bias (candidate for residue-corrected potentials).

Failure modes

Conditioning artifacts: sampling only odds is correct for odd-map dynamics but must be consistent across 
𝑡
t. Don’t mix “all integers” with “odds only.”

Multiplicity-of-3 handling: since 
𝑇
T is defined on odds and outputs odds, mod 
3
𝑘
3
k
 state space should be restricted to units; accidentally including residue 0 corrupts distances.

Small-
𝑛
n attractor bias: late-time samples overrepresent small values because many trajectories fall; mitigate by (i) restricting analysis to early 
𝑡
t, (ii) reporting results with and without excluding samples where 
𝑛
𝑡
≤
𝑛
min
⁡
n
t
	​

≤n
min
	​

 (e.g., 
𝑛
min
⁡
=
10
6
n
min
	​

=10
6
).

Finite-
𝑁
N edge effects: validate stability across disjoint 
𝑛
n-ranges.

M3 — Distribution & autocorrelation of 
𝑎
(
𝑛
)
=
𝑣
2
(
3
𝑛
+
1
)
a(n)=v
2
	​

(3n+1) under evolved measure
Hypotheses

H3.1: Marginal 
𝑎
𝑡
:
=
𝑎
(
𝑛
𝑡
)
a
t
	​

:=a(n
t
	​

) is close to geometric on 
{
1
,
2
,
…
 
}
{1,2,…} under the evolved measure at moderate 
𝑡
t (possibly with residue-dependent deviations).

H3.2: Autocorrelation of 
(
𝑎
𝑡
)
(a
t
	​

) decays quickly (short memory), possibly faster after conditioning on residue 
𝑛
𝑡
 
m
o
d
 
3
𝑘
n
t
	​

mod3
k
.

Metrics

Histograms 
𝑝
𝑡
(
𝑗
)
=
Pr
⁡
[
𝑎
𝑡
=
𝑗
]
p
t
	​

(j)=Pr[a
t
	​

=j], for 
𝑗
=
1..
𝐽
j=1..J (cap 
𝐽
∼
30
J∼30, aggregate tail).

Fit to geometric 
𝑞
𝜃
(
𝑗
)
=
(
1
−
𝜃
)
𝑗
−
1
𝜃
q
θ
	​

(j)=(1−θ)
j−1
θ; compare via TV/KL, and report MLE 
𝜃
^
𝑡
θ
^
t
	​

.

Conditional histograms 
𝑝
𝑡
,
𝑟
(
𝑗
)
=
Pr
⁡
[
𝑎
𝑡
=
𝑗
∣
𝑛
𝑡
 
m
o
d
 
3
𝑘
=
𝑟
]
p
t,r
	​

(j)=Pr[a
t
	​

=j∣n
t
	​

mod3
k
=r].

Autocorrelation: 
𝜌
(
ℓ
)
=
C
o
r
r
(
𝑎
𝑡
,
𝑎
𝑡
+
ℓ
)
ρ(ℓ)=Corr(a
t
	​

,a
t+ℓ
	​

) (pooled over 
𝑡
t in a window), plus mutual information 
𝐼
(
𝑎
𝑡
;
𝑎
𝑡
+
ℓ
)
I(a
t
	​

;a
t+ℓ
	​

) as a non-linear dependence check.

Design

Choose a “stationary-ish” time window 
𝑡
∈
[
𝑡
0
,
𝑡
1
]
t∈[t
0
	​

,t
1
	​

] (from M2 mixing curves), e.g. 
𝑡
0
=
15
,
𝑡
1
=
35
t
0
	​

=15,t
1
	​

=35.

For sampled trajectories, record 
𝑎
𝑡
a
t
	​

 for 
𝑡
∈
[
𝑡
0
,
𝑡
1
]
t∈[t
0
	​

,t
1
	​

] and residues 
𝑟
=
𝑛
𝑡
 
m
o
d
 
3
𝑘
r=n
t
	​

mod3
k
.

Compute global 
𝑝
(
𝑗
)
p(j) pooled over 
𝑡
∈
[
𝑡
0
,
𝑡
1
]
t∈[t
0
	​

,t
1
	​

], and conditional 
𝑝
𝑟
(
𝑗
)
p
r
	​

(j) for each residue (or coarse bins if data sparse).

Compute 
𝜌
(
ℓ
)
ρ(ℓ) for 
ℓ
=
1..
𝐿
ℓ=1..L (e.g., 
𝐿
=
20
L=20), both unconditional and conditional on residue classes (or by residualizing: subtract 
𝐸
[
𝑎
∣
𝑟
]
E[a∣r]).

Parameters

𝑘
∈
{
4
,
6
,
8
}
k∈{4,6,8} (tradeoff between resolution and per-state counts).

𝐽
=
30
J=30, tail bin 
𝑗
>
𝐽
j>J.

Sample size: 
≥
10
6
≥10
6
 state-visits in window; for conditional on 
𝑘
=
8
k=8, consider aggregating residues by 
𝑟
 
m
o
d
 
3
𝑘
′
rmod3
k
′
 with 
𝑘
′
<
𝑘
k
′
<k if sparse.

Interpretation

Close-to-geometric 
𝑝
(
𝑗
)
p(j) supports drift heuristics; systematic residue-dependent deviations identify “danger residues.”

Correlation length estimate: smallest 
ℓ
ℓ with 
∣
𝜌
(
ℓ
)
∣
<
𝜏
∣ρ(ℓ)∣<τ (e.g., 
𝜏
=
0.02
τ=0.02) consistently across holdouts.

Failure modes

Evolved-measure bias: pooling over 
𝑡
t too late overweights small 
𝑛
n; stick to mixing window, and report sensitivity to 
𝑡
0
,
𝑡
1
t
0
	​

,t
1
	​

.

Tail noise: large 
𝑗
j rare; always aggregate tail and report confidence intervals (bootstrap over trajectories).

M4 — Drift measurement: 
𝐸
[
Δ
log
⁡
𝑛
]
E[Δlogn] and state-dependent drift
Hypotheses

H4.1: Mean drift 
𝐸
[
Δ
𝑡
]
E[Δ
t
	​

] is negative in the mixing window, where 
Δ
𝑡
=
log
⁡
𝑛
𝑡
+
1
−
log
⁡
𝑛
𝑡
Δ
t
	​

=logn
t+1
	​

−logn
t
	​

.

H4.2: Drift depends on residue 
𝑟
=
𝑛
𝑡
 
m
o
d
 
3
𝑘
r=n
t
	​

mod3
k
; a small set of residues have less-negative or positive drift (“bad states”).

Metrics

Δ
𝑡
=
log
⁡
(
𝑛
𝑡
+
1
)
−
log
⁡
(
𝑛
𝑡
)
Δ
t
	​

=log(n
t+1
	​

)−log(n
t
	​

) (natural log).

Global drift 
Δ
ˉ
=
𝐸
[
Δ
𝑡
]
Δ
ˉ
=E[Δ
t
	​

] pooled over 
𝑡
∈
[
𝑡
0
,
𝑡
1
]
t∈[t
0
	​

,t
1
	​

].

State drift 
𝑔
(
𝑟
)
=
𝐸
[
Δ
𝑡
∣
𝑛
𝑡
 
m
o
d
 
3
𝑘
=
𝑟
]
g(r)=E[Δ
t
	​

∣n
t
	​

mod3
k
=r].

“Badness” score: 
𝑏
(
𝑟
)
=
𝑔
(
𝑟
)
−
m
e
d
i
a
n
𝑟
′
𝑔
(
𝑟
′
)
b(r)=g(r)−median
r
′
	​

g(r
′
) or simply rank by 
𝑔
(
𝑟
)
g(r).

Uncertainty: standard errors per state; require minimum count per state (e.g., 
≥
5000
≥5000).

Design

Use same time window 
[
𝑡
0
,
𝑡
1
]
[t
0
	​

,t
1
	​

] as M3.

For each state visit, compute 
Δ
𝑡
Δ
t
	​

 and accumulate sums/counts globally and per residue.

Identify bad states as those with:

𝑔
(
𝑟
)
≥
0
g(r)≥0 (strong criterion), or

top 
1
%
1% by 
𝑔
(
𝑟
)
g(r) with CI excluding global mean.

Parameters

𝑘
∈
{
6
,
8
}
k∈{6,8}; 
𝑡
0
,
𝑡
1
t
0
	​

,t
1
	​

 from M2.

Optional robustness: compute drift for block steps 
Δ
(
𝑚
)
=
log
⁡
𝑛
𝑡
+
𝑚
−
log
⁡
𝑛
𝑡
Δ
(m)
=logn
t+m
	​

−logn
t
	​

 for 
𝑚
∈
{
5
,
10
,
20
}
m∈{5,10,20}.

Interpretation

Uniform negativity of 
𝑔
(
𝑟
)
g(r) (for some 
𝑘
k) is a concrete “finite-state drift certificate” candidate (still conjectural).

If only few bad states exist, focus later work on proving or forcing escape from them (candidate reduction).

Failure modes

Survivorship bias: trajectories that descend quickly contribute more late-time samples at small 
𝑛
n; limit to mixing window and report sensitivity.

State sparsity: for larger 
𝑘
k, many residues under-sampled; enforce count thresholds and/or reduce 
𝑘
k.

Repo documentation (minimal, reproducible)

experiments/M2_mixing/

config.yaml (N, sample method, k list, t range, t_star)

counts_mu_k_t.npz (histograms)

mixing_metrics.csv (TV/KL/chi2 vs t)

report.md (plots + narrative)

experiments/M3_a_dist/

hist_a_global.csv, hist_a_by_residue_k{K}.parquet

autocorr_a.csv, fits_geometric.csv

report.md

experiments/M4_drift/

drift_global.csv, drift_by_residue_k{K}.parquet

bad_states_k{K}.csv (with counts, CIs)

Naming: N{N}_S{S}_k{K}_t{t0}-{t1}_seed{seed}_git{sha} embedded in filenames; all plots generated by scripts that read only these artifacts.
