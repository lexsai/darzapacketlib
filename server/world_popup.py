"""This module contains a class representing an WorldPopup packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class WorldPopupPacket(Packet):
    """Class representing an WorldPopup packet."""

    packet_id = PACKET_NAME_TO_ID['WorldPopup']

    def __init__(self):
        self.world_popup_name: str = ''
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = WorldPopupPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.world_popup_name = reader.read_int8_string()

        return packet

    @classmethod
    def from_params(cls, world_popup_name=''):
        packet = WorldPopupPacket()
        packet.world_popup_name = world_popup_name

        writer = StreamWriter()
        writer.write_int8_string(world_popup_name)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
