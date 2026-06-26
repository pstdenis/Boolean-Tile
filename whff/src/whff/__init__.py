"""WHFF - Walsh Holographic File Format v0.1."""

from whff.spec import (MAGIC, VERSION, HEADER_SIZE, MODE_TILE_NATIVE,
                       MODE_WALSH_SPECTRAL, RESOLUTION, N_TILES,
                       TILE_NAMES, TRUTH_TABLES, WALSH_BASIS, WHFFHeader)
from whff.bitstream import BitReader, BitWriter
from whff.tiles import (project_tile, walsh_transform, walsh_coefficients,
                        bloch_vector, bures_distance, tile_color,
                        tile_bloch_coords, tile_to_array)
from whff.addressing import (morton_encode, morton_decode,
                             coordinate_to_morton, morton_to_coordinate,
                             grid_to_mortons, morton_to_grid)
from whff.encoder import encode
from whff.decoder import decode

__all__ = [
    "MAGIC", "VERSION", "HEADER_SIZE", "MODE_TILE_NATIVE",
    "MODE_WALSH_SPECTRAL", "RESOLUTION", "N_TILES",
    "TILE_NAMES", "TRUTH_TABLES", "WALSH_BASIS", "WHFFHeader",
    "BitReader", "BitWriter",
    "project_tile", "walsh_transform", "walsh_coefficients",
    "bloch_vector", "bures_distance", "tile_color",
    "tile_bloch_coords", "tile_to_array",
    "morton_encode", "morton_decode", "coordinate_to_morton",
    "morton_to_coordinate", "grid_to_mortons", "morton_to_grid",
    "encode", "decode",
]

__version__ = "0.1.0"
