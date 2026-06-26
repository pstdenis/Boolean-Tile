"""WHFF v0.1 Specification Constants and Data Classes."""

from dataclasses import dataclass
import struct
import zlib

import numpy as np

# File format constants
MAGIC = 0x57484646  # "WHFF" as 32-bit integer
VERSION = 1
HEADER_SIZE = 64
CRC_SIZE = 4

# Mode constants
MODE_TILE_NATIVE = 0
MODE_WALSH_SPECTRAL = 1

# Grid constants
RESOLUTION = 256
LOG2_RES = 8
MAX_DEPTH = 8
N_TILES = 16

# Tile indices (Convention A: 0=False, 1=True)
# Truth tables as 4-element tuples in order: (00, 01, 10, 11)
TILE_NAMES = [
    "0000",       # 0
    "0001",       # 1
    "0010",       # 2
    "0011",       # 3
    "0100",       # 4
    "0101",       # 5
    "0110",       # 6
    "0111",       # 7
    "1000",       # 8
    "1001",       # 9
    "1010",       # 10
    "1011",       # 11
    "1100",       # 12
    "1101",       # 13
    "1110",       # 14
    "1111",       # 15
]

# Truth tables: 0/1 boolean values in (00, 01, 10, 11) order
TRUTH_TABLES: dict[int, tuple[int, int, int, int]] = {
    0:  (0, 0, 0, 0),
    1:  (0, 0, 0, 1),
    2:  (0, 0, 1, 0),
    3:  (0, 0, 1, 1),
    4:  (0, 1, 0, 0),
    5:  (0, 1, 0, 1),
    6:  (0, 1, 1, 0),
    7:  (0, 1, 1, 1),
    8:  (1, 0, 0, 0),
    9:  (1, 0, 0, 1),
    10: (1, 0, 1, 0),
    11: (1, 0, 1, 1),
    12: (1, 1, 0, 0),
    13: (1, 1, 0, 1),
    14: (1, 1, 1, 0),
    15: (1, 1, 1, 1),
}

# Walsh-Hadamard basis H2 (unnormalized, 2x2)
WALSH_BASIS = np.array([[1, 1], [1, -1]], dtype=np.int8)

# 4x4 Walsh basis for spectral mode (reserved)
WALSH_BASIS_4 = np.array([
    [1, 1, 1, 1],
    [1, -1, 1, -1],
    [1, 1, -1, -1],
    [1, -1, -1, 1],
], dtype=np.int8)


def crc32(data: bytes) -> int:
    """Compute CRC32 checksum."""
    return zlib.crc32(data) & 0xFFFFFFFF


HEADER_FORMAT = struct.Struct("<IHHIII")

@dataclass
class WHFFHeader:
    """64-byte WHFF header.

    Layout:
      offset  size  field
      0       4     magic (0x57484646)
      4       2     version
      6       2     mode
      8       4     resolution
      12      4     depth (log2 resolution)
      16      4     payload_size
      20      44    reserved (zero-filled)
    """
    magic: int = MAGIC
    version: int = VERSION
    mode: int = MODE_TILE_NATIVE
    resolution: int = RESOLUTION
    depth: int = LOG2_RES
    payload_size: int = 0

    def to_bytes(self) -> bytes:
        base = HEADER_FORMAT.pack(
            self.magic,
            self.version,
            self.mode,
            self.resolution,
            self.depth,
            self.payload_size,
        )
        return base + b'\x00' * (HEADER_SIZE - len(base))

    @classmethod
    def from_bytes(cls, data: bytes) -> "WHFFHeader":
        if len(data) < HEADER_SIZE:
            msg = f"Data too short: {len(data)} < {HEADER_SIZE}"
            raise ValueError(msg)
        fields = HEADER_FORMAT.unpack(data[:HEADER_FORMAT.size])
        return cls(
            magic=fields[0],
            version=fields[1],
            mode=fields[2],
            resolution=fields[3],
            depth=fields[4],
            payload_size=fields[5],
        )

    def crc32(self) -> int:
        return crc32(self.to_bytes())
