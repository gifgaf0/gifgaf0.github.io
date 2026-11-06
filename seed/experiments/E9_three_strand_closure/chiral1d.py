"""
E9 chiral term, 1D calculations (NOTE_chiral_term.md §8 items 1 and 2; PREREG_chiral1d.md).
Label: Exploration. Model units only (gl3.py coordinates, xi = 1/sqrt 2). No particle identification.

Locked model (A5, A6). psi = (psi_1, psi_2, psi_3) complex 3-vector, depending on s = n.x only.
Energy per unit area over one periodic cell s in [0, P):
  int ds [ sum_jk |D_j psi_k|^2 + 1/2 sum_k (|psi_k|^2-1)^2 - eta sum_{i<j} Re(psi_i psi_j*)
           + 1/2 |n x A'|^2 + gamma Re( psi*.(n x psi') - i e psi*.(A x psi) ) ]
with D_j psi_k = n_j psi_k' - i e A_j psi_k.

Lattice (M sites, spacing h = P/M, periodic):
  psi_k on sites; A_par = n.A on links s -> s+1 (U_s = exp(-i e h A_par,s)); A_perp (2 components in an
  orthonormal basis e1, e2 of the plane perpendicular to n) on sites.
  sum_jk |D_j psi_k|^2 = sum_k |D_s psi_k|^2 + e^2 |A_perp|^2 |psi|^2 exactly (n.A_perp = 0), with the
    covariant forward difference D_s psi(s) = (U_s psi(s+1) - psi(s))/h.
  magnetic: 1/2 |n x A'|^2 = 1/2 |A_perp'|^2, forward difference on sites.
  chiral: covariant CENTRAL difference,
    C = h sum_s psi*(s).( n x [U_s psi(s+1) - U*_{s-1} psi(s-1)] )/(2h)  - i e h sum_s psi*(s).(A_perp(s) x psi(s)),
    which is real identically (checked); the code evaluates the equal expression
    sum_s Re[psi*(s).(n x U_s psi(s+1))] + h sum_s Re(-i e psi*.(A_perp x psi)).
  The parallel part of -ie psi*.(A x psi) is carried by the links U_s, which makes the term exactly gauge covariant.
"""
import numpy as np, json, sys, time, os
from scipy.optimize import minimize

E_CH = 1/np.sqrt(12.0)          # kappa = 2 (E9)
H_TARGET = 0.05
P_GRID = np.geomspace(1.5, 80.0, 24)
GAMMA_BRACKET = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
GAIN_TOL = -1e-8
BISECT_TOL = 1e-3
NHAT = {'z': np.array([0., 0., 1.]),
        'diag': np.array([1., 1., 1.])/np.sqrt(3),
        'perp': np.array([1., -1., 0.])/np.sqrt(2)}
DHAT = np.array([1., 1., 1.])/np.sqrt(3)
SOLVER = dict(maxiter=40000, maxfun=80000, gtol=1e-10, ftol=1e-16, maxcor=20)

def cross(u, v):
    return np.stack([u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]])

def perp_basis(n):
    t = np.array([1., 0., 0.]) if abs(n[0]) < 0.9 else np.array([0., 1., 0.])
    e1 = t - n*np.dot(t, n); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    return e1, e2

def e_vac(eta):
    return 3*(0.5*eta**2 - eta*(1+eta))


