# Proof-oriented lemma candidates (GPT 5.2 Pro extract)

Source: ChatGPT response extracted via `~/clawd/scripts/chatgpt-extract.sh` (see `/tmp/lemma_candidates.txt`).

---

Here’s a proof‑oriented roadmap that takes your M2–M4 measurements and tries to compress them into a small set of lemma-shaped targets—each one something a human could plausibly prove with finite‑state methods, explicit constants, and controlled exceptional sets.

 

One meta‑remark up front: what you’re doing (mod‑
3
𝑘
3
k
 mixing + drift control) is very much in the same “shape” as the hard technical ingredient in Terence Tao’s “almost all” result, where a key step is bounding characteristic functions of a skew random walk on a 
3
3-adic cyclic group. 
arXiv
 That doesn’t give you a proof for free—but it’s a strong hint that your chosen observables (M2–M4) are aimed at real proof bottlenecks, not decorative statistics.

 

Below, I’ll write the candidates as “lemmas”, but you should read them as proof targets (some are conditional on making the “evolved measure” precise).

Lemma candidate 1 — Finite‑state Markov reduction and spectral gap on 
 
m
o
d
 
3
𝑘
mod3
k
1) Precise statement (conditional but crisp)

Fix 
𝑘
≥
1
k≥1. Let 
𝑆
𝑘
:
=
(
𝑍
/
3
𝑘
𝑍
)
×
S
k
	​

:=(Z/3
k
Z)
×
 (the units; equivalently residue classes not divisible by 
3
3).
For an odd starting integer 
𝑛
0
n
0
	​

, define the Syracuse trajectory 
𝑛
𝑡
+
1
=
𝑇
(
𝑛
𝑡
)
n
t+1
	​

=T(n
t
	​

) and the state process

𝑋
𝑡
:
=
𝑛
𝑡
(
m
o
d
3
𝑘
)
∈
𝑆
𝑘
(
𝑡
≥
1
)
.
X
t
	​

:=n
t
	​

(mod3
k
)∈S
k
	​

(t≥1).

(As you know, 
3
∤
𝑛
𝑡
3∤n
t
	​

 for all 
𝑡
≥
1
t≥1, so the state really does live in 
𝑆
𝑘
S
k
	​

.)

 

Lemma target (Markovization + mixing). There exists a time‑homogeneous Markov kernel 
𝑃
𝑘
P
k
	​

 on 
𝑆
𝑘
S
k
	​

, a stationary distribution 
𝜋
𝑘
π
k
	​

, and constants 
𝐶
𝑘
<
∞
C
k
	​

<∞, 
0
<
𝜌
𝑘
<
1
0<ρ
k
	​

<1 such that the following holds for the “evolved measure” 
𝜇
μ you are using:

If 
𝑛
0
∼
𝜇
n
0
	​

∼μ and 
𝑋
𝑡
X
t
	​

 is defined as above, then for all 
𝑡
≥
0
t≥0,

∥
𝐿
(
𝑋
𝑡
)
−
𝜋
𝑘
∥
T
V
≤
𝐶
𝑘
 
𝜌
𝑘
 
𝑡
.
	​

L(X
t
	​

)−π
k
	​

	​

TV
	​

≤C
k
	​

ρ
k
t
	​

.

Moreover, the joint law of 
(
𝑋
𝑡
,
𝑋
𝑡
+
1
)
(X
t
	​

,X
t+1
	​

) is exactly (or up to a quantified 
𝜀
𝑘
ε
k
	​

) given by 
𝜋
𝑘
(
𝑥
)
𝑃
𝑘
(
𝑥
,
𝑦
)
π
k
	​

(x)P
k
	​

(x,y).

A slightly weaker (often easier) version is: there is a spectral gap,

𝜆
2
(
𝑃
𝑘
)
≤
1
−
𝛾
𝑘
for some 
𝛾
𝑘
>
0
,
λ
2
	​

(P
k
	​

)≤1−γ
k
	​

for some γ
k
	​

>0,

in the 
ℓ
2
(
𝜋
𝑘
)
ℓ
2
(π
k
	​

) sense.

2) Why this matters

