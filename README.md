# Boolean Tile Basis

**GitHub Pages site:** [https://pstdenis.github.io/Boolean-Tile/](https://pstdenis.github.io/Boolean-Tile/)

The 16 Boolean functions of two variables — the "Boolean tiles" — form a complete algebraic, geometric, and physical system. This project traces them from truth tables through Łukasiewicz logic, iterated function system (IFS) fractals, Bloch-sphere quantum states, 2-qubit unitary gates, and Ising spin Hamiltonians.

## Repository structure

- **`docs/`** — GitHub Pages site with the full paper and interactive visualizations
- **`docs/Boolean Tile Basis.html`** — The working paper
- **`docs/Polar IFS.html`** — 2D polar IFS attractor visualization (greyscale annular rings)
- **`docs/Bloch.html`** — 3D Bloch-sphere spherical visualization of the 16 tiles
- **`docs/`** — Additional interactive HTML demos

## Key idea

Each 2×2 truth table (tile) defines a carry-free bitwise logic that, when iterated to infinite depth, produces a self-similar fractal attractor. Under $H^{\otimes 2}$ conjugation, the diagonal operator $D_f = \operatorname{diag}(f(00), f(01), f(10), f(11))$ becomes a real orthogonal 4×4 matrix $U_f^{(X)}$ — a genuine 2-qubit quantum gate whose generating Hamiltonian is a physical transverse Ising model:

$$U_f^{(X)} = \exp\!\bigl(-i\,(\tfrac{\pi}{2}I - \tfrac{\pi}{2}\sum_{S\neq\emptyset} \hat f(S) X_S)\bigr)$$

## Chain of layers

1. **Boolean** — 16 truth tables
2. **Continuous** — Łukasiewicz (MV-algebra) extension
3. **Complex** — Phase-preserving near-MV-algebra on the disk
4. **Fractal** — IFS attractor (chaos game)
5. **Quantum** — $H^{\otimes2}$-conjugated unitary gates
6. **Temporal** — Depth iteration as discrete time
7. **Many-worlds** — Branching measure interpretation
8. **Multi-qubit** — $n$-register depth process
9. **Physical** — Ising spin Hamiltonians

## Related work

The IFS/liear chaos-game approach to logical systems originates with Grim, Mar, and St. Denis (*The Philosophical Computer*, MIT Press 1998). This project extends their framework to the Bloch sphere, to quantum gate synthesis, and to physical Hamiltonian realizations.

## Blog

Research notes live in [`content/blog/`](./content/blog/) and are published at the
[/blog/](https://pstdenis.github.io/Boolean-Tile/blog/) page.

A local CMS (**BL4@**) runs on port 8746 for writing and editing posts:

```sh
cd blag && npm start
```

Open [http://localhost:8746](http://localhost:8746) in a browser.

## gir

This repo has an in-house AI personality called **gir** (Git Intelligence Reader).
`gir.md` defines its commands and character. If an LLM reads this repo, it should
also read `gir.md` — that file is gir's identity.

Available commands (say in any LLM chat with this context):
- `gir push` — commit and push changes
- `gir talk` — review recent blog posts
- `gir build` — build the Eleventy site
- `gir status` — repo summary
- `gir help` — list commands

## License

All materials are provided for research and educational purposes.
