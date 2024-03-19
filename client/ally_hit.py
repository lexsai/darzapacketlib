"""This module contains a class representing an AllyHit packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class AllyHitPacket(Packet):
    """Class representing an AllyHit packet."""

    packet_id = PACKET_NAME_TO_ID['AllyHit']

    def __init__(self):
        self.time: int = 0
        self.projectile_id: int = 0
        self.object_id: int = 0
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = AllyHitPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.time = reader.read_varint()
        packet.projectile_id = reader.read_varint()
        packet.object_id = reader.read_varint()

        return packet

    @classmethod
    def from_params(cls, time=0, projectile_id=0, object_id=0):
        packet = AllyHitPacket()
        packet.time = time
        packet.projectile_id = projectile_id
        packet.object_id = object_id

        writer = StreamWriter()
        writer.write_varint(time)
        writer.write_varint(projectile_id)
        writer.write_varint(object_id)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
