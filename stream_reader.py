"""This module contains a reader for streams of binary data."""

import struct

from darzapacketlib.packet_types import Position, Color

class StreamReader:
    """This class represents a reader for streams of binary data."""

    def __init__(self, raw_bytes: bytes):
        self.raw_bytes: bytearray = bytearray(raw_bytes)
        self.reader_index = 0

    def read_bool(self) -> int:
        """Read a byte."""
        data = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        return data == 1

    def read_char(self) -> int:
        """Read a byte."""
        data = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        return data

    def read_int16(self) -> int:
        """Read a 32 bit integer."""
        data = struct.unpack('<h', self.get_reader_bytes(2))[0]
        self.reader_index += 2
        return data

    def read_int(self) -> int:
        """Read a 32 bit integer."""
        data = struct.unpack('<i', self.get_reader_bytes(4))[0]
        self.reader_index += 4
        return data

    def read_float(self) -> float:
        """Read a 32 bit float."""
        data = struct.unpack('<f', self.get_reader_bytes(4))[0]
        self.reader_index += 4
        return data

    def read_int8_string(self) -> str:
        """Read a string with length indicated by a 8 bit integer."""
        data_length = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        data = self.get_reader_bytes(data_length).decode('utf-8')
        self.reader_index += data_length
        return data

    def read_int_string(self) -> str:
        """Read a string with length indicated by a 32 bit integer."""
        data_length = struct.unpack('<i', self.get_reader_bytes(4))[0]
        self.reader_index += 4
        data = self.get_reader_bytes(data_length).decode('utf-8')
        self.reader_index += data_length
        return data

    def read_varint(self) -> int:
        """Read a varint."""
        b = self.get_reader_bytes(1)[0]
        self.reader_index += 1
        flag = (b & 0b01000000) > 0
        b2 = 6
        num = b & 0b00111111
        while (b & 0b10000000) != 0:
            b = self.get_reader_bytes(1)[0]
            self.reader_index += 1
            num |= (b & 0b01111111) << b2
            b2 += 7
        if flag:
            num = -num
        return num

    def read_position(self) -> Position:
        """Read a 2 dimensional vector of two floats."""
        x = struct.unpack('<f', self.get_reader_bytes(4))[0]
        self.reader_index += 4
        y = struct.unpack('<f', self.get_reader_bytes(4))[0]
        self.reader_index += 4
        return Position(x,y)

    def read_color(self) -> Color:
        """Read a color."""
        a = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        if a == 0:
            return Color(0, 255, 255, 255)
        r = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        g = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        b = struct.unpack('B', self.get_reader_bytes(1))[0]
        self.reader_index += 1
        return Color(a,r,g,b)

    def get_reader_bytes(self, size) -> bytes:
        """Get some bytes from the reader byte buffer."""
        return self.raw_bytes[self.reader_index : self.reader_index + size]
