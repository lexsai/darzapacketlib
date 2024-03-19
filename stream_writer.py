"""This module contains a writer for streams of binary data."""

import struct

from darzapacketlib.packet_types import Position, Color

class StreamWriter:
    """This class represents a writer for streams of binary data."""

    def __init__(self):
        self.raw_bytes: bytearray = bytearray()

    def write_byte(self, data: int):
        """Write a byte."""
        self.raw_bytes.extend(struct.pack('B', data))

    def write_int(self, data: int):
        """Write a 32 bit integer."""
        self.raw_bytes.extend(struct.pack('<i', data))

    def write_int16(self, data: int):
        """Write a 32 bit integer."""
        self.raw_bytes.extend(struct.pack('<h', data))

    def write_int8_string(self, data: str):
        """Write a string with length indicated by a 8 bit integer."""
        data_bytes = bytes(data, 'utf-8')
        self.write_byte(len(data_bytes))
        self.write_data(data_bytes)

    def write_int_string(self, data: str):
        """Write a string with length indicated by a 32 bit integer."""
        data_bytes = bytes(data, 'utf-8')
        self.write_int(len(data_bytes))
        self.write_data(data_bytes)

    def write_float(self, data: float):
        """Write a 32 bit integer."""
        self.raw_bytes.extend(struct.pack('<f', data))

    def write_varint(self, data: int):
        """Write a varint."""
        num = abs(data)
        b = num & 0b00111111
        if data < 0:
            b |= 0b01000000
        num >>= 6
        flag = num > 0
        if flag:
            b |= 0b10000000
        self.write_byte(b)
        while flag:
            b = num & 0b01111111
            num >>= 7
            flag = num > 0
            if flag:
                b |= 128
            self.write_byte(b)

    def write_position(self, data: Position):
        """Write a 2 dimensional vector of two floats."""
        self.write_float(data[0])
        self.write_float(data[1])

    def write_color(self, data: Color):
        """Write a color."""
        self.write_byte(data.a)
        if data.a == 0:
            return
        self.write_byte(data.r)
        self.write_byte(data.g)
        self.write_byte(data.b)

    def write_data(self, data: bytes):
        """Write some given bytes of data into the stream."""
        self.raw_bytes.extend(data)
