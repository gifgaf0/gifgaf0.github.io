"""Sanity test: my LNR Dirac/Majorana forms span exactly the F21-invariant couplings (Reynolds projector)."""
import numpy as np, sys
sys.path.insert(0, '.')
import cc_texture as T
F21 = np.load('out/F21_elements.npy')
# invariant tensors T_{ijkl} in 3 x 3 x 3b x 3b ; M_ij = T_ijkl u_k u'_l
P = sum(np.kron(np.kron(np.kron(g, g), g.conj()), g.conj()) for g in F21) / 21
# P acts on vectors; invariants = range of P^T? invariant vectors v with (g x g x gb x gb) v = v
u, s, vh = np.linalg.svd(P); k = (s > 1e-9).sum(); inv = u[:, :k]
print("number of invariants:", k)
rng = np.random.default_rng(0)
ok = True
for trial in range(5):
    uu = rng.normal(size=3) + 1j * rng.normal(size=3); vv = rng.normal(size=3) + 1j * rng.normal(size=3)
    # couplings psi_i psi'_j xi_k xi'_l with xi in 3b: the familon vev enters as its components; M_ij = sum T_ijkl u_k v_l
    Ms = [np.einsum('ijkl,k,l->ij', inv[:, a].reshape(3, 3, 3, 3), uu, vv) for a in range(k)]
    Mine = [T.dirac(uu, vv, e) for e in np.eye(5)]
    A = np.array([m.ravel() for m in Ms]); B = np.array([m.ravel() for m in Mine])
    r = np.linalg.matrix_rank(np.vstack([A, B]), tol=1e-9)
    ok &= (r == 5 and np.linalg.matrix_rank(B, tol=1e-9) == 5)
print("Dirac(u,u';c0..c4) spans the 5 invariant couplings at 5 random vevs:", ok)
# Majorana: symmetric psi=psi', xi=xi'
Ps = sum(np.kron(np.kron(np.kron(g, g), g.conj()), g.conj()) for g in F21) / 21
okm = True
for trial in range(5):
    uu = rng.normal(size=3) + 1j * rng.normal(size=3)
    Ms = [np.einsum('ijkl,k,l->ij', inv[:, a].reshape(3, 3, 3, 3), uu, uu) for a in range(k)]
    Ms = [(m + m.T) / 2 for m in Ms]
    A = np.array([m.ravel() for m in Ms])
    B = np.array([T.maj(uu, 0).ravel(), (T.maj(uu, 1) - T.maj(uu, 0)).ravel()])
    okm &= np.linalg.matrix_rank(A, tol=1e-9) == 2 and np.linalg.matrix_rank(np.vstack([A, B]), tol=1e-9) == 2
print("Maj(u; alpha) spans the symmetric invariants (2):", okm)
