# Łukasiewicz Logic on the Bloch Sphere & Polar Disk

**Date**: 6/13/2026, 12:15:27 AM
**Domain**: stem/mathematics
**Taxonomy**: academic/research_paper
**Filter**: Active comments

---

## Overall Feedback

Here are some overall reactions to the document, focusing on the structural logic and mathematical bridges.

**Łukasiewicz/McNaughton extensions and digitwise evaluation**

Sections 8.2, 12.1, 14, and Open Question 8 treat the digitwise carry-free evaluation as identical to the continuous Łukasiewicz/McNaughton extension of a Boolean connective, arguing that this establishes uniform convergence and graph dimension. There appears to be a structural gap here, as this identification is false in general. For example, evaluating bitwise AND at $\alpha=\beta=.75$ gives $.75$, while Łukasiewicz strong conjunction yields $\max(0, .75 + .75 - 1) = .5$. Similarly, bitwise OR gives $.75$, whereas strong disjunction gives $1$. Because the digitwise construction depends on binary-expansion conventions and inherently contains dyadic discontinuities, it does not independently support the later claims about continuous limits, IFS attractors as graphs of McNaughton functions, or depth-as-time approximations. The manuscript would benefit from cleanly separating the piecewise-linear MV/McNaughton connectives from the digitwise IFS/fractal operations and formally proving any bridge between them.

**Consistency in the near-MV axiom classification**

Section 4 serves as the algebraic spine of the paper, yet there seem to be internal instabilities in the axiom classification. For example, MV6 is marked as proven and Theorem 4.1 lists it as holding, but the accompanying proof states that MV6 is identical to MV4, which fails on $\mathbb{D}$. The failure of MV7 also needs a direct counterexample, since the failure of associativity does not by itself imply the failure of the Łukasiewicz identity. Regarding Theorem 4.2, it successfully shows that argument-preserving projections cannot satisfy MV4, but the subsequent corollary overstates this by claiming any MV4-restoring projection requires collapsing the disk to the real line. Finally, the paragraph after the MV2 proof indicates that the actual IFS primitive is a multi-argument carry-free sum with one final projection, rather than the binary $\oplus$ used to define the near-MV structure. If the primitive is multi-argument, the text needs to clarify how the binary algebra and its MV4 obstruction formally govern the depth process built upon in the rest of the text.

**Coordinate mappings and pole orientations**

There are incompatible maps and orientations between the Polar IFS disk and the Bloch sphere that affect the structure of the quotient cylinder. Section 2.1 uses the stereographic formula $z=e^{i\phi}\tan(\theta_B/2)$ but states the incorrect hemisphere relation for $|z|\le1$. Section 2.3 then shifts to the equal-area map $r=(1+\cos\theta_B)/2$. This conflicts with the statement in Section 2.1 that the truth value is $p=r$, given that Section 2.2 defines $p=(1-\cos\theta_B)/2$, which makes the displayed transform $r=1-p$. Additionally, the pole identifications appear to be reversed: $r=1$ corresponds to $\theta_B=0$ (the North Pole), not the South Pole, and $r=0$ corresponds to $\theta_B=\pi$ (the South Pole), not the North Pole. Because these choices determine which points encode True/False and how negation acts, they are load-bearing structural alignments rather than cosmetic conventions.

**The source of the quantum/Ising correspondence**

The strongest quantum-information result in Section 7 is the standard Walsh–Pauli fact that a $\pm1$-valued Boolean truth table defines a diagonal $D_f$, and $H^{\otimes n}$ conjugation expands it in the $\{I,X\}^{\otimes n}$ basis. Readers will note that this construction does not actually rely on the disk operation, radial projection, or the failure of MV4. As a result, the claims in Sections 4.2, 9, 13, and 14 that the MV4 failure "enables" entangling gates, nonzero Ising coupling, the tensor hierarchy, or the quantum regime currently remain unproved. The entangling terms specifically emerge from the non-monomial Walsh support of the Boolean function. Furthermore, Section 13 requires tighter discipline regarding signs and global phases: using $H_f=(\pi/2)(I-U_f)$, the non-identity Pauli coefficients take on the opposite sign to those in the Section 13.4 formula. The treatment of the identity/global phase term also appears internally inconsistent across Claim 13.1, Claim 13.2, and the TRUE row of the parameter table.

