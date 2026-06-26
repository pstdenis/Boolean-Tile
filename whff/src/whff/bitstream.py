"""Bit-level read/write primitives for WHFF bitstream."""


class BitWriter:
    """Write individual bits to a byte buffer."""

    def __init__(self):
        self.buffer = bytearray()
        self._current = 0
        self._bit_pos = 0

    def write_bit(self, bit: int) -> None:
        """Write a single bit (0 or 1)."""
        self._current |= (bit & 1) << self._bit_pos
        self._bit_pos += 1
        if self._bit_pos >= 8:
            self.buffer.append(self._current & 0xFF)
            self._current = 0
            self._bit_pos = 0

    def write_bits(self, value: int, n: int) -> None:
        """Write n bits of value (LSB first)."""
        for _ in range(n):
            self.write_bit(value & 1)
            value >>= 1

    def flush(self) -> None:
        """Flush remaining bits (padded with 0s)."""
        if self._bit_pos > 0:
            self.buffer.append(self._current & 0xFF)
            self._current = 0
            self._bit_pos = 0

    def to_bytes(self) -> bytes:
        """Return complete byte buffer with flushed padding."""
        self.flush()
        return bytes(self.buffer)

    def __len__(self) -> int:
        """Total bits written."""
        return len(self.buffer) * 8 + self._bit_pos


class BitReader:
    """Read individual bits from a byte buffer."""

    def __init__(self, data: bytes):
        self.data = data
        self._byte_pos = 0
        self._bit_pos = 0

    def read_bit(self) -> int:
        """Read a single bit (0 or 1)."""
        if self._byte_pos >= len(self.data):
            raise EOFError("No more bits to read")
        bit = (self.data[self._byte_pos] >> self._bit_pos) & 1
        self._bit_pos += 1
        if self._bit_pos >= 8:
            self._byte_pos += 1
            self._bit_pos = 0
        return bit

    def read_bits(self, n: int) -> int:
        """Read n bits and return as integer (LSB)."""
        value = 0
        for i in range(n):
            value |= self.read_bit() << i
        return value

    def bits_remaining(self) -> int:
        """Number of unread bits."""
        total = len(self.data) * 8
        read = self._byte_pos * 8 + self._bit_pos
        return total - read

    def bytes_consumed(self) -> int:
        """Bytes fully consumed."""
        return self._byte_pos + (1 if self._bit_pos > 0 else 0)