This turns your infinite deterministic system into a finite, analyzable object: an ergodic chain on 
𝑆
𝑘
S
k
	​

. Once you have a spectral gap, you get:

exponential decay of correlations for any bounded observable of 
𝑋
𝑡
X
t
	​

;

the machinery you need for Poisson equations, additive functionals, large deviations, and Foster–Lyapunov criteria.

In other words: this lemma is the bridge from “we saw mixing” to “we can actually prove drift/recurrence statements with constants.”

3) What M2 evidence supports it

Strong support looks like:

Empirical transition matrix 
𝑃
^
𝑘
P
k
	​

 (estimated from long runs under your evolved measure) has:

a clear stationary vector 
𝜋
^
𝑘
π
k
	​

 (often close to uniform on 
𝑆
𝑘
S
k
	​

);

a stable estimate of the second eigenvalue magnitude 
∣
𝜆
^
2
∣
∣
λ
^
2
	​

∣ bounded away from 1;

Total variation (or chi‑square) distance of 
𝑋
𝑡
X
t
	​

 from 
𝜋
^
𝑘
π
k
	​

 decays roughly exponentially in 
𝑡
t, and the rate is robust across:

different initial distributions (uniform in an interval vs log‑weighted vs conditioned on size),

different magnitude bands of 
𝑛
n.

4) Plausible proof strategy

Two human‑scale routes:

 

(A) Fourier/spectral route on 
𝑍
/
3
𝑘
𝑍
Z/3
k
Z
Prove decay of Fourier coefficients of the pushforward distribution:

∣
𝐸
 
𝑒
2
𝜋
𝑖
𝜉
𝑋
𝑡
/
3
𝑘
∣
≤
𝐶
 
𝜌
𝑡
(
𝜉
≠
0
)
.
	​

Ee
2πiξX
t
	​

/3
k
	​

≤Cρ
t
(ξ

=0).

This is exactly the kind of “high frequency” control that appears in Tao’s approach to Syracuse. 
arXiv

Your empirical M2 can tell you which frequencies are the last to die, i.e., where the proof effort needs to go.

 

(B) Doeblin/minorization route (finite‑step smoothing)
Try to prove there exists 
𝑚
=
𝑚
(
𝑘
)
m=m(k) and 
𝜂
>
0
η>0 such that

𝑃
𝑘
𝑚
(
𝑥
,
⋅
)
≥
𝜂
 
𝜈
(
⋅
)
∀
𝑥
∈
𝑆
𝑘
P
k
m
	​

(x,⋅)≥ην(⋅)∀x∈S
k
	​


for some reference measure 
𝜈
ν on 
𝑆
𝑘
S
k
	​

. That implies geometric ergodicity. This often reduces to showing that within 
𝑚
m steps, the random “division by 
2
𝑎
2
a
” component can generate enough spread in the multiplicative group.

5) Minimal extra experiments to de‑risk it

Estimate 
𝜆
^
2
λ
^
2
	​

 (and maybe a few next eigenvalues) of 
𝑃
^
𝑘
P
k
	​

 for 
𝑘
=
6
,
8
,
10
,
12
k=6,8,10,12. Look for a gap that doesn’t collapse with 
𝑘
k.

Fourier diagnostic: track 
𝜙
^
𝑡
(
𝜉
)
:
=
𝐸
(
𝑒
2
𝜋
𝑖
𝜉
𝑋
𝑡
/
3
𝑘
)
ϕ
	​

t
	​

(ξ):=E(e
2πiξX
t
	​

/3
k
) over 
𝑡
t, and identify the slowest‑decaying 
𝜉
ξ. Those 
𝜉
ξ are your proof targets.

Stress test with multiple initial measures (uniform vs log‑uniform vs conditioned on large 
𝑛
n).

Lemma candidate 2 — Conditional geometric law for 
𝑎
(
𝑛
)
a(n) and short memory
1) Precise statement

Let 
𝑎
𝑡
:
=
𝑎
(
𝑛
𝑡
)
=
𝑣
2
(
3
𝑛
𝑡
+
1
)
a
t
	​

:=a(n
t
	​

)=v
2
	​

