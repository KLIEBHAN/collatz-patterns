Sehr gut – das ist genau der richtige nächste Schritt: ein exaktes, endliches „Lemma‑Objekt“ bauen, an dem man wirklich rechnen (und ggf. rigoros abschätzen) kann.

 

Wichtig vorweg (damit wir uns nicht selbst trollen): Das 
𝑃
𝑘
P
k
	​

-Modell mit i.i.d. geometrischem 
𝑎
a ist ein idealisiertes Random‑Model für die Residuen‑Dynamik, nicht die echte deterministische Syracuse‑Dynamik. Aber: Es ist ein perfekt sauberes Test‑ und Beweisobjekt, an dem man Methoden (Spektral, Poisson, Lyapunov‑Korrektur) rigoros demonstrieren kann.

 

Im Folgenden bekommst du:

(1) die exakte Konstruktion von 
𝑃
𝑘
P
k
	​

 (inkl. “unendliche Summe → endlich”),

(2) Implementationstipps (Fraction vs. SymPy),

(3) Spektrallücke: was „exakt“ realistisch heißt – und ein überraschend starker Struktur‑Satz für dieses Modell,

(4) exaktes Lösen der Poisson‑Gleichung,

(5) ein vollständiges Code‑Beispiel für 
𝑘
=
4
k=4 (Mod 
81
81).

1) Exakte Übergangsmatrix 
𝑃
𝑘
P
k
	​

 für Syracuse mod 
3
𝑘
3
k
Zustandsraum

Setze

𝑀
=
3
𝑘
,
𝑆
𝑘
=
(
𝑍
/
𝑀
𝑍
)
×
=
{
𝑥
∈
{
1
,
…
,
𝑀
−
1
}
:
3
∤
𝑥
}
.
M=3
k
,S
k
	​

=(Z/MZ)
×
={x∈{1,…,M−1}:3∤x}.

Dann 
∣
𝑆
𝑘
∣
=
𝜑
(
3
𝑘
)
=
2
⋅
3
𝑘
−
1
∣S
k
	​

∣=φ(3
k
)=2⋅3
k−1
.

Random‑Syracuse‑Schritt (Idealmodell)

Wir modellieren den “accelerated odd step” als:

gegeben 
𝑋
𝑡
=
𝑥
∈
𝑆
𝑘
X
t
	​

=x∈S
k
	​

,

ziehe 
𝐴
∈
{
1
,
2
,
3
,
…
 
}
A∈{1,2,3,…} mit

𝑃
(
𝐴
=
𝑚
)
=
2
−
𝑚
,
P(A=m)=2
−m
,

setze

𝑋
𝑡
+
1
≡
(
3
𝑥
+
1
)
⋅
2
−
𝐴
(
m
o
d
3
𝑘
)
.
X
t+1
	​

≡(3x+1)⋅2
−A
(mod3
k
).

Da 
2
2 modulo 
3
𝑘
3
k
 invertierbar ist, ist 
2
−
𝐴
2
−A
 wohldefiniert.

Warum die unendliche Summe endlich wird

Der Trick ist, dass 
2
𝑚
(
m
o
d
3
𝑘
)
2
m
(mod3
k
) periodisch ist, weil 
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
 endlich ist. Definiere

𝑟
:
=
ord
⁡
3
𝑘
(
2
)
,
r:=ord
3
k
	​

(2),

also die multiplikative Ordnung von 
2
2 modulo 
3
𝑘
3
k
.

 

Für 
3
𝑘
3
k
 gilt tatsächlich (und man kann es per Induktion beweisen oder einfach programmatisch verifizieren):

𝑟
=
𝜑
(
3
𝑘
)
=
2
⋅
3
𝑘
−
1
.
r=φ(3
k
)=2⋅3
k−1
.

Das heißt 
2
𝑟
≡
1
(
m
o
d
3
𝑘
)
2
r
≡1(mod3
k
) und damit hängt 
2
−
𝐴
(
m
o
d
3
𝑘
)
2
−A
(mod3
k
) nur von 
𝐴
 
m
o
d
 
𝑟
Amodr ab.

 

Also bündeln wir alle 
𝑚
m in Klassen 
𝑚
≡
𝑚
0
 
(
m
o
d
 
𝑟
)
m≡m
0
	​

 (mod r) mit 
𝑚
0
∈
{
1
,
…
,
𝑟
}
m
0
	​

∈{1,…,r}.

 

Die zusammengefasste Masse ist:

