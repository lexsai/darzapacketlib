"""This module contains a class representing an ActivateObject packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.packet_types import Position
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class ActivateObjectPacket(Packet):
    """Class representing an ActivateObject packet."""

    packet_id = PACKET_NAME_TO_ID['ActivateObject']

    def __init__(self):
        self.object_id: int = 0
        self.value: str = ""
        self.position: Position = (0.0,0.0)
        self.time: int = 0
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = ActivateObjectPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.object_id = reader.read_varint()
        packet.value = reader.read_int_string()
        packet.position = reader.read_position()
        packet.time = reader.read_int()

        return packet

    @classmethod
    def from_params(cls, object_id=0, value="", position: Position=(0.0,0.0), time=0):
        packet = ActivateObjectPacket()
        packet.object_id = object_id
        packet.value = value
        packet.position = position
        packet.time = time

        writer = StreamWriter()
        writer.write_varint(object_id)
        writer.write_int_string(value)
        writer.write_position(position)
        writer.write_int(time)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