(3n
t
	​

+1). Fix 
𝑘
k and view the joint process 
(
𝑋
𝑡
,
𝑎
𝑡
)
(X
t
	​

,a
t
	​

).

 

Lemma target (conditional law + mixing). Under the evolved/stationary regime,
there exist 
𝜀
𝑘
→
0
ε
k
	​

→0 and 
0
<
𝜃
𝑘
<
1
0<θ
k
	​

<1 such that:

(Uniform conditional geometric tail)

sup
⁡
𝑥
∈
𝑆
𝑘
 
sup
⁡
𝑚
≥
1
 
∣
𝑃
(
𝑎
𝑡
=
𝑚
∣
𝑋
𝑡
=
𝑥
)
−
2
−
𝑚
∣
 
≤
 
𝜀
𝑘
 
2
−
𝑚
.
x∈S
k
	​

sup
	​

 
m≥1
sup
	​

 
	​

P(a
t
	​

=m∣X
t
	​

=x)−2
−m
	​

 ≤ ε
k
	​

2
−m
.

(Exponential decorrelation)
For bounded functions 
𝐹
,
𝐺
F,G,

∣
C
o
v
(
𝐹
(
𝑎
𝑡
,
𝑋
𝑡
)
,
 
𝐺
(
𝑎
𝑡
+
𝑠
,
𝑋
𝑡
+
𝑠
)
)
∣
≤
𝐶
 
𝜃
𝑘
 
𝑠
 
∥
𝐹
∥
∞
∥
𝐺
∥
∞
.
∣Cov(F(a
t
	​

,X
t
	​

),G(a
t+s
	​

,X
t+s
	​

))∣≤Cθ
k
s
	​

∥F∥
∞
	​

∥G∥
∞
	​

.

(You can weaken “uniform in 
𝑥
x” to “
𝜋
𝑘
π
k
	​

-a.e. 
𝑥
x” if needed.)

2) Why this matters

This is the “noise model becomes real” lemma.

The heuristic negative drift comes from 
𝑎
a behaving roughly geometric with mean 2, giving average log‑drift 
≈
log
⁡
3
−
2
log
⁡
2
=
log
⁡
(
3
/
4
)
<
0
≈log3−2log2=log(3/4)<0.

To convert that into a proof, you need not just the marginal distribution, but control of correlations (otherwise rare long correlated stretches of small 
𝑎
𝑡
a
t
	​

 can dominate).

If you can prove this lemma (even with modest 
𝜀
𝑘
ε
k
	​

), you’re 80% of the way to large‑deviation bounds for block drift (Lemma 4).

3) What M3 evidence supports it

The histogram of 
𝑎
𝑡
a
t
	​

 under the evolved measure matches 
2
−
𝑚
2
−m
 over a decent range of 
𝑚
m (say 
𝑚
≤
15
m≤15 before sample noise dominates).

Conditional histograms given 
𝑋
𝑡
=
𝑥
X
t
	​

=x (or coarse bins of 
𝑥
x) remain close to geometric—no “toxic residue classes” where 
𝑎
=
1
,
2
a=1,2 are anomalously frequent.

Autocorrelation of 
𝑎
𝑡
a
t
	​

 (and of indicators 
1
𝑎
𝑡
=
𝑚
1
a
t
	​

=m
	​

) drops to near 0 quickly; mutual information 
𝐼
(
𝑎
𝑡
;
𝑎
𝑡
+
𝑠
)
I(a
t
	​

;a
t+s
	​

) decays roughly exponentially.

4) Plausible proof strategy

(A) Reduce to correlation bounds for congruence constraints.
Events like 
{
𝑎
𝑡
≥
𝑚
}
{a
t
	​

≥m} are congruence conditions mod 
2
𝑚
2
m
 on 
𝑛
𝑡
n
t
	​

. Track how these congruence classes pull back through 
𝑇
T. For fixed finite patterns 
(
𝑎
𝑡
,
…
,
𝑎
𝑡
+
ℓ
)
(a
t
	​

,…,a
t+ℓ
	​

), you can often write a single affine congruence constraint modulo 
2
∑
𝑎
𝑖
2
∑a
i
	​

 (plus oddness constraints). Then the problem becomes a counting / equidistribution estimate.

 

