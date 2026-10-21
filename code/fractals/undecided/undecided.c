/* undecided.c — how much of the Mandelbrot plane can a computer actually decide?
 *
 * For each sample point c on a grid over the upper half of [-2,0.5]x[0,1.25]
 * we record the iteration at which its membership was *settled*:
 *   - escape: |z_n| > 2 at step n  -> certainly outside M
 *   - interior: at checkpoint n = 2^k we look for an attracting cycle near z_n
 *     (find a near-return of period p, Newton-refine the cycle, check that the
 *     multiplier has modulus < 1)  -> inside a hyperbolic component of M
 *   - the main cardioid and period-2 disc are settled analytically at step 0.
 * Anything not settled by the cap is "undecided".
 *
 * The interior test is numerical (double precision), not interval-certified,
 * but an attracting cycle found by a converged Newton step is strong evidence.
 *
 * Output: binary file of int32 settle-times (positive = escaped at n,
 * negative = interior detected at checkpoint n, 0 = never settled) plus
 * a header line on stdout.
 *
 * Each sample is placed uniformly at random inside its grid cell (stratified
 * sampling), so the fraction of never-settled samples is an unbiased estimate
 * of the fraction of the box that never settles by the cap.
 *
 * build: gcc -O3 -fopenmp -o undecided undecided.c -lm
 * run:   ./undecided W H LOG2CAP out.bin
 *        ./undecided --points LOG2CAP < points.txt
 */
#include <complex.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

/* longest cycle searched for at a checkpoint n is min(n, PMAX) */
#define PMAX (1L << 20)

/* splitmix64: a cheap deterministic per-cell random number in [0,1) */
static double jitter(uint64_t k)
{
    k += 0x9E3779B97F4A7C15ULL;
    k = (k ^ (k >> 30)) * 0xBF58476D1CE4E5B9ULL;
    k = (k ^ (k >> 27)) * 0x94D049BB133111EBULL;
    k ^= k >> 31;
    return (k >> 11) * (1.0 / 9007199254740992.0);
}

static int attracting_cycle(double complex c, double complex z0, long pmax)
{
    /* look for the smallest p with |f^p(z0) - z0| small */
    double complex z = z0;
    int p = 0;
    double best = 1e300;
    int bestp = 0;
    for (int k = 1; k <= pmax; k++) {
        z = z * z + c;
        double d = cabs(z - z0);
        if (d < 1e-6) { p = k; break; }
        if (d < best) { best = d; bestp = k; }
    }
    if (p == 0) {
        if (best < 1e-3) p = bestp; else return 0;
    }
    /* Newton on g(w) = f^p(w) - w */
    double complex w = z0;
    for (int it = 0; it < 30; it++) {
        double complex fw = w, dfw = 1.0;
        for (int k = 0; k < p; k++) { dfw = 2.0 * fw * dfw; fw = fw * fw + c; }
        double complex g = fw - w, dg = dfw - 1.0;
        if (cabs(dg) < 1e-300) return 0;
        double complex step = g / dg;
        w -= step;
        if (cabs(step) < 1e-14 * (1.0 + cabs(w))) break;
    }
    double complex fw = w, lam = 1.0;
    for (int k = 0; k < p; k++) { lam = 2.0 * fw * lam; fw = fw * fw + c; }
    /* Accept only if every test positively passes. (An earlier version wrote
     * these as "if (bad > tol) reject"; when Newton diverged to NaN, every
     * comparison was false and the point was declared interior.) The cycle
     * must close, be attracting, and be the one the orbit is near. */
    if (cabs(fw - w) <= 1e-10 && cabs(lam) < 1.0 && cabs(w - z0) <= 1e-2)
        return p;
    return 0;
}

/* --points LOG2CAP: read "re im" lines on stdin, iterate each up to 2^LOG2CAP
 * with the same checks, print the settle time */
static int points_mode(int L)
{
    long cap = 1L << L;
    double x, y;
    while (scanf("%lf %lf", &x, &y) == 2) {
        double complex c = x + I * y, z = 0;
        long next = 16, res = 0;
        for (long n = 1; n <= cap; n++) {
            z = z * z + c;
            if (creal(z) * creal(z) + cimag(z) * cimag(z) > 4.0) { res = n; break; }
            if (n == next) {
                int p = attracting_cycle(c, z, n < PMAX ? n : PMAX);
                if (p) { res = -n; printf("period %d ", p); break; }
                next <<= 1;
            }
        }
        printf("%.17g %.17g %ld\n", x, y, res);
        fflush(stdout);
    }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc == 3 && argv[1][0] == '-') return points_mode(atoi(argv[2]));
    if (argc < 5) { fprintf(stderr, "usage: W H LOG2CAP out.bin\n"); return 1; }
    int W = atoi(argv[1]), H = atoi(argv[2]), L = atoi(argv[3]);
    long cap = 1L << L;
    double x0 = -2.0, x1 = 0.5, y0 = 0.0, y1 = 1.25;
    int32_t *out = malloc(sizeof(int32_t) * (size_t)W * H);

    #pragma omp parallel for schedule(dynamic, 1)
    for (int j = 0; j < H; j++) {
        for (int i = 0; i < W; i++) {
            uint64_t key = ((uint64_t)j << 32) | (uint64_t)i;
            double x = x0 + (i + jitter(2 * key)) * (x1 - x0) / W;
            double y = y0 + (j + jitter(2 * key + 1)) * (y1 - y0) / H;
            double complex c = x + I * y;
            int32_t res = 0;
            /* analytic: main cardioid, period-2 disc */
            double q = (x - 0.25) * (x - 0.25) + y * y;
            if (q * (q + (x - 0.25)) <= 0.25 * y * y ||
                (x + 1) * (x + 1) + y * y <= 0.0625) {
                out[(size_t)j * W + i] = -1;
                continue;
            }
            double complex z = 0;
            long next = 16;
            for (long n = 1; n <= cap; n++) {
                z = z * z + c;
                double re = creal(z), im = cimag(z);
                if (re * re + im * im > 4.0) { res = (int32_t)n; break; }
                if (n == next) {
                    if (attracting_cycle(c, z, n < PMAX ? n : PMAX)) { res = -(int32_t)n; break; }
                    next <<= 1;
                }
            }
            out[(size_t)j * W + i] = res;
        }
    }
    FILE *f = fopen(argv[4], "wb");
    fwrite(out, sizeof(int32_t), (size_t)W * H, f);
    fclose(f);
    printf("W=%d H=%d cap=%ld box=[%g,%g]x[%g,%g]\n", W, H, cap, x0, x1, y0, y1);
    return 0;
}
