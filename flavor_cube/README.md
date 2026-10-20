# Flavor Cube

An interactive page (`index.html`, served at `/flavor_cube/` on the site) built on the exploration note of October 19, 2026, *Geometric fermion operators at a vertex, and the Rubik's cube* (copied here as `SOURCE_NOTE.md`). Mathematics only: the research program it grew out of is closed (ledger V4.97, `STATUS.md`), and the page makes no physics claim.

The page has three modes:

- **Mixing.** The cube is turned by the three mixing angles of the standard parametrization (θ₁₂ about the third axis, then θ₁₃ about the second, then θ₂₃ about the first). The grid shows |U<sub>ij</sub>|², and χ² is computed live against the data E4 used (NuFIT 6.0 for leptons, UTfit 2022 for quarks). The presets are the measurements, tri-bimaximal mixing, E4's residual-symmetry patterns, and the gauge paper's two readings of 3/13.
- **Vertex.** The six neighbours of v₀ as faces: Furey's three colors are the axes, QR is a corner, the three pairings J₃, J₅, J₆ are drawn on the cube, and the 24 Fano symmetries fixing v₀ are buttons that move the cube (12 turns and 12 mirror moves, the group T<sub>d</sub>). Flat pictures show the torus link, the dual Szilassi face and the Fano plane.
- **Puzzle.** A working 3×3×3 cube labelled by e₁…e₆, with the corner-twist count of the note's R7(c), which is an analogy only.

## Files

| File | What it is |
|---|---|
| `index.html` | The page. Self-contained apart from three.js r128 (cdnjs) and Google Fonts. Its `<script id="pure">` block holds the logic and runs in Node too. |
| `check_geometry.py` | Recomputes every geometric statement the page uses (claims G1–G19), exact arithmetic; writes `geometry.json`. |
| `check_mixing.py` | Recomputes every mixing preset with E4's own `data_targets.py` and `e4lib.py`; writes `mixing.json`. |
| `crosscheck/` | An independent second computation of both, written without reading the first, and its outputs. |
| `test_page.mjs` | Runs the page's logic in Node: the 24 Fano moves are exactly T<sub>d</sub>, the puzzle is the Rubik's group (order of R U is 105), every preset's χ² matches E4 and `mixing.json`. |
| `test_browser.mjs` | Headless Chromium smoke test of all three modes at desktop and phone widths, both themes. |
| `SOURCE_NOTE.md` | The note the page is built on. |

## Reproducing

```
python3 flavor_cube/check_geometry.py      # numpy only
python3 flavor_cube/check_mixing.py        # imports E4's data_targets.py and e4lib.py
node flavor_cube/test_page.mjs
node flavor_cube/test_browser.mjs [--three path/to/three.min.js]   # needs playwright; --three if cdnjs is unreachable
```

## Conventions

- Labels ℤ₇, v₀ = 0 (Furey's e₇ is e₀ here). Up-triangles {i, i+1, i+3} are the Fano⁺ lines with e<sub>i</sub>e<sub>i+1</sub> = e<sub>i+3</sub>; down-triangles {i, i+2, i+3} are the Fano⁻ lines. QR = {1, 2, 4}.
- Cube faces: e₁ = +x, e₃ = −x, e₂ = +y, e₆ = −y, e₄ = +z, e₅ = −z. Axis k is Furey's color z<sub>k</sub> = e<sub>r</sub> + i e<sub>3r</sub> (r = 1, 2, 4); in the Mixing tab it is generation k, as in the gauge paper's §4.
- A complex phase cannot be shown as a turn, so the cube takes δ at the nearer of 0° and 180°. The grid and χ² use the full δ.
- p-values on the page count four observables with nothing fitted. E4's own p-values for its survivors (quoted in the preset notes) use two degrees of freedom, because two parameters were fitted.