(B) Use Lemma 1’s spectral gap: additive functional of a finite chain.
If 
(
𝑋
𝑡
)
(X
t
	​

) mixes geometrically and the conditional law of 
𝑎
𝑡
a
t
	​

 given 
𝑋
𝑡
X
t
	​

 is controlled, then 
(
𝑋
𝑡
,
𝑎
𝑡
)
(X
t
	​

,a
t
	​

) is a hidden Markov model with exponential mixing. Standard finite‑state techniques give decorrelation.

5) Minimal extra experiments to de‑risk it

Conditional KL divergence: 
𝐷
K
L
(
𝑃
^
(
𝑎
∣
𝑋
=
𝑥
)
 
∥
 
Geom
(
1
/
2
)
)
D
KL
	​

(
P
(a∣X=x)∥Geom(1/2)) as a function of 
𝑥
x, then summarize by quantiles over 
𝑥
x. You want “no fat right tail” in that divergence.

Autocorrelation/mutual information not just for 
𝑎
𝑡
a
t
	​

, but for the drift increment 
𝑑
𝑡
:
=
log
⁡
(
3
+
1
/
𝑛
𝑡
)
−
𝑎
𝑡
log
⁡
2
d
t
	​

:=log(3+1/n
t
	​

)−a
t
	​

log2.

Check stability across magnitude bins of 
𝑛
𝑡
n
t
	​

. If the law depends on 
log
⁡
𝑛
logn, you may need to include a coarse “size bin” into the state.

Lemma candidate 3 — Poisson correction 
𝜓
𝑘
ψ
k
	​

 and a Foster–Lyapunov drift inequality

This is the “turn M4 into an actual Lyapunov function” move.

1) Precise statement

Define the one‑step log increment

Δ
𝑡
:
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
=
log
⁡
(
3
+
1
/
𝑛
𝑡
)
−
𝑎
𝑡
log
⁡
2.
Δ
t
	​

:=logn
t+1
	​

−logn
t
	​

=log(3+1/n
t
	​

)−a
t
	​

log2.

Fix 
𝑘
k and let 
𝑋
𝑡
=
𝑛
𝑡
 
m
o
d
 
3
𝑘
X
t
	​

=n
t
	​

mod3
k
. Suppose Lemma 1 gives a Markov kernel 
𝑃
𝑘
P
k
	​

 and stationary 
𝜋
𝑘
π
k
	​

. Define the state‑dependent mean increment (under the stationary regime)

𝑔
𝑘
(
𝑥
)
:
=
𝐸
[
Δ
𝑡
∣
𝑋
𝑡
=
𝑥
]
.
g
k
	​

(x):=E[Δ
t
	​

∣X
t
	​

=x].

Let 
𝑐
𝑘
:
=
𝐸
𝜋
𝑘
[
𝑔
𝑘
(
𝑋
)
]
c
k
	​

:=E
π
k
	​

	​

[g
k
	​

(X)] be the stationary average drift.

 

Lemma target (Poisson/Foster–Lyapunov).
There exists a bounded function 
𝜓
𝑘
:
𝑆
𝑘
→
𝑅
ψ
k
	​

:S
k
	​

→R solving the Poisson equation

(
𝐼
−
𝑃
𝑘
)
𝜓
𝑘
=
𝑔
𝑘
−
𝑐
𝑘
,
(I−P
k
	​

)ψ
k
	​

=g
k
	​

−c
k
	​

,

and constants 
𝛿
>
0
δ>0, 
𝑁
0
N
0
	​

 such that if 
𝑐
𝑘
≤
−
2
𝛿
c
k
	​

≤−2δ, then for all 
𝑛
≥
𝑁
0
n≥N
0
	​

,

𝐸
[
(
log
⁡
𝑛
𝑡
+
1
+
𝜓
𝑘
(
𝑋
𝑡
+
1
)
)
−
(
log
⁡
𝑛
𝑡
+
𝜓
𝑘
(
𝑋
𝑡
)
)
 
∣
 
𝑛
𝑡
=
𝑛
]
≤
−
𝛿
.
E[(logn
t+1
	​

+ψ
k
	​

(X
t+1
	​

))−(logn
t
	​

+ψ
k
	​

(X
t
	​

)) 
	​

 n
t
	​

=n]≤−δ.

