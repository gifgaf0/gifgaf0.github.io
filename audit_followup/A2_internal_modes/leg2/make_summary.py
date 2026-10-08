"""Assemble A2_LEG2_RESULTS.json (all integer counts, Watanabe-Murayama numbers, homotopy answers and the
key numbers behind tasks 5 and 6) from the per-task result files."""
import json

t1 = json.load(open("task1_results.json"))
t3 = json.load(open("task3_results.json"))
t4 = json.load(open("task4_results.json"))
t5 = json.load(open("task5_results.json"))
t6 = json.load(open("task6_results.json"))

counts = {}
for n in (14, 16):
    for g in ("a", "b", "c"):
        for d in (2, 4, 6):
            k = f"R{n}_{g}_d{d}"
            counts[k] = dict(all=t1["counts"][k]["all"], T_even=t1["counts"][k]["T_even"])

res = {
    "prereg_md5_verified": "fd2e95973de02d9a0e6d719cb579ccc0",
    "groups": {"a": "G2 x U(1)_global", "b": "G2 x U(1)_psi0", "c": "G2 x U(1)_psi0 x Z3"},
    "task1_invariant_counts": counts,
    "task1_methods_agree": dict(A_vs_B_all_degrees=t1["agree_AB"], A_vs_C_degrees_2_4=t1["agree_AC_deg2_4"],
                                bigraded_A_vs_B=t1["agree_bigraded"]),
    "task1_bigraded_G2_invariants_I(p,q)": t1["methodB_bigraded"],
    "task1_T_trace_on_I(p,p)": t1["methodB_Ttrace"],
    "task1_controls": dict(molien=t1["methodB_controls"], g2=t1["setup"]["g2_checks"],
                           transitivity=t1["setup"]["transitivity"], weyl_group_order=t1["setup"]["cartan"]["weyl_group_order"]),
    "task2_basis_group_c_T_even_R14": {
        "deg2": ["N"], "deg4": ["N^2", "|S|^2"], "deg6": ["N^3", "N|S|^2", "Re(S^3)"],
        "on_polar_orbit_psi7=e^{i theta} n": {"N": 1, "N^2": 1, "|S|^2": 1, "N^3": 1, "N|S|^2": 1, "Re(S^3)": "cos(6 theta)"},
        "theta_dependent": ["Re(S^3)"],
        "machine_kernel_theta_dependent_directions": t1["task2"]["machine_kernel"]["n_theta_dependent_directions"],
        "T_odd_companion": "Im(S^3) (sin 6 theta)"},
    "task3_homotopy": {
        "P7_case_i": dict(V="(S^1 x S^6)/Z2", pi0="0 (connected)", pi1="Z", generator="half-quantum (theta -> theta+pi, n -> -n)"),
        "P7_case_ii": dict(V="3 disjoint copies of S^6", pi0="Z3 (3 components)", pi1="0",
                           half_quantum_protected=False,
                           note="half-quantum = end of 3 domain walls (Delta theta = pi/3 each); 2pi vortex = end of 6"),
        "mixed_c_case_i": dict(V="S^1_theta0 x (S^1 x S^6)/Z2", pi1="Z + Z", generators="psi0 2pi winding; 7-sector half-quantum"),
        "mixed_c_case_ii": dict(V="S^1_theta0 x (3 copies of S^6)", pi0="Z3", pi1="Z", generator="psi0 2pi winding only"),
        "mixed_alt_with_(a)_locking_term_Re(psi0^2 Sbar)_(forbidden_under_c)": dict(V="S^1 x S^6", pi1="Z (common 2pi winding)"),
        "numerics": {k: v for k, v in t3.items()},
    },
    "task4_watanabe_murayama": t4["requested"],
    "task4_bogoliubov_check": {k: {kk: vv for kk, vv in v.items() if kk in ("linear", "quadratic", "gapped", "gaps", "linear_speeds")}
                               for k, v in t4["bogoliubov_check"].items()},
    "task4_supplementary_G2xU1psi0": t4["supplementary_G2xU1psi0"],
    "task5": dict(rho_linear=t5["symbolic"]["rho_linear"], rho_linear_contains_chi=t5["symbolic"]["rho_linear_contains_chi"],
                  j_linear_contains_chi=t5["symbolic"]["j_linear_contains_chi"],
                  periodic_background_hessian=t5["periodic_background_hessian"],
                  density_vertex_Nperp_relative_change=t5["gp_dynamics"]["density_vertex_Nperp_rel_change"],
                  linear_mixing_vertex_dPperp_dt_over_golden_rule=t5["gp_dynamics"]["mixing_vertex"]["ratio"]),
    "task6": dict(drag_2D="F = m^2 |s(0)|^2 v  (prop. v)", drag_3D="F = m^3 |s(0)|^2 v^2 / pi  (prop. v^2)",
                  fitted_exponents=dict(d2=t6["c_golden_rule_drag"]["fitted_exponent_2D"], d3=t6["c_golden_rule_drag"]["fitted_exponent_3D"]),
                  sim_1D_source_ratio_to_golden_rule={k: v["ratio"] for k, v in t6["a_c_1D_moving_source_simulation"]["results"].items()},
                  uniform_bound_state_final_overlap={k: v["final_overlap"] for k, v in t6["b_uniform_background_bound_state"]["results"].items()},
                  crystal_bound_state={k: dict(Gv=v["Gv"], decay=v["fitted_decay_rate"], fgr=v["fgr_rate"]) for k, v in t6["d_crystal_bound_state"]["results"].items()},
                  answers={"a": "must radiate for every v > 0 (resonance sphere |k - m v| = m v through k = 0); no threshold",
                           "b": "no radiation in a uniform background at any v (Galilean covariance)",
                           "c": "F prop. v (2D), v^2 (3D); generally v^(d-1)",
                           "d": "emits iff hbar G.v >= E_b for a reciprocal vector G with nonzero U*rho0 Fourier weight; leading v_c = E_b/(hbar |G_min|)"}),
}
json.dump(res, open("A2_LEG2_RESULTS.json", "w"), indent=1, default=str)
print(json.dumps({k: res[k] for k in ("task1_invariant_counts", "task1_methods_agree", "task4_watanabe_murayama")}, indent=1))
