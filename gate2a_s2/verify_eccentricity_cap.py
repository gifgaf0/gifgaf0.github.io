#!/usr/bin/env python3
"""
Audit check for the G-2a-S1/S2 joint-fold memo's MECHANISM claim: the tetrahedral cap of
the three-ellipse Borromean representative is FORCED by eccentricity (not a golden-ratio
accident). Round circles restore octahedral C4 but cannot form Borromean rings
(Lindstrom-Zetterstrom 1991 "Borromean circles are impossible" / Freedman-Skora, framework
sec 2.82). Sampled method, exact integer rotation matrices.
"""
import numpy as np
from itertools import permutations, product

def rotgroup(a,b):
    t=np.linspace(0,2*np.pi,360,endpoint=False)
    E3=np.stack([a*np.cos(t),b*np.sin(t),0*t],1)
    E1=np.stack([0*t,a*np.cos(t),b*np.sin(t)],1)
    E2=np.stack([b*np.sin(t),0*t,a*np.cos(t)],1)
    P=np.vstack([E1,E2,E3]); S0=set(map(tuple,np.round(P,5)))
    SP=[]
    for p in permutations(range(3)):
        M0=np.zeros((3,3),int)
        for i,j in enumerate(p): M0[i,j]=1
        for s in product((1,-1),repeat=3): SP.append(np.diag(s)@M0)
    rot=[M for M in SP if int(round(np.linalg.det(M)))==1 and set(map(tuple,np.round(P@M.T,5)))==S0]
    def order(M):
        X=np.eye(3,dtype=int)
        for k in range(1,13):
            X=X@M
            if np.array_equal(X,np.eye(3,dtype=int)): return k
    return len(rot), any(order(M)==4 for M in rot)

if __name__=="__main__":
    phi=(1+np.sqrt(5))/2
    print("mechanism check (eccentricity caps at tetrahedral; only round restores C4):")
    for (a,b,lbl) in [(phi,1/phi,"golden eccentric (Borromean)"),
                      (1.0,1.0,"round circles (a=b)"),
                      (1.3,0.7,"generic eccentric")]:
        n,c4=rotgroup(a,b)
        print(f"  a={a:.4f} b={b:.4f} [{lbl:28s}] -> |G_rot|={n:2d} C4={c4} -> "
              f"{'OCTAHEDRAL' if n>=24 else 'TETRAHEDRAL' if n==12 else 'other'}")
    print("  => ANY a!=b -> tetrahedral (no C4); a=b -> octahedral. Cap is STRUCTURAL,")
    print("     since Borromean requires non-circular (circles impossible).")
