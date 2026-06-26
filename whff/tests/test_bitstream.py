"""Tests for the WHFF bitstream module."""

import pytest
from hypothesis import given, strategies as st

from whff.bitstream import BitReader, BitWriter


@given(st.lists(st.integers(min_value=0, max_value=1), max_size=1000))
def test_bit_write_read_roundtrip(bits):
    writer = BitWriter()
    for b in bits:
        writer.write_bit(b)
    data = writer.to_bytes()
    reader = BitReader(data)
    for b in bits:
        assert reader.read_bit() == b


@given(st.integers(min_value=0, max_value=2**16 - 1),
       st.integers(min_value=1, max_value=16))
def test_bits_write_read_roundtrip(value, n):
    max_val = 2**n - 1
    value = value & max_val
    writer = BitWriter()
    writer.write_bits(value, n)
    data = writer.to_bytes()
    reader = BitReader(data)
    result = reader.read_bits(n)
    assert result == value


@pytest.mark.parametrize("value,n,expected_bytes", [
    (0, 1, b'\x00'),
    (1, 1, b'\x01'),
    (5, 3, b'\x05'),
    (0xFF, 8, b'\xFF'),
    (0xFFFF, 16, b'\xFF\xFF'),
])
def test_bit_writer_known_values(value, n, expected_bytes):
    writer = BitWriter()
    writer.write_bits(value, n)
    assert writer.to_bytes() == expected_bytes


def test_bit_reader_eof():
    writer = BitWriter()
    writer.write_bits(42, 8)
    data = writer.to_bytes()
    reader = BitReader(data)
    reader.read_bits(8)
    with pytest.raises(EOFError):
        reader.read_bit()


def test_bit_reader_bytes_consumed():
    writer = BitWriter()
    writer.write_bits(0xABCD, 16)
    data = writer.to_bytes()
    assert len(data) == 2
    reader = BitReader(data)
    assert reader.bytes_consumed() == 0
    reader.read_bits(8)
    assert reader.bytes_consumed() == 1
    reader.read_bits(8)
    assert reader.bytes_consumed() == 2
