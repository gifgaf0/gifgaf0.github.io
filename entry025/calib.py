# Exploratory pipeline calibration on exhaustive low ranges (seen data; not part of any decisive test).
import cypari2, sys, time
pari = cypari2.Pari(); pari.allocatemem(2*10**9)
pari('count(e,t,x,mod4)=my(c=0,c1=0,c2=0,bad=ellglobalred(e)[1]);forprime(p=5,x,if(bad%p==0,next);if(mod4&&p%4!=1,next);my(N=p+1-ellap(e,p));if(N%t,next);if(isprime(N/t),c++;if(p%3==1,c1++,c2++)));[c,c1,c2]')
X=int(sys.argv[1]); which=sys.argv[2]
curves={'zyw_serre':('[0,0,0,6,-2]',1,0),'cm32':('[0,0,0,-1,0]',8,1),'37a1':('[0,0,1,-1,0]',1,0),'cm32_t4check':('[0,0,0,4,0]',8,1)}
a,t,m=curves[which]; t0=time.time()
print(which,X,pari(f'count(ellinit({a}),{t},{X},{m})'),'%.0fs'%(time.time()-t0))