class Chain:
    def __init__(self, n, eta, gamma, P, Afree=True, M=None, e=E_CH):
        self.n = np.asarray(n, float); self.n /= np.linalg.norm(self.n)
        self.e1, self.e2 = perp_basis(self.n)
        self.eta, self.gamma, self.P, self.Afree, self.e = eta, gamma, P, Afree, e
        self.M = int(round(P/H_TARGET)) if M is None else M
        self.h = P/self.M
        self.nA = 3*self.M if Afree else 0

    # ---- packing ----
    def pack(self, psi, a=None, c=None):
        v = [psi.real.ravel(), psi.imag.ravel()]
        if self.Afree: v += [a, c.ravel()]
        return np.concatenate(v)
    def unpack(self, x):
        M = self.M
        psi = (x[:3*M] + 1j*x[3*M:6*M]).reshape(3, M)
        if self.Afree:
            a = x[6*M:7*M]; c = x[7*M:9*M].reshape(2, M)
        else:
            a = np.zeros(M); c = np.zeros((2, M))
        return psi, a, c
    def ncross(self, v):
        return cross(np.broadcast_to(self.n[:, None], v.shape), v)
    def Aperp(self, c):
        return c[0]*self.e1[:, None] + c[1]*self.e2[:, None]

    # ---- energy pieces (all per unit area over the cell) ----
    def parts(self, x, gamma=None):
        g = self.gamma if gamma is None else gamma
        psi, a, c = self.unpack(x); h, e, eta = self.h, self.e, self.eta
        U = np.exp(-1j*e*h*a); psi1 = np.roll(psi, -1, axis=1)
        D = (U*psi1 - psi)/h
        rho = np.abs(psi)**2; rt = rho.sum(0); A2 = (c**2).sum(0)
        Ap = self.Aperp(c)
        S = np.real(1j*cross(psi, np.conj(psi)))
        W = np.sum(np.conj(psi)*self.ncross(U*psi1), axis=0)
        out = dict(
            gradient=h*np.sum(np.abs(D)**2) + h*e**2*np.sum(A2*rt),
            potential=h*0.5*np.sum((rho-1)**2),
            josephson=-eta*h*sum(np.sum(np.real(psi[i]*np.conj(psi[j]))) for i in range(3) for j in range(i+1, 3)),
            magnetic=h*0.5*np.sum(((np.roll(c, -1, axis=1)-c)/h)**2),
            chiral_link=g*np.sum(np.real(W)),
            chiral_AperpS=g*h*np.sum(-e*np.sum(Ap*S, axis=0)))
        out['chiral'] = out['chiral_link'] + out['chiral_AperpS']
        out['total'] = out['gradient']+out['potential']+out['josephson']+out['magnetic']+out['chiral']
        return out

    def energy_grad(self, x):
        g = self.gamma
        psi, a, c = self.unpack(x); h, e, eta, M = self.h, self.e, self.eta, self.M
        U = np.exp(-1j*e*h*a); psi1 = np.roll(psi, -1, axis=1)
        Upsi1 = U*psi1
        D = (Upsi1 - psi)/h
        rho = np.abs(psi)**2; rt = rho.sum(0); A2 = (c**2).sum(0)
        Ap = self.Aperp(c)
        Npsi = self.ncross(psi); NUpsi1 = self.ncross(Upsi1)
        W = np.sum(np.conj(psi)*NUpsi1, axis=0)
        S = np.real(1j*cross(psi, np.conj(psi)))
        tot = psi.sum(0)
        E = (h*np.sum(np.abs(D)**2) + h*e**2*np.sum(A2*rt) + h*0.5*np.sum((rho-1)**2)
             - eta*h*0.5*np.sum(np.abs(tot)**2 - rt)                      # = -eta h sum_{i<j} Re(psi_i psi_j*)
             + h*0.5*np.sum(((np.roll(c, -1, axis=1)-c)/h)**2)
             + g*np.sum(np.real(W)) - g*h*e*np.sum(Ap*S))
        # Wirtinger derivative dE/dpsi*
        dps = (-D + np.roll(np.conj(U)*D, 1, axis=1)
               + h*e**2*A2*psi + h*(rho-1)*psi - 0.5*eta*h*(tot - psi)
               + 0.5*g*(NUpsi1 - np.roll(np.conj(U)*Npsi, 1, axis=1))
               + g*h*(-1j*e)*cross(Ap, psi))
        gr = [2*dps.real.ravel(), 2*dps.imag.ravel()]
        if self.Afree:
            ga = h*np.sum(2*e*np.imag(np.conj(D)*Upsi1), axis=0) + g*e*h*np.imag(W)
            gc = (2*h*e**2*c*rt + (2*c - np.roll(c, -1, axis=1) - np.roll(c, 1, axis=1))/h
                  - g*h*e*np.stack([self.e1 @ S, self.e2 @ S]))
            gr += [ga, gc.ravel()]
        return E, np.concatenate(gr)

    # ---- states ----
    def vacuum(self):
        f0 = np.sqrt(1+self.eta)
        psi = f0*np.ones((3, self.M), complex)
        return self.pack(psi, np.zeros(self.M), np.zeros((2, self.M)))
    def seed(self, kind, rng_seed=0, amp=0.05):
        x = self.vacuum(); s = np.arange(self.M)*self.h; q = 2*np.pi/self.P
        if kind in ('R', 'L'):
            sg = 1 if kind == 'R' else -1
            d = amp*(np.outer(self.e1, np.cos(q*s)) + sg*np.outer(self.e2, np.sin(q*s)))  # rotates e1 -> e2 (R) about n
            psi, a, c = self.unpack(x); psi = psi + d
            return self.pack(psi, a, c)
        if kind == 'noise':
            rng = np.random.default_rng(rng_seed)
            return x + amp*rng.normal(size=x.size)
        raise ValueError(kind)
    def winding_seed(self):
        f0 = np.sqrt(1+self.eta); s = np.arange(self.M)*self.h
        psi = f0*np.ones((3, self.M), complex); psi[0] = f0*np.exp(2j*np.pi*s/self.P)
        return self.pack(psi, np.zeros(self.M), np.zeros((2, self.M)))

    def solve(self, x0):
        t0 = time.time()
        r = minimize(self.energy_grad, x0, jac=True, method='L-BFGS-B', options=SOLVER)
        return r, time.time()-t0

    # ---- diagnostics ----
    def axial_gauge(self, x):
        psi, a, c = self.unpack(x)
        if not self.Afree: return x
        ab = a.mean(); alpha = np.concatenate([[0.], np.cumsum(-self.e*self.h*(a - ab))[:-1]])
        return self.pack(psi*np.exp(1j*alpha), np.full(self.M, ab), c)

    def diagnostics(self, x):
        x = self.axial_gauge(x)
        pt = self.parts(x); psi, a, c = self.unpack(x); P = self.P
        d = {k: v/P for k, v in pt.items()}
        d['gain'] = pt['total']/P - e_vac(self.eta)
        # literal split of the chiral term in the axial gauge (A_par = const = abar)
        W0 = np.sum(np.conj(psi)*self.ncross(np.roll(psi, -1, axis=1)), axis=0)
        d['chiral_twist'] = self.gamma*np.sum(np.real(W0))/P            # gamma Re psi*.(n x psi')
        d['chiral_AS'] = d['chiral'] - d['chiral_twist']                  # gamma Re(-ie psi*.(A x psi)), A_par + A_perp
        d['A_par_mean'] = float(a.mean()); d['A_perp_rms'] = float(np.sqrt(np.mean((c**2).sum(0))))
        rho = np.abs(psi)**2; rt = rho.sum(0)
        S = np.real(1j*cross(psi, np.conj(psi))); Sn = np.linalg.norm(S, axis=0)
        d['S_over_rho_mean'] = float(np.mean(Sn/rt)); d['S_mean'] = float(np.mean(Sn))
        d['S_over_rho_max'] = float(np.max(Sn/rt))
        # director: top eigenvector of Re(psi psi^dagger)
        Q = np.real(np.einsum('is,js->sij', psi, np.conj(psi)))
        w, V = np.linalg.eigh(Q); u = V[:, :, -1]            # (M, 3)
        for i in range(1, self.M):
            if np.dot(u[i], u[i-1]) < 0: u[i] = -u[i]
        cosang = np.abs(u @ self.n); ang = np.degrees(np.arccos(np.clip(cosang, 0, 1)))
        d['cone_deg_mean'] = float(ang.mean()); d['cone_deg_min'] = float(ang.min()); d['cone_deg_max'] = float(ang.max())
        un = np.roll(u, -1, axis=0); un[-1] *= np.sign(np.dot(un[-1], u[-1])) or 1
        turn = np.sum(np.arcsin(np.clip(np.cross(u, un) @ self.n, -1, 1)))
        d['director_turn_deg'] = float(np.degrees(turn))      # > 0: right-handed about n
        d['biaxial_ratio_mean'] = float(np.mean(w[:, -2]/w[:, -1]))
        dk = rho.mean(1); d['rho_k_mean'] = dk.tolist()
        d['amp_spread'] = float((dk.max()-dk.min())/dk.mean())
        d['amp_min'] = np.sqrt(rho.min(1)).tolist()
        dph = np.angle(np.roll(psi, -1, axis=1)*np.conj(psi))
        d['winding_k'] = (dph.sum(1)/(2*np.pi)).tolist()
        rel = np.angle(psi[0]*np.conj(psi[1])); drel = np.angle(np.exp(1j*(np.roll(rel, -1)-rel)))
        d['winding_rel12'] = float(drel.sum()/(2*np.pi))
        d['handedness'] = 'R' if d['chiral'] < -1e-12 else ('L' if d['chiral'] > 1e-12 else '0')
        return d


