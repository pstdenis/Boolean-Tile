"""Tests for the WHFF spec module."""

import pytest

from whff.spec import (MAGIC, VERSION, HEADER_SIZE, MODE_TILE_NATIVE,
                       MODE_WALSH_SPECTRAL, RESOLUTION, N_TILES,
                       TILE_NAMES, TRUTH_TABLES, WALSH_BASIS, WHFFHeader)


def test_constants():
    assert MAGIC == 0x57484646
    assert VERSION == 1
    assert HEADER_SIZE == 64
    assert MODE_TILE_NATIVE == 0
    assert MODE_WALSH_SPECTRAL == 1
    assert RESOLUTION == 256
    assert N_TILES == 16


def test_tile_names():
    assert len(TILE_NAMES) == 16
    assert TILE_NAMES[0] == "0000"
    assert TILE_NAMES[15] == "1111"


def test_truth_tables():
    assert len(TRUTH_TABLES) == 16
    assert TRUTH_TABLES[0] == (0, 0, 0, 0)
    assert TRUTH_TABLES[15] == (1, 1, 1, 1)


def test_walsh_basis():
    assert WALSH_BASIS.shape == (2, 2)
    assert WALSH_BASIS[0, 0] == 1
    assert WALSH_BASIS[0, 1] == 1
    assert WALSH_BASIS[1, 0] == 1
    assert WALSH_BASIS[1, 1] == -1


def test_header_roundtrip():
    header = WHFFHeader(
        magic=MAGIC,
        version=VERSION,
        mode=MODE_TILE_NATIVE,
        resolution=RESOLUTION,
        depth=8,
        payload_size=1024,
    )
    data = header.to_bytes()
    assert len(data) == HEADER_SIZE
    header2 = WHFFHeader.from_bytes(data)
    assert header2.magic == MAGIC
    assert header2.version == VERSION
    assert header2.mode == MODE_TILE_NATIVE
    assert header2.resolution == RESOLUTION
    assert header2.depth == 8
    assert header2.payload_size == 1024


def test_header_crc():
    header = WHFFHeader(
        magic=MAGIC,
        version=VERSION,
        mode=MODE_TILE_NATIVE,
        resolution=RESOLUTION,
        depth=8,
        payload_size=0,
    )
    crc = header.crc32()
    assert 0 <= crc <= 0xFFFFFFFF
    # CRC should be deterministic
    assert header.crc32() == crc


def test_header_defaults():
    header = WHFFHeader()
    assert header.magic == MAGIC
    assert header.version == VERSION
    assert header.mode == MODE_TILE_NATIVE
    assert header.resolution == 256
    assert header.depth == 8
    assert header.payload_size == 0


@pytest.mark.parametrize("mode", [MODE_TILE_NATIVE, MODE_WALSH_SPECTRAL])
def test_header_modes(mode):
    header = WHFFHeader(mode=mode)
    data = header.to_bytes()
    header2 = WHFFHeader.from_bytes(data)
    assert header2.mode == mode
