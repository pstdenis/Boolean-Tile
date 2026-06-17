# Abstract: From Boolean Tiles to Ising Hamiltonians

Paul St. Denis — June 2026

## Overview

The 16 Boolean truth tables of two variables (the "tiles") are shown to generate a single mathematical structure that manifests in ten progressively richer layers — from discrete logic to continuous Łukasiewicz connectives, complex-valued near-MV-algebra, fractal IFS attractors, quantum unitary gates, many-worlds branching, multi-qubit entanglement dynamics, physical Ising Hamiltonians, and finally an emergent holographic bulk geometry in $H^3$ whose boundary is the Bloch sphere $S^2$. The chain is homomorphic: each layer preserves the structure of the layer below while adding new degrees of freedom.

## The Central Claim

The chain is held together by a single algebraic event: the **failure of MV4** (annihilation: $x\oplus 1 = 1$) when the real Łukasiewicz operations are extended to the complex unit disk. The real projection $x\mapsto \operatorname{sgn}(x)$ discards directional information; the complex radial projection $\operatorname{proj}_{\mathbb{D}}(w) = w/\max(1,|w|)$ preserves the argument of the overflow. Within this framework, this phase-preserving projection is the algebraic event from which the remaining layers unfold. Without it, the chain collapses to the real line — no phase, no Bloch ball, no gates, no holography.

## The 10-Layer Chain

| Layer | Domain | Key structure |
|---|---|---|
| 1. **Boolean** | $\{0,1\}^2$ | 16 truth tables |
| 2. **Logical** | $[0,1]^2$ | Carry-free IFS evaluation → McNaughton functions |
| 3. **Geometric** | $\mathbb{D}$ | Complex extension, MV4 fails, phase-preserving projection |
| 4. **Fractal** | $S^2$ | Chaos game attractor, Walsh spectrum → visual geometry |
| 5. **Quantum** | $U(4)$ | $H^{\otimes 2}$ conjugation, 16 unitary gates |
| 6. **Temporal** | $\mathbb{R}$ | IFS depth = discrete time, tent map, Bernoulli shift |
| 7. **Many-worlds** | Everett tree | IFS paths as branches, unitary as world-coupler |
| 8. **Multi-qubit** | $(\mathbb{C}^2)^{\otimes n}$ | Joint IFS depth process, entanglement from Walsh spectrum |
| 9. **Physical** | Ising model | $H_f = J\,ZZ + h_1 ZI + h_2 IZ$, parameters from Walsh coefficients |
| 10. **Holographic** | $H^3 / S^2$ | Bures metric = $H^3$, Bloch sphere = conformal boundary, RT-like area from entanglement growth |
| 11. **Relational** | $(\mathbb{N})^n$ | Per-qubit depths $d_i$, chaotic liar as internal clock, Page-Wootters mechanism, causal structure from common resolved depth |
| Extension | Clifford hierarchy | $\{\pm1\}$ diagonals + $H^{\otimes n}$ → 16 symmetric gates; $\{\pm1\}$ diagonals + selective $H_S$ → full Clifford group (CNOT, Toffoli); $U(1)$ diagonals + selective $H_S$ → full Clifford hierarchy ($T$, $V$, etc.) |

## Key Results

1. **All 16 tiles generate 2-qubit unitaries** under $H^{\otimes 2} D_f H^{\otimes 2}$, where $D_f$ is the diagonal ±1 matrix encoding the truth table. The 8 monomials give pure tensor products $\pm A\otimes B$ ($A,B\in\{I,X\}$). The 8 entangling gates are superpositions requiring all three Ising couplings simultaneously.

2. **Every tile corresponds to an Ising Hamiltonian** $H_f = J\cdot ZZ + h_1\cdot ZI + h_2\cdot IZ$ with parameters $(J, h_1, h_2) = (\pi/2)\cdot(\hat f(\{1,2\}), \hat f(\{1\}), \hat f(\{2\}))$, where $\hat f(S)$ are the Walsh-Hadamard coefficients of $f$. The 8 monomials have exactly one non-zero parameter; the 8 entangling gates have all three non-zero at magnitude $\pi/4$.

3. **The carry-free IFS evaluation IS the commuting $X$-basis dynamics** of the Ising model. Each depth level reveals one bit per input; the gate network processes all bit-positions in parallel because the $\{I, X\}^{\otimes n}$ Hamiltonian terms commute.

4. **Selective Hadamard conjugation** (applying $H$ to a subset of qubits instead of uniformly to all) extends the symmetric 16 gates to the full Clifford hierarchy. Toffoli = $f = \text{AND}_3$, $S = \{\text{target}\}$: a 3-input AND seed conjugated by $H$ on the target qubit only. The diagonal seed encodes the Boolean condition; the subset $S$ selects which qubits are targets ($X$-basis, quantum) vs controls ($Z$-basis, classical).

