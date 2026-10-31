import numpy as np, sys
sys.path.insert(0, '.')
from gl3 import GL3
from starts import start_fields
from linking import analyse
xi, h = 1/np.sqrt(2), 0.5
def check_grad_e(e, eta, N=6, seed=0):   # gl3.check_grad body, with e passed to GL3
    g = GL3(N=N, h=0.5, e=e, eta=eta)
    rng = np.random.default_rng(seed)
    v = rng.normal(size=9 * g.nsite) * 0.5
    E, grad = g.energy_grad(v)
    idx = rng.choice(v.size, 40, replace=False); eps = 1e-6; worst = 0.0
    for i in idx:
        vp = v.copy(); vp[i] += eps; vm = v.copy(); vm[i] -= eps
        fd = (g.energy_grad(vp)[0] - g.energy_grad(vm)[0]) / (2 * eps)
        worst = max(worst, abs(fd - grad[i]) / (abs(fd) + 1e-8))
    return worst
cells = [(1, 0.1), (2, 0.0), (1, 0.0)]
for kap, eta in cells:
    e = 1/(kap*np.sqrt(3)); lam = 1/(e*np.sqrt(6))
    print(f'cell kappa={kap} eta={eta}: e={e!r} lambda={lam:.6f} xi={xi:.6f} lambda/xi={lam/xi:.6f}')
    print('  gradient check, worst relative error:', check_grad_e(e, eta))
    g = GL3(N=65, h=0.5, e=e, eta=eta)
    vac = g.vacuum_energy()
    # direct energy of the uniform vacuum: equal phases, |psi|^2 = 1 + eta, A = 0
    psi = np.full((3, 65, 65, 65), np.sqrt(1 + eta), complex); A = np.zeros((3, 65, 65, 65))
    Edir = g.energy_grad(g.pack(psi, A))[0]
    print(f'  vacuum_energy()={vac!r}  direct E(uniform |psi|^2=1+eta)={Edir!r}  diff={Edir-vac:.3e}')
    if eta == 0:
        # any other rho is higher: check rho=1 is the minimum of the potential per site
        for r in (0.9, 1.0, 1.1):
            psi = np.full((3, 65, 65, 65), np.sqrt(r), complex)
            print(f'    E(uniform rho={r}) - vacuum_energy() = {g.energy_grad(g.pack(psi, A))[0]-vac:.4e}')
        # at eta=0 relative phases are free: uniform state with phases (0, 2pi/3, 4pi/3) has same energy
        psi = np.stack([np.ones((65,)*3)*np.exp(1j*a) for a in (0, 2*np.pi/3, 4*np.pi/3)])
        print(f'    E(rho=1, phases 0,120,240 deg) - vacuum_energy() = {g.energy_grad(g.pack(psi, A))[0]-vac:.4e}')
    print('  start check:', [analyse(start_fields(g, s, 6.0)) for s in 'AB'])
# the README's own check (default GL3), for comparison
g = GL3(N=65); print('README check (default GL3(N=65)):', [analyse(start_fields(g, s, 6.0)) for s in 'AB'])