𝑤
𝑚
0
=
𝑃
(
𝐴
≡
𝑚
0
 ⁣
 ⁣
 ⁣
(
m
o
d
𝑟
)
)
=
∑
𝑗
=
0
∞
2
−
(
𝑚
0
+
𝑗
𝑟
)
=
2
−
𝑚
0
1
−
2
−
𝑟
=
2
𝑟
−
𝑚
0
2
𝑟
−
1
.
w
m
0
	​

	​

=P(A≡m
0
	​

(modr))=
j=0
∑
∞
	​

2
−(m
0
	​

+jr)
=
1−2
−r
2
−m
0
	​

	​

=
2
r
−1
2
r−m
0
	​

	​

.

Das ist eine exakte rationale Zahl. Und

∑
𝑚
0
=
1
𝑟
𝑤
𝑚
0
=
1
m
0
	​

=1
∑
r
	​

w
m
0
	​

	​

=1

weil 
∑
𝑚
0
=
1
𝑟
2
𝑟
−
𝑚
0
=
2
𝑟
−
1
∑
m
0
	​

=1
r
	​

2
r−m
0
	​

=2
r
−1.

Übergänge

Definiere für jedes 
𝑚
0
∈
{
1
,
…
,
𝑟
}
m
0
	​

∈{1,…,r}:

𝑢
𝑚
0
≡
2
−
𝑚
0
(
m
o
d
3
𝑘
)
.
u
m
0
	​

	​

≡2
−m
0
	​

(mod3
k
).

Dann ist der deterministische Zielzustand

𝑇
𝑚
0
(
𝑥
)
≡
(
3
𝑥
+
1
)
⋅
𝑢
𝑚
0
(
m
o
d
3
𝑘
)
.
T
m
0
	​

	​

(x)≡(3x+1)⋅u
m
0
	​

	​

(mod3
k
).

Und die Übergangsmatrix ist:

𝑃
𝑘
(
𝑥
,
𝑦
)
=
∑
𝑚
0
=
1
𝑟
𝑤
𝑚
0
 
1
{
𝑦
=
𝑇
𝑚
0
(
𝑥
)
}
.
P
k
	​

(x,y)=
m
0
	​

=1
∑
r
	​

w
m
0
	​

	​

1{y=T
m
0
	​

	​

(x)}.

Praktisch: du implementierst das, indem du für jedes 
𝑥
x über 
𝑚
0
=
1
,
…
,
𝑟
m
0
	​

=1,…,r iterierst, das jeweilige 
𝑦
y ausrechnest und 
𝑤
𝑚
0
w
m
0
	​

	​

 auf 
𝑃
[
𝑥
,
𝑦
]
P[x,y] addierst (Kollisionen sind möglich, aber bei 
3
𝑘
3
k
 und Ordnung 
𝑟
=
∣
𝑆
𝑘
∣
r=∣S
k
	​

∣ ist 
𝑚
0
↦
𝑢
𝑚
0
m
0
	​

↦u
m
0
	​

	​

 sogar eine Permutation aller Einheiten, was das oft vereinfacht).

2) Rationale Arithmetik: Fraction vs SymPy
fractions.Fraction

Super für Skalare und kleine Vektoren.

Für lineare Algebra (Stationärverteilung, Poisson‑Gleichung) musst du dann selbst Gauß‑Elimination schreiben.

sympy.Rational + sympy.Matrix

Beste Wahl, wenn du wirklich exakt lineare Systeme lösen willst.

SymPy arbeitet intern mit exakten rationalen Zahlen und kann LU‑Solve etc.

Empfehlung:
Für 
𝑘
=
4
k=4 (54 Zustände) ist SymPy perfekt. Für 
𝑘
=
8
k=8 (4374 Zustände) ist eine dichte exakte Matrix nicht mehr realistisch. Dann brauchst du Operator‑Form / Sparse‑Ideen / Iteration (und evtl. Zertifizierung über Residuen), aber als Start‑Lemmaobjekt ist 
𝑘
=
4
k=4 genau richtig.

3) Spektrallücke 
∣
𝜆
2
∣
∣λ
2
	​

∣ „exakt“ bestimmen
Realistische Wahrheit

Eine rationale Matrix hat i.A. algebraische Eigenwerte (Roots eines Polynoms).

„Exakt als geschlossene Formel“ ist selten sinnvoll, selbst bei 54×54.

Aber: in diesem Modell gibt es einen starken Struktur‑Satz

Hier kommt ein nerdiger, aber extrem nützlicher Punkt:

