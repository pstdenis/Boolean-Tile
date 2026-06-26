# WHFF — Walsh Holographic File Format v0.1

## One Sentence

WHFF is a **lossless 3D boolean voxel format** that encodes a 256³ binary grid as an octree of 4-bit tile indices, where each tile is one of the 16 possible 2×2 Boolean patterns — the complete Walsh spectrum of two binary variables.

## Design Philosophy

1. **Tiles are atomic.** The 16 Boolean connectives (FALSE, AND, A, B, XOR, OR, NOR, XNOR, NAND, TRUE, …) are not arbitrary patterns — they are the full 2-variable Walsh fragment. A 2×2 block of voxels is always exactly one of these 16 states; no approximation, no quantization.

2. **Lossless by construction.** The format encodes exhaustively: every 2×2 block maps to a unique 4-bit tile index. The decoder reconstructs the identical grid bit-for-bit.

3. **Dual-mode architecture.** v0.1 implements **mode 0 (tile-native)** — a flat 4-bit-per-block bitstream. **Mode 1 (Walsh-spectral)** is reserved for v0.2, which will store Walsh coefficients directly, enabling lossy compression, spectral filtering, and ML integration.

4. **Built for hierarchy.** Morton (Z-order) addressing gives a natural octree structure, extensible to sparse encoding, LOD, and streaming.

## Mathematical Foundation

### The 16 Tiles

For two binary inputs (A, B), there are exactly 16 Boolean functions. Each maps the four input pairs (00, 01, 10, 11) to {0, 1}. These 16 truth tables are the **atomic tiles** of WHFF:

```
Tile   Name     00 01 10 11
  0    FALSE     0  0  0  0
  1    AND       0  0  0  1
  2    A_AND_NOTB 0  0  1  0
  3    A         0  0  1  1
  4    NOTA_AND_B 0  1  0  0
  5    B         0  1  0  1
  6    XOR       0  1  1  0
  7    OR        0  1  1  1
  8    NOR       1  0  0  0
  9    XNOR      1  0  0  1
 10    NOTB      1  0  1  0
 11    B_IMP_A   1  0  1  1
 12    NOTA      1  1  0  0
 13    A_IMP_B   1  1  0  1
 14    NAND      1  1  1  0
 15    TRUE      1  1  1  1
```

### Walsh-Hadamard Transform

Each tile corresponds to a 2×2 block of voxels. The 2×2 Walsh-Hadamard transform (H₂ = [[1,1],[1,-1]]) maps the block to four coefficients (DC, R₀, R₁, R₀R₁). These coefficients live in the **spectral domain** and form the bridge to:

### Bloch Sphere Embedding

The four Walsh coefficients (a, x, y, z) of a tile map to a point (x/a, y/a, z/a) on the Bloch sphere — the state space of a single qubit. The Bures distance between two tiles is the quantum information distance between their Bloch vectors, giving a rigorous geometric structure to the 16-tile set.

## File Format

### Header (64 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 4 | magic | `0x57484646` ("WHFF") |
| 4 | 2 | version | 1 |
| 6 | 2 | mode | 0 = tile-native, 1 = Walsh-spectral |
| 8 | 4 | resolution | grid size per dimension (e.g. 256) |
| 12 | 4 | depth | log₂(resolution) |
| 16 | 4 | payload_size | byte length of payload |
| 20 | 44 | reserved | zero-filled |

### CRC (4 bytes)

CRC32 of the 64-byte header, stored immediately after the header.

### Payload (mode 0)

For each Z-slice (z = 0…resolution-1), for each 2×2 block in Morton order: a **4-bit tile index** (0–15). Total payload = resolution³ / 4 × 4 bits = resolution³ / 8 bytes.

For 256³: 256³ / 8 = 2,097,152 bytes ≈ 2 MB.

## Encoding (mode 0)

1. Partition the 3D grid into 2×2×1 slabs
2. For each slab, find the exact matching tile index (0–15) by comparing its 4 voxels against the 16 truth tables
3. Write the 4-bit index to the bitstream in depth-first Morton order
4. Prepend 64-byte header + 4-byte CRC

## Decoding (mode 0)

1. Read 64-byte header, validate magic and CRC
2. Read 4-bit tile index per block from the bitstream
3. Look up the truth table for each index and place the 4 voxels at the corresponding (x, y, z) positions
4. Return the reconstructed 3D grid

## Status

- **v0.1** (current): mode 0 tile-native encode/decode complete, 56/56 tests passing
- **v0.2** (planned): mode 1 Walsh-spectral encoding, lossy compression, quality metrics
- **Future**: sparse octree, streaming, 5D+temporal extension, Rust port

## Relationship to Other Formats

WHFF is not a competitor to:

| Format | Domain | WHFF difference |
|--------|--------|----------------|
| **OpenEXR** | 2D floating-point images | 3D boolean voxels, lossless |
| **glTF** | Triangle meshes + materials | Voxel grid, not mesh |
| **NeRF** | Continuous neural fields | Discrete, lossless, tile-based |
| **.vox / .binvox** | Voxel grids | WHFF adds Walsh spectral mode, Bloch geometry, tile algebra |
| **Draco** | Mesh compression | Not a mesh format |

WHFF's value is in the **mathematical structure**: the 16-tile Walsh basis, the Bloch sphere embedding, and the future spectral mode for ML-driven compression.
