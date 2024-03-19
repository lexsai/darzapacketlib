"""This module contains a class representing an BuyItem packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class BuyItemPacket(Packet):
    """Class representing an BuyItem packet."""

    packet_id = PACKET_NAME_TO_ID['BuyItem']

    def __init__(self):
        self.item_type: int = 0
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = BuyItemPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.item_type = reader.read_int16()

        return packet

    @classmethod
    def from_params(cls, item_type=0):
        packet = BuyItemPacket()
        packet.item_type = item_type

        writer = StreamWriter()
        writer.write_int16(item_type)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
