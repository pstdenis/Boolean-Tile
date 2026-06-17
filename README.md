# Boolean Tile Basis

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

## License

All materials are provided for research and educational purposes.
