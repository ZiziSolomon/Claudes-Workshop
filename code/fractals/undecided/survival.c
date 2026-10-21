/* survival.c — is the 1/N law a fact about c or about double precision?
 *
 * Draws M uniform random c in [-2,0.5]x[0,1.25] (skipping the main cardioid
 * and period-2 disc), iterates each in double, long double and __float128 up
 * to 2^L steps, and prints, for N = 2^k, the fraction of samples not yet
 * escaped by N in each arithmetic. Per-point escape steps differ between
 * precisions; the question is whether these survival curves do.
 *
 * build: gcc -O3 -fopenmp -o survival survival.c -lquadmath -lm
 * run:   ./survival M L
 */
#include <quadmath.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double u01(uint64_t k)
{
    k += 0x9E3779B97F4A7C15ULL;
    k = (k ^ (k >> 30)) * 0xBF58476D1CE4E5B9ULL;
    k = (k ^ (k >> 27)) * 0x94D049BB133111EBULL;
    k ^= k >> 31;
    return (k >> 11) * (1.0 / 9007199254740992.0);
}

#define ESC(T, cr, ci, cap, out)                                       \
    do {                                                               \
        T a = 0, b = 0, r_ = (cr), i_ = (ci);                          \
        long n_;                                                       \
        for (n_ = 1; n_ <= (cap); n_++) {                              \
            T t_ = a * a - b * b + r_;                                 \
            b = 2 * a * b + i_;                                        \
            a = t_;                                                    \
            if (a * a + b * b > 4) break;                              \
        }                                                              \
        (out) = n_;                                                    \
    } while (0)

int main(int argc, char **argv)
{
    long M = atol(argv[1]);
    int L = atoi(argv[2]);
    long cap = 1L << L;
    long cnt[3][64] = {{0}}, used = 0;
    #pragma omp parallel for schedule(dynamic, 256) reduction(+:used)
    for (long s = 0; s < M; s++) {
        double x = -2.0 + 2.5 * u01(2 * s), y = 1.25 * u01(2 * s + 1);
        double q = (x - 0.25) * (x - 0.25) + y * y;
        if (q * (q + (x - 0.25)) <= 0.25 * y * y || (x + 1) * (x + 1) + y * y <= 0.0625) continue;
        long e[3];
        ESC(double, x, y, cap, e[0]);
        ESC(long double, x, y, cap, e[1]);
        ESC(__float128, x, y, cap, e[2]);
        used++;
        for (int p = 0; p < 3; p++)
            for (int k = 0; k <= L; k++)
                if (e[p] > (1L << k)) {
                    #pragma omp atomic
                    cnt[p][k]++;
                }
    }
    printf("# %ld samples outside the analytic regions; fraction not escaped by N\n", used);
    printf("%9s %12s %12s %12s\n", "N", "double", "long double", "float128");
    for (int k = 4; k <= L; k++)
        printf("%9ld %12.4e %12.4e %12.4e\n", 1L << k, (double)cnt[0][k] / used,
               (double)cnt[1][k] / used, (double)cnt[2][k] / used);
    return 0;
}