Lemma (k‑Step Coalescence / Endliches Mixing):
Für das Random‑Residuen‑Modell

𝑋
𝑡
+
1
≡
(
3
𝑋
𝑡
+
1
)
 
𝑈
𝑡
+
1
(
m
o
d
3
𝑘
)
,
X
t+1
	​

≡(3X
t
	​

+1)U
t+1
	​

(mod3
k
),

wobei 
𝑈
𝑡
U
t
	​

 stets eine Einheit mod 
3
𝑘
3
k
 ist (egal welche Verteilung!), gilt:
Nach spätestens 
𝑘
k Schritten ist die Verteilung unabhängig vom Startzustand.
Äquivalent: 
𝑃
𝑘
𝑘
P
k
k
	​

 hat identische Zeilen, also Rang 1.

Beweisidee (kurz, aber wirklich wasserdicht):
Kopple zwei Ketten 
𝑋
𝑡
,
𝑋
𝑡
′
X
t
	​

,X
t
′
	​

 mit derselben Zufallssequenz 
𝑈
𝑡
U
t
	​

. Dann

𝑋
𝑡
+
1
−
𝑋
𝑡
+
1
′
≡
(
3
𝑋
𝑡
+
1
)
𝑈
𝑡
+
1
−
(
3
𝑋
𝑡
′
+
1
)
𝑈
𝑡
+
1
=
3
(
𝑋
𝑡
−
𝑋
𝑡
′
)
𝑈
𝑡
+
1
(
m
o
d
3
𝑘
)
.
X
t+1
	​

−X
t+1
′
	​

≡(3X
t
	​

+1)U
t+1
	​

−(3X
t
′
	​

+1)U
t+1
	​

=3(X
t
	​

−X
t
′
	​

)U
t+1
	​

(mod3
k
).

Da 
𝑈
𝑡
+
1
U
t+1
	​

 eine Einheit ist, erhöht sich die 3‑adische Teilbarkeit der Differenz pro Schritt um 1. Nach 
𝑘
k Schritten ist die Differenz durch 
3
𝑘
3
k
 teilbar, also

𝑋
𝑘
≡
𝑋
𝑘
′
(
m
o
d
3
𝑘
)
.
X
k
	​

≡X
k
′
	​

(mod3
k
).

Damit hängt 
𝑋
𝑘
X
k
	​

 (mod 
3
𝑘
3
k
) nicht mehr vom Start 
𝑋
0
X
0
	​

 ab ⇒ alle Zeilen von 
𝑃
𝑘
P
k
 sind gleich ⇒ Rang 1.

 

Konsequenz für Eigenwerte:
Wenn 
𝑃
𝑘
=
Π
P
k
=Π (Projektor auf die stationäre Verteilung), dann gilt für jeden Eigenwert 
𝜆
≠
1
λ

=1:

𝜆
𝑘
=
0
⇒
𝜆
=
0.
λ
k
=0⇒λ=0.

Also:

∣
𝜆
2
∣
=
0
exakt.
∣λ
2
	​

∣=0exakt.

Die „Spektrallücke“ (im Sinne 
1
−
∣
𝜆
2
∣
1−∣λ
2
	​

∣) ist dann 1.

 

Das ist krass – und erklärt nebenbei, warum dieses Idealmodell viel stärker mischt als eure empirische Syracuse‑Dynamik: dort ist 
𝑈
𝑡
+
1
=
2
−
𝑎
(
𝑛
𝑡
)
U
t+1
	​

=2
−a(n
t
	​

)
 eben nicht i.i.d./extern, sondern vom Zustand abhängig.

4) Poisson‑Gleichung 
(
𝐼
−
𝑃
)
𝜓
=
𝑔
−
𝑔
ˉ
(I−P)ψ=g−
g
ˉ
	​

 exakt lösen

Sei 
𝑔
:
𝑆
𝑘
→
𝑄
g:S
k
	​

→Q (oder allgemein „exakt repräsentierbar“) und 
𝜋
π die stationäre Verteilung. Setze

𝑔
ˉ
=
∑
𝑥
𝜋
(
𝑥
)
 
𝑔
(
𝑥
)
,
𝑏
=
𝑔
−
𝑔
ˉ
1.
g
ˉ
	​

=
x
∑
	​

π(x)g(x),b=g−
g
ˉ
	​

1.

Gesucht ist 
𝜓
ψ (bis auf additive Konstante) mit

