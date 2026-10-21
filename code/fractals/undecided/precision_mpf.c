/* precision_mpf.c — the slowest orbit in GMP mpf arithmetic at BITS precision.
 * Same parameter as precision.c (the exact binary values of the two doubles).
 * Prints the start of each cluster of close passes to 0 and the escape step.
 *
 * build: gcc -O2 -o precision_mpf precision_mpf.c -lgmp -lm
 * run:   ./precision_mpf BITS [trace]
 * With "trace", also prints "n r" every 2^15 steps: the distance from the
 * near-neutral 4-cycle point (as in drift.c), for drift_plot.py.
 */
#include <gmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv)
{
    mpf_set_default_prec(atoi(argv[1]));
    mpf_t cr, ci, x, y, x2, y2, t;
    mpf_inits(cr, ci, x, y, x2, y2, t, NULL);
    mpf_set_d(cr, 0.30761860802680241);
    mpf_set_d(ci, 0.49591127971481713);
    long last = -100000000;
    int trace = argc > 2;
    double wr = -0.14319555200872658, wi = -0.035767671737117764; /* 4-cycle point */
    for (long n = 1; n < (1L << 32); n++) {
        mpf_mul(x2, x, x);
        mpf_mul(y2, y, y);
        mpf_add(t, x2, y2);
        if (mpf_cmp_d(t, 4.0) > 0) { printf("escaped at %ld\n", n - 1); break; }
        mpf_mul(y, x, y);
        mpf_mul_2exp(y, y, 1);
        mpf_add(y, y, ci);
        mpf_sub(x, x2, y2);
        mpf_add(x, x, cr);
        if (trace && (n & ((1 << 15) - 1)) == 0) {
            /* min distance to the cycle point over the next 4 steps, in double */
            double a = mpf_get_d(x), b = mpf_get_d(y), r = 1e9;
            for (int k = 0; k < 4; k++) {
                double d = hypot(a - wr, b - wi);
                if (d < r) r = d;
                double t2 = a * a - b * b + 0.30761860802680241;
                b = 2 * a * b + 0.49591127971481713;
                a = t2;
            }
            printf("%ld %.6g\n", n, r);
        }
        {
            mpf_mul(x2, x, x);
            mpf_mul(y2, y, y);
            mpf_add(t, x2, y2);
            if (mpf_cmp_d(t, 4e-6) < 0) {
                if (n - last > 10000000) { printf("close-pass cluster at %ld\n", n); fflush(stdout); }
                last = n;
            }
        }
    }
    return 0;
}
