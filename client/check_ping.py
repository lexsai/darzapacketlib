"""This module contains a class representing an CheckPing packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class CheckPingPacket(Packet):
    """Class representing an CheckPing packet."""

    packet_id = PACKET_NAME_TO_ID['CheckPing']

    def __init__(self):
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = CheckPingPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        return packet

    @classmethod
    def from_params(cls):
        packet = CheckPingPacket()

        writer = StreamWriter()
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
