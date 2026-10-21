/* growth.c — how many bits does the slowest orbit consume?
 * Accumulates S(n) = sum log|2 z_k| (the log of the derivative of f^n, i.e. how
 * much an initial rounding error is stretched) along the double-precision orbit,
 * printing S every 2^26 steps and the largest growth over any window.
 * build: gcc -O3 -o growth growth.c -lm
 */
#include <complex.h>
#include <math.h>
#include <stdio.h>
int main(){double complex c=0.30761860802680241+0.49591127971481713*I,z=0; double S=0, Smin=0, best=0; long nmin=0,b1=0,b2=0;
 for(long n=1;;n++){ if(n>1)S+=log(2*cabs(z)); z=z*z+c; if(cabs(z)>2)break;
  if(S<Smin){Smin=S;nmin=n;} if(S-Smin>best){best=S-Smin;b1=nmin;b2=n;}
  if(n%(1L<<26)==0) printf("n=%.2e  S=%.1f nats\n",(double)n,S);}
 printf("largest growth over any window: %.1f nats (= %.0f bits) from n=%ld to n=%ld\n",best,best/log(2),b1,b2);}