# =====================================================================================
def _solve_task(args):
    n, eta, gamma, P, Afree, kind = args
    ch = Chain(n, eta, gamma, P, Afree)
    r, dt = ch.solve(ch.seed(kind))
    gain = r.fun/P - e_vac(eta)
    return dict(P=float(P), M=ch.M, seed=kind, gain=float(gain), success=bool(r.success),
                message=str(r.message), nit=int(r.nit), maxgrad=float(np.max(np.abs(r.jac))),
                time=dt, x=r.x)

def scan(pool, n, eta, gamma, Afree, Ps=P_GRID):
    tasks = [(n, eta, gamma, P, Afree, k) for P in Ps for k in ('R', 'L', 'noise')]
    res = pool.map(_solve_task, tasks, chunksize=1)
    return res

def best(res):
    return min(res, key=lambda r: r['gain'])

def strip(res):
    return [{k: v for k, v in r.items() if k != 'x'} for r in res]


def run_case(pool, nkey, eta, Afree, log, store):
    n = NHAT[nkey]; tag = f"{nkey}_eta{eta}_{'Afree' if Afree else 'A0'}"
    hist = {}
    def unstable(gamma):
        res = scan(pool, n, eta, gamma, Afree)
        b = best(res); hist[float(gamma)] = strip(res)
        nc = [r for r in res if not r['success']]
        log(f"  [{tag}] gamma={gamma:.6f} min gain={b['gain']:+.3e} at P={b['P']:.3f} seed={b['seed']} "
            f"non-converged={len(nc)}/{len(res)}")
        return b['gain'] < GAIN_TOL, res
    lo, hi, hires = 0.0, None, None
    for gm in GAMMA_BRACKET:
        u, res = unstable(gm)
        if u: hi, hires = gm, res; break
        lo = gm
    if hi is None:
        log(f"  [{tag}] gamma_c > 5"); store[tag] = dict(gamma_c=None, note='gamma_c > 5', history=hist); return store[tag]
    while hi - lo > BISECT_TOL:
        mid = 0.5*(lo+hi); u, res = unstable(mid)
        if u: hi, hires = mid, res
        else: lo = mid
    log(f"  [{tag}] gamma_c = {hi:.5f}  (bracket [{lo:.5f}, {hi:.5f}])")
    store[tag] = dict(gamma_c=hi, bracket=[lo, hi], history=hist)
    return store[tag]


