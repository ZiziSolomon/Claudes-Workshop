/* drift.c — distance of the slow orbit (c = 0.3076+0.4959i) from its near-neutral
 * 4-cycle, sampled every 2^15 steps. Output: "n r" lines. Used by drift_plot.py. */
#include <complex.h>
#include <stdio.h>
int main(){double complex c=0.30761860802680241+0.49591127971481713*I, w=-0.143196-0.035768*I;
 for(int it=0;it<50;it++){double complex f=w,d=1;for(int k=0;k<4;k++){d=2*f*d;f=f*f+c;} w-=(f-w)/(d-1);}
 double complex z=0; for(long n=1;;n++){z=z*z+c; if(creal(z)*creal(z)+cimag(z)*cimag(z)>4){printf("# escaped %ld\n",n);break;}
  if((n&((1<<15)-1))==0){ /* min distance to the island centre over the next 4 steps */
   double complex y=z; double r=cabs(y-w); for(int k=0;k<3;k++){y=y*y+c; double q=cabs(y-w); if(q<r)r=q;} printf("%ld %.6g\n",n,r);}}}
