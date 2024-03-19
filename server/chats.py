"""This module contains a class representing an Chats packet."""

from packets.packet import Packet
from packets.packet_ids import PACKET_NAME_TO_ID
from packets.packet_types import ChatItem, Color
from packets.stream_reader import StreamReader
from packets.stream_writer import StreamWriter

class ChatsPacket(Packet):
    """Class representing an Chats packet."""

    packet_id = PACKET_NAME_TO_ID['Chats']

    def __init__(self):
        self.chat_items: list[ChatItem] = []
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = ChatsPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        num_chat_items = reader.read_varint()
        for _ in range(num_chat_items):
            color = reader.read_color()
            owner_id = reader.read_varint()
            text = reader.read_int8_string()
            icon = reader.read_int8_string()
            packet.chat_items.append(ChatItem(color, owner_id, text, icon))

        return packet

    @classmethod
    def from_params(cls, chat_items: list[ChatItem]=None):
        packet = ChatsPacket()
        packet.chat_items = chat_items

        writer = StreamWriter()
        writer.write_varint(len(chat_items))
        for item in chat_items:
            writer.write_color(item.color)
            writer.write_varint(item.owner_id)
            writer.write_int8_string(item.text)
            writer.write_int8_string(item.icon)

        packet.packet_bytes = writer.raw_bytes

        return packet

    @classmethod
    def from_msg(cls, text: str, color: Color):
        """A simplified set of parameters to build a ChatsPacket from."""

        packet = ChatsPacket()
        packet.chat_items = [ChatItem(color, -1, text, '')]

        writer = StreamWriter()
        writer.write_varint(1)
        writer.write_color(color)
        writer.write_varint(-1)
        writer.write_int8_string(text)
        writer.write_int8_string('')

        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