**Defining the infinite-depth limit**

Section 12.4 asserts that $\lim_{d\to\infty}|\psi_d\rangle\langle\psi_d|$ characterizes "the branching measure over all tent-map orbits." However, this sequence exists in Hilbert spaces whose dimensions continuously grow with $d$, and the text does not specify the required embedding, topology, or mode of convergence. A finite-depth register state cannot be said to converge to a classical orbit measure without explicitly defining the limiting construction—whether this entails weak-* convergence of induced measures, convergence of cylinder distributions, or an inductive-limit Hilbert-space construction. Because Sections 11.4, 11.7, 12.6, and 14 promote the finite-depth IFS state into a universal-wavefunction or many-worlds branching object based on this limit, formalizing the mathematics of this sequence is essential for the later claims to hold up algebraically.

**The Bures metric calculation**

Section 15.1 claims that the qubit Bures metric $ds^2=dr^2/(1-r^2)+r^2d\Omega^2$ is hyperbolic $H^3$, with the Bloch sphere as its conformal boundary. Mathematically, with the substitution $r=\sin\chi$, this metric is (up to conventional scaling) the round three-sphere/hemisphere metric, meaning the pure-state boundary resides at a finite distance. The substitution $r=\tanh\rho$ does not output $d\rho^2+\sinh^2\rho\,d\Omega^2$. Because this core calculation does not produce a hyperbolic geometry, Theorem 15.1, the RT-style Theorem 15.2, the boundary-CFT claims, and the synthesis claim in Section 14 that "the Bures metric is $H^3$" cannot formally stand as theorems. The manuscript would be much stronger if this section either adopted the correctly specified information-geometric metric or was recast explicitly as a speculative analogy rather than a mathematical proof.

**Status**: [Pending]

---

## Detailed Comments (7)

### 1. Radial Bures distance in Section 15.2 conflicts with the metric

**Status**: [Pending]

**Quote**:
> Consider the reduced density matrix \$\\rho_i = \\operatorname{Tr}\_{j\\neq i}\|\\psi_d\\rangle\\langle\\psi_d\|\$ of a single qubit register. Its Bloch vector has radial coordinate \$r(d) = 1 - O(2\^{-d})\$ for entangling gates (the purity approaches 1 as depth increases because more of the branch space is resolved). The Bures distance from the center to this state is:

\$\$ \\rho(d) = \\operatorname{arctanh}\\, r(d) \\sim d\\cdot\\frac{\\log 2}{2} + O(1) \$\$

**Feedback**:
The radial distance used in Section 15.2 is inconsistent with the metric stated in Theorem 15.1. For $ds_B^2=dr^2/(1-r^2)+r^2d\Omega^2$, a radial path has length $\int_0^r ds/\sqrt{1-s^2}=\arcsin r$, not $\operatorname{arctanh} r$. Consequently the boundary is at finite radial distance for the displayed metric, and the claimed scaling $\rho(d)\sim d\log 2/2$ does not follow from it.

---

### 2. Equivalence calculation conflicts with negation in sec3-4

**Status**: [Pending]

