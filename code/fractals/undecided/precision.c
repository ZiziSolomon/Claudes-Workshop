/* precision.c — does the slowest orbit's escape time survive more precision?
 *
 * Iterates z -> z^2 + c for c = 0.30761860802680241 + 0.49591127971481713i
 * (the double nearest each decimal is used as the exact parameter in every
 * precision, so only the arithmetic changes) in double, long double and
 * __float128, and prints the escape step and the three reinjection times
 * (steps where |z| < 2e-3, i.e. close passes to the critical point).
 *
 * build: gcc -O3 -o precision precision.c -lquadmath -lm
 * run:   ./precision d|ld|q
 */
#include <quadmath.h>
#include <stdio.h>
#include <string.h>

#define RUN(T)                                                             \
    do {                                                                   \
        T cr = 0.30761860802680241, ci = 0.49591127971481713, x = 0, y = 0; \
        for (long n = 1; n < (1L << 32); n++) {                            \
            T x2 = x * x, y2 = y * y;                                      \
            if (x2 + y2 > 4) { printf("escaped at %ld\n", n - 1); break; } \
            y = 2 * x * y + ci;                                            \
            x = x2 - y2 + cr;                                              \
            if (x * x + y * y < (T)4e-6)                                   \
                printf("close pass to 0 at %ld\n", n);                     \
        }                                                                  \
    } while (0)

int main(int argc, char **argv)
{
    if (argc < 2) return 1;
    if (!strcmp(argv[1], "d")) RUN(double);
    else if (!strcmp(argv[1], "ld")) RUN(long double);
    else RUN(__float128);
    return 0;
}
