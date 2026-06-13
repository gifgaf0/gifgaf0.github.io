"""
phase1_object.py — GZ1 Phase 1 (REBUILD): big-box quench, p6m object reproduction
Targets (report §1): psi6 ≈ 0.834 (±0.02 acceptable), psi4 small, density
contrast ≈ 1.6, n_peaks ≈ 234; measure k_c. Canonical run: N=160, L=20, full
quench, seed 7 (mv_g1_minimiser.py defaults, cited by the pre-registration:
dtau=2e-3, steps=4000, 1% noise seed, renorm each step).
Runs the quench with BOTH the continuum Bessel kernel (the binding GZ1 model)
and the V4.26 grid-FFT disk kernel (canonical-object replication cross-check);
both logged, headline = the disk-FFT canonical replication. -> phase1.json
"""
import json
import numpy as np
import gz1_core as core

N, L, SEED, DTAU, STEPS = 160, 20.0, 7, 2e-3, 4000


def quench(kernel):
    X, Y, KX, KY, K2, dx, dy = core.rect_grids(N, N, L, L)
    if kernel == "disk_fft":
        Uk = core.U_disk_fft(N, L)
    else:
        Uk = core.U_tilde(np.sqrt(K2))
    rng = np.random.default_rng(SEED)
    psi = np.sqrt(core.RHO0) * (1.0 + 0.01 * rng.standard_normal((N, N)))
    psi = psi.astype(complex)
    norm_target = core.RHO0 * N * N

    def renorm(p):
        return p * np.sqrt(norm_target / np.sum(np.abs(p) ** 2))

    psi = renorm(psi)
    Kprop = np.exp(-0.25 * K2 * DTAU)
    for it in range(STEPS):
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))
        rho = np.abs(psi) ** 2
        Uc = np.fft.ifft2(Uk * np.fft.fft2(rho)).real
        psi = psi * np.exp(-Uc * DTAU)
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))
        psi = renorm(psi)
    rho = np.abs(psi) ** 2
    bo = core.bond_orientational(rho, dx, L)
    contrast = float((rho - rho.mean()).std() / rho.mean())
    kc = core.structure_kc(rho, KX, KY)
    a_kc = 4 * np.pi / (np.sqrt(3) * kc)
    return dict(psi6=round(bo["psi6_local"], 4), psi4=round(bo["psi4_local"], 4),
                n_peaks=bo["n_peaks"], contrast=round(contrast, 4),
                kc=round(kc, 4), a_from_kc=round(float(a_kc), 4))


def main():
    out = {"params": dict(N=N, L=L, seed=SEED, dtau=DTAU, steps=STEPS,
                          g=core.G_COUPLING, R=core.R_CORE, rho0=core.RHO0)}
    out["disk_fft_kernel"] = quench("disk_fft")     # V4.26 canonical replication
    out["bessel_kernel"] = quench("bessel")         # binding GZ1 continuum kernel
    hl = out["disk_fft_kernel"]
    p6m = hl["psi6"] > 0.60 and hl["psi6"] > hl["psi4"] + 0.15
    out["p6m_confirmed"] = bool(p6m)
    with open("phase1.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    print("p6m:", "CONFIRMED" if p6m else "NOT CONFIRMED")


if __name__ == "__main__":
    main()
