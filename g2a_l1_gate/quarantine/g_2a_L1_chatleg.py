#!/usr/bin/env python3
# =============================================================================
# g_2a_L1_chatleg.py — Gate G-2a-L1 chat leg: the spin-isospin locking assembly
# Locked pre-registration: G_2a_L1_EXECUTION_PREREGISTRATION.md
#   md5 da9c25d19ff91f2c0809ac0027a7bebb (locked before this leg executed)
# Exact arithmetic throughout: Q(sqrt2) Fraction pairs; Cl(3)^q (q = +-1);
# integer matrices; F(3) matrices for the GL(2,3) discriminator.
# NOTE (F4/F5, logged): the registration's D1 pushforward is implemented as an
# ATTEMPT whose failure is exhibited as a THEOREM (z in [Gamma~,Gamma~]); the
# pre-committed re-pose is the obstruction formulation. See report.
# =============================================================================
from fractions import Fraction as Fr
import itertools

ASSERTS = 0
def chk(cond, label):
    global ASSERTS
    if not cond:
        raise AssertionError("FALSIFIER/ASSERT FIRED: " + label)
    ASSERTS += 1

# ---------------------------------------------------------------- Q(sqrt2)
QZ  = (Fr(0), Fr(0)); QONE = (Fr(1), Fr(0)); QMONE = (Fr(-1), Fr(0))
def qadd(a,b): return (a[0]+b[0], a[1]+b[1])
def qmul(a,b): return (a[0]*b[0] + 2*a[1]*b[1], a[0]*b[1] + a[1]*b[0])
def qneg(a):   return (-a[0], -a[1])
INV_SQRT2 = (Fr(0), Fr(1,2))

# ---------------------------------------------------------------- Cl(3)^q
def blade_mul(A, B, q):
    swaps = 0
    for b in range(3):
        if (B >> b) & 1:
            swaps += bin(A >> (b+1)).count('1')
    val = (-1 if (swaps & 1) else 1) * (q ** bin(A & B).count('1'))
    return A ^ B, val

def cscal(v):
    c = [QZ]*8; c[0] = (Fr(v), Fr(0)); return tuple(c)
def cbasis(i):
    c = [QZ]*8; c[1 << i] = QONE; return tuple(c)
def cmul(x, y, q):
    out = [QZ]*8
    for A in range(8):
        xa = x[A]
        if xa == QZ: continue
        for B in range(8):
            yb = y[B]
            if yb == QZ: continue
            C, s = blade_mul(A, B, q)
            v = qmul(xa, yb)
            if s < 0: v = qneg(v)
            out[C] = qadd(out[C], v)
    return tuple(out)
def cadd(x,y): return tuple(qadd(a,b) for a,b in zip(x,y))
def cneg(x):   return tuple(qneg(a) for a in x)
def cscale(x,s): return tuple(qmul(a,s) for a in x)
GRADE = [bin(m).count('1') for m in range(8)]
def alpha(x): return tuple(qneg(a) if GRADE[m] & 1 else a for m,a in enumerate(x))
def rever(x): return tuple(qneg(a) if GRADE[m] in (2,3) else a for m,a in enumerate(x))
def cinv(x, q):
    r = rever(x); s = cmul(x, r, q)
    chk(all(s[m] == QZ for m in range(1,8)), "inv: not scalar")
    chk(s[0] in (QONE, QMONE), "inv: scalar not +-1")
    return r if s[0] == QONE else cneg(r)
def rho(u, q):
    ui = cinv(u, q); au = alpha(u)
    M = [[0]*3 for _ in range(3)]
    for i in range(3):
        y = cmul(cmul(au, cbasis(i), q), ui, q)
        for m in range(8):
            if y[m] != QZ:
                chk(GRADE[m] == 1 and y[m][1] == 0 and y[m][0].denominator == 1,
                    "rho image bad")
        for j in range(3):
            M[j][i] = int(y[1 << j][0])
    return tuple(tuple(r) for r in M)
