/* gen_E_026.c -- Entry 026 arm E generator.
 * All primes lo <= p < hi by a segmented sieve of Eratosthenes (odd numbers only).
 * Output (binary, little-endian uint64): header {magic, lo, hi, blocksize, nblocks, nprimes,
 * sum of primes mod 2^64, xor of primes}, then per block:
 * {nprimes, first prime, last prime, lag1[16][16], lag2[16][16]}.
 * lag1[i][j] counts adjacent pairs (p_n, p_n+1) with p_n mod 60 = U[i], p_n+1 mod 60 = U[j];
 * lag2 the same for (p_n, p_n+2). A pair is assigned to the block of its first prime.
 * Only pairs with both primes in [lo, hi) are counted, so lag-1 total = nprimes - 1.
 * Usage: gen_E_026 lo hi blocksize outfile
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#define SEG (1u << 24)          /* odd numbers per segment: covers 2^25 integers */
static const int U[16] = {1,7,11,13,17,19,23,29,31,37,41,43,47,49,53,59};

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: lo hi blocksize outfile\n"); return 1; }
    uint64_t lo = strtoull(argv[1], 0, 10), hi = strtoull(argv[2], 0, 10), B = strtoull(argv[3], 0, 10);
    if (lo < 100 || hi <= lo || B == 0) { fprintf(stderr, "bad args\n"); return 1; }
    uint64_t nb = (hi - lo + B - 1) / B;
    int idx[60]; for (int i = 0; i < 60; i++) idx[i] = -1;
    for (int i = 0; i < 16; i++) idx[U[i]] = i;

    /* base primes up to sqrt(hi) */
    uint64_t r = (uint64_t)sqrtl((long double)hi) + 2;
    while (r * r < hi) r++;
    char *bs = calloc(r + 1, 1);
    uint32_t *bp = malloc(sizeof(uint32_t) * (r / 2 + 10)); size_t nbp = 0;
    for (uint64_t i = 2; i <= r; i++) if (!bs[i]) { if (i > 2) bp[nbp++] = (uint32_t)i; for (uint64_t j = i * i; j <= r; j += i) bs[j] = 1; }
    free(bs);

    uint64_t per = 3 + 2 * 256;
    uint64_t *blk = calloc(nb * per, sizeof(uint64_t));
    uint64_t np = 0, sum = 0, xr = 0;
    int prev = -1, prev2 = -1; uint64_t prevblk = 0, prev2blk = 0;
    unsigned char *seg = malloc(SEG);
    uint64_t start = lo | 1;                     /* first odd >= lo */
    for (uint64_t s = start; s < hi; s += 2ull * SEG) {
        uint64_t e = s + 2ull * SEG; if (e > hi) e = hi;          /* odd numbers s, s+2, ..., < e */
        uint64_t n = (e - s + 1) / 2;
        memset(seg, 1, n);
        for (size_t k = 0; k < nbp; k++) {
            uint64_t p = bp[k];
            if (p * p >= e) break;
            uint64_t m = p * p;
            if (m < s) { m = ((s + p - 1) / p) * p; if (!(m & 1)) m += p; }
            for (uint64_t j = (m - s) / 2; j < n; j += p) seg[j] = 0;
        }
        for (uint64_t j = 0; j < n; j++) if (seg[j]) {
            uint64_t p = s + 2 * j;
            int c = idx[p % 60];
            uint64_t b = (p - lo) / B;
            uint64_t *B0 = blk + b * per;
            if (B0[0] == 0) B0[1] = p;
            B0[0]++; B0[2] = p;
            if (prev >= 0) blk[prevblk * per + 3 + prev * 16 + c]++;
            if (prev2 >= 0) blk[prev2blk * per + 3 + 256 + prev2 * 16 + c]++;
            prev2 = prev; prev2blk = prevblk; prev = c; prevblk = b;
            np++; sum += p; xr ^= p;
        }
    }
    FILE *f = fopen(argv[4], "wb");
    uint64_t hdr[8] = {0x3032364547454e45ull, lo, hi, B, nb, np, sum, xr};
    fwrite(hdr, 8, 8, f); fwrite(blk, 8, nb * per, f); fclose(f);
    fprintf(stderr, "primes %llu in [%llu, %llu), blocks %llu\n", (unsigned long long)np,
            (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)nb);
    return 0;
}
