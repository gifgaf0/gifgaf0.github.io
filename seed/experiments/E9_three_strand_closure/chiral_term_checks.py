"""Checks for the chiral (Lifshitz) term note. Periodic N^3 grid, spectral derivatives.
E_c = int psi* . (D x psi),  D = grad - i e A.  psi is a complex 3-vector (strand index locked to space)."""
import numpy as np, itertools
rng = np.random.default_rng(1); N = 32; L = 2*np.pi; e = 0.7
k = np.fft.fftfreq(N, d=L/N)*2*np.pi; KX = np.meshgrid(k, k, k, indexing='ij')
def smooth(z):  # band-limit a random field
    f = np.fft.fftn(z); f[(np.abs(KX[0])>3)|(np.abs(KX[1])>3)|(np.abs(KX[2])>3)] = 0; return np.fft.ifftn(f)
def d(f, j): return np.fft.ifftn(1j*KX[j]*np.fft.fftn(f))
psi = np.array([smooth(rng.normal(size=(N,)*3)+1j*rng.normal(size=(N,)*3)) for _ in range(3)])
A = np.array([smooth(rng.normal(size=(N,)*3)).real for _ in range(3)])
eps = np.zeros((3,3,3))
for i,j,l in itertools.permutations(range(3)): eps[i,j,l] = np.linalg.det(np.eye(3)[[i,j,l]])
def Ec(p, A):
    D = lambda j, f: d(f, j) - 1j*e*A[j]*f
    return sum(eps[i,j,l]*np.sum(np.conj(p[i])*D(j, p[l])) for i in range(3) for j in range(3) for l in range(3))*(L/N)**3
E0 = Ec(psi, A); print('E_c =', E0, ' |Im|/|Re| =', abs(E0.imag)/abs(E0.real))
G = np.meshgrid(*(3*[np.arange(N)*L/N]), indexing="ij"); al = 0.5*np.sin(G[0]) + 0.3*np.cos(G[2])   # smooth gauge transformation (a random one aliases on the grid)
E1 = Ec(psi*np.exp(1j*al), A + np.array([d(al, j).real for j in range(3)])/e)
print('gauge invariance  rel diff =', abs(E1-E0)/abs(E0))
# parity: x -> -x on the grid, psi -> -psi (vector), A -> -A (vector)
flip = lambda f: np.roll(f[::-1, ::-1, ::-1], 1, axis=(0, 1, 2))
Ep = Ec(np.array([-flip(f) for f in psi]), np.array([-flip(a) for a in A]))
print('parity: E_c(P psi)/E_c(psi) =', (Ep/E0).real)
# locked rotation by a signed permutation R (det +1): rotate space and index together
def rotate(field, R, vec=True):
    # R maps axis a -> axis b with sign; apply to coordinates via transposes/flips (exact on the grid)
    perm = [int(np.nonzero(R[:, a])[0][0]) for a in range(3)]
    out = []
    for comp in range(3):
        f = field[comp]
        g = np.transpose(f, np.argsort(perm))
        for b in range(3):
            if R[b, np.nonzero(R[b])[0][0]] < 0: g = flip_axis(g, b)   # negative entry in row b: reflect axis b
        out.append(g)
    out = np.array(out)
    return np.einsum('ab,b...->a...', R, out) if vec else out
def flip_axis(f, ax): return np.roll(np.flip(f, ax), 1, axis=ax)
def V(p, eta=0.1):
    pot = 0.5*np.sum((np.abs(p)**2-1)**2)
    jos = -eta*sum(np.sum((p[i]*np.conj(p[j])).real) for i in range(3) for j in range(i+1, 3))
    return pot, jos
mats = []
for P in itertools.permutations(range(3)):
    for s in itertools.product([1, -1], repeat=3):
        R = np.zeros((3, 3)); 
        for a in range(3): R[P[a], a] = s[a]
        if round(np.linalg.det(R)) == 1: mats.append(R)
pot0, jos0 = V(psi)
keep = []
for R in mats:
    pr = rotate(psi, R); Ar = rotate(A.astype(complex), R).real
    pot, jos = V(pr); ec = Ec(pr, Ar)
    ok = abs(pot-pot0) < 1e-8*abs(pot0) and abs(jos-jos0) < 1e-8*abs(jos0)
    keep.append(ok)
    print(R.astype(int).tolist(), 'E_c inv:', abs(ec-E0)/abs(E0) < 1e-9, ' pot inv:', abs(pot-pot0) < 1e-8*abs(pot0), ' Josephson inv:', abs(jos-jos0) < 1e-8*abs(jos0))
print('locked proper rotations (of the 24 cube rotations) preserving potential + Josephson:', sum(keep))
# real-director reduction: psi = f e^{i theta} u  ->  psi*.curl psi = f^2 u.curl u
z = np.arange(N)*L/N; Z = np.meshgrid(z, z, z, indexing='ij')[2]; q = 2
u = np.array([np.cos(q*Z), np.sin(q*Z), 0*Z]); th = smooth(rng.normal(size=(N,)*3)).real
p = u*np.exp(1j*th)
dens = sum(eps[i,j,l]*np.conj(p[i])*d(p[l], j) for i in range(3) for j in range(3) for l in range(3))
print('helix u.curl u: mean psi*.curl psi =', dens.mean().real, ' expected -q =', -q)