def optimum(pool, nkey, eta, gamma, Afree):
    """Full P sweep at gamma; returns diagnostics of the lowest-energy state and the E/P curve."""
    n = NHAT[nkey]; res = scan(pool, n, eta, gamma, Afree)
    b = best(res); ch = Chain(n, eta, gamma, b['P'], Afree)
    d = ch.diagnostics(b['x'])
    d.update(P_star=b['P'], q_star=2*np.pi/b['P'], q_star_xi=2*np.pi/b['P']/np.sqrt(2), seed=b['seed'],
             success=b['success'], message=b['message'])
    curve = {}
    for r in res:
        k = f"{r['P']:.4f}"; curve[k] = min(curve.get(k, np.inf), r['gain'])
    d['gain_vs_P'] = curve
    d['solves'] = strip(res)
    return d


# =====================================================================================
# Checks
def checks(log):
    out = {}
    rng = np.random.default_rng(7)
    for nkey, n in NHAT.items():
        ch = Chain(n, 0.1, 0.8, P=3.0, Afree=True)
        M = ch.M
        psi = rng.normal(size=(3, M)) + 1j*rng.normal(size=(3, M)); a = rng.normal(size=M); c = rng.normal(size=(2, M))
        x = ch.pack(psi, a, c)
        # reality: complex central-difference form
        U = np.exp(-1j*ch.e*ch.h*a)
        fwd = np.conj(psi)*ch.ncross(U*np.roll(psi, -1, axis=1))
        bwd = np.conj(psi)*ch.ncross(np.roll(np.conj(U)[None, :]*psi, 1, axis=1))
        Ccplx = np.sum(fwd - bwd)/2 + ch.h*np.sum(-1j*ch.e*np.conj(psi)*cross(ch.Aperp(c), psi))
        Creal = ch.parts(x, gamma=1.0)['chiral']
        out[f'reality_{nkey}'] = dict(im_over_re=float(abs(Ccplx.imag)/abs(Ccplx.real)),
                                      cplx_vs_code=float(abs(Ccplx.real-Creal)/abs(Creal)))
        # gauge covariance: random lattice gauge function
        al = rng.uniform(-np.pi, np.pi, M)
        x2 = ch.pack(psi*np.exp(1j*al), a + (np.roll(al, -1)-al)/(ch.e*ch.h), c)
        p1, p2 = ch.parts(x), ch.parts(x2)
        out[f'gauge_{nkey}'] = dict(chiral_rel=float(abs(p1['chiral']-p2['chiral'])/abs(p1['chiral'])),
                                   total_rel=float(abs(p1['total']-p2['total'])/abs(p1['total'])))
        # mirror: s -> -s, A -> -A maps E_gamma to E_{-gamma}
        idx = (-np.arange(M)) % M
        x3 = ch.pack(psi[:, idx], -a[(-np.arange(M)-1) % M], -c[:, idx])
        Em = ch.parts(x3)['total']; Eneg = ch.parts(x, gamma=-ch.gamma)['total']
        out[f'mirror_{nkey}'] = float(abs(Em-Eneg)/abs(Eneg))
        # gradient check, 5-point stencil, A free and A frozen
        for Af in (True, False):
            c2 = Chain(n, 0.1, 0.8, P=3.0, Afree=Af)
            xv = c2.pack(psi, a, c) if Af else c2.pack(psi)
            E, g = c2.energy_grad(xv)
            ii = rng.choice(xv.size, 60, replace=False); worst = 0.0; eps = 1e-3
            for i in ii:
                f = []
                for k in (-2, -1, 1, 2):
                    xp = xv.copy(); xp[i] += k*eps; f.append(c2.energy_grad(xp)[0])
                fd = (f[0] - 8*f[1] + 8*f[2] - f[3])/(12*eps)
                worst = max(worst, abs(fd-g[i])/(abs(fd)+1e-8))
            out[f'gradcheck_{nkey}_{"Afree" if Af else "A0"}'] = worst
            # energy_grad total equals parts total
            out[f'Econsistency_{nkey}_{"Afree" if Af else "A0"}'] = float(abs(E - c2.parts(xv)['total'])/abs(E))
    # vacuum
    import gl3
    for eta in (0.1, 0.0):
        g3 = gl3.GL3(N=5, h=0.5, eta=eta)
        dens_gl3 = g3.vacuum_energy()/(g3.h**3*g3.nsite)
        ch = Chain(NHAT['z'], eta, 0.0, P=5.0, Afree=True)
        xv = ch.vacuum(); E, g = ch.energy_grad(xv)
        r, _ = ch.solve(ch.seed('noise'))
        out[f'vacuum_eta{eta}'] = dict(e_vac=e_vac(eta), gl3_density=dens_gl3, code_E_over_P=E/ch.P,
                                       grad_at_vac=float(np.max(np.abs(g))),
                                       from_noise_gain=float(r.fun/ch.P - e_vac(eta)), from_noise_success=bool(r.success),
                                       from_noise_nit=int(r.nit))
        # Hessian at vacuum non-negative (random directions, gamma = 0)
        mins = []
        rr = np.random.default_rng(3)
        for _ in range(20):
            v = rr.normal(size=xv.size); v /= np.linalg.norm(v); t = 1e-4
            mins.append((ch.energy_grad(xv+t*v)[0] + ch.energy_grad(xv-t*v)[0] - 2*E)/t**2)
        out[f'vacuum_eta{eta}']['min_curv_random_dirs'] = float(min(mins))
    for k, v in out.items(): log(f"  check {k}: {v}")
    return out


