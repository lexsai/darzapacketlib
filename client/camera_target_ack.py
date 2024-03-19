"""This module contains a class representing an CameraTargetAck packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class CameraTargetAckPacket(Packet):
    """Class representing an CameraTargetAck packet."""

    packet_id = PACKET_NAME_TO_ID['CameraTargetAck']

    def __init__(self):
        self.client_time: int = 0
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = CameraTargetAckPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.client_time = reader.read_int()

        return packet

    @classmethod
    def from_params(cls, client_time=0):
        packet = CameraTargetAckPacket()
        packet.client_time = client_time

        writer = StreamWriter()
        writer.write_int(client_time)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
