#!/usr/bin/env python3
"""E2 figures (small PNGs) from profile.json and out/*.json. Runtime ~3 s."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"     # categorical slots 1-3 (reference palette, light)
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                     "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.6,
                     "legend.frameon": False})


def fig_profile():
    pr = json.load(open(os.path.join(HERE, "profile.json")))
    x = np.array(pr["x"]); F = np.array(pr["F"]); Fp = np.array(pr["dFdx"]); C = pr["C"]
    m = x <= 12
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.8))
    ax[0].plot(x[m], F[m], color=S1, label="F(x), solved")
    xa = x[(x >= 2) & m]
    ax[0].plot(xa, C / xa ** 2, color=S2, ls="--", lw=1.2, label=f"C/x², C = {C:.3f}")
    ax[0].set_xlabel("x = e F_π r"); ax[0].set_ylabel("F (rad)"); ax[0].set_ylim(0, 3.3)
    ax[0].set_title("hedgehog profile, F(0) = π", color=INK, fontsize=9)
    ax[0].legend(loc="upper right")
    xs = x[(x > 0) & m]; Fs = F[(x > 0) & m]; Fps = Fp[(x > 0) & m]
    q = np.sin(Fs) ** 2 / xs ** 2
    e2 = 0.125 * (Fps ** 2 + 2 * q); e4 = 0.5 * q * (q + 2 * Fps ** 2); p = (e4 - e2) / 3
    w = 4 * np.pi * xs ** 2
    ax[1].plot(xs, w * e2, color=S1, label="4πx² ε₂ (stretching)")
    ax[1].plot(xs, w * e4, color=S2, label="4πx² ε₄ (Skyrme)")
    ax[1].plot(xs, w * p, color=S3, label="4πx² p (pressure)")
    ax[1].axhline(0, color=INK2, lw=0.6)
    ax[1].set_xlabel("x = e F_π r"); ax[1].set_ylabel("density per unit x (F_π/e units)")
    ax[1].set_title("E₂ = E₄; ∫ p d³x = 0", color=INK, fontsize=9)
    ax[1].legend(loc="upper right"); ax[1].set_xlim(0, 8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_profile.png"), dpi=120)
    plt.close(fig)


def fig_derrick():
    d = json.load(open(os.path.join(OUT, "derrick.json")))
    mu = np.array(d["scaling_curve"]["mu"]); E2 = np.array(d["scaling_curve"]["E2"]); E4 = np.array(d["scaling_curve"]["E4"])
    M = d["E2"] + d["E4"]
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    ax.plot(mu, (E2 + E4) / M, color=S1, label="E(μ) = E₂/μ + μE₄ (Skyrme model; min at μ = 1)")
    ax.plot(mu, E2 / M, color=S2, label="E₂(μ) only (no Skyrme term)")
    ax.plot(mu, E4 / M, color=S3, lw=1.2, ls="--", label="E₄(μ)")
    ax.plot([1], [1], "o", ms=5, color=S1, mec=SURF, mew=1.5)
    ax.axvline(1.0, color=INK2, lw=0.6, ls=":")
    ax.set_xscale("log")
    ax.set_xticks([0.2, 0.5, 1, 2, 5]); ax.set_xticklabels(["0.2", "0.5", "1", "2", "5"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("dilation μ  (F(x) → F(μx); μ > 1 shrinks the fold)")
    ax.set_ylabel("energy / M_cl"); ax.set_ylim(0, 2.6)
    ax.set_title("Derrick: no minimum without the Skyrme term", color=INK, fontsize=9)
    ax.legend(loc="upper center", fontsize=7.5)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_derrick.png"), dpi=120)
    plt.close(fig)


def fig_spectrum():
    r = json.load(open(os.path.join(OUT, "rotor.json")))
    sets = [("ANW_SU2_fit", "ANW fit to N, Δ\n(F_π = %.0f MeV, e = %.2f)"),
            ("SU3_refit_PDG_centres", "SU(3) fit to 8, 10 centres\n(F_π = %.0f MeV, e = %.2f)")]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    want = [("8", "1/2"), ("10", "3/2"), ("10bar", "1/2"), ("27", "3/2"), ("35", "5/2"), ("27", "1/2")]
    lab = {"8": "8", "10": "10", "10bar": "10bar", "27": "27", "35": "35"}
    for k, (key, title) in enumerate(sets):
        ps = r["parameter_sets"][key]
        lev = {(s["irrep"], s["J"]): s["E_MeV"] for s in r["spectra"][key]}
        x0 = 2.2 * k
        placed = []
        for (ir, J) in sorted(want, key=lambda w: lev[w]):
            E = lev[(ir, J)]
            col = S1 if ir in ("8", "10") else S2
            ax.plot([x0, x0 + 1.0], [E, E], color=col, lw=2)
            yt = E
            if placed and yt - placed[-1] < 95:
                yt = placed[-1] + 95
            placed.append(yt)
            ax.text(x0 + 1.05, yt, f"{lab[ir]} (J={J}) {E:.0f}", va="center", fontsize=7.2, color=INK)
        if key == "ANW_SU2_fit":
            for E, nm in [(ps["E_N_SU2"], "N"), (ps["E_Delta_SU2"], "Δ")]:
                ax.plot([x0 - 0.6, x0 - 0.1], [E, E], color=S3, lw=2)
                ax.text(x0 - 0.62, E, f"SU(2) {nm} {E:.0f}", va="center", ha="right", fontsize=7.2, color=INK)
        ax.text(x0 + 0.5, 3280, title % (ps["F_pi"], ps["e"]), ha="center", va="top", fontsize=7.5, color=INK2)
    c8, c10 = r["pdg"]["octet_centre_MeV"], r["pdg"]["decuplet_centre_MeV"]
    for i, E in enumerate([c8, c10]):
        ax.axhline(E, color=INK2, lw=0.7, ls=":", label=f"PDG 2026 octet and decuplet centres ({c8:.0f}, {c10:.0f} MeV)" if i == 0 else None)
    ax.plot([], [], color=S1, lw=2, label="octet, decuplet")
    ax.plot([], [], color=S2, lw=2, label="exotic (10bar, 27, 35)")
    ax.plot([], [], color=S3, lw=2, label="SU(2) rotor N, Δ (fit input)")
    ax.legend(loc="upper left", fontsize=7, bbox_to_anchor=(0.0, 0.84))
    ax.set_xlim(-1.9, 4.9); ax.set_ylim(800, 3300)
    ax.set_xticks([]); ax.set_ylabel("energy (MeV)")
    ax.set_title("SU(3) rigid rotor, Y_R = 1: lowest allowed multiplets (J)", color=INK, fontsize=9)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_spectrum.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    fig_profile(); fig_derrick(); fig_spectrum()
    for f in ["fig_profile.png", "fig_derrick.png", "fig_spectrum.png"]:
        print(f, os.path.getsize(os.path.join(HERE, f)) // 1024, "KB")