# =====================================================================================
# Linear stability of the vacuum, from the lattice functional itself (descriptive cross-check)
def lin_min_eig(n, eta, gamma, P, Afree, m):
    ch = Chain(n, eta, gamma, P, Afree); xv = ch.vacuum(); M = ch.M; s = np.arange(M)*ch.h
    q = 2*np.pi*m/P
    nfield = 9 if Afree else 6
    basis = []
    for f in range(nfield):
        for fn in ((np.cos, np.sin) if m > 0 else (np.cos,)):
            v = np.zeros(xv.size); v[f*M:(f+1)*M] = fn(q*s) if m > 0 else 1.0
            basis.append(v/np.linalg.norm(v))
    B = np.array(basis).T
    _, g0 = ch.energy_grad(xv); t = 1e-6
    HB = np.array([(ch.energy_grad(xv+t*B[:, i])[1] - ch.energy_grad(xv-t*B[:, i])[1])/(2*t) for i in range(B.shape[1])]).T
    Hs = B.T @ HB; Hs = 0.5*(Hs+Hs.T)
    return np.linalg.eigvalsh(Hs)[0]/ch.h

def lin_gamma(n, eta, Afree, Ps=P_GRID, mmax_q=12.0, tol=1e-4):
    """Smallest gamma at which some Fourier block (q = 2 pi m / P, q <= mmax_q) of the vacuum Hessian goes negative."""
    def unst(gm):
        for P in Ps:
            for m in range(0, int(mmax_q*P/(2*np.pi))+1):
                if lin_min_eig(n, eta, gm, P, Afree, m) < -1e-7: return True, P, m
        return False, None, None
    lo, hi = 0.0, 8.0
    if not unst(hi)[0]: return None
    while hi-lo > tol:
        mid = 0.5*(lo+hi)
        if unst(mid)[0]: hi = mid
        else: lo = mid
    _, P, m = unst(hi)
    return dict(gamma_lin=hi, P=float(P), m=m, q=2*np.pi*m/P)