(
𝐼
−
𝑃
)
𝜓
=
𝑏
,
𝜋
⊤
𝜓
=
0.
(I−P)ψ=b,π
⊤
ψ=0.
Standard‑Weg: exaktes lineares Lösen

Nimm 
𝐴
=
𝐼
−
𝑃
A=I−P (singulär).

Fixiere Gauge, z.B. 
𝜓
(
𝑥
0
)
=
0
ψ(x
0
	​

)=0 (ersetze eine Gleichung).

Löse exakt mit SymPy LUsolve.

Spezial‑Weg in diesem Modell (weil 
𝑃
𝑘
=
Π
P
k
=Π): endliche Summe

Wenn 
𝑃
𝑘
=
Π
P
k
=Π und 
𝑏
b mittelfrei ist (
𝜋
⊤
𝑏
=
0
π
⊤
b=0), dann gilt 
𝑃
𝑘
𝑏
=
Π
𝑏
=
0
P
k
b=Πb=0 und

𝜓
  
=
  
∑
𝑡
=
0
𝑘
−
1
𝑃
𝑡
𝑏
ψ=
t=0
∑
k−1
	​

P
t
b

ist eine exakte Lösung, denn

(
𝐼
−
𝑃
)
(
∑
𝑡
=
0
𝑘
−
1
𝑃
𝑡
𝑏
)
=
(
𝐼
−
𝑃
𝑘
)
𝑏
=
𝑏
.
(I−P)(
t=0
∑
k−1
	​

P
t
b)=(I−P
k
)b=b.

Und 
𝜋
⊤
𝜓
=
∑
𝑡
=
0
𝑘
−
1
𝜋
⊤
𝑏
=
0
π
⊤
ψ=∑
t=0
k−1
	​

π
⊤
b=0.

 

Das ist extrem proof‑freundlich: keine Numerik, keine Konditionierungsangst.

5) Konkretes Code‑Beispiel für 
𝑘
=
4
k=4 (Mod 81)

Das hier ist ein kompletter Startpunkt: baut 
𝑃
4
P
4
	​

 exakt, berechnet 
𝜋
π, verifiziert 
𝑃
4
=
Π
P
4
=Π, und löst eine Poisson‑Gleichung exakt.

python
Code kopieren
import sympy as sp

def build_exact_P_k(k: int):
    """
    Exact kernel P_k on units mod 3^k for the idealized random Syracuse model:
        X_{t+1} = (3 X_t + 1) * 2^{-A}  (mod 3^k),
        P(A=m) = 2^{-m}, m>=1.

    Collapsing uses r = ord_{3^k}(2) = phi(3^k) = 2*3^(k-1).
    """
    M = 3**k
    states = [x for x in range(1, M) if x % 3 != 0]   # units mod 3^k
    n = len(states)

    r = 2 * 3**(k-1)  # for mod 3^k, ord(2)=phi(3^k)
    assert r == n

    D = 2**r - 1  # common denominator
    w = [None] + [sp.Rational(2**(r-m), D) for m in range(1, r+1)]

    inv2 = pow(2, -1, M)
    inv2pow = [None]*(r+1)
    cur = inv2 % M
    for m in range(1, r+1):
        inv2pow[m] = cur
        cur = (cur * inv2) % M

    idx = {x:i for i, x in enumerate(states)}
    P = sp.MutableDenseMatrix(n, n, [0]*(n*n))

    for x in states:
        i = idx[x]
        c = (3*x + 1) % M
        for m in range(1, r+1):
            y = (c * inv2pow[m]) % M
            P[i, idx[y]] += w[m]

    P = sp.Matrix(P)

    # stationary distribution pi: solve (P^T - I) pi = 0 with sum pi = 1
    A = P.T - sp.eye(n)
    b = sp.Matrix([0]*n)
    A[n-1, :] = sp.Matrix([1]*n).T
    b[n-1] = 1
    pi = sp.Matrix(A).LUsolve(b)

    return states, P, pi, M, r


def verify_projection(P: sp.Matrix, pi: sp.Matrix, k: int):
    """Check that P^k = 1*pi^T exactly (rank-1 projection)."""
    n = P.rows
    Pk = P**k
    Pi = sp.Matrix([[pi[j] for j in range(n)] for _ in range(n)])  # every row = pi^T
    return (Pk - Pi) == sp.zeros(n)


