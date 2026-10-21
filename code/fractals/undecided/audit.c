/* audit.c — re-check every "interior" verdict in an undecided.c output file.
 *
 * For each sample flagged interior by the cycle test (not the analytic
 * cardioid/disc test), recompute its c (same jitter) and iterate a further
 * 2^EXTRA steps beyond its settle time. Any escape is a false certificate.
 *
 * build: gcc -O3 -fopenmp -o audit audit.c -lm
 * run:   ./audit out.bin W H EXTRA
 */
#include <complex.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double jitter(uint64_t k)
{
    k += 0x9E3779B97F4A7C15ULL;
    k = (k ^ (k >> 30)) * 0xBF58476D1CE4E5B9ULL;
    k = (k ^ (k >> 27)) * 0x94D049BB133111EBULL;
    k ^= k >> 31;
    return (k >> 11) * (1.0 / 9007199254740992.0);
}

int main(int argc, char **argv)
{
    if (argc < 5) { fprintf(stderr, "usage: out.bin W H EXTRA\n"); return 1; }
    int W = atoi(argv[2]), H = atoi(argv[3]);
    long extra = 1L << atoi(argv[4]);
    int32_t *t = malloc(sizeof(int32_t) * (size_t)W * H);
    FILE *f = fopen(argv[1], "rb");
    if (fread(t, sizeof(int32_t), (size_t)W * H, f) != (size_t)W * H) return 1;
    fclose(f);
    long checked = 0, bad = 0;
    #pragma omp parallel for schedule(dynamic, 16) reduction(+:checked, bad)
    for (int j = 0; j < H; j++) {
        for (int i = 0; i < W; i++) {
            int32_t s = t[(size_t)j * W + i];
            if (s >= -1) continue;              /* escaped, unsettled, or analytic */
            uint64_t key = ((uint64_t)j << 32) | (uint64_t)i;
            double x = -2.0 + (i + jitter(2 * key)) * 2.5 / W;
            double y = (j + jitter(2 * key + 1)) * 1.25 / H;
            double complex c = x + I * y, z = 0;
            long total = (long)(-s) + extra;
            checked++;
            for (long n = 1; n <= total; n++) {
                z = z * z + c;
                if (creal(z) * creal(z) + cimag(z) * cimag(z) > 4.0) {
                    bad++;
                    #pragma omp critical
                    printf("FALSE INTERIOR %.17g %.17g flagged@%d escaped@%ld\n", x, y, -s, n);
                    break;
                }
            }
        }
    }
    printf("audited %ld interior verdicts, %ld escaped within settle+2^%s steps\n", checked, bad, argv[4]);
    return 0;
}