Equivalently, 
𝑉
𝑘
(
𝑛
)
:
=
log
⁡
𝑛
+
𝜓
𝑘
(
𝑛
 
m
o
d
 
3
𝑘
)
V
k
	​

(n):=logn+ψ
k
	​

(nmod3
k
) has strictly negative drift above 
𝑁
0
N
0
	​

.

2) Why this matters

This is the classic “random walk with state‑dependent drift” fix:

Raw drift 
𝐸
[
Δ
𝑡
∣
𝑋
𝑡
=
𝑥
]
E[Δ
t
	​

∣X
t
	​

=x] might vary by 
𝑥
x.

The Poisson correction 
𝜓
𝑘
ψ
k
	​

 absorbs that variation so that the corrected process behaves like a constant‑drift walk (plus bounded noise).

Once you have this, you can invoke finite‑state Foster–Lyapunov results to get:

descent to a compact set with high probability / almost surely (under the probabilistic model),

quantitative bounds on return times, tail probabilities, etc.

3) What M4 evidence supports it

𝑔
𝑘
(
𝑥
)
g
k
	​

(x) is negative on average and not “nearly zero” (you want a margin).

Solving the empirical Poisson equation using 
𝑃
^
𝑘
,
𝑔
^
𝑘
P
k
	​

,
g
	​

k
	​

 yields a 
𝜓
^
𝑘
ψ
	​

k
	​

 such that the corrected drift

𝑑
^
𝑘
(
𝑥
)
:
=
𝑔
^
𝑘
(
𝑥
)
+
(
𝑃
^
𝑘
𝜓
^
𝑘
)
(
𝑥
)
−
𝜓
^
𝑘
(
𝑥
)
d
k
	​

(x):=
g
	​

k
	​

(x)+(
P
k
	​

ψ
	​

k
	​

)(x)−
ψ
	​

k
	​

(x)

is nearly constant across 
𝑥
x, and that constant is negative with margin.

The worst corrected drift state isn’t scary (or if it is, it tells you exactly what extra state info you need).

4) Plausible proof strategy

This is very “human‑doable” once Lemma 1 is in place:

On a finite irreducible aperiodic chain, the Poisson equation has a bounded solution (unique up to an additive constant) as soon as you pin down 
𝜋
𝑘
(
𝜓
𝑘
)
=
0
π
k
	​

(ψ
k
	​

)=0.

The remaining work is to lift the statement from the finite chain approximation to the actual Syracuse dynamics under your evolved measure, and to manage the 
log
⁡
(
3
+
1
/
𝑛
)
log(3+1/n) vs 
log
⁡
3
log3 correction by taking 
𝑁
0
N
0
	​

 large and brute‑forcing below 
𝑁
0
N
0
	​

.

5) Minimal extra experiments to de‑risk it

Compute 
𝜓
^
𝑘
ψ
	​

k
	​

 for 
𝑘
=
8
,
10
,
12
k=8,10,12 and compare: does 
𝜓
^
𝑘
ψ
	​

k
	​

 stabilize (modulo additive constant) as 
𝑘
k grows?

Measure the empirical distribution of the corrected increment

𝑍
𝑡
:
=
Δ
𝑡
+
𝜓
𝑘
(
𝑋
𝑡
+
1
)
−
𝜓
𝑘
(
𝑋
𝑡
)
Z
t
	​

:=Δ
t
	​

+ψ
k
	​

(X
t+1
	​

)−ψ
k
	​

(X
t
	​

)

and record:

mean,

variance,

worst‑state conditional mean,

tail behavior.

If the “worst‑state conditional mean” is near 0 or positive, you’ve learned something extremely valuable: your state space is missing a crucial bit (maybe 
𝑋
𝑡
 
m
o
d
 
3
𝑘
+
1
X
t
	​

mod3
k+1
, or parity of 
𝑎
𝑡
a
t
	​

, etc.).

Lemma candidate 4 — Exponential rarity of “bad blocks” (large deviations)
1) Precise statement

