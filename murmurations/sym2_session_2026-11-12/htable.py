"""Build tables of 12*H(4p^2 - t^2) for t in [t_lo(p), 2p), with H computed
unconditionally from qfbclassno (Shanks; documented unconditional for |D| < 2e10).
Usage: python3 -I htable.py <jobfile.json> <worker_id> <n_workers> <outprefix>
jobfile: list of [p, t_lo].
"""
import sys, json, time
import numpy as np
import cypari2

pari = cypari2.Pari()
pari.allocatemem(1 * 10**9)
pari('''Hpr(N)=my(s=0,D);if(N==0,return(-1/12));if(N%4==1||N%4==2,return(0));
 if(N>=2*10^10, error("N too large for unconditional qfbclassno"));
 fordiv(core(N,1)[2],f, D=-N/f^2; if(D%4==0||D%4==1, s+= qfbclassno(D)/if(D==-3,3,if(D==-4,2,1))));s''')
pari('''Hrow(p,tlo)=vector(2*p-tlo,i,my(t=tlo+i-1);12*Hpr(4*p^2-t^2))''')
Hrow = pari('Hrow')

jobs = json.load(open(sys.argv[1]))
wid, nw, outp = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
mine = jobs[wid::nw]
ps, tlos, offs, chunks = [], [], [0], []
t0 = time.time()
for i, (p, tlo) in enumerate(mine):
    row = np.array([int(v) for v in Hrow(p, tlo)], dtype=np.int64)
    ps.append(p); tlos.append(tlo); chunks.append(row); offs.append(offs[-1] + len(row))
    if (i + 1) % 200 == 0 or i + 1 == len(mine):
        np.savez(f"{outp}_w{wid}.npz", ps=np.array(ps), tlos=np.array(tlos),
                 offs=np.array(offs), vals=np.concatenate(chunks))
        print(f"w{wid}: {i+1}/{len(mine)} p={p} elapsed {time.time()-t0:.0f}s", flush=True)
print(f"w{wid} DONE {time.time()-t0:.0f}s", flush=True)
