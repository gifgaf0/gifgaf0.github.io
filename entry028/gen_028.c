/* gen_028.c -- Entry 028 stratum generator.
 * For each stratum read from stdin as "r y_r s_r pair_index", finds the first NTAKE = n + 2 = 12,500,002 primes
 * >= s_r by a segmented sieve of Eratosthenes (odd numbers only, presieve pattern for 3,5,7,11,13),
 * drops the first, and keeps NK = n + 1 = 12,500,001 primes q_0 < ... < q_{NK-1}:
 *   lag1[i][j] = #{t : q_t mod 60 = U[i], q_{t+1} mod 60 = U[j]}   (NK - 1 = n = 12,500,000 pairs)
 *   lag2[i][j] = same for (q_t, q_{t+2})                            (NK - 2 = 12,499,999 pairs)
 * plus count, first and last kept prime, sum mod 2^64 and xor of the kept primes, and the sampled pair
 * (q_j, q_{j+1}) for j = pair_index.  The sieve never goes beyond y_r + WIDTH (5e8); if it would,
 * the record's flags bit 0 is set (boundary failure) and the build refuses it.
 * Output: binary records (little-endian), struct rec below, one per input line.
 * Usage: gen_028 OUTFILE < strata.txt          (compile: gcc -O3 -march=native -o gen_028 gen_028.c -lm)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#define NTAKE 12500002ull
#define WIDTH 500000000ull
#define SEG   (1u << 21)                 /* odd numbers per segment (covers 2^22 integers) */
#define PMAX  1460000ull                 /* > sqrt(2.1315e12): covers the band (sqrt(2.05e12) = 1431782.8) and the 2.1e12 boundary smoke */
static const int U[16] = {1,7,11,13,17,19,23,29,31,37,41,43,47,49,53,59};

typedef struct {
    uint64_t magic, r, y_r, s_r, nkept, first, last, sum, xr, pair_index, pair_p, pair_q, flags, nseen;
    uint32_t lag1[256], lag2[256];
} rec;

static uint32_t *bp; static size_t nbp;
static unsigned char *pat; static const uint64_t PER = 15015;   /* 3*5*7*11*13 odd period */

static void base_primes(void) {
    char *bs = calloc(PMAX + 1, 1); bp = malloc(sizeof(uint32_t) * 120000); nbp = 0;
    for (uint64_t i = 2; i <= PMAX; i++) if (!bs[i]) { if (i > 13) bp[nbp++] = (uint32_t)i;
        for (uint64_t j = i * i; j <= PMAX; j += i) bs[j] = 1; }
    free(bs);
    /* pattern over odd numbers: pat[k] = 1 iff odd number (2k+1) coprime to 15015; period 15015 in k */
    pat = malloc(PER + SEG);
    for (uint64_t k = 0; k < PER + SEG; k++) { uint64_t n = 2 * k + 1;
        pat[k] = (n % 3 && n % 5 && n % 7 && n % 11 && n % 13) ? 1 : 0; }
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: gen_028 OUTFILE < strata.txt\n"); return 1; }
    base_primes();
    int idx[60]; for (int i = 0; i < 60; i++) idx[i] = -1; for (int i = 0; i < 16; i++) idx[U[i]] = i;
    FILE *fo = fopen(argv[1], "wb"); if (!fo) { perror("out"); return 1; }
    unsigned char *seg = malloc(SEG);
    uint64_t *nxt = malloc(sizeof(uint64_t) * nbp);      /* next odd multiple index per base prime */
    unsigned long long r, yr, sr, pj;
    while (scanf("%llu %llu %llu %llu", &r, &yr, &sr, &pj) == 4) {
        rec R; memset(&R, 0, sizeof R);
        R.magic = 0x3832304E45474545ull; R.r = r; R.y_r = yr; R.s_r = sr; R.pair_index = pj;
        uint64_t lim = yr + WIDTH;                       /* hard boundary */
        uint64_t start = sr | 1;                         /* first odd >= s_r (s_r > 2) */
        uint64_t k0 = (start - 1) / 2;                   /* odd n = 2k+1 */
        for (size_t t = 0; t < nbp; t++) {               /* first odd multiple of p >= start, as k index */
            uint64_t p = bp[t], m = ((start + p - 1) / p) * p; if (!(m & 1)) m += p;
            nxt[t] = (m - 1) / 2;
        }
        uint64_t seen = 0; int prev = -1, prev2 = -1; int done = 0;
        for (uint64_t k = k0; !done; k += SEG) {
            uint64_t n = SEG;
            if (2 * (k + n) + 1 > lim) {                 /* clip at boundary */
                if (2 * k + 1 >= lim) { R.flags |= 1; break; }
                n = (lim - (2 * k + 1) + 1) / 2;
            }
            memcpy(seg, pat + (k % PER), n);              /* presieve 3,5,7,11,13 */
            for (size_t t = 0; t < nbp; t++) {
                uint64_t p = bp[t], j = nxt[t];
                if (j >= k + n) continue;
                for (j -= k; j < n; j += p) seg[j] = 0;
                nxt[t] = j + k;
            }
            /* s_r >= 1.05e12 > 13^2 so the small primes themselves are never in range */
            for (uint64_t j = 0; j < n; j++) if (seg[j]) {
                uint64_t p = 2 * (k + j) + 1;
                seen++;
                if (seen == 1) continue;                  /* drop the first prime >= s_r */
                uint64_t t = seen - 2;                    /* kept index */
                int c = idx[p % 60];
                if (t == 0) R.first = p;
                if (prev >= 0) R.lag1[prev * 16 + c]++;
                if (prev2 >= 0) R.lag2[prev2 * 16 + c]++;
                prev2 = prev; prev = c;
                R.sum += p; R.xr ^= p; R.nkept++; R.last = p;
                if (t == pj) R.pair_p = p;
                if (t == pj + 1) R.pair_q = p;
                if (seen == NTAKE) { done = 1; break; }
            }
        }
        if (!done) R.flags |= 1;
        if (R.last >= lim) R.flags |= 2;
        R.nseen = seen;
        fwrite(&R, sizeof R, 1, fo); fflush(fo);
    }
    fclose(fo);
    return 0;
}
