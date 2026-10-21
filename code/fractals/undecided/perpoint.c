/* perpoint.c — escape step of each "re im t_double" line in long double and __float128.
 * Prints "t_double t_longdouble t_quad". Input made from huge.bin samples (see README).
 * build: gcc -O3 -o perpoint perpoint.c -lquadmath
 */
#include <stdio.h>
#include <quadmath.h>
int main(){double x,y;long td;
 while(scanf("%lf %lf %ld",&x,&y,&td)==3){
  long double a=0,b=0,cr=x,ci=y; long n;
  for(n=1;n<(1L<<26);n++){long double t=a*a-b*b+cr; b=2*a*b+ci; a=t; if(a*a+b*b>4)break;}
  __float128 qa=0,qb=0,qr=x,qi=y; long m;
  for(m=1;m<(1L<<26);m++){__float128 t=qa*qa-qb*qb+qr; qb=2*qa*qb+qi; qa=t; if(qa*qa+qb*qb>4)break;}
  printf("%ld %ld %ld\n",td,n,m);}}