def poisson_solve_by_finite_sum(P: sp.Matrix, pi: sp.Matrix, g: sp.Matrix, k: int):
    """
    Solve (I - P)psi = g - gbar exactly via psi = sum_{t=0}^{k-1} P^t (g - gbar).
    Works when P^k is the rank-1 projection (true for this model).
    """
    n = P.rows
    one = sp.Matrix([1]*n)
    gbar = (pi.T * g)[0]
    b = g - gbar*one

    psi = sp.zeros(n, 1)
    Pt = sp.eye(n)
    for _ in range(k):
        psi += Pt * b
        Pt = Pt * P

    return sp.simplify(gbar), sp.simplify(psi)


if __name__ == "__main__":
    k = 4
    states, P, pi, M, r = build_exact_P_k(k)

    # Row sums sanity check
    for i in range(P.rows):
        assert sp.simplify(sum(P[i, j] for j in range(P.cols)) - 1) == 0

    # Verify the strong structure: P^k is exactly the projection to stationarity
    assert verify_projection(P, pi, k)

    # Example observable g (toy): g(x)=1 if x ≡ 1 mod 9 else 0
    g = sp.Matrix([1 if (x % 9) == 1 else 0 for x in states])

    gbar, psi = poisson_solve_by_finite_sum(P, pi, g, k)

    # Check Poisson equation exactly
    one = sp.Matrix([1]*P.rows)
    residual = (sp.eye(P.rows) - P) * psi - (g - gbar*one)
    assert residual == sp.zeros(P.rows, 1)

    print("k =", k, "M =", M, "|S_k| =", len(states), "r =", r)
    print("Verified: P^k is projection. (=> all nontrivial eigenvalues are 0)")
    print("Example gbar =", gbar)
    print("psi[0:5] =", list(psi[:5, 0]))


Was dieser Code dir „rigoros“ liefert:

eine exakt rationale Matrix 
𝑃
4
P
4
	​

,

eine exakt rationale stationäre Verteilung 
𝜋
π,

einen Beweis per Rechnercheck, dass 
𝑃
4
P
4
 bereits ein Rang‑1‑Projektor ist,

und eine exakte Poisson‑Lösung 
𝜓
ψ (für beliebiges rationales 
𝑔
g).

Wie ihr das als „Lemma‑Objekt“ benutzt (ohne zu überclaimen)

Lemma über das Idealmodell:
„Im i.i.d.-Random‑Residuenmodell mod 
3
𝑘
3
k
 gilt 
𝑃
𝑘
𝑘
=
Π
P
k
k
	​

=Π ⇒ 
∣
𝜆
2
∣
=
0
∣λ
2
	​

∣=0 und Poisson‑Gleichungen haben eine endliche Summenlösung.“

Dann die echte Arbeit (Brücke zur echten Syracuse‑Dynamik):
Ihr müsst zeigen/quantifizieren, wie weit die echte deterministische Dynamik (unter eurer evolved measure) von diesem Ideal‑
𝑃
𝑘
P
k
	​

 als Operator abweicht. Das ist der Ort, wo eure empirischen M2–M4 Resultate reinkommen (Mixing proxy, Autokorrelation, state drift, etc.).
Aber: jetzt habt ihr einen exakten Referenzpunkt, an dem man “Perturbation” überhaupt sinnvoll definieren kann.

Poisson‑Korrektur als stabiles Ziel:
In der Realität ist 
𝑃
P nicht nilpotent, und 
∣
𝜆
2
∣
∣λ
2
	​

∣ ist nicht 0. Aber wenn ihr zeigen könnt, dass die reale Kette eine “kleine” Störung des Ideal‑Operators ist (in einem passenden Norm‑/Coupling‑Sinn), könnt ihr aus der exakten Struktur robuste Abschätzungen bauen.

Wenn du als nächstes einen wirklich proof‑orientierten “Bridge‑Step” willst, ist der natürliche nächste Baustein:

Definiere einen Operator‑Abstand 
∥
𝑃
𝑘
emp
−
𝑃
𝑘
ideal
∥
∥P
k
emp
	​

−P
k
ideal
	​

∥ (z.B. max‑TV pro Zeile, oder Wasserstein über Zustände),

und leite daraus eine harte Schranke für (i) 
∣
𝜆
2
∣
∣λ
2
	​

∣ und (ii) den Poisson‑Fehler 
∥
(
𝐼
−
𝑃
)
𝜓
−
(
𝑔
−
𝑔
ˉ
)
∥
∥(I−P)ψ−(g−
g
ˉ
	​

)∥ ab.

Das wäre der nächste große Hebel von „exakt gebaut“ zu „rigoros nutzbar“.