def mat_vec(M,v): return tuple(sum(Fr(M[i][j])*v[j] for j in range(3)) for i in range(3))
def mat_mul(M,N): return tuple(tuple(sum(M[i][k]*N[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
IDM = ((1,0,0),(0,1,0),(0,0,1))

class Ctx:
    def __init__(self, q):
        self.q = q; self.rc = {}
    def R(self, u):
        if u not in self.rc: self.rc[u] = rho(u, self.q)
        return self.rc[u]
    def amul(self, g, h):
        return (cmul(g[0], h[0], self.q),
                tuple(a+b for a,b in zip(g[1], mat_vec(self.R(g[0]), h[1]))))
    def ainv(self, g):
        ui = cinv(g[0], self.q)
        return (ui, tuple(-x for x in mat_vec(self.R(ui), g[1])))
def taumod2(t): return tuple(x % 2 for x in t)
def amod(g): return (g[0], taumod2(g[1]))

# =============================== PART 1+2+3: per-algebra flat-home rebuild ===
def flat_home(q, name):
    print(f"\n=== {name} (e_i^2 = {q:+d}) ===")
    X = Ctx(q)
    E1,E2,E3 = cbasis(0), cbasis(1), cbasis(2)
    ONE, MONE = cscal(1), cscal(-1)
    q1 = cmul(E2,E3,q); q2 = cmul(E3,E1,q); q3 = cmul(E1,E2,q)
    for qq in (q1,q2,q3):
        chk(cmul(qq,qq,q) == MONE, "bivector^2=-1 (Pin-blind Spin sector, F1)")
    omega = cmul(q3, E3, q)
    chk(cmul(omega,omega,q) == cscal(-q), "omega^2=-q (F1)")
    W12 = cscale(cadd(E1, cneg(E2)), INV_SQRT2)
    W23 = cscale(cadd(E2, cneg(E3)), INV_SQRT2)
    u_c3 = cmul(W23, W12, q)
    r1 = (q1, (Fr(0),Fr(0),Fr(1)))
    r2 = (q2, (Fr(1),Fr(0),Fr(0)))
    r3 = (q3, (Fr(0),Fr(1),Fr(0)))
    te1 = (ONE, (Fr(1),Fr(0),Fr(0)))
    n_c3 = (u_c3, (Fr(0),Fr(0),Fr(0)))
    h = (W23, (Fr(1,2),Fr(1,2),Fr(1,2)))
    n_inv = (omega, (Fr(0),Fr(0),Fr(0)))
    # F1 anchors
    hh = X.amul(h,h)
    chk(hh[0] in (ONE,MONE) and hh[1] == (Fr(1),Fr(1),Fr(1)), "h^2 covers t111 (F1)")
    glide = X.amul(r1, n_inv)
    chk(X.R(glide[0]) == ((-1,0,0),(0,1,0),(0,0,1)) and glide[1] == (Fr(0),Fr(0),Fr(1)),
        "glide = r1 o (-I) (F1)")
    for rf in (r1,r2,r3):
        sq = X.amul(rf, rf)
        chk(sq[0] == MONE and sq[1] == (Fr(0),Fr(0),Fr(0)), "meridian -1 (F1)")
    # BFS closures (F1)
    gens = [amod(g) for g in (r1,r2,r3,te1,n_c3,h,n_inv)]
    def bfs(gg0):
        idel = (ONE,(Fr(0),Fr(0),Fr(0)))
        seen = {idel: None}; frontier=[idel]
        gg = gg0 + [amod(X.ainv(g)) for g in gg0]
        while frontier:
            nxt=[]
            for e in frontier:
                for g in gg:
                    p = amod(X.amul(e,g))
                    if p not in seen:
                        seen[p]=None; nxt.append(p)
            frontier=nxt
        return list(seen.keys())
    Gt = bfs(gens)
    chk(len(Gt) == 768, "|G~_fin|=768 (F1)")
    Gam_t = bfs([amod(g) for g in (r1,r2,r3)])
    chk(len(Gam_t) == 16, "|Gamma~_2|=16 (F1)")
    proj = {}
    for e in Gt: proj.setdefault((X.R(e[0]), e[1]), e)
    chk(len(proj) == 384, "|G_fin|=384 (F1)")
    Gam_proj = set((X.R(e[0]), e[1]) for e in Gam_t)
    chk(len(Gam_proj) == 8, "|Gamma_fin|=8 (F1)")
    # axial-law spot check (S10 regression)
    tau_g = {0:r1[1],1:r2[1],2:r3[1]}
    qs = (q1,q2,q3)
    for n in (n_c3, h, n_inv, te1):
        Pn = X.R(n[0]); dP = det3(Pn)
        axial = tuple(tuple(dP*Pn[i][j] for j in range(3)) for i in range(3))
        for f in range(3):
            c = X.amul(X.amul(n, (qs[f], tau_g[f])), X.ainv(n))
            hit = None
            for fp in range(3):
                if c[0] == qs[fp]: hit=(fp,1)
                if c[0] == cneg(qs[fp]): hit=(fp,-1)
            chk(hit is not None, "axial spot: conjugate is +-q_f'")
            fp,s = hit
            col = [axial[jj][f] for jj in range(3)]
            chk(sum(1 for v in col if v!=0)==1 and col[fp]==s, "axial law (S10 regression)")
    # characters trivial on Gamma (C-layer)
    def chi_sgn(P):
        sig = tuple(next(j for j in range(3) if P[j][i]!=0) for i in range(3))
        inv = sum(1 for a in range(3) for b in range(a+1,3) if sig[a]>sig[b])
        return -1 if inv & 1 else 1
    for gp in Gam_proj:
        chk(chi_sgn(gp[0]) == 1 and det3(gp[0]) == 1, "characters trivial on Gamma")
    # ---------------- PART 2: the motion group M = G_fin / Gamma_fin -------
    # affine-only model of G_fin (no Clifford): (P, tau) with tau mod 2
    def pm(a, b):  # (P,t)*(P',t')
        return (mat_mul(a[0], b[0]), taumod2(tuple(x+y for x,y in zip(a[1], mat_vec(a[0], b[1])))))
    def pinv(a):
        Pi = tuple(tuple(a[0][j][i] for j in range(3)) for i in range(3))  # orthogonal int: inverse = transpose
        chk(mat_mul(Pi, a[0]) == IDM, "point inverse = transpose")
        return (Pi, taumod2(tuple(-x for x in mat_vec(Pi, a[1]))))
    Gfin = list(proj.keys())
    Gam = sorted(Gam_proj)
    Gset = set(Gfin)
    for gp in Gam: chk(gp in Gset, "Gamma_fin inside G_fin")
    # cosets
    def coset_key(g):
        return min(pm(g, gp) for gp in Gam)
    ck = {}
    for g in Gfin: ck[g] = coset_key(g)
    cosets = sorted(set(ck.values()))
    chk(len(cosets) == 48, "|M| = 48")
    cid = {c:i for i,c in enumerate(cosets)}
    def mprod(i, j): return cid[coset_key(pm(cosets[i], cosets[j]))]
    def minv(i): return cid[coset_key(pinv(cosets[i]))]
    ident = cid[coset_key((IDM, (Fr(0),Fr(0),Fr(0))))]
    # multiplication table + group checks
    MT = [[mprod(i,j) for j in range(48)] for i in range(48)]
    for i in range(48):
        chk(MT[ident][i] == i and MT[i][ident] == i, "M identity")
        chk(MT[i][minv(i)] == ident, "M inverses")
    # center
    center = [i for i in range(48) if all(MT[i][j] == MT[j][i] for j in range(48))]
    chk(len(center) == 2, "Z(M) = Z/2")
    c_inv_coset = cid[coset_key((tuple(tuple(-1 if a==b else 0 for b in range(3)) for a in range(3)), (Fr(0),Fr(0),Fr(0))))]
    chk(set(center) == {ident, c_inv_coset}, "central element = the -I class (S9)")
    # det well-defined on cosets; M+ = det +1
    for c in cosets:
        chk(all(det3(pm(c,gp)[0]) == det3(c[0]) for gp in Gam), "det constant on cosets")
    Mplus = [i for i in range(48) if det3(cosets[i][0]) == 1]
    chk(len(Mplus) == 24, "|M+| = 24")
    chk(c_inv_coset not in Mplus, "-I class improper")
    # conjugacy classes of M+
    Mp = set(Mplus)
    chk(all(MT[i][j] in Mp for i in Mplus for j in Mplus), "M+ closed")
    def conj_classes(elems):
        rem = set(elems); cls=[]
        while rem:
            x = min(rem); orb = set()
            for g in elems:
                orb.add(MT[MT[g][x]][minv(g)])
            cls.append(sorted(orb)); rem -= orb
        return cls
    ccM = conj_classes(Mplus)
    sizes = sorted(len(c) for c in ccM)
    chk(sizes == [1,3,6,6,8], "M+ class sizes = S4's [1,3,6,6,8]")
    # element orders sanity (S4: orders 1,2,2,3,4)
    def order_of(i):
        k=1; x=i
        while x != ident: x = MT[x][i]; k+=1
        return k
    ordset = sorted(set(order_of(c[0]) for c in ccM))
    chk(ordset == [1,2,3,4], "M+ element orders {1,2,3,4} (S4)")
    chk(len([1 for c in ccM if order_of(c[0])==2]) == 2, "two involution classes (3+6)")
    # M = Z x M+ (direct product)
    chk(all(MT[c_inv_coset][m] == MT[m][c_inv_coset] for m in Mplus), "central commutes")
    chk(len({MT[z][m] for z in center for m in Mplus}) == 48, "M = Z/2 x S4 (direct)")
    print("  M = N/Gamma verified: Z/2 x S4; center = the -I class; M+ = S4 with classes [1,3,6,6,8]")
    # ---------------- PART 3: B1 — the obstruction --------------------------
    # z is a commutator in Gamma~_2: [q~1, q~2] = z exactly (finite model)
    zt = (MONE, (Fr(0),Fr(0),Fr(0)))
    r1m, r2m = amod(r1), amod(r2)
    comm = amod(X.amul(X.amul(r1m, r2m), X.amul(X.ainv(r1m), X.ainv(r2m))))
    chk(comm == zt, "B1 OBSTRUCTION: z = [q~1, q~2] in Gamma~_2 (z is a commutator)")
    # exhaustive: every Hom(Gamma~_2, Z/2) kills z
    # derived subgroup of Gamma~_2
    Gam_t_set = set(Gam_t)
    D = set()
    for a in Gam_t:
        for b in Gam_t:
            D.add(amod(X.amul(X.amul(a,b), X.amul(X.ainv(a), X.ainv(b)))))
    # closure of commutator set under multiplication
    Dg = {amod((ONE,(Fr(0),Fr(0),Fr(0))))}
    frontier = list(D)
    while frontier:
        nxt=[]
        for x in frontier:
            for y in list(D):
                p = amod(X.amul(x,y))
                if p not in Dg:
                    Dg.add(p); nxt.append(p)
            if x not in Dg: Dg.add(x)
        frontier = nxt
    chk(zt in Dg, "z in derived subgroup of Gamma~_2")
    # characters = homs Gamma~_2 -> {+-1}: brute force on generator images
    hom_count = 0
    gens3 = [r1m, r2m, amod(r3)]
    # build word representation for each element via BFS with words
    idel = amod((ONE,(Fr(0),Fr(0),Fr(0))))
    words = {idel: ()}
    frontier=[idel]
    gg = gens3 + [amod(X.ainv(g)) for g in gens3]
    lab = {0:0,1:1,2:2,3:0,4:1,5:2}  # inverse letters map to same generator index (order-4: g^-1 = g^3; char value same as g^(+-1) -> chi(g)^(-1)=chi(g))
    while frontier:
        nxt=[]
        for e in frontier:
            for k,g in enumerate(gg):
                p = amod(X.amul(e,g))
                if p not in words:
                    words[p] = words[e] + (lab[k],)
                    nxt.append(p)
        frontier=nxt
    chk(len(words) == 16, "word cover of Gamma~_2")
    for eps in itertools.product((1,-1), repeat=3):
        val = {}
        ok = True
        for el, w in words.items():
            v = 1
            for L in w: v *= eps[L]
            val[el] = v
        for a in Gam_t:
            for b in Gam_t:
                if val[amod(X.amul(a,b))] != val[a]*val[b]: ok=False; break
            if not ok: break
        if ok:
            hom_count += 1
            chk(val[zt] == 1, "every character of Gamma~_2 kills z (B1 obstruction, exhaustive)")
    chk(hom_count >= 1, "trivial character found (sanity)")
    print(f"  B1: z = [q~1,q~2]; {hom_count} characters on Gamma~_2, all kill z ->")
    print("      NO equivariant pushforward of 1->Gamma~->N~->M->1 to a Z/2-extension exists.")
    # D2 collapse lemma: the quotient N~/Gamma~ has order 48 = |M| (the sign is absorbed)
    lift_cosets = set()
    Gam_t_sorted = sorted(Gam_t)
    for e in Gt:
        lift_cosets.add(min(amod(X.amul(e, gp)) for gp in Gam_t_sorted))
    chk(len(lift_cosets) == 48, "D2 collapse: |N~_fin / Gamma~_fin| = 48 = |M| (no residual Z/2)")
    print("  D2 collapse lemma VERIFIED: the static home absorbs the sign (z in the deck image).")
    return True

flat_home(+1, "Pin+ / Cl(3,0)")
flat_home(-1, "Pin- / Cl(0,3)")

# ====================== PART 4: F2 discriminators (Spin-side, Pin-blind) =====
print("\n=== F2 discriminators + B2/B3 (Spin sector; Pin-blind per bivector^2 regression) ===")
q = +1
X = Ctx(q)
E1,E2,E3 = cbasis(0), cbasis(1), cbasis(2)
ONE, MONE = cscal(1), cscal(-1)
W12 = cscale(cadd(E1, cneg(E2)), INV_SQRT2)
W23 = cscale(cadd(E2, cneg(E3)), INV_SQRT2)
u4 = cscale(cadd(ONE, cmul(E1,E2,q)), INV_SQRT2)     # lift of C4 about e3
u3 = cmul(W23, W12, q)                                # lift of C3 (x,y,z)->(y,z,x)-type
P4 = rho(u4, q)
chk(P4 in (((0,-1,0),(1,0,0),(0,0,1)), ((0,1,0),(-1,0,0),(0,0,1))),
    "rho(u4) is a C4 about e3 (either orientation; convention not load-bearing)")
chk(det3(P4) == 1 and mat_mul(mat_mul(P4,P4),mat_mul(P4,P4)) == IDM
    and mat_mul(P4,P4) != IDM, "rho(u4) order 4, proper")
# BFS 2O
seen = {ONE: None}; frontier=[ONE]
gg2 = [u4, u3, cinv(u4,q), cinv(u3,q)]
while frontier:
    nxt=[]
    for e in frontier:
        for g in gg2:
            p = cmul(e,g,q)
            if p not in seen:
                seen[p]=None; nxt.append(p)
    frontier=nxt
TwoO = list(seen.keys())
chk(len(TwoO) == 48, "|2O| = 48")
invols = [u for u in TwoO if cmul(u,u,q) == ONE and u != ONE]
chk(invols == [MONE] or invols == [cneg(ONE)] or (len(invols)==1 and invols[0]==MONE),
    "2O has a UNIQUE involution = -1 (binary-cover fingerprint)")
# projection to O
Omats = {}
for u in TwoO: Omats.setdefault(rho(u,q), []).append(u)
chk(len(Omats) == 24 and all(len(v)==2 for v in Omats.values()), "2O -> O double cover")
Olist = sorted(Omats.keys())
chk(all(det3(P) == 1 for P in Olist), "O proper")
# O group ops
def omul(A,B): return mat_mul(A,B)
def oinv(A): return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))
def oord(A):
    k=1; Xm=A
    while Xm != IDM: Xm = omul(Xm,A); k+=1
    return k
def occ(elems):
    rem = set(elems); cls=[]
    while rem:
        x = min(rem); orb=set()
        for g in elems: orb.add(omul(omul(g,x), oinv(g)))
        cls.append(sorted(orb)); rem -= orb
    return cls
Occ = occ(Olist)
csz = sorted((len(c), oord(c[0])) for c in Occ)
chk(csz == [(1,1),(3,2),(6,2),(6,4),(8,3)], "O ~ S4 classes: sizes/orders [(1,1),(3,2),(6,2),(6,4),(8,3)]")
# sgn character of O: kernel = derived subgroup (A4)
Dgen = set()
for a in Olist:
    for b in Olist:
        Dgen.add(omul(omul(a,b), omul(oinv(a), oinv(b))))
Der = {IDM}; frontier=list(Dgen)
while frontier:
    nxt=[]
    for x in frontier:
        for y in list(Dgen):
            p = omul(x,y)
            if p not in Der: Der.add(p); nxt.append(p)
        if x not in Der: Der.add(x)
    frontier=nxt
chk(len(Der) == 12, "[O,O] = A4")
def sgnO(P): return 1 if P in Der else -1
chk(all(sgnO(omul(a,b)) == sgnO(a)*sgnO(b) for a in Olist[:8] for b in Olist), "sgn homomorphism")
# transposition class (size 6, order 2): 2O preimages have order 4
def cord(u):
    k=1; x=u
    while x != ONE: x = cmul(x,u,q); k+=1
    return k
for c in Occ:
    if len(c) == 6 and oord(c[0]) == 2:
        for P in c:
            for u in Omats[P]:
                chk(cord(u) == 4, "2O: transposition-class preimages order 4")
    if len(c) == 3:
        for P in c:
            for u in Omats[P]:
                chk(cord(u) == 4, "2O: double-transposition preimages order 4")
# GL(2,3) reference
F3 = [0,1,2]
GL = []
for a,b,c_,d in itertools.product(F3, repeat=4):
    if (a*d - b*c_) % 3 != 0: GL.append((a,b,c_,d))
chk(len(GL) == 48, "|GL(2,3)| = 48")
def gmul(m,n):
    a,b,c_,d = m; e,f,g_,h_ = n
    return ((a*e+b*g_)%3, (a*f+b*h_)%3, (c_*e+d*g_)%3, (c_*f+d*h_)%3)
def gord(m):
    k=1; x=m
    while x != (1,0,0,1): x = gmul(x,m); k+=1
    return k
IDG = (1,0,0,1); MIG = (2,0,0,2)
# PGL classes: quotient by {I, -I}
def pkey(m): return min(m, gmul(MIG, m))
pel = sorted(set(pkey(m) for m in GL))
chk(len(pel) == 24, "|PGL(2,3)| = 24")
# find a PGL order-2 element in the size-6 class with a genuine involution preimage
def pmul_(a,b): return pkey(gmul(a,b))
def pcc(elems):
    rem=set(elems); cls=[]
    def pinv_(m):
        k = m
        while pmul_(k, m) != pkey(IDG): k = pmul_(k, m)
        return k
    while rem:
        x=min(rem); orb=set()
        for g in elems:
            gi = pinv_(g)
            orb.add(pmul_(pmul_(g,x), gi))
        cls.append(sorted(orb)); rem-=orb
    return cls
Pcc = pcc(pel)
def pord(m):
    k=1; x=m
    while x != pkey(IDG): x = pmul_(x,m); k+=1
    return k
found_gl_fingerprint = False
for c in Pcc:
    if len(c) == 6 and pord(c[0]) == 2:
        # preimages in GL of each: m and -m; check one has order 2
        for pk in c:
            pre = [pk, gmul(MIG, pk)]
            chk(any(gord(m) == 2 for m in pre),
                "GL(2,3): transposition-class HAS an involution preimage (distinct cover)")
        found_gl_fingerprint = True
chk(found_gl_fingerprint, "GL(2,3) size-6 order-2 class located")
print("  F2 discriminator PASSES: 2O (all order-2 classes lift at order 4) vs GL(2,3) (involution preimages exist) separated.")

# ====================== PART 5: B2 — lifts over S4 and the module ============
# count homs alpha: 2O -> 2O covering the identity of the S4-quotients
# word representation of 2O on generators u4, u3
words = {ONE: ()}
frontier=[ONE]
G4 = [(u4, 'a'), (u3, 'b'), (cinv(u4,q), 'A'), (cinv(u3,q), 'B')]
while frontier:
    nxt=[]
    for e in frontier:
        for g,L in G4:
            p = cmul(e,g,q)
            if p not in words:
                words[p] = words[e] + (L,)
                nxt.append(p)
    frontier=nxt
chk(len(words) == 48, "word cover of 2O")
def eval_word(w, a_img, b_img):
    v = ONE
    ai = cinv(a_img, q); bi = cinv(b_img, q)
    d = {'a': a_img, 'b': b_img, 'A': ai, 'B': bi}
    for L in w: v = cmul(v, d[L], q)
    return v
lifts = []
for ea, eb in itertools.product((1,-1), repeat=2):
    a_img = u4 if ea==1 else cneg(u4)
    b_img = u3 if eb==1 else cneg(u3)
    # consistency: same element via different words must map identically;
    # equivalently the induced map is well-defined AND a homomorphism.
    img = {}
    ok = True
    for el, w in words.items():
        img[el] = eval_word(w, a_img, b_img)
    for x in TwoO:
        for y in (u4, u3, MONE, cneg(u3)):
            if img[cmul(x,y,q)] != cmul(img[x], img[y], q): ok=False; break
        if not ok: break
    if ok:
        chk(rho(img[u4], q) == rho(u4, q) and rho(img[u3], q) == rho(u3, q),
            "lift covers the identity on S4")
        chk(img[MONE] == MONE, "lift fixes z")
        lifts.append((ea,eb,img))
chk(len(lifts) == 2, "exactly 2 lifts over id_{S4} (torsor over Hom(S4,Z/2))")
# characters: chi_J via Chebyshev U_{2J}(scalar part)
def scal(u): return u[0]
def chebU(n, s):
    U0, U1 = QONE, qmul((Fr(2),Fr(0)), s)
    if n == 0: return U0
    if n == 1: return U1
    for _ in range(n-1):
        U0, U1 = U1, qadd(qmul(qmul((Fr(2),Fr(0)), s), U1), qneg(U0))
    return U1
def chiJ(twoJ, u): return chebU(twoJ, scal(u))
chk(all(chiJ(1,u) == qmul((Fr(2),Fr(0)), scal(u)) for u in TwoO[:6]), "chi_{1/2} = 2s")
# S1 regressions: <chi_{3/2}, chi_{3/2}> = 1; chi_{3/2}(z) = -4
acc = QZ
for u in TwoO:
    acc = qadd(acc, qmul(chiJ(3,u), chiJ(3,u)))
chk(acc == (Fr(48), Fr(0)), "<chi_3/2, chi_3/2> = 1 over 2O (S1 regression)")
chk(chiJ(3, MONE) == (Fr(-4), Fr(0)), "chi_3/2(z) = -4 (S1 regression)")
# sgn-twist invisibility on the 4 (module transport unique)
for u in TwoO:
    s = sgnO(rho(u, q))
    if s == -1:
        chk(chiJ(3,u) == QZ, "chi_3/2 vanishes on odd classes -> sgn-twist fixes the 4 (B2)")
print("  B2: exactly 2 lifts over id_{S4}, both fixing z; the sgn-twist acts trivially on the")
print("      4-dim module (chi_3/2 odd-class-supported nowhere) -> module transport UNIQUE.")

# ====================== PART 6: B3 — the admissibility lattice ===============
def lattice(elems, denom, use_sgn):
    tab = {}
    for twoJ in (1,3,5,7):
        for twoI in (1,3,5):
            acc = QZ
            for u in elems:
                t = qmul(chiJ(twoJ,u), chiJ(twoI,u))
                if use_sgn and sgnO(rho(u,q)) == -1: t = qneg(t)
                acc = qadd(acc, t)
            chk(acc[1] == 0 and acc[0] % denom == 0, "multiplicity integral")
            m = int(acc[0] // denom)
            chk(m >= 0, "multiplicity nonnegative")
            tab[(twoJ,twoI)] = m
    return tab
tab_triv = lattice(TwoO, 48, False)
tab_sgn  = lattice(TwoO, 48, True)
TwoT = [u for u in TwoO if sgnO(rho(u,q)) == 1]
chk(len(TwoT) == 24, "|2T| = 24 (preimage of A4)")
tab_T = lattice(TwoT, 24, False)
# parity law: nonzero => J+I integer
for tab in (tab_triv, tab_sgn, tab_T):
    for (tJ,tI), m in tab.items():
        if m != 0:
            chk((tJ + tI) % 2 == 0, "parity law: m!=0 -> J+I integer (half-integer isospin forced)")
def show(tab, name):
    print(f"  {name}: (2J,2I)->m :", {k:v for k,v in sorted(tab.items()) if v != 0})
show(tab_triv, "2O-locked, chi_FR=triv")
show(tab_sgn,  "2O-locked, chi_FR=sgn ")
show(tab_T,    "2T-restricted (repr.) ")

print(f"\nALL CHECKS PASS. Assertions: {ASSERTS}")
print("B1: NOT-INDUCED-BY-OBSTRUCTION (z = [q~1,q~2]; all characters kill z; D2 collapse verified)")
print("B2: ASSEMBLED-RELOCATED on the loop-sector substrate; lifts = 2, module transport unique")
print("B3: admissibility lattices above; parity law machine-verified; Assignment: NEUTRAL")