Fix 
𝑘
k and use the corrected increment 
𝑍
𝑡
Z
t
	​

 from Lemma 3. Let 
𝑆
𝐿
:
=
∑
𝑡
=
0
𝐿
−
1
𝑍
𝑡
S
L
	​

:=∑
t=0
L−1
	​

Z
t
	​

.

 

Lemma target (uniform block contraction).
There exist 
𝐿
∈
𝑁
L∈N and constants 
𝜂
>
0
η>0, 
𝑏
>
0
b>0 such that uniformly over starting states 
𝑥
∈
𝑆
𝑘
x∈S
k
	​

,

𝑃
(
𝑆
𝐿
≥
−
𝑏
𝐿
∣
𝑋
0
=
𝑥
)
≤
𝑒
−
𝜂
𝐿
.
P(S
L
	​

≥−bL∣X
0
	​

=x)≤e
−ηL
.

A “nicer” special case is 
𝑏
=
0
b=0:

𝑃
(
𝑆
𝐿
≥
0
∣
𝑋
0
=
𝑥
)
≤
𝑒
−
𝜂
𝐿
.
P(S
L
	​

≥0∣X
0
	​

=x)≤e
−ηL
.
2) Why this matters

This is the lever that turns “negative drift in expectation” into “almost sure descent”:

If blocks with non‑negative (or insufficiently negative) drift are exponentially rare, you can union‑bound/Borel–Cantelli your way to: only finitely many bad blocks occur almost surely.

Then 
𝑉
𝑘
(
𝑛
𝑡
)
V
k
	​

(n
t
	​

) tends to 
−
∞
−∞, meaning 
𝑛
𝑡
n
t
	​

 enters a bounded region.

This is exactly where M3 (autocorrelation) and M2 (mixing) cash out into a theorem‑shaped inequality.

3) What M2–M4 evidence supports it

From M4: empirical block sums 
𝑆
𝐿
S
L
	​

 have mean 
≈
−
𝑐
𝐿
≈−cL with 
𝑐
>
0
c>0, and the upper tail 
𝑃
(
𝑆
𝐿
≥
0
)
P(S
L
	​

≥0) drops roughly like 
exp
⁡
(
−
𝜂
𝐿
)
exp(−ηL).

From M3: correlations decay fast enough that the block sums behave close to a Markov‑additive process (not a long‑memory monster).

From M2: your mod‑
3
𝑘
3
k
 state doesn’t lock into slow “bad” modes; otherwise the tail won’t be exponential uniformly in starting state.

4) Plausible proof strategy

For a finite‑state Markov chain, this is wonderfully standard and explicit:

Consider the tilted matrix for 
𝜆
>
0
λ>0:

𝑀
𝜆
(
𝑥
,
𝑦
)
:
=
𝑃
𝑘
(
𝑥
,
𝑦
)
 
𝐸
 ⁣
[
𝑒
𝜆
𝑍
𝑡
∣
𝑋
𝑡
=
𝑥
,
𝑋
𝑡
+
1
=
𝑦
]
.
M
λ
	​

(x,y):=P
k
	​

(x,y)E[e
λZ
t
	​

∣X
t
	​

=x,X
t+1
	​

=y].

The exponential growth rate of 
𝐸
(
𝑒
𝜆
𝑆
𝐿
)
E(e
λS
L
	​

) is controlled by the Perron–Frobenius eigenvalue 
𝜌
(
𝑀
𝜆
)
ρ(M
λ
	​

).

If the mean drift is negative, you can show there exists 
𝜆
>
0
λ>0 with 
𝜌
(
𝑀
𝜆
)
<
1
ρ(M
λ
	​

)<1, giving a Chernoff bound:

𝑃
(
𝑆
𝐿
≥
0
)
≤
𝐸
(
𝑒
𝜆
𝑆
𝐿
)
≤
𝐶
 
𝜌
(
𝑀
𝜆
)
𝐿
.
P(S
L
	​

≥0)≤E(e
λS
L
	​

)≤Cρ(M
λ
	​

)
L
.

All of this is finite‑dimensional linear algebra once you have a validated 
𝑃
𝑘
P
k
	​

 and a validated conditional law of 
𝑍
𝑡
Z
t
	​