**Quote**:
> | System           | Formula                                                                                                                  |
|------------------|--------------------------------------------------------------------------------------------------------------------------|
| Convention A     | \$x\\leftrightarrow y = 1 - \|x-y\|\$                                                                                    |
| \$\[0,1\]\$ form | \$p\\leftrightarrow q = 1 - \|p - q\|\$                                                                                  |
| Polar IFS disk   | \$z\\leftrightarrow w = \\operatorname{proj}\_{\\mathbb{D}}(1 - \|z - w\|)\$                                             |
| Bloch sphere     | \$(\\theta_B,\\phi) \\leftrightarrow (\\theta\'\_B,\\phi\') = 1 - \|\\cos\\theta_B - \\cos\\theta\'\_B\|\$ (up to phase) |

**Critical observation:** On the boundary \$\|z\|=1\$, \$\|z-\\neg z\| = \|e\^{i\\theta} + e\^{-i\\theta}\| = 2\|\\cos\\theta\|\$, so \$z\\leftrightarrow\\neg z = 1 - 2\|\\cos\\theta\|\$

**Feedback**:
The equivalence section contains two related inconsistencies. Under Convention A, transporting the usual $[0,1]$ equivalence $1-|p-q|$ to $[-1,1]$ gives $|x-y|-1$, not $1-|x-y|$. Also, the boundary calculation does not use the defined disk negation: with $\neg z=-z$, $z=e^{i\theta}$ gives $z-\neg z=2e^{i\theta}$ and $|z-\neg z|=2$, not $|e^{i\theta}+e^{-i\theta}|=2|\cos\theta|$.

---

### 3. RT normalization and $C_{ij}$ mapping in Theorem 15.2

**Status**: [Pending]

**Quote**:
> The coefficient \$C\_{ij}\$ in Theorem 12.4 thus corresponds to the **angular separation on \$S\^2\$** between the two boundary points: \$C\_{ij} \\propto 1/\\log\\sin(\\Delta\\theta\_{ij}/2)\$. More precisely, the Walsh spectrum of the Boolean function \$f\$ determines the effective angular separation between the two registers in the boundary CFT, and the entanglement growth rate \$C\_{ij}\$ is the holographic dual of the boundary operator's conformal dimension.

::: theorem
**Theorem 15.2 (Ryu-Takayanagi form of entanglement growth).** For the \$n\$-qubit IFS depth process with non-constant Boolean function \$f\$, the mutual information between any two input registers \$i,j\$ at depth \$d\$ equals (up to an additive constant) the length of a geodesic in \$H\^3\$ anchored to the boundary points defined by the Walsh spectrum of \$f\$:

\$\$ I(\\alpha_i:\\alpha_j\\,\|\\,\\psi_d) = \\frac{c}{3} \\cdot L\_{\\text{geo}}(\\rho(d), \\Delta\\theta\_{ij}) \$\$

where \$c = 3C\_{ij}/(2\\log 2)\$ is the effective central charge of the boundary CFT, and \$\\Delta\\theta\_{ij}\$ is determined by \$\\hat f(S)\$. For \$d \\gg 1\$ with \$r(d) \to 1\$, \$L\_{\\text{geo}} \\sim 2\\rho(d)\$ and the linear scaling \$I = d \\cdot C\_{ij} + O(1)\$ is recovered.

**Feedback**:
The quantitative dictionary in Theorem 15.2 is not internally consistent. Substituting the paper’s formulas $\rho(d)\sim d\log2/2$, $L_{\mathrm{geo}}\sim2\rho(d)$, and $c=3C_{ij}/(2\log2)$ gives $(c/3)L_{\mathrm{geo}}\sim dC_{ij}/2$, not $dC_{ij}$. Also, in the displayed geodesic formula the angular separation contributes only an additive $O(1)$ term at large $d$, so it cannot by itself encode the leading slope $C_{ij}$; the stated proportionality $C_{ij}\propto1/\log\sin(\Delta\theta_{ij}/2)$ also has sign and singularity problems for ordinary angular separations.

---

### 4. Pole assignment is reversed in sec2-3

**Status**: [Pending]

**Quote**:
> The relationship between the Polar IFS coordinates \$(r,\\theta)\$ and Bloch sphere coordinates \$(\\theta_B,\\phi)\$ is a **cylindrical equal-area projection**:

\$\$ r = \\frac{1 + \\cos\\theta_B}{2} = 1 - p, \\qquad \\theta = \\phi \$\$

Or equivalently:

\$\$ \\cos\\theta_B = 2r - 1, \\qquad \\phi = \\theta \$\$

Under this map:

-   The Polar IFS cone (P identity) becomes the north-south axis of the Bloch sphere
-   The Polar IFS helix (Q identity) becomes the equatorial phase winding of the Bloch sphere
-   The outer boundary \$r=1\$ maps to the South Pole (True)
-   The origin \$r=0\$ maps to the North Pole (False)

**Feedback**:
The endpoint identification in Section 2.3 is internally inconsistent. The displayed map $r=(1+\cos\theta_B)/2$ gives $r=1$ at $\theta_B=0$ (North Pole, $p=0$, False) and $r=0$ at $\theta_B=\pi$ (South Pole, $p=1$, True), while the bullets and proof state the opposite. This also needs to be reconciled with the earlier statement that the Polar IFS truth value is $p=r$.

---

### 5. MV6 status contradicts MV4 in sec4

**Status**: [Pending]

**Quote**:
> | **(MV4) Annihilation**  | \$z\\oplus 1 = 1\$                                                      | [Fails]{.status-badge .status-unverified} | \$z=i\$ counterexample (\\S4.1 proof); see \\S4.2 for the implications of this failure                                                                                                                                                                   |
| **(MV5) Involution**    | \$\\neg\\neg z = z\$                                                    | [Proven]{.status-badge .status-proven}    | \$\\neg\\neg z = -(-z) = z\$                                                                                                                                                                                                                             |
| **(MV6) Boundary**      | \$z\\oplus \\neg 0 = \\neg 0\$                                          | [Proven]{.status-badge .status-proven}    | Under the MV-algebra axioms, \$\\neg 0 = 1\$ (the top element), so MV6 (\$x\\oplus\\neg0 = \\neg0\$) is identical to MV4 (\$x\\oplus 1 = 1\$). Whether MV6 holds therefore matches MV4\'s status: it holds on \$\[-1,1\]\$ and fails on \$\\mathbb{D}\$. |

**Feedback**:
The MV6 row is internally inconsistent. Since $0=+1$ and $\neg 0=-1=1$ in the disk structure, MV6 $z\oplus\neg 0=\neg 0$ is the same identity as MV4 $z\oplus 1=1$. The row itself says this identity fails on $\mathbb{D}$, so MV6 should not simultaneously be marked or summarized as proven for the disk.

---

### 6. Hyperbolic sphere area asymptotic in Section 15.2

**Status**: [Pending]

**Quote**:
> The area of a 2-sphere at this radial distance in \$H\^3\$ is:

\$\$ A(d) = 4\\pi \\sinh\^2\\rho(d) \\sim \\pi\\,e\^{\\rho(d)} \\quad\\text{(for large \$d\$)} \$\$

For early depths (small \$\\rho\$), \$\\sinh\^2\\rho \\approx \\rho\^2\$, giving \$A(d) \\sim \\rho(d)\^2 \\sim d\^2\$. However, the mutual information \$I(\\alpha_i:\\alpha_j) = d \\cdot C\_{ij} + O(1)\$ is linear, not quadratic.

**Feedback**:
The large-$\rho$ asymptotic for the displayed hyperbolic sphere area is incorrect: $4\pi\sinh^2\rho\sim \pi e^{2\rho}$, not $\pi e^{\rho}$. Although the text then shifts from sphere area to geodesic length, this error and the later wording about an area scaling as $d$ make the intended RT-like scaling dictionary ambiguous.

---

### 7. MV7 failure is not proved in sec4

**Status**: [Pending]

**Quote**:
> ::: proof
**Proof (MV7 failure).** Since MV7 = \$\\neg(\\neg z\\oplus w)\\oplus w = \\neg(\\neg w\\oplus z)\\oplus z\$ is the Łukasiewicz axiom that ensures the lattice structure (the existence of \$\\max\$ and \$\\min\$ as derived operations), and its proof in standard MV-algebras depends on associativity, the failure of MV2 on \$\\mathbb{D}\$ implies MV7 also fails. The counterexample above for MV2 can be adapted to MV7 directly. ✓
:::

**Feedback**:
The MV7 failure may be true, but the proof as written does not establish it. Failure of associativity does not by itself imply failure of the separate MV7 identity; the section should give an explicit MV7 counterexample or a derivation showing that MV7 would force one of the already-failed identities in this disk structure.

---
