#!/usr/bin/env python3
# =============================================================================
# g_2a_s8_chatleg.py — Gate G-2a-S8, chat-side first leg
# Pre-registration: G_2a_S8_EXECUTION_PREREGISTRATION.md (LOCKED July 10, 2026)
# Base: SQT_Master_Ledger_v4_56_CANONICAL.md (md5 1b1dc6b8824daf5c9c06c521d97065db)
#
# Exact arithmetic throughout: Fractions for affine parts; Q(sqrt2) for Spin(3).
# Every decisive bit machine-decided with live falsifiers. No numeric targets.
# Deterministic; no randomness.
# =============================================================================
from fractions import Fraction as F
import itertools, hashlib, math, sys

PASS = 0
def ok(label, cond):
    global PASS
    if not cond:
        print(f"[FAIL] {label}")
        sys.exit(1)
    PASS += 1
    print(f"[PASS] {label}")

def note(label):
    print(f"[NOTE] {label}")

# -----------------------------------------------------------------------------
# Exact field Q(sqrt2): elements a + b*sqrt2 with a, b in Q.
# -----------------------------------------------------------------------------
class R2:
    __slots__ = ("a", "b")
    def __init__(self, a, b=0):
        self.a = F(a); self.b = F(b)
    def __add__(s, o): return R2(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return R2(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return R2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)
    def __neg__(s):    return R2(-s.a, -s.b)
    def __eq__(s, o):  return s.a == o.a and s.b == o.b
    def __hash__(s):   return hash((s.a, s.b))
    def is_zero(s):    return s.a == 0 and s.b == 0
    def sign(s):
        if s.a == 0 and s.b == 0: return 0
        if s.a >= 0 and s.b >= 0: return 1
        if s.a <= 0 and s.b <= 0: return -1
        d = s.a * s.a - 2 * s.b * s.b          # never 0 for rational a,b not both 0
        t = 1 if d > 0 else -1
        return t * (1 if s.a > 0 else -1)
    def __repr__(s):
        return f"({s.a}+{s.b}\u221a2)"

R2_0 = R2(0); R2_1 = R2(1); R2_m1 = R2(-1); R2_h = R2(F(1, 2)); R2_s2h = R2(0, F(1, 2))

# -----------------------------------------------------------------------------
# Quaternions over Q(sqrt2)
# -----------------------------------------------------------------------------
class Q4:
    __slots__ = ("w", "x", "y", "z")
    def __init__(self, w, x, y, z):
        self.w, self.x, self.y, self.z = w, x, y, z
    def __mul__(a, b):
        return Q4(a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z,
                  a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
                  a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
                  a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w)
    def conj(s): return Q4(s.w, -s.x, -s.y, -s.z)
    def __neg__(s): return Q4(-s.w, -s.x, -s.y, -s.z)
    def __eq__(a, b): return a.w == b.w and a.x == b.x and a.y == b.y and a.z == b.z
    def __hash__(s): return hash(((s.w.a, s.w.b), (s.x.a, s.x.b), (s.y.a, s.y.b), (s.z.a, s.z.b)))
    def comps(s): return (s.w, s.x, s.y, s.z)
    def __repr__(s): return f"Q4[{s.w},{s.x},{s.y},{s.z}]"

def q_scal(c):  # scalar quaternion from R2
    return Q4(c, R2_0, R2_0, R2_0)

ONE  = q_scal(R2_1)
MONE = q_scal(R2_m1)
QI = Q4(R2_0, R2_1, R2_0, R2_0)
QJ = Q4(R2_0, R2_0, R2_1, R2_0)
QK = Q4(R2_0, R2_0, R2_0, R2_1)
HUR = Q4(R2_h, R2_h, R2_h, R2_h)                 # (1+i+j+k)/2   (3-fold about (1,1,1))
W4X = Q4(R2_s2h + R2_s2h, R2_s2h + R2_s2h, R2_0, R2_0)  # placeholder; fixed below

# (1+i)/sqrt2 = (sqrt2/2)(1+i):
W4X = Q4(R2(0, F(1, 2)), R2(0, F(1, 2)), R2_0, R2_0)

BASIS = (QI, QJ, QK)

def rho(q):
    """SO(3) matrix of unit quaternion q (integer entries asserted)."""
    qc = q.conj()
    cols = []
    for e in BASIS:
        p = q * e * qc
        assert p.w.is_zero(), "rho: non-pure image"
        col = []
        for comp in (p.x, p.y, p.z):
            assert comp.b == 0 and comp.a.denominator == 1, "rho: non-integer entry"
            col.append(int(comp.a))
        cols.append(col)
    # cols[j] = image of e_j; matrix rows:
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))