.

5) Minimal extra experiments to de‑risk it

Estimate the empirical mgf 
𝐸
^
(
𝑒
𝜆
𝑆
𝐿
)
E
(e
λS
L
	​

) for a grid of 
𝜆
λ and 
𝐿
L; see if 
log
⁡
𝐸
^
(
𝑒
𝜆
𝑆
𝐿
)
/
𝐿
log
E
(e
λS
L
	​

)/L stabilizes.

Identify the dominant contribution to bad blocks: is it many 
𝑎
=
1
a=1 in a row, or some state‑dependent pattern? That will guide whether you need to refine the state space.

Uniformity check: estimate 
𝑃
(
𝑆
𝐿
≥
0
∣
𝑋
0
=
𝑥
)
P(S
L
	​

≥0∣X
0
	​

=x) for a sample of “worst” 
𝑥
x’s.

Lemma candidate 5 — Conditional “almost sure termination” from block descent + finite verification

This is the optional “capstone lemma” that turns the previous lemmas into a result that looks like progress toward termination.

1) Precise statement (conditional theorem)

Assume Lemmas 1–4 hold for some 
𝑘
k with explicit constants, and assume further that all odd 
𝑛
≤
𝑁
⋆
n≤N
⋆
	​

 are verified to reach 
1
1 under 
𝑇
T.

 

Then for 
𝑛
0
n
0
	​

 drawn from your evolved measure (e.g., log‑uniform on a large range, evolved past burn‑in), the Syracuse trajectory hits 
[
1
,
𝑁
⋆
]
[1,N
⋆
	​

] almost surely; hence it reaches 
1
1 almost surely (for that measure).

 

You can state it in density language: the set of starting values failing to reach 
1
1 has logarithmic density 0.

 

This would be in the spirit of (but stronger in conclusion than) Tao’s logarithmic‑density “almost bounded” theorem. 
arXiv

2) Why this matters

It’s a clean “proof‑shaped” deliverable:

you’re not proving Collatz for all 
𝑛
n,

but you’re converting empirical drift/mixing into a rigorous “almost all” termination statement with explicit constants and an explicit finite verification threshold.

That’s exactly the kind of result humans can plausibly prove in the near term.

3) What evidence supports it

Your block contraction probability is strong enough that you can bound the chance of avoiding 
[
1
,
𝑁
⋆
]
[1,N
⋆
	​

] across many blocks by a summable series.

Empirically, the escape probability seems to fall faster than any power.

4) Plausible proof strategy

Use Lemma 3 to build a supermartingale 
𝑉
𝑘
(
𝑛
𝑡
)
V
k
	​

(n
t
	​

).

Use Lemma 4 to get an exponential tail for excursions upward / for failure to decrease over blocks.

Apply a stopping time argument to show 
𝑉
𝑘
V
k
	​

 must hit the finite region almost surely.

Patch with brute force for 
𝑛
≤
𝑁
⋆
n≤N
⋆
	​

.

5) Minimal extra experiments to de‑risk it

Choose a realistic 
𝑁
⋆
N
⋆
	​

 you can fully verify (maybe you already have this infrastructure).

Empirically estimate the probability of avoiding 
[
1
,
𝑁
⋆
]
[1,N
⋆
	​

] up to time 
𝑡
t and check that it’s consistent with an exponential bound derived from Lemma 4’s 
𝜂
η.

Parameter recommendations (k, horizons, samples)

You want parameters that (i) make the finite‑state objects tractable, (ii) are large enough to be convincing, (iii) let you see stability as 
𝑘
k grows.

Suggested 
𝑘
k ladder

Start: 
𝑘
=
8
k=8.
State space size 
∣
𝑆
𝑘
∣
=
2
⋅
3
𝑘
−
1
=
2
⋅
3
7
=
4374
∣S
k
	​

∣=2⋅3
k−1
=2⋅3
7
=4374. That’s small enough to:

build 
𝑃
^
𝑘
P
k
	​

 accurately,

solve Poisson equations comfortably,

do eigen/spectral diagnostics.

Confirm: 
𝑘
=
10
k=10.

∣
𝑆
10
∣
=
2
⋅
3
9
=
39366
∣S
10
	​

