"""G-TSH4 INTERNAL-CONSISTENCY audit (NOT the independent E6 leg — see blockers).
Verifies the chat leg's derived quantities are internally consistent with its own raw JSON:
elastic->speed, Zener, A_3D, hex F-ISO identity, Route-D static/dynamical cross-check, mapper logic.
This checks arithmetic/logic only; it does NOT independently adjudicate the split-step bias or the
physics (that needs the blind from-scratch leg with the locked instrument).
"""
import json, numpy as np
R=json.load(open("/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/d4066cdd-gtsh4_phase12_results.json"))
V=json.load(open("/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/e4a5a122-gtsh4_qc_verdict.json"))
P=[];F=[]
def ok(c,m):(P if c else F).append(m)

# --- controls ---
ctl=R["controls"]["christoffel"]
ok(ctl["spring_cauchy_C12_minus_C44"]==0.0 and ctl["spring_C11_over_C44"]==2.0,
   f"C-POS central-force cubic: Cauchy C12=C44 (resid {ctl['spring_cauchy_C12_minus_C44']}), C11/C44=2 — closed-form")
ok(ctl["hex_closed_form_maxerr"]<1e-14 and ctl["cubic_closed_form_err"]<1e-14,
   f"C-POS Christoffel hex/cubic closed forms machine-exact ({ctl['hex_closed_form_maxerr']:.1e}/{ctl['cubic_closed_form_err']:.1e})")
ok(R["controls"]["uniform_bdg"]["err"]<1e-9, f"C-NEG uniform Bogoliubov err {R['controls']['uniform_bdg']['err']:.1e} <1e-9")

# --- elastic -> shear speed consistency (verdict C_ij vs Route-D static refs) ---
hs=V["classes"]["hex:step"]; rd=V["route_D_crosscheck"]
ok(abs(np.sqrt(hs["C44_over_rho"])-rd["static_sqrtC44"])<1e-3,
   f"hex:step √C44={np.sqrt(hs['C44_over_rho']):.4f} == Route-D static_sqrtC44={rd['static_sqrtC44']:.4f}")
ok(abs(np.sqrt(hs["C66_over_rho"])-rd["static_sqrtC66"])<1e-3,
   f"hex:step √C66={np.sqrt(hs['C66_over_rho']):.4f} == static_sqrtC66={rd['static_sqrtC66']:.4f}")

# --- hex F-ISO identity residual: C66 vs (C11-C12)/2 ---
for k in ("hex:step","hex:gem8"):
    c=V["classes"][k]; c66=c["C66_over_rho"]; ident=c["C11mC12_over_rho"]/2.0
    resid=abs(c66-ident)/c66*100
    ok(abs(resid-c["F_ISO_identity_residual_pct"])<0.05,
       f"{k}: F-ISO identity |C66-(C11-C12)/2|/C66={resid:.3f}% == reported {c['F_ISO_identity_residual_pct']:.3f}% (>2% FIRED)")
    ok(c["F_ISO"]=="FIRED" and "NOT VERDICT-ELIGIBLE" in c["verdict"], f"{k}: F-ISO fired -> NOT verdict-eligible (static hex blocked)")

# --- cubic Zener A = C44/C' and A_3D from transverse multiset ---
for k in ("cubic:step","cubic:gem8"):
    c=V["classes"][k]; zener=c["C44_over_rho"]/c["Cprime_over_rho"]
    ok(abs(zener-c["Zener_A"])<1e-3, f"{k}: Zener A=C44/C'={zener:.4f} == reported {c['Zener_A']:.4f}")
    ms=np.array(c["transverse_multiset"]); mean=ms.mean(); a3d=np.max(np.abs(ms-mean))/mean*100
    ok(abs(mean-c["v_mean"])<1e-3 and abs(a3d-c["A3D_pct"])<0.05,
       f"{k}: A_3D max-from-mean={a3d:.2f}% == reported {c['A3D_pct']:.2f}% (>θ2=10% -> ANISO-3D)")
    ok("ANISO-3D" in c["verdict"] and a3d>V["thresholds"]["theta2_pct"], f"{k}: ANISO-3D verdict consistent (A_3D>θ2)")

# --- Route-D dynamical vs static cross-check (axial z) ---
zsl=rd["z_modes56_slopes"]; dev=[abs(s-rd["static_sqrtC44"])/rd["static_sqrtC44"]*100 for s in zsl]
ok(max(dev)<2.6, f"Route-D axial-z dynamical slopes {['%.4f'%s for s in zsl]} vs √C44 within {max(dev):.2f}% (static-dynamic agree)")
# dynamical F-ISO (basal K vs M) PASS <=2%
fi=R["routeD_extension"]["fiso_dynamical_pct"]
ok(fi["SV_KvsM"]<2 and fi["SH_KvsM"]<2, f"dynamical F-ISO SV {fi['SV_KvsM']:.3f}% / SH {fi['SH_KvsM']:.3f}% ΓK-vs-ΓM PASS (<=2%)")

# --- Q-A class gap (AB vs BCC) + sub-order ---
for kern in ("step","gem8"):
    qa=R["polished_reeval"]["kernels"][kern]["QA"]
    ok(qa["cp_min"]=="AB" and qa["ncp_min"]=="BCC" and qa["class_gap"]>1e-4,
       f"Q-A {kern}: close-packed AB < non-CP BCC by {qa['class_gap']:.2e} (STACK-SELECTED); sub-order {qa['sub_order']}")

# --- split-step bias magnitude (chat's OWN comparison; NOT independent adjudication) ---
for kern in ("step","gem8"):
    st=R["polished_reeval"]["kernels"][kern]["structures"]["AB"]
    bias_pct=st["bias"]/st["e_polished"]*100
    ok(2.5<bias_pct<3.6, f"[chat-internal] {kern}:AB split-step bias {st['bias']:.3f}/particle = {bias_pct:.2f}% above polished min (2.6-3.4% class)")

print(f"[AUDIT] {len(P)} consistency checks PASS, {len(F)} FAIL\n")
for m in P: print("  ✓",m)
for m in F: print("  ✗",m)