# -----------------------------------------------------------------------------
# Exact affine machinery: (M | t), x -> Mx + t. M integer 3x3, t Fraction 3-vec.
# -----------------------------------------------------------------------------
def mv(M, v): return tuple(sum(F(M[i][j]) * v[j] for j in range(3)) for i in range(3))
def mm(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def tr(M):    return tuple(tuple(M[j][i] for j in range(3)) for i in range(3))
def vadd(a, b): return tuple(a[i] + b[i] for i in range(3))
def vsub(a, b): return tuple(a[i] - b[i] for i in range(3))

I3 = ((1,0,0),(0,1,0),(0,0,1))
A1 = ((1,0,0),(0,-1,0),(0,0,-1))
A2 = ((-1,0,0),(0,1,0),(0,0,-1))
A3 = ((-1,0,0),(0,-1,0),(0,0,1))

def aff(M, t): return (M, tuple(F(x) for x in t))
def acomp(g, h):  # g after h : x -> Mg(Mh x + th) + tg
    return (mm(g[0], h[0]), vadd(mv(g[0], h[1]), g[1]))
def ainv(g):
    Mi = tr(g[0])                      # orthogonal integer => inverse = transpose
    return (Mi, tuple(-x for x in mv(Mi, g[1])))
AEID = aff(I3, (0,0,0))

r1 = aff(A1, (0,0,1)); r2 = aff(A2, (1,0,0)); r3 = aff(A3, (0,1,0))
avec = {I3: (F(0),F(0),F(0)), A1: (F(0),F(0),F(1)), A2: (F(1),F(0),F(0)), A3: (F(0),F(1),F(0))}

def in_L(v):
    if any(x.denominator != 1 for x in v): return False
    xs = [int(x) for x in v]
    return all(x % 2 == 0 for x in xs) or all(x % 2 == 1 for x in xs)

def in_Gamma(g):
    M, t = g
    if M not in avec: return False
    return in_L(vsub(t, avec[M]))

print("=" * 78)
print("PART 0 — Gamma machinery (inherited objects re-asserted, not imported)")
print("=" * 78)
ok("r1^2 = e", acomp(r1, r1) == AEID)
ok("r2^2 = e", acomp(r2, r2) == AEID)
ok("r3^2 = e", acomp(r3, r3) == AEID)
ok("r1,r2,r3 in Gamma", all(in_Gamma(g) for g in (r1, r2, r3)))

comms = {}
for (i, gi), (j, gj) in itertools.permutations(((1, r1), (2, r2), (3, r3)), 2):
    if i < j:
        c = acomp(acomp(gi, gj), acomp(gi, gj))   # (r_i r_j)^2 = [r_i, r_j] for involutions
        comms[(i, j)] = c
        assert c[0] == I3
tvals = sorted(tuple(int(x) for x in c[1]) for c in comms.values())
ok("commutators (r_i r_j)^2 are pure translations", all(c[0] == I3 for c in comms.values()))
twoEs = sorted([(2,0,0), (0,2,0), (0,0,2)])
got = sorted([tuple(abs(v) for v in t) for t in tvals])
ok(f"commutators give {{2e_k}} (found {tvals})", got == twoEs)

# word search: t_(1,1,1) as a word in r1,r2,r3
gens = {"1": r1, "2": r2, "3": r3}
word111 = None
for length in range(2, 9):
    for wtuple in itertools.product("123", repeat=length):
        g = AEID
        for ch in wtuple: g = acomp(g, gens[ch])
        if g[0] == I3 and tuple(int(x) for x in g[1]) == (1, 1, 1):
            word111 = "".join(wtuple); break
    if word111: break
ok(f"t_(1,1,1) attained as word r-word '{word111}'", word111 is not None)
t111 = aff(I3, (1,1,1))
ok("t_(1,1,1) in Gamma (all-odd in L)", in_Gamma(t111))

# Gamma_2 = Gamma / 2Z^3 : elements (M, t mod 2) with integer t
def m2i(t): return tuple(int(x) % 2 for x in t)
def g2(g): return (g[0], m2i(g[1]))
def g2mul(x, y):
    M = mm(x[0], y[0])
    t = tuple((x[1][i] + sum(x[0][i][j] * y[1][j] for j in range(3))) % 2 for i in range(3))
    return (M, t)
G2 = {g2(AEID)}
frontier = [g2(AEID)]
G2gens = [g2(r1), g2(r2), g2(r3)]
while frontier:
    x = frontier.pop()
    for g in G2gens:
        y = g2mul(x, g)
        if y not in G2:
            G2.add(y); frontier.append(y)
ok("|Gamma_2| = |Gamma/2Z^3| = 8", len(G2) == 8)
ok("Gamma_2 abelian", all(g2mul(x, y) == g2mul(y, x) for x in G2 for y in G2))
ok("Gamma_2 exponent 2", all(g2mul(x, x) == g2(AEID) for x in G2))
note("=> [Gamma,Gamma] = 2Z^3 exactly (super: commutators; sub: Gamma/2Z^3 abelian).")
note("=> Gamma^ab (x) F2 = (Z/2)^3 on rbar_1, rbar_2, rbar_3.  [R1]")

# class map Gamma -> F2^3 (basis rbar_1, rbar_2, rbar_3)
BASECLS = {I3: (0,0,0), A1: (1,0,0), A2: (0,1,0), A3: (0,0,1)}
def cls_aff(g):
    assert in_Gamma(g)
    M, t = g
    v = vsub(t, avec[M])
    vm = m2i(v)
    assert vm in ((0,0,0), (1,1,1)), "L-class error"
    b = BASECLS[M]
    add = (1,1,1) if vm == (1,1,1) else (0,0,0)
    return tuple((b[i] + add[i]) % 2 for i in range(3))
# verify class map is a homomorphism on the full quotient (8x8 via representatives)
reps = {}
for length in range(0, 7):
    for wtuple in itertools.product("123", repeat=length):
        g = AEID
        for ch in wtuple: g = acomp(g, gens[ch])
        key = g2(g)
        if key not in reps: reps[key] = g
    if len(reps) == 8: break
ok("8 coset representatives found", len(reps) == 8)
hom_ok = all(cls_aff(acomp(x, y)) == tuple((cls_aff(x)[i] + cls_aff(y)[i]) % 2 for i in range(3))
             for x in reps.values() for y in reps.values())
ok("class map Gamma -> F2^3 is a homomorphism (64/64 pairs)", hom_ok)
ok("cls(t_111) = rbar1+rbar2+rbar3 = (1,1,1)", cls_aff(t111) == (1,1,1))

# -----------------------------------------------------------------------------
print("=" * 78)
print("PART 1 — H-A: the spin extension over Gamma is NON-SPLIT (falsifier live)")
print("=" * 78)
for f, (q, A) in enumerate(((QI, A1), (QJ, A2), (QK, A3)), start=1):
    ok(f"rho(q_{f}) = A_{f}", rho(q) == A)
    ok(f"q_{f}^2 = -1", q * q == MONE)

# Full (unquotiented) Spin(3) x| R^3 check of deck-rotation squares — BOTH lifts
def sp_comp(a, b):  # (q,t)(q',t') = (qq', t + rho(q) t')
    return (a[0] * b[0], vadd(a[1], mv(rho(a[0]), b[1])))
SPID = (ONE, (F(0),F(0),F(0)))
qmap = {1: QI, 2: QJ, 3: QK}
amap = {1: (F(0),F(0),F(1)), 2: (F(1),F(0),F(0)), 3: (F(0),F(1),F(0))}
cnt = 0
for f in (1,2,3):
    for s in (1, -1):
        el = ((qmap[f] if s == 1 else -qmap[f]), amap[f])
        sq = sp_comp(el, el)
        assert sq[0] == MONE and all(x == 0 for x in sq[1]), "deck square not central -1"
        cnt += 1
ok(f"every lift of every deck pi-rotation squares to (-1, 0)  [{cnt}/6]", cnt == 6)

fails = 0
for signs in itertools.product((1, -1), repeat=3):
    section_ok = True
    for f in (1,2,3):
        el = ((qmap[f] if signs[f-1] == 1 else -qmap[f]), amap[f])
        if sp_comp(el, el) != SPID:      # relation r_f^2 = e must lift to identity
            section_ok = False
    if not section_ok: fails += 1
ok(f"H-A: all 8 generator sign-assignments FAIL to define a section  [{fails}/8 fail]", fails == 8)
note("H-A VERDICT [R1]: 1 -> Z/2 -> Gamma~ -> Gamma -> 1 is NON-SPLIT.")
note("  Every spinorial representation of the flat home's deck group forces -1 |-> -Id.")

# -----------------------------------------------------------------------------
print("=" * 78)
print("PART 2 — H-B / decisive bit B1: ambient-2pi meridian sign, full twist sweep")
print("=" * 78)
note("Loop dictionary (as registered): cone loop m_f |-> chi_f * q_f ;")
note("ambient 2pi meridian mu_f = m_f traversed twice |-> (chi_f q_f)^2.")
b1 = 0
for chi in itertools.product((1, -1), repeat=3):
    for f in (1,2,3):
        m = qmap[f] if chi[f-1] == 1 else -qmap[f]
        M2 = m * m
        assert M2 == MONE, f"B1 FALSIFIER FIRED at chi={chi}, f={f}"
        # cone-loop order check (Z/4 bank):
        assert (M2 * M2) == ONE and M2 != ONE
        b1 += 1
ok(f"B1: mu_f monodromy = -1 for ALL structures x strands  [{b1}/24]", b1 == 24)
note("B1 VERDICT [R1]: the ambient-2pi per-strand spinor sign is -1, twist-independently,")
note("  in every Gamma-spinorial structure. Cone loop m_f has order 4 (sign chi-dependent):")
note("  Z/4 refinement BANKED R3, uninterpreted, per registration.")

# -----------------------------------------------------------------------------
print("=" * 78)
print("PART 3 — N+ generators (solved, not hand-picked), Q~ (384), Hom(Q, F2)")
print("=" * 78)
E1a = aff(I3, (1,0,0)); E2a = aff(I3, (0,1,0)); E3a = aff(I3, (0,0,1))
def normalizes(g):
    gi = ainv(g)
    return all(in_Gamma(acomp(acomp(g, rf), gi)) for rf in (r1, r2, r3)) and \
           all(in_Gamma(acomp(acomp(gi, rf), g)) for rf in (r1, r2, r3))
ok("e_1, e_2, e_3 normalize Gamma; none lies in Gamma",
   all(normalizes(e) and not in_Gamma(e) for e in (E1a, E2a, E3a)))

P  = ((0,0,1),(1,0,0),(0,1,0))     # P e1=e2, P e2=e3, P e3=e1  (check below)
R4 = ((1,0,0),(0,0,-1),(0,1,0))    # +pi/2 about x: e2->e3, e3->-e2
ok("P is the 3-cycle e1->e2->e3 (det +1)",
   mv(P, (F(1),0,0)) == (0,1,0) and mv(P, (0,F(1),0)) == (0,0,1) and mv(P, (0,0,F(1))) == (1,0,0))
ok("R4 is the +pi/2 x-rotation (det +1)",
   mv(R4, (0,F(1),0)) == (0,0,1) and mv(R4, (0,0,F(1))) == (0,-1,0) and mv(R4, (F(1),0,0)) == (1,0,0))

grid = [F(k, 4) for k in range(8)]  # quarter grid mod 2
def solve_b(M):
    sols = []
    for b in itertools.product(grid, repeat=3):
        if normalizes(aff(M, b)): sols.append(b)
    return sols
solP  = solve_b(P)
solR4 = solve_b(R4)
ok(f"c3 translation solutions exist ({len(solP)} on the quarter grid mod 2)", len(solP) > 0)
ok("all c3 solutions integral (even coset unshifted — re-derives an S7 H-B slice)",
   all(all(x.denominator == 1 for x in b) for b in solP))
ok("b = (0,0,0) is a c3 solution", tuple(F(0) for _ in range(3)) in [tuple(b) for b in solP])
ok(f"g4 translation solutions exist ({len(solR4)} on the quarter grid mod 2)", len(solR4) > 0)
ok("all g4 solutions have fractional parts (1/2,1/2,1/2) — re-derives S7's odd-coset shift class",
   all(all(x - math.floor(x) == F(1, 2) for x in b) for b in solR4))
c3a = aff(P, (0, 0, 0))
g4a = aff(R4, sorted(solR4)[0])
note(f"chosen g4 translation part: {tuple(str(x) for x in g4a[1])}")

# ---- 2O (binary octahedral) closure, exact
seeds = [QI, QJ, HUR, W4X]
twoO = set(seeds) | {ONE}
front = list(twoO)
while front:
    x = front.pop()
    for s in seeds:
        y = x * s
        if y not in twoO:
            twoO.add(y); front.append(y)
ok("|2O| = 48 (exact closure)", len(twoO) == 48)
def lifts_of(M):
    return [q for q in twoO if rho(q) == M]
qc3 = lifts_of(P);  ok("exactly two 2O lifts of c3 rotation", len(qc3) == 2)
qg4 = lifts_of(R4); ok("exactly two 2O lifts of g4 rotation", len(qg4) == 2)

# ---- Q~ = N+ /(spin-trivial 2Z^3 translations): elements (q in 2O, t mod 2, halves ok)
def fm2(x): return x - 2 * math.floor(x / 2)
def tm2(t): return tuple(fm2(x) for x in t)
def qt_mul(a, b):
    return (a[0] * b[0], tm2(vadd(a[1], mv(rho(a[0]), b[1]))))
QTID = (ONE, (F(0),F(0),F(0)))
Z    = (MONE, (F(0),F(0),F(0)))
gens_qt = {
    "r1": (QI, tm2(amap[1])), "r2": (QJ, tm2(amap[2])), "r3": (QK, tm2(amap[3])),
    "E1": (ONE, (F(1),F(0),F(0))),
    "c3": (qc3[0], tm2(c3a[1])),
    "g4": (qg4[0], tm2(g4a[1])),
}
Qt = {QTID}
front = [QTID]
while front:
    x = front.pop()
    for g in gens_qt.values():
        y = qt_mul(x, g)
        if y not in Qt:
            Qt.add(y); front.append(y)
ok("|Q~| = 384", len(Qt) == 384)
ok("z = (-1,0) in Q~, z^2 = id", Z in Qt and qt_mul(Z, Z) == QTID)
ok("z central (commutes with all generators)",
   all(qt_mul(Z, g) == qt_mul(g, Z) for g in gens_qt.values()))

def qnorm(q):
    for c in q.comps():
        s = c.sign()
        if s != 0:
            return q if s > 0 else -q
    raise ValueError
def norm_el(x): return (qnorm(x[0]), x[1])
Q = {norm_el(x) for x in Qt}
ok("|Q| = |Q~ / {+-1}| = 192", len(Q) == 192)
def q_mul(a, b): return norm_el(qt_mul(a, b))
QID = norm_el(QTID)

# Gamma~_2 inside Q~ and the 8 structure realizations U_chi
seeds2 = [gens_qt["r1"], gens_qt["r2"], gens_qt["r3"]]
Gt2 = set(seeds2) | {QTID}
front = list(Gt2)
while front:
    x = front.pop()
    for s in seeds2:
        y = qt_mul(x, s)
        if y not in Gt2:
            Gt2.add(y); front.append(y)
ok("|Gamma~_2| = 16 (contains z)", len(Gt2) == 16 and Z in Gt2)

RHO2A = {A1: A1, A2: A2, A3: A3, I3: I3}
def cls_qt(el):
    """class in F2^3 of the Gamma_2-image of an element of Gamma~_2"""
    M = rho(el[0])
    assert M in avec, "not over Gamma"
    t = el[1]
    assert all(x.denominator == 1 for x in t)
    v = tuple((int(t[i]) - int(avec[M][i])) % 2 for i in range(3))
    assert v in ((0,0,0), (1,1,1)), "class error"
    b = BASECLS[M]
    add = (1,1,1) if v == (1,1,1) else (0,0,0)
    return tuple((b[i] + add[i]) % 2 for i in range(3))

realized = 0
for chi in itertools.product((1, -1), repeat=3):
    def chival(c): return chi[0]**c[0] * chi[1]**c[1] * chi[2]**c[2]
    def U(el):
        s = chival(cls_qt(el))
        return el[0] if s == 1 else -el[0]
    good = all(U(qt_mul(x, y)) == U(x) * U(y) for x in Gt2 for y in Gt2)
    good = good and (U(Z) == MONE)
    assert good, f"structure realization failed at chi={chi}"
    realized += 1
ok(f"all 8 twists chi realize genuine structures U_chi (hom 16x16; U(z) = -Id)  [{realized}/8]",
   realized == 8)

# ---- Hom(Q, F2): exhaustive sweep over generator sign assignments
gnames = ["r1", "r2", "r3", "E1", "c3", "g4"]
gQ = {n: norm_el(gens_qt[n]) for n in gnames}
E2q = norm_el((ONE, (F(0),F(1),F(0))))
E3q = norm_el((ONE, (F(0),F(0),F(1))))
T111q = norm_el((ONE, (F(1),F(1),F(1))))
homs = []
for assign in itertools.product((1, -1), repeat=6):
    s = dict(zip(gnames, assign))
    labels = {QID: 1}
    front = [QID]
    consistent = True
    while front and consistent:
        x = front.pop()
        for n in gnames:
            y = q_mul(x, gQ[n])
            lab = labels[x] * s[n]
            if y in labels:
                if labels[y] != lab:
                    consistent = False; break
            else:
                labels[y] = lab; front.append(y)
    if consistent and len(labels) == 192:
        homs.append((s, labels))
ok(f"Hom(Q, F2) enumerated exhaustively: |W| = {len(homs)}", len(homs) >= 1)
note("Hom(Q, F2) table (values on key elements):")
print(f"   {'r1':>3} {'r2':>3} {'r3':>3} | {'E1':>3} {'E2':>3} {'E3':>3} | {'t111':>4} | {'c3':>3} {'g4':>3}")
restr = set()
for s, lab in homs:
    row = (s['r1'], s['r2'], s['r3'], lab[gQ['E1']], lab[E2q], lab[E3q],
           lab[T111q], s['c3'], s['g4'])
    print("   " + " ".join(f"{v:>3}" if i not in (3, 6) else f"{v:>4}" if i == 6 else f"{v:>3}"
                           for i, v in enumerate([f'{r:+d}' for r in row])))
    restr.add((s['r1'], s['r2'], s['r3']))
    # forced identities (falsifiers live):
    assert lab[gQ['E1']] == lab[E2q] == lab[E3q], "S4-collapse of turn-over signs FAILED"
    assert lab[gQ['E1']] * lab[E2q] * lab[E3q] == lab[T111q], "triple relation FAILED"
    assert lab[T111q] == s['r1'] * s['r2'] * s['r3'], "Gamma^ab relation FAILED"
ok("per-hom forced identities all hold (turn-over uniformity; triple product; t111 class)", True)
note(f"Structure twists admissible under full N+ equivariance: {sorted(restr)}")

# ---- conjugation action of N+ on Gamma^ab (x) F2 and invariant characters
def conj_cls(g, rf):
    x = acomp(acomp(g, rf), ainv(g))
    assert in_Gamma(x)
    return cls_aff(x)
Mats = {}
for name, g in (("E1", E1a), ("c3", c3a), ("g4", g4a)):
    cols = [conj_cls(g, rf) for rf in (r1, r2, r3)]
    Mats[name] = cols
    note(f"conjugation matrix (columns = classes of g r_f g^-1) for {name}: {cols}")
inv_chars = []
for chi in itertools.product((0, 1), repeat=3):
    def val(c): return (chi[0]*c[0] + chi[1]*c[1] + chi[2]*c[2]) % 2
    if all(val(Mats[n][f]) == chi[f] for n in Mats for f in range(3)):
        inv_chars.append(chi)
note(f"N+-invariant characters of Gamma^ab (x) F2: {inv_chars}")
restr01 = {tuple(0 if v == 1 else 1 for v in r) for r in restr}
ok("every admissible restriction is an invariant character (necessity check)",
   restr01 <= set(inv_chars))

# -----------------------------------------------------------------------------
print("=" * 78)
print("PART 4 — canonical-lift contrast table and the triple composite (B2 core)")
print("=" * 78)
for f, Eq in ((1, gens_qt["E1"]), (2, (ONE,(F(0),F(1),F(0)))), (3, (ONE,(F(0),F(0),F(1))))):
    for sgn in (ONE, MONE):
        el = ((sgn * Eq[0]), Eq[1])
        sq = qt_mul(el, el)
        assert sq == QTID and el != QTID, "turn-over lift order != 2"
ok("BOTH lifts of every turn-over e_f are involutions in Q~ (square = id, never z)", True)
for f in (1,2,3):
    for sgn in (ONE, MONE):
        el = ((sgn * qmap[f]), tm2(amap[f]))
        assert qt_mul(el, el) == Z, "deck rotation lift order != 4"
ok("BOTH lifts of every deck pi-rotation have square = z in Q~ (order 4)", True)
tripQ = qt_mul(qt_mul(gens_qt["E1"], (ONE,(F(0),F(1),F(0)))), (ONE,(F(0),F(0),F(1))))
ok("canonical (+1)-lifts compose: E1 E2 E3 = (+1)-lift of t_(1,1,1)",
   tripQ == (ONE, (F(1),F(1),F(1))))
note("Per-structure composite of canonical turn-over lifts (deck value of t_111):")
for chi in itertools.product((1, -1), repeat=3):
    v = chi[0] * chi[1] * chi[2]
    print(f"   chi = {chi}:  T_e1 T_e2 T_e3 = {'+Id' if v == 1 else '-Id'}")
note("=> the single Z/2 datum chi(t_111) = chi1*chi2*chi3 carries the entire residual sign.")

# -----------------------------------------------------------------------------
print("=" * 78)
print("PART 5 — positive control: the section solver on the torus subgroup")
print("=" * 78)
found = 0
for signs in itertools.product((1, -1), repeat=3):
    lifts = [((ONE if s == 1 else MONE), t) for s, t in
             zip(signs, ((F(1),F(0),F(0)), (F(0),F(1),F(0)), (F(0),F(0),F(1))))]
    H = set(lifts) | {QTID}
    front = list(H)
    while front:
        x = front.pop()
        for g in lifts:
            y = qt_mul(x, g)
            if y not in H:
                H.add(y); front.append(y)
    if Z not in H and len(H) == 8:
        found += 1
ok(f"solver finds ALL 8 sections over T_N/2Z^3 (the classical T^3 spin structures)  [{found}/8]",
   found == 8)
note("Control passes: the machinery is capable of finding sections when they exist;")
note("the H-A negative is therefore a property of Gamma, not of the solver.")

# -----------------------------------------------------------------------------
print("=" * 78)
print("SUMMARY — decisive bits and registered branch mapping")
print("=" * 78)
print(f"total assertions passed: {PASS}")
print("""
H-A [R1]  : NON-SPLIT. -1 |-> -Id forced for every spinorial object over Gamma.
B1  [R1]  : FORCED(-1). Ambient-2pi meridian monodromy = -1 for every strand,
            across ALL 8 Gamma-spinorial structures (24/24). Cone loop = order 4
            (Z/4 bank, R3, uninterpreted).
B2  [R1]  : GRADED, exactly as the registered (c2)+(c3) decomposition anticipated:
            (i)  every lift of every turn-over is an INVOLUTION (square = +Id,
                 never -Id): the -1 is NOT in the turn-over channel;
            (ii) S4-equivariance collapses the three per-strand signs to ONE
                 global Z/2 = chi(t_111), the body-diagonal antiperiodicity bit;
            (iii) full-N+ homomorphic families: see Hom(Q,F2) table above.
VERDICT CLASS (registered): SPLIT — B1-FORCED + B2-CHOICE with the choice
located as a single boundary-condition bit. NOT a Section 2.50 closure.
""")
with open(__file__, "rb") as fh:
    print("self md5:", hashlib.md5(fh.read()).hexdigest())