∣=2⋅3
9
=39366. This is the first “serious” size where spurious finite‑state artifacts start dying.

Stress test: 
𝑘
=
12
k=12.

∣
𝑆
12
∣
=
2
⋅
3
11
=
354294
∣S
12
	​

∣=2⋅3
11
=354294. You probably won’t do dense linear algebra, but you can still do:

sparse power iteration for leading eigenvalues,

Monte‑Carlo estimates of block tails,

approximate Poisson solves (iterative methods).

Horizons

Mixing (M2): measure up to 
𝑡
=
50
t=50 for 
𝑘
=
8
k=8, 
𝑡
=
100
t=100–
200
200 for 
𝑘
=
10
k=10.
The decisive thing is seeing a clear exponential regime, not “wiggles.”

Autocorrelation (M3): compute ACF / mutual information out to lag 50–100.

Block tails (Lemma 4 / M4‑adjacent): block lengths 
𝐿
∈
{
20
,
50
,
100
,
200
}
L∈{20,50,100,200}.
You’re hunting an exponential tail; those 
𝐿
L’s usually reveal it.

Sample sizes (rule of thumb)

Think in state‑visits, not trajectories.

For 
𝑘
=
8
k=8: target 
4
×
10
7
4×10
7
 state‑visits.
That gives ~9k visits per state if near‑uniform.

For 
𝑘
=
10
k=10: target 
1
×
10
8
1×10
8
 state‑visits.
That gives ~2500 visits per state on average—enough to stabilize conditional means.

You can get these visits by, e.g., 
2
×
10
5
2×10
5
 trajectories of length 200 (40M visits), then scale.

Diagnostics that are most decisive

If you only had time to compute a handful of plots/numbers, these are the “proof‑shaped” ones:

Spectral gap proxy for 
𝑃
𝑘
P
k
	​

: estimate 
∣
𝜆
2
∣
∣λ
2
	​

∣ (or mixing time via TV distance decay).
If 
∣
𝜆
2
∣
∣λ
2
	​

∣ creeps toward 1 as 
𝑘
k increases, your state is missing something.

Worst‑state corrected drift: after computing 
𝜓
𝑘
ψ
k
	​

,

min
⁡
𝑥
 
𝐸
^
[
𝑍
𝑡
∣
𝑋
𝑡
=
𝑥
]
x
min
	​

 
E
[Z
t
	​

∣X
t
	​

=x]

(and maybe also a small quantile like 1%).
Proofs die in worst‑case corners.

Block non‑descent probability vs 
𝐿
L:

𝑝
(
𝐿
)
:
=
sup
⁡
𝑥
𝑃
^
(
𝑆
𝐿
≥
0
∣
𝑋
0
=
𝑥
)
.
p(L):=
x
sup
	​

P
(S
L
	​

≥0∣X
0
	​

=x).

Plot 
log
⁡
𝑝
(
𝐿
)
logp(L) vs 
𝐿
L. A straight line is the smell of a future Chernoff bound.

Conditional deviation from geometric for 
𝑎
a: the distributional sanity check that prevents self‑deception:

sup
⁡
𝑥
𝐷
K
L
 ⁣
(
𝑃
^
(
𝑎
∣
𝑋
=
𝑥
)
 
∥
 
Geom
(
1
/
2
)
)
.
x
sup
	​

D
KL
	​

(
P
(a∣X=x)∥Geom(1/2)).

If a few states are wildly off, you know exactly where to refine the state.

Closing thought

The “dream stack” is: (Markov/spectral gap) ⇒ (Poisson correction) ⇒ (large deviations) ⇒ (almost sure descent to a finite verified set). That’s a very sane proof pipeline: finite‑dimensional linear algebra + explicit constants + a controlled exceptional set. It also has a nice feature: every time an empirical diagnostic fails, it doesn’t just say “oops”—it tells you what information your state is missing.

 

Your M2–M4 plan is basically a truth‑serum test for whether this pipeline is viable.

 

(And yes, the universe is ridiculous: a conjecture about dividing by 2 and multiplying by 3 pushes you into spectral gaps on 
3
3-adic groups. Mathematics is a prankster.)
