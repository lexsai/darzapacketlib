"""This module contains a class representing an Chat packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class ChatPacket(Packet):
    """Class representing an Chat packet."""

    packet_id = PACKET_NAME_TO_ID['Chat']

    def __init__(self):
        self.text: str = ""
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = ChatPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.text = reader.read_int8_string()

        return packet

    @classmethod
    def from_params(cls, text=""):
        packet = ChatPacket()
        packet.text = text

        writer = StreamWriter()
        writer.write_int8_string(text)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