# =====================================================================================
def _lin_task(args):
    nkey, eta, Af = args
    return (nkey, eta, Af, lin_gamma(NHAT[nkey], eta, Af, mmax_q=4.0, tol=1e-4))

def main():
    import multiprocessing as mp, platform, scipy
    os.environ.setdefault('OMP_NUM_THREADS', '1')
    logf = open('log_chiral1d.txt', 'w')
    def log(s):
        print(s, flush=True); logf.write(s+'\n'); logf.flush()
    R = dict(meta=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                       e=E_CH, kappa=2, h_target=H_TARGET, P_grid=P_GRID.tolist(), gamma_bracket=GAMMA_BRACKET,
                       gain_tol=GAIN_TOL, bisect_tol=BISECT_TOL, solver=SOLVER, nhat={k: v.tolist() for k, v in NHAT.items()},
                       seeds='R/L: vacuum + 0.05*(e1 cos qs +/- e2 sin qs), real; noise: vacuum + N(0, 0.05) on every free variable, default_rng(0)'))
    def save():
        with open('chiral1d_results.json', 'w') as f: json.dump(R, f, indent=1, default=float)
    t0 = time.time()
    log('== checks'); R['checks'] = checks(log); save()
    cases = [(nk, eta) for eta in (0.1, 0.0) for nk in ('z', 'diag', 'perp')]
    with mp.Pool(4) as pool:
        log('== linear stability of the vacuum (descriptive cross-check)')
        R['linear'] = {}
        for nk, eta, Af, res in pool.map(_lin_task, [(nk, eta, Af) for nk, eta in cases for Af in (True, False)]):
            tag = f"{nk}_eta{eta}_{'Afree' if Af else 'A0'}"; R['linear'][tag] = res; log(f"  lin {tag}: {res}")
        save()
        R['gamma_c'] = {}
        for Af in (True, False):
            log(f"== gamma_c, {'A free (Calculation 1)' if Af else 'A = 0 (Calculation 2a)'}")
            for nk, eta in cases:
                run_case(pool, nk, eta, Af, log, R['gamma_c']); save()
                log(f"     elapsed {time.time()-t0:.0f} s")
        # diagnostics at 1.1 gamma_c, mirror checks
        R['optimum'] = {}; R['mirror'] = {}
        for Af in (True, False):
            for nk, eta in cases:
                tag = f"{nk}_eta{eta}_{'Afree' if Af else 'A0'}"; gc = R['gamma_c'][tag]
                if gc['gamma_c'] is None: continue
                g11 = 1.1*gc['gamma_c']
                log(f"== optimum {tag} at 1.1 gamma_c = {g11:.5f}")
                d = optimum(pool, nk, eta, g11, Af); R['optimum'][tag] = d
                log(f"  P*={d['P_star']:.3f} q*={d['q_star']:.4f} gain={d['gain']:+.3e} hand={d['handedness']} seed={d['seed']} "
                    f"|S|/rho={d['S_over_rho_mean']:.4f} cone={d['cone_deg_mean']:.2f} turn={d['director_turn_deg']:.1f} spread={d['amp_spread']:.4f}")
                if eta == 0.0 and gc['bracket'][0] == 0.0:
                    log(f"== optimum {tag} at gamma = 0.01 (smallest bracket value)")
                    d2 = optimum(pool, nk, eta, 0.01, Af); R['optimum'][tag+'_g0.01'] = d2
                    log(f"  P*={d2['P_star']:.3f} gain={d2['gain']:+.3e} hand={d2['handedness']} |S|/rho={d2['S_over_rho_mean']:.4f}")
                # mirror: gamma -> -gamma
                lo, hi = gc['bracket']; mres = {}
                for gm in ([-lo] if lo > 0 else []) + [-hi]:
                    res = scan(pool, NHAT[nk], eta, gm, Af); b = best(res)
                    mres[f'{gm:.6f}'] = dict(min_gain=b['gain'], unstable=b['gain'] < GAIN_TOL, P=b['P'], seed=b['seed'])
                dm = optimum(pool, nk, eta, -g11, Af)
                mres['at_-1.1gc'] = {k: dm[k] for k in ('gain', 'P_star', 'handedness', 'chiral', 'director_turn_deg', 'S_over_rho_mean', 'seed')}
                R['mirror'][tag] = mres
                log(f"  mirror {tag}: {json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()}) for k, v in mres.items()}, default=float)}")
                save()
        # Calculation 2b
        R['calc2b'] = {}
        for nk, eta in cases:
            gc = R['gamma_c'][f"{nk}_eta{eta}_Afree"]['gamma_c']
            if gc is None: continue
            for fac in (0.5, 1.5):
                for Af in (True, False):
                    tag = f"{nk}_eta{eta}_{fac}gc_{'Afree' if Af else 'A0'}"
                    d = optimum(pool, nk, eta, fac*gc, Af); d.pop('solves')
                    R['calc2b'][tag] = d
                    log(f"== 2b {tag}: gamma={fac*gc:.5f} gain={d['gain']:+.3e} P*={d['P_star']:.3f} chiral={d['chiral']:+.3e} "
                        f"AS={d['chiral_AS']:+.3e} AperpS={d['chiral_AperpS']:+.3e} |S|={d['S_mean']:.4f} mag={d['magnetic']:.3e}")
            save()
    # Calculation 2c (P5)
    R['calc2c'] = {}
    for eta in (0.1, 0.0):
        gc = R['gamma_c'][f"z_eta{eta}_Afree"]['gamma_c']
        for Af in (True, False):
            ch = Chain(NHAT['z'], eta, gc, 20.0, Af); x0 = ch.winding_seed()
            d0 = ch.diagnostics(x0)
            r, dt = ch.solve(x0); d1 = ch.diagnostics(r.x)
            tag = f"eta{eta}_{'Afree' if Af else 'A0'}"
            R['calc2c'][tag] = dict(gamma=gc, unrelaxed=d0, relaxed=d1, success=bool(r.success), message=str(r.message), nit=int(r.nit),
                                    chiral_over_grad=d1['chiral']/d1['gradient'])
            log(f"== P5 {tag}: gamma={gc:.5f} unrelaxed chiral={d0['chiral']:+.3e} (grad {d0['gradient']:.4e}); relaxed chiral={d1['chiral']:+.3e} "
                f"grad={d1['gradient']:.4e} ratio={d1['chiral']/d1['gradient']:+.3e} wind_k={np.round(d1['winding_k'],3).tolist()} "
                f"rel12={d1['winding_rel12']:+.3f} amp_min={np.round(d1['amp_min'],4).tolist()} gain={d1['gain']:+.3e} {r.message}")
    save(); log(f"done, {time.time()-t0:.0f} s")

if __name__ == '__main__':
    main()
