import sys, json, frac, numpy as np
N=int(sys.argv[1]); frac.N=N
frac.X,frac.Y=[a.astype(float) for a in np.meshgrid(np.arange(N)-N//2, np.arange(N)-N//2, indexing='ij')]
out=[frac.run(d,0.0) for d in (16,32)]
print(N, json.dumps(out), "log slope 16->32:", (out[1]['E']-out[0]['E'])/np.log(2), flush=True)
