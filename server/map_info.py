"""This module contains a class representing an MapInfo packet."""

from darzapacketlib.packet import Packet
from darzapacketlib.packet_ids import PACKET_NAME_TO_ID
from darzapacketlib.stream_reader import StreamReader
from darzapacketlib.stream_writer import StreamWriter

class MapInfoPacket(Packet):
    """Class representing an MapInfo packet."""

    packet_id = PACKET_NAME_TO_ID['MapInfo']

    def __init__(self):
        self.name: str = ''
        self.width: int = 0
        self.height: int = 0
        self.player_id: int = 0
        self.can_teleport: bool = False
        self.show_ui: bool = False
        self.music: str = ''
        self.levels: str = ''
        self.quote: str = ''
        self.show_world_display: bool = False
        self.difficulty: int = 0
        self.image: str = ''
        self.ambient_light: int = 0
        self.space: bool = False
        self.game_time: float = 0.0
        self.day_night_cycle: bool = False
        self.force_angle: float = 0.0
        self.light_influence: float = 0.0
        self.packet_bytes: bytes = bytes()

    @classmethod
    def from_bytes(cls, raw_bytes):
        packet = MapInfoPacket()

        reader = StreamReader(raw_bytes)

        reader.read_int()
        assert reader.read_char() == packet.packet_id

        packet.packet_bytes = raw_bytes[reader.reader_index:]

        packet.name = reader.read_int8_string()
        packet.width = reader.read_varint()
        packet.height = reader.read_varint()
        packet.player_id = reader.read_varint()
        packet.can_teleport = reader.read_bool()
        packet.show_ui = reader.read_bool()
        packet.music = reader.read_int8_string()
        packet.levels = reader.read_int8_string()
        packet.quote = reader.read_int8_string()
        packet.show_world_display = reader.read_bool()
        packet.difficulty = reader.read_char()
        packet.image = reader.read_int8_string()
        packet.ambient_light = reader.read_varint()
        packet.space = reader.read_bool()
        packet.game_time = reader.read_float()
        packet.day_night_cycle = reader.read_bool()
        packet.force_angle = reader.read_float()
        packet.light_influence = reader.read_float()

        return packet

    @classmethod
    def from_params(
        cls,
        name='', width=0, height=0, player_id=0, can_teleport=False, show_ui=False, music='',
        levels='', quote='', show_world_display=False, difficulty=0, image='', ambient_light=0,
        space=False, game_time=0.0, day_night_cycle=False, force_angle=0.0, light_influence=0.0
    ):
        packet = MapInfoPacket()
        packet.name = name
        packet.width = width
        packet.height = height
        packet.player_id = player_id
        packet.can_teleport = can_teleport
        packet.show_ui = show_ui
        packet.music = music
        packet.levels = levels
        packet.quote = quote
        packet.show_world_display = show_world_display
        packet.difficulty = difficulty
        packet.image = image
        packet.ambient_light = ambient_light
        packet.space = space
        packet.game_time = game_time
        packet.day_night_cycle = day_night_cycle
        packet.force_angle = force_angle
        packet.light_influence = light_influence

        writer = StreamWriter()
        writer.write_int8_string(name)
        writer.write_varint(width)
        writer.write_varint(height)
        writer.write_varint(player_id)
        writer.write_byte(can_teleport)
        writer.write_byte(show_ui)
        writer.write_int8_string(music)
        writer.write_int8_string(levels)
        writer.write_int8_string(quote)
        writer.write_byte(show_world_display)
        writer.write_byte(difficulty)
        writer.write_int8_string(image)
        writer.write_varint(ambient_light)
        writer.write_byte(space)
        writer.write_byte(game_time)
        writer.write_byte(day_night_cycle)
        writer.write_byte(force_angle)
        writer.write_byte(light_influence)
        packet.packet_bytes = writer.raw_bytes

        return packet

    def to_raw_bytes(self):
        writer = StreamWriter()
        writer.write_int(len(self.packet_bytes) + 1)
        writer.write_byte(self.packet_id)
        writer.write_data(self.packet_bytes)
        return writer.raw_bytes
