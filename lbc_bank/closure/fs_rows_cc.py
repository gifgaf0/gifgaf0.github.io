#!/usr/bin/env python3
"""Second computation of the same superfluid fractions with the second leg's own instrument (second_leg/cc2d.py on
main, unchanged): a* by its Brent search (run_point, full=False), ground state by L-BFGS + Newton, and f_s by its
exact linear-response formula (twist check included). The metastable points use a seeded continuation along the
second leg's branch table from g = 13.0, at its tabulated a* values."""
import sys, json, time
sys.path.insert(0, "/tmp/claude-0/-home-claude-gifgaf0-github-io/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad")          # copy of lbc_bank/second_leg/cc2d.py from main (md5 checked below)
import hashlib
assert hashlib.md5(open("/tmp/claude-0/-home-claude-gifgaf0-github-io/b6f78e01-abcd-58dd-b0ba-f9859dbecce8/scratchpad/cc2d.py", "rb").read()).hexdigest() == "e6da46ef68bea7ede8de7dbefa0f9ada"
import cc2d as C
out = {}; t0 = time.time()
def save(): json.dump(C.jsonable(out), open("fs_rows_cc.json", "w"), indent=1)
for lab, kind, g, aguess in (("soft_g44", "step", 44.0, 1.3926604829399247), ("soft_g34", "step", 34.0, 1.4165),
                             ("soft_g28", "step", 28.0, 1.434440781135794), ("g6_g35", "g6", 35.0, 1.438)):
    res, st = C.run_point(kind, g, aguess, N=64, full=False)
    fx = C.superfluid_fraction(st, (1.0, 0.0), True); fy = C.superfluid_fraction(st, (0.0, 1.0), False)
    out[lab] = dict(g=g, kind=kind, astar=res.get("astar"), collapsed=res.get("collapsed_to_uniform"),
                    contrast=st.contrast, f_s=fx["fs_lr"], f_s_y=fy["fs_lr"], f_s_twist=fx["fs_twist"])
    print(f"[{lab}] a*={res.get('astar')} contrast={st.contrast:.2f} f_s(lr)={fx['fs_lr']:.6f} "
          f"f_s(y)={fy['fs_lr']:.6f} f_s(twist)={fx['fs_twist']:.6f} ({time.time()-t0:.0f}s)", flush=True); save()
kern = C.Kernel("step", 13.0)
path = [(13.0, 1.5099592443626995), (12.9, 1.5109044165973526), (12.8, 1.5118912026209708), (12.7, 1.5129328893871443),
        (12.6, 1.5140526146768853), (12.5, 1.51529816851384), (12.45, 1.516002330056777), (12.4, 1.5168103105250197)]
seed = None
for g, a in path:
    st = C.ground_state(C.hex_cell(a), C.Kernel("step", g), 64, 1.0, seed=seed)
    seed = st
    if g in (12.5, 12.4):
        fx = C.superfluid_fraction(st, (1.0, 0.0), True)
        out[f"meta_g{g}"] = dict(g=g, kind="step", astar=a, contrast=st.contrast, uniform=st.uniform,
                                 f_s=fx["fs_lr"], f_s_twist=fx["fs_twist"])
        print(f"[meta g={g}] a={a:.6f} contrast={st.contrast:.2f} uniform={st.uniform} f_s(lr)={fx['fs_lr']:.6f} "
              f"f_s(twist)={fx['fs_twist']:.6f} ({time.time()-t0:.0f}s)", flush=True); save()
    else:
        print(f"[meta g={g}] seed step contrast={st.contrast:.2f} uniform={st.uniform} ({time.time()-t0:.0f}s)", flush=True)
print("FS_ROWS_CC DONE", flush=True)
