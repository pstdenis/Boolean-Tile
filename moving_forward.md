# Moving Forward: From Single Connective to Quantum Circuit

## Status

The system has three verified layers (from `Complex Łukasiewicz Algebra on the Unit Disk.html`):

1. **16 Tiles → 4×4 unitaries** (§7): Each Boolean operator maps to a gate under H^⊗² conjugation. XOR → X⊗X, AND → entangling, etc. Verified.
2. **Tensor hierarchy** (§9): The 2-qubit gates embed in SU(2ⁿ) for n variables. The n-variable parity maps to X^⊗ⁿ (Thm 7.1). Verified.
3. **MV4 boundary** (§4.1): The real axis is the classical MV-sublogic; the disk is the quantum extension where MV4 fails — this failure is the algebraic phase transition, not a defect.

The IFS (`native_spherical_chaos.html`) is a **single-connective calibration tool** — it visualizes the attractor of one operator on one Bloch ball. It does not compose.

## The Gap

No mechanism to take a **compound sentence** like XOR(AND(a,b), OR(c,d)) and:
- Map it to a multi-qubit circuit
- Apply the unitaries from the gate table
- Extract Born-rule probabilities

## Plan

### Phase 1: Circuit Runner (core engine)

Build a `sentence_to_circuit` module that:

1. **Parses** a compound sentence into an AST with variables, connectives (tile indices)
2. **Allocates** one qubit per distinct variable, plus ancillas as needed
3. **Maps** each connective node to its 4×4 unitary from the gate table (§7)
4. **Composes** the unitaries via tensor product and matrix multiply on the full n-qubit state vector
5. **Evaluates** starting from |0...0⟩, outputs the final state vector and Born probabilities

Example:
```
XOR(AND(a,b), OR(c,d))  →  4 vars → 4 qubits
                             AND(a,b) → U₁ applied to qubits 0,1
                             OR(c,d)  → U₂ applied to qubits 2,3
                             XOR(U₁_out, U₂_out) → U₃ applied to qubits (0,1,2,3 via SWAP/embedding)
```

### Phase 2: Visualization

Extend `native_spherical_chaos.html` or build a new viewer that:

1. **Input**: compound sentence + variable truth-value assignments
2. **Output**: a Bloch ball for each qubit, with the state vector plotted as a point (pure) or ball (mixed)
3. **Overlay**: the attractor from the IFS for each connective used
4. **Interference toggle**: show how the Born probabilities change when phases are rotated

### Phase 3: Verification

- Cross-check against known quantum circuits (Bell state, GHZ, Deutsch-Jozsa)
- Verify that `XOR(a,b)` on 2 qubits gives the same distribution as `a XOR b` classically
- Verify that `AND(a,b)` on 2 qubits gives entanglement that cannot be simulated classically
- Test the MV4 boundary: circuits that stay on the real axis should reproduce classical Łukasiewicz results; circuits with phases should diverge

### Non-Goals

- No rewrite of the IFS — it stays as the single-connective calibration tool
- No new algebraic framework — the unitaries in §7 are sufficient
- No full quantum computer simulator — just the 16 tiles and their compositions

## Concrete Next Step

Write `circuit_runner.js`: a module that takes a compound sentence string, parses it, maps each connective to its §7 unitary, and computes the n-qubit state vector. Start with 2-variable sentences to verify against the IFS, then extend to n variables.