5. **The Bloch ball forms a Rational MV-algebra** (RMV-algebra) under the midpoint operation $\delta_2(\rho_1,\rho_2) = (\rho_1+\rho_2)/2$, with negation as central inversion. The non-simplex geometry (non-unique decomposition of mixed states into pure states) is the geometric expression of the MV4 failure — the interior of the Bloch ball is exactly where MV4 is active and the classical MV-algebra must give way to the Rational Łukasiewicz structure.

6. **Associativity (MV2) fails on the disk** (proved by counterexample), and MV7 fails as a consequence. The failure is generic: the radial projection $\operatorname{proj}_{\mathbb{D}}$ does not distribute over nested addition. However, the IFS depth process uses a single multi-argument accumulation (not binary composition), so the binary non-associativity does not affect the well-definedness of the system.

7. **Phase-collapse obstruction (Theorem 4.2).** Any argument-preserving projection $p: \mathbb{C} \to \mathbb{D}$ that is the identity on $\mathbb{D}$ necessarily violates MV4. The radial projection $\operatorname{proj}_{\mathbb{D}}(z) = z/\max(1,|z|)$ used throughout this paper is one such. Restoring MV4 requires discarding the phase, collapsing the disk to $[-1,1]$. This proves that preserving phase and preserving full MV-structure are incompatible.

8. **The discrete-to-continuous time convergence is formally proved**: the $d$-bit IFS approximations $U_f^{(d)}$ converge uniformly to the continuous Hamiltonian geodesic $U_f(t) = e^{-iH_f t}$ at rate $O(2^{-d})$, with $t_d = 1-2^{-d}$ as the natural time parameter.

9. **The Bures metric on the Bloch ball is $H^3$** (hyperbolic 3-ball, Theorem 15.1). The Bloch sphere $S^2$ is its conformal boundary. The purity $r$ is the radial holographic coordinate. This is an exact mathematical isometry — the Bloch ball with its quantum Fisher information metric *is* the hyperbolic space $EAdS_3$.

10. **Entanglement entropy takes Ryu-Takayanagi form** (Theorem 15.2). The mutual information $I(\alpha_i:\alpha_j\,|\,\psi_d) = d \cdot C_{ij} + O(1)$ equals a geodesic length in $H^3$, with the Walsh correlation coefficient $C_{ij}$ determining the angular separation on the boundary. The IFS depth process is a tensor network whose continuum limit is $H^3$.

11. **Decoherence bounds the maximum useful depth** to $d_{\max} \sim T_2/(\tau_g \cdot \operatorname{size}(f))$ for physical qubits, but does not alter the predicted entanglement structure within the coherent regime.

12. **Topological note.** The map from the Polar IFS cylinder $[0,1]\times S^1$ to the Bloch sphere $S^2$ induces a homeomorphism only after collapsing the boundary circles $r=0$ and $r=1$ to points (North and South Poles). The corrected statement: $([0,1]\times S^1/\!\sim) \cong S^2$.

13. **Relational time (proposal).** The single global depth $d$ can be generalized to per-qubit proper depths $d_i$, with the chaotic liar (P↔¬P) serving as the internal clock (Page-Wootters mechanism). The joint state depends on $\min(d_i)$ for common causal structure. The selective Hadamard switching is determined by the compound sentence's three-domain embedding, not by external control. (§13.7, §15.5)

## The Three-Sentence Summary

**Boolean logic, continuously extended, produces the Łukasiewicz connectives. Allowing the phase to survive the projection produces the near-MV-algebra on the disk. $H^{\otimes 2}$ conjugation shows this disk is the Bloch ball of a 2-qubit quantum system whose generating Hamiltonian is a physical Ising model — the three parameters of a 2-spin system encode the 16 Boolean functions of 2 variables, and the 16 tiles are the full set of possible 2-qubit Ising gates of the form $\exp(-it(J\,ZZ + h_1 ZI + h_2 IZ))$ at the special time $t=1$. The Bures metric on this Bloch ball is $H^3$; the Bloch sphere $S^2$ is its conformal boundary; the entanglement growth $S(d) = d \cdot C_{ij}$ is a Ryu-Takayanagi area formula derived from logic — the chain completes in an emergent holographic bulk geometry built from Boolean truth tables.**

## Files

- `Complex Łukasiewicz Algebra on the Unit Disk.html` — Complete specification (14 sections, 1200+ lines)
- `native_spherical_chaos.html` — IFS chaos game visualization (classical calibration)
- `quantum_bloch.html` — Quantum Bloch vector visualization (purity-colored)
- `circuit_runner.html` — Standalone circuit evaluator for compound sentences
- `many_worlds_framing.html` — Standalone essay on the Everett interpretation
