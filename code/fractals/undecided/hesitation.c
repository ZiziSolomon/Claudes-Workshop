/* hesitation.c — where does an orbit spend a billion steps before escaping?
 *
 * Iterates z -> z^2 + c from 0 until |z| > 2 (or a cap), accumulating a
 * density histogram of the orbit on an S x S grid over [-R,R]^2, and also
 * records the orbit's distance from its starting cycle in coarse time bins.
 *
 * build: gcc -O3 -o hesitation hesitation.c -lm
 * run:   ./hesitation RE IM S R LOG2CAP hist.bin [CX CY]
 * hist.bin: S*S uint64 counts over [CX-R,CX+R]x[CY-R,CY+R], row 0 = top
 */
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    if (argc < 7) { fprintf(stderr, "usage: RE IM S R LOG2CAP hist.bin\n"); return 1; }
    double complex c = atof(argv[1]) + I * atof(argv[2]);
    int S = atoi(argv[3]);
    double R = atof(argv[4]);
    long cap = 1L << atoi(argv[5]);
    uint64_t *h = calloc((size_t)S * S, sizeof(uint64_t));
    double complex z = 0;
    long n;
    double scale = S / (2 * R);
    double cx = argc > 8 ? atof(argv[7]) : 0, cy = argc > 8 ? atof(argv[8]) : 0;
    for (n = 1; n <= cap; n++) {
        z = z * z + c;
        double x = creal(z), y = cimag(z);
        if (x * x + y * y > 4.0) break;
        int i = (int)((x - cx + R) * scale), j = (int)((cy + R - y) * scale);
        if (i >= 0 && i < S && j >= 0 && j < S) h[(size_t)j * S + i]++;
    }
    printf("c=%.17g%+.17gi escaped=%s n=%ld\n", creal(c), cimag(c),
           n <= cap ? "yes" : "no", n);
    FILE *f = fopen(argv[6], "wb");
    fwrite(h, sizeof(uint64_t), (size_t)S * S, f);
    fclose(f);
    return 0;
}
