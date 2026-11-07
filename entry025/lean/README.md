# Lean check: 2-adic facts for y² = x³ − x

`CMTwoAdic.lean` proves the two 2-adic facts used in Entry 025 (PREREGISTRATION §3 and §7, paper Proposition 3). Both start from Gauss's formula #E(𝔽_p) = p + 1 − 2α with p = α² + β² and the stated normalisation of α mod 4:

- `split_one_mod_eight`: p ≡ 1 (mod 8), α ≡ 1 (mod 4) ⇒ 16 ∣ p + 1 − 2α
- `split_five_mod_eight`: p ≡ 5 (mod 8), α ≡ 3 (mod 4) ⇒ p + 1 − 2α ≡ 8 (mod 16)

Gauss's formula itself is an input and is **not** formalized here, as the file's header says.

## Checked with

- **Lean:** `Lean (version 4.22.0, x86_64-unknown-linux-gnu, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)`. This is the official v4.22.0 release binary.
- **Dependencies:** core library only (no Mathlib, no lake project). Run as `lean CMTwoAdic.lean`.
- **Result (2026-11-07):** exit 0, with no errors, warnings or `sorry`.
- **File:** SHA-256 `bb2069a10177664ecb1cd25c7a007f9c311db65394b503cabe89f181224fcf06`.

`#print axioms` output, verbatim (also in `lean_output.txt`):

```
'split_one_mod_eight' depends on axioms: [propext, Classical.choice, Quot.sound]
'split_five_mod_eight' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are Lean's three standard axioms. `sorryAx` does not appear.

The file ends with two non-vacuity examples:
- p = 17, α = 1, #E = 16;
- p = 37, α = −1, #E = 40.

The file was written outside this repository and added after the data were generated. It is not part of the frozen manifest.
