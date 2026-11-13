import cypari2, time, random
pari=cypari2.Pari(); pari.allocatemem(2*10**9)
pari('''Hpr(N)=my(s=0,F=factor(N),f2,D);if(N==0,return(-1/12));if(N%4==1||N%4==2,return(0));
 fordiv(core(N,1)[2],f, D=-N/f^2; if(D%4==0||D%4==1, s+= qfbclassno(D)/ if(D==-3,3,if(D==-4,2,1))));s''')
Hpr=pari("Hpr"); random.seed(2)
for P in [3000,11320,10**5,10**6]:
    p=int(pari.nextprime(P)); ts=[2*p-random.randrange(1,5000) for _ in range(1000)]
    Ns=[4*p*p-t*t for t in ts]
    bad=0; t0=time.perf_counter()
    for N in Ns: Hpr(N)
    t1=time.perf_counter()
    for N in Ns: pari.qfbhclassno(N)
    t2=time.perf_counter()
    for N in Ns[:300]:
        if Hpr(N)!=pari.qfbhclassno(N): bad+=1
    print(f"p~{P}: maxN={max(Ns):.2e} proven {1e6*(t1-t0)/1000:.0f}us  qfbh {1e6*(t2-t1)/1000:.0f}us  mismatches/300={bad}")
