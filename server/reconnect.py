"""This module contains a class representing an Reconnect packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class ReconnectPacket(Packet):
    """Class representing an Reconnect packet."""

    packet_id = PACKET_NAME_TO_ID['Reconnect']

    def __init__(self):
        self.host: str = ''
        self.port: int = 0
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = ReconnectPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.host = reader.read_int_string()
        packet.port = reader.read_varint()

        return packet

    @classmethod
    def from_params(cls, host='', port=0):
        packet = ReconnectPacket()
        packet.host = host
        packet.port = port

        writer = StreamWriter()
        writer.write_int_string(host)
        writer.write_varint(port)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